---
name: gt-diagnostico-maturidade-digital
description: "Analisa a maturidade digital do cliente (5 pilares: Mídia, Orgânico/SEO, Criativos, CRM, CRO) com base em dados V4MOS ou briefing. Gera score por pilar, benchmark setorial e sequência de turnaround. Use quando o operador disser 'maturidade', 'diagnóstico digital', 'score', ou na Semana 2 (POP 2.4)."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies: []
outputs: ["gt-diagnostico-maturidade-digital.json"]
week: 2
estimated_time: "30-45 min"
v4mos_integration: connectors_only
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Diagnóstico de Maturidade Digital (POP 2.4)

> **Posição no fluxo:** sintetiza os diagnósticos de mídia, orgânico e criativos em um score por pilar. Rode depois dos diagnósticos especializados e antes do posicionamento.

Você é um estrategista sênior de marketing digital. Vai analisar a maturidade digital do cliente e produzir um diagnóstico que direciona toda a priorização estratégica.

> **INTEGRAÇÃO V4MOS:** A API V4MOS disponibiliza dados de CONECTORES (integrações ativas como Meta Ads, Google Ads, etc.). Dados de diagnóstico, workspace e perfil de marketing NÃO estão disponíveis via API — são coletados no briefing e nas perguntas ao operador.

## Dados necessários

### Fonte V4MOS (conectores)
Leia `squads/{squad}/clientes/{cliente}/client.json` (seção `connectors`). Se `fetched_at` existir e não for null, extraia:
- `google_ads` → campanhas Google Ads (total_campaigns, total_cost, avg_cpa, lista de campanhas com status)
- `facebook_ads` → campanhas Meta Ads (total_campaigns, total_spend, avg_cpm, lista de campanhas)
- Quais plataformas estão conectadas = indicador de maturidade em mídia paga

Se `connectors.fetched_at` for nulo ou inexistente, use `/v4mos-dados-meta-ads` para Meta Ads. Para Google Ads, use exportações ou dados já presentes na KB. Se não houver integração, siga com briefing e evidências disponíveis, marcando claramente a limitação.

**Formato atual dos connectors:**
```json
{
  "fetched_at": "2026-04-18T15:30:00Z",
  "period": { "start": "2025-01-01", "end": "2026-04-18" },
  "google_ads": { "total_campaigns": 15, "total_cost": 13975, "avg_cpa": 11.41, "campaigns": [...] },
  "facebook_ads": { "total_campaigns": 15, "total_spend": 3472, "avg_cpm": 10.10, "campaigns": [...] }
}
```

### Fonte principal: Briefing + Operador
Leia `squads/{squad}/clientes/{cliente}/client.json (briefing)`. Extraia:
- `identification.segment` → segmento para benchmark
- `digital_situation` → situação digital declarada pelo cliente
- `accesses` → quais acessos o operador já tem

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

### Cenário A: V4MOS tem dados de conectores
Se `client.json.connectors.fetched_at` não é null, incorpore no diagnóstico:
- Período dos dados (`period.start` → `period.end`)
- Google Ads: quantas campanhas, gasto total, CPA médio, status das campanhas (ENABLED/PAUSED)
- Facebook Ads: quantas campanhas, gasto total, CPM médio, objetivos usados
- Quais plataformas estão ausentes (ex: sem Google Analytics = gap de rastreamento)

Isso dá uma visão real da maturidade — não só "tem mídia paga" mas "como está performando".

### Cenário B: Diagnóstico baseado em briefing + operador (SEMPRE executado)
O diagnóstico completo sempre usa os dados do briefing (`digital_situation`) e as seguintes informações. Se não encontrar no client.json, pergunte ao operador TUDO de uma vez:

**Mídia Paga:** plataformas usadas, investimento mensal, pixel/tag configurado, ROAS ou CPA atual
**Criativos:** criativos ativos, quem produz, frequência de atualização
**CRO (Conversão):** site/LP existente, taxa de conversão, pontos de conversão
**CRM:** CRM usado, registros de leads, automação de follow-up
**SEO:** posição no Google, blog/conteúdo indexado, Google Meu Negócio

### Output completo

Consulte `references/scoring-framework.md` para calibrar a análise. Gere:

**Resumo Executivo (máx. 3 parágrafos)**

Escreva em tom direto, sem eufemismo. Se o score é ruim, diga que é ruim e por quê.

