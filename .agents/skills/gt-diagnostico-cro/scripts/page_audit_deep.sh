#!/bin/bash
# page_audit_deep.sh — Orquestra a auditoria PROFUNDA de uma URL (Playwright).
# Complementa page_audit.sh (PSI + on-page estatico) com:
#   - Tracking stack (GTM, GA4, Meta Pixel, Clarity, etc.)
#   - Eventos disparados (GA4 + Meta Pixel capturados via network)
#   - dataLayer dump
#   - CRO elements (CTAs, forms, WhatsApp, prova social)
#   - Compliance LGPD (pre-consent tracker detection)
#   - Quality flags (UA legacy, pixel duplicado, etc.)
#
# Uso:  page_audit_deep.sh <client_dir> <url>
# Ex:   page_audit_deep.sh squads/{squad}/clientes/{cliente} https://www.site-do-cliente.com.br
#
# Le:    <client_dir>/client.json
# Grava: <client_dir>/cache/page_audit_deep-<timestamp>.json (raw)
#        <client_dir>/client.json (campo page_audit_deep com resumo)

set -euo pipefail

CLIENT_DIR="${1:?Uso: page_audit_deep.sh <client_dir> <url>}"
URL="${2:?Uso: page_audit_deep.sh <client_dir> <url>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/page_audit_deep.py"

if [ ! -f "$PY_SCRIPT" ]; then
  echo "ERROR: page_audit_deep.py nao encontrado em $PY_SCRIPT" >&2
  exit 1
fi

# Cache dir
mkdir -p "$CLIENT_DIR/cache"
TS=$(date -u +%Y%m%d-%H%M%S)
RAW_OUT="$CLIENT_DIR/cache/page_audit_deep-$TS.json"

echo ">> Deep audit (Playwright: 3 passes — desktop full, mobile full, compliance pre-consent)..."
python3 "$PY_SCRIPT" "$URL" "$RAW_OUT"

# O Builders Hub não exige client.json. Quando ele não existe, preserve o
# cache bruto e deixe a skill interpretar os dados junto com a KB do cliente.
if [ ! -f "$CLIENT_DIR/client.json" ]; then
  echo "[OK] Auditoria profunda bruta concluída; client.json ausente, merge ignorado."
  echo "Cache raw: $RAW_OUT"
  exit 0
fi

# Merge resumo no client.json
python3 << PYEOF
import json
from datetime import datetime, timezone

raw_path = "$RAW_OUT"
client_path = "$CLIENT_DIR/client.json"

with open(raw_path, encoding='utf-8') as f:
    raw = json.load(f)

with open(client_path, encoding='utf-8') as f:
    client = json.load(f)

# Summary condensado — raw fica no cache (inclui screenshots full-page pesados)
tracking = raw.get("tracking_stack") or {}
events = raw.get("events_fired") or {}
cro_el = raw.get("cro_elements") or {}
dl = raw.get("datalayer") or {}
flags = raw.get("quality_flags") or []
compliance = raw.get("compliance_lgpd") or {}
nav = raw.get("navigation") or {}

# tools_detected no summary: so id+name+category (sem evidence detalhada)
tools_light = {}
for tid, info in (tracking.get("tools_detected") or {}).items():
    tools_light[tid] = {
        "name": info.get("name"),
        "category": info.get("category"),
    }

summary = {
    "fetched_at": raw.get("fetched_at"),
    "url": raw.get("url"),
    "cache_file": raw_path.replace("$CLIENT_DIR/", ""),
    "engine": raw.get("engine"),
    "tracking_stack": {
        "tools_detected": tools_light,
        "ids_found": tracking.get("ids_found") or {},
        "categories_summary": tracking.get("categories_summary") or {},
        "total_tools": tracking.get("total_tools") or 0,
    },
    "events_fired": {
        "ga4_event_count": events.get("ga4_event_count") or 0,
        "meta_event_count": events.get("meta_event_count") or 0,
        "ga4_event_names": events.get("ga4_event_names") or [],
        "meta_event_names": events.get("meta_event_names") or [],
        # eventos detalhados so no raw
    },
    "datalayer": {
        "desktop_length": (dl.get("desktop") or {}).get("length"),
        "mobile_length": (dl.get("mobile") or {}).get("length"),
    },
    "cro_elements": cro_el,  # leve o suficiente p/ ficar no client.json
    "quality_flags": flags,
    "compliance_lgpd": compliance,
    "navigation": nav,
    # Screenshots full-page NAO vao pro client.json (pesados) — so no raw
}

client["page_audit_deep"] = summary

with open(client_path, "w", encoding="utf-8") as f:
    json.dump(client, f, ensure_ascii=False, indent=2)

print(f"[OK] page_audit_deep salvo em client.json (raw: {raw_path})")
PYEOF

echo "Cache raw: $RAW_OUT"
