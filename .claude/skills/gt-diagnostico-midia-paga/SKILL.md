---
name: gt-diagnostico-midia-paga
description: "Diagnostico de midia paga: metricas atuais vs benchmarks, top 3 problemas e plano de acao 30 dias. Puxa dados reais do V4MOS (MediaInvestment). Use quando o operador disser /gt-diagnostico-midia-paga ou 'analisar midia paga' ou 'diagnostico de ads' ou 'como esta a conta de anuncios'."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
tools: []
week: 2
estimated_time: "3h"
output_file: "gt-diagnostico-midia-paga.json"
v4mos_data: true
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Diagnostico de Midia Paga (POP 2.1)

Voce e um especialista em midia paga com foco em performance para PMEs brasileiras. Vai analisar a conta de midia do cliente, comparar com benchmarks do setor, e gerar um plano de acao prioritizado.

> **Posição no fluxo:** Semana 2 — comum a todos os modelos. Pull de 90 dias, CAC/CPL/ROAS vs benchmark, diagnóstico campanha a campanha, plano de 30 dias e cenários de realocação. Alimenta o forecast (POP 3.12).

**DIFERENCIAL V4MOS:** Se o cliente tem workspace ativo no V4MOS, voce puxa dados REAIS de MediaInvestment via API. Isso e ouro — a maioria das ferramentas so trabalha com dados que o operador exporta manualmente.

## Dados necessários

1. Leia `client.json` (seção `briefing`) — extraia: NOME_CLIENTE, SEGMENTO, BUDGET_MENSAL, OBJETIVO_MIDIA
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, canais preferenciais do ICP
3. Verifique `client.json` (seção `connectors`):
   - Se `connectors.fetched_at` não é null: use os dados de `google_ads` e `facebook_ads` já salvos
   - Se `connectors.fetched_at` é null: use `/v4mos-dados-meta-ads` para Meta Ads e os dados reais disponíveis na KB para Google Ads
   - Se não há `workspace_id` no client.json: peça dados ao operador (exportação manual dos últimos 90 dias)

   **Estrutura dos dados V4MOS em connectors (atualizada — agregações temporais e por dimensão):**
   - `connectors.google_ads.campaigns[]` → {name, type, status, cost, clicks, impressions, conversions, ctr, cpa}
   - `connectors.google_ads.monthly_evolution[]` → {month, cost, clicks, impressions, conversions, ctr, cpa} — **use direto em `google_ads.monthly_evolution`**
   - `connectors.google_ads.day_of_week[]` → {day, clicks, impressions, cost, pct, ctr} — ordem Seg→Dom
   - `connectors.google_ads.gender_breakdown[]` → {gender, clicks, cost, pct_clicks, ctr, cpa}
   - `connectors.google_ads.top_keywords[]` → {keyword, match_type, clicks, impressions, ctr, cost, cpc, cpa, conversions}
   - `connectors.facebook_ads.campaigns[]` → {name, objective, spend, impressions, clicks, reach, cpm, ctr}
   - `connectors.facebook_ads.monthly_evolution[]` → {month, spend, impressions, clicks, reach, cpm, ctr}
   - `connectors.facebook_ads.creatives[]` → {ad_id, ad_name, spend, impressions, clicks, ctr, cpc, cpm, reach, object_type, thumbnail_url, instagram_permalink_url, ad_created_time, ...}
   - `connectors.period` → {start, end} — período dos dados (normalmente 90 dias)

   **IMPORTANTE — evite a armadilha de totais inflados:** o endpoint V4MOS `facebook/ads/campaigns` (e potencialmente outros) **ignora** o filtro de data `createdStart/createdEnd` e retorna histórico completo. O script `v4mos_fetch.sh` agora filtra por `segments_date`/`date_start` no Python — portanto os totais em `connectors.*.total_*` refletem o período real. Não some campanhas brutas por conta própria sem filtrar data.

   **API V4MOS (para referência, se precisar buscar manualmente):**
   ```bash
   # workspaceId é QUERY PARAMETER — não path
   curl -s "https://api.data.v4.marketing/v1/google/ads/campaigns?workspaceId={WORKSPACE_ID}&limit=500" \
     -H "x-client-id: {CLIENT_ID}" -H "x-client-secret: {CLIENT_SECRET}"
   curl -s "https://api.data.v4.marketing/v1/facebook/ads/campaigns?workspaceId={WORKSPACE_ID}&limit=500" \
     -H "x-client-id: {CLIENT_ID}" -H "x-client-secret: {CLIENT_SECRET}"
   ```
   Nunca exponha credenciais. Se a integração não estiver configurada, peça uma exportação dos últimos 90 dias.

