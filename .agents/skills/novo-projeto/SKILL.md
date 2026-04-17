---
name: novo-projeto
description: Cria uma nova pasta de projeto com estrutura padrao em bases/. Use quando o usuario rodar /novo-projeto ou disser que quer adicionar um projeto novo, uma area de trabalho ou qualquer base que nao seja cliente.
---

Voce vai criar a pasta de um novo projeto com a estrutura padrao.

## Processo

### Passo 1 — Nome do projeto

Pergunte:
> "Qual o nome do projeto ou area de trabalho?"

Use o nome para criar a pasta. Converta para lowercase-com-hifens (ex: "Conciliação Bancária" → "conciliacao-bancaria").

### Passo 2 — Criar a estrutura

```bash
cp -r bases/_template "bases/[nome-formatado]"
```

### Passo 3 — Contexto inicial

Pergunte:
> "Me conta em 1-2 frases o que e esse projeto. Pra que ele serve?"

Crie `bases/[nome-formatado]/CLAUDE.md`:
```markdown
# [Nome do Projeto]

## Resumo
[Descricao que o usuario deu]

## Contexto
Rode `/contexto` apos adicionar dados nesta pasta para gerar o contexto completo.
```

### Passo 4 — Confirmar

Mostre a estrutura criada:
```
bases/[nome-formatado]/
├── CLAUDE.md
├── docs/
├── dados/
└── referencias/
```

Diga:
> "Projeto criado. Jogue seus dados nas pastas (docs, dados, referencias) e rode `/contexto` quando tiver pronto."
