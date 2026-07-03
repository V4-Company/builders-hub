---
name: gestao-ekyte-tags
description: Aplica etiquetas (tags) padronizadas em tarefas do Ekyte em lote via MCP oficial, seguindo o Playbook de Tags da Colli & Co. Dois modos — ROTINA (rotina + semana, ex: SPRINT GROWTH + SEMANA 23) e TIPO de entregável (LANDING PAGE, Criativo Ads). Faz merge seguro com as tags atuais (nunca sobrescreve), resolve IDs automaticamente e mostra preview antes de aplicar. Use sempre que precisar taguear tarefas de rotina (Sprint Growth, Weekly Expansão, Ação Gerencial, Quality Control, WAR, Alinhamento Comitê), marcar a semana do ano, ou etiquetar entregáveis de landing page / criativo ads — em uma ou várias tasks de uma vez.
area: gestao
author: fabio
version: 1.0.0
---

# Gestão — Tags/Etiquetas no Ekyte em Lote

Aplica tags padronizadas em tarefas do Ekyte respeitando o **Playbook de Tags da Colli & Co**. Substitui o trabalho manual de abrir task por task na UI por: resolver IDs → merge com as tags atuais → preview → aplicar em paralelo.

A regra de ouro vem do comportamento da API: **`update_task_tags` SUBSTITUI a lista inteira de tags da task.** Se você mandar só a tag nova, apaga todas as outras. Por isso esta skill **sempre** lê as tags atuais e envia o conjunto completo (atuais + novas). Errar isso = perder tag de cliente. É o coração da skill.

## Pré-requisitos

- MCP `ekyte-oficial` (`api.ekyte.com`) ativo em `~/.claude/mcp.json` — token fixo na URL, autentica a empresa Colli (companyId 3597). Tools usadas: `mcp__ekyte-oficial__list_tags`, `mcp__ekyte-oficial__get_detailed_task`, `mcp__ekyte-oficial__update_task_tags`.
- **IDs das tasks** a taguear — você passa, ou a skill lista por filtro (projeto/workspace) via `mcp__ekyte-oficial__list_tasks`. Sempre filtrar: `list_tasks` sem filtro e com `limit:200` **dá timeout** na conta Colli.

> Os dois MCPs do Ekyte: `ekyte-oficial` (escrita — esta skill) e `ekyte` n8n (leitura/BI). Ver `gestao-ekyte-rename-tasks` para o contexto completo.

## Os dois modos

### Modo ROTINA (governado pelo Playbook)

Toda tarefa que nasce de uma rotina recorrente leva **exatamente duas tags**: a tag da **rotina** + a tag da **semana do ano**. Isso é o que deixa coordenador/gestor filtrar no "Controle de Tarefas" com cláusula **E** (rotina + semana) e validar o que cada squad subiu na semana.

**Tags de rotina** (permanentes, IDs sequenciais 250506–250511):

| Rotina | Tag no Ekyte | ID |
|---|---|---|
| Ação Gerencial | `AÇÃO GERENCIAL` | 250510 |
| Sprint Growth | `SPRINT GROWTH` | 250506 |
| Weekly Expansão | `WEEKLY EXPANSÃO` | 250507 |
| Alinhamento Comitê | `ALINHAMENTO COMITÊ` | 250508 |
| Quality Control | `QUALITY CONTROL` | 250509 |
| WAR | `WAR` | 250511 |

**Tag de semana** — formato `SEMANA NN` (maiúsculo, **zero-padded a 2 dígitos**: `SEMANA 01` … `SEMANA 52`). A semana é a do **calendário ISO** da demanda. Default = semana ISO de hoje; o usuário pode fixar outra ("essas são da semana 22").

Calcular a semana (Python):
```python
import datetime; datetime.date.today().isocalendar()[1]   # ex: 2026-06-02 → 23
```
Referência de sanidade (Playbook 2026): SEMANA 22 = 25–31 mai · **SEMANA 23 = 01–07 jun** · SEMANA 24 = 08–14 jun. O ISO bate com a tabela do Playbook.

