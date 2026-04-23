---
name: trafego-analise-funil
description: Analisa trafego pago e funil completo de clientes, cruzando Meta Ads, Google Ads, V4mos, GA4, CRM, budget e planilhas. Use quando o usuario pedir analise de trafego, analise de funil, pacing de budget, fechamento semanal/mensal, preparacao de check-in, Sprint Planning, diagnostico de gargalos ou leitura de performance para decidir proximas otimizacoes.
area: trafego
author: marighv4
version: 1.2.0
---

# /trafego-analise-funil

Skill para transformar dados de midia, budget e funil em uma analise acionavel para gestor de trafego. Ela cobre tanto a leitura geral de trafego pago quanto o diagnostico completo do funil, com foco em reduzir trabalho manual de puxar dados, preencher planilhas e preparar check-ins.

## Novidades v1.2

- Comparacao temporal obrigatoria (periodo contra periodo anterior equivalente, media movel 4s, mesmo periodo mes anterior).
- Guard-rails de significancia: volume minimo fixo + banda historica dinamica.
- Arvore de diagnostico obrigatoria antes de qualquer conclusao.
- Modo `--rapido` para check-in ao vivo (pula arvore, mantem guard-rails).
- Output de hipotese testavel nas acoes recomendadas.

## Quando usar

- Quando o usuario quiser ver o overview de trafego ou funil de um cliente.
- Para preparar check-ins quinzenais ou mensais.
- Para gerar resumo de acoes para Sprint Planning.
- Para revisar pacing de budget e decidir se precisa acelerar, segurar ou redistribuir verba.
- Para separar problema de midia, landing page, CRM, comercial, budget ou dados inconsistentes.
- Frases-chave: "analise o funil", "analise o trafego", "veja as travas do cliente X", "como esta o funil", "como esta o pacing", "prepare o check-in".

## Modos de execucao

- **Padrao:** roda tudo, inclusive arvore de diagnostico. Use para fechamento, sprint planning, diagnostico profundo.
- **`--rapido`:** pula arvore de diagnostico, mantem guard-rails e comparacao temporal. Use para check-in ao vivo.
- **`--comparativo=off`:** desliga comparacao temporal quando nao houver dado historico disponivel. Sinaliza isso no output.

## Principios

1. Nunca misture periodos. Declare o periodo analisado no topo.
2. Nunca trate dado manual como dado de API. Sinalize quando MQL, SQL, vendas, faturamento ou ticket vierem do usuario, CRM manual ou cliente.
3. Separe Meta Ads e Google Ads quando os dados permitirem. Se consolidar, explique o que entrou no consolidado.
4. Diferencie metrica de plataforma e metrica de negocio. Plataforma pode otimizar lead ruim; CRM valida qualidade.
5. Mostre confiabilidade dos dados antes de conclusao forte.
6. Se faltar dado critico, gere analise parcial e liste o que falta.
7. Nao recomende aumentar verba se o gargalo estiver em qualificacao, SQL, venda ou dados inconsistentes sem deixar a ressalva clara.
8. **Novo v1.2:** variacao sem contexto historico nao e sinal. Toda conclusao forte precisa passar pelos guard-rails.
9. **Novo v1.2:** acao recomendada vira hipotese testavel (o que muda, resultado esperado, em quanto tempo, medido por qual metrica).

## Entradas aceitas

- Nome do cliente em `clientes/[cliente]/`.
- Arquivos em `clientes/[cliente]/campanhas/`, `docs/` ou `copy/`.
- CSVs exportados de Meta Ads, Google Ads, GA4, CRM ou planilhas.
- JSONs de V4mos ou outputs do script `v4mos-dados-meta-ads`.
- Links ou IDs de Google Sheets, quando o conector estiver disponivel.
- Numeros manuais informados pelo usuario no chat.

## Passo 1 - Identificar cliente e contexto

