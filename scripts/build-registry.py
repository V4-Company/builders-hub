#!/usr/bin/env python3
"""
build-registry.py
Regenera REGISTRY.md a partir dos frontmatters das skills em .claude/skills/.
Agrupa por funcao/papel, usa `area:` do frontmatter (mantido por compat); se ausente, deriva do prefixo do nome da pasta.

Uso: python3 scripts/build-registry.py
Tambem rodado pela GitHub Action em toda merge na main.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
OUTPUT = REPO_ROOT / "REGISTRY.md"

# Prefixos de FUNCAO/PAPEL (skills que entregam trabalho final, agrupadas por quem usa)
FUNCTIONS = ["geral", "gt", "designer", "copy", "account", "coord"]

# Prefixos de FONTE (skills que puxam/expoem dados de uma integracao)
SOURCES = ["v4mos", "google", "ga4", "meta", "hubspot", "kommo", "shopify", "tray"]

FUNCTION_LABEL = {
    "geral": "🌐 Geral",
    "gt": "🎯 Gestao de Trafego",
    "designer": "🎨 Designer",
    "copy": "✍️ Copy",
    "account": "🤝 Account",
    "coord": "📋 Coordenacao",
    "_base": "🛠 Base (setup/fluxo)",
}

SOURCE_LABEL = {
    "v4mos": "🔌 V4mos",
    "google": "🔌 Google Ads",
    "ga4": "🔌 GA4",
    "meta": "🔌 Meta (direto)",
    "hubspot": "🔌 HubSpot",
    "kommo": "🔌 Kommo",
    "shopify": "🔌 Shopify",
    "tray": "🔌 Tray",
}

# Skills de base/fluxo — sem prefixo, ficam numa secao propria.
# Sao a "mecanica do hub" (setup, novo cliente, criar/compartilhar skill, sync).
# Skills de trabalho universal (sabatina, frontend-design, brainstormar-sobre-minha-funcao)
# vao com prefixo `geral-*` em vez de aqui.
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


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        # "key: value"
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            fm[key] = value
    return fm


def truncate(s: str, n: int = 110) -> str:
    s = s.replace("\n", " ").replace("|", "\\|").strip()
    if len(s) <= n:
        return s
    return s[: n - 3].rstrip() + "..."


def classify(name: str, fm: dict[str, str]) -> tuple[str, str]:
    """Retorna (family, key) onde family e 'base' | 'function' | 'source'.
    key e '_base', o prefixo de funcao/papel, ou o prefixo de fonte.
    """
    if name in BASE_SKILLS:
        return "base", "_base"
    prefix = name.split("-", 1)[0]
    if prefix in SOURCES:
        return "source", prefix
    # campo `area:` no frontmatter agora carrega o papel (nome do campo mantido por compat)
    function = fm.get("area") or prefix
    if function not in FUNCTIONS:
        function = "geral"
    return "function", function


def render_registry() -> str:
    if not SKILLS_DIR.is_dir():
        raise FileNotFoundError(f"{SKILLS_DIR} não existe")

    # Coleta todas as skills
    skills: list[tuple[str, dict[str, str], str, str]] = []
    for path in sorted(SKILLS_DIR.iterdir()):
        skill_md = path / "SKILL.md"
        if not skill_md.is_file():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8")
        except OSError as e:
            print(f"Aviso: não consegui ler {skill_md}: {e}", file=sys.stderr)
            continue
        fm = parse_frontmatter(text)
        family, key = classify(path.name, fm)
        skills.append((path.name, fm, family, key))

    total = len(skills)
    # Conta por chave (funcao ou source)
    counts: dict[str, int] = {"_base": 0}
    for fn in FUNCTIONS:
        counts[fn] = 0
    for s in SOURCES:
        counts[s] = 0
    for _, _, _, key in skills:
        counts[key] = counts.get(key, 0) + 1

    lines: list[str] = []
    lines.append("# Builders Hub — Registry")
    lines.append("")
    lines.append(f"**{total} skills**")
    lines.append("")
    lines.append(
        "> Catálogo auto-gerado por `scripts/build-registry.py`. "
        "Não edite à mão — rode `/sync-hub` ou envie PR pela `/compartilhar-skill`."
    )
    lines.append("")
    lines.append("## Índice")
    lines.append("")
    lines.append(f"- [{FUNCTION_LABEL['_base']}](#base) ({counts['_base']})")
    for fn in FUNCTIONS:
        c = counts.get(fn, 0)
        if c == 0:
            continue
        lines.append(f"- [{FUNCTION_LABEL[fn]}](#{fn}) ({c})")
    # Seção de fontes (se alguma tem skills)
    source_total = sum(counts.get(s, 0) for s in SOURCES)
    if source_total:
        lines.append(f"- [🔌 Integrações / Fontes](#fontes) ({source_total})")
        for s in SOURCES:
            c = counts.get(s, 0)
            if c == 0:
                continue
            lines.append(f"  - [{SOURCE_LABEL[s]}](#{s}) ({c})")
    lines.append("")

    def render_section(label: str, anchor: str, match_fn) -> None:
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f'<a id="{anchor}"></a>')
        lines.append("")
        lines.append("| Skill | O que faz | Autor | v |")
        lines.append("|---|---|---|---|")
        found = False
        for name, fm, family, key in skills:
            if not match_fn(family, key):
                continue
            desc = truncate(fm.get("description", "(sem descrição)"))
            author = fm.get("author", "—") or "—"
            version = fm.get("version", "—") or "—"
            author_display = f"@{author}" if author != "—" else "—"
            lines.append(f"| `{name}` | {desc} | {author_display} | {version} |")
            found = True
        if not found:
            lines.append("| _(vazio)_ | | | |")
        lines.append("")

    # Renderiza base primeiro
    render_section(FUNCTION_LABEL["_base"], "base", lambda f, k: f == "base")
    # Funcoes/papeis
    for fn in FUNCTIONS:
        if counts.get(fn, 0) == 0:
            continue
        render_section(
            FUNCTION_LABEL[fn], fn, lambda f, k, _fn=fn: f == "function" and k == _fn
        )
    # Integrações / Fontes (se tem qualquer uma)
    if source_total:
        lines.append("## 🔌 Integrações / Fontes")
        lines.append("")
        lines.append('<a id="fontes"></a>')
        lines.append("")
        lines.append(
            "_Skills que puxam dados de integrações externas. Reutilizáveis por outras skills._"
        )
        lines.append("")
        for s in SOURCES:
            if counts.get(s, 0) == 0:
                continue
            render_section(
                SOURCE_LABEL[s], s, lambda f, k, _s=s: f == "source" and k == _s
            )

    lines.append("---")
    lines.append("")
    lines.append(
        "_Quer contribuir? Roda `/compartilhar-skill`. "
        "Mais detalhes em [CONTRIBUTING.md](./CONTRIBUTING.md)._"
    )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenera ou valida o REGISTRY.md")
    parser.add_argument(
        "--check",
        action="store_true",
        help="não altera arquivos; falha se o REGISTRY.md estiver desatualizado",
    )
    args = parser.parse_args()

    try:
        rendered = render_registry()
    except FileNotFoundError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1

    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.is_file() else ""
        if current != rendered:
            print(
                "✗ REGISTRY.md está desatualizado; rode python3 scripts/build-registry.py",
                file=sys.stderr,
            )
            return 1
        print("✓ REGISTRY.md está atualizado")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print("✓ REGISTRY.md regenerado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
