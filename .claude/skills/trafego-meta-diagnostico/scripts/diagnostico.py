#!/usr/bin/env python3
"""
trafego-meta-diagnostico — diagnostico de Meta Ads via V4mos API.

Pre-requisitos: variaveis de ambiente
  V4MOS_CLIENT_ID, V4MOS_CLIENT_SECRET, V4MOS_WORKSPACE_ID

Uso:
  python3 diagnostico.py [--dias N] [--ate YYYY-MM-DD] [--account-id ACT_ID] [--out path.md]

Default: ultimos 7 dias ate ontem, todas as contas do workspace, salva em cwd.

Por que ontem e nao hoje: V4mos sincroniza 1x/dia de madrugada (SP tz) e dados
de midia tem D-3 de latencia do proprio Facebook. Hoje sempre esta incompleto.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
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

BR_MONEY = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
BR_INT = lambda v: f"{int(v):,}".replace(",", ".")
PCT = lambda v: f"{v*100:.2f}%".replace(".", ",")


def require_env() -> dict[str, str]:
    required = ["V4MOS_CLIENT_ID", "V4MOS_CLIENT_SECRET", "V4MOS_WORKSPACE_ID"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERRO: variaveis de ambiente faltando: {', '.join(missing)}", file=sys.stderr)
        print("Adicione no seu ~/.zshrc:", file=sys.stderr)
        for k in missing:
            print(f'  export {k}="..."', file=sys.stderr)
        sys.exit(2)
    return {k: os.environ[k] for k in required}


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
    creds = require_env()

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
