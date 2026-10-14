#!/usr/bin/env python3
"""Detecta motores de break-even disponíveis sem alterar o ambiente."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


ENGINES = ("projecao-breakeven", "breakeven-projetos")
DEPENDENCIES = ("pandas", "openpyxl", "pycel", "xlsxwriter")


def candidates(workspace: Path) -> list[Path]:
    roots = [
        workspace / ".agents" / "skills",
        workspace / ".claude" / "skills",
        workspace / ".codex" / "skills",
        Path.home() / ".agents" / "skills",
        Path.home() / ".claude" / "skills",
        Path.home() / ".codex" / "skills",
    ]
    return roots


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    args = parser.parse_args()

    print("# Diagnóstico dos motores de break-even\n")
    print("## Motores\n")
    print("| Motor | Status | Caminho |")
    print("|---|---|---|")
    for engine in ENGINES:
        matches = [root / engine for root in candidates(args.workspace) if (root / engine / "SKILL.md").exists()]
        status = "disponível" if matches else "ausente"
        location = str(matches[0]) if matches else "—"
        print(f"| {engine} | {status} | {location} |")

    print("\n## Dependências Python\n")
    print("| Dependência | Status |")
    print("|---|---|")
    for dependency in DEPENDENCIES:
        status = "disponível" if importlib.util.find_spec(dependency) else "ausente"
        print(f"| {dependency} | {status} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