### Se o cliente NAO investe em midia

Se nao ha dados de midia paga (nem no V4MOS, nem exportacao):

> Este cliente ainda nao investe em midia paga. Em vez de diagnostico, vou gerar um **plano de lancamento** de midia alinhado ao ICP e posicionamento. Posso seguir?

Se sim, adapte a geração para plano de lancamento (estrutura de campanhas, budget recomendado, publicos iniciais, criativos prioritarios).

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

Consulte `references/benchmarks-por-setor.md` para os benchmarks do segmento.

### Dados de mídia e status de integração

Apresente fonte dos dados, período, budget, integrações V4MOS e métricas atuais (CPL, CTR, taxa de conversão LP, ROAS, CPC). Liste dados faltantes.

Se algum dado crítico estiver faltando, pergunte ao operador de uma vez.

### Blocos `google_ads` e `meta_ads` — obrigatórios (por canal)

O portal renderiza cada canal em uma seção separada, iniciando por um **bloco de abertura** com 4 cards + 1 card "Resumo Executivo". Gere os dois objetos top-level `google_ads` e `meta_ads` com os campos abaixo — o renderer NÃO inventa fallback, se o campo estiver ausente o card some.

**`google_ads` — campos esperados:**
```json
{
  "integration": "nome da conta no V4MOS",
  "budget_monthly_declared": 2400,
  "budget_monthly_actual": 1450.92,
  "total_campaigns": 6,
  "active_campaigns": 1,
  "paused_campaigns": 5,
  "status": "healthy_but_choked | subscale | healthy | critical | broken",
  "score": 62,
  "score_classification": "medium",
  "total_spend_90d": 4352.77,
  "total_clicks_90d": 1751,
  "total_impressions_90d": 46491,
  "total_conversions_90d": 300,
  "avg_cpa": 14.51,
  "avg_ctr": 3.77,
  "strategic_diagnosis": "3-5 linhas. Veredito do canal: o que está acontecendo, por que acontece, qual é o destravamento. Usado no card Resumo Executivo.",
  "active_campaign": { "name":"...", "type":"SEARCH", "status":"ENABLED", "cost_90d":..., "ctr":..., "cpa":..., "note":"..." },
  "paused_campaigns_opportunity": [ {name,type,cost_90d,clicks,impressions,conversions,ctr,cpa,note} ],
  "monthly_evolution": [ {month,cost,clicks,impressions,conversions,ctr,cpa} ],
  "day_of_week": [ {day,clicks,impressions,cost,pct,ctr} ],
  "gender_breakdown": [ {gender,clicks,cost,pct_clicks,ctr,cpa} ],
  "top_keywords": [ {keyword,match_type,clicks,impressions,ctr,cost,cpc,cpa,conversions,insight?,tag?} ]
}
```

**`meta_ads` — campos esperados:**
```json
{
  "integration": "nome da conta no V4MOS",
  "budget_monthly_declared": 800,
  "budget_monthly_actual": 424.53,
  "total_campaigns": 5,
  "total_ads": 43,
  "total_creatives": 43,
  "status": "critical | subscale | healthy | broken",
  "score": 38,
  "score_classification": "medium_low",
  "total_spend_90d": 1273.60,
  "total_clicks_90d": 1442,
  "total_impressions_90d": 112295,
  "total_reach_90d": 71890,
  "avg_ctr": 1.28,
  "avg_cpm": 11.34,
  "strategic_diagnosis": "3-5 linhas. Veredito do canal. Usado no card Resumo Executivo.",
  "critical_issues": [ "marcador por linha, começa com ▲ implicitamente no render" ],
  "top_5_ads_by_spend": [ {ad_name,campaign_context,spend,impressions,clicks,ctr,cpc,cpm,object_type,creative_id,note} ],
  "icp_aligned_creatives": [ ... ],          // opcional — destaques temáticos alinhados ao ICP
  "monthly_evolution": [ {month,spend,impressions,clicks,reach,cpm,ctr} ],
  "creative_gallery": [ ... ],              // vem do connectors.facebook_ads.creatives, mas com verdict M/O/E por ad
  "creative_gallery_summary": { total_displayed, total_ads, manter, otimizar, eliminar, note }
}
```

