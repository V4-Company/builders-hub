---
name: ekyte-apontamento-horas
description: Aponta horas/timesheet em tarefas do Ekyte via API interna, com validacao de task, periodo, duplicidade e verificacao pos-criacao. Use sempre que o Fabio pedir "aponte horas", "aponta 1h", "apontamento", "timesheet", "das 13 as 14", "registra tempo" ou citar um ID de tarefa Ekyte junto com intervalo/duracao.
area: ekyte
author: fabio
version: 1.0.0
---

# Ekyte - Apontamento de Horas

Use esta skill para registrar horas em uma task do Ekyte sem abrir a UI.

## Quando usar

Use quando o usuario pedir algo como:
- "aponte 1h nessa tarefa, das 13 as 14, 9509098"
- "aponta 30min hoje na task 123456"
- "registra timesheet de ontem das 16:30 as 17:15 na tarefa X"
- "faz apontamento no Ekyte"

Se faltar o ID da task ou faltar o intervalo/duracao, pergunte so o dado que falta.

## Principio critico

Nunca invente confirmacao. So diga que apontou depois de receber HTTP 200 da API e verificar o apontamento criado.

Nunca exponha token do Ekyte em mensagens, logs ou arquivos. Diga apenas "token presente", "token ausente" ou "token expirado".

## Dependencias

O script usa o token REST do app Ekyte em:

```text
CLIENTES V4/_skill-ekyte/.env
```

Chaves esperadas:

```text
EKYTE_TOKEN=<jwt do app, sem Bearer>
EKYTE_COMPANY_ID=3597
```

Tambem aceita variaveis de ambiente `EKYTE_TOKEN`, `EKYTE_COMPANY_ID` e `EKYTE_ENV_PATH`.

## Fluxo obrigatorio

1. Parseie o pedido:
   - `task_id`: numero da tarefa Ekyte.
   - `date`: se o usuario disser "hoje", use a data atual do ambiente em America/Sao_Paulo. Se disser "ontem", subtraia um dia. Se nao disser data, assuma hoje e mencione a data absoluta no resultado.
   - `start`: hora inicial, formato HH:MM.
   - `end`: hora final, formato HH:MM.
   - `duration`: se o usuario der duracao mas nao der fim, calcule `end = start + duration`.
   - `comment`: opcional.

2. Valide que o intervalo tem duracao positiva. Nao aceite intervalo cruzando meia-noite sem confirmar explicitamente.

3. Rode o script em `--dry-run` se for a primeira vez daquele padrao de payload ou se algo parecer ambiguo:

```powershell
python ".codex/skills/ekyte-apontamento-horas/scripts/apontar_horas_ekyte.py" --task-id 9509098 --date 2026-06-04 --start 13:00 --end 14:00 --dry-run
```

4. Para criar de fato:

```powershell
python ".codex/skills/ekyte-apontamento-horas/scripts/apontar_horas_ekyte.py" --task-id 9509098 --date 2026-06-04 --start 13:00 --end 14:00
```

5. Leia o JSON retornado. So finalize como sucesso se `created_id` vier preenchido e `verified` for `true`.

## API usada

O endpoint correto de escrita nao e o `/api/v2`. O apontamento manual usa a API interna do app:

```text
POST https://api.ekyte.com/api/companies/{company_id}/workspaces/{workspace_id}/time-trackings
```

Antes de postar, o script busca a task em:

```text
GET https://api.ekyte.com/api/companies/{company_id}/ctc-tasks/{task_id}
```

Use sempre o `workspaceId`, `ctcTaskTypeId` e `phaseId` retornados pela propria task. Nao reutilize `workspaceId` de requests da Network de outra task.

Payload base:

```json
{
  "typeTimeTracking": 2,
  "startDate": "2026-06-04T13:00:00",
  "startDateTime": "13:00",
  "endDate": "2026-06-04T14:00:00",
  "endDateTime": "14:00",
  "effort": 60,
  "comment": "",
  "workspaceId": 10313,
  "type": 1,
  "ctcTaskId": 9509098,
  "ctcTaskTypeId": 34483,
  "phaseId": 1,
  "ticketId": null,
  "ticketPhaseId": null,
  "planningId": null,
  "planId": null,
  "modeOverlap": true
}
```

`effort` e sempre em minutos.

## Duplicidade

Por padrao o script bloqueia criacao se ja existir apontamento ativo da mesma task no mesmo dia com o mesmo `startDate` e `endDate`.

Use `--force` apenas se o usuario pedir explicitamente para duplicar ou corrigir um caso incomum.

## Resposta ao usuario

Responda curto:

```text
Feito. Apontei 1h na task 9509098, em 04/06/2026, das 13:00 as 14:00.

ID do apontamento: 11535154.
Task: [titulo da task].
```

Se falhar, diga o erro acionavel:

```text
Nao consegui apontar: token Ekyte expirado (HTTP 401). Preciso que voce atualize o EKYTE_TOKEN em CLIENTES V4/_skill-ekyte/.env.
```

## Setup do token

Se o token estiver ausente ou expirado:

1. Abra `https://app.ekyte.com` e faca login.
2. Abra DevTools > Network.
3. Filtre por `api.ekyte`.
4. Faca qualquer acao autenticada simples no app.
5. Copie o header `Authorization: Bearer ...`.
6. Salve apenas o JWT em:

```text
CLIENTES V4/_skill-ekyte/.env
EKYTE_TOKEN=<jwt sem Bearer>
```

Nao cole o token no chat.

