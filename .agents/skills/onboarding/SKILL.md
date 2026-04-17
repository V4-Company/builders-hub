---
name: onboarding
description: Configura o ambiente do usuario para trabalhar com IA na V4 via o Builders Hub. Valida git 100%, instala dependencias, ensina a usar o repositorio, as skills e o fluxo de sync/compartilhamento. Use quando o usuario rodar /onboarding ou quando for a primeira vez usando o repositorio. Sempre chama /verificar-setup primeiro — git quebrado trava todo o resto.
---

Voce e um assistente de setup que vai guiar o usuario na configuracao do ambiente e ensinar como usar o Builders Hub.

## Objetivo

Garantir que o usuario saia com:
1. **Git 100% configurado** (validado pelo /verificar-setup — pre-requisito obrigatorio)
2. Dependencias instaladas (Node.js, Python, Claude Code, notebooklm-py)
3. Entendimento claro de como o Builders Hub funciona (repo + skills + compartilhamento)
4. Sabendo usar cada skill disponivel
5. Pronto pra trabalhar, puxar skills do time (`/sync-hub`) e contribuir de volta (`/compartilhar-skill`)

## Processo

### Passo 0 — Abrir o tutorial

Antes de qualquer coisa, abra o tutorial visual no browser do usuario:

```bash
open tutorial.html   # Mac
# ou
start tutorial.html  # Windows
```

Diga: "Abri o tutorial no seu browser. Ele explica visualmente tudo sobre o Builders Hub. Pode deixar aberto pra consultar enquanto a gente configura."

### Passo 0.5 — Validar setup git/gh (CRITICO, NAO PULE)

Antes de instalar qualquer outra dependencia ou ensinar qualquer coisa, garanta que o fundamento ta 100%. **Invoque /verificar-setup agora**.

A /verificar-setup vai rodar bateria completa:
- Git instalado
- Git identity configurada (user.name + user.email)
- Default branch = main
- GitHub CLI (gh) instalado + autenticado
- Repo builders-hub com remote correto e na branch main
- Python 3.8+
- Teste ponta-a-ponta de push em branch descartavel

**Regra de ouro:** se /verificar-setup retornar qualquer pendencia (⚠), PARE o onboarding aqui. Resolva com o usuario, re-rode /verificar-setup ate ficar 100% ✅, e so ai siga pro Passo 1.

Por que isso importa: sem git bem configurado, `/sync-hub` nao baixa skills novas, `/compartilhar-skill` nao consegue abrir PR, e commits do usuario ficam com identidade quebrada. Tudo o resto do Builders Hub depende dessa base. Nao vale a pena seguir sem isso.

### Passo 1 — Detectar sistema operacional

Rode `uname -s` ou equivalente para detectar se e Mac ou Windows. Adapte todos os comandos seguintes conforme o SO detectado.

### Passo 2 — Verificar Node.js e npm

Rode `node --version` e `npm --version`.

**Se instalado:** confirme as versoes e siga.

**Se NAO instalado:**

Mac:
```bash
brew install node
```

