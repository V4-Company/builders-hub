# Contribuindo pro Builders Hub

Tem uma skill que funciona bem no seu dia a dia? Compartilha com o time. A ideia do Hub e simples: **o que serve pra um V4er serve pra outro**.

## Como compartilhar (caminho fácil)

No terminal, rode:

```
/compartilhar-skill
```

A skill faz tudo:

1. Te pergunta qual skill quer compartilhar
2. Valida o nome (`{papel}-{slug}` ou `{fonte}-{slug}`) e o frontmatter (`name`, `description`, `area`, `author`, `version`)
3. Remove qualquer info pessoal/credencial do conteudo
4. Cria uma branch, commita a skill em `.claude/skills/` E `.agents/skills/`
5. Faz push e abre um Pull Request automatico com o template preenchido
6. Te da o link do PR pra acompanhar

O curador revisa, aprova, e em poucos dias sua skill entra no hub. Todo mundo que rodar `/sync-hub` vai recebe-la.

## Como compartilhar (caminho tecnico)

Se voce manja de git, tambem pode:

1. Fork do repo
2. Branch nova: `skill/{papel}-{nome}` (ou `skill/{fonte}-{nome}`)
3. Copie sua skill pra `.claude/skills/{prefixo}-{nome}/SKILL.md` E `.agents/skills/{prefixo}-{nome}/SKILL.md`
4. Commit + push
5. Rode as validações abaixo
6. Abra PR preenchendo o template

```bash
python3 scripts/build-registry.py
python3 scripts/validate-repo.py
python3 scripts/build-registry.py --check
python3 scripts/run-tests.py
```

## Regras de contribuição

### Naming
- **Prefixo obrigatorio** no nome — pode ser:
  - **Papel** (skills agrupadas por quem usa): `geral`, `gt`, `designer`, `copy`, `account`, `coord`
  - **Fonte** (puxador de dados, reutilizavel): `v4mos`, `google`, `ga4`, `meta`, `hubspot`, `kommo`, `shopify`, `tray`
- Slug em kebab-case: `gt-analise-anomalias`, `v4mos-dados-meta-ads`
- Nome dentro do frontmatter bate com o nome da pasta
- Pra `/gt`, `/designer` etc. filtrarem so as skills do papel no autocomplete do Claude Code, o prefixo precisa estar no nome (nao basta no frontmatter)

### Frontmatter obrigatorio
```yaml
---
name: gt-analise-anomalias
description: O que a skill faz em uma frase. Triggera quando [cenarios].
area: gt            # papel OU fonte (bate com o prefixo do nome). Campo se chama `area:` por compat historica.
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

A skill `/compartilhar-skill` ja tenta rebasear em `origin/main` antes de abrir o PR. Se der conflito, ela te guia pela resolucao. Arquivos pessoais (`squads/` e KBs em `bases/`) nunca conflitam porque estao no `.gitignore`.

## Duvidas?

Abra uma issue ou fale no canal V4 AI. Bora construir juntos.