**COMO O PORTAL RENDERIZA O BLOCO DE ABERTURA (Google e Meta):**
1. **4 cards** com cores semáforo:
   - Google: Investido 90d · CTR médio · CPA médio · Conversões 90d
   - Meta: Investido 90d · CTR médio · CPM médio · Alcance 90d (fallback: Clicks 90d)
2. **Linha de stats secundárias** (muted): Média mensal · Clicks · Impressões · Ads/Campanhas
3. **Card "Resumo Executivo"** com o texto de `strategic_diagnosis` (use este campo para a narrativa do canal — não é local para sinônimo do `summary` global, é o veredito específico de Google OU Meta).

Se `strategic_diagnosis` estiver ausente, o card some. Sempre preencha.

### Métricas vs benchmarks por segmento

| Metrica | Atual | Benchmark setor | Status | Gap |
|---------|-------|-----------------|--------|-----|
| CPL | R$ {atual} | R$ {bench} | {acima/abaixo/ok} | {%} |
| CTR | {atual}% | {bench}% | ... | ... |
| Conv. LP | {atual}% | {bench}% | ... | ... |
| ROAS | {atual}x | {bench}x | ... | ... |
| CPC | R$ {atual} | R$ {bench} | ... | ... |

Legenda: 🔴 Critico (>50% abaixo) | 🟡 Atencao (20-50% abaixo) | 🟢 Saudavel

### Diagnóstico por dimensão

**ESTRUTURA DE CONTA:** organização, segmentação, budget allocation
**CRIATIVOS:** ativos, melhor/pior performance, teste A/B, frequência
**PÁGINAS DE DESTINO:** LPs usadas, coerência, taxa de rejeição
**PÚBLICOS:** tipos usados, sobreposição, retargeting

### Top 3 problemas críticos

Para cada: título, evidência nos dados, impacto estimado, dimensão afetada.

### Plano de ação — 30 dias

| # | Acao | Prioridade | Impacto esperado | Responsavel | Prazo |
|---|------|-----------|------------------|-------------|-------|

### Keyword Clusters (OBRIGATÓRIO — search)

Não trate keywords como lista única. Agrupe em 4-6 clusters estratégicos. Para cada:
- `cluster`: nome (ex: "Marca", "Produto/Serviço", "Localização", "Genéricas")
- `keywords`: exemplos (5-15) — keywords ATUALMENTE EM USO no cluster
- `intent`: navegacional | informacional | transacional | comercial
- `budget_allocation_pct`: % do budget de search para esse cluster
- `expected_cpc_range`: faixa esperada (R$)
- `bid_strategy`: estratégia (máx. conv., CPA alvo, manual)
- `copy_angle`: ângulo da copy para esse cluster
- `risk`: principal risco (ex: concorrência alta, baixa intenção, canibalização)
- `opportunity_keywords`: **opcional mas RECOMENDADO** — lista de keywords relevantes para o ICP que o cliente NÃO usa hoje. Itens `{keyword, intent?, volume_estimate?|search_volume_monthly?, expected_cpc?|cpc_range?, rationale}`. Base: compare `google_ads.top_keywords` (ativas) contra ICP + segmento + concorrentes. O portal renderiza uma tabela "Keywords Relevantes Não Utilizadas Hoje — Oportunidades" agregando estes campos de todos os clusters.

Alternativa: gere `opportunity_keywords` como array top-level (fora dos clusters) no formato `[{keyword, cluster, intent, volume_estimate, expected_cpc, rationale}]` — o renderer aceita ambos.

### Budget Reallocation Scenarios (OBRIGATÓRIO — 3 cenários)

Não entregue apenas uma recomendação de budget — gere 3 cenários para o operador escolher.
- **A. Conservador:** mantém budget atual, reorganiza mix
- **B. Realista (RECOMENDADO):** reorganização + leve aumento, mapeamento de campanhas — o renderer marca automaticamente o cenário do meio como "★ Recomendado"
- **C. Agressivo:** aumento significativo para buscar teto de demanda

