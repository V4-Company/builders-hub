---
name: account-cro-analise
description: Roda diagnostico de CRO (Conversion Rate Optimization) de landing page ou site puxando dados automaticos do Microsoft Clarity (rage click, dead click, quick back, excessive scroll, erros de script) e organizando o achado em hipoteses de teste priorizadas. Use sempre que o usuario pedir "analise de CRO", "por que a LP nao converte", "diagnostico de conversao", "o que ta travando no site/pagina", "otimizar taxa de conversao", mencionar Microsoft Clarity, rage click, dead click, ou quiser saber onde o usuario esta desistindo/travando numa pagina — mesmo sem falar "CRO" explicitamente.
area: account
author: beatrizandrade-lgtm
version: 1.1.0
---

# /account-cro-analise

Diagnostico de CRO acionavel: puxa sinais de fricção reais do Microsoft Clarity, cruza com o contexto de negocio do cliente e devolve hipoteses de teste priorizadas — nao uma lista de achismos sobre a pagina.

## Quando usar

Dispara quando o usuario:
- Pede analise/diagnostico de CRO, taxa de conversao, ou "por que a LP nao converte"
- Menciona Microsoft Clarity, rage click, dead click, quick back, heatmap de comportamento
- Quer saber onde o usuario final trava, abandona ou se frustra numa pagina
- Pede hipoteses de teste A/B pra uma landing page ou site

Nao usa pra: analise de trafego pago isolada (isso e `v4mos-dados-meta-ads`), benchmark de concorrente (isso e `copy-benchmarking-estrategico`), copy de anuncio (`copy-social-media`).

## Limitacao importante — leia antes de prometer algo ao usuario

A API do Clarity (Data Export API) **so devolve metricas agregadas dos ultimos 1 a 3 dias** — nao da pra puxar historico maior nem pra exportar o heatmap visual ou a gravacao de sessao em si. Isso significa:

- Esta skill e forte pra **sinais quantitativos de friccao** (onde o usuario clica sem efeito, onde volta rapido, onde rola demais, onde da erro)
- Nao substitui olhar o heatmap/replay no dashboard do Clarity com os proprios olhos — se o usuario quiser esse nivel de detalhe visual, oriente a abrir o dashboard diretamente
- Se o cliente pedir tendencia de mais de 3 dias, **nao existe forma de puxar retroativo** — a API rejeita `numOfDays` acima de 3 com HTTP 400, e nao ha endpoint alternativo pra historico. So da pra construir serie temporal daqui pra frente, acumulando snapshots. Deixe isso claro ao usuario antes de ele esperar um "historico completo" que nao existe.
- Pra acumular historico manualmente (sem automacao — o usuario roda a skill de novo quando quiser um snapshot novo): use `--history-file squads/<squad>/clientes/<cliente>/docs/clarity-historico.jsonl`. Cada chamada acrescenta uma linha JSONL com `fetched_at` + `days` + `data`, sem sobrescrever as anteriores. Assim, ao longo de semanas, da pra reconstruir tendencia mesmo a API so cobrindo 3 dias por vez.

## Passo 1 — Identificar o cliente e localizar a KB

1. Se o usuario ja nomeou o cliente, va direto. Se nao, pergunte ou detecte pelo cwd (`squads/<squad>/clientes/<cliente>/`).
2. Se a pasta do cliente nao existir, ofereça `/novo-cliente` antes de continuar.
3. Leia o `CLAUDE.md` do cliente (se existir) pra pegar contexto de negocio, publico-alvo e metas — isso e o que transforma "rage click na secao X" em "hipotese relevante pro objetivo do cliente". Se nao tiver CLAUDE.md, continue sem ele, mas avise que o diagnostico vai ser mais generico.

## Passo 2 — Garantir o token do Clarity

O token fica em `squads/<squad>/clientes/<cliente>/.env`, chave `CLARITY_API_TOKEN`.

1. Confira se ja existe:
   ```bash
   grep -E "^CLARITY_API_TOKEN=." "squads/<squad>/clientes/<cliente>/.env" 2>/dev/null
   ```
2. Se estiver vazio ou o arquivo nao tiver essa chave, peca ao usuario:
   > "Preciso do token de API do Clarity desse cliente. Gera em: **clarity.microsoft.com** → abre o projeto → **Settings** → **Data Export** → **Generate new API token** (escopo `Data.Export`). O valor so aparece uma vez, entao copia na hora."
3. Assim que receber, grave no `.env` do cliente via Edit tool, preservando o resto do arquivo. Nunca imprima o token de volta no chat depois de salvo — trate como credencial.
4. Token e por projeto Clarity (1 por cliente), diferente do V4mos onde client_id/secret sao reusaveis entre clientes.

## Passo 3 — Puxar os dados

Use o script `fetch_clarity.py` que vem junto com esta skill (nao reescreva a chamada de API na mao — ele ja trata erro de token invalido e limite de dias).

O caminho e relativo a **raiz do repositorio**, nao a pasta da skill:

```bash
python .claude/skills/account-cro-analise/scripts/fetch_clarity.py \
  --env-file "squads/<squad>/clientes/<cliente>/.env" \
  --days 3
```

Se estiver rodando no Anti-Gravity, troque `.claude/` por `.agents/` — o conteudo e identico.

Isso devolve uma lista de metricas no formato:
```json
[{"metricName": "DeadClickCount", "information": [{"sessionsCount": 35, "sessionsWithMetricPercentage": 8.57, ...}]}, ...]
```

Metricas de friccao confirmadas e uteis pro diagnostico (a API pode devolver outras dependendo do que o projeto rastreia — trate a lista de forma dinamica, nao trave em nomes fixos):

- **RageClickCount** — cliques repetidos e frustrados no mesmo elemento → geralmente CTA/botao que parece clicavel mas nao responde, ou responde devagar
- **DeadClickCount** — clique em algo que nao faz nada → elemento com aparencia de interativo (texto sublinhado, icone, "falso botao") que na verdade e estatico
- **QuickbackClick** — usuario entra numa pagina e volta rapido → conteudo nao entregou o que o anuncio/link prometeu (falta de congruencia mensagem→pagina)
- **ExcessiveScroll** — rolagem excessiva/erratica → usuario procurando algo que nao acha facilmente (hierarquia visual ruim ou informacao enterrada)
- **ScriptErrorCount** — erro de JS na sessao → pode estar quebrando formulario, tracking ou elemento interativo sem o usuario nem saber reportar
- **ErrorClickCount** — clique que dispara erro de JS → diferente do dead click (que nao faz nada) e do script error (que pode acontecer sem interacao): aqui o usuario **agiu e a acao quebrou**. Costuma ser o sinal mais grave dos tres, porque atinge quem estava tentando converter

Se `sessionsWithMetricPercentage` de qualquer metrica de friccao vier alto (use bom senso: acima de ~15-20% ja e um sinal forte pra poucos dias de dado), isso e prioridade de investigacao.

**Atencao ao denominador:** o `sessionsCount` que vem dentro de cada metrica de friccao e o total de sessoes **incluindo bots**, e o `sessionsWithMetricPercentage` ja vem calculado sobre essa base inflada. Se metade do trafego for bot, todo percentual de friccao chega ate voce diluido pela metade. Veja o proximo bloco antes de citar qualquer numero.

Alem das metricas de friccao, a API tambem devolve metricas de contexto — use pra enriquecer o LIFT, nao ignore:
- **Traffic** — repare em `totalBotSessionCount` vs `totalSessionCount`. **Sempre desconte bots antes de calcular qualquer percentual pro diagnostico ou pro cliente.** Bot nao tem rage click nem desiste de formulario: a friccao toda aconteceu na fatia humana, entao o percentual real e quase sempre **maior** do que o que a API devolve. Recalcule assim antes de citar qualquer numero:

  ```
  humanas        = totalSessionCount - totalBotSessionCount
  sessoes_afetadas = round(sessionsWithMetricPercentage / 100 * sessionsCount)
  pct_real       = sessoes_afetadas / humanas * 100
  ```

  Exemplo: 110 sessoes, 55 bots, `ScriptErrorCount` a 50,91%. A leitura ingenua e "metade das sessoes". A real e 56 sessoes afetadas sobre 55 humanas — ou seja, praticamente **toda** sessao humana bateu em erro de JS. O diagnostico muda de "vale investigar" pra "para tudo e conserta isso primeiro". Diga sempre qual base voce usou.

- **ReferrerUrl / PopularPages** — de onde vem o trafego e pra onde ele vai; usa pra avaliar Relevancia (o que trouxe o clique bate com a pagina que ele caiu?)
- **Browser / Device / OS** — se a friccao concentra num device/browser especifico, o problema pode ser tecnico (bug de renderizacao) e nao de copy/design
- **Country** — trafego concentrado fora do mercado do cliente costuma ser bot ou midia mal segmentada; cruze com `totalBotSessionCount` antes de tratar como publico real
- **ScrollDepth / EngagementTime** — apoiam o diagnostico de Distracao e Clareza. Em `EngagementTime`, olhe a **razao `activeTime / totalTime`**, nao o tempo absoluto: se o usuario ficou 175s na pagina mas so 44s ativos (~25%), ele nao estava lendo — estava parado, perdido ou em outra aba. Tempo alto com atividade baixa e sinal de Clareza ruim, nao de engajamento

### Schema real do retorno — confira a chave antes de parsear

Cada metrica traz `information` com chaves **diferentes**. Errar a chave devolve vazio em silencio, sem erro:

| Metrica | Chaves dentro de `information` |
|---|---|
| Friccao (todas) | `sessionsCount` · `sessionsWithMetricPercentage` · `pagesViews` · `subTotal` |
| `Traffic` | `totalSessionCount` · `totalBotSessionCount` · `distinctUserCount` · `pagesPerSessionPercentage` |
| `PopularPages` | `url` · `visitsCount` |
| `PageTitle` / `ReferrerUrl` / `Browser` / `Device` / `OS` / `Country` | `name` · `sessionsCount` |
| `ScrollDepth` | `averageScrollDepth` |
| `EngagementTime` | `totalTime` · `activeTime` |

