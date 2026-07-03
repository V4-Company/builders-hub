---
name: ekyte-refresh
description: Atualiza o cache local da skill ekyte-task — re-busca workspaces fixos, projetos do trimestre vigente para cada cliente, tipos de tarefa do workflow "Padrão Colli&Co (Oficial)", e regenera o cache de fluxos (fases por tipo) via MCP oficial. Use quando o Fabio rodar /ekyte-refresh, disser que entrou cliente novo, projeto novo, que mudou fluxo/fase de algum tipo, ou que o cache parece desatualizado.
area: ekyte
author: fabio
version: 1.0.0
user-invocable: true
---

# /ekyte-refresh — Atualizar cache do ekyte

Re-popula `clientes/_skill-ekyte/cache.md` puxando dados frescos da MCP `ekyte`. Roda em <2 minutos.

## Quando usar

- `/ekyte-refresh` (invocação direta)
- "atualiza o cache do ekyte"
- "entrou cliente novo, atualiza"
- "projeto Q3/2026 começou, atualiza"
- Cache com mais de 30 dias

## Pré-requisitos

- MCP `ekyte` configurada
- Arquivo `clientes/_skill-ekyte/cache.md` existente (criado pela skill `/ekyte-task`)

## Fluxo

### 1) Confirmar trimestre vigente

Calcular trimestre atual com base na data de hoje:
- Jan/Fev/Mar → Q1
- Abr/Mai/Jun → Q2
- Jul/Ago/Set → Q3
- Out/Nov/Dez → Q4

Mostrar pro Fabio: "Vou atualizar o cache pro **Q2/2026**. Confirma?"

### 2) Workspaces

Os 8 workspaces fixos não mudam (já estão hardcoded no cache). Pular esta etapa, a menos que o Fabio mencione cliente novo. Nesse caso:
- Perguntar nome do cliente novo
- Chamar `ekyte.listar_workspaces_tool({"name_list_workspaces": "<nome>", "squad_id_list_workspaces": "", "situation_id_list_workspaces": "1"})`
- Confirmar com o Fabio qual é o ID certo (pode vir múltiplos)
- Adicionar ao cache

### 3) Projetos do trimestre vigente para cada workspace

Para cada um dos 8 workspaces:
- Chamar `ekyte.listar_projetos_tool` com:
  - `workspace_id_list_projects`: ID do workspace
  - `created_from_list_projects`: data 90 dias antes do início do trimestre (margem)
  - `created_to_list_projects`: data de hoje
- Filtrar projetos cujo nome contém `Q2/2026` (ou trimestre vigente)
- Salvar `project_id` no cache

Se um workspace não tiver projeto do trimestre: avisar o Fabio ("Cliente A não tem projeto Q2/2026 — quer que eu pule ou tem nome diferente?")

### 4) Tipos de tarefa

Chamar `ekyte.listar_tipos_de_tarefas_tool({"name_type_task": "", "parameters1_Value": "3535"})` (workflow Padrão Colli&Co Oficial).

Filtrar tipos cujo nome casa o regex `^\[\d+\]\[([A-Z]+)\]`.

Atualizar a tabela do cache com qualquer tipo novo. **Não remover** entradas existentes (podem aparecer em desambiguação).

### 4.5) Fluxos por tipo (regenerar `flows.md`)

Regenera `clientes/_skill-ekyte/flows.md` — as fases reais de cada tipo (com `phaseId`) + dicionário `nome da fase → phaseId`, usado pela `/ekyte-task` pra trocar responsável de etapa (passo 9.6 de lá).

Roda o script bundlado (lê o token do MCP oficial direto do `~/.claude/mcp.json` — sem segredo no repo; parseia os tipos do `cache.md`; usa `get_task_type_flow` e fica só com fases `effort/duration > 0`):

```bash
python ".claude/skills/ekyte-refresh/scripts/fetch_flows.py"
```

- Rode **depois** do passo 4 (assim qualquer tipo novo já entra no `flows.md`).
- Precisa do MCP `ekyte-oficial` configurado. Se faltar, o script avisa e você pula esta etapa (o resto do refresh segue).
- Saída esperada: `OK -> ...flows.md: N/N tipos, M fases distintas`. Se algum tipo der `ERR`, ele entra no `flows.md` marcado com ⚠️ e o resto continua.
- Paths customizados: `--cache "<...>"` / `--out "<...>"` (defaults relativos à raiz do repo).

### 5) Salvar e reportar

Atualizar `clientes/_skill-ekyte/cache.md`:
- Atualizar campo "Última atualização total" no topo
- Reescrever as seções que mudaram

Reportar pro Fabio:
```
✅ Cache atualizado:
  - 8 workspaces (sem mudanças)
  - <N> projetos Q2/2026 descobertos
  - <M> tipos de tarefa (<+X> novos)
  - flows.md regenerado (<T> tipos, <P> fases distintas)
```

## O que NÃO fazer

- Não rodar refresh sem confirmação do trimestre.
- Não criar workspaces, projetos ou tipos. Skill é read-only no ekyte.
- Não apagar entradas do cache automaticamente (preservar histórico de IDs).