IDs de semana conhecidos (cache; resolver o resto via `list_tags`):

| Tag | ID | | Tag | ID |
|---|---|---|---|---|
| SEMANA 20 | 250535 | | SEMANA 25 | 250540 |
| SEMANA 21 | 250536 | | SEMANA 26 | 250541 |
| SEMANA 22 | 250537 | | SEMANA 27 | 250542 |
| SEMANA 23 | 250538 | | SEMANA 28 | 250543 |
| SEMANA 24 | 250539 | | SEMANA 29 | 250544 |

### Modo TIPO (entregável)

Tags de **tipo de entregável** — independentes da rotina, podem coexistir com as duas tags de rotina/semana. Detectadas pela **sigla no título** (`[NN][SIGLA][IA] Cliente | Demanda`):

| Gatilho | Tag no Ekyte | ID |
|---|---|---|
| sigla `[LP]` | `LANDING PAGE` | 90834 |
| sigla `[CA]` | `Criativo Ads` | 79390 |
| criativo **em vídeo** (só quando você sinalizar) | `criativo em vídeo` | 228775 |

`[CA]` → `Criativo Ads` por padrão. `criativo em vídeo` (228775) é aplicado **só quando você sinalizar** que aquele lote é vídeo — não há tag `CRIAÇÃO DE VIDEO` no Ekyte e o MCP não cria tags, então usamos a existente. Se quiser a nomenclatura exata `CRIAÇÃO DE VIDEO`, crie a tag manual na UI e me avise pra cadastrar o ID.

## Fluxo de execução

Para cada task do lote:

1. **Resolver os IDs das tags-alvo.** Use o cache acima. Para semana fora do cache (ou pra confirmar), `list_tags(type:0, textSearch:"SEMANA NN")` e pegue o match **exato** da série canônica (2505xx) — ignore variantes ("SEMANA 20 " com espaço, "Sprint Growth - Semana 20", "Expansão semana 23 - Nayara"). Se a tag não existir, **PARE e reporte** (não dá pra criar tag via MCP).

2. **Ler tags atuais:** `get_detailed_task(taskId)` → extrair a lista de tags já aplicadas (cada uma tem seu `tagId`/`id`). Esse é o estado que NÃO pode ser perdido.

3. **Merge:** `conjunto_final = tags_atuais ∪ tags_novas` (dedupe por ID). Se todas as novas já estão lá, é **no-op** — reportar "já taguada" e pular.

4. **Preview obrigatório** (ver formato abaixo) — esperar "ok".

5. **Aplicar:** `update_task_tags(taskId, tags)` onde `tags` é a lista **completa** no formato:
   ```json
   [{"ctcTaskId": 9342321, "tagId": 250538}, {"ctcTaskId": 9342321, "tagId": 250506}, ...]
   ```
   Um item por tag do conjunto final, todos com o mesmo `ctcTaskId`. Disparar em paralelo (uma chamada por task).

6. **Relatório** consolidado: ✅ aplicadas / ⏭️ já tinham / ❌ falhas.

## Preview (obrigatório antes de aplicar)

```
🏷️  Tags a aplicar — 3 tasks (modo ROTINA: Weekly Expansão · Semana 23)

• 9342321  [02][CA][IA] Cliente X | Remarketing
     atuais:  Criativo Ads
     +novas:  WEEKLY EXPANSÃO (250507), SEMANA 23 (250538)
     final →  Criativo Ads, WEEKLY EXPANSÃO, SEMANA 23

• 9342322  [01][LP][IA] Cliente X | LP Black Friday
     atuais:  (nenhuma)
     +novas:  WEEKLY EXPANSÃO (250507), SEMANA 23 (250538), LANDING PAGE (90834)
     final →  WEEKLY EXPANSÃO, SEMANA 23, LANDING PAGE

• 9342323  já tem WEEKLY EXPANSÃO + SEMANA 23 → ⏭️ pula (no-op)

Confirma aplicar? (ok / ajusta)
```

