#!/bin/bash
# page_audit.sh — Orquestra a auditoria tecnica de uma URL
# Uso:  page_audit.sh <client_dir> <url>
# Ex:   page_audit.sh squads/{squad}/clientes/{cliente} https://www.site-do-cliente.com.br
#
# Le:    .credentials/google.json (pagespeed_api_key)
#        <client_dir>/client.json
# Grava: <client_dir>/cache/page_audit-<timestamp>.json (raw)
#        <client_dir>/client.json (campo page_audit com resumo)

set -euo pipefail

CLIENT_DIR="${1:?Uso: page_audit.sh <client_dir> <url>}"
URL="${2:?Uso: page_audit.sh <client_dir> <url>}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/page_audit.py"

if [ ! -f "$PY_SCRIPT" ]; then
  echo "ERROR: page_audit.py nao encontrado em $PY_SCRIPT" >&2
  exit 1
fi

# Descobrir credenciais (sobe na arvore procurando .credentials/google.json)
CRED_FILE=""
SEARCH_DIR="$CLIENT_DIR"
for i in 1 2 3 4 5; do
  SEARCH_DIR="$(cd "$SEARCH_DIR/.." && pwd)"
  if [ -f "$SEARCH_DIR/.credentials/google.json" ]; then
    CRED_FILE="$SEARCH_DIR/.credentials/google.json"
    break
  fi
done

PSI_API_KEY=""
if [ -n "$CRED_FILE" ]; then
  PSI_API_KEY=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('pagespeed_api_key',''))" "$CRED_FILE" 2>/dev/null || true)
fi

# Cache dir
mkdir -p "$CLIENT_DIR/cache"
TS=$(date -u +%Y%m%d-%H%M%S)
RAW_OUT="$CLIENT_DIR/cache/page_audit-$TS.json"

# Rodar Python worker
if [ -n "$PSI_API_KEY" ]; then
  echo ">> Rodando auditoria (PSI mobile+desktop + on-page + security) em paralelo..."
  PSI_API_KEY="$PSI_API_KEY" python3 "$PY_SCRIPT" "$URL" "$RAW_OUT"
else
  echo ">> Sem PSI_API_KEY — rodando apenas on-page + security (PageSpeed sera pulado)..."
  python3 "$PY_SCRIPT" "$URL" "$RAW_OUT" --skip-psi
fi

# O Builders Hub não exige client.json. Quando ele não existe, preserve o
# cache bruto e deixe a skill interpretar os dados junto com a KB do cliente.
if [ ! -f "$CLIENT_DIR/client.json" ]; then
  echo "[OK] Auditoria bruta concluída; client.json ausente, merge ignorado."
  echo "Cache raw: $RAW_OUT"
  exit 0
fi

# Merge resumo no client.json
python3 << PYEOF
import json, sys
from datetime import datetime, timezone

raw_path = "$RAW_OUT"
client_path = "$CLIENT_DIR/client.json"

with open(raw_path, encoding='utf-8') as f:
    raw = json.load(f)

with open(client_path, encoding='utf-8') as f:
    client = json.load(f)

# Resumo condensado para client.json (raw fica no cache)
psi = raw.get("pagespeed") or {}
mob = (psi.get("mobile") or {})
des = (psi.get("desktop") or {})
onp = raw.get("onpage") or {}
sec = raw.get("security") or {}

summary = {
    "fetched_at": raw.get("fetched_at"),
    "url": raw.get("url"),
    "cache_file": raw_path.replace("$CLIENT_DIR/", ""),
    "pagespeed": {
        "mobile_scores": (mob or {}).get("scores") if isinstance(mob, dict) else None,
        "desktop_scores": (des or {}).get("scores") if isinstance(des, dict) else None,
        "mobile_cwv_lab": (mob or {}).get("cwv_lab") if isinstance(mob, dict) else None,
        "desktop_cwv_lab": (des or {}).get("cwv_lab") if isinstance(des, dict) else None,
        "mobile_cwv_field": (mob or {}).get("cwv_field") if isinstance(mob, dict) else None,
        "desktop_cwv_field": (des or {}).get("cwv_field") if isinstance(des, dict) else None,
        "mobile_top_opportunities": ((mob or {}).get("opportunities") or [])[:10] if isinstance(mob, dict) else [],
        "desktop_top_opportunities": ((des or {}).get("opportunities") or [])[:10] if isinstance(des, dict) else [],
        "mobile_error": (mob or {}).get("error") if isinstance(mob, dict) else None,
        "desktop_error": (des or {}).get("error") if isinstance(des, dict) else None,
        "skipped": raw.get("pagespeed_skipped", False),
    },
    "screenshots": {
        "mobile": (mob or {}).get("final_screenshot") if isinstance(mob, dict) else None,
        "desktop": (des or {}).get("final_screenshot") if isinstance(des, dict) else None,
    },
    "onpage": {
        "mobile": onp.get("mobile"),
        "desktop": onp.get("desktop"),
        "divergences": onp.get("divergences") or [],
    },
    "security": sec,
}

# Remove 'headers' e payload pesado do summary (fica no raw)
for k in ("mobile", "desktop"):
    blk = summary["onpage"].get(k)
    if isinstance(blk, dict):
        blk.pop("headers", None)

client["page_audit"] = summary

with open(client_path, "w", encoding="utf-8") as f:
    json.dump(client, f, ensure_ascii=False, indent=2)

print(f"[OK] page_audit salvo em client.json (raw: {raw_path})")
PYEOF

echo "Cache raw: $RAW_OUT"
