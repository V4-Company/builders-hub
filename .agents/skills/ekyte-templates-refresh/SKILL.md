---
name: ekyte-templates-refresh
description: Atualiza, adiciona ou ajusta os templates de briefing por sigla usados pela `/ekyte-briefing` em `clientes/_skill-ekyte/briefing-templates/`. Use quando o Fabio rodar `/ekyte-templates-refresh`, mencionar que quer "criar template novo" pra uma sigla que ainda não tem (ex: KV, MT, EM, EV), "ajustar o template de CA" pra adicionar/remover seção, ou quando rodar 5 tasks reais e quiser refinar perguntas/campos.
area: ekyte
author: fabio
version: 1.0.0
user-invocable: true
---

# /ekyte-templates-refresh — Manutenção dos templates de briefing

Cuida do diretório `clientes/_skill-ekyte/briefing-templates/`. Adicionar sigla nova, ajustar template existente, ou propagar uma melhoria pra múltiplos templates.

## Quando usar

- `/ekyte-templates-refresh` (direto)
- "cria template pro KV" / "preciso de template pra MT (Motion)"
- "no template de CA, adiciona pergunta sobre [X]"
- "remove a seção [Y] do PC"
- "depois de 5 tasks, quero refinar o template de CA"

## Pré-requisitos

- Diretório `clientes/_skill-ekyte/briefing-templates/` existente, com pelo menos:
  - `_header-universal.md`
  - `_base-criativo.md`
  - `_5w1h.md`
  - `CA.md`, `LP.md`, `RV.md`, `PC.md`, `AN.md`, `CRM.md`

## Fluxo

### 1) Identificar a operação

```
O que você quer fazer?

1) Adicionar template novo (sigla que ainda não tem .md)
2) Ajustar template existente (adicionar/remover/modificar seção ou pergunta)
3) Atualizar arquivo compartilhado (_header-universal, _base-criativo, _5w1h)
4) Listar templates atuais (saber o que já existe)
```

### 2) Modo "Adicionar template novo"

Perguntar:
- **Sigla** (ex: `MT`, `EM`, `KV`)
- **Tipo de tarefa** (nome legível, ex: "Motion", "E-mail Marketing")
- **task_type_id** (puxar do `cache.md` se já existe; se não, perguntar)
- **Família** (qual base usar):
  - Criativo (importa `_base-criativo.md`) → CA, LP, RV, KV, MT, EV, DC, DLP, DE, AC, OCA, SM, EM, PAPP, PI, PMS, PPSH, PSMS, PWPP
  - Operacional (só `_header-universal.md`) → PC, RI, EKT, REL, OVERVIEW
  - Analítica (só `_header-universal.md`, sem KV) → AN, AUX
  - CRM/Relacionamento (`_header-universal.md` + bloco extra de infra CRM) → CRM, ACRM, ATM, CB
  - Outra → criar do zero, perguntar estrutura

Skill propõe um esqueleto baseado na família + perguntas comuns + perguntas específicas que **Fabio** define. Mostra preview do template antes de salvar.

### 3) Modo "Ajustar template existente"

Perguntar:
- Qual sigla ajustar?
- Qual tipo de ajuste:
  - Adicionar seção/pergunta nova
  - Remover seção/pergunta
  - Modificar pergunta (texto, opções, default)
  - Reordenar seções

Mostrar diff (linhas antes/depois) antes de aplicar.

### 4) Modo "Atualizar arquivo compartilhado"

`_header-universal.md`, `_base-criativo.md`, `_5w1h.md`. **Cuidado redobrado** — mudança aqui afeta TODOS os templates que importam.

Avisar: "Esta mudança vai afetar os templates X, Y, Z. Confirma?"

### 5) Modo "Listar templates atuais"

Output:
```
📂 Templates em clientes/_skill-ekyte/briefing-templates/

Compartilhados:
  • _header-universal.md (vai em todo briefing)
  • _base-criativo.md (CA, LP, RV)
  • _5w1h.md (modo plano de ação)

Por sigla:
  • CA.md — Criativo Ads
  • LP.md — Landing Page
  • RV.md — Roteiro de Vídeo
  • PC.md — Publicação de Campanha
  • AN.md — Análise de Dados
  • CRM.md — CRM / Relacionamento

Siglas SEM template ainda (cairão no fallback genérico):
  • KV, MT, EV, EM, OCA, SM, ... (lista do cache.md filtrando os que já existem)
```

### 6) Salvar e reportar

Diff antes de cada Write/Edit. Após salvar:
```
✅ Template atualizado:
  - clientes/_skill-ekyte/briefing-templates/CA.md (3 linhas adicionadas)
```

## Guardrails

1. **Diff obrigatório.** Antes de qualquer Write/Edit, mostrar mudanças linha-a-linha.
2. **Mudança em compartilhado afeta múltiplos.** Listar templates afetados antes.
3. **Não criar template duplicado** sem confirmação. Se sigla já tem `.md`, perguntar se é pra sobrescrever ou se é variante (ex: `CA-v4s.md` pra task_type_id 37979).
4. **Manter o padrão de conversão Markdown→HTML.** Toda nova seção precisa seguir as regras: `<div>` por linha, `<strong>` em CAIXA ALTA pra título de seção, sem `<h>`/`<p>`/`<ul>`.
5. **Validar referências cruzadas.** Se template importa `_base-criativo.md`, ele precisa existir. Se referência sigla mas pula uma seção dela, alertar.

## Como invocar

- `/ekyte-templates-refresh` (direto).
- "cria template pro [SIGLA]".
- "ajusta o template de [SIGLA]".

## O que NÃO fazer

- Não tocar em `drives.md` ou `backups-crm.md` (use `/ekyte-briefing-refresh`).
- Não tocar em `cache.md` (use `/ekyte-refresh`).
- Não escrever templates sem validar a família primeiro (cliente vai querer brieffar uma analítica como criativo se template estiver errado).
- Não esquecer da regra de KV: aplicável **só** pra siglas criativas (CA/LP/RV/etc). Templates analíticos/operacionais omitem KV.
