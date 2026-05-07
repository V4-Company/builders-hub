#!/usr/bin/env python3
"""
Gera arquivos -radar.md compactos a partir dos arquivos completos de produto V4.

Uso:
  python scripts/gerar-radares.py

Lê todos os .md em referencias/ (exceto os já -*radar.md, _template, CLAUDE, produtos-v4)
e gera um {produto}-radar.md compacto para cada um que tiver conteúdo real.

Seções extraídas (tentativa por ordem de prioridade):
- "O que é" / "O que entrega" / "Descrição"
- "Para quem" / "ICP" / "Público-alvo" / "Perfil de cliente"
- "Quando faz sentido vender" / "Sinais de compra" / "Match" / "Momento de compra"
- "O que NÃO é" / "Fora do escopo" / "Não inclui"
- "Pré-requisito" / "Pré-requisitos"
- "Preço" / "CSP" / "Investimento" / "Pacote"
"""

import re
import sys
from pathlib import Path

REFERENCIAS_DIR = Path(__file__).parent.parent / "referencias"

# Arquivos a ignorar
IGNORAR = {"_template-produto.md", "CLAUDE.md", "produtos-v4.md"}

# Mapeamento: nome da seção no radar → padrões a buscar no arquivo completo
SECAO_PATTERNS = {
    "O que é": [
        r"o que [eé]",
        r"o que entrega",
        r"descri[çc][aã]o",
        r"sobre o produto",
        r"overview",
    ],
    "Para quem": [
        r"para quem",
        r"\bicp\b",
        r"p[uú]blico.alvo",
        r"perfil de cliente",
        r"cliente ideal",
        r"a quem se destina",
    ],
    "Quando faz sentido vender": [
        r"quando faz sentido vender",
        r"sinais de compra",
        r"momento de compra",
        r"quando vender",
        r"gatilhos",
        r"\bmatch\b",
        r"quando abordar",
        r"oportunidade",
    ],
    "O que NÃO é": [
        r"o que n[aã]o [eé]",
        r"fora do escopo",
        r"n[aã]o inclui",
        r"limites",
        r"exclus[oõ]es",
    ],
    "Pré-requisito para": [
        r"pr[eé].requisito",
        r"depende de",
        r"antes deste produto",
    ],
    "Preço / Pacote": [
        r"pre[çc]o",
        r"\bcsp\b",
        r"investimento",
        r"pacote",
        r"valor",
        r"mensalidade",
    ],
}


def normalizar(texto):
    return texto.lower().strip()


def encontrar_secoes(conteudo):
    """Divide o markdown em dicionário {header: conteúdo_da_seção}."""
    secoes = {}
    header_atual = None
    linhas_secao = []

    for linha in conteudo.splitlines():
        match = re.match(r"^#{1,4}\s+(.+)", linha)
        if match:
            if header_atual is not None:
                secoes[header_atual] = "\n".join(linhas_secao).strip()
            header_atual = match.group(1).strip()
            linhas_secao = []
        else:
            if header_atual is not None:
                linhas_secao.append(linha)

    if header_atual is not None:
        secoes[header_atual] = "\n".join(linhas_secao).strip()

    return secoes


def eh_placeholder(texto):
    """Retorna True se o conteúdo for só comentário HTML de template."""
    limpo = re.sub(r"<!--.*?-->", "", texto, flags=re.DOTALL).strip()
    return len(limpo) < 20


def encontrar_melhor_secao(nome_radar, secoes):
    """Para cada nome de seção do radar, encontra a melhor seção equivalente no doc completo."""
    patterns = SECAO_PATTERNS.get(nome_radar, [])
    for pattern in patterns:
        for header, conteudo in secoes.items():
            if re.search(pattern, normalizar(header)):
                if not eh_placeholder(conteudo):
                    return conteudo
    return None


def titulo_do_arquivo(caminho: Path) -> str:
    """Usa o primeiro H1 do arquivo, ou o nome do arquivo formatado."""
    conteudo = caminho.read_text(encoding="utf-8")
    match = re.search(r"^#\s+(.+)", conteudo, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return caminho.stem.replace("-", " ").title()


def gerar_radar(arquivo: Path) -> bool:
    """Gera o arquivo -radar.md para um produto. Retorna True se gerou."""
    conteudo = arquivo.read_text(encoding="utf-8")
    secoes = encontrar_secoes(conteudo)

    if not secoes:
        print(f"  [skip] {arquivo.name} — sem seções encontradas")
        return False

    # Verifica se há conteúdo real além de placeholders
    conteudo_real = any(
        not eh_placeholder(v) for v in secoes.values()
    )
    if not conteudo_real:
        print(f"  [skip] {arquivo.name} — só tem placeholders de template")
        return False

    titulo = titulo_do_arquivo(arquivo)
    linhas = [f"# {titulo} — Radar de Upsell\n"]

    for nome_secao in SECAO_PATTERNS.keys():
        conteudo_secao = encontrar_melhor_secao(nome_secao, secoes)
        if conteudo_secao:
            linhas.append(f"## {nome_secao}\n")
            # Limita a 20 linhas por seção para manter compacto
            linhas_sec = conteudo_secao.splitlines()[:20]
            linhas.append("\n".join(linhas_sec))
            linhas.append("")

    if len(linhas) <= 1:
        print(f"  [skip] {arquivo.name} — nenhuma seção mapeável encontrada")
        return False

    radar_path = arquivo.parent / (arquivo.stem + "-radar.md")
    radar_path.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  [ok]   {radar_path.name}")
    return True


def main():
    print(f"Buscando produtos em: {REFERENCIAS_DIR}\n")

    arquivos = sorted(REFERENCIAS_DIR.glob("*.md"))
    candidatos = [
        f for f in arquivos
        if f.name not in IGNORAR
        and not f.stem.endswith("-radar")
    ]

    print(f"Encontrados: {len(candidatos)} arquivos de produto\n")
    gerados = 0
    pulados = 0

    for arq in candidatos:
        if gerar_radar(arq):
            gerados += 1
        else:
            pulados += 1

    print(f"\nConcluído: {gerados} radar(s) gerado(s), {pulados} pulado(s) (sem conteúdo)")
    if pulados > 0:
        print("→ Preencha o conteúdo nos arquivos pulados e rode o script novamente.")


if __name__ == "__main__":
    main()