Parágrafo 1: Score geral e o que significa na prática para o negócio. Não diga só o número — traduza em impacto: "Você está deixando X na mesa" ou "Seus concorrentes no setor Y estão [comparação]."

Parágrafo 2: Os 2 maiores gaps que estão custando resultado AGORA. Seja específico: não "melhorar mídia paga" mas "seus anúncios no Meta estão rodando sem público lookalike e o CPA está 3x acima da média do setor."

Parágrafo 3: Os 2 pontos fortes que precisam ser aproveitados/acelerados.

**Score por Pilar (tabela)**

| Pilar | Score | Classificação | Destaque |
|-------|-------|---------------|----------|
| Mídia Paga | X/100 | [Crítico/Baixo/Médio/Bom/Excelente] | [1 frase] |
| Criativos | X/100 | ... | ... |
| CRO | X/100 | ... | ... |
| CRM | X/100 | ... | ... |
| SEO | X/100 | ... | ... |
| **GERAL** | **X/100** | ... | ... |

Se não houver dados V4MOS, atribua scores estimados com base na conversa com o operador, marcando como "(estimado)" na tabela.

**Prioridades de Ação (5 ações, ranqueadas)**

Para cada ação:
1. **O que fazer** (específico e acionável)
2. **Por que é prioridade** (impacto esperado)
3. **Esforço** (baixo/médio/alto)
4. **Dependências** (o que precisa estar pronto antes)

**Benchmark do Setor**

Compare o score do cliente com a média do setor (use `references/scoring-framework.md`).
- Quais pilares estão acima da média?
- Quais estão abaixo?
- Qual o gap mais crítico vs. o setor?

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos acima, SEMPRE inclua:

- **`summary_headline`** (max 200 char) — manchete com o veredito. Ex: "[Cliente] tem 5.2/10 de maturidade digital — Mídia e CRM são os pilares que mais travam crescimento."
- **`summary_highlights`** (4-6 itens, `{category, label, value, subtext, tone}`) — para maturidade sugestões:
  - `maturidade`: score geral, pilar mais forte, pilar mais fraco
  - `posicao`: score vs benchmark do setor (gap %)
  - `oportunidade`: pilar com maior upside e retorno estimado
  - `risco`: pilar crítico que bloqueia outros
- **`summary_key_findings`** (3-5 itens, `{category, text}`) — `vantagem|contexto|ameaca|acao`.

### Ponto de alavancagem

Em diagnóstico de maturidade, o ponto de alavancagem é o **pilar mais fraco com maior impacto sistêmico** (bloqueia outros pilares ou representa o maior gap vs benchmark). Estruture em `key_insight`:
```json
"key_insight": {
  "headline": "Frase sobre o pilar-chave (ex: 'CRM em 2/10 bloqueia ROI de toda mídia paga')",
  "context": "2-3 linhas sobre cascata de efeitos",
  "numbered_reasons": ["(1) evidência do score baixo", "(2) efeito cascata", "(3) ROI de destravar"],
  "discussion_anchor": "Por que o stakeholder precisa priorizar este pilar antes dos outros"
}
```

Se o diagnóstico revelou maturidade baixa em todos os pilares (ex: score médio < 4) ou dados insuficientes, inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores?
- [ ] Resumo executivo traduz scores em impacto de negócio (não só números)?
- [ ] Prioridades são específicas e acionáveis (não "melhorar mídia")?
- [ ] Benchmark do setor está referenciado com fonte?
- [ ] Tem `summary_headline` específico?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos?
- [ ] Identificou `key_insight` (pilar-chave com efeito sistêmico)?
- [ ] Se há fragilidade geral, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "A análise condiz com o que você vê no dia a dia do cliente?"
- "As prioridades fazem sentido na ordem apresentada?"
- "Tem algum contexto que muda a priorização? (ex: cliente já fechou contrato de mídia, CRM já está em implementação)"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/gt-diagnostico-maturidade-digital.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira a próxima skill com base nas dependências e no estado da KB
   - "Diagnóstico de maturidade salvo. Fecha o bloco de diagnósticos da Semana 2; o próximo passo é o Posicionamento (geral-posicionamento-estrategico), que sintetiza tudo."
   - O score por pilar e a sequência de turnaround alimentam o posicionamento e o forecast de mídia.
