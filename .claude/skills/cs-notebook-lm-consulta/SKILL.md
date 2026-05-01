---
name: cs-notebook-lm-consulta
description: Consulta o NotebookLM de um cliente especifico decompondo uma tarefa em ate 5 perguntas direcionadas, dispara contra o NotebookLM via CLI notebooklm-py, agrega as respostas em sintese executiva e salva tudo num artefato datado em clientes/<cliente>/contexto-notebook/. Use sempre que o usuario rodar /notebook-lm-consulta, pedir pra "consultar o NotebookLM do cliente X sobre Y", "puxar contexto do cliente X pra tarefa Y", "buscar insumos no NotebookLM do cliente", "preparar briefing usando o NotebookLM", ou quando ele quiser informacao de um cliente especifico SEM carregar arquivos locais no contexto. Ative tambem se o usuario diz "ja tem NotebookLM cadastrado, busca la" ou "quero economizar tokens consultando o notebook".
area: cs
author: junioraiellogestaodetrafego
version: 1.0.0
---

# notebook-lm-consulta — Consulta direcionada a NotebookLM

Dado um cliente e uma tarefa, decompoe a tarefa em ate 5 perguntas fechadas, dispara contra o NotebookLM do cliente, agrega num briefing executivo, e salva o artefato datado.

Existe pra resolver o caso "preciso de contexto desse cliente pra esta tarefa especifica, mas nao quero carregar 50 arquivos no chat". O ganho real aparece quando o cliente tem base volumosa (calls transcritas, varios docs, briefings) e voce quer respostas pontuais, nao analise transversal.

## Pre-requisitos

- `notebooklm-py` instalado e autenticado. Se nao estiver, rode `notebooklm login`.
- O cliente precisa ter o bloco `## NotebookLM` cadastrado em `clientes/<cliente>/CLAUDE.md`. Se nao tem, rode `/notebooklm-cadastrar` antes.

## Quando usar

- Usuario roda `/notebook-lm-consulta <cliente> "<tarefa>"`.
- Usuario diz "consulta o NotebookLM do <cliente> sobre <X>".
- Usuario diz "puxa contexto do <cliente> pra eu preparar <Y>".
- Usuario quer briefing baseado em conhecimento ja registrado no NotebookLM, sem carregar arquivos locais.

**Nao confundir com `/contexto`:** `/contexto` le arquivos locais e gera CLAUDE.md rico (uso amplo, uma vez por cliente). Esta skill aqui consulta NotebookLM remoto pra uma tarefa especifica (uso pontual, varias vezes). As duas convivem.

## Fluxo

### Passo 1 — Validar argumentos

Voce precisa de **dois** inputs:
- `<cliente>`: nome normalizado (lowercase + hifens, ex: `empresa-x`).
- `<tarefa>`: prompt em linguagem natural sobre o que voce quer descobrir.

Se faltar algum, peca antes de prosseguir.

### Passo 2 — Validar cliente

- Verifique se `clientes/<cliente>/` existe. Se nao, aborte com:
  > "Cliente `<X>` nao tem pasta. Roda `/novo-cliente` primeiro."

- Leia `clientes/<cliente>/CLAUDE.md`. Procure pelo bloco `## NotebookLM` e extraia o **Notebook ID** (linha `- **Notebook ID:** <ID>`).

- Se nao encontrar o bloco ou o ID, aborte com:
  > "Cliente `<X>` nao tem NotebookLM cadastrado. Roda `/notebooklm-cadastrar` ou edita o CLAUDE.md manualmente."

### Passo 3 — Echo de protecao contra typo

Antes de disparar qualquer pergunta, ecoe pro usuario:

> "Vou consultar o NotebookLM de **<Cliente>** (notebook ID: `<id-resumido-ate-8-chars>...`) pra tarefa: <tarefa>. Disparando agora."

Isso permite o usuario interromper se digitou cliente errado por engano.