1. Pergunte o nome do cliente se nao estiver claro.
2. Leia `clientes/[cliente]/CLAUDE.md` se existir. Se nao existir, leia `clientes/[cliente]/README.md` e documentos recentes em `docs/`.
3. Procure:
   - nicho
   - modelo comercial: inside sales, ecommerce, hibrido ou outro
   - SQL definido
   - evento de lead correto
   - fontes de MQL, SQL, vendas e faturamento
   - metas, benchmarks e budget planejado
   - **Novo v1.2:** bandas historicas ja conhecidas (ex: "CPL oscila entre R$40 e R$70 naturalmente")
   - **Novo v1.2:** mudancas estruturais recentes (novo criativo, troca de publico, mudanca de budget, nova LP)
4. Se nao encontrar o evento de lead correto, liste os eventos disponiveis e pergunte qual usar antes de calcular lead LP.
5. Se houver conflito entre contexto antigo e dado novo, diga explicitamente qual fonte esta usando.

## Passo 2 - Coletar e organizar dados

Priorize dados estruturados nesta ordem:

1. V4mos/V4mkt para midia.
2. Exportacoes CSV/JSON de plataformas.
3. Google Sheets do cliente.
4. CRM/API quando disponivel.
5. Dados manuais do usuario ou do cliente.

**Novo v1.2:** sempre que possivel, puxe tambem os **3 periodos de comparacao**:
- periodo atual (P0)
- periodo anterior equivalente (P-1)
- ultimas 4 semanas antes do periodo atual (para media movel)

Se nao conseguir puxar os tres, declare e siga com o que tiver.

### Midia via V4mos

Para Meta Ads, use o script quando houver credenciais do cliente:

```bash
python3 .claude/skills/v4mos-dados-meta-ads/scripts/v4mos_meta.py campaigns --cliente [cliente] --days 7 --format json
```

Para comparacao temporal, rode tambem com `--days 14` e `--days 35` (ou ajuste conforme o periodo analisado) e separe os buckets depois.

Extraia, quando disponivel:

- investimento
- impressoes
- cliques
- link clicks
- landing page views
- leads/eventos de conversao
- campanhas

### CRM

Se o cliente usar Kommo via V4mos, use a API quando houver `WORKSPACE_ID`, `CLIENT_ID` e `CLIENT_SECRET` no `.env` do cliente:

```bash
curl -s "https://api.data.v4.marketing/v1/kommo/leads?workspaceId=[WORKSPACE_ID]" -H "x-client-id: [CLIENT_ID]" -H "x-client-secret: [CLIENT_SECRET]"
```

Conte no periodo:

- MQL: lead qualificado
- SQL: status definido no contexto do cliente
- vendas: ganhos/fechado
- faturamento: soma do campo de valor/preco, quando confiavel

Se MQL, SQL, vendas ou faturamento vierem manualmente do CRM do cliente, registre como dado manual.

### Controle de fontes

Sempre monte mentalmente esta tabela antes da conclusao:

| Fonte | O que trouxe | Periodo | Confiabilidade |
|---|---|---|---|
| V4mos | investimento, cliques, impressoes, leads | data consultada | alta/media/baixa |
| CRM | MQL, SQL, vendas, faturamento | data consultada | alta/media/baixa |
| Manual | ajustes do usuario/cliente | data informada | media/baixa |

Se uma API ou CSV tiver linhas de total que duplicam dados, remova essas linhas antes de calcular.

## Passo 3 - Calcular metricas

### Inside sales

Calcule quando houver dados:

| Etapa | Metrica |
|---|---|
| Midia | Investimento |
| Exposicao | CPM, Impressoes |
| Atencao | CPC, CTR, Cliques |
| Landing page | Taxa de conversao LP |
| Lead | Leads, CPL |
| Qualificacao | Lead > MQL, MQL, CPMQL |
| Compromisso | MQL > SQL, SQL, Custo por SQL |
| Venda | SQL > Venda, Vendas, CPV |
| Receita | Ticket medio, Faturamento, ROAS |

