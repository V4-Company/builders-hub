---
name: novo-cliente
description: Cria uma nova pasta de cliente com estrutura padrao e CLAUDE.md inicial. Pergunta nome e NotebookLM. Use quando o usuario rodar /novo-cliente ou disser que quer adicionar um cliente novo.
---

Voce vai criar a pasta de um novo cliente com a estrutura padrao e um CLAUDE.md inicial.

## Processo

### Passo 1 — Nome do cliente

Pergunte:
> "Qual o nome do cliente?"

Use o nome para criar a pasta. Converta para lowercase-com-hifens para o nome da pasta (ex: "Academia Estação Saúde" → "academia-estacao-saude").

### Passo 2 — Criar a estrutura

```bash
cp -r clientes/_template "clientes/[nome-formatado]"
```

### Passo 3 — NotebookLM

Pergunte:
> "Esse cliente tem um NotebookLM? Se sim, cola o link aqui. Se nao, so aperta Enter."

**Se tiver link** (formato `https://notebooklm.google.com/notebook/XXXXX`):
- Extraia o notebook ID da URL

Crie `clientes/[nome-formatado]/CLAUDE.md`:
```markdown
# [Nome do Cliente]

## NotebookLM
- **Link:** [URL]
- **Notebook ID:** [ID]

Use `notebooklm` CLI com o notebook ID acima para consultar a base de conhecimento desse cliente, gerar podcasts ou resumos.

## Contexto
Rode `/contexto` apos adicionar dados nesta pasta para gerar o contexto completo.
```

**Se NAO tiver link:**

Crie `clientes/[nome-formatado]/CLAUDE.md`:
```markdown
# [Nome do Cliente]

## Contexto
Rode `/contexto` apos adicionar dados nesta pasta para gerar o contexto completo.
```

### Passo 4 — Confirmar

Mostre a estrutura criada:
```
clientes/[nome-formatado]/
├── CLAUDE.md
├── calls/
├── docs/
└── campanhas/
```

Diga:
> "Cliente criado. Jogue os dados dele nas pastas (calls, docs, campanhas) e rode `/contexto` quando tiver pronto."
