# Builders Hub

**O hub open-source de skills de IA da V4.** Um lugar onde V4ers compartilham skills que usam no dia a dia — account, tráfego, criativo, copy, coordenação, dados e áreas gerais.

> _"Builders of the Future"_ — construa, compartilhe, reutilize.

## O que tem aqui

- **Skills prontas** organizadas por papel ou fonte de dados (veja [REGISTRY.md](./REGISTRY.md))
- **Skills de setup** pra você configurar seu ambiente sem saber git
- **Templates** de KB pra organizar squads, clientes e projetos
- **Mission Control de cliente** pra manter OKRs, apostas vivas, combinados, personas e histórico de check-ins
- **Padrão compartilhado**: funciona no Claude Code e no Anti-Gravity

## Como começar (3 passos)

### 1. Baixe o repo

```bash
git clone https://github.com/V4-Company/builders-hub.git
cd builders-hub
```

Use um clone Git. O ZIP serve apenas para leitura e não permite `/sync-hub`, commits ou PRs.

### 2. Abra no Anti-Gravity (ou Claude Code)

- Anti-Gravity: `File > Open Folder` → selecione `builders-hub`
- Abra o terminal (`Cmd+~` ou `Ctrl+~`)

### 3. Rode o onboarding

```
/onboarding
```

Valida git/GitHub CLI/dependências 100%, instala o que faltar, e te guia pelo resto: primeiro cliente/projeto, primeiras skills, fluxo de trabalho. Pode rodar de novo sempre que algo quebrar — os checks que já passaram voam.

Para usar scripts de integração diretamente, instale também as dependências Python:

```bash
python3 -m pip install -r requirements.txt
```

## Skills principais

| Skill | O que faz |
|---|---|
| `/onboarding` | Configura tudo e te ensina o fluxo V4 |
| `/sync-hub` | Atualiza suas skills com o que o time compartilhou |
| `/compartilhar-skill` | Empacota uma skill sua e manda pro Hub (abre PR automático) |
| `/criador-de-skills` | Cria skill nova do zero com prefixo de papel ou fonte |
| `/contexto` | Lê uma KB, gera CLAUDE.md/AGENTS.md e atualiza Mission Control quando for cliente |
| `/novo-squad` | Cria um squad antes do primeiro cliente |
| `/novo-cliente` | Cria cliente dentro de um squad com `calls/`, `checkins/`, `docs/`, `campanhas/` e `links.md` |
| `/novo-projeto` | Cria uma KB genérica em `bases/` |
| `/geral-brainstormar-sobre-minha-funcao` | Descobre onde IA agrega mais valor no seu dia |
| `/geral-sabatina` | Stress-test de planos e ideias |
| `/geral-discovery-produto` | Transforma evidências dispersas em decisões de produto e oferta |
| `/geral-backup-kb-drive` | Espelha uma KB no Drive com checagem de permissão e de segredos |

## Skills de account e check-in

| Skill | Quando usar |
|---|---|
| `/account-handoff` | Primeiro fluxo quando um cliente sai de vendas. Gera KB preliminar, Mission Control preliminar e deck HTML de kickoff. |
| `/account-pesquisa-profunda-cliente` | Pesquisa profunda depois que dados internos mínimos já estão na KB. |
| `/account-checkin-roleplay` | Antes do check-in. Prepara ROPRE, simula o cliente real e salva o ensaio em `checkins/`. |
| `/account-checkin-review` | Depois do check-in. Lê o transcript, atualiza Mission Control e salva review em `checkins/`. |

Fluxo recomendado de cliente:

```text
/novo-squad
/novo-cliente
/account-handoff
/contexto
/account-checkin-roleplay   # antes da call
/account-checkin-review     # depois da call
```

Todas as skills compartilhadas pelo time ficam em [REGISTRY.md](./REGISTRY.md).

## Convenção de nomes

Toda skill compartilhada tem prefixo de papel ou de fonte:

- `geral-*` — qualquer papel
- `gt-*` — gestor de trafego
- `designer-*` — design
- `copy-*` — copy
- `account-*` — relacionamento, check-in, pesquisa profunda, handoff
- `coord-*` — coordenacao

Skills **puxadoras de dados** (libraries de fonte) usam prefixo da integração:

- `v4mos-*` — V4mos / V4mkt (Meta Ads, Google Ads, CRMs agregados)
- `google-*` · `ga4-*` · `meta-*` — APIs diretas
- `hubspot-*` · `kommo-*` — CRMs
- `shopify-*` · `tray-*` — e-commerce

Exemplo: `gt-analise-anomalias`, `account-checkin-roleplay`, `v4mos-dados-meta-ads`.

## Estrutura do repo

```
builders-hub/
├── README.md                 # esse arquivo
├── REGISTRY.md               # catálogo auto-gerado de skills
├── CONTRIBUTING.md           # como contribuir
├── CLAUDE.md · AGENTS.md     # instruções pra IA
├── .claude/skills/           # skills pro Claude Code
├── .agents/skills/           # skills pro Anti-Gravity (espelho)
├── squads/                   # squads e KBs de clientes (gitignored)
├── bases/                    # seus KBs de projetos (gitignored)
├── docs/                     # guias e specs
├── tests/                    # testes automatizados do repositorio
├── tutorial.html             # guia visual do hub
├── requirements.txt          # dependencias dos scripts de integracao
└── scripts/                  # geracao do registry e validacao estrutural
```

Clientes vivem em `squads/{squad}/clientes/{cliente}/`. Dentro de cada cliente:

```text
calls/             # transcripts brutos
checkins/          # pautas, ensaios, reviews e materiais finais de check-in
docs/              # briefings, propostas, contratos, apresentacoes
campanhas/         # dados de campanhas
mission-control/   # OKRs, apostas vivas, combinados, personas e historicos
CLAUDE.md/AGENTS.md
links.md
```

`calls/`, `checkins/` e `mission-control/` têm papéis diferentes:

- `calls/`: matéria-prima bruta, principalmente transcripts.
- `checkins/`: entregáveis de condução e melhoria, como pauta ROPRE, ensaio, review e relatório.
- `mission-control/`: estado vivo usado pelas skills, como OKRs, apostas vivas, combinados e personas.

**Importante:** `squads/` e `bases/` são seus — ficam no seu computador, nunca sobem pro repo público (estão no `.gitignore`, exceto templates).

## Arquivos de contexto

O hub usa dois arquivos de instrução:

- `CLAUDE.md`: lido pelo Claude Code.
- `AGENTS.md`: lido por Codex/Anti-Gravity/outros agentes.

Sempre que uma skill criar ou atualizar contexto duradouro, os dois devem ficar alinhados.

## Configuração e segurança

- Copie `.env.example` para `.env` apenas dentro da KB que precisa da integração.
- Nunca preencha nem commite `.env.example`; ele documenta somente os nomes das variáveis.
- A integração V4mos usa `V4MOS_CLIENT_ID`, `V4MOS_CLIENT_SECRET` e `V4MOS_WORKSPACE_ID`.
- Arquivos `*.local.json`, `squads/`, KBs de `bases/` e credenciais são ignorados pelo Git.
- O script `scripts/validate-repo.py` confere duplo-write, frontmatters, arquivos locais rastreados e padrões de segredo de alta confiança.

## Desenvolvimento e validação

Antes de abrir um PR:

```bash
python3 scripts/build-registry.py
python3 scripts/validate-repo.py
python3 scripts/build-registry.py --check
python3 scripts/run-tests.py
```

Skills que têm testes próprios guardam os casos em `.claude/skills/<skill>/tests/`. A CI executa esses testes, compila os scripts Python e faz um smoke test da CLI V4mos.

## Atualização e operação

Este repositório é uma biblioteca de skills e KBs locais: não há servidor, banco de dados, migrations ou build de produção para publicar. Em uma máquina limpa, clone o repositório, instale `requirements.txt` e rode `/onboarding`. Para atualizar, use `/sync-hub` ou faça `git pull` na sua cópia; não existe processo que precise ser reiniciado.

## Contribuir

Tem uma skill que funciona bem? Compartilha com o time:

```
/compartilhar-skill
```

A skill empacota, valida, cria branch, abre PR. Você só aprova no final. Detalhes em [CONTRIBUTING.md](./CONTRIBUTING.md).

## Links

- **Aula 1 Foundation**: https://aula-1-foundation.vercel.app
- **Anti-Gravity**: https://antigravity.dev
- **Claude Code**: https://code.claude.com

---

_V4 Company · Builders of the Future_
