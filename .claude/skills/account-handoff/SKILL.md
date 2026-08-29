---
name: account-handoff
description: 'Primeira skill que o account roda quando recebe um cliente novo de vendas. Le form de kickoff + transcript da reuniao de vendas (+ proposta comercial opcional) e gera a primeira versao da KB do cliente: resumo de vendas, form estruturado, perguntas pro kickoff, promessas e riscos, CLAUDE.md/AGENTS.md preliminares, Mission Control preliminar e um deck HTML interativo com modo Account/Cliente pra conduzir a reuniao de kickoff. Use quando o usuario rodar /account-handoff, disser que recebeu um cliente novo de vendas, ou que precisa transformar form+reuniao de vendas em KB pra preparar a primeira reuniao da operacao.'
area: account
author: guilhermelippert
version: 1.0.0
---

# /account-handoff

Transforme **form de kickoff + transcript da reuniao de vendas** na **primeira versao da Knowledge Base** e do **Mission Control** de um cliente que acabou de sair de vendas. O entregavel estrela e um **deck HTML interativo** com **dois modos**:
- **Modo Account** (default) — account abre antes da reuniao, ve toda a analise interna (chips de factibilidade + alertas internos com red flags).
- **Modo Cliente** — account aperta antes de compartilhar tela. Esconde analise interna. Cliente so ve linguagem diplomatica e neutra.

**Diferente de `/contexto`** (continua, atualiza KB ao longo da operacao), `/account-handoff` e a **primeira** skill que roda na transicao vendas → operacao. **Diferente de `/account-pesquisa-profunda-cliente`** (pesquisa externa via Deep Research), `/account-handoff` consome **material interno** (form, reuniao, proposta).

## Posicionamento no fluxo

1. `/novo-cliente` — cria a pasta (pre-requisito).
2. **`/account-handoff`** — esta skill (consome inputs de vendas).
3. `/account-pesquisa-profunda-cliente` — sugerida no fim (pesquisa externa).
4. **Reuniao de kickoff** com o cliente (account abre o deck HTML em modo Cliente, marca confirmado/ajustar/lacuna ao vivo).
5. `/contexto` — consolida tudo (incluindo o JSON exportado do deck) num CLAUDE.md/AGENTS.md final e atualiza `mission-control/`.

## Principios

- Nao inventar fatos. Separar **EVIDENCIA** (do form/transcript/proposta) vs **INFERENCIA** vs **LACUNA**.
- Material interno tem prioridade absoluta sobre suposicao.
- **Roda com o que tem.** Lacuna nao bloqueia — vira pergunta no `03-perguntas-kickoff.md` e item `❓` no deck.
- Nao criar pasta de cliente aqui. Cliente inexistente → manda pra `/novo-cliente` e para.
- Nao transcrever audio. Se vier so link de gravacao, oriente o usuario a rodar Read.ai/Fireflies primeiro.
- **Linguagem cliente-facing por padrao.** A tela do deck vai ser compartilhada com o cliente — analise critica fica em `alertaInterno` (so visivel em Modo Account) e nos markdowns internos.
- **Modo Cliente nao e redacao.** Ele apenas esconde elementos na tela; o HTML e o JSON exportado continuam contendo `alertaInterno`. Nunca envie esses arquivos ao cliente. Se precisar enviar uma copia, gere outro arquivo removendo `alertaInterno` e `factibilidade` do payload e valide a copia antes.
- Portugues brasileiro em tudo.

## Passo 1 — Identificar e validar a pasta do cliente

1. Pergunte qual o cliente (ou detecte da pasta corrente, se ja estiver dentro de `squads/{squad}/clientes/{cliente}/`).
2. Se a pasta nao existir, **pare** e mande:
   > "Cliente ainda nao existe. Roda `/novo-cliente` primeiro pra criar a pasta dentro do squad. Depois volta aqui."
3. Trabalhe em `squads/{squad}/clientes/{cliente}/docs/handoff/`. Crie `docs/handoff/inputs/` se nao existir.

## Passo 2 — Coletar inputs

Verifique o que ja tem em `docs/handoff/inputs/`:

```bash
ls "squads/{squad}/clientes/{cliente}/docs/handoff/inputs/" 2>/dev/null
```

