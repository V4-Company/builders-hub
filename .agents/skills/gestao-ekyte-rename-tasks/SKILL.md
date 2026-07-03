---
name: gestao-ekyte-rename-tasks
description: Renomeia títulos de tarefas no Ekyte em lote via MCP oficial (update_task) com fallback PATCH REST. Aceita lista de IDs ou filtro (projeto, workspace, tipo). Operações find-replace (ex: [WEB]→[P&P], V4 Company→V4 Company Colli & Co). Output: relatório com sucessos/falhas por task. Use sempre que precisar renomear múltiplas tasks de uma vez — é muito mais rápido que editar uma por uma na UI.
area: gestao
author: fabio
version: 2.0.0
---

# Gestão — Renomear Tasks Ekyte em Lote

Edita títulos de múltiplas tarefas no Ekyte em paralelo. Ideal para operações de rename em lote: mudar tags (ex: `[WEB]` → `[P&P]`), atualizar nomes de clientes, padronizar prefixos, etc.

## Os dois MCPs do Ekyte

A partir de 2026-06 há **dois servidores MCP do Ekyte** configurados (`~/.claude/mcp.json`):

| Servidor | Prefixo das tools | Uso |
|---|---|---|
| `ekyte-oficial` (`api.ekyte.com`) | `mcp__ekyte-oficial__*` | **Escrita/edição** — `update_task`, `update_task_phase`, `update_task_responsibles`, `create_task`, comentários. Token fixo na URL (não expira a cada uso). |
| `ekyte` (n8n) | `mcp__ekyte__*` | **Leitura/BI** — insights, performance por fase, BI de projetos/workspaces, time tracking por dia. |

Para esta skill (rename = escrita), o caminho **primário** é `mcp__ekyte-oficial__update_task`. O PATCH REST cru (com JWT manual) vira **fallback** caso o MCP oficial esteja indisponível.

## Pré-requisitos

- **Caminho primário (recomendado):** MCP `ekyte-oficial` ativo. Não precisa de token manual — ele já vai na URL do servidor. Confirme que as tools `mcp__ekyte-oficial__update_task` / `mcp__ekyte-oficial__list_tasks` estão disponíveis na sessão.

- **Fallback (REST):** `Token Ekyte` em `clientes/_skill-ekyte/.env`:
  ```
  EKYTE_TOKEN=eyJhbGc...
  EKYTE_COMPANY_ID=3597
  EKYTE_API_BASE=https://api.ekyte.com/api/v2
  ```
  Só necessário se for usar o fallback REST. Veja "Setup do Token" no final.

- **IDs das tasks** a renomear — obtém via `mcp__ekyte-oficial__list_tasks` (ou `mcp__ekyte__list_tasks`). Use o `id`/`taskId` retornado pela listagem, não o id da criação.

## Como usar

### Modo 1: IDs explícitos + find-replace

Passe uma lista de IDs e operações find-replace:

```
Renomeia as seguintes tasks no Ekyte (IDs: 9342321, 9342322, 9342323):
- Troca: [WEB] → [P&P]

Tira um relatório com sucessos e falhas.
```

Skill vai:
1. Buscar título atual de cada task via GET
2. Aplicar find-replace
3. Disparar PATCH em paralelo
4. Retornar relatório: ✅ 3/3 ok, 0 falhas

### Modo 2: Filtro + find-replace

Se não tiver IDs na mão, pedida filtro (projeto, workspace, tipo) e a skill lista as tasks:

```
No projeto "People & Performance" (workspace V4 Company), renomeia:
- Troca: V4 Company | → V4 Company Colli & Co |
```

Skill vai:
1. Listar tasks do projeto via `listar_tarefas_tool`
2. Extrair IDs
3. Aplicar rename
4. Retornar relatório

## Operações suportadas

- **Find-replace simples**: `[WEB]` → `[P&P]`, `V4 Company` → `V4 Company Colli & Co`
- **Múltiplas substituições em sequência**: lista de find-replace é aplicada na ordem
- **Case-sensitive**: respeita maiúsculas/minúsculas no pattern

Exemplos:
- `Substitui: "Urgente -" → ""`  (remove prefixo)
- `Substitui: "[01]" → "[02]"`  (altera quantity prefix)
- `Substitui: "Cliente A |" → "Cliente A |"` (expande nome curto)

## Output esperado

Relatório estruturado:
```
✅ SUCCESSO: 22 tasks renomeadas
   • 9342321: [01][P&P][IA] V4 Company Colli & Co | Política de Paternidade
   • 9342322: [01][P&P][IA] V4 Company Colli & Co | Ferramentas para TAs
   ...
   • 9342342: [01][P&P][IA] V4 Company Colli & Co | PCI — Social Media

⏱️ Tempo total: ~5s (22 tasks em paralelo)
```

