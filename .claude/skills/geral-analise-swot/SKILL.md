---
name: geral-analise-swot
description: "Análise de Concorrentes + Matriz SWOT estratégica: scorecard digital dos concorrentes (com evidência), SWOT acionável, matriz TOWS, cenários e priorização em Gantt de 90 dias. Use quando o operador disser 'SWOT', 'análise de concorrentes', 'forças e fraquezas', 'análise estratégica', ou na Semana 1."
area: geral
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
outputs: ["geral-analise-swot.json"]
week: 1
estimated_time: "1h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Análise de Concorrentes + Matriz SWOT (POP 1.5)

Você é um estrategista de negócios sênior. Vai mapear o cenário competitivo com evidência observável e gerar uma Matriz SWOT acionável que direciona a estratégia das próximas semanas.

> **Posição no fluxo:** Semana 1 (POP 1.5). Roda com base no briefing, no ICP/Persona e na pesquisa de concorrentes — **não depende** do Diagnóstico de Maturidade (que ocorre na Semana 2). Se um diagnóstico de maturidade já existir de um ciclo anterior, use como reforço; senão, ancore nos dados de briefing e na pesquisa observável.

> **REGRA DE OURO:** Cada item da SWOT deve ser específico para ESTE cliente. Se você trocar o nome da empresa e o item ainda fizer sentido para qualquer negócio do setor, está genérico demais. Refaça.

## Dados necessários

Leia os seguintes arquivos do diretório do cliente:

1. `client.json` (seção `briefing`) — dados base do cliente (OBRIGATÓRIO)
2. `outputs/geral-persona-icp.json` — ICP/Persona para cruzar concorrentes por fit, faixa de preço e geografia (OBRIGATÓRIO — é dependência)
3. `client.json` (seção `connectors`) — dados V4MOS se disponíveis
4. `outputs/gt-diagnostico-maturidade-digital.json` — scores de maturidade, **se já existir** de um ciclo anterior (opcional; normalmente só existe a partir da Semana 2)
5. `client.json` (seção `history`) — decisões anteriores relevantes

Extraia do briefing:
- `identification.name` → nome do cliente
- `identification.segment` → setor
- `identification.revenue` → faturamento (se disponível)
- `identification.years_in_market` → tempo de mercado
- `product.main_product` → produtos/serviços
- `product.differentials` → diferenciais declarados pelo cliente
- `competition.competitors` → lista de concorrentes
- `competition.differentials` → diferencial real vs concorrentes

Do diagnóstico de maturidade (SE já existir — opcional na Semana 1):
- `overall_score`, `pillar_scores`, `priorities`, `sector_benchmark` → reforçam forças/fraquezas digitais
- Se não existir ainda, derive forças/fraquezas digitais do `briefing.digital_situation` e da pesquisa observável dos canais do cliente.

Se não encontrar informações sobre concorrência no client.json, pergunte ao operador de uma vez:
- "Dos concorrentes listados, qual é o mais perigoso e por quê?"
- "Tem algum concorrente que faz algo melhor que o cliente? O quê?"
- "O cliente tem alguma vantagem que os concorrentes não conseguem copiar facilmente?"
- "Existe alguma tendência do mercado que pode impactar esse negócio nos próximos 6-12 meses?"
- "O cliente depende muito de algum canal ou fornecedor?"

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

Consulte `references/exemplos-swot-bom-vs-ruim.md` para calibrar a especificidade.

### Análise de Concorrentes (scorecard digital) — PRIMEIRO PASSO

Antes da SWOT, mapeie o cenário competitivo com **evidência observável** (não percepção). É a base factual que alimenta forças/fraquezas/ameaças.

1. **Selecione 3-5 concorrentes diretos + 1-2 indiretos/aspiracionais.** Cruze com o ICP (fit, faixa de preço, geografia) para não listar concorrente percebido que não compete de fato. Valide a lista com o operador.
2. **Scorecard digital** — pontue cada concorrente de **0-10** por dimensão, **cada nota com 1 linha de evidência observável** (link/print/fato):
   - `site`, `seo`, `midia_paga`, `social`, `gmn`, `reputacao`, `comunicacao`
   - Inclua o próprio cliente na tabela para contraste.
3. **Leitura competitiva** — onde o cliente está acima/abaixo, e qual o gap mais explorável.

Cada concorrente vira um objeto em `competitor_scorecard[]`: `{name, type: "direto|indireto", scores: {site, seo, midia_paga, social, gmn, reputacao, comunicacao}, evidence: {<dimensao>: "evidência"}, overall}`.

