---
name: contexto
description: Le todos os arquivos em uma base de conhecimento (cliente ou projeto) e gera um CLAUDE.md com o contexto completo. Use quando o usuario rodar /contexto ou quiser que a IA "conheca" um cliente ou projeto.
---

Voce vai analisar toda a Knowledge Base de um cliente ou projeto e gerar um arquivo CLAUDE.md que resume tudo que a IA precisa saber.

## Objetivo

Ler todos os arquivos na pasta e gerar um CLAUDE.md que funcione como "memoria" para qualquer trabalho futuro.

## Processo

### Passo 1 — Identificar a base

Verifique se existem pastas em `clientes/` ou `bases/` (ignorando `_template`).

- Se existirem pastas em `clientes/`, liste e pergunte qual cliente
- Se existirem pastas em `bases/`, liste e pergunte qual projeto
- Se existirem nos dois, liste tudo e pergunte

### Passo 2 — Detectar o tipo

Olhe a estrutura de subpastas para entender o tipo:

**Operacao (cliente):** tem `calls/`, `docs/`, `campanhas/`
**Generico (projeto/area):** tem `docs/`, `dados/`, `referencias/`

Adapte a analise conforme o tipo detectado.

### Passo 3 — Ler tudo

Leia TODOS os arquivos na pasta. Leia cada arquivo por completo. Nao pule nada.

### Passo 4 — Analisar e extrair

**Se for CLIENTE (operacao):**

Extraia:
- Nome da empresa, segmento, produto/servico, publico-alvo, diferenciais
- Canais de marketing, investimento, metricas (CPC, CPL, ROAS)
- Contatos/stakeholders, combinados, pendencias
- Objetivos, teses em andamento, historico, proximos passos

Gere o CLAUDE.md com:
```markdown
# [Nome da Empresa]

## Resumo
[2-3 frases: quem e, o que faz, momento atual]

## Negocio
- **Segmento:** [X]
- **Produto/Servico:** [X]
- **Publico-alvo:** [X]
- **Diferenciais:** [X]

## Operacao
- **Canais ativos:** [X]
- **Investimento:** [X/mes]
- **Metricas atuais:** [CPC, CPL, ROAS, etc]
- **Problemas:** [X]
- **Oportunidades:** [X]

## Relacionamento
- **Contatos:** [nomes e funcoes]
- **Combinados:** [o que foi prometido/acordado]
- **Pendencias:** [entregas pendentes]

## Estrategia
- **Objetivos:** [X]
- **Teses atuais:** [X]
- **Historico:** [o que ja testaram]
- **Proximos passos:** [X]

## Notas Importantes
[Qualquer informacao critica que nao se encaixou acima]
```

**Se for PROJETO/AREA (generico):**

Extraia:
- Nome do projeto/area, objetivo principal
- Pessoas envolvidas, responsabilidades
- Dados e metricas relevantes encontrados
- Processos e workflows identificados
- Problemas e oportunidades
- Decisoes ja tomadas, pendencias

Gere o CLAUDE.md com:
```markdown
# [Nome do Projeto/Area]

## Resumo
[2-3 frases: o que e, qual o objetivo, momento atual]

## Contexto
- **Objetivo:** [X]
- **Pessoas envolvidas:** [nomes e papeis]
- **Status atual:** [X]

## Dados
- **Metricas principais:** [o que foi encontrado nos dados]
- **Fontes:** [de onde vem os dados]

## Processos
- **Workflows identificados:** [o que a area faz]
- **Ferramentas usadas:** [se mencionado]

## Situacao Atual
- **Problemas:** [X]
- **Oportunidades:** [X]
- **Decisoes tomadas:** [X]
- **Pendencias:** [X]

## Notas Importantes
[Qualquer informacao critica que nao se encaixou acima]
```

### Passo 5 — Apresentar ao usuario

Mostre um resumo do que encontrou e o CLAUDE.md gerado. Pergunte:
- "Tem algo que eu errei ou que falta?"
- "Quer adicionar alguma informacao que nao estava nos arquivos?"

Ajuste conforme o feedback.

### Passo 6 — Confirmar

Salve o arquivo e diga:
> "Pronto. Agora toda vez que voce trabalhar nessa pasta, a IA vai ler esse CLAUDE.md automaticamente e ja vai saber tudo. Se os dados mudarem, rode /contexto de novo pra atualizar."

## Regras

- NAO invente informacoes. Se nao encontrou algo nos arquivos, deixe como "[nao disponivel]"
- Se a KB estiver vazia ou quase vazia, avise o usuario e sugira quais dados adicionar
- Priorize fatos sobre interpretacoes. O CLAUDE.md deve ser factual
- Mantenha o CLAUDE.md conciso — maximo 150 linhas