Ou se tiver falhas:
```
⚠️ PARCIAL: 20/22 ok, 2 falhas

✅ OK (20):
   • 9342321: ...

❌ FALHAS (2):
   • 9342350 (HTTP 500): título não pode ser vazio
   • 9342351 (HTTP 401): token expirado
```

## Detalhes técnicos

### Caminho primário — MCP oficial `update_task`

A tool `mcp__ekyte-oficial__update_task` recebe **o mesmo JSON Patch** que o PATCH REST, sem token manual:

```
mcp__ekyte-oficial__update_task(
  taskId: 9342321,                                              // integer, da listagem
  patchDoc: [{"op":"replace","path":"/title","value":"novo título"}]
)
```

- `taskId` = id da task (inteiro). `patchDoc` = array de operações JSON Patch RFC 6902 — idêntico ao body REST.
- Disparar várias chamadas em paralelo (uma por task) numa mesma mensagem.
- Acentos e `&` vão literais no `value` — o MCP cuida do encoding, sem `--data-binary`.
- Antes de renomear, busque o título atual via `mcp__ekyte-oficial__list_tasks` (ou `get_detailed_task`) e aplique o find-replace sobre ele.

### Fallback — PATCH REST (só se o MCP oficial estiver fora)

**Endpoint usado:**
```
PATCH https://api.ekyte.com/api/v2/companies/{company_id}/ctc-tasks/{task_id}?type=grid&updateAllTickets=undefined
```

**Headers:**
- `Authorization: Bearer {EKYTE_TOKEN}`
- `Content-Type: application/json`
- `Origin: https://app.ekyte.com`
- `Referer: https://app.ekyte.com/`

**Body (JSON Patch RFC 6902):**
```json
[{"op":"replace","path":"/title","value":"novo título"}]
```

**Encoding crítico:** payload é enviado via `--data-binary @file` com bytes UTF-8 corretos. Acentos + `&` devem ser literais no JSON, não escapados.

## Setup do Token

Se não tiver `EKYTE_TOKEN` em `.env`:

1. Abre `https://app.ekyte.com` e faz login
2. F12 → aba **Network** → filtra por `api.ekyte`
3. Clica em qualquer task → edita o título → salva
4. Procura na Network pela request `9342XXX?type=grid&updateAllTickets=undefined` (POST/PATCH)
5. Headers → `Authorization: Bearer eyJhbGc...` → copia só o JWT (sem "Bearer ")
6. Cola em `clientes/_skill-ekyte/.env`:
   ```
   EKYTE_TOKEN=eyJhbGc...
   ```

Token vale ~180 dias. Quando expirar (skill retorna HTTP 401), renova repetindo os passos acima.

## Limitações

- **Sem validação de título**: se o novo título viola regras do Ekyte (vazio, caracteres inválidos), a task falha (HTTP 400/422). Revise o find-replace antes de rodar.
- **Sem undo**: renames são imediatos e permanentes. Se precisar reverter, pode rodar a skill de novo com find-replace inverso.
- **Sem garantia de idempotência**: se rodar a skill 2× com mesmo find-replace, a segunda rodada faz nada (ou encontra o novo título e tenta "substituir" de novo, resultando em noop).

## Exemplos reais

**Exemplo 1: Rename de tags**
```
IDs: 9342321 a 9342342 (22 tasks People & Performance)
Substitui: [WEB] → [P&P]
```
Resultado: 22/22 ok em ~5s

**Exemplo 2: Atualizar nome de cliente**
```
Projeto: "Cliente A | Q2/2026"
Substitui: "Cliente A" → "Cliente A — Novembro"
```
Resultado: 15/15 ok (todas as tasks do projeto Cliente A atualizadas)

**Exemplo 3: Cleanup de urgência**
```
Workspace: V4 Company
Substitui: "🔴 URGENTE — " → ""
```
Resultado: 8/8 ok (remove prefix antigo de urgência)

---

**Quando usar essa skill:**
- Múltiplas tasks (3+) pra renomear — evita UI click-by-click
- Find-replace repetitivo (mesma operação em lote)
- Lotes de geração automática onde prefixo/suffix precisa atualizar

**Quando NÃO usar:**
- 1-2 tasks — mais rápido editar direto na UI
- Edições complexas (alterar responsável, prazo, fase, briefing) — agora possíveis via MCP oficial: `mcp__ekyte-oficial__update_task_responsibles`, `update_task_phase`, ou `update_task` com o `patchDoc` apontando o campo certo. Esta skill cobre só título; para o resto, chame essas tools direto.