Se nao tem brew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install node
```

Windows:
- Guie o usuario para baixar e instalar em https://nodejs.org (versao LTS)
- Apos instalar, peca pra fechar e reabrir o terminal

Confirme que `node --version` e `npm --version` retornam versoes validas antes de prosseguir.

### Passo 3 — Verificar Python

Rode `python3 --version` (Mac/Linux) ou `python --version` (Windows).

**Se instalado:** confirme a versao (precisa ser 3.10+) e siga.

**Se NAO instalado:**

Mac:
```bash
brew install python
```

Windows:
- Guie o usuario para https://python.org/downloads (versao 3.12+)
- IMPORTANTE: marcar "Add Python to PATH" durante a instalacao

### Passo 4 — Instalar Claude Code

Rode `claude --version`.

**Se instalado:** confirme a versao e siga.

**Se NAO instalado:**

Mac:
```bash
brew install claude-code
```

Windows:
```bash
npm install -g @anthropic-ai/claude-code
```

Peca pro usuario autenticar com `claude` se for a primeira vez (vai abrir o browser).

### Passo 5 — Instalar notebooklm-py

```bash
pip install "notebooklm-py[browser]"
playwright install chromium
```

Apos instalar, rode:
```bash
notebooklm login
```

Isso abre um browser Chromium. O usuario faz login com a conta Google dele. Os cookies sao salvos automaticamente em `~/.notebooklm/`.

Teste se funcionou:
```bash
notebooklm list
```

Se retornar a lista de notebooks (mesmo que vazia), esta funcionando.

### Passo 6 — Identificar o perfil do usuario

Pergunte:
> "Voce atua diretamente operando clientes na V4? (sim/nao)"

Guarde a resposta. Isso define quais skills sao relevantes e como explicar o repositorio.

- **Sim (operacao):** vai usar `clientes/`, `/novo-cliente`, `/contexto`
- **Nao (outras areas):** vai usar `bases/`, `/contexto`

### Passo 7 — Ensinar o repositorio

Explique o que e cada coisa e como usar:

---

**"Esse repositorio e sua base de trabalho com IA. Tudo que voce precisa ta aqui dentro."**

**CLAUDE.md / AGENTS.md**
> "Esse arquivo e o cerebro. A IA le ele automaticamente toda vez que voce abre esse repositorio. Ele diz pra IA como se comportar, que skills existem e como trabalhar com seus dados."

**Knowledge Bases (pastas de dados)**

Se operacao:
> "A pasta `clientes/` e onde ficam os dados dos seus clientes. Cada cliente tem sua propria pasta com calls (transcricoes de reunioes), docs (documentos) e campanhas (dados de performance). Quanto mais dados voce coloca, melhor a IA trabalha."

Se outras areas:
> "A pasta `bases/` e onde ficam os dados dos seus projetos. Cada projeto tem sua propria pasta com docs, dados e referencias. Quanto mais dados voce coloca, melhor a IA trabalha."

---

### Passo 8 — Ensinar as skills

Explique cada skill disponivel com exemplos praticos:

**`/onboarding`**
> "Essa que voce ta rodando agora. So precisa rodar uma vez pra configurar tudo."

**`/verificar-setup`**
> "Valida git, GitHub CLI e dependencias. Roda automatico aqui no onboarding e toda vez que algo do fluxo git/sync quebrar. Se der problema de push, conflito, PR nao abrir — roda `/verificar-setup` que ela diagnostica e corrige."

**`/sync-hub`**
> "Puxa as skills mais recentes que o time compartilhou no hub publico. Roda de tempos em tempos pra sempre ter o que ha de mais novo. Mostra resumo do que chegou desde a ultima sync (skills novas, atualizadas)."

**`/compartilhar-skill`**
> "Quando voce criou uma skill que funciona bem e quer que o time inteiro use tambem, roda `/compartilhar-skill`. Ela valida que ta tudo certo, cria uma branch, faz o commit e abre um Pull Request automatico pro curador (o Guilherme) aprovar. Voce nao precisa saber git — a skill faz tudo. Exemplo: voce criou uma skill `/trafego-analise-anomalias` que funciona bem. Roda `/compartilhar-skill`, confirma os dados, e em 5 segundos ta la um PR no GitHub pra review."

**`/novo-cliente`** (so pra operacao)
> "Toda vez que voce pegar um cliente novo, roda `/novo-cliente`. Ele cria a pasta com a estrutura certa, pergunta se o cliente tem NotebookLM e ja deixa tudo pronto. Exemplo: voce roda `/novo-cliente`, digita 'Empresa X', cola o link do NotebookLM e pronto — pasta criada com tudo configurado."

**`/novo-projeto`** (so pra outras areas)
> "Mesma ideia do `/novo-cliente`, mas pra projetos. Roda `/novo-projeto`, digita o nome do projeto e pronto — pasta criada com docs, dados e referencias."

**`/contexto`**
> "Depois que voce jogou os dados na pasta (calls, docs, etc), roda `/contexto`. A IA le TUDO que tem la dentro e gera um resumo completo — o CLAUDE.md do cliente ou projeto. A partir dai, toda vez que voce trabalhar nessa pasta, a IA ja sabe tudo. Exemplo: voce jogou 3 transcricoes de call e 2 relatorios de campanha. Roda `/contexto` e a IA gera um resumo com: quem e o cliente, o que foi combinado, como tao as metricas, o que ta pendente."

**`/criador-de-skills`**
> "Essa e a mais poderosa. Quando voce fizer algo com a IA que ficou bom — uma analise, um relatorio, um check-in — voce pode transformar esse processo em uma skill. Ai na proxima vez voce so roda a skill e a IA faz igual. Exemplo: voce usou a IA pra preparar um check-in e ficou otimo. Roda `/criador-de-skills`, descreve o que fez, e ela cria uma skill `/check-in` que repete o processo toda vez."

**`/brainstormar-sobre-minha-funcao`**
> "Essa skill e pra quem nao sabe por onde comecar. Ela te entrevista sobre o seu trabalho — o que voce faz, suas tarefas, sua agenda — e descobre onde a IA agrega mais valor pra voce. No final ela atualiza o CLAUDE.md com seu perfil pra IA sempre saber quem voce e. Recomendo rodar agora se voce quer um mapa personalizado de como usar isso tudo."

**`/sabatina`**
> "Quando voce tiver um plano ou ideia e quiser testar se faz sentido, roda `/sabatina`. A IA vai questionar cada aspecto do seu plano ate voce ter certeza de que esta bom. Funciona pra estrategia de cliente, proposta, campanha — qualquer coisa que precise ser stress-testada."

**`notebooklm` (CLI)**
> "O NotebookLM e uma ferramenta do Google pra criar bases de conhecimento. Com o `notebooklm` instalado, voce pode criar notebooks, adicionar fontes e ate gerar podcasts automaticamente pelo terminal. Exemplo: `notebooklm create 'Cliente X'` cria um notebook, `notebooklm source add ./arquivo.pdf` adiciona um arquivo, `notebooklm ask 'resumo do cliente'` pergunta pra base."

### Passo 9 — Resumo e proximos passos

Mostre um checklist do que foi configurado:
- [ ] Git 100% (identidade, remote, gh autenticado) — via /verificar-setup
- [ ] Node.js + npm
- [ ] Python 3.10+
- [ ] Claude Code
- [ ] notebooklm-py

Depois diga:

> "Tudo pronto. Recomendo comecar por:"

**Passo 1 (todo mundo):**
> "Roda `/sync-hub` pra puxar as skills mais novas que o time ja compartilhou. Assim voce ja comeca com tudo disponivel."

**Passo 2 (todo mundo):**
> "Depois roda `/brainstormar-sobre-minha-funcao`. Ela vai te entrevistar sobre seu trabalho e montar um plano personalizado de como usar IA no seu dia a dia. E o melhor primeiro passo de uso real."

**Passo 3, se operacao:**
> "Depois, rode `/novo-cliente` pra criar seu primeiro cliente, jogue os dados e rode `/contexto`."

**Passo 3, se outras areas:**
> "Depois, rode `/novo-projeto` pra criar seu primeiro projeto, jogue seus dados e rode `/contexto`."

**Passo 4 (todo mundo):**
> "Quando algo funcionar bem, rode `/criador-de-skills` pra transformar em skill reutilizavel. E quando a skill estiver redonda, `/compartilhar-skill` leva ela pro hub publico — o time inteiro passa a poder usar."

**Lembrete final:**
> "O Builders Hub cresce com quem contribui. Cada skill boa que voce compartilhar economiza horas do time. Quando a sua primeira skill cair no hub, seu github handle aparece no REGISTRY.md como author — isso e reconhecimento publico."

## Tom

- Direto, sem enrolacao
- Se algo falhar, nao entre em panico — explique o que deu errado e como resolver
- Nao assuma conhecimento tecnico — explique cada passo como se fosse a primeira vez que a pessoa usa um terminal
- Use exemplos concretos quando explicar as skills — abstrato nao cola
