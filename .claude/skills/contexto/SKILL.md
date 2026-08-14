---
name: contexto
description: Le todos os arquivos em uma KB (cliente, squad ou projeto), gera CLAUDE.md e AGENTS.md, e quando for cliente cria/atualiza mission-control/ com OKRs, apostas vivas, combinados, personas e historico de check-ins. Rodada na raiz do hub, gera o PANORAMA.local.md com a visao consolidada da carteira inteira: combinados em aberto de todos os clientes, sinais de atencao, apostas vivas e estado do hub. Detecta o nivel automaticamente. Use quando o usuario rodar /contexto, quiser que a IA "conheca" um cliente/squad/projeto, quiser criar/atualizar Mission Control de cliente, ou perguntar como esta a carteira inteira, o que ele deve pra quem, quais clientes estao esfriando ou o que esta em aberto no geral.
version: 1.1.0
---

Voce vai analisar uma Knowledge Base e gerar os arquivos `CLAUDE.md` e `AGENTS.md` que funcionem como "memoria" pra qualquer trabalho futuro. Quando a KB for de CLIENTE, tambem crie/atualize `mission-control/`, que e o estado vivo usado por skills de check-in. Quando o alvo for a raiz do hub, o resultado e outro: um `PANORAMA.local.md` que consolida a carteira inteira.

## Estrutura esperada

- `squads/{squad}/` — pasta de squad (tem `README.md` com membros, `docs/`, e subpasta `clientes/`)
- `squads/{squad}/clientes/{cliente}/` — pasta de cliente (tem `calls/`, `checkins/`, `docs/`, `campanhas/`, `links.md`, e pode ter `mission-control/`)
- `bases/{projeto}/` — pasta de projeto/area (tem `docs/`, `dados/`, `referencias/`)
- raiz do hub: a pasta que contem `REGISTRY.md`, `.claude/skills/`, `squads/` e `bases/`

**Padrao obrigatorio:** todo cliente vive em `squads/{squad}/clientes/{cliente}/`. Cliente solto, fora de squad, nao existe.

## Processo

### Passo 1 — Identificar a base

Detecte o que rodar com base na pasta corrente do usuario:

- **Pasta corrente e cliente** (tem `calls/`, `docs/`, `campanhas/`; `checkins/` pode existir ou ser criado; E nao tem subpasta `clientes/`): use ela direto.
- **Pasta corrente e squad** (tem subpasta `clientes/` E `README.md`): use ela direto.
- **Pasta corrente e projeto** (`bases/{X}/`): use ela direto.
- **Pasta corrente e a raiz do hub** (tem `REGISTRY.md` e `.claude/skills/`): pergunte antes de assumir, porque as duas coisas sao uteis daqui:

  > "Voce esta na raiz do hub. Quer o panorama geral da carteira (`PANORAMA.local.md`) ou o contexto de uma KB especifica?"

  Se pedir o panorama, siga o caminho HUB. Se pedir uma KB, caia no fallback abaixo.

- **Caso contrario:** liste todas as KBs disponiveis e pergunte:
  - Squads: `squads/*/` (ignorando `_template-*`)
  - Clientes: `squads/*/clientes/*/`
  - Projetos: `bases/*/` (ignorando `_template`)

### Passo 2 — Detectar o tipo

- **CLIENTE** (operacao): tem `calls/`, `docs/`, `campanhas/`; `checkins/` e recomendado
- **SQUAD**: tem subpasta `clientes/` e `README.md` com membros
- **PROJETO/AREA** (generico): tem `docs/`, `dados/`, `referencias/`
- **HUB**: a raiz do repositorio, com `REGISTRY.md` e `.claude/skills/`

### Passo 3 — Ler tudo

Leia TODOS os arquivos da pasta:

- **Cliente**: leia tudo em `calls/`, `checkins/`, `docs/`, `campanhas/`, `links.md`, `mission-control/` se existir, e qualquer outro arquivo.
- **Squad**: leia `README.md` e tudo em `docs/`. NAO leia o conteudo dos clientes filhos — so liste os nomes das pastas.
- **Projeto**: leia tudo recursivamente.

