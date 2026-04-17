---
name: sync-hub
description: Atualiza o Builders Hub local puxando as skills mais recentes do repo publico, mostra diff do que mudou desde a ultima sync e regenera o REGISTRY.md. Use quando o usuario rodar /sync-hub, quiser "baixar as skills novas do time", "atualizar meu hub" ou similar. Preserva arquivos pessoais de clientes/ e bases/ (gitignored). Lida com conflitos de forma segura e guia o usuario se algo precisar de resolucao manual.
---

# /sync-hub — Atualiza o Builders Hub local

Faz o usuario receber as skills novas que o time compartilhou desde a ultima vez que ele rodou. Pensado pra ser 100% seguro: nao toca em arquivos pessoais, nao descarta trabalho em andamento, e guia qualquer conflito passo a passo.

## Pre-requisitos

Rode os checks minimos:

```bash
git rev-parse --show-toplevel
git remote -v | grep origin
gh auth status
```

Se qualquer falhar, chame `/onboarding` (os checks de setup sao a primeira coisa que ele faz).

## Fluxo

### Passo 1 — Mapear estado atual

```bash
# Branch atual
CURRENT_BRANCH=$(git branch --show-current)

# Tem mudancas nao commitadas?
git status --porcelain
```

- Se tem mudancas nao commitadas, salve em stash com mensagem descritiva:
  ```bash
  git stash push -u -m "sync-hub-auto-$(date +%s)"
  ```
  Lembre-se dessa stash pra restaurar no fim.

- Se o usuario esta em uma branch que NAO e main (ex: `skill/trafego-x` de um PR em aberto), **nao force ele pra main**. Sync funciona assim:
  1. Salva a branch atual (`ORIG_BRANCH=$CURRENT_BRANCH`)
  2. Vai pra main, sincroniza
  3. Volta pra branch original
  4. Rebase opcional da branch em cima da main nova (pergunte antes)

### Passo 2 — Capturar ponto de referencia pra diff

Se existe `.sync-hub-last` na raiz do repo, le o SHA de la — e o commit da ultima sync bem-sucedida. Se nao existe, use o commit atual de main local:

```bash
if [ -f .sync-hub-last ]; then
  LAST_SHA=$(cat .sync-hub-last)
else
  LAST_SHA=$(git rev-parse main 2>/dev/null || echo "")
fi
```

### Passo 3 — Fetch + fast-forward main

```bash
git fetch origin main --quiet

git checkout main
git pull --ff-only origin main
```

`--ff-only` garante que a gente so avanca. Se der erro (`not a fast-forward`), significa que o usuario commitou coisa direto na main local (nao deveria). Nesse caso:
1. Mostre `git log main..origin/main` e `git log origin/main..main`
2. Explique: "Voce tem commits na sua main local que nao estao no remoto. Isso acontece quando alguem commita direto sem branch. Vou criar uma branch `rescue-local-main` com seus commits e resetar main pra origin. Ok?"
3. Se ele topar: `git branch rescue-local-main && git reset --hard origin/main`

### Passo 4 — Calcular o que mudou desde a ultima sync

```bash
NEW_SHA=$(git rev-parse main)

if [ -n "$LAST_SHA" ] && [ "$LAST_SHA" != "$NEW_SHA" ]; then
  # Arquivos que viraram skills novas
  git diff --name-only --diff-filter=A "$LAST_SHA" "$NEW_SHA" -- ".claude/skills/"
  # Arquivos de skills atualizadas
  git diff --name-only --diff-filter=M "$LAST_SHA" "$NEW_SHA" -- ".claude/skills/"
fi
```

Agrupe por skill (pegue o diretorio pai dentro de `.claude/skills/`) e monte um resumo:

```
✨ 3 skills novas desde sua ultima sync:
  • trafego-analise-anomalias (por @deborah, v1.0.0)
  • criativo-briefing-corretor (por @fernanda, v1.0.0)
  • cs-checkin-ppt (por @joao, v1.2.0)

🔄 1 skill atualizada:
  • trafego-diagnostico-diario (por @guilherme, v1.0.0 → v1.1.0)
```

Se for a primeira sync (sem `.sync-hub-last`), mostre a contagem total de skills no hub em vez de diff.

