# Builders Hub

**O hub open-source de skills de IA da V4.** Um lugar onde V4ers compartilham skills que usam no dia a dia — tráfego, criativo, CS, estratégia, gestão, dados.

> _"Builders of the Future"_ — construa, compartilhe, reutilize.

## O que tem aqui

- **Skills prontas** organizadas por área (veja [REGISTRY.md](./REGISTRY.md))
- **Skills de setup** pra você configurar seu ambiente sem saber git
- **Templates** de KB (clientes / bases) pra organizar seu trabalho
- **Padrão compartilhado**: funciona no Claude Code e no Anti-Gravity

## Como começar (3 passos)

### 1. Baixe o repo

```bash
git clone https://github.com/V4-Company/builders-hub.git
cd builders-hub
```

Ou baixe o ZIP pelo GitHub.

### 2. Abra no Anti-Gravity (ou Claude Code)

- Anti-Gravity: `File > Open Folder` → selecione `builders-hub`
- Abra o terminal (`Cmd+~` ou `Ctrl+~`)

### 3. Rode o onboarding

```
/onboarding
```

Valida git/GitHub CLI/dependências 100%, instala o que faltar, e te guia pelo resto: primeiro cliente/projeto, primeiras skills, fluxo de trabalho. Pode rodar de novo sempre que algo quebrar — os checks que já passaram voam.

## Skills principais

| Skill | O que faz |
|---|---|
| `/onboarding` | Configura tudo e te ensina o fluxo V4 |
| `/sync-hub` | Atualiza suas skills com o que o time compartilhou |
| `/compartilhar-skill` | Empacota uma skill sua e manda pro Hub (abre PR automático) |
| `/criador-de-skills` | Cria skill nova do zero com prefixo de área |
| `/contexto` | Lê uma KB e gera CLAUDE.md com o contexto |
| `/novo-cliente` · `/novo-projeto` | Cria pasta com estrutura padrão |
| `/brainstormar-sobre-minha-funcao` | Descobre onde IA agrega mais valor no seu dia |
| `/sabatina` | Stress-test de planos e ideias |

Todas as skills compartilhadas pelo time ficam em [REGISTRY.md](./REGISTRY.md).

## Convenção de nomes

Toda skill tem prefixo de área:

- `trafego-*` — gestão de mídia, análise de contas, anomalias
- `criativo-*` — copy, briefing, design, LPs
- `cs-*` — check-in, relatório, playbook, transcrição
- `estrategia-*` — diagnóstico, planejamento, pesquisa
- `gestao-*` — reuniões, tasks, overview
- `dados-*` — análise, dashboards, insights

Além das áreas, skills **puxadoras de dados** (libraries de fonte) usam prefixo da integração:

- `v4mos-*` — V4mos / V4mkt (Meta Ads, Google Ads, CRMs agregados)
- `google-*` · `ga4-*` · `meta-*` — APIs diretas
- `hubspot-*` · `kommo-*` — CRMs
- `shopify-*` · `tray-*` — e-commerce

Exemplo: `trafego-analise-anomalias`, `cs-checkin-ppt`, `v4mos-dados-meta-ads`.

## Estrutura do repo

```
builders-hub/
├── README.md                 # esse arquivo
├── REGISTRY.md               # catálogo auto-gerado de skills
├── CONTRIBUTING.md           # como contribuir
├── CLAUDE.md · AGENTS.md     # instruções pra IA
├── .claude/skills/           # skills pro Claude Code
├── .agents/skills/           # skills pro Anti-Gravity (espelho)
├── clientes/                 # seus KBs de clientes (gitignored)
├── bases/                    # seus KBs de projetos (gitignored)
├── docs/                     # guias
└── scripts/build-registry.sh # regenera REGISTRY.md
```

**Importante:** `clientes/` e `bases/` são seus — ficam no seu computador, nunca sobem pro repo público (estão no `.gitignore`).

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