Leia cada arquivo por completo. Nao pule nada.

**Se for HUB, a regra e o contrario: leia pouco de muitos lugares.** Ler todas as calls de todos os clientes estoura o contexto e nao melhora o panorama. Leia so isto:

- De cada cliente em `squads/*/clientes/*/`: os arquivos de `mission-control/` (todos os 5) e o `CLAUDE.md`.
- De cada squad: o `README.md`.
- Metadados, nao conteudo, de `calls/` e `checkins/`: nome do arquivo, quantidade e data de modificacao do mais recente. Use `ls -lt` ou equivalente.
- Do hub: `REGISTRY.md`, saida de `git status --short` e a contagem de pastas em `.claude/skills/`.

Pegue a data de hoje do sistema (`date +%F`). Voce vai precisar dela para calcular atraso, e chutar a data corrente inventa numero.

### Passo 4 — Analisar e gerar

**Se for CLIENTE (operacao):**

Extraia: nome da empresa, segmento, produto/servico, publico-alvo, diferenciais, canais, investimento, metricas, contatos, combinados, pendencias, objetivos, teses, historico, proximos passos e aprendizados de check-ins. Tambem inclua os links uteis encontrados em `links.md`.

Gere o `CLAUDE.md` e o `AGENTS.md` (mesmo conteudo) com:

```markdown
# [Nome da Empresa]

## Resumo
[2-3 frases: quem e, o que faz, momento atual]

## Recursos
Veja `links.md` na raiz desta pasta pra todos os links uteis.
[Liste aqui os principais inline: NotebookLM, Drive, site — pra ja entrarem no contexto cascateado.]

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

## Quando trabalhar com este cliente
- Comece lendo `links.md` pra saber dos recursos disponiveis.
- Se o usuario compartilhar um link util durante a conversa, pergunte se quer adicionar a `links.md`.
```

Depois, crie ou atualize `mission-control/` na raiz do cliente com os 5 arquivos abaixo. Se o arquivo ja existir, preserve informacoes historicas e atualize com base no material novo. Nao apague aprendizados antigos sem evidencia clara de que ficaram obsoletos.

Garanta tambem que exista a pasta `checkins/` na raiz do cliente. Ela guarda pautas, ensaios, reviews e relatorios de check-in. Nao coloque transcripts brutos ali; transcripts ficam em `calls/`.

```text
mission-control/
|-- okr-quarter.md
|-- apostas-vivas.md
|-- combinados.md
|-- personas-call.md
`-- historico-checkins.md
```

**`okr-quarter.md`**
- Objetivo do quarter atual.
- KRs mensuraveis.
- Status atual e mes N de 3.
- Fonte usada (planejamento pos-kickoff, kickoff, check-in, docs).
- Se nao houver OKR explicito, escreva `[nao encontrado nos docs disponiveis]` e liste o que o account precisa preencher.

**`apostas-vivas.md`**
Use a tabela obrigatoria:

```markdown
| Aposta (o que cremos) | Por que apostamos | Como mata (sinal + prazo) | Plano B se morrer |
|---|---|---|---|
```

Registre 3 a 5 apostas estrategicas atuais. Cada aposta precisa ser testavel. Quando inferir criterio de morte ou plano B, marque `[INFERIDO - confirmar com account]`.

**`combinados.md`**
Separe pendentes, em andamento e feitos. Use o schema:

```markdown
- [ ] {dono} {acao} ate {prazo}
- [->] {dono} {acao} (em andamento)
- [x] {dono} {acao} (feito em {data})
```

Se nao houver dono ou prazo, marque `[A CONFIRMAR]`.

**`personas-call.md`**
Para cada stakeholder relevante, registre:
- Papel na conta.
- Arquetipo de call (ex: decisor agressivo, operacional cetico, estrategista, passivo).
- Voz e jeito de falar.
- Gatilhos.
- Padroes de provocacao.
- Como argumenta.
- Frases tipicas (citacao literal curta ou parafrase fiel).

Se nao houver check-ins salvos, pergunte ao account quais arquetipos parecem mais com os stakeholders e marque como `[declarado pelo account - refinar com proximas calls]`.

**`historico-checkins.md`**
Liste as calls em ordem cronologica:

```markdown
## YYYY-MM-DD - {Tipo da call}
**Modo:** TEM | SEM | ND
**Resumo (1 linha):** ...
**Transcript:** [link relativo](../calls/{arquivo}.md)
**Pontos criticos:**
- ...
```

Use `ND` para calls anteriores ao framework ROPRE V2 ou quando o modo nao estiver claro.

**Se for SQUAD:**

Extraia do `README.md`: nome do squad, membros (nome + funcao). Extraia de `docs/`: acordos do squad, processos, links uteis. Liste os clientes filhos (so os nomes das pastas).

Gere o `CLAUDE.md` e o `AGENTS.md` (mesmo conteudo) com:

```markdown
# Squad [Nome]

