#!/usr/bin/env python3
"""Valida invariantes estruturais e checks de segurança do Builders Hub."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
AGENT_SKILLS = ROOT / ".agents" / "skills"

FUNCTION_PREFIXES = {"geral", "gt", "designer", "copy", "account", "coord"}
SOURCE_PREFIXES = {
    "v4mos",
    "google",
    "ga4",
    "meta",
    "hubspot",
    "kommo",
    "shopify",
    "tray",
}
VALID_PREFIXES = FUNCTION_PREFIXES | SOURCE_PREFIXES
BASE_SKILLS = {
    "onboarding",
    "contexto",
    "criador-de-skills",
    "novo-cliente",
    "novo-projeto",
    "novo-squad",
    "compartilhar-skill",
    "sync-hub",
}
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SECRET_PATTERNS = {
    "chave privada": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "token GitHub": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "chave OpenAI": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "access key AWS": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
}


def parse_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if not match:
        return {}
    values: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        if ":" not in raw or raw.lstrip().startswith("#"):
            continue
        key, _, value = raw.partition(":")
        values[key.strip()] = value.strip().strip("'\"")
    return values


def relative_files(root: Path) -> dict[Path, Path]:
    return {
        path.relative_to(root): path
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }


def repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return []
    return [ROOT / raw.decode() for raw in result.stdout.split(b"\0") if raw]


def validate() -> list[str]:
    errors: list[str] = []
    claude_files = relative_files(CLAUDE_SKILLS)
    agent_files = relative_files(AGENT_SKILLS)

    if claude_files.keys() != agent_files.keys():
        missing_agent = sorted(str(p) for p in claude_files.keys() - agent_files.keys())
        missing_claude = sorted(
            str(p) for p in agent_files.keys() - claude_files.keys()
        )
        if missing_agent:
            errors.append("arquivos ausentes em .agents: " + ", ".join(missing_agent))
        if missing_claude:
            errors.append("arquivos ausentes em .claude: " + ", ".join(missing_claude))

    for relative in sorted(claude_files.keys() & agent_files.keys()):
        if claude_files[relative].read_bytes() != agent_files[relative].read_bytes():
            errors.append(f"duplo-write divergente: {relative}")

    for skill_dir in sorted(path for path in CLAUDE_SKILLS.iterdir() if path.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"skill sem SKILL.md: {skill_dir.name}")
            continue
        fm = parse_frontmatter(skill_md)
        if fm.get("name") != skill_dir.name:
            errors.append(f"name divergente da pasta: {skill_dir.name}")
        if not fm.get("description"):
            errors.append(f"description ausente: {skill_dir.name}")
        if (
            fm.get("license", "").endswith("LICENSE.txt")
            and not (skill_dir / "LICENSE.txt").is_file()
        ):
            errors.append(f"licenca referenciada mas ausente: {skill_dir.name}")
        if skill_dir.name not in BASE_SKILLS:
            prefix = skill_dir.name.split("-", 1)[0]
            if prefix not in VALID_PREFIXES:
                errors.append(f"prefixo invalido: {skill_dir.name}")
            for field in ("area", "author", "version"):
                if not fm.get(field):
                    errors.append(f"frontmatter {field} ausente: {skill_dir.name}")
            if fm.get("area") and fm["area"] != prefix:
                errors.append(f"area nao corresponde ao prefixo: {skill_dir.name}")
            if fm.get("version") and not VERSION_RE.fullmatch(fm["version"]):
                errors.append(f"versao sem SemVer: {skill_dir.name}")

    root_pairs = [(ROOT / "CLAUDE.md", ROOT / "AGENTS.md")]
    root_pairs.extend(
        (path, path.with_name("AGENTS.md"))
        for path in (ROOT / "bases" / "_template").rglob("CLAUDE.md")
    )
    for claude_md, agents_md in root_pairs:
        if not agents_md.is_file() or claude_md.read_bytes() != agents_md.read_bytes():
            errors.append(
                f"contextos divergentes: {claude_md.relative_to(ROOT).parent}"
            )

    files = repository_files()
    for path in files:
        relative = path.relative_to(ROOT)
        if path.name == ".env" or path.name.endswith(".local.json"):
            errors.append(f"arquivo local/sensivel candidato a versao: {relative}")
        if not path.is_file() or path.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pdf",
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possivel {label} em {relative}")

    for env_example in ROOT.rglob(".env.example"):
        if any(part in {"squads", ".git"} for part in env_example.parts):
            continue
        for number, raw in enumerate(
            env_example.read_text(encoding="utf-8").splitlines(), 1
        ):
            line = raw.strip()
            if (
                line
                and not line.startswith("#")
                and "=" in line
                and line.split("=", 1)[1].strip()
            ):
                errors.append(
                    f"valor preenchido em template de credencial: {env_example.relative_to(ROOT)}:{number}"
                )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Falhas de validação:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("✓ estrutura, duplo-write, frontmatters e checks de segurança válidos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