**Se a pasta tem arquivos**, liste o que encontrou e pergunte se pode prosseguir.

**Se a pasta esta vazia**, peca (uma vez, em bloco):

> Joga em `docs/handoff/inputs/`:
> 1. **Form de kickoff** em markdown (exportado do Google Forms ou similar). Esperado.
> 2. **Transcript da reuniao de vendas** em markdown (Anotacoes do Gemini, Read.ai, Otter, Fireflies, etc). Esperado.
> 3. **Proposta comercial** (PDF, markdown, qualquer formato). Opcional — se nao tiver, sigo sem.
>
> Se voce so tem link de gravacao (Drive/Meet) sem transcript, roda no Read.ai ou Fireflies antes — eu nao transcrevo audio.
>
> Aperta enter quando os arquivos estiverem la.

**Filosofia:** se vier so um dos dois (form OU transcript), prossiga mesmo assim. Cada lacuna vira pergunta a mais no kickoff. Nao trave.

## Passo 3 — Ler todos os inputs por completo

Leia **todos** os arquivos em `docs/handoff/inputs/` integralmente. Nao pule. Para cada arquivo, identifique:

- O que e (form? transcript? proposta?)
- Quem disse o que (no transcript: vendedor V4 vs cliente)
- Datas, valores, prazos, KPIs mencionados
- Links uteis (Drive de vendas, gravacao, deck da proposta, site, redes do cliente)
- **Inconsistencias** entre fontes (form diz X, reuniao diz Y) — viram alertas internos

## Passo 4 — Gerar os 4 markdowns em `docs/handoff/`

> Em todos os markdowns: marque cada afirmacao como **EVIDENCIA** (cita fonte: form/transcript/proposta + trecho), **INFERENCIA** (deduzido do conjunto), ou **LACUNA** (nao tem).

### `00-resumo-vendas.md` — Resumo executivo

Estrutura: o que foi vendido (servico, escopo, prazo, valor, inicio), contatos do cliente, expectativas em ordem de prioridade, time V4 envolvido, dados da reuniao de vendas.

### `02-form-kickoff.md` — Form estruturado

Reorganize o form bruto em secoes claras: identidade, oferta, mercado, digital, objetivo de marketing, KPIs, restricoes, preferencias. Mantenha respostas literais entre aspas quando o cliente respondeu algo importante. Marque campos vazios como `LACUNA`.

(Pulo dos numeros 01 e 05: reservados pra possivel expansao.)

### `03-perguntas-kickoff.md` — Perguntas pro kickoff

A lista que o account vai usar pra **conduzir** a primeira reuniao com o cliente. Tres categorias:

```markdown
# Perguntas pro kickoff

## 1. Confirmar (validar com o cliente o que vendas anotou)
- [ ] Confirmar que escopo combinado foi [X].
- [ ] Confirmar contato principal e [Nome].

## 2. Aprofundar (informacao parcial nos inputs)
- [ ] Qual o ticket medio real do produto X? (form diz "varia").

## 3. Cobrir lacunas (dados que nao apareceram em lugar nenhum)
- [ ] Qual o budget mensal de midia disponivel? (LACUNA total).
- [ ] Tem conta de Meta/Google Ads ja criada? Acesso?
- [ ] Quem aprova criativo final?
```

### `04-promessas-e-riscos.md` — Promessas de vendas e analise de risco

**Esta e a parte mais importante.** Liste cada promessa que vendas fez (escopo, prazo, KPI, entrega) e classifique:

```markdown
# Promessas de vendas e riscos

## Promessas explicitas (o que cliente espera)
| # | Promessa | Fonte | Factibilidade | Justificativa |
|---|----------|-------|---------------|---------------|
| 1 | "Vamos entregar 50 leads/mes em 30 dias" | Reuniao 12:34 | 🟡 Otimista | Setor X tipicamente faz CPL R$80; com R$3k/mes da 37 leads, nao 50 |
| 2 | LP no ar em 2 semanas | Form | 🟢 Factivel | Escopo simples, sem integracao |
| 3 | ROAS 4 garantido | Reuniao 28:10 | 🔴 Perigoso | Setor faz ROAS 2-3 medio; cliente nunca rodou antes |

## KPIs prometidos
- [Lista do que vendas falou que ia entregar]

## Red flags
- [Coisas que vao virar problema]

## Compromissos da V4 (alem do escopo)
- [Coisas que vendas falou que faria fora do contrato]
```