> Regra: nota sem evidência observável não entra. Se não conseguir evidência, marque a dimensão como `null` + motivo.

### Forças (Strengths) — 4-6 itens
Fatores INTERNOS positivos. Busque em:
- Diagnóstico digital: pilares com score acima da média do setor
- Briefing: diferenciais declarados que são REAIS (valide com dados)
- Tempo de mercado / base de clientes existente
- Equipe / expertise interna
- Localização / infraestrutura

Para cada força, inclua:
- **Título:** frase curta e específica
- **Descrição:** evidência concreta que sustenta essa força (use dados do diagnóstico quando possível)
- **Implicação estratégica:** como essa força pode ser ALAVANCADA na estratégia

### Fraquezas (Weaknesses) — 4-6 itens
Fatores INTERNOS negativos. Busque em:
- Diagnóstico digital: pilares com score abaixo da média do setor
- Gaps identificados no diagnóstico
- Limitações de equipe / budget / conhecimento
- Dependências perigosas

Para cada fraqueza:
- **Título:** frase curta e específica
- **Descrição:** evidência concreta
- **Implicação estratégica:** qual o risco se não for tratada E como mitigar

### Oportunidades (Opportunities) — 4-6 itens
Fatores EXTERNOS positivos. Busque em:
- Tendências do setor favoráveis
- Gaps dos concorrentes
- Canais não explorados
- Mudanças de comportamento do consumidor
- Tecnologia acessível (IA, automação)

Para cada oportunidade:
- **Título:** frase curta e específica
- **Descrição:** por que essa oportunidade existe AGORA
- **Implicação estratégica:** como capturar essa oportunidade

### Ameaças (Threats) — 4-6 itens
Fatores EXTERNOS negativos. Busque em:
- Concorrentes em ascensão
- Mudanças regulatórias
- Dependência de plataformas (Meta, Google, iFood, etc.)
- Mudanças de algoritmo / custos de mídia
- Saturação de mercado

Para cada ameaça:
- **Título:** frase curta e específica
- **Descrição:** evidência de que essa ameaça é real
- **Implicação estratégica:** como se proteger ou mitigar

### Síntese Estratégica (2-3 parágrafos)

Cruze os quadrantes para responder: "Qual é a jogada mais inteligente que este negócio pode fazer AGORA?"

Parágrafo 1: **Forças + Oportunidades (Alavancagem)** — Como usar as forças para capturar as oportunidades? Esta é a aposta principal.

Parágrafo 2: **Fraquezas + Ameaças (Proteção)** — Quais fraquezas, se não tratadas, vão amplificar as ameaças? Este é o risco principal.

Parágrafo 3: **Estratégia recomendada** — Em 1 parágrafo, o que esse negócio deve priorizar nos próximos 90 dias.

### Matriz TOWS (OBRIGATÓRIA — cruzamento estratégico)

Derive estratégias específicas cruzando os quadrantes. Não é redundância da SWOT — é onde a análise vira ação. Gere 2-3 estratégias por célula:

- **SO (Forças × Oportunidades) — Estratégias Ofensivas:** use a força X para capturar a oportunidade Y. Onde o cliente ATACA.
- **WO (Fraquezas × Oportunidades) — Estratégias de Reforço:** como eliminar a fraqueza X para não perder a oportunidade Y. Onde o cliente INVESTE.
- **ST (Forças × Ameaças) — Estratégias Defensivas:** use a força X para neutralizar a ameaça Y. Onde o cliente PROTEGE.
- **WT (Fraquezas × Ameaças) — Estratégias de Sobrevivência:** o pior cenário. O que fazer para reduzir a fraqueza X que se amplifica com a ameaça Y. Onde o cliente MINIMIZA DANO.

Para cada estratégia: `id` (ex: SO1, WT2), `strategy` (ação), `rationale` (por que funciona), `expected_outcome` (o que muda se executar).

### Ações Prioritárias (5-7 ações) — com risk-adjusted scoring

