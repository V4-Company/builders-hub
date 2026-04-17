---
name: compartilhar-skill
description: Empacota uma skill local e abre Pull Request no Builders Hub publico automaticamente. Use quando o usuario rodar /compartilhar-skill, disser que quer "compartilhar essa skill com o time", "publicar no hub", "enviar pro repo" ou similar. Valida nome/frontmatter/duplo-write, resolve conflitos com origin/main via rebase, cria branch, commita, faz push e abre PR via gh CLI — o usuario so precisa aprovar depois. Nunca commita arquivos pessoais de clientes/ ou bases/.
---

# /compartilhar-skill — Envia skill pro Builders Hub

Pega uma skill que ja funciona no ambiente local do usuario, valida tudo, e abre um Pull Request no repo publico pro curador revisar. O usuario termina com um link do PR e a ideia de que o time inteiro vai poder usar a skill em poucos dias.

## Pre-requisitos

Antes de comecar, confirme que o ambiente esta OK. Se tiver duvida, rode `/onboarding` primeiro. Os bloqueadores fatais sao:

- Sem git identity → commit fica anonimo
- Sem `gh` autenticado → impossivel abrir PR automatico
- Sem remote configurado pra `builders-hub` → nao tem pra onde pushar
- Usuario fora do repo `builders-hub` (rodando em outra pasta)

Se qualquer um falhar, chame `/onboarding` (os checks de setup sao a primeira coisa que ele faz) e pare aqui.

## Fluxo

### Passo 1 — Descobrir qual skill compartilhar

Pergunte ao usuario: **"Qual skill voce quer compartilhar com o time?"**

Se ele nao souber o nome exato, liste as skills locais que NAO sao skills de base:

```bash
ls .claude/skills/
```

Filtre as skills de base (onboarding, contexto, criador-de-skills, novo-cliente, novo-projeto, brainstormar-sobre-minha-funcao, sabatina, compartilhar-skill, sync-hub, frontend-design). Apresente so as que tem prefixo de area (`trafego-*`, `criativo-*`, etc.) ou que parecem ser de contribuicao.

### Passo 2 — Validar naming

A skill DEVE seguir o padrao `{area}-{slug}`:

```
^(trafego|criativo|cs|estrategia|gestao|dados|outra|v4mos|google|ga4|meta|hubspot|kommo|shopify|tray)-[a-z0-9-]+$
```

Se o nome nao bater, pare e oriente o usuario:
1. Opcao (a): renomear a skill (rode `/criador-de-skills` com a skill existente pra renomear corretamente)
2. Opcao (b): escolher outro nome aqui mesmo (mas precisa mover pasta)

**Nao prossiga** com nome fora do padrao — o curador vai rejeitar.

### Passo 3 — Validar frontmatter

Leia `.claude/skills/{nome}/SKILL.md` e extraia o frontmatter. Deve ter os 5 campos:

```yaml
name: {nome}            # bate com a pasta
description: ...        # nao vazio, explica quando triggera
area: {area}            # bate com prefixo do nome
author: {github-user}   # se vazio, pegar do git: git config user.name
version: ...            # padrao 1.0.0 se vazio
```

Se algum campo estiver faltando, **pergunte ao usuario e preencha antes de commitar**. Nao invente valores — confirme com ele, especialmente `author` (pode nao ser o mesmo nome do git).

Se `author` nao estiver preenchido, sugira rodar `gh api user --jq .login` pra pegar o github-handle exato.

### Passo 4 — Validar duplo-write

Confira que existe `.claude/skills/{nome}/SKILL.md` E `.agents/skills/{nome}/SKILL.md` com **conteudo identico**:

```bash
diff ".claude/skills/{nome}/SKILL.md" ".agents/skills/{nome}/SKILL.md"
```

Se forem diferentes: mostre o diff, pergunte qual e a versao correta, e sincronize copiando pro outro lado. A skill deve ir identica pros dois paths no commit.

Se um dos dois nao existir: crie copiando do que existe.

### Passo 5 — Checagem de seguranca (dados pessoais / credenciais)

Escaneie o conteudo do SKILL.md procurando padroes que NAO podem ser compartilhados:

**Padroes criticos (bloqueiam o compartilhamento):**
- Tokens/keys aparentes: `sk-`, `ghp_`, `AKIA`, `AIza`, chaves longas base64-looking
- Emails privados de pessoas especificas (que nao sejam o author)
- URLs internas da V4 ou de clientes (ex: `painel.cliente-x.com`)
- Nomes de clientes reais (pesquise strings tipo "Cliente X", "Ltda", "LTDA", "SA ")
- Dados de campanha reais (IDs de conta Google/Meta, valores em R$ com precisao)
- Credenciais DB: strings tipo `postgres://user:pass@host`

**Padroes de alerta (mostre pro usuario e deixe ele decidir):**
- Numeros que parecem CNPJ/CPF
- Caminhos absolutos com nomes de pessoas (`/Users/fulano/...`)
- URLs de Google Docs/Drive compartilhados
- Screenshots embarcados em base64

Se encontrar padrao critico: **pare e peca pra ele corrigir antes**. Se padroes de alerta, pergunte: "Encontrei X. Isso pode ir publico?"

### Passo 6 — Decidir: skill nova vs update

Verifique se a skill ja existe no `origin/main`:

```bash
git fetch origin main --quiet
git cat-file -e "origin/main:.claude/skills/{nome}/SKILL.md" 2>/dev/null && echo "EXISTE" || echo "NOVA"
```