### Passo 5 — Espelhar skills pra `.agents/`

A GitHub Action SO atualiza `.claude/skills/` (porque e a source-of-truth do build-registry). Mas o usuario usa Anti-Gravity tambem, que le `.agents/skills/`. Entao depois de pull, rode:

```bash
rsync -a --delete ".claude/skills/" ".agents/skills/"
```

Se `rsync` nao estiver disponivel (Windows nativo), fallback Python:
```bash
python3 -c "
import shutil, pathlib
src = pathlib.Path('.claude/skills')
dst = pathlib.Path('.agents/skills')
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src, dst)
"
```

**Importante:** o rsync/copy nao toca em `clientes/` ou `bases/`, porque essas pastas estao fora de `.claude/skills/`.

### Passo 6 — Regenerar REGISTRY.md local

```bash
python3 scripts/build-registry.py
```

Isso regenera o index humano localmente pra o usuario navegar.

### Passo 7 — Salvar marker de sync

```bash
echo "$NEW_SHA" > .sync-hub-last
```

`.sync-hub-last` fica no `.gitignore` (so local, nao sobe pro repo).

### Passo 8 — Voltar pro estado original do usuario

Se o usuario estava em outra branch:

```bash
git checkout "$ORIG_BRANCH"
```

Pergunte se quer rebase:
> "Voce estava na branch `skill/trafego-x`. Quer que eu rebase ela em cima da main nova? Isso garante que seu PR nao vai dar conflito. (Recomendado: sim)"

Se sim: `git rebase main` (e se der conflito, pare e guie).

Se tinha stash, restaure:

```bash
git stash pop
```

Se o pop der conflito, pare e mostre os arquivos em conflito pro usuario resolver.

### Passo 9 — Garantir que `.sync-hub-last` esta no gitignore

Se ainda nao tiver, adicione:

```bash
grep -q ".sync-hub-last" .gitignore || echo ".sync-hub-last" >> .gitignore
```

### Passo 10 — Relatar

```
✅ Sync completa

Estado anterior: {LAST_SHA:0:7}
Estado atual:    {NEW_SHA:0:7}

✨ 3 skills novas | 🔄 1 atualizada | 📦 48 skills totais

Ver tudo em: REGISTRY.md (no seu repo local)
```

## Tratamento de erros

### Usuario nao esta no repo builders-hub
`git rev-parse --show-toplevel` nao retornar nada, ou retornar path diferente: pare e oriente `cd` pra o repo.

### `git pull --ff-only` falha
Ja tratado no passo 3 (branch `rescue-local-main`).

### `stash pop` conflita
Mostre arquivos em conflito. Oriente: "Resolva os conflitos, `git add` os arquivos, e rode `git stash drop` pra limpar a stash antiga."

### Rebase da branch do usuario conflita
Pare, mostre os conflitos, oriente:
> "Rebase deu conflito em X, Y, Z. Abra cada arquivo, resolva os marcadores `<<<<<<<`, salve, rode `git add <arquivo>`, depois `git rebase --continue`. Se quiser abortar, rode `git rebase --abort`."

### Usuario sem internet
`git fetch` vai falhar. Detecte timeout/erro de rede, mostre mensagem clara: "Sem conexao com o remote. Verifique sua internet e tente de novo."

## O que NUNCA fazer

- Forcar push (essa skill so pulls, nao push nada)
- Descartar stash/mudancas sem confirmar
- Resetar branch do usuario sem ele aceitar (passo 3 exige confirmacao)
- Tocar em `clientes/` ou `bases/` (sao gitignored e sagradas — sao dados pessoais)
- Apagar `.sync-hub-last` (e o estado de progresso)

## Observacoes

- O `.sync-hub-last` so serve pra mostrar o "diff desde a ultima sync". Se o usuario apagar, a proxima sync mostra tudo como "primeira vez" mas nao quebra nada.
- Sync deve ser **idempotente**: rodar duas vezes seguidas nao faz mal (segunda rodada mostra "0 skills novas").
- A skill nunca falha silenciosamente. Se qualquer passo critico falhar (pull, rsync, build-registry), pare e mostre erro claro pro usuario, em vez de seguir pretendendo que deu certo.
