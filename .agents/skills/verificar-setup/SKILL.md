---
name: verificar-setup
description: Valida e configura tudo que o Builders Hub precisa pra funcionar — git, GitHub CLI (gh), identidade git, remote, Python 3. Use quando o usuario rodar /verificar-setup, quando for a primeira vez usando o repo, antes de /compartilhar-skill, ou quando algo do fluxo git/sync quebrar. Roda uma bateria de checks e CORRIGE o que estiver faltando guiando o usuario passo a passo — nunca assume que "provavelmente ta ok". Git precisa estar 100% antes de liberar qualquer outra coisa.
---

# /verificar-setup — Valida ambiente Builders Hub

Essa skill e o primeiro passo de qualquer fluxo no Builders Hub. Ela garante que o ambiente do usuario tem tudo pra:

1. Trabalhar localmente com skills (git, Python 3, repo clonado)
2. Puxar atualizacoes do hub (`/sync-hub`)
3. Compartilhar skills com o time (`/compartilhar-skill` → push + PR via `gh`)

## Contexto importante

Muitos V4ers **nao sao tecnicos**. Eles podem nunca ter rodado `git config` na vida. Sua postura aqui e de **mentor paciente**: explica por que cada coisa importa, mostra o comando, confirma que funcionou, e SO avanca pro proximo check quando o atual esta passando.

**Nunca** pule um check assumindo "provavelmente ta ok". Git quebrado gera commits com identidade errada, pushes rejeitados, conflitos mal resolvidos. A gente previne tudo isso rodando a bateria completa toda vez.

## Fluxo

Execute os checks na ordem. Pra cada um: rode o comando de verificacao, mostre o resultado ao usuario, e SE estiver quebrado, guie pela correcao antes de seguir.

### Check 1 — Git instalado

```bash
git --version
```

- **Ok:** output tipo `git version 2.x.y`
- **Quebrado:** "command not found" ou versao < 2.25

**Correcao:**
- **Mac:** `xcode-select --install` ou `brew install git`
- **Windows:** baixar em https://git-scm.com/download/win
- **Linux:** `sudo apt install git` ou equivalente

Apos instalar, peca pro usuario reabrir o terminal e rode `git --version` de novo.

### Check 2 — Identidade git configurada (CRITICO)

```bash
git config --global user.name
git config --global user.email
```

- **Ok:** ambos retornam valores nao-vazios
- **Quebrado:** um dos dois vazio

**Por que importa:** Todo commit carrega nome + email. Sem isso, commits viram "unknown <unknown>" e PRs podem ser rejeitados. Se o email nao bate com a conta GitHub, os commits aparecem como "unverified".

**Correcao:**

1. Pergunte ao usuario o nome completo dele (tipo "Guilherme Lippert")
2. Pergunte o email da conta GitHub dele (**precisa ser exatamente o mesmo do GitHub**, se nao, os commits nao linkam ao perfil)
3. Rode:
   ```bash
   git config --global user.name "Nome Completo"
   git config --global user.email "email@dominio.com"
   ```
4. Verifique de novo com `git config --global user.name` e `git config --global user.email`

**Importante:** Se o usuario tem um email especifico usado no GitHub (ex: `guilherme@v4company.com`), use ESSE email. Ele pode confirmar indo em https://github.com/settings/emails.

### Check 3 — Default branch = main

```bash
git config --global init.defaultBranch
```

- **Ok:** retorna `main`
- **Quebrado:** vazio ou `master`

**Correcao:**
```bash
git config --global init.defaultBranch main
```

Isso evita que novos repos criados localmente saiam com `master` (o GitHub usa `main`, causa confusao no primeiro push).

### Check 4 — GitHub CLI (`gh`) instalado

```bash
gh --version
```

- **Ok:** output tipo `gh version 2.x.y`
- **Quebrado:** "command not found"

**Por que importa:** O `/compartilhar-skill` usa `gh pr create` pra abrir PRs automaticamente. Sem `gh`, o usuario teria que abrir PR manualmente pelo site — friccao alta.

**Correcao:**
- **Mac:** `brew install gh`
- **Windows:** `winget install --id GitHub.cli` ou baixar em https://cli.github.com
- **Linux:** https://github.com/cli/cli/blob/trunk/docs/install_linux.md

### Check 5 — `gh` autenticado

```bash
gh auth status
```

- **Ok:** mostra "Logged in to github.com as {username}"
- **Quebrado:** "You are not logged into any GitHub hosts"

**Correcao:**

Rode `gh auth login` e guie o usuario:

1. Selecione **GitHub.com**
2. Selecione **HTTPS** (mais simples que SSH pra nao-tecnicos)
3. Quando perguntar "Authenticate Git with your GitHub credentials?" → **Yes**
4. "How would you like to authenticate GitHub CLI?" → **Login with a web browser**
5. Copie o codigo que aparece, aperte Enter, o browser abre, cole o codigo, aprove

Apos login, rode `gh auth status` de novo pra confirmar.

**Tambem verifique** que o git ta usando as credenciais do gh:
```bash
gh auth setup-git
```

### Check 6 — Repo Builders Hub corretamente configurado

Primeiro detecte onde o usuario esta:

```bash
pwd
git rev-parse --show-toplevel 2>/dev/null
```

Se nao estiver dentro do builders-hub, pergunte onde ele baixou e faca `cd`.

Dentro do repo, verifique:

```bash
git remote -v
```

- **Ok:** mostra remote `origin` apontando pra `https://github.com/{org}/builders-hub.git` (ou `.git` no final)
- **Quebrado (caso A):** sem remote algum (usuario baixou ZIP em vez de clonar)
- **Quebrado (caso B):** remote apontando pra fork antigo ou URL errada

**Correcao caso A (baixou ZIP):**

ZIP nao tem historia git. O ideal e re-clonar. Guie:

1. Mova a pasta atual pra outro lugar (caso tenha arquivos pessoais em `clientes/` ou `bases/`)
2. Clone de novo:
   ```bash
   git clone https://github.com/V4-Company/builders-hub.git
   ```
3. Mova de volta os arquivos de `clientes/` e `bases/` pro novo clone (eles sao gitignored, ficam locais)

**Correcao caso B (remote errado):**
```bash
git remote set-url origin https://github.com/V4-Company/builders-hub.git
```

### Check 7 — Branch atual = main (ou tem rastreamento correto)

```bash
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null
```

- **Ok:** branch e `main` e upstream e `origin/main`
- **Quebrado:** branch detached ou sem upstream

**Correcao:**
```bash
git checkout main
git branch --set-upstream-to=origin/main main
```

### Check 8 — Python 3 (pra rodar build-registry.py localmente)

```bash
python3 --version
```

- **Ok:** retorna `Python 3.x.y` com x >= 8
- **Quebrado:** "command not found" ou versao < 3.8

**Correcao:**
- **Mac:** `brew install python@3.11`
- **Windows:** https://www.python.org/downloads/ (marque "Add to PATH")
- **Linux:** `sudo apt install python3`

### Check 9 — Teste ponta-a-ponta (opcional mas recomendado)

Faca um commit de validacao em branch descartavel pra confirmar que pushes funcionam:

```bash
git checkout -b verificar-setup-test
git commit --allow-empty -m "test: validando setup"
git push -u origin verificar-setup-test
```

- **Ok:** push sucesso, mostra URL do branch no GitHub
- **Quebrado:** erro de auth, permission denied, etc.

Se passou, limpe:
```bash
git push origin --delete verificar-setup-test
git checkout main
git branch -D verificar-setup-test
```

Se falhou, o erro vai indicar qual check anterior precisa ser reajustado (normalmente auth do gh ou email da identidade).

---

## Relatorio final

Depois de rodar todos os checks, mostre um resumo pro usuario:

```
✅ Setup Builders Hub OK

Git: 2.43.0
Identidade: Guilherme Lippert <guilherme@v4company.com>
GitHub CLI: autenticado como guilherme-1708
Repo: builders-hub na branch main
Python 3: 3.11.5

Pronto pra usar /sync-hub e /compartilhar-skill.
```

Ou, se algo ficou pendente:

```
⚠ Setup incompleto

Pendente: [lista do que falta]

Resolva isso antes de rodar /compartilhar-skill (senao o PR nao vai abrir).
```

## Quando re-rodar

- Toda vez que o usuario trocar de maquina
- Apos qualquer erro de push/pull
- Antes do primeiro `/compartilhar-skill` da sessao
- Se o usuario pediu `/onboarding` (onboarding chama essa skill primeiro)

## Observacoes

- Se o usuario esta em um ambiente corporativo com proxy/firewall, pushes HTTPS podem falhar. Nesse caso, oriente a usar SSH (`gh auth login` com opcao SSH) e documente no relatorio final.
- Se o usuario nao tem conta GitHub, guie ele a criar em https://github.com/join antes de qualquer outra coisa — sem conta, nada do hub funciona.
- Nao salve tokens/credenciais em arquivo nenhum. Tudo fica no keychain do sistema operacional via `gh auth`.