Formulas:

- CPM = investimento / impressoes * 1000
- CPC = investimento / cliques
- CTR = cliques / impressoes
- Taxa de conversao LP = leads / cliques ou leads / landing page views, conforme dado disponivel
- CPL = investimento / leads
- Lead > MQL = MQL / leads
- CPMQL = investimento / MQL
- MQL > SQL = SQL / MQL
- Custo por SQL = investimento / SQL
- SQL > Venda = vendas / SQL
- CPV = investimento / vendas
- Ticket medio = faturamento / vendas
- ROAS = faturamento / investimento

### Hibrido ecommerce

Inclua, quando houver dados:

- sessoes
- visualizacoes de produto
- add to cart
- checkout
- compras
- checkout > compras
- receita
- ticket medio
- ROAS
- CPA compra

Formulas adicionais:

- Checkout > Compras = compras / checkouts
- CPA compra = investimento / compras

## Passo 4 - Comparacao temporal (obrigatorio v1.2)

Para cada metrica calculada no Passo 3, gere tres deltas:

1. **Periodo anterior equivalente** = (P0 - P-1) / P-1
2. **vs media movel 4 semanas** = (P0 - MM4) / MM4
3. **MoM mesmo periodo** = (P0 - M-1) / M-1 (quando disponivel)

Regras de leitura:

- **Reporte SEMPRE delta percentual E delta absoluto.** Em base pequena, % engana. Ex: CPL foi de R$ 20 pra R$ 30 = +50% mas pode ser irrelevante se leads < 30.
- **Se os 3 deltas convergem na mesma direcao:** sinal forte.
- **Se 2 de 3 convergem:** sinal medio.
- **Se divergem entre si:** ruido ou mudanca estrutural recente. Investigar antes de concluir.
- Se nao houver dado historico, pule este passo, declare no output e siga.

## Passo 5 - Guard-rails de significancia (obrigatorio v1.2)

Antes de declarar qualquer metrica como "boa" ou "ruim", aplique os dois filtros:

### 5.1 - Volume minimo fixo (padrao)

Nao tire conclusao sobre a metrica se o volume estiver abaixo de:

| Metrica | Volume minimo |
|---|---|
| CTR | 1.000 impressoes ou 100 cliques |
| CPC | 100 cliques |
| Taxa conversao LP | 500 sessoes de LP ou 100 cliques |
| CPL | 30 leads |
| Lead > MQL | 30 leads |
| CPMQL | 20 MQL |
| MQL > SQL | 20 MQL |
| Custo por SQL | 10 SQL |
| SQL > Venda | 10 SQL |
| CPV / ROAS | 10 vendas |
| Checkout > Compra | 50 checkouts |

Se volume abaixo do minimo: marque a metrica como **"inconclusivo - baixo volume"** e nao use como base de decisao.

### 5.2 - Banda historica dinamica (quando houver dado)

Se houver pelo menos 8 semanas de historico confiavel:

1. Calcule media e desvio-padrao da metrica nas ultimas 8 semanas.
2. Defina banda normal = media +/- 1 desvio.
3. Se o valor atual cai dentro da banda: **"dentro da variacao natural"** - nao e sinal, mesmo que delta % pareca grande.
4. Se o valor atual cai fora da banda mas dentro de 2 desvios: **"desvio moderado"** - vale investigar.
5. Se cai fora de 2 desvios: **"anomalia estatistica"** - sinal forte, investigar obrigatorio.

Quando banda dinamica e volume minimo conflitarem, **volume minimo vence** (nao leia metrica de base pequena, mesmo que pareca anomalia).

### 5.3 - Janela de reaprendizagem

Se houve mudanca estrutural nos ultimos 3-7 dias (novo criativo ativo, budget alterado, novo publico, nova LP), sinalize:

> "Dados em janela de reaprendizagem - interpretacao com cautela ate [data + 7 dias]."