Repare que `PopularPages` e a excecao: usa `url`/`visitsCount` enquanto as vizinhas usam `name`/`sessionsCount`.

**Cuidado com `PageTitle`:** o export do Clarity corrompe acentuacao em PT-BR — o titulo chega na chave `name` com `�` no lugar de ç, ã, é (ex: `"A solu��o em containers"`). Ja foi confirmado em projeto real, nao e caso isolado. E problema do proprio export da Microsoft, sem conserto do nosso lado. **Nunca cole o `PageTitle` bruto num relatorio pro cliente** — use a URL (`PopularPages.url`) ou peca a URL real da pagina pra descrever a secao.

## Passo 4 — Cruzar com outras fontes (opcional, nao trava se faltar)

- Se o cliente ja usa `v4mos-dados-meta-ads` e tem campanha ativa apontando pra essa mesma pagina, puxe CTR/CPA do periodo — ajuda a distinguir "problema de trafego" (gente errada chegando) de "problema de pagina" (gente certa, mas trava)
- Se tiver Mission Control do cliente (`mission-control/`), confira persona e objetivo da pagina pra calibrar o que conta como "friccao relevante" vs "ruido"

## Passo 5 — Aplicar o framework de diagnostico

Estruture o achado usando o **LIFT Model**, seção por seção da pagina (ideal: peça a URL ou print da LP se ainda nao tiver sido descrita na conversa):

| Dimensao | Pergunta que orienta o diagnostico |
|---|---|
| Value Proposition | A proposta de valor fica clara na secao que concentra a friccao? |
| Relevancia | O que trouxe trafego pra essa secao bate com o que ela entrega? |
| Clareza | O elemento que gerou rage/dead click é ambiguo sobre o que faz? |
| Urgencia | Falta gatilho de acao na secao onde o usuario desiste (quick back)? |
| Ansiedade/Atrito | O que gera desconfianca ou esforco extra nessa secao? |
| Distracao | Tem elemento competindo por atencao que desvia do objetivo da secao? |

Para cada sinal de friccao do Clarity, associe pelo menos uma dimensao do LIFT com uma explicacao causal — nunca so reporte o numero cru ("8,57% das sessoes tiveram dead click" nao e diagnostico, e dado; o diagnostico e "o dead click provavelmente esta no [elemento X], que parece clicavel mas e so texto — isso é friccao de Clareza").

## Passo 6 — Priorizar hipoteses com PXL

Transforme cada diagnostico em **hipotese testavel** (formato: "Se eu mudar [X], espero [efeito] porque [racional apoiado no dado]") e priorize com PXL — pontue 0/1/2 em cada criterio, some, ordene do maior pro menor:

| Hipotese | Potencial (o sinal e forte/generalizado?) | Importancia (secao critica pro funil?) | Facilidade (da pra testar rapido?) | Total |
|---|---|---|---|---|

Nunca entregue "mude o botao pra verde" como hipotese — isso nao e testavel de forma acionavel. Entregue algo como: "Trocar o CTA de 'Enviar' pra 'Quero meu orcamento agora' na secao do formulario, porque X% das sessoes tiveram dead click ali e o texto atual nao comunica o que acontece ao clicar (friccao de Clareza)."

## Passo 7 — Entregar o resultado

Formato padrao no chat:
1. Resumo executivo (2-3 frases: qual e o principal ponto de friccao e por que importa pro objetivo do cliente)
2. Diagnostico por secao (LIFT)
3. Tabela de hipoteses priorizadas (PXL)
4. Limitacoes dos dados usados (janela de dias, ausencia de heatmap visual)

Se o usuario pedir versao HTML pra apresentar ao cliente, **nao crie um layout do zero** — invoque `/geral-relatorio-v4` passando esse conteudo, pra manter o Design System V4 consistente com outros relatorios do time.

## Exemplo de uso

**Input do usuario:** "roda uma analise de CRO na LP do cliente Y, a gente ta gastando bem em trafego mas a conversao ta baixa"

**Comportamento esperado:**
1. Confirma qual cliente/squad, confere `.env` pra `CLARITY_API_TOKEN`
2. Roda `python .claude/skills/account-cro-analise/scripts/fetch_clarity.py --days 3` a partir da raiz do repo
3. Le `CLAUDE.md` do cliente pra pegar objetivo/persona da LP
4. Opcionalmente cruza com `v4mos-dados-meta-ads` pra ver se o trafego que chega e o publico certo
5. Devolve diagnostico LIFT + tabela PXL com 3-6 hipoteses priorizadas, avisando que os dados cobrem so os ultimos dias

**Output:** diagnostico estruturado no chat (secoes acima), oferecendo gerar HTML via `/geral-relatorio-v4` se o usuario quiser apresentar pro cliente.