Mostrar sempre **atuais → final** pra deixar explícito que nada está sendo apagado.

## Output esperado

```
✅ 2 tasks taguadas · ⏭️ 1 já estava · ❌ 0 falhas

✅ 9342321: + WEEKLY EXPANSÃO, SEMANA 23
✅ 9342322: + WEEKLY EXPANSÃO, SEMANA 23, LANDING PAGE
⏭️ 9342323: já tinha as tags
```

Se falha:
```
⚠️ PARCIAL: 1/2 ok
✅ 9342321: + SEMANA 23, SPRINT GROWTH
❌ 9342322 (erro): get_detailed_task não retornou — task pode ter sido excluída
```

## Guardrails (não-negociáveis)

1. **Nunca aplicar sem merge.** Sempre `get_detailed_task` antes. Mandar `update_task_tags` só com as novas apaga o resto. É o erro que destrói trabalho.
2. **Preview sempre**, mesmo em lote. Mostrar atuais → final por task.
3. **Tag inexistente = parar e reportar.** O MCP não cria tags. Não inventar ID, não usar tag "parecida" (ex: combinar "SPRINT GROWTH - SEMANA 21" no lugar de "SEMANA 23"). Resolver pelo match exato da série canônica.
4. **Modo ROTINA = exatamente 2 tags** (rotina + semana). Não adicionar tag de rotina sem semana nem vice-versa — o filtro com cláusula E do coordenador depende do par.
5. **Idempotência:** rodar 2× não duplica nem apaga — o merge dedupe e no-op em quem já tem.
6. **Companhia:** o token MCP já é da Colli (3597). Não passar `companyId` salvo se mudar de empresa.

## Exemplos de uso

**Ex 1 — Rotina, lote por projeto:**
```
Taguea as tasks do projeto "Cliente X | Q2/2026" criadas hoje como Weekly Expansão.
```
→ resolve `WEEKLY EXPANSÃO` (250507) + `SEMANA 23` (250538, semana atual) → merge → preview → aplica.

**Ex 2 — Rotina, semana fixada + IDs explícitos:**
```
IDs 9342321, 9342322, 9342323 → Sprint Growth, semana 22.
```
→ `SPRINT GROWTH` (250506) + `SEMANA 22` (250537).

**Ex 3 — Tipo por sigla (auto):**
```
Nessas 5 tasks, aplica a tag de tipo pelo título.
```
→ `[LP]`→LANDING PAGE, `[CA]`→Criativo Ads, lendo a sigla de cada título.

**Ex 4 — Rotina + tipo juntos:**
```
Tasks do Sprint Growth dessa semana; as de criativo são vídeo.
```
→ cada task: SPRINT GROWTH + SEMANA 23; as `[CA]` sinalizadas vídeo recebem também `criativo em vídeo` (228775).

## Quando NÃO usar

- Renomear título → `gestao-ekyte-rename-tasks`.
- Criar a task → `ekyte-task` (que já aceita tags na criação; esta skill é pra taguear o que já existe ou corrigir).
- Mudar responsável/fase/prazo → tools `mcp__ekyte-oficial__update_task_responsibles` / `update_task_phase` / `update_task` direto.

## Manutenção do cache de IDs

Tags de rotina são permanentes (set 250506–250511 estável). Tags de semana são criadas no início do ano (`SEMANA 01`–`52`). Se um ID mudar ou faltar, reabrir via `list_tags(type:0, textSearch:"...")` e atualizar a tabela aqui. Tipos de entregável (LANDING PAGE 90834, Criativo Ads 79390, criativo em vídeo 228775) raramente mudam.
