#!/usr/bin/env python3
"""Executa os testes do repositorio e os testes portaveis de cada skill."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_directories() -> list[Path]:
    directories = [ROOT / "tests"]
    directories.extend(sorted((ROOT / ".claude" / "skills").glob("*/tests")))
    return [path for path in directories if path.is_dir()]


def main() -> int:
    suite = unittest.TestSuite()
    directories = test_directories()
    for directory in directories:
        loader = unittest.TestLoader()
        suite.addTests(
            loader.discover(
                start_dir=str(directory),
                pattern="test_*.py",
                top_level_dir=str(directory),
            )
        )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(f"\n{result.testsRun} testes em {len(directories)} diretorio(s)")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
