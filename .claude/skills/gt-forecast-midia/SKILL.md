---
name: gt-forecast-midia
description: "Cria o forecast e plano de mídia de 6 meses: modelagem financeira evolutiva, distribuição por plataforma/funil, campanhas detalhadas (TECR), cronograma e assumptions explícitas. Output exportado para Google Sheets. Use quando disser /gt-forecast-midia ou 'planejamento de mídia' ou 'forecast' ou 'budget de anúncios'."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies:
  - gt-diagnostico-midia-paga
inputs:
  - client.json (briefing)
  - gt-diagnostico-midia-paga.json
  - geral-persona-icp.json
  - geral-posicionamento-estrategico.json
output: gt-forecast-midia.json
export: google-sheets
week: 4
type: automated
estimated_time: "2h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Forecast e Plano de Mídia — 6 Meses (POP 3.12)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (e-commerce / inside-sales / pdv) — entregável final que amarra toda a estratégia. Horizonte de **6 meses** com curva evolutiva (não linear) e **assumptions explícitas**. Se mudar a premissa, refaz o forecast.

Você é um especialista em planejamento de mídia paga para PMEs brasileiras. Vai criar o forecast completo de 6 meses: budget recomendado, distribuição por plataforma e funil, campanhas detalhadas, metas de resultado evolutivas e critérios de alerta.

## Dados necessários

1. `client.json` (seção `briefing`) — nome, segmento, budget disponível, ticket médio, objetivo
2. `outputs/gt-diagnostico-midia-paga.json` — análise de mídia atual, CPL/ROAS atual, problemas, benchmarks
3. `outputs/geral-persona-icp.json` — ICP, canais preferidos
4. `outputs/geral-posicionamento-estrategico.json` — PUV, diferenciais
5. `client.json` (seção `history`) — decisões anteriores

Consulte `references/benchmarks-forecast.md` para benchmarks de CPL/ROAS por segmento.

---

## Geração

Gere o output COMPLETO de uma vez: modelagem + distribuição + cronograma + alertas. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

### Premissas (explicitar todas)

CPL estimado (com fonte), taxa de conversão, ROAS esperado, ramp-up (Mês 1 tem CPL 20-30% maior), sazonalidade.

### Modelagem financeira de 6 meses (evolutiva, não linear)

Fases: **M1 setup/aprendizado** · **M2–M3 otimização** · **M4–M6 escala**.

| Métrica | M1 (setup) | M2 | M3 | M4 | M5 | M6 |
|---|---|---|---|---|---|---|
| Budget, CPL, Leads, Taxa conversão, Vendas, Faturamento, ROAS |

A curva evolui: M1 com CPL 20-30% maior (aprendizado), ganho gradual de eficiência em M2-M3, escala em M4-M6. NÃO modele crescimento linear ("+10%/mês").

**Cenários:** Otimista (CPL -20%, conversão +20%), Realista (benchmarks), Pessimista (CPL +30%, conversão -20%).

### Campanhas detalhadas (TECR)

Para cada campanha: **T**ópico, **E**stratégia, **C**onjunto (segmentação/criativos), **R**esultado esperado — com objetivo, verba e fase de funil.

### Distribuição por plataforma

| Plataforma | % do budget | R$/mês | Objetivo principal |
Lógica: ICP busca no Google? → Google Search. ICP impactado visual? → Meta. Budget < R$3k? → 1 plataforma só.

### Distribuição por fase do funil

| Fase | % do budget | Objetivo |
Regras: Marca nova → mais topo (40-50%). Marca conhecida → mais fundo (40-50%). Remarketing sempre 10-15%.

### Cronograma de 6 meses (180 dias)

*M1 (Setup/Aprendizado):* configuração, lançamento, primeiras otimizações. Meta e ações semanais.
*M2–M3 (Otimização):* eliminar piores, escalar melhores, novos hooks, calibrar segmentação. Metas e ações.
*M4–M6 (Escala):* dobrar budget nos melhores, expandir lookalike/novas praças, sustentar eficiência. Metas e ações.

Cada fase com `assumptions` e `dependencies` explícitas (criativo pronto, LP no ar, SDR treinado).

### Alertas e critérios de pausa

| Métrica | Limite de alerta | Ação imediata |
CPL, CTR, ROAS, CPC, Frequência, Budget diário.

### Critérios de escala

| Métrica | Limite para escalar | Ação |

### Disclaimer

Variáveis que podem impactar: qualidade dos criativos, velocidade de aprovação, sazonalidade, tempo de resposta aos leads, mudanças de algoritmo, concorrência, qualidade da LP.

### Exportação para Google Sheets

```bash
gog sheets create --title "Forecast Mídia - {NOME_CLIENTE}" --no-input
```
5 abas: Modelagem Financeira (6 meses), Distribuição, Cronograma 6 Meses, Alertas/Critérios, Assumptions/Premissas.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (diagnóstico de mídia)?
- [ ] Premissas têm fonte (não "números mágicos")?
- [ ] Cenário pessimista é realista (não assustador demais)?
- [ ] Disclaimer é honesto sobre variáveis de risco?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "O budget mensal de R$ {BUDGET_MENSAL} está confirmado?"
- "O ticket médio de R$ {TICKET_MEDIO} está correto?"
- "A taxa de conversão é realista para o processo comercial atual?"
- "O cronograma é factível com os recursos disponíveis?"
- "Os limites de alerta são adequados?"
- "O disclaimer é honesto? O cliente vai entender que forecast não é garantia?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/gt-forecast-midia.json` (com campo `summary` no topo, incluindo link Sheets)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph

## Formato do output (gt-forecast-midia.json)

```json
{
  "financial_model": [{ "month": 1, "label": "Ramp-up", "budget": 0, "cpl": 0, "leads": 0, "conversion_rate": 0, "sales": 0, "revenue": 0, "roas": 0 }],
  "assumptions": ["string"],
  "scenarios": { "optimistic": {}, "realistic": {}, "pessimistic": {} },
  "platform_distribution": [{ "platform": "Meta Ads", "percentage": 0, "monthly_value": 0, "objective": "string" }],
  "funnel_distribution": [{ "phase": "Topo", "percentage": 0, "objective": "string" }],
  "timeline": [{ "month": 1, "focus": "Ramp-up", "weekly_actions": ["string"], "goal": "string" }],
  "alerts": [{ "metric": "CPL", "threshold": "> R$ X", "action": "string" }],
  "scale_criteria": [{ "metric": "ROAS", "threshold": "> Xx", "action": "string" }],
  "disclaimer": ["string"],
  "sheets_url": "string"
}
```


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do forecast de mídia: investimento total, leads projetados e ROAS esperado. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
