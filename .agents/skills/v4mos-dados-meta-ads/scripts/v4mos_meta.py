#!/usr/bin/env python3
"""
v4mos-dados-meta-ads — puxador generico de dados Meta Ads via V4mos API.

Uso:
  python3 v4mos_meta.py <endpoint> [flags]

Onde <endpoint> e um path V4mos (ex: /v1/facebook/ads/ad) ou um alias
curto: ad, adset, campaigns, creatives, accounts, platform, region,
demographic, actions.

Credenciais: ver `squads/<squad>/clientes/<cliente>/.env` (auto-detect
do cwd ou via --squad/--cliente) + env vars do shell. Falta algo e stdin
e TTY? Pergunta e salva no .env existente do cliente. Sem TTY? Exit 2.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://api.data.v4.marketing"
RATE_SLEEP = 2.0
TIMEOUT = 45
V4MOS_KEYS_URL = "https://v4marketing.mktlab.app/configuracoes/api-dados"

# Aliases curtos → paths completos
ENDPOINT_ALIASES = {
    "accounts": "/v1/facebook/accounts",
    "campaigns": "/v1/facebook/ads/campaigns",
    "adset": "/v1/facebook/ads/adset",
    "adsets": "/v1/facebook/ads/adset",
    "ad": "/v1/facebook/ads/ad",
    "ads": "/v1/facebook/ads/ad",
    "creatives": "/v1/facebook/ads/creatives",
    "actions": "/v1/facebook/ads/actions",
    "demographic": "/v1/facebook/ads/demographic",
    "platform": "/v1/facebook/ads/platform",
    "region": "/v1/facebook/ads/region",
}


# ──────────── .env + creds (herdado da v1.2.0) ────────────


def load_dotenv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if (val.startswith('"') and val.endswith('"')) or (
            val.startswith("'") and val.endswith("'")
        ):
            val = val[1:-1]
        if val:
            out[key] = val
    return out


def find_hub_root(start: Path | None = None) -> Path | None:
    """Encontra a raiz do hub sem depender do nome do diretorio."""
    start = (start or Path.cwd()).resolve()
    for candidate in [start, *start.parents]:
        if (candidate / "squads").is_dir() and (
            (candidate / "AGENTS.md").is_file()
            or (candidate / ".claude" / "skills").is_dir()
        ):
            return candidate
    return None


def find_client_env(
    cliente: str | None,
    squad: str | None = None,
    start: Path | None = None,
) -> tuple[Path | None, str | None]:
    cwd = (start or Path.cwd()).resolve()
    if cliente:
        hub_root = find_hub_root(cwd)
        if not hub_root:
            return None, cliente
        if squad:
            client_dir = hub_root / "squads" / squad / "clientes" / cliente
            return (
                (client_dir / ".env", cliente)
                if client_dir.is_dir()
                else (None, cliente)
            )
        matches = sorted(
            path
            for path in (hub_root / "squads").glob(f"*/clientes/{cliente}")
            if path.is_dir()
        )
        if len(matches) > 1:
            squads = ", ".join(path.parents[1].name for path in matches)
            raise ValueError(
                f"cliente {cliente!r} existe em mais de um squad ({squads}); use --squad"
            )
        if matches:
            return matches[0] / ".env", cliente
        return None, cliente

    parts = cwd.parts
    for i in range(len(parts) - 3):
        if parts[i] == "squads" and parts[i + 2] == "clientes":
            nome = parts[i + 3]
            client_dir = Path(*parts[: i + 4])
            if client_dir.is_dir():
                return client_dir / ".env", nome
    return None, None


def require_creds(
    cliente: str | None, squad: str | None = None
) -> tuple[dict[str, str], str | None]:
    required = ["V4MOS_CLIENT_ID", "V4MOS_CLIENT_SECRET", "V4MOS_WORKSPACE_ID"]
    try:
        env_path, detected = find_client_env(cliente, squad)
    except ValueError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        sys.exit(2)
    file_vars = load_dotenv(env_path) if env_path else {}
    shell_vars = {k: os.environ.get(k, "") for k in required}
    creds = {}
    for k in required:
        if k == "V4MOS_WORKSPACE_ID":
            creds[k] = file_vars.get(k) or shell_vars.get(k) or ""
        else:
            creds[k] = shell_vars.get(k) or file_vars.get(k) or ""

    missing = [k for k in required if not creds[k]]
    if missing and sys.stdin.isatty() and sys.stderr.isatty():
        creds, env_path = prompt_and_save(env_path, creds, missing)
        missing = [k for k in required if not creds[k]]

    if missing:
        print(f"✗ Credenciais V4mos faltando: {', '.join(missing)}", file=sys.stderr)
        print(file=sys.stderr)
        if env_path:
            print(f"  .env do cliente: {env_path}", file=sys.stderr)
        elif cliente:
            target = (
                f"squads/{squad}/clientes/{cliente}/.env"
                if squad
                else f"squads/<squad>/clientes/{cliente}/.env"
            )
            print(f"  Cliente não encontrado em: {target}", file=sys.stderr)
        else:
            print(
                "  Pasta de cliente não identificada. Use --squad e --cliente, ou entre na KB.",
                file=sys.stderr,
            )
        print(
            "  Crie a KB com /novo-cliente antes de salvar credenciais.",
            file=sys.stderr,
        )
        print(file=sys.stderr)
        print(f"  Onde pegar: {V4MOS_KEYS_URL}", file=sys.stderr)
        sys.exit(2)

    return creds, detected


def prompt_and_save(env_path, creds, missing):
    if env_path is None:
        return creds, env_path

    labels = {
        "V4MOS_CLIENT_ID": "Client ID (uuid)",
        "V4MOS_CLIENT_SECRET": "Client Secret (hex)",
        "V4MOS_WORKSPACE_ID": "Workspace ID do cliente (uuid)",
    }
    print(f"\n▶ Faltam credenciais. Vou salvar em: {env_path}", file=sys.stderr)
    print(f"  Onde pegar: {V4MOS_KEYS_URL}\n", file=sys.stderr)
    for key in missing:
        while True:
            try:
                val = input(f"  {labels.get(key, key)}: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n✗ Cancelado.", file=sys.stderr)
                sys.exit(130)
            if val:
                creds[key] = val
                break
            print("  (valor vazio — tenta de novo, Ctrl+C cancela)", file=sys.stderr)

    existing = (
        env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    )
    new_lines, seen = [], set()
    for line in existing:
        m = re.match(r"^([A-Z_][A-Z0-9_]*)\s*=", line.strip())
        if m and m.group(1) in creds and creds[m.group(1)]:
            new_lines.append(f"{m.group(1)}={creds[m.group(1)]}")
            seen.add(m.group(1))
        else:
            new_lines.append(line)
    for key in ["V4MOS_CLIENT_ID", "V4MOS_CLIENT_SECRET", "V4MOS_WORKSPACE_ID"]:
        if key not in seen and creds.get(key):
            new_lines.append(f"{key}={creds[key]}")
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    env_path.chmod(0o600)
    print(f"\n✓ Credenciais salvas em {env_path}\n", file=sys.stderr)
    return creds, env_path


# ──────────── V4mos client (paginacao + rate limit) ────────────


class V4mos:
    def __init__(self, creds: dict[str, str]):
        if requests is None:
            raise RuntimeError(
                "dependência ausente: rode python3 -m pip install -r requirements.txt"
            )
        self.headers = {
            "x-client-id": creds["V4MOS_CLIENT_ID"],
            "x-client-secret": creds["V4MOS_CLIENT_SECRET"],
            "User-Agent": "v4mos-dados-meta-ads/2.1",
        }
        self.workspace_id = creds["V4MOS_WORKSPACE_ID"]
        self.last_call = 0.0

    def get(self, path: str, max_rows: int | None = None, **params) -> list[dict]:
        params.setdefault("workspaceId", self.workspace_id)
        params.setdefault("limit", 5000)
        rows: list[dict] = []
        page = 1
        while True:
            elapsed = time.time() - self.last_call
            if elapsed < RATE_SLEEP:
                time.sleep(RATE_SLEEP - elapsed)
            params["page"] = page
            for attempt in range(3):
                self.last_call = time.time()
                r = requests.get(
                    f"{BASE_URL}{path}",
                    headers=self.headers,
                    params=params,
                    timeout=TIMEOUT,
                )
                if r.status_code in {429, 500, 502, 503, 504}:
                    try:
                        retry_after = float(r.headers.get("Retry-After", 2**attempt))
                    except (TypeError, ValueError):
                        retry_after = float(2**attempt)
                    time.sleep(retry_after)
                    continue
                r.raise_for_status()
                payload = r.json()
                rows.extend(payload.get("data") or [])
                if max_rows and len(rows) >= max_rows:
                    return rows[:max_rows]
                meta = payload.get("meta") or {}
                if not meta.get("hasNextPage"):
                    return rows
                page += 1
                break
            else:
                raise RuntimeError(
                    f"{path}: falhou após 3 tentativas em erro transitório"
                )
        return rows


# ──────────── Filtros client-side ────────────

WHERE_RE = re.compile(r"^([a-zA-Z_][\w.]*)\s*(>=|<=|!=|=|<|>|~|\^)\s*(.+)$")


def parse_where(expr: str) -> Callable[[dict], bool]:
    m = WHERE_RE.match(expr.strip())
    if not m:
        raise ValueError(f"filtro invalido: {expr!r} (use field OP value)")
    field, op, val = m.group(1), m.group(2), m.group(3).strip()
    # strip aspas
    if (val.startswith('"') and val.endswith('"')) or (
        val.startswith("'") and val.endswith("'")
    ):
        val = val[1:-1]

    def pred(row: dict) -> bool:
        got = row.get(field)
        if got is None:
            return False
        if op in {">", "<", ">=", "<="}:
            try:
                g = float(got)
                v = float(val)
            except (TypeError, ValueError):
                return False
            return {">": g > v, "<": g < v, ">=": g >= v, "<=": g <= v}[op]
        got_s = str(got)
        if op == "=":
            return got_s == val
        if op == "!=":
            return got_s != val
        if op == "~":
            return val.lower() in got_s.lower()
        if op == "^":
            return got_s.lower().startswith(val.lower())
        return False

    pred.__doc__ = f"{field} {op} {val}"
    return pred


def apply_wheres(rows: list[dict], preds: list[Callable[[dict], bool]]) -> list[dict]:
    if not preds:
        return rows
    return [r for r in rows if all(p(r) for p in preds)]


# ──────────── Enriquecimento (CTR recalc) ────────────


def enrich(rows: list[dict]) -> list[dict]:
    """Recalcula CTR quando impressions/clicks disponiveis (API vem quebrado)."""
    for r in rows:
        if "clicks" in r and "impressions" in r:
            imp = r.get("impressions")
            clk = r.get("clicks")
            try:
                imp_f = float(imp or 0)
                clk_f = float(clk or 0)
                r["ctr_calc"] = (clk_f / imp_f) if imp_f > 0 else 0.0
            except (TypeError, ValueError):
                r["ctr_calc"] = None
    return rows


# ──────────── Ordenacao + fields ────────────


def sort_rows(rows: list[dict], order_by: str | None, order_dir: str) -> list[dict]:
    if not order_by:
        return rows
    reverse = order_dir.upper() == "DESC"

    def key(r):
        v = r.get(order_by)
        try:
            return (0, float(v))
        except (TypeError, ValueError):
            return (1, str(v).casefold())

    present = [row for row in rows if row.get(order_by) is not None]
    missing = [row for row in rows if row.get(order_by) is None]
    return sorted(present, key=key, reverse=reverse) + missing


def select_fields(rows: list[dict], fields: list[str] | None) -> list[dict]:
    if not fields:
        return rows
    return [{k: r.get(k) for k in fields} for r in rows]


# ──────────── Renderers ────────────


def render_json(rows: list[dict]) -> str:
    return json.dumps(rows, ensure_ascii=False, indent=2, default=str)


def render_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    cols = list(rows[0].keys())
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
    w.writeheader()

    def safe_cell(value):
        if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + value
        return value

    for r in rows:
        w.writerow({c: safe_cell(r.get(c, "")) for c in cols})
    return buf.getvalue()


def render_table(rows: list[dict], max_width: int = 40) -> str:
    if not rows:
        return "(sem dados)"
    cols = list(rows[0].keys())
    widths = {c: len(c) for c in cols}
    str_rows = []
    for r in rows:
        sr = {}
        for c in cols:
            v = str(r.get(c, "") if r.get(c) is not None else "")
            if len(v) > max_width:
                v = v[: max_width - 1] + "…"
            sr[c] = v
            widths[c] = max(widths[c], len(v))
        str_rows.append(sr)
    sep = "─" * (sum(widths.values()) + 3 * len(cols) + 1)
    out = [sep]
    out.append("│ " + " │ ".join(c.ljust(widths[c]) for c in cols) + " │")
    out.append(sep)
    for sr in str_rows:
        out.append("│ " + " │ ".join(sr[c].ljust(widths[c]) for c in cols) + " │")
    out.append(sep)
    return "\n".join(out)


def render_md(rows: list[dict]) -> str:
    if not rows:
        return "_(sem dados)_"
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        vals = []
        for c in cols:
            v = r.get(c)
            s = "" if v is None else str(v).replace("|", "\\|").replace("\n", " ")
            vals.append(s)
        out.append("| " + " | ".join(vals) + " |")
    return "\n".join(out)


RENDERERS = {
    "json": render_json,
    "csv": render_csv,
    "table": render_table,
    "md": render_md,
}


# ──────────── CLI ────────────


def parse_args():
    p = argparse.ArgumentParser(description="V4mos Meta Ads — data puller generico")
    p.add_argument(
        "endpoint", help="Path V4mos ou alias (ad, campaigns, platform, ...)"
    )
    p.add_argument("--cliente", default=None)
    p.add_argument(
        "--squad",
        default=None,
        help="squad da KB; evita ambiguidade entre clientes homônimos",
    )

    p.add_argument(
        "--days", type=int, default=None, help="Janela em dias terminando ontem"
    )
    p.add_argument("--since", default=None, help="dateStart YYYY-MM-DD")
    p.add_argument("--until", default=None, help="dateEnd YYYY-MM-DD")

    p.add_argument("--account", default=None, help="account_id FB (ex: act_XXX)")
    p.add_argument("--order-by", default=None)
    p.add_argument(
        "--order-dir", default="DESC", choices=["ASC", "DESC", "asc", "desc"]
    )
    p.add_argument(
        "--limit", type=int, default=500, help="rows por pagina da API (max 5000)"
    )
    p.add_argument("--max", type=int, default=None, help="total cap apos paginacao")
    p.add_argument("--fields", default=None, help="CSV de colunas pra manter")
    p.add_argument(
        "--where",
        action="append",
        default=[],
        help="filtro client-side (pode repetir, AND)",
    )

    p.add_argument("--format", default=None, choices=["json", "csv", "table", "md"])
    p.add_argument("--out", default=None)
    return p.parse_args()


def resolve_endpoint(x: str) -> str:
    if x.startswith("/"):
        return x
    return ENDPOINT_ALIASES.get(x, f"/v1/facebook/ads/{x}")


def validate_args(args) -> None:
    if args.days is not None and args.days < 1:
        raise SystemExit("ERRO: --days deve ser maior que zero")
    if args.days is not None and args.since:
        raise SystemExit("ERRO: use --days ou --since, não os dois")
    if not 1 <= args.limit <= 5000:
        raise SystemExit("ERRO: --limit deve estar entre 1 e 5000")
    if args.max is not None and args.max < 1:
        raise SystemExit("ERRO: --max deve ser maior que zero")
    parsed_dates: dict[str, dt.date] = {}
    for field in ("since", "until"):
        value = getattr(args, field)
        if not value:
            continue
        try:
            parsed_dates[field] = dt.date.fromisoformat(value)
        except ValueError as exc:
            raise SystemExit(f"ERRO: --{field} deve usar YYYY-MM-DD") from exc
    if (
        parsed_dates.get("since")
        and parsed_dates.get("until")
        and parsed_dates["since"] > parsed_dates["until"]
    ):
        raise SystemExit("ERRO: --since não pode ser posterior a --until")


def main():
    args = parse_args()
    validate_args(args)
    creds, cliente = require_creds(args.cliente, args.squad)
    if cliente:
        print(f"▶ Cliente: {cliente}", file=sys.stderr)

    endpoint = resolve_endpoint(args.endpoint)
    print(f"▶ Endpoint: {endpoint}", file=sys.stderr)

    # Resolver datas
    params: dict[str, Any] = {}
    if args.since:
        params["dateStart"] = args.since
    if args.until:
        params["dateEnd"] = args.until
    if args.days:
        end = (
            dt.date.fromisoformat(args.until)
            if args.until
            else dt.datetime.now().astimezone().date() - dt.timedelta(days=1)
        )
        start = end - dt.timedelta(days=args.days - 1)
        params["dateStart"] = start.isoformat()
        params["dateEnd"] = end.isoformat()
        print(
            f"▶ Periodo: {params['dateStart']} a {params['dateEnd']} ({args.days} dias)",
            file=sys.stderr,
        )

    if args.account:
        params["account_id"] = args.account
    if args.order_by:
        params["orderBy"] = args.order_by
        params["orderDirection"] = args.order_dir.upper()
    if args.limit:
        params["limit"] = args.limit

    # Parse wheres antes do fetch (falha rapido)
    preds = [parse_where(w) for w in args.where]

    # Fetch
    v4 = V4mos(creds)
    rows = v4.get(endpoint, max_rows=args.max, **params)
    print(f"  → {len(rows)} rows brutas", file=sys.stderr)

    # Pipeline: enrich -> where -> sort (client-side fallback) -> fields
    rows = enrich(rows)
    rows = apply_wheres(rows, preds)
    if args.where:
        print(f"  → {len(rows)} rows apos filtros", file=sys.stderr)

    # Se a API nao honrou orderBy (ex: endpoints Google), resort client-side
    if args.order_by:
        rows = sort_rows(rows, args.order_by, args.order_dir)
    if args.max and len(rows) > args.max:
        rows = rows[: args.max]

    fields = [f.strip() for f in args.fields.split(",")] if args.fields else None
    rows = select_fields(rows, fields)

    # Format detection
    fmt = args.format
    if not fmt:
        if args.out:
            suffix = Path(args.out).suffix.lower()
            fmt = {".csv": "csv", ".json": "json", ".md": "md"}.get(suffix, "json")
        else:
            fmt = "table" if sys.stdout.isatty() else "json"

    output = RENDERERS[fmt](rows)

    if args.out:
        output_path = Path(args.out)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(f"✓ {len(rows)} rows em {args.out} ({fmt})", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