Derive ações concretas da SWOT/TOWS. Para cada:
1. **Ação** — o que fazer (específico)
2. **Base SWOT** — quais quadrantes/estratégias TOWS essa ação endereça (ex: "Alavanca F2, captura O3, executa SO1")
3. **Impacto** — alto/médio/baixo
4. **Prazo sugerido** — semana 1/2/3 da estruturação
5. **Financial impact** — objeto com `investment` (R$) + `expected_return_90d` (R$) + `payback_days` + `roi_multiple`. Campos alternativos aceitos: `investment_brl`, `monthly_return_brl` (×3 dá o 90d), `note`.
6. **Risk-adjusted score** — pode ser NÚMERO 0-100 **ou** OBJETO com dimensões 1-10:
   ```json
   {"impact": 9, "probability_of_success": 8, "reversibility": 7, "score": 8.2}
   ```
   Use o objeto quando o score for derivado de múltiplas dimensões (mais transparente). O campo `score` é obrigatório.
7. **Dependência** — se depende de alguma outra ação ou skill

Ordene as ações por risk_adjusted_score (maior primeiro).

> **NÃO GERE:** os campos `scenarios` e `financial_summary_90d` foram removidos do schema — o renderer do portal não os exibe mais. Projeções de cenários vivem em `gt-diagnostico-midia-paga` (budget_reallocation_scenarios). A consolidação financeira é redundante com `priority_actions[].financial_impact`, que o portal já agrega.

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos acima, SEMPRE inclua:

- **`summary_headline`** (max 200 char) — manchete com o veredito da SWOT. Ex: "[Cliente] tem know-how técnico raro (certificação X), mas mídia zerada — janela SO de 12 meses antes de novo entrante."
- **`summary_highlights`** (4-6 itens, `{category, label, value, subtext, tone}`) — para SWOT sugestões:
  - `posicao`: score SWOT líquido, nº de forças vs fraquezas
  - `oportunidade`: top priority action com ROI projetado, payback
  - `risco`: ameaça de maior impacto
  - `janela`: tempo até janela fechar / urgência
- **`summary_key_findings`** (3-5 itens, `{category, text}`) — `vantagem|contexto|ameaca|acao` — cubra pelo menos 3 dos 4.

### Ponto de alavancagem

Em SWOT, o ponto de alavancagem é a **combinação Força × Oportunidade mais assimétrica** (quadrante SO com maior risk_adjusted_score). Estruture em `key_insight`:
```json
"key_insight": {
  "headline": "Cruzamento F×O em 1 frase (pode virar quote)",
  "context": "2-3 linhas sobre por que esta combinação é única",
  "numbered_reasons": ["(1) força específica...", "(2) oportunidade específica...", "(3) timing/janela..."],
  "discussion_anchor": "Por que o stakeholder precisa decidir sobre apetite e ritmo"
}
```

Se SWOT revelou fragilidade estrutural (mais ameaças que forças, ausência de diferencial real), inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] `competitor_scorecard` tem 3-5 diretos (+ indiretos), notas 0-10 e **evidência observável** por nota (não percepção)?
- [ ] Concorrentes validados por fit/ICP (não listou percebido que não compete)?
- [ ] Cada item da SWOT é específico — se trocar o nome da empresa, NÃO serve para outro negócio do setor?
- [ ] Síntese cruza quadrantes (não é apenas resumo)?
- [ ] Ações derivam dos quadrantes (referência F/W/O/T explícita)?
- [ ] Matriz TOWS tem pelo menos 2 estratégias por célula (SO, WO, ST, WT)?
- [ ] Cada priority_action tem `financial_impact` (investment, return, payback, ROI) e `risk_adjusted_score`?
- [ ] Priority_actions estão ORDENADAS por risk_adjusted_score (maior primeiro)?
- [ ] NÃO gerou `scenarios` nem `financial_summary_90d` (removidos do schema)?
- [ ] Tem `summary_headline` específico?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos?
- [ ] Identificou `key_insight` (cruzamento SO mais assimétrico) para stakeholder?
- [ ] Se há fragilidade estrutural, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador em formato visual claro (tabela ou lista organizada por quadrante).

Revise o output. O que está errado, exagerado ou faltando?

- "Algum item está genérico demais? (lembre: se serve pra qualquer empresa do setor, está genérico)"
- "Falta alguma força ou fraqueza que você enxerga no dia a dia?"
- "Alguma oportunidade ou ameaça que eu não considerei?"
- "A síntese captura a essência do que o cliente precisa fazer?"
- "As ações fazem sentido no contexto do que será trabalhado nas próximas semanas?"
- "Quer ajustar a priorização?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/geral-analise-swot.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "SWOT salva. Este output será usado pela skill geral-posicionamento-estrategico (semana 2) e como referência para todas as skills de produção."
   - Sugira a próxima skill da semana 1 (account-auditoria-comunicacao ou geral-persona-icp se ainda não feita)
