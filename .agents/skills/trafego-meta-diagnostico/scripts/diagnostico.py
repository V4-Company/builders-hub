#!/usr/bin/env python3
"""
trafego-meta-diagnostico — diagnostico de Meta Ads via V4mos API.

Credenciais sao lidas em ordem de prioridade:
  1. --cliente <nome>  -> le clientes/<nome>/.env
  2. cwd dentro de clientes/<X>/ ou bases/<X>/ -> le <X>/.env
  3. variaveis de ambiente do shell (V4MOS_CLIENT_ID, V4MOS_CLIENT_SECRET, V4MOS_WORKSPACE_ID)

Se faltar alguma credencial, o script sai com exit=2 e orienta onde pegar
(https://app.v4mkt.com/... ou matheus.netto@v4company.com).

Uso:
  python3 diagnostico.py [--cliente NOME] [--dias N] [--ate YYYY-MM-DD]
                         [--account-id ACT_ID] [--out path.md]

Default: ultimos 7 dias ate ontem, todas as contas do workspace, salva em cwd.

Por que ontem e nao hoje: V4mos sincroniza 1x/dia de madrugada (SP tz) e dados
de midia tem D-3 de latencia do proprio Facebook. Hoje sempre esta incompleto.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("ERRO: pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.data.v4.marketing"
RATE_SLEEP = 2.0  # segundos entre chamadas (conservador — 30 req/min)
TIMEOUT = 45

V4MOS_KEYS_URL = "https://v4marketing.mktlab.app/configuracoes/api-dados"

BR_MONEY = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
BR_INT = lambda v: f"{int(v):,}".replace(",", ".")
PCT = lambda v: f"{v*100:.2f}%".replace(".", ",")


def load_dotenv(path: Path) -> dict[str, str]:
    """Parser minimal de .env (KEY=VALUE por linha, ignora # e linhas vazias)."""
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$', line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        # strip matching quotes
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        if val:  # so grava se nao vazio
            out[key] = val
    return out


def find_client_env(cliente: str | None) -> tuple[Path | None, str | None]:
    """
    Resolve o .env do cliente. Busca em:
    - builders_hub/clientes/<cliente>/.env (se --cliente passado)
    - cwd e ancestors ate achar clientes/<X>/.env ou bases/<X>/.env

    Retorna (path_do_env_ou_None, nome_do_cliente_ou_None).
    """
    cwd = Path.cwd().resolve()

    # Caso 1: --cliente explicito. Procura em cwd e ancestors por clientes/<cliente>
    if cliente:
        cand = cwd / "clientes" / cliente / ".env"
        if cand.is_file():
            return cand, cliente
        # sobe ancestors
        for parent in cwd.parents:
            cand = parent / "clientes" / cliente / ".env"
            if cand.is_file():
                return cand, cliente
        return None, cliente  # pediu cliente mas nao achou

    # Caso 2: cwd esta dentro de clientes/<X>/ ou bases/<X>/
    parts = cwd.parts
    for i, part in enumerate(parts):
        if part in ("clientes", "bases") and i + 1 < len(parts):
            nome = parts[i + 1]
            if nome == "_template":
                continue
            base = Path(*parts[: i + 2])
            env_path = base / ".env"
            if env_path.is_file():
                return env_path, nome
    return None, None


def require_creds(cliente: str | None) -> tuple[dict[str, str], str | None]:
    """
    Retorna (creds, cliente_detectado). Estrategia:
      1. Procura .env do cliente
      2. Mistura com env vars do shell (shell vence se tiver)
    """
    required = ["V4MOS_CLIENT_ID", "V4MOS_CLIENT_SECRET", "V4MOS_WORKSPACE_ID"]
    env_path, detected = find_client_env(cliente)
    file_vars = load_dotenv(env_path) if env_path else {}
    shell_vars = {k: os.environ.get(k, "") for k in required}
    # shell tem prioridade pra CLIENT_ID/SECRET (sao globais do V4er), arquivo pra WORKSPACE_ID
    creds = {}
    for k in required:
        if k == "V4MOS_WORKSPACE_ID":
            # priorizar .env do cliente (workspace e por cliente)
            creds[k] = file_vars.get(k) or shell_vars.get(k) or ""
        else:
            creds[k] = shell_vars.get(k) or file_vars.get(k) or ""

    missing = [k for k in required if not creds[k]]
    if missing:
        # Modo interativo (usuario rodando direto no terminal): pergunta e salva no .env
        if sys.stdin.isatty() and sys.stderr.isatty():
            creds, env_path = prompt_and_save(cliente, detected, env_path, creds, missing)
            missing = [k for k in required if not creds[k]]

    if missing:
        print(f"✗ Credenciais V4mos faltando: {', '.join(missing)}", file=sys.stderr)
        print("", file=sys.stderr)
        if env_path:
            print(f"  .env do cliente: {env_path}", file=sys.stderr)
        elif cliente:
            print(f"  Esperado em: clientes/{cliente}/.env", file=sys.stderr)
        else:
            print("  Pasta de cliente nao identificada. Use --cliente <nome> ou cd na pasta.", file=sys.stderr)
        print("", file=sys.stderr)
        print(f"  Onde pegar as credenciais:", file=sys.stderr)
        print(f"    1. {V4MOS_KEYS_URL} (logado com sua conta V4)", file=sys.stderr)
        print(f"    2. Selecione o workspace do cliente", file=sys.stderr)
        print(f"    3. Settings > API / Integracoes > gerar client credentials", file=sys.stderr)
        sys.exit(2)

    return creds, detected


def prompt_and_save(cliente: str | None, detected: str | None, env_path: Path | None,
                    creds: dict[str, str], missing: list[str]) -> tuple[dict[str, str], Path | None]:
    """
    Pergunta ao usuario as chaves que faltam e salva no .env do cliente.
    So chamado se stdin e stderr sao TTYs (usuario rodou direto no terminal).
    """
    # Resolve o path do .env destino
    nome_cliente = cliente or detected
    if env_path is None and nome_cliente:
        # Acha raiz do builders-hub (procura clientes/ nos ancestors)
        cwd = Path.cwd().resolve()
        hub_root = None
        for p in [cwd, *cwd.parents]:
            if (p / "clientes").is_dir():
                hub_root = p
                break
        if hub_root:
            client_dir = hub_root / "clientes" / nome_cliente
            client_dir.mkdir(parents=True, exist_ok=True)
            env_path = client_dir / ".env"
            if not env_path.exists():
                template = hub_root / "clientes" / "_template" / ".env.example"
                if template.is_file():
                    env_path.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
                else:
                    env_path.write_text("# V4mos\nV4MOS_CLIENT_ID=\nV4MOS_CLIENT_SECRET=\nV4MOS_WORKSPACE_ID=\n", encoding="utf-8")
    if env_path is None:
        return creds, env_path  # nao da pra salvar, volta vazio

    labels = {
        "V4MOS_CLIENT_ID": "Client ID (uuid)",
        "V4MOS_CLIENT_SECRET": "Client Secret (hex)",
        "V4MOS_WORKSPACE_ID": "Workspace ID do cliente (uuid)",
    }

    print("", file=sys.stderr)
    print(f"▶ Faltam credenciais V4mos pra rodar. Vou perguntar e salvar em:", file=sys.stderr)
    print(f"  {env_path}", file=sys.stderr)
    print(f"  (onde pegar: {V4MOS_KEYS_URL} > workspace do cliente > Settings > API)", file=sys.stderr)
    print("", file=sys.stderr)

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
            print(f"  (valor vazio — tenta de novo, ou Ctrl+C pra cancelar)", file=sys.stderr)

    # Merge no .env existente (preserva comentarios e chaves ja preenchidas)
    existing_lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    new_lines = []
    seen = set()
    for line in existing_lines:
        m = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=', line.strip())
        if m and m.group(1) in creds and creds[m.group(1)]:
            new_lines.append(f"{m.group(1)}={creds[m.group(1)]}")
            seen.add(m.group(1))
        else:
            new_lines.append(line)
    # Adiciona chaves que nao estavam no arquivo
    for key in ["V4MOS_CLIENT_ID", "V4MOS_CLIENT_SECRET", "V4MOS_WORKSPACE_ID"]:
        if key not in seen and creds.get(key):
            new_lines.append(f"{key}={creds[key]}")
    env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    print("", file=sys.stderr)
    print(f"✓ Credenciais salvas em {env_path}", file=sys.stderr)
    print("", file=sys.stderr)

    return creds, env_path


class V4mos:
    def __init__(self, creds: dict[str, str]):
        self.headers = {
            "x-client-id": creds["V4MOS_CLIENT_ID"],
            "x-client-secret": creds["V4MOS_CLIENT_SECRET"],
            "User-Agent": "trafego-meta-diagnostico/1.0",
        }
        self.workspace_id = creds["V4MOS_WORKSPACE_ID"]
        self.last_call = 0.0

    def get(self, path: str, **params) -> list[dict]:
        """GET com paginacao automatica + rate limit + retry 429."""
        params.setdefault("workspaceId", self.workspace_id)
        params.setdefault("limit", 5000)
        all_rows: list[dict] = []
        page = 1
        while True:
            elapsed = time.time() - self.last_call
            if elapsed < RATE_SLEEP:
                time.sleep(RATE_SLEEP - elapsed)
            params["page"] = page
            for attempt in range(3):
                self.last_call = time.time()
                r = requests.get(f"{BASE_URL}{path}", headers=self.headers, params=params, timeout=TIMEOUT)
                if r.status_code == 429:
                    retry_after = float(r.headers.get("Retry-After", 2**attempt))
                    time.sleep(retry_after)
                    continue
                if r.status_code == 500:
                    # algum endpoint retorna 500 quando vazio — tratar como []
                    return all_rows
                r.raise_for_status()
                payload = r.json()
                rows = payload.get("data") or []
                all_rows.extend(rows)
                meta = payload.get("meta") or {}
                if not meta.get("hasNextPage"):
                    return all_rows
                page += 1
                break
            else:
                raise RuntimeError(f"{path}: 3x 429 consecutivos, desisto")
        return all_rows


def parse_args():
    p = argparse.ArgumentParser(description="Diagnostico Meta Ads V4mos")
    p.add_argument("--cliente", type=str, default=None,
                   help="Nome do cliente (pasta em clientes/<nome>). Auto-detecta se cwd estiver dentro.")
    p.add_argument("--dias", type=int, default=7, help="Janela em dias (default 7)")
    p.add_argument("--ate", type=str, default=None,
                   help="Data final YYYY-MM-DD (default ontem)")
    p.add_argument("--account-id", type=str, default=None,
                   help="Filtra por account_id especifico (ex: act_1206859723140742)")
    p.add_argument("--out", type=str, default=None,
                   help="Path de saida (default: meta-diagnostico-YYYY-MM-DD.md no cwd)")
    return p.parse_args()


def safe_num(v: Any) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def recalc_ctr(clicks: float, impressions: float) -> float:
    """CTR da API Facebook vem quebrado (>100%). Recalcular sempre."""
    return clicks / impressions if impressions > 0 else 0.0


def aggregate_by(rows: list[dict], group_key: str, metrics: list[str]) -> dict[str, dict]:
    """Agrega rows por group_key somando metrics."""
    agg: dict[str, dict] = defaultdict(lambda: {m: 0.0 for m in metrics})
    for r in rows:
        k = r.get(group_key) or "—"
        for m in metrics:
            agg[k][m] += safe_num(r.get(m))
    return dict(agg)


def fmt_quality(v: str | None) -> str:
    """Formata quality_ranking com icone. API retorna graduacoes finas:
    BELOW_AVERAGE_10, BELOW_AVERAGE_20, BELOW_AVERAGE_35 (pior tercil), AVERAGE, ABOVE_AVERAGE, UNKNOWN.
    """
    if not v:
        return "—"
    u = v.upper()
    if u.startswith("BELOW_AVERAGE"):
        return f"🔴 {v}"
    if u.startswith("ABOVE_AVERAGE"):
        return f"🟢 {v}"
    if u == "AVERAGE":
        return f"🟡 {v}"
    return f"⚪ {v}"


def is_below_avg(v: str | None) -> bool:
    return bool(v) and v.upper().startswith("BELOW_AVERAGE")


def build_report(data: dict) -> str:
    w = data["window"]
    a = data["accounts"]
    c_now = data["campaigns_now"]
    c_prev = data["campaigns_prev"]
    ads_now = data["ads_now"]
    platforms = data["platforms"]

    # Totais agregados
    def total(rows, fields):
        return {f: sum(safe_num(r.get(f)) for r in rows) for f in fields}

    now = total(c_now, ["spend", "impressions", "clicks", "reach"])
    prev = total(c_prev, ["spend", "impressions", "clicks", "reach"])
    now["ctr"] = recalc_ctr(now["clicks"], now["impressions"])
    prev["ctr"] = recalc_ctr(prev["clicks"], prev["impressions"])
    now["cpm"] = (now["spend"] / now["impressions"] * 1000) if now["impressions"] else 0
    now["cpc"] = (now["spend"] / now["clicks"]) if now["clicks"] else 0

    def delta(curr: float, prev_v: float) -> str:
        if prev_v == 0:
            return "—"
        pct = (curr - prev_v) / prev_v
        arrow = "↑" if pct > 0 else "↓" if pct < 0 else "→"
        return f"{arrow} {abs(pct)*100:.1f}%"

    # Top campanhas por spend
    camp_agg = aggregate_by(c_now, "campaign_name", ["spend", "impressions", "clicks"])
    top_spend = sorted(camp_agg.items(), key=lambda x: x[1]["spend"], reverse=True)[:5]

    # Ads com quality ruim (qualquer graduacao BELOW_AVERAGE_*)
    below_avg = [
        r for r in ads_now
        if is_below_avg(r.get("quality_ranking"))
        and safe_num(r.get("spend")) > 0
    ]
    below_avg.sort(key=lambda r: safe_num(r.get("spend")), reverse=True)
    below_avg_spend = sum(safe_num(r.get("spend")) for r in below_avg)

    # Ads com ROAS — topo
    ads_roas = [
        (r, safe_num(r.get("website_purchase_roas")))
        for r in ads_now
        if safe_num(r.get("website_purchase_roas")) > 0
    ]
    ads_roas.sort(key=lambda x: x[1], reverse=True)
    top_roas = ads_roas[:5]

    # Breakdown por plataforma
    plat_agg = aggregate_by(platforms, "publisher_platform", ["spend", "impressions", "clicks"])
    for k, v in plat_agg.items():
        v["cpm"] = (v["spend"] / v["impressions"] * 1000) if v["impressions"] else 0
        v["ctr"] = recalc_ctr(v["clicks"], v["impressions"])

    # Saldo
    saldo_info = ""
    for acc in a:
        balance = safe_num(acc.get("balance"))
        spent = safe_num(acc.get("amount_spent"))
        name = acc.get("name") or acc.get("account_id", "?")
        if balance > 0 and now["spend"] > 0:
            daily = now["spend"] / w["dias"]
            runway = balance / daily if daily else 0
            saldo_info += f"- **{name}**: {BR_MONEY(balance)} saldo · burn {BR_MONEY(daily)}/dia · **runway ~{runway:.0f} dias**\n"
        else:
            saldo_info += f"- **{name}**: saldo {BR_MONEY(balance)} · spent lifetime {BR_MONEY(spent)}\n"

    # Monta markdown
    out = []
    out.append(f"# Meta Ads — Diagnostico {w['dias']} dias")
    out.append("")
    out.append(f"**Periodo:** {w['start']} a {w['end']}")
    out.append(f"**Workspace:** `{data['workspace_id']}`")
    out.append(f"**Contas:** {len(a)}")
    out.append(f"**Gerado em:** {data['generated_at']}")
    out.append("")
    out.append("## KPIs do periodo")
    out.append("")
    out.append("| Metrica | Agora | Anterior | Delta |")
    out.append("|---|---:|---:|---:|")
    out.append(f"| Spend | {BR_MONEY(now['spend'])} | {BR_MONEY(prev['spend'])} | {delta(now['spend'], prev['spend'])} |")
    out.append(f"| Impressoes | {BR_INT(now['impressions'])} | {BR_INT(prev['impressions'])} | {delta(now['impressions'], prev['impressions'])} |")
    out.append(f"| Cliques | {BR_INT(now['clicks'])} | {BR_INT(prev['clicks'])} | {delta(now['clicks'], prev['clicks'])} |")
    out.append(f"| CTR | {PCT(now['ctr'])} | {PCT(prev['ctr'])} | — |")
    out.append(f"| CPM | {BR_MONEY(now['cpm'])} | — | — |")
    out.append(f"| CPC | {BR_MONEY(now['cpc'])} | — | — |")
    out.append("")

    if saldo_info:
        out.append("## Saldo e runway")
        out.append("")
        out.append(saldo_info)

    out.append("## Top 5 campanhas por spend")
    out.append("")
    out.append("| Campanha | Spend | Impressoes | CTR |")
    out.append("|---|---:|---:|---:|")
    for name, m in top_spend:
        ctr_c = recalc_ctr(m["clicks"], m["impressions"])
        out.append(f"| {name[:60]} | {BR_MONEY(m['spend'])} | {BR_INT(m['impressions'])} | {PCT(ctr_c)} |")
    out.append("")

    if top_roas:
        out.append("## Top 5 ads por ROAS")
        out.append("")
        out.append("| Ad | ROAS | Spend | Quality |")
        out.append("|---|---:|---:|---|")
        for ad, roas in top_roas:
            name = (ad.get("ad_name") or ad.get("ad_id") or "?")[:55]
            out.append(f"| {name} | {roas:.2f}x | {BR_MONEY(safe_num(ad.get('spend')))} | {fmt_quality(ad.get('quality_ranking'))} |")
        out.append("")

    if below_avg:
        out.append(f"## ⚠️ Ads com quality_ranking BELOW_AVERAGE")
        out.append("")
        out.append(f"**{len(below_avg)} ads queimando {BR_MONEY(below_avg_spend)}** no periodo. "
                   f"Revisao ou pausa imediata recomendada — esses ads estao abaixo da mediana do leilao e custando caro.")
        out.append("")
        out.append("| Ad | Spend | CTR | CPM | Engagement |")
        out.append("|---|---:|---:|---:|---|")
        for ad in below_avg[:10]:
            name = (ad.get("ad_name") or ad.get("ad_id") or "?")[:55]
            spend = safe_num(ad.get("spend"))
            ctr_c = recalc_ctr(safe_num(ad.get("clicks")), safe_num(ad.get("impressions")))
            cpm = (safe_num(ad.get("spend")) / safe_num(ad.get("impressions")) * 1000) if safe_num(ad.get("impressions")) else 0
            eng = fmt_quality(ad.get("engagement_rate_ranking"))
            out.append(f"| {name} | {BR_MONEY(spend)} | {PCT(ctr_c)} | {BR_MONEY(cpm)} | {eng} |")
        if len(below_avg) > 10:
            out.append(f"| _... + {len(below_avg)-10} ads_ | | | | |")
        out.append("")

    if plat_agg:
        out.append("## Breakdown por plataforma (Feed / Stories / Reels)")
        out.append("")
        out.append("| Plataforma | Spend | Impressoes | CPM | CTR |")
        out.append("|---|---:|---:|---:|---:|")
        for plat, m in sorted(plat_agg.items(), key=lambda x: x[1]["spend"], reverse=True):
            out.append(f"| {plat} | {BR_MONEY(m['spend'])} | {BR_INT(m['impressions'])} | {BR_MONEY(m['cpm'])} | {PCT(m['ctr'])} |")
        out.append("")

    out.append("---")
    out.append("")
    out.append("_Skill `trafego-meta-diagnostico` · Dados V4mos · CTR recalculado (`clicks/impressions`) porque o campo da API vem quebrado. Google Ads fora desse relatorio — API V4mos ignora filtro de data no Google._")

    return "\n".join(out)


def main():
    args = parse_args()
    creds, cliente = require_creds(args.cliente)
    if cliente:
        print(f"▶ Cliente: {cliente}", file=sys.stderr)

    # Janela: termina ontem (dados de hoje sempre incompletos) ou na data informada
    end = dt.date.fromisoformat(args.ate) if args.ate else dt.date.today() - dt.timedelta(days=1)
    start = end - dt.timedelta(days=args.dias - 1)
    prev_end = start - dt.timedelta(days=1)
    prev_start = prev_end - dt.timedelta(days=args.dias - 1)

    print(f"▶ Periodo: {start} a {end} ({args.dias} dias)", file=sys.stderr)
    print(f"▶ Periodo anterior: {prev_start} a {prev_end}", file=sys.stderr)

    v4 = V4mos(creds)
    common = {"dateStart": start.isoformat(), "dateEnd": end.isoformat()}
    common_prev = {"dateStart": prev_start.isoformat(), "dateEnd": prev_end.isoformat()}
    if args.account_id:
        common["account_id"] = args.account_id
        common_prev["account_id"] = args.account_id

    print("▶ fetching /v1/facebook/accounts", file=sys.stderr)
    accounts = v4.get("/v1/facebook/accounts")
    if args.account_id:
        accounts = [a for a in accounts if a.get("account_id") == args.account_id.replace("act_", "")]

    print("▶ fetching /v1/facebook/ads/campaigns (agora)", file=sys.stderr)
    campaigns_now = v4.get("/v1/facebook/ads/campaigns", **common)
    print(f"  → {len(campaigns_now)} rows", file=sys.stderr)

    print("▶ fetching /v1/facebook/ads/campaigns (anterior)", file=sys.stderr)
    campaigns_prev = v4.get("/v1/facebook/ads/campaigns", **common_prev)
    print(f"  → {len(campaigns_prev)} rows", file=sys.stderr)

    print("▶ fetching /v1/facebook/ads/ad (agora)", file=sys.stderr)
    ads_now = v4.get("/v1/facebook/ads/ad", **common)
    print(f"  → {len(ads_now)} rows", file=sys.stderr)

    print("▶ fetching /v1/facebook/ads/platform (agora)", file=sys.stderr)
    platforms = v4.get("/v1/facebook/ads/platform", **common)
    print(f"  → {len(platforms)} rows", file=sys.stderr)

    data = {
        "workspace_id": creds["V4MOS_WORKSPACE_ID"],
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "window": {"start": start.isoformat(), "end": end.isoformat(), "dias": args.dias},
        "accounts": accounts,
        "campaigns_now": campaigns_now,
        "campaigns_prev": campaigns_prev,
        "ads_now": ads_now,
        "platforms": platforms,
    }

    md = build_report(data)
    out_path = Path(args.out) if args.out else Path(f"meta-diagnostico-{end.isoformat()}.md")
    out_path.write_text(md, encoding="utf-8")
    print(f"✓ relatorio salvo em {out_path}", file=sys.stderr)
    print(md)


if __name__ == "__main__":
    main()
