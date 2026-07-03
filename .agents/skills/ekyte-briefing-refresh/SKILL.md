---
name: ekyte-briefing-refresh
description: Atualiza os arquivos de cache da `/ekyte-briefing` — `clientes/_skill-ekyte/drives.md` (links de Drive por cliente) e `clientes/_skill-ekyte/backups-crm.md` (planilhas de backup CRM por cliente). Use quando o Fabio entrar com cliente novo, trocar link de Drive de algum cliente, criar planilha de backup CRM nova, ou quando rodar `/ekyte-briefing-refresh`. Não toca em templates da skill (esses são gerenciados pela `/ekyte-templates-refresh`).
area: ekyte
author: fabio
version: 1.0.0
user-invocable: true
---

# /ekyte-briefing-refresh — Atualizar drives e backups CRM

Mantém os dois arquivos de lookup que a `/ekyte-briefing` usa: `drives.md` (sempre presente) e `backups-crm.md` (preenchido sob demanda).

## Quando usar

- `/ekyte-briefing-refresh` (invocação direta)
- "atualiza o Drive do cliente X"
- "entrou cliente novo, atualiza"
- "criei a planilha de backup do CRM, salva aqui"
- "Cliente H agora tem Drive: <link>"

## Pré-requisitos

- `clientes/_skill-ekyte/drives.md` existente (criado pela `/ekyte-briefing` na primeira instalação).
- `clientes/_skill-ekyte/backups-crm.md` existente.

## Fluxo

### 1) Perguntar o que atualizar

```
O que você quer atualizar?

1) Drive de cliente — adicionar/trocar link de Drive
2) Planilha de Backup CRM — adicionar/trocar planilha de backup
3) Ambos
```

### 2) Modo "Drive de cliente"

```
Qual cliente?
1) Cliente E                  → atual: <link>
2) Cliente F  → atual: <link>
3) Cliente A           → atual: <link>
4) Cliente B                   → atual: <link>
5) Cliente C                → atual: <link>
6) Cliente D                  → atual: <link>
7) Cliente G        → atual: <link>
8) Cliente H         → atual: _sem Drive ainda_
9) Cliente novo (não está nos 8 acima)
```

- Opções 1-8: pedir novo link, validar formato (URL Google Drive), atualizar `drives.md`.
- Opção 9: pedir nome do cliente + alias + link. **Avisar**: cliente novo também precisa estar no `cache.md` (workspaces) — sugerir rodar `/ekyte-refresh` na sequência se ainda não rodou.

Mostrar diff antes de salvar:
```
Drive de Cliente G:
  ANTES: https://drive.google.com/drive/folders/1R1TGag8...
  DEPOIS: https://drive.google.com/drive/folders/NOVO_ID...

Confirma? (sim/não)
```

### 3) Modo "Planilha de Backup CRM"

```
Qual cliente vai ter planilha de backup atualizada?
[lista os 8 com status atual: vazio / link]
```

Pedir link da planilha. Salvar em `backups-crm.md`. Mesmo padrão de diff antes de confirmar.

### 4) Modo "Ambos"

Roda 2) e depois 3) em sequência.

### 5) Salvar e reportar

Após cada update:
- Atualizar tabela do arquivo correspondente.
- Atualizar campo "Última atualização" no topo do arquivo.
- Reportar resumo:

```
✅ Atualizações salvas:
  • Drive de Cliente G atualizado
  • Backup CRM de Cliente C adicionado

Arquivos modificados:
  - clientes/_skill-ekyte/drives.md
  - clientes/_skill-ekyte/backups-crm.md
```

## Guardrails

1. **Diff obrigatório.** Sempre mostrar antes/depois antes de salvar. Erros de digitação em link de Drive quebram o briefing inteiro depois — vale pedir confirmação.

2. **Validação mínima de URL.** Drive precisa ser `drive.google.com`. Backup pode ser sheets.google.com OU outro formato. Se URL não bate o domínio esperado, perguntar se está certo antes de salvar.

3. **Cliente fora dos 8 fixos** → exigir confirmação extra ("Esse cliente não está nos 8 do `cache.md`. Tem certeza? Vai precisar adicionar no cache.md depois também."). Não bloquear, mas avisar.

4. **Não mexer em templates.** Esta skill toca **só** em `drives.md` e `backups-crm.md`. Templates são responsabilidade de `/ekyte-templates-refresh`.

## Como invocar

- `/ekyte-briefing-refresh` (direto).
- "atualiza Drive do Y" / "salva planilha de backup do X".

## O que NÃO fazer

- Não escrever em `briefing-templates/` (use `/ekyte-templates-refresh`).
- Não mexer em `cache.md` (use `/ekyte-refresh`).
- Não criar cliente novo silenciosamente — sempre avisar que `cache.md` também precisa ser atualizado.