Para cada cenário, gere os seguintes campos (os nomes **preferidos** são os primeiros; alternativas são aceitas pelo renderer):

**Obrigatórios / estruturais:**
- `name` (pref) ou `label` — nome do cenário
- `total_budget_monthly` — budget total mensal. Se ausente, o renderer soma automaticamente os splits.
- `google_split` (pref) ou `google_allocation{value|amount|brl, pct}` — valor em R$ no Google
- `meta_split` (pref) ou `meta_allocation{value|amount|brl, pct}` — valor em R$ no Meta
- `expected_leads_monthly` (pref) ou `projected_leads_month` — leads/mês esperados
- `expected_cpl` (pref) ou `projected_cpl` — CPL esperado em R$
- `expected_roas` — ROAS esperado
- `risk_assessment` — avaliação do risco

**Opcionais (enriquecem o card do cenário):**
- `delta_leads` — variação vs. atual (número ou "+15%")
- `effort_weeks` — semanas para implementar
- `confidence` — high/medium/low (ou alta/média/baixa)
- `campaigns_structure[]` — lista de campanhas com {campaign, platform, budget_monthly, objective}

> **COMO O PORTAL RENDERIZA:** Tabela side-by-side com cenários como colunas e métricas (Budget, Google, Meta, Leads/mês, CPL, ROAS) como linhas. Cada linha tem barras normalizadas por métrica para comparação visual. **Não existe mais gráfico de barras agrupadas com escalas mistas** — escolha os campos acima e o renderer formata o resto.

### Creative Testing Hypotheses (OBRIGATÓRIO — 4-6 hipóteses)

Cada hipótese é um teste A/B real, não uma ideia vaga. Para cada (H1, H2, ...):
- `hypothesis`: afirmação testável ("Se X, então Y, porque Z")
- `angle`: ângulo de comunicação
- `format`: formato (single image, carousel, reels, VSL)
- `hook`: primeiras 3 segundos / headline
- `body`: copy principal
- `cta`: call to action
- `target_audience`: público específico
- `success_criteria`: métrica + threshold (ex: "CTR > 1.5% E CPL < R$20")
- `testing_budget`: R$ do teste
- `testing_duration_days`: dias

Feche com `testing_budget_total_week_1`.

### Daypart Optimization (OBRIGATÓRIO)

Não basta "rodar o dia todo". Proponha ajustes de lance por dia/hora baseados no comportamento da persona. Para cada ajuste:
- `day_time`: janela (ex: "Segunda-Sexta 9-12h", "Sábado 10-18h", "Domingo")
- `bid_adjustment_pct`: +X% ou -X%
- `rationale`: por que (dado de comportamento, padrão do segmento)

### Forecast Sensitivity Analysis (opcional)

**Status:** Não é mais obrigatório. O portal suporta o bloco mas ele é dispensável — `honesty_alert` e `realistic_goal_90d.alert` cobrem os riscos principais. Gere apenas se:
- O caso tem múltiplas variáveis interdependentes que mudam significativamente o forecast, ou
- O operador pede explicitamente o what-if.

Se gerar, use a estrutura:
- `base_case`: meta central com `leads_monthly`, `cpl`, `cac`, `revenue_monthly`, `roas`.
- `variations`: 4-6 cenários "what-if" `{scenario, variable_change, impact_on_leads, impact_on_cpl, impact_on_revenue, delta_vs_base_pct}`.

O renderer exibe apenas os cards (sem gráfico).

### Meta realista — 90 dias

Gere `realistic_goal_90d` com os seguintes campos (o portal renderiza 4 cards + card "Premissas"):
- `current_cpl`, `target_cpl` — CPL atual e alvo em R$
- `current_cac`, `target_cac` — CAC atual e alvo em R$
- `current_leads_month`, `target_leads_month` — volume de leads atual e alvo
- `current_agendamentos_month`, `target_agendamentos_month` — opcional, se a skill de posicionamento define funil lead→agendamento
- `premissas`: lista de 3-6 premissas concretas (ex: "LP do produto principal no ar na Semana 3")

**NÃO gere** o campo `alert` em `realistic_goal_90d` — o portal não renderiza mais essa caixa. Se há risco de prazo/acesso/budget, inclua em `honesty_alert` (global) ou como premissa condicional.