> **Padroes de factibilidade:** 🟢 Factivel · 🟡 Otimista (precisa validar) · 🔴 Perigoso (alta chance de bola fora).

## Passo 5 — Popular `CLAUDE.md` e `AGENTS.md` preliminares

Na **raiz** da pasta do cliente, escreva `CLAUDE.md` e `AGENTS.md` com o mesmo conteudo preliminar. Marque claramente que e preliminar:

```markdown
# [Nome do Cliente] (KB preliminar pos-handoff)

> ⚠️ **Esta KB e preliminar.** Foi gerada por `/account-handoff` antes do kickoff com o cliente. Apos a primeira reuniao, rode `/contexto` pra consolidar (vai puxar o `kickoff-resultado.json` exportado do deck).

## Recursos
Veja `links.md` na raiz pra todos os links uteis.

## Negocio (do form + reuniao de vendas)
- **Segmento:** [...]
- **Produto/Servico:** [...]
- **Publico-alvo:** [...]
- **Diferenciais:** [...]

## Operacao prevista
- **Servico vendido:** [...]
- **Investimento:** [...]
- **KPIs combinados:** [veja `04-promessas-e-riscos.md` pra detalhe e factibilidade]

## Relacionamento
- **Contatos do cliente:** [...]
- **Time V4:** [...]
- **Combinados:** [veja `00-resumo-vendas.md`]

## Pendencias pro kickoff
Veja `03-perguntas-kickoff.md` — sao [N] perguntas pra fazer ao cliente na primeira reuniao.

## Riscos identificados no handoff
[Lista breve dos red flags do `04-promessas-e-riscos.md`]

## Quando trabalhar com este cliente
- Le `links.md` antes de qualquer coisa.
- Antes do kickoff, rode tambem `/account-pesquisa-profunda-cliente` pra ter pesquisa externa.
- Apos o kickoff com o cliente, rode `/contexto` pra atualizar esta KB.
```

## Passo 6 — Criar `mission-control/` preliminar

Crie `mission-control/` na raiz do cliente com os arquivos abaixo. E a primeira versao do estado vivo da conta, antes do kickoff.

```text
mission-control/
|-- okr-quarter.md
|-- apostas-vivas.md
|-- combinados.md
|-- personas-call.md
|-- historico-checkins.md
`-- historico-preparacoes.md
```

### `okr-quarter.md`

Extraia dos inputs qualquer objetivo/KPI vendido ou esperado. Se ainda nao houver OKR real, marque como preliminar:

```markdown
# OKRs do Quarter

> Status: preliminar pos-handoff. Confirmar no kickoff e consolidar via `/contexto`.

## Objetivo
[EVIDENCIA/INFERENCIA/LACUNA]

## Key Results
- [ ] KR 1 - [fonte ou LACUNA]

## A confirmar no kickoff
- [...]
```

### `apostas-vivas.md`

Crie 1 a 3 apostas iniciais, sempre marcadas como preliminares. Se nao houver informacao suficiente, deixe a tabela vazia com lacunas claras.

```markdown
| Aposta (o que cremos) | Por que apostamos | Como mata (sinal + prazo) | Plano B se morrer |
|---|---|---|---|
| [INFERIDO - confirmar no kickoff] ... | ... | [A CONFIRMAR] | [A CONFIRMAR] |
```

### `combinados.md`

Registre promessas de vendas e pendencias do kickoff como combinados preliminares:

```markdown
# Combinados

## Pendentes para kickoff
- [ ] Account confirmar {ponto} no kickoff [fonte]

## Feitos
- [x] Handoff de vendas processado em {data}
```

### `personas-call.md`

Crie perfis iniciais dos stakeholders citados na venda. Use arquétipos com baixa confianca se ainda nao houver check-in:

```markdown
# Personas das Calls

> Preliminar pos-handoff. Refinar com `account-checkin-review` apos calls reais.

## {Nome} - {papel}
- **Arquétipo inicial:** [decisor agressivo / operacional cetico / estrategista / passivo] [INFERIDO]
- **Voz:** [A CONFIRMAR]
- **Gatilhos:** [...]
```

### `historico-checkins.md`

Crie vazio, deixando claro que so recebe calls reais:

```markdown
# Histórico de Check-ins e Calls

