# Guia de Instalacao

## Passo 1 — Baixar o repositorio

1. Instale o Git se ainda não tiver: [git-scm.com](https://git-scm.com/downloads)
2. Abra um terminal na pasta onde quer guardar o Hub
3. Rode:

```bash
git clone https://github.com/V4-Company/builders-hub.git
cd builders-hub
```

O ZIP serve apenas para leitura. Sem um clone Git, `/sync-hub`, commits e Pull Requests não funcionam.

## Passo 2 — Instalar o Anti-Gravity

### Mac
1. Acesse [antigravity.dev](https://antigravity.dev)
2. Baixe o instalador para Mac
3. Arraste para a pasta Aplicativos
4. Abra o Anti-Gravity

### Windows
1. Acesse [antigravity.dev](https://antigravity.dev)
2. Baixe o instalador para Windows
3. Rode o instalador e siga as instrucoes
4. Abra o Anti-Gravity

## Passo 3 — Instalar a extensao do Claude

1. No Anti-Gravity, clique no icone de **Extensions** (quadradinhos) na barra lateral esquerda
2. Busque por **"Claude"**
3. Clique em **Install**
4. Quando pedido, conecte sua conta Anthropic

## Passo 4 — Abrir o repositorio

1. No Anti-Gravity: **File > Open Folder**
2. Navegue ate a pasta `builders-hub` que voce descompactou
3. Clique em **Open**

## Passo 5 — Abrir o terminal

1. Use o atalho: `Ctrl + ~` (Windows) ou `Cmd + ~` (Mac)
2. Ou va em: **View > Terminal**
3. O terminal vai abrir na parte de baixo da tela

## Passo 6 — Rodar o onboarding

No terminal, digite:
```
/onboarding
```

A skill valida git e GitHub CLI primeiro (garante que seu push/PR vao funcionar), depois instala o que faltar (Claude Code CLI, notebooklm, etc) e te mostra como compartilhar skills com o time via `/compartilhar-skill`.

## Passo 7 — Dependencias dos scripts

Se for usar integrações por API, instale as dependências Python na raiz do repositório:

```bash
python3 -m pip install -r requirements.txt
```

Para confirmar que o clone está consistente:

```bash
python3 scripts/validate-repo.py
python3 scripts/build-registry.py --check
python3 scripts/run-tests.py
```

O Builders Hub não possui servidor, banco, migrations ou processo residente. Depois da instalação não há serviço para iniciar ou reiniciar: as skills são usadas diretamente pelo agente.

## Problemas comuns

**"Comando nao encontrado"**
- Verifique se a extensao do Claude esta instalada e ativa
- Tente fechar e reabrir o Anti-Gravity

**"Erro de autenticacao"**
- Va em Extensions > Claude > Settings e reconecte sua conta

**"MCP nao conecta"**
- Verifique sua conexao com a internet
- Tente rodar `/onboarding` novamente — ele vai tentar reconectar

**"No module named requests"**
- Rode `python3 -m pip install -r requirements.txt` na raiz do repositório
