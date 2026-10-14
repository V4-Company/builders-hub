#!/usr/bin/env python3
"""Valida frontmatter, módulos esperados e triplo-write da família."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


EXPECTED = {
    "account-retrospectiva-performance-maestro",
    "account-retrospectiva-contexto-fontes",
    "account-retrospectiva-midia",
    "account-retrospectiva-criativos",
    "account-retrospectiva-funil-inside-sales",
    "account-retrospectiva-vendedores",
    "account-retrospectiva-atendimento",
    "account-retrospectiva-ecommerce",
    "account-retrospectiva-breakeven",
    "account-retrospectiva-reconciliacao",
    "account-retrospectiva-evidencias",
    "account-retrospectiva-achados-gaps",
    "account-retrospectiva-consolidacao",
    "account-retrospectiva-drive-handoff",
}

ADAPTERS = {"account-ropre-quarter-retrospectiva"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root: Path) -> dict[str, Path]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): path
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", type=Path, nargs="?", default=Path.cwd())
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    mirrors = [workspace / tree / "skills" for tree in (".agents", ".claude", ".codex")]
    errors: list[str] = []

    for name in sorted(EXPECTED | ADAPTERS):
        left = mirrors[0] / name
        if not left.is_dir():
            errors.append(f"diretório ausente: {mirrors[0].parent.name}/{name}")
            continue
        left_files = files(left)
        for mirror in mirrors[1:]:
            right = mirror / name
            if not right.is_dir():
                errors.append(f"diretório ausente: {mirror.parent.name}/{name}")
                continue
            right_files = files(right)
            if set(left_files) != set(right_files):
                errors.append(f"estrutura divergente: {mirror.parent.name}/{name}")
                continue
            for relative in left_files:
                if digest(left_files[relative]) != digest(right_files[relative]):
                    errors.append(f"hash divergente: {mirror.parent.name}/{name}/{relative}")

        if name in ADAPTERS:
            continue

        skill = (left / "SKILL.md").read_text(encoding="utf-8")
        pattern = rf"(?ms)^---\s*\nname: {re.escape(name)}\n.*?\narea: account\nauthor: .+\nversion: \d+\.\d+\.\d+\n---"
        if not re.search(pattern, skill):
            errors.append(f"frontmatter inválido: {name}")

    if errors:
        print("FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"OK: {len(EXPECTED)} skills + adaptador com triplo-write e frontmatter válido")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
