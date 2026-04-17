#!/usr/bin/env python3
"""
build-registry.py
Regenera REGISTRY.md a partir dos frontmatters das skills em .claude/skills/.
Agrupa por area, usa `area:` do frontmatter; se ausente, deriva do prefixo do nome da pasta.

Uso: python3 scripts/build-registry.py
Tambem rodado pela GitHub Action em toda merge na main.
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / ".claude" / "skills"
OUTPUT = REPO_ROOT / "REGISTRY.md"

# Prefixos de AREA (skills que entregam trabalho final)
AREAS = ["trafego", "criativo", "cs", "estrategia", "gestao", "dados", "outra"]

# Prefixos de FONTE (skills que puxam/expoem dados de uma integracao)
SOURCES = ["v4mos", "google", "ga4", "meta", "hubspot", "kommo", "shopify", "tray"]

AREA_LABEL = {
    "trafego": "🎯 Tráfego",
    "criativo": "🎨 Criativo",
    "cs": "🤝 Customer Success",
    "estrategia": "🧭 Estratégia",
    "gestao": "📋 Gestão",
    "dados": "📊 Dados",
    "outra": "🧩 Outras",
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

# Skills de base/fluxo — sem prefixo, ficam numa secao propria
BASE_SKILLS = {
    "onboarding",
    "contexto",
    "criador-de-skills",
    "novo-cliente",
    "novo-projeto",
    "brainstormar-sobre-minha-funcao",
    "sabatina",
    "compartilhar-skill",
    "sync-hub",
    "frontend-design",
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
    """Retorna (family, key) onde family e 'base' | 'area' | 'source'.
    key e '_base', o prefixo de area, ou o prefixo de fonte.
    """
    if name in BASE_SKILLS:
        return "base", "_base"
    prefix = name.split("-", 1)[0]
    if prefix in SOURCES:
        return "source", prefix
    area = fm.get("area") or prefix
    if area not in AREAS:
        area = "outra"
    return "area", area


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"Erro: {SKILLS_DIR} não existe", file=sys.stderr)
        return 1

    # Coleta todas as skills
    skills: list[tuple[str, dict[str, str], str]] = []
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
    today = datetime.date.today().isoformat()

    # Conta por chave (area ou source)
    counts: dict[str, int] = {"_base": 0}
    for a in AREAS:
        counts[a] = 0
    for s in SOURCES:
        counts[s] = 0
    for _, _, _, key in skills:
        counts[key] = counts.get(key, 0) + 1

    lines: list[str] = []
    lines.append("# Builders Hub — Registry")
    lines.append("")
    lines.append(f"**{total} skills** · última atualização: {today}")
    lines.append("")
    lines.append(
        "> Catálogo auto-gerado por `scripts/build-registry.py`. "
        "Não edite à mão — rode `/sync-hub` ou envie PR pela `/compartilhar-skill`."
    )
    lines.append("")
    lines.append("## Índice")
    lines.append("")
    lines.append(f"- [{AREA_LABEL['_base']}](#base) ({counts['_base']})")
    for a in AREAS:
        c = counts.get(a, 0)
        if c == 0:
            continue
        lines.append(f"- [{AREA_LABEL[a]}](#{a}) ({c})")
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
    render_section(AREA_LABEL["_base"], "base", lambda f, k: f == "base")
    # Áreas
    for a in AREAS:
        if counts.get(a, 0) == 0:
            continue
        render_section(AREA_LABEL[a], a, lambda f, k, _a=a: f == "area" and k == _a)
    # Integrações / Fontes (se tem qualquer uma)
    if source_total:
        lines.append("## 🔌 Integrações / Fontes")
        lines.append("")
        lines.append('<a id="fontes"></a>')
        lines.append("")
        lines.append("_Skills que puxam dados de integrações externas. Reutilizáveis por outras skills._")
        lines.append("")
        for s in SOURCES:
            if counts.get(s, 0) == 0:
                continue
            render_section(SOURCE_LABEL[s], s, lambda f, k, _s=s: f == "source" and k == _s)

    lines.append("---")
    lines.append("")
    lines.append(
        "_Quer contribuir? Roda `/compartilhar-skill`. "
        "Mais detalhes em [CONTRIBUTING.md](./CONTRIBUTING.md)._"
    )
    lines.append("")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ REGISTRY.md regenerado ({total} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