> Apenas calls reais/transcripts. Preparacoes ficam em `historico-preparacoes.md`.
```

### `historico-preparacoes.md`

Registre a preparacao inicial:

```markdown
# Histórico de Preparações de Check-in

## {YYYY-MM-DD} - handoff inicial
**Resumo:** Mission Control preliminar criado a partir de vendas/form/proposta.
**Pontos fracos a treinar:** [lacunas principais]
```

## Passo 7 — Atualizar `links.md`

Abra `links.md` na raiz do cliente. Adicione na secao "Outros" qualquer link que apareceu nos inputs e ainda nao esta listado:

- Gravacao da reuniao de vendas (Meet/Drive)
- Pasta de vendas no Drive
- Deck da proposta comercial
- Site/redes do cliente
- LinkedIn do contato principal
- Qualquer ferramenta que cliente mencionou usar

## Passo 8 — Gerar `docs/handoff/kickoff-deck.html`

**Este e o entregavel estrela.** Single-page HTML interativo, sem CDN, com auto-save em localStorage e toggle Modo Account/Cliente.

### Como gerar

1. Leia o template `assets/template-kickoff.html` (espelhado nesta skill).
2. Substitua o conteudo do `<script id="dados-handoff" type="application/json">...</script>` pelo JSON real do cliente.
3. Salve o resultado em `docs/handoff/kickoff-deck.html`.

### Schema do JSON

```json
{
  "capa": {
    "cliente": "Nome do Cliente",
    "squad": "squad-x",
    "account": "Nome do Account",
    "dataGeracao": "2026-05-01",
    "vendedor": "Nome do Vendedor"
  },
  "resumoVendas":   [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ],
  "empresa":        [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ],
  "promessas":      [ { "titulo": "...", "conteudo": "...", "factibilidade": "factivel|otimista|perigoso", "alertaInterno": "..." } ],
  "acessos":        [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ],
  "combinados":     [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ],
  "perguntas":      [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ],
  "proximosPassos": [ { "titulo": "...", "conteudo": "...", "alertaInterno": "..." } ]
}
```

Cada bloco tem ate 4 campos:

- **`titulo`** (obrigatorio) — frase curta, **cliente-facing** (vai aparecer na tela compartilhada).
- **`conteudo`** (obrigatorio) — explicacao do bloco, **cliente-facing**. Suporta **negrito** com `**texto**`.
- **`factibilidade`** (so na secao `promessas`, opcional) — `"factivel"`, `"otimista"` ou `"perigoso"`. Vira chip colorido **so visivel em Modo Account**.
- **`alertaInterno`** (opcional, **so visivel em Modo Account**) — analise critica, red flags, dados sensiveis. Aqui mora "RECONCILIAR numeros", "INCONSISTENCIA grave", "verba insuficiente — preparar cliente". O account ve antes da reuniao pra saber o que cobrar com diplomacia.

### Regras de linguagem

**Em `titulo` e `conteudo` (visiveis ao cliente):**

- Primeira pessoa do plural: "vamos alinhar", "vamos confirmar", "nossa estrategia".
- Tom diplomatico: "vamos confirmar volume mensal" ❌ "RECONCILIAR numeros".
- Sem jargao interno V4: nada de "lacuna", "perigoso", "promessa de vendas".
- Sem expor erros do cliente: nao escreva "form contradiz reuniao" — vira pergunta neutra.
- Sem expor falhas internas: nao escreva "vendedor prometeu X mas escopo nao tem".

**Em `alertaInterno` (so account ve):**

- Pode ser direto e tecnico: "🔴 INCONSISTENCIA grave", "Verba insuficiente pro setor", "Forcar definicao agora".
- Inclui **a razao** da preocupacao + **o que o account deve fazer** ao chegar nesse bloco na reuniao.

### Exemplo de bom contraste

```json
{
  "titulo": "Volume e faturamento",
  "conteudo": "Pra dimensionar bem nossa estrategia, queria entender melhor: dos numeros que conversamos, qual e a fotografia mais real da operacao hoje?",
  "alertaInterno": "🔴 O volume declarado e a receita informada nao fecham. Pergunta diplomatica pra reconciliar sem expor o erro de preenchimento."
}
```

## Passo 9 — Resumo final pro usuario

Mostre:

```
Handoff pronto. O que foi gerado em squads/{squad}/clientes/{cliente}/:

docs/handoff/
├── inputs/                       (seus arquivos originais)
├── 00-resumo-vendas.md           (X paragrafos)
├── 02-form-kickoff.md            (N campos, X lacunas)
├── 03-perguntas-kickoff.md       (N perguntas: A confirmar, B aprofundar, C cobrir lacunas)
├── 04-promessas-e-riscos.md      (N promessas: X factivel, Y otimista, Z perigoso)
└── kickoff-deck.html             ← ESTE e o que voce abre na reuniao

CLAUDE.md / AGENTS.md (raiz) — preliminares, serao atualizados pos-kickoff via /contexto
mission-control/               — OKRs, apostas, combinados, personas e historicos preliminares
links.md (raiz)                — atualizado com [N] novos links

⚠️ Lacunas criticas que precisam virar pergunta no kickoff:
- [...]
- [...]

📊 Promessas perigosas pra atencao redobrada:
- [...]

→ Pra abrir o deck antes da reuniao:
  open "squads/{squad}/clientes/{cliente}/docs/handoff/kickoff-deck.html"

  ⚠️ Antes de compartilhar tela com o cliente, troque pra "Modo Cliente" no botao do topo.
  Em Modo Account voce ve a analise interna; em Modo Cliente ela some — fica so a linguagem
  diplomatica que o cliente pode ler.
  Nao envie o arquivo HTML nem o JSON exportado ao cliente: ambos preservam a analise interna.

→ Antes do kickoff, considera rodar /account-pesquisa-profunda-cliente
  pra chegar ainda mais preparado (pesquisa externa de mercado/concorrencia/consumidor).
  Os dados internos que essa skill pede ja estao consolidados em docs/handoff/.

→ Apos o kickoff, rode /contexto pra consolidar a KB final.
```

## Como o deck funciona na reuniao (so pra contextualizar o usuario)

- Account abre o HTML em **Modo Account** (default), revisa todos os blocos vendo a analise interna.
- Antes de compartilhar tela com o cliente, **clica no botao "Modo: Account" no topo** — ele vira "Modo: Cliente". Chips de factibilidade somem. Caixas amarelas de alerta interno somem.
- O toggle e apenas visual. O payload interno continua no arquivo-fonte; **nao envie o HTML nem o JSON exportado ao cliente**.
- Compartilha tela. Conduz a conversa rolando pra baixo.
- Cada bloco tem 3 botoes: ✅ confirmado · ✏️ ajustar · ❓ lacuna.
- Cliques sao salvos automaticamente no localStorage do navegador (chave `handoff-{slug-cliente}`).
- Botao "Ajustar" abre textarea pra anotacao livre.
- No fim da reuniao, account aperta **Exportar JSON** e baixa `kickoff-resultado.json`.
- Esse JSON deve ser salvo em `docs/handoff/`. O `/contexto` (ou skill futura) le ele pra consolidar a KB.

### Atalhos de teclado (no deck)

- `1` · `2` · `3` — marca o bloco em foco como confirmado / ajustar / lacuna.
- `e` — exporta JSON.
- `↓` (na capa) — rola pra primeira secao.

### Estados visuais do bloco

- **Sem acao:** borda transparente, fundo branco.
- **Confirmado:** borda esquerda verde + tint verde no fundo + botao ✅ preenchido.
- **Ajustar:** borda ambar + tint ambar + botao ✏️ preenchido + textarea revelada.
- **Lacuna:** borda vermelha + tint vermelho + botao ❓ preenchido.

## Lacunas e seguranca

- Se um input for muito grande (>50k tokens), corte por secoes relevantes mas avise o usuario.
- Nunca exponha credenciais (CNPJ, senhas, tokens). Se aparecer no input, marque como `[REDIGIDO]` no markdown.
- Se a reuniao mencionar concorrentes V4 ou clientes de outros squads, ignore — nao e pra entrar na KB.
- **Toda analise critica vai em `alertaInterno`, nunca em `conteudo`.** Se voce hesitar entre os dois, vai pro alerta — e mais seguro nao expor pro cliente.