Gere também `realistic_goal` com `target_cpl`, `target_roas`, `justification`, `assumptions`, `risk_factors` — usado como texto de apoio.

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos acima, SEMPRE inclua:

- **`summary_headline`** (max 200 char) — manchete com o veredito. Ex: "CPL atual (R$ 85) está 40% acima do benchmark — realocação B recupera R$ 12K/mês sem subir orçamento."
- **`summary_highlights`** (4-6 itens, `{category, label, value, subtext, tone}`) — para diagnóstico de mídia sugestões:
  - `posicao`: CPL atual vs benchmark, leads/mês, CAC, ROAS
  - `oportunidade`: cenário de realocação com maior upside, economia projetada
  - `risco`: plataforma/campanha queimando verba sem retorno
  - `janela`: tempo de ramp-up para estabilizar CPL alvo
- **`summary_key_findings`** (3-5 itens, `{category, text}`) — `vantagem|contexto|ameaca|acao`.

### Ponto de alavancagem

Em diagnóstico de mídia, o ponto de alavancagem é o **canal/campanha com maior gap entre performance atual e potencial** — tipicamente o cenário de realocação recomendado + hipótese criativa principal. Estruture em `key_insight`:
```json
"key_insight": {
  "headline": "Frase sobre o destravamento (ex: 'Cortar Performance Max e dobrar Search Branded baixa CPL em 35%')",
  "context": "2-3 linhas sobre por que o desperdício acontece e o caminho",
  "numbered_reasons": ["(1) evidência do gap", "(2) causa-raiz (estrutura/copy/segmentação)", "(3) upside projetado"],
  "discussion_anchor": "Por que o stakeholder precisa aprovar a realocação antes do próximo ciclo"
}
```

Se os dados são insuficientes (menos de 60 dias, tracking quebrado) ou o orçamento é incompatível com o objetivo, inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP)?
- [ ] Benchmarks são do segmento correto do cliente?
- [ ] Plano de ação tem responsáveis e prazos realistas?
- [ ] Meta de 90 dias é honesta (não promessa mágica)?
- [ ] `google_ads` tem total_spend_90d, avg_ctr, avg_cpa, total_conversions_90d E `strategic_diagnosis` preenchido (3-5 linhas)?
- [ ] `meta_ads` tem total_spend_90d, avg_ctr, avg_cpm, total_reach_90d E `strategic_diagnosis` preenchido (3-5 linhas)?
- [ ] Totais 90d de google_ads e meta_ads BATEM com `connectors.google_ads.total_cost` e `connectors.facebook_ads.total_spend` (V4MOS filtrado)?
- [ ] `budget_monthly_actual` por canal é `total_spend_90d / 3` (cliente pode estar subinvestindo — flag isso se delta vs declarado > 20%)?
- [ ] `keyword_clusters` (search) tem 4-6 clusters com intent, budget %, copy angle e risco?
- [ ] Pelo menos 1 cluster tem `opportunity_keywords[]` (keywords relevantes para o ICP NÃO ativas hoje)?
- [ ] `budget_reallocation_scenarios` tem 3 cenários (A/B/C) com estrutura de campanhas e projeção?
- [ ] `creative_testing_hypotheses` tem 4-6 hipóteses testáveis com success_criteria numérico e budget?
- [ ] `daypart_optimization` traz ajustes específicos por janela com rationale?
- [ ] `forecast_sensitivity_analysis` (opcional) — se gerar, tem base_case + 4-6 variações?
- [ ] Tem `summary_headline` específico?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos?
- [ ] Identificou `key_insight` (realocação/hipótese com maior upside)?
- [ ] Se há limitação de dados/orçamento, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "Os benchmarks fazem sentido para a realidade deste cliente especifico? Algum contexto que mude a leitura?"
- "O plano de acao e executavel na realidade deste cliente? Alguma acao que depende de algo que nao temos?"
- "A meta de 90 dias parece realista?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/gt-diagnostico-midia-paga.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Diagnóstico concluído. CPL atual: R$ {atual} → Meta 90d: R$ {meta}. Problemas críticos: {numero}."
   - "Este diagnostico alimenta: /gt-forecast-midia, /copy-anuncios, /designer-criativos-anuncios"
   - "Proximo passo recomendado: /gt-diagnostico-criativos"


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do diagnóstico de mídia: principal problema e ROAS atual vs benchmark. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