## Membros
- [Nome — Funcao]
- ...

## Clientes
- [nome-formatado-da-pasta]
- ...

## Acordos e processos
[Sintese do que esta em docs/. Se vazio, "Nada documentado ainda — adicione em docs/."]

## Notas Importantes
[Qualquer info critica que nao se encaixa acima]
```

**Se for PROJETO/AREA (generico):**

Extraia: nome, objetivo, pessoas, responsabilidades, dados, metricas, processos, workflows, problemas, oportunidades, decisoes, pendencias.

Gere o `CLAUDE.md` e o `AGENTS.md` (mesmo conteudo) com:

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

**Se for HUB:**

Gere um unico arquivo, `PANORAMA.local.md`, na raiz. A extensao `.local.md` ja e coberta pelo `.gitignore`, entao o panorama nunca sobe pro repo publico. Isso e obrigatorio: o arquivo cruza dado de cliente da carteira inteira e nao pode virar commit.

Nao gere `CLAUDE.md` nem `AGENTS.md` na raiz. Esses dois descrevem o hub como projeto open-source e sao versionados; sobrescrever com estado de carteira vaza dado de cliente.

O panorama tem quatro blocos, nesta ordem.

**Bloco 1: combinados em aberto**

Junte os `mission-control/combinados.md` de todos os clientes e liste o que esta pendente (`- [ ]`) e em andamento (`- [->]`). Ignore o que esta feito (`- [x]`).

Divida em duas tabelas, porque na pratica a maioria dos combinados da carteira nao tem prazo e uma ordenacao por data joga quase tudo no mesmo balde.

Primeiro os que tem prazo, mais vencido no topo:

```markdown
| Cliente | Combinado | Dono | Prazo | Situacao |
|---|---|---|---|---|
| aviv | Enviar novo criativo de stories | Natalia | 2026-07-28 | Vencido ha 3 dias |
| dr-energia | Revisar copy da LP | Luiz | 2026-08-05 | No prazo |
```

Situacao sai da comparacao com a data de hoje: `Vencido ha N dias`, `Vence hoje` ou `No prazo`.

Depois os sem prazo, agrupados por cliente e com a contagem no titulo, do tipo "aviv (11 em aberto, nenhum com prazo)". Nao esconda esses atras de um resumo: combinado sem prazo e combinado que ninguem vai cobrar, e o volume deles por cliente e em si um sinal. Se um cliente tem mais de 5 combinados sem prazo, diga isso no bloco 2 tambem.

Dono generico (`V4`, `time`) nao e dono. Mantenha como veio, mas conte quantos estao assim e registre no fecho, porque combinado sem pessoa e sem data e o padrao que mais gera cobranca de cliente na call seguinte.

**Bloco 2: sinais de atencao**

Um cliente entra aqui quando bate pelo menos um criterio. Use estes limiares, nao invente outros:

| Sinal | Criterio |
|---|---|
| Sem contato | Arquivo mais recente em `calls/` tem mais de 30 dias |
| Nunca teve check-in | `checkins/` vazio ou inexistente |
| Mission Control incompleto | Menos de 5 arquivos em `mission-control/` |
| KB no template | `CLAUDE.md` com menos de 40 linhas |
| Combinado vencido | Pelo menos um pendente com prazo passado |
| Combinado sem prazo acumulando | Mais de 5 pendentes sem prazo definido |
| Sem material | `calls/` e `campanhas/` os dois vazios |

Escreva um bloco por cliente afetado, com os sinais que ele disparou e a acao que resolve. Cliente que nao disparou nada nao aparece: a lista serve para separar o que precisa de atencao do que nao precisa, e listar todo mundo destroi isso.

**Bloco 3: apostas vivas da carteira**

Junte as `mission-control/apostas-vivas.md` de todos os clientes numa tabela so:

```markdown
| Cliente | Aposta | Como mata | Prazo | Situacao |
|---|---|---|---|---|
```

Situacao segue a mesma regra de data do bloco 1. Aposta cujo prazo de verificacao ja passou e o achado mais importante do bloco, porque significa que ninguem olhou o sinal que ia matar ou confirmar a tese. Deixe essas no topo.

Preserve as marcacoes `[INFERIDO - confirmar com account]` que vierem dos arquivos de origem. Elas dizem o que e evidencia e o que e chute.

**Bloco 4: estado do hub**

Coisas do repositorio, nao dos clientes:

- Quantidade de skills instaladas e se os dois espelhos batem (`.claude/skills/` e `.agents/skills/`).
- O que esta sem commit, a partir do `git status --short`. Skill nova sem commit e o caso mais comum e vale dizer ha quanto tempo, usando a data de modificacao do arquivo.
- Squads e membros.
- Clientes sem squad, se houver. Nao deveria haver: o padrao obrigatorio e `squads/{squad}/clientes/{cliente}/`.

**Fecho do arquivo**

Termine com as tres a cinco coisas que voce faria primeiro, na ordem, cada uma com a razao em uma linha. Priorize combinado vencido e aposta com prazo estourado acima de tarefa de estrutura: cliente esperando resposta custa mais caro que KB incompleta.

### Passo 5 — Apresentar ao usuario

Mostre um resumo do que encontrou e os arquivos gerados. Pergunte:
- "Tem algo que eu errei ou que falta?"
- "Quer adicionar alguma informacao que nao estava nos arquivos?"

Ajuste conforme o feedback.

### Passo 6 — Confirmar

Salve e diga:
> "Pronto. Agora toda vez que voce trabalhar nessa pasta, a IA vai ler esse contexto automaticamente. Se os dados mudarem, rode `/contexto` de novo pra atualizar."

No caso do HUB a mensagem e outra, porque o arquivo nao entra em contexto sozinho:
> "Panorama salvo em `PANORAMA.local.md`. Ele e uma fotografia, nao um arquivo vivo: rode `/contexto` na raiz de novo quando quiser atualizar. Fica fora do git por causa da extensao `.local.md`."

## Regras

- NAO invente informacoes. Se nao encontrou algo, deixe como "[nao disponivel]".
- Em `mission-control/`, diferencie evidencia direta de inferencia com `[INFERIDO]` ou `[A CONFIRMAR]`.
- Se a KB estiver vazia ou quase vazia, avise e sugira quais dados adicionar.
- Priorize fatos sobre interpretacoes.
- Mantenha os arquivos concisos — maximo 150 linhas.
- Em pasta de squad, NUNCA leia o conteudo de pastas de clientes filhos. Cada cliente tem seu proprio CLAUDE.md.

### Regras do panorama (HUB)

- O panorama sai sempre em `PANORAMA.local.md`, nunca no `CLAUDE.md` ou `AGENTS.md` da raiz. Os dois sao versionados e vao pro repo publico da V4.
- Nao invente prazo, dono nem data. O que estiver vago no arquivo de origem continua vago no panorama, com `[A CONFIRMAR]`.
- Cliente que nao disparou nenhum sinal de atencao fica fora do bloco 2.
- Nao leia transcript de call para montar panorama. Se um cliente parecer merecer analise profunda, diga isso no fecho e sugira rodar `/contexto` na pasta dele.
- Limite de 200 linhas. Panorama que nao cabe numa leitura nao e panorama.
- Se um cliente nao tiver `mission-control/`, registre isso como sinal de atencao e siga. Nao pare o processo nem gere o Mission Control dele no meio do caminho.
