---
name: ekyte-status-cliente
description: Puxa o status operacional de um cliente no Ekyte e devolve o que foi concluido no periodo, o que esta em andamento, o que esta atrasado e onde as horas estouraram o estimado. Use sempre que o usuario perguntar como esta a operacao de um cliente, o que o time entregou, o que esta parado, o que atrasou, quantas horas foram gastas, ou quando estiver preparando pauta de check-in e precisar dos fatos de entrega. Tambem cobre o caminho inverso: transformar combinados de call em tarefas no Ekyte, sempre com confirmacao antes de criar.
area: ekyte
author: luizricardo
version: 1.0.0
---

# /ekyte-status-cliente

Radar de operacao por cliente. Le o Ekyte, separa fato de impressao e entrega o material que alimenta check-in e Mission Control.

## Pre-requisito

O MCP do Ekyte precisa estar configurado (ferramentas `mcp__ekyte__*` disponiveis). Se nao estiverem:

```bash
claude mcp add --transport http ekyte "https://api.ekyte.com/mcp?token=SEU_TOKEN" --scope user
```

Token em: avatar → Perfil de Acesso → Integracoes MCP. Gerar token novo invalida o anterior. Depois de adicionar, reinicie o Claude Code. Nunca cole o token no chat, porque o comando roda no terminal do usuario.

## Passo 1: Identificar o cliente

Descubra o `workspaceId`. Nao chute: cada cliente e um workspace.

```
mcp__ekyte__list_short_workspaces  { "textSearch": "<primeiro nome do cliente>", "active": 1 }
```

O nome do workspace no Ekyte quase nunca bate com o nome da pasta na KB. Busque pelo
primeiro nome do cliente e confirme pelo `id` que a busca devolveu, nunca pelo nome.
Guarde os ids que voce usa com frequencia no `links.md` do cliente.

## Passo 2: Definir a janela

Padrao: ultimos 30 dias. Se o cliente tem `checkins/` na KB, use a data do ultimo check-in como inicio. O recorte util e "o que andou desde a ultima vez que falamos com ele".

Datas em ISO (`2026-07-27`).

## Passo 3: Puxar os quatro recortes

Sempre `list_tasks` com `workspaceId` e `limit: 200`.

| Recorte | Argumentos |
|---|---|
| Concluidas no periodo | `situation: "30"`, `concludedDateStart`, `concludedDateEnd` |
| Em andamento | `situation: "10"` |
| Pausadas | `situation: "20"` |
| Atrasadas | `situation: "10,20"`, `currentDueDateEnd: <ontem>` |
| Canceladas no periodo | `situation: "40"` |

### Armadilhas que ja custaram caro

- **Nao use o filtro `concluded`.** Ele nao significa "nao concluida". Em teste real, `concluded: false` devolveu 19 tarefas das quais 15 estavam concluidas e 3 canceladas. Use `situation`, que e explicito.
- **`situation` e string, nunca array.** `"10,20"` funciona; `[10,20]` da erro.
- **Codigos:** Ativa=10, Pausada=20, Concluida=30, Cancelada=40.
- **Teto de 200 tarefas por consulta.** Se vier exatamente 200, avise que a lista pode estar truncada e estreite a janela.
- Prioridade: 10=Nao priorizado, 100=Baixa, 200=Media, 300=Alta, 400=Urgente.

## Passo 4: Ler os numeros antes de escrever

Cada tarefa traz `estimatedTime` e `actualTime` (minutos), `phase.name`, `executor.userName`, `responsibles[]`, `ctcTaskType.name`, `currentDueDate` e `tags`.

Calcule:

- **Atraso em dias** por tarefa: hoje menos `currentDueDate`.
- **Estouro de horas**: `actualTime` contra `estimatedTime`, por tarefa e somado no periodo. Tarefa com estimado 60 e real 180 e um fato de conversa, nao um detalhe.
- **Onde a fila trava**: agrupe as em andamento e as atrasadas por `phase.name`. Se todas param na mesma fase, o gargalo tem dono.
- **Distribuicao por executor**, quando fizer sentido para carga de time.

Para horas apontadas de verdade, `mcp__ekyte__list_time_trackings` aceita `workspaceId`, `startDate`, `endDate` e `executorId`, e devolve ate 400 registros.

## Passo 5: Entregar

Pergunte como o usuario quer consumir, ou infira pelo contexto:

- **Resumo no chat** (padrao): entregues no periodo, em andamento com prazo, atrasadas com dias de atraso, gargalo por fase, estouro de horas.
- **Pauta de check-in**: o bloco de entregas vira o "o que fizemos" do ROPRE. Combine com `/account-checkin-roleplay`.
- **Atualizar Mission Control**: escreva os fatos em `mission-control/` do cliente. Nao invente status de combinado que o Ekyte nao comprova.

Regras de leitura, herdadas do hub:

- Diferencie **fato do Ekyte** de inferencia. "13 tarefas concluidas" e fato; "o time está performando bem" e opiniao.
- Tarefa concluida nao prova resultado de negocio. Nao apresente volume de entrega como resultado para o cliente.
- Se o dado nao existe no Ekyte, diga que nao existe.

## Passo 6: Combinados viram tarefas (escrita, opcional)

So quando o usuario pedir. **Confirmacao obrigatoria**: monte a lista completa (titulo, tipo, executor, prazo, estimativa) e mostre para aprovacao antes de criar qualquer coisa. Toda escrita fica registrada no usuario dono do token.

`create_task` exige: `title`, `description`, `phaseDueDate`, `currentDueDate`, `estimatedTime`, `workspaceId`, `executorId`, `phaseId`, `ctcTaskTypeId`, `situation`, `flow`.

Para montar sem chutar:

1. `list_task_types` ou `list_task_types_create_task` → pega `ctcTaskTypeId`.
2. `get_task_type_flow` ou `list_task_flow_phases` → pega a primeira fase (`phaseId`) e o `flow`.
3. `list_admin_editors_users` → pega o `executorId`.
4. `situation: 10` (Ativa) e `phaseDueDate` calculado a partir de `currentDueDate`.

Depois de criar, confirme devolvendo os IDs criados. Se algo falhar no meio, diga o que foi criado e o que nao foi. Nunca deixe o usuario achando que criou tudo.

Para mover fase use `update_task_phase`; consulte o estado atual antes, porque o fluxo tem regras de progressao.

## Fora de escopo

- Dados de midia (Meta, Google, GA4): use os prefixos `meta-*`, `google-*`, `ga4-*`.
- CRM e vendas: `hubspot-*`, `kommo-*`.
- Ekyte nao tem receita nem CAC. Nao tente derivar resultado comercial daqui.