### Passo 4 — Decompor a tarefa em perguntas

Transforme a tarefa em **ate 5 perguntas independentes e fechadas**. Limite e 5: se a tarefa parece demandar mais, priorize as 5 mais valiosas — qualidade > quantidade.

**Cada pergunta deve:**
- Ser fechada e especifica (escopo, periodo, angulo claros).
- Pedir citacao literal da fonte ("cite o trecho exato e a fonte").
- Incluir literalmente esta protecao anti-alucinacao no final:
  > "Se a informacao nao estiver disponivel, responda exatamente 'NAO ENCONTRADO'. Nao invente."

**Por que perguntas independentes:** o `notebooklm-py` e stateless entre chamadas — nao tem memoria de pergunta pra pergunta. Cada uma tem que se sustentar sozinha. Nao adianta fazer "aprofunde a anterior" — vai vir resposta solta.

**Por que fechadas:** NotebookLM diverga e generaliza com pergunta aberta. Fechada = especifica = resposta cirurgica.

**Exemplo de decomposicao** (tarefa: "vou montar campanha de Black Friday"):
1. Quais ofertas o cliente <X> ja realizou em campanhas sazonais anteriores? Cite o documento e o trecho exato. Se nao houver registro, responda 'NAO ENCONTRADO'.
2. Qual e o ticket medio mencionado nos materiais e em que documento aparece? Se nao houver, 'NAO ENCONTRADO'.
3. Quais sao os principais segmentos de cliente identificados nas calls/briefings? Cite a fonte literal. Se nao houver, 'NAO ENCONTRADO'.
4. Existe alguma restricao documentada sobre tipo de oferta (descontos, parcelamentos, brindes)? Cite. Se nao houver, 'NAO ENCONTRADO'.
5. Quem e o decisor final de aprovacao criativa segundo os materiais? Cite o trecho. Se nao houver, 'NAO ENCONTRADO'.

### Passo 5 — Disparar perguntas em sequencia

Pra cada pergunta, execute **em sequencia (nao paralelo)**:

```bash
notebooklm ask "<pergunta-completa-com-anti-alucinacao>" --notebook <notebook-id>
```

Por que sequencial: `notebooklm-py` e browser automation (sobe Chromium headless). Em paralelo, ele engasga e respostas se misturam ou falham.

**Tratamento de erro de sessao:** se qualquer chamada retornar erro tipo "auth", "session expired", "login required" ou similar, **aborte imediatamente** com:

> "Sessao NotebookLM expirou. Roda `notebooklm login` e tenta de novo."

Nao tente relogar automaticamente — se algo der errado no Chromium, voce trava de um jeito ruim de debugar. Erro claro + comando manual e melhor.

### Passo 6 — Salvar artefato

Crie a pasta se nao existir: `clientes/<cliente>/contexto-notebook/`.

Salve em: `clientes/<cliente>/contexto-notebook/<YYYY-MM-DD-HHMM>-<slug-da-tarefa>.md`

- `YYYY-MM-DD-HHMM`: data e hora da execucao (ordenacao alfabetica = cronologica).
- `slug-da-tarefa`: 3-6 palavras-chave da tarefa em kebab-case (ex: `black-friday`, `preparacao-call-icp`, `briefing-criativo`).

**Formato exato do arquivo:**

```markdown
# <Tarefa> — <Cliente> — <YYYY-MM-DD HH:MM>

## Tarefa original
<prompt original do usuario, na integra>

## Perguntas disparadas
1. <pergunta 1>
2. <pergunta 2>
...

## Respostas

### 1. <pergunta 1>
<resposta literal do NotebookLM, incluindo citacoes que ele retornou>

### 2. <pergunta 2>
<resposta literal>

...

## Sintese
<1-3 paragrafos agregando as respostas pra responder a tarefa original. Aqui voce conecta os pontos: o que isso significa pra acao que o usuario quer tomar? Nao repete as respostas — sintetiza.>
```

