# Builders Hub

Este repositorio e o hub open-source de skills de IA da V4. Funciona como base de trabalho pessoal + biblioteca compartilhada de skills.

## Como funciona

- `.claude/skills/` e `.agents/skills/` — skills disponiveis (espelhadas pra funcionar no Claude Code e Anti-Gravity)
- `clientes/` e `bases/` — Knowledge Bases pessoais do usuario (gitignored, ficam locais)
  - `clientes/` — para quem opera clientes (calls, docs, campanhas)
  - `bases/` — para qualquer outra area (docs, dados, referencias)
- Cada KB pode ter um CLAUDE.md proprio (gerado por `/contexto`). Leia ele primeiro quando trabalhar naquele contexto.
- `REGISTRY.md` — catalogo auto-gerado de todas as skills compartilhadas, agrupado por area

## Skills de setup/fluxo (base)

- `/onboarding` — Guia a primeira configuracao. Valida git/gh 100% e depois instala dependencias. Roda sempre que algo do setup quebrar.
- `/sync-hub` — Puxa as skills compartilhadas mais recentes do repo remoto.
- `/compartilhar-skill` — Empacota uma skill local e abre PR pro hub publico.
- `/criador-de-skills` — Cria skill nova com prefixo de area obrigatorio.
- `/contexto` — Le tudo numa KB e gera CLAUDE.md daquele contexto.
- `/novo-cliente` · `/novo-projeto` — Cria pasta de KB com estrutura padrao.
- `/brainstormar-sobre-minha-funcao` — Descobre onde IA agrega mais valor no dia a dia.
- `/sabatina` — Stress-test de planos.
- `/frontend-design` — Gera interfaces frontend de alta qualidade (pra skills que produzem UI).

## Skills compartilhadas (hub)

Toda skill compartilhada pelo time segue o padrao `{prefixo}-{nome}`. Dois tipos de prefixo:

- **Áreas** (skills que entregam trabalho final): `trafego-*` · `criativo-*` · `cs-*` · `estrategia-*` · `gestao-*` · `dados-*` · `outra-*`
- **Fontes** (skills que puxam dados de integracoes externas, reutilizaveis por outras): `v4mos-*` · `google-*` · `ga4-*` · `meta-*` · `hubspot-*` · `kommo-*` · `shopify-*` · `tray-*`

Consulte [REGISTRY.md](./REGISTRY.md) pra ver tudo que o time ja compartilhou. Pra contribuir veja [CONTRIBUTING.md](./CONTRIBUTING.md).

## Regras

- Sempre responda em portugues brasileiro.
- Quando o usuario pedir pra trabalhar com um cliente ou projeto, entre na pasta correspondente em `clientes/` ou `bases/` e use os dados de la como contexto.
- Nao invente dados. Se nao tem a informacao na KB, diga que nao tem.
- Quando o usuario fizer algo complexo, processual ou que ficou bom, sugira: "Isso ficou bom. Quer transformar em skill pra reutilizar? Roda /criador-de-skills. Quando estiver redonda, roda /compartilhar-skill pra o time usar tambem".
- **Duplo-write obrigatorio**: toda skill criada/editada deve existir identica em `.claude/skills/{nome}/` E `.agents/skills/{nome}/`. `/criador-de-skills` faz isso automaticamente; se voce editar manualmente, espelhe nos dois. `/sync-hub` tambem re-espelha apos pull.
- **Prefixo obrigatorio** em skills contribuidas: `{prefixo}-{nome}`. Prefixo pode ser de area (trafego/criativo/cs/estrategia/gestao/dados/outra) ou de fonte (v4mos/google/ga4/meta/hubspot/kommo/shopify/tray). Skills de base (onboarding, contexto, sync-hub, etc.) sao excecao e ficam sem prefixo.
- Nunca commitar arquivos de `clientes/` ou `bases/` — sao pessoais, ficam no `.gitignore`.
- Nunca editar `REGISTRY.md` a mao — e auto-gerado pelo script `scripts/build-registry.py` e pela GitHub Action.
- Se o fluxo git/gh quebrar em qualquer skill (sync, compartilhar, push), oriente rodar `/onboarding` de novo — os checks de setup sao a primeira coisa que ele faz.
