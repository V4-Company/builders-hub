# Contribuindo pro Builders Hub

Tem uma skill que funciona bem no seu dia a dia? Compartilha com o time. A ideia do Hub e simples: **o que serve pra um V4er serve pra outro**.

## Como compartilhar (caminho fácil)

No terminal, rode:

```
/compartilhar-skill
```

A skill faz tudo:

1. Te pergunta qual skill quer compartilhar
2. Valida o nome (`{area}-{slug}`) e o frontmatter (`name`, `description`, `area`, `author`, `version`)
3. Remove qualquer info pessoal/credencial do conteudo
4. Cria uma branch, commita a skill em `.claude/skills/` E `.agents/skills/`
5. Faz push e abre um Pull Request automatico com o template preenchido
6. Te da o link do PR pra acompanhar

O curador revisa, aprova, e em poucos dias sua skill entra no hub. Todo mundo que rodar `/sync-hub` vai recebe-la.

## Como compartilhar (caminho tecnico)

Se voce manja de git, tambem pode:

1. Fork do repo
2. Branch nova: `skill/{area}-{nome}`
3. Copie sua skill pra `.claude/skills/{area}-{nome}/SKILL.md` E `.agents/skills/{area}-{nome}/SKILL.md`
4. Commit + push
5. Abra PR preenchendo o template

## Regras de contribuição

### Naming
- **Prefixo obrigatorio** de area: `trafego`, `criativo`, `cs`, `estrategia`, `gestao`, `dados`
- Slug em kebab-case: `trafego-analise-anomalias`
- Nome dentro do frontmatter bate com o nome da pasta

### Frontmatter obrigatorio
```yaml
---
name: trafego-analise-anomalias
description: O que a skill faz em uma frase. Triggera quando [cenarios].
area: trafego
author: seu-github-username
version: 1.0.0
---
```

### Conteudo
- Escrito em portugues brasileiro
- Instrucoes claras, diretas, orientadas a acao
- Sem dados pessoais, credenciais, nomes de clientes especificos
- Exemplos genericos ou anonimizados
- Se a skill depende de ferramenta externa (MCP, API), documentar setup no proprio SKILL.md

### Duplicar em ambos os agentes
Toda skill vive em `.claude/skills/` E `.agents/skills/`. A `/criador-de-skills` faz isso automaticamente, mas se voce editar manualmente, garanta que os dois estao sincronizados.

### Sem quebrar o que ja existe
- Nao renomeia skills ja existentes (ate pode, mas abre issue primeiro)
- Se sua skill e variacao de uma existente, considere melhorar a existente em vez de criar nova

## O que acontece depois do PR

1. **Auto-checks** rodam (frontmatter valido? naming correto? sem credenciais?)
2. **Curador humano** (por enquanto, @guilherme) revisa
3. Se aprovado, merge na `main`
4. GitHub Action regenera `REGISTRY.md` automaticamente
5. Todos que rodarem `/sync-hub` recebem a skill

## Conflitos de merge

A skill `/compartilhar-skill` ja tenta rebasear em `origin/main` antes de abrir o PR. Se der conflito, ela te guia pela resolucao. Arquivos pessoais (`clientes/`, `bases/`) nunca conflitam porque estao no `.gitignore`.

## Duvidas?

Abra uma issue ou fale no canal V4 AI. Bora construir juntos.
