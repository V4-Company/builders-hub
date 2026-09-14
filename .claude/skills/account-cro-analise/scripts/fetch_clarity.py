#!/usr/bin/env python3
"""Puxa metricas agregadas do Microsoft Clarity (Data Export API)."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

API_URL = "https://www.clarity.ms/export-data/api/v1/project-live-insights"


def load_token_from_env_file(env_path):
    if not os.path.exists(env_path):
        return None
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CLARITY_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None


def fetch(token, num_of_days):
    url = f"{API_URL}?numOfDays={num_of_days}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"Erro HTTP {e.code} da API do Clarity: {body}")
    except urllib.error.URLError as e:
        sys.exit(f"Falha de conexao com a API do Clarity: {e.reason}")


def main():
    parser = argparse.ArgumentParser(
        description="Puxa metricas agregadas do Microsoft Clarity (Data Export API)"
    )
    parser.add_argument("--env-file", help="Caminho pro .env do cliente (le CLARITY_API_TOKEN de la)")
    parser.add_argument("--token", help="Token direto (sobrepoe --env-file)")
    parser.add_argument(
        "--days", type=int, default=3, choices=[1, 2, 3],
        help="Janela em dias (max 3, limite da API do Clarity)",
    )
    parser.add_argument("--out", help="Salva o JSON bruto nesse caminho em vez de so imprimir no stdout")
    parser.add_argument(
        "--history-file",
        help="Alem de imprimir/salvar, acrescenta uma linha JSONL nesse arquivo "
             "(um snapshot datado por chamada) pra ir construindo historico manualmente ao longo do tempo",
    )
    args = parser.parse_args()

    token = args.token
    if not token and args.env_file:
        token = load_token_from_env_file(args.env_file)
    if not token:
        sys.exit(
            "Token nao encontrado. Passe --token ou --env-file apontando pro .env "
            "do cliente com CLARITY_API_TOKEN preenchido."
        )

    data = fetch(token, args.days)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Salvo em {args.out}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

    if args.history_file:
        entry = {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "days": args.days,
            "data": data,
        }
        os.makedirs(os.path.dirname(args.history_file) or ".", exist_ok=True)
        with open(args.history_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"Snapshot acrescentado em {args.history_file}")


if __name__ == "__main__":
    main()