- **NOVA:** commit message `feat(skills): add {nome}`, branch `skill/{nome}`
- **EXISTE (update):** incremente a versao no frontmatter automaticamente (ex: `1.0.0` → `1.0.1` pra patches, `1.1.0` pra melhorias, `2.0.0` pra mudanca grande) e pergunte ao usuario qual bump fazer. Commit: `feat(skills): update {nome} to v{x.y.z}`, branch `skill/{nome}-v{x.y.z}`.

### Passo 7 — Garantir main atualizada e fazer o commit

```bash
# Guarda mudancas nao commitadas em outras pastas (ex: clientes/ ja esta gitignored, mas garante)
git stash --include-untracked --quiet 2>/dev/null || true

# Atualiza main
git checkout main
git pull --rebase origin main

# Cria branch nova
git checkout -b "skill/{nome}"

# Stage SO os arquivos da skill (nunca clientes/, bases/, arquivos pessoais)
git add ".claude/skills/{nome}" ".agents/skills/{nome}"

# Confirme que so esses arquivos estao staged
git diff --cached --name-only
```

Mostre ao usuario **exatamente** quais arquivos vao no commit. Ele deve ver:
- `.claude/skills/{nome}/SKILL.md`
- `.agents/skills/{nome}/SKILL.md`
- (opcionalmente) arquivos em `references/`, `scripts/`, `assets/` dentro da skill

Se aparecer QUALQUER coisa fora `.claude/skills/{nome}/` ou `.agents/skills/{nome}/`, pare e investigue. Provavelmente .gitignore esta quebrado.

Commit:

```bash
git commit -m "feat(skills): add {nome}

Autor: @{author}
Area: {area}
Versao: {version}

{description do frontmatter, 1-2 linhas}
"
```

### Passo 8 — Push e abrir PR

```bash
git push -u origin "skill/{nome}"
```

Se o push falhar com `rejected — non-fast-forward` ou conflito:
1. Roda `git pull --rebase origin main` de novo
2. Se tiver conflito: pare e peca pro usuario resolver manualmente (ou chame `/sync-hub` pra guiar resolucao)
3. Tenta o push de novo

Apos push bem-sucedido:

```bash
gh pr create \
  --base main \
  --head "skill/{nome}" \
  --title "feat(skills): add {nome}" \
  --body "$(cat <<'EOF'
## Skill sendo compartilhada

**Nome:** `{nome}`
**Area:** {area}
**Autor:** @{author}
**Versao:** {version}

## O que ela faz

{description completa do frontmatter}

## Como testar

1. Rode `/sync-hub` pra puxar a branch localmente
2. Rode `/{nome}` (ou descreva o cenario de trigger)
3. Valide que {resultado esperado}

## Checklist do contribuidor

- [x] Nome segue `{area}-{slug}` em kebab-case
- [x] Frontmatter completo (name, description, area, author, version)
- [x] Duplo-write em .claude/ e .agents/ (conteudo identico)
- [x] Testada pelo menos uma vez com sucesso
- [x] Sem credenciais, tokens, clientes reais, dados pessoais
- [x] Portugues brasileiro

---

_Gerado via \`/compartilhar-skill\`._
EOF
)"
```

Capture a URL do PR do output do `gh pr create`.

### Passo 9 — Relatar ao usuario

Mostre:

```
✅ Skill {nome} enviada pro hub!

Branch: skill/{nome}
PR: {URL}

Proximos passos:
1. O curador (@guilherme) vai revisar em breve
2. Quando aprovado, a skill vai pra main e o REGISTRY.md regenera
3. Quem rodar /sync-hub vai receber sua skill automaticamente
4. Voce vai ser citado como author no REGISTRY

Obrigado por construir com o time!
```

Depois volte pra main local pra nao deixar o usuario em branch solta:

```bash
git checkout main
```

## Tratamento de erros comuns

### `gh: not authenticated`
Pare e chame `/onboarding` (os checks de setup sao a primeira coisa que ele faz).

### `fatal: not a git repository`
Usuario nao esta em `builders-hub`. Peca pra ele navegar pra la: `cd /caminho/builders-hub`.

### Conflito no rebase
Mostre os arquivos em conflito. Se forem skills de outras pessoas em `.claude/skills/` que nao tem nada a ver com a skill sendo compartilhada, use `git checkout --theirs` pra aceitar a versao de origin/main. Se for conflito dentro da propria skill (raro), pare e peca resolucao manual.

### PR ja existe pra mesma branch
Se `gh pr create` der erro dizendo que ja existe PR: mostre a URL do PR existente e ofereca fazer mais um commit na mesma branch (update do PR). Nunca force push main.

### Usuario esta em branch que nao e main
Se `git branch --show-current` nao for `main`, pergunte se as mudancas atuais sao parte da skill sendo compartilhada. Se nao forem, oriente a commitar primeiro essas outras mudancas (ou fazer stash).

## O que NUNCA fazer

- Commitar conteudo de `clientes/` ou `bases/` (devem estar no .gitignore, mas verifique)
- Editar arquivos em `.claude/skills/` de **outras** skills que nao a sendo compartilhada
- Fazer push direto em `main` (sempre via branch + PR)
- Forcar push (`--force`, `--force-with-lease`) sem instrucao explicita do usuario
- Modificar `REGISTRY.md` manualmente (e auto-gerado pela GitHub Action)
- Mergear o proprio PR (so o curador aprova)

## Depois do PR aprovado

Voce nao precisa fazer nada. A GitHub Action vai:
1. Regenerar REGISTRY.md automaticamente
2. Commitar na main
3. A skill fica disponivel pra todos

Quando o usuario rodar `/sync-hub` da proxima vez, a skill vai aparecer como "nova disponivel" pra ele tambem (se nao tiver sido dele a contribuicao).
