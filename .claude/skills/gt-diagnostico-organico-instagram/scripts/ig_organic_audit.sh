#!/bin/bash
# ig_organic_audit.sh — Orquestra a auditoria de conteudo organico no Instagram
# Uso:  ig_organic_audit.sh <client_dir>
# Ex:   ig_organic_audit.sh squads/{squad}/clientes/{cliente}
#
# Opcional (override dos handles dos concorrentes):
#   CMP_HANDLES="Concorrente 1=@concorrente1;Concorrente 2=@concorrente2" \
#     ig_organic_audit.sh squads/{squad}/clientes/{cliente}

set -euo pipefail

CLIENT_DIR="${1:?Uso: ig_organic_audit.sh <client_dir>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PY_SCRIPT="$SCRIPT_DIR/ig_organic_audit.py"

if [ ! -f "$PY_SCRIPT" ]; then
  echo "ERROR: ig_organic_audit.py nao encontrado em $PY_SCRIPT" >&2
  exit 1
fi

if [ ! -d "$CLIENT_DIR" ]; then
  echo "ERROR: client_dir $CLIENT_DIR nao existe" >&2
  exit 1
fi

mkdir -p "$CLIENT_DIR/cache"

echo ">> Rodando ig_organic_audit para $CLIENT_DIR ..."
python3 "$PY_SCRIPT" "$CLIENT_DIR"

echo
echo ">> Summary pronto em: $CLIENT_DIR/cache/ig_organic_audit-summary.json"