### Passo 7 — Devolver no chat

No chat, devolva **dois blocos**:

1. A sintese (copia do conteudo da secao `## Sintese`).
2. O caminho do arquivo salvo, formato clicavel:
   `Arquivo salvo em [clientes/<cliente>/contexto-notebook/<arquivo>.md](clientes/<cliente>/contexto-notebook/<arquivo>.md)`

## Exemplo completo

**Input:**
```
/notebook-lm-consulta empresa-x "vou montar uma campanha de Black Friday e preciso entender o historico de ofertas e o publico"
```

**Skill responde (echo):**
> Vou consultar o NotebookLM de **empresa-x** (notebook ID: `abc12345...`) pra tarefa: vou montar uma campanha de Black Friday e preciso entender o historico de ofertas e o publico. Disparando agora.

**Skill decompoe e dispara:**
- (5 perguntas como no Passo 4, em sequencia)
- (cada chamada leva 15-40s pelo `notebooklm-py`)

**Skill salva** em `clientes/empresa-x/contexto-notebook/2026-04-28-1430-black-friday.md`.

**Skill devolve no chat:**

```
## Sintese

Empresa-X realizou 2 campanhas sazonais anteriores (Black Friday 2024 e Natal 2024),
ambas com desconto progressivo + frete gratis acima de R$ 200. Ticket medio historico
de R$ 287, concentrado em 2 segmentos principais: ... [conteudo real]

Restricao documentada: nao usar imagens com modelos infantis (decisao da diretoria
em call de 2024-09). Decisor de aprovacao criativa: <Nome>, gerente de marketing.

Recomendacao implicita: replicar formato desconto progressivo + frete, evitar
imagens com criancas, submeter peca a <Nome> antes de subir.

Arquivo salvo em [clientes/empresa-x/contexto-notebook/2026-04-28-1430-black-friday.md](clientes/empresa-x/contexto-notebook/2026-04-28-1430-black-friday.md)
```

## Edge cases

- **Tarefa muito vaga** ("me fala desse cliente"): peca pro usuario refinar. Decompor em perguntas vazias gera respostas genericas que NotebookLM nao consegue ancorar.
- **Tarefa que precisa de mais de 5 perguntas:** priorize as 5 mais valiosas. Mencione na sintese: "limitei a 5 perguntas — se quiser aprofundar X, rode de novo focando nele."
- **NotebookLM responde 'NAO ENCONTRADO' em todas as 5 perguntas:** o cliente provavelmente nao tem material indexado sobre o tema. Salve o arquivo mesmo assim (registro do que foi tentado) e na sintese diga claramente: "NotebookLM nao tem material sobre esse tema. Considere rodar /contexto pra ler arquivos locais ou alimentar o NotebookLM com material novo."
- **Resposta do NotebookLM esta visivelmente errada/alucinada:** voce pode comentar na sintese ("a resposta 3 menciona X mas a citacao nao confirma — verificar"). NotebookLM as vezes ignora a instrucao de 'NAO ENCONTRADO'.
- **Cliente com NotebookLM vazio:** mesmo comportamento de "NAO ENCONTRADO em todas".

## Por que isso e importante

NotebookLM e otimo em consulta pontual ancorada em fontes (RAG nativo do Google). Pessimo em raciocinio transversal e analise comparativa. Esta skill explora o ponto forte (consulta cirurgica) e evita o ponto fraco (forcando perguntas fechadas e especificas em vez de abertas). A protecao 'NAO ENCONTRADO' reduz alucinacao — sem isso, NotebookLM as vezes inventa.

A latencia do `notebooklm-py` (~30s por pergunta) e o motivo do teto de 5: alem disso o usuario espera muito pra chegar no briefing, e o ganho marginal de cada pergunta extra cai. Se voce sentir que o teto esta apertado pra um caso, melhor rodar duas vezes com prompts diferentes do que aumentar o teto e gerar lentidao em todos os casos.
