#!/usr/bin/env python3
"""
plano-backup.py
Varre uma KB, classifica cada arquivo por sensibilidade e compara com o
manifesto do ultimo backup. Devolve o plano em JSON no stdout.

Uso:
    python3 plano-backup.py <caminho-da-kb> [--modo espelho|material]
                             [--destino ID_DA_PASTA]

Saida (JSON):
    {
      "kb": "...", "modo": "espelho",
      "resumo": {"segredo": 4, "interno": 11, "material": 38, "naoclassificado": 0,
                 "a_subir": 49, "ja_atualizados": 0},
      "segredo": [...],           # nunca sobem
      "interno": [...],           # so no modo espelho
      "material": [...],          # sobem nos dois modos
      "naoclassificado": [...],   # PERGUNTE ao usuario
      "pastas": ["calls", "docs", "docs/comercial", ...],
      "manifesto_compativel": true
    }

Cada arquivo selecionado traz: caminho, tamanho, sha, binario, mime, mudou.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

MANIFESTO = ".backup-drive.json"

# --- Regras de classificacao -------------------------------------------------
# Uma regra nova aprendida em campo vira uma linha aqui.

SEGREDO_NOMES = {
    ".env",
    "credentials.json",
    "token.json",
    ".DS_Store",
    "Thumbs.db",
    ".gitkeep",
    MANIFESTO,
}
SEGREDO_PREFIXOS = (".env",)  # .env.local, .env.producao...
SEGREDO_SUFIXOS = (".pem", ".key", ".p12", ".keystore")
SEGREDO_CONTEM = ("service-account", "secret", "credencial")
# .env.example nao tem segredo, mas tambem nao serve de backup: fica de fora.

INTERNO_PASTAS = ("mission-control", "checkins")
INTERNO_NOMES = {"CLAUDE.md", "AGENTS.md", "client.json"}
INTERNO_CONTEM = ("analise-", "review", "sabatina", "diagnostico-interno")

MATERIAL_PASTAS = ("calls", "docs", "outputs", "campanhas", "relatorios", "assets")
MATERIAL_NOMES = {"README.md", "links.md"}

BINARIOS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".docx",
    ".xlsx",
    ".pptx",
    ".zip",
    ".mp4",
    ".mov",
    ".mp3",
    ".woff",
    ".woff2",
    ".ttf",
}

MIMES = {
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".json": "application/json",
    ".html": "text/html",
    ".csv": "text/csv",
    ".yaml": "text/yaml",
    ".yml": "text/yaml",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".zip": "application/zip",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def classificar(rel: pathlib.PurePosixPath) -> str:
    nome = rel.name
    partes = rel.parts
    topo = partes[0] if len(partes) > 1 else ""

    if (
        nome in SEGREDO_NOMES
        or nome.startswith(SEGREDO_PREFIXOS)
        or rel.suffix.lower() in SEGREDO_SUFIXOS
        or any(t in nome.lower() for t in SEGREDO_CONTEM)
    ):
        return "segredo"

    if (
        topo in INTERNO_PASTAS
        or nome in INTERNO_NOMES
        or any(t in nome.lower() for t in INTERNO_CONTEM)
    ):
        return "interno"

    if topo in MATERIAL_PASTAS or nome in MATERIAL_NOMES:
        return "material"

    return "naoclassificado"


def sha256(caminho: pathlib.Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as fh:
        for bloco in iter(lambda: fh.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description="Plano de backup de uma KB para o Drive.")
    ap.add_argument("kb", help="caminho da pasta da KB")
    ap.add_argument("--modo", choices=["espelho", "material"], default="espelho")
    ap.add_argument(
        "--destino",
        help="ID da pasta do Drive; evita reaproveitar hashes de outro destino",
    )
    args = ap.parse_args()

    raiz = pathlib.Path(args.kb).expanduser().resolve()
    if not raiz.is_dir():
        print(f"erro: {raiz} nao e uma pasta", file=sys.stderr)
        return 1

    anterior: dict = {}
    manifesto_compativel = False
    manifesto = raiz / MANIFESTO
    if manifesto.exists():
        try:
            dados_manifesto = json.loads(manifesto.read_text(encoding="utf-8"))
            destino_anterior = dados_manifesto.get("pasta_destino")
            manifesto_compativel = not args.destino or destino_anterior == args.destino
            if manifesto_compativel:
                anterior = dados_manifesto.get("arquivos", {})
            else:
                print(
                    "aviso: o destino mudou; tratando todos os arquivos como novos",
                    file=sys.stderr,
                )
        except (json.JSONDecodeError, OSError):
            print("aviso: manifesto ilegivel, tratando tudo como novo", file=sys.stderr)

    baldes: dict[str, list] = {
        "segredo": [],
        "interno": [],
        "material": [],
        "naoclassificado": [],
    }
    for caminho in sorted(raiz.rglob("*")):
        if ".git" in caminho.parts or caminho.is_dir():
            continue
        rel = pathlib.PurePosixPath(caminho.relative_to(raiz).as_posix())

        # Nunca siga links: eles podem apontar para fora da KB e puxar arquivos
        # que o usuario nao colocou no escopo do backup.
        if caminho.is_symlink():
            baldes["segredo"].append(
                {
                    "caminho": str(rel),
                    "tamanho": 0,
                    "motivo": "link simbolico ignorado",
                }
            )
            continue

        if not caminho.is_file():
            continue
        nivel = classificar(rel)

        item = {"caminho": str(rel), "tamanho": caminho.stat().st_size}

        if nivel != "segredo":
            digest = sha256(caminho)
            item.update(
                sha=digest,
                binario=caminho.suffix.lower() in BINARIOS,
                mime=MIMES.get(caminho.suffix.lower(), "application/octet-stream"),
                mudou=anterior.get(str(rel), {}).get("sha") != digest,
            )

        baldes[nivel].append(item)

    sobe = baldes["material"] + (baldes["interno"] if args.modo == "espelho" else [])
    a_subir = [f for f in sobe if f["mudou"]]
    pastas: set[str] = set()
    for item in sobe:
        pai = pathlib.PurePosixPath(item["caminho"]).parent
        if pai == pathlib.PurePosixPath("."):
            continue
        acumulado: list[str] = []
        for parte in pai.parts:
            acumulado.append(parte)
            pastas.add("/".join(acumulado))

    print(
        json.dumps(
            {
                "kb": str(raiz),
                "modo": args.modo,
                "resumo": {
                    "segredo": len(baldes["segredo"]),
                    "interno": len(baldes["interno"]),
                    "material": len(baldes["material"]),
                    "naoclassificado": len(baldes["naoclassificado"]),
                    "selecionados": len(sobe),
                    "a_subir": len(a_subir),
                    "ja_atualizados": len([f for f in sobe if not f["mudou"]]),
                },
                **baldes,
                "pastas": sorted(pastas),
                "manifesto_compativel": manifesto_compativel,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    if baldes["naoclassificado"]:
        print(
            f"\naviso: {len(baldes['naoclassificado'])} arquivo(s) sem regra — "
            f"pergunte ao usuario antes de subir",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