## Passo 6 - Budget e pacing

Sempre que houver budget planejado:

1. Calcule dias decorridos e dias restantes do periodo.
2. Calcule investimento esperado ate hoje.
3. Compare investimento real vs esperado.
4. Classifique:
   - `Abaixo do pacing`: investiu menos que o esperado.
   - `No pacing`: diferenca pequena e aceitavel.
   - `Acima do pacing`: investiu mais que o esperado.
5. Sugira acao:
   - acelerar verba
   - segurar verba
   - redistribuir entre canais/campanhas
   - revisar teto diario

## Passo 7 - Arvore de diagnostico (obrigatorio, exceto `--rapido`)

Em vez de "chutar" o gargalo, rode a arvore por eliminacao. Siga a ordem, de cima pra baixo. Na primeira resposta "sim com evidencia", pare e marque esse como diagnostico principal - os demais sao secundarios.

### 7.1 - Dados estao confiaveis?

- Periodo correto?
- Evento de lead correto?
- Fontes cruzam (plataforma vs CRM vs Sheets)?
- Ha duplicidade ou linha de total suja?

Se NAO: **Trava 0 - Cegueira.** Nao avance. Corrija dados primeiro.

### 7.2 - Budget esta sendo entregue?

- Pacing dentro do planejado?
- Campanhas ativas entregando volume normal?
- Nao ha limite diario atingido prematuramente?

Se NAO: **Problema de Pacing.** Pode mascarar ou gerar falso gargalo.

### 7.3 - Exposicao esta acontecendo?

- Impressoes dentro da banda historica?
- CPM dentro do normal para o nicho/conta?

Se NAO: **Trava 7 - Exposicao.** Investigar segmentacao, leilao, qualidade de criativo no feed.

### 7.4 - Cliques e atencao estao OK?

- CTR dentro da banda historica?
- CPC dentro do normal?

Se NAO: **Trava 6 - Atencao.** Criativo, copy de anuncio, oferta.

### 7.5 - Landing page converte?

- Taxa de conversao LP dentro da banda?
- Landing page views / cliques razoavel (detecta drop antes da LP)?

Se NAO: **Trava 5 - Interesse.** LP, oferta, formulario, velocidade.

### 7.6 - Qualidade do lead?

- CPL ok mas Lead > MQL caiu?
- Fonte de trafego trazendo lead qualificado?

Se NAO: **Trava 4 - Qualificacao.** Segmentacao, palavra-chave, copy de anuncio gerando expectativa errada.

### 7.7 - Comercial esta processando?

- MQL > SQL dentro do historico?
- Tempo de resposta do SDR ok (se dado disponivel)?
- Taxa de contato ok (se dado disponivel)?

Se NAO: **Trava 3 - Compromisso.** Nao e problema de trafego - e comercial/operacao.

### 7.8 - SQL esta fechando?

- SQL > Venda dentro do historico?
- Ticket medio caiu (pode indicar mix pior)?

Se NAO: **Trava 2 - Decisao.** Proposta, objecoes, comercial.

### 7.9 - Cliente repete?

- LTV caiu?
- Recompra/renovacao caiu?

Se NAO: **Trava 1 - Retencao.** Fora do escopo direto de trafego, mas afeta budget sustentavel.

### Saida da arvore

Ao terminar, declare:

- **Diagnostico primario:** [trava/categoria com evidencia numerica]
- **Diagnosticos secundarios:** [se houver]
- **Descartados com evidencia:** [etapas que passaram no guard-rail, para nao voltar nelas]

Se o diagnostico primario for Trava 3, 2 ou 1 (pos-lead), **deixe explicito que aumentar verba nao resolve e pode piorar CAC.**

## Passo 8 - Traducao para linguagem de mercado (opcional)

Para conteudo externo, LinkedIn, apresentacao para cliente nao-V4, traduza as Travas:

| Trava V4 | Linguagem de mercado |
|---|---|
| Trava 7 - Exposicao | TOFU / Awareness / Reach |
| Trava 6 - Atencao | TOFU / Creative efficiency |
| Trava 5 - Interesse | MOFU / LP conversion |
| Trava 4 - Qualificacao | MOFU / Lead quality |
| Trava 3 - Compromisso | BOFU / SDR efficiency |
| Trava 2 - Decisao | BOFU / Close rate |
| Trava 1 - Retencao | Retention / LTV |
| Trava 0 - Cegueira | Data integrity |

## Passo 9 - Output padrao

Comece sempre com periodo, modelo e confiabilidade.

```markdown
# Analise de Trafego e Funil - [Cliente]

Periodo: [data inicial] a [data final]
Modelo: [inside sales/ecommerce/hibrido]
Confiabilidade dos dados: [alta/media/baixa]
Janela de reaprendizagem: [sim/nao - se sim, ate quando]

## Resumo executivo
- [1-3 bullets com a leitura principal]
- [inclua o diagnostico primario aqui]

## Tabela de metricas com comparacao temporal

| Metrica | P0 | vs periodo anterior | vs MM4 | MoM | Volume ok? | Leitura |
|---|---:|---:|---:|---:|:---:|---|
| CPL | R$ 45 | -12% | -8% | -15% | sim (n=120) | melhora consistente |
| CTR | 1.8% | +5% | +2% | +10% | sim (n=15k) | dentro da banda |
| Lead > MQL | 22% | -30% | -25% | -28% | sim (n=120) | piora consistente - investigar |

## Budget e pacing
- Budget planejado: [valor]
- Investimento realizado: [valor]
- Pacing: [abaixo/no/acima]
- Acao recomendada: [acao]

## Diagnostico (via arvore)

**Primario:** [Trava X - Nome] - [evidencia numerica]
**Secundarios:** [se houver]
**Descartados:** [lista curta do que passou no guard-rail]

## Hipoteses testaveis

1. **Hipotese:** [o que voce acredita que esta causando]
   **Acao:** [o que mudar]
   **Resultado esperado:** [metrica alvo e direcao]
   **Janela de teste:** [tempo]
   **Criterio de sucesso:** [numero especifico]

2. [segunda hipotese]
3. [terceira hipotese]

## Dados pendentes ou duvidosos
- [lista objetiva]
```

Para Sprint Planning, acrescente:

```markdown
### Sprint Planning - [Cliente] ([Periodo])

**Qual a Trava do Negocio?**
- **[Trava X - Nome]:** [explicacao com evidencia numerica e comparacao temporal]

**Hipoteses do Sprint:**
- H1: [hipotese formatada como acima]
- H2: [hipotese formatada como acima]

**Nao mexer em:**
- [itens que passaram no guard-rail e estao estaveis]
```

## Regras de perguntas

Se faltar informacao, pergunte o minimo necessario:

1. Qual cliente e periodo?
2. Qual modelo do cliente: inside sales, ecommerce ou hibrido?
3. Onde esta a planilha/CSV/JSON?
4. MQL, SQL, vendas e faturamento vem de qual fonte?
5. **Novo v1.2:** houve mudanca estrutural nos ultimos 7 dias (criativo, publico, budget, LP)?

Se o usuario ja forneceu arquivos ou contexto suficiente, nao pare para perguntar. Analise com ressalvas.

## Criterios de qualidade

Uma boa analise v1.2:

- bate com a fonte de verdade
- nao mistura periodo
- separa Meta e Google quando necessario
- nao conta lead duplicado
- sinaliza dado manual
- **passa pelos guard-rails antes de concluir**
- **compara com pelo menos um periodo anterior**
- **chega ao diagnostico via arvore, nao por intuicao**
- **formata acoes como hipotese testavel**
- destaca gargalo do funil
- mostra pacing de budget
- termina com acoes praticas para o gestor de trafego
