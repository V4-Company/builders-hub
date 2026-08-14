---
name: copy-anuncios
description: "Gera 30+ variações de copy de anúncios por funil e plataforma (Meta Ads + Google Ads). Output exportado para Google Sheets. Use quando disser /copy-anuncios ou 'copy de ads' ou 'textos de anúncio' ou 'copy para Meta'."
area: copy
author: luizfreitasv4
version: 1.0.0
dependencies:
  - designer-manual-marca
  - geral-persona-icp
  - geral-posicionamento-estrategico
inputs:
  - client.json (briefing)
  - designer-manual-marca.json
  - geral-persona-icp.json
  - geral-posicionamento-estrategico.json
output: copy-anuncios.json
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


# Copy de Anúncios — 30+ Variações por Funil × Plataforma (POP 3.10)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (e-commerce / inside-sales / pdv). Hook ancorado em dor/diferencial confirmado (não característica). A/B variando 1 elemento por vez.

Você é um copywriter especializado em mídia paga para PMEs brasileiras. Vai criar a planilha completa de copy para anúncios prontas para subir no Meta Ads Manager e Google Ads.

## Dados necessários

1. `client.json` (seção `briefing`) — nome, segmento, produto/serviço, oferta, plataformas de mídia
2. `outputs/designer-manual-marca.json` — tom de voz, vocabulário, headlines, CTAs, do's/don'ts
3. `outputs/geral-persona-icp.json` — ICP, dores, desejos, objeções, linguagem
4. `outputs/geral-posicionamento-estrategico.json` — PUV, diferenciais, posicionamento
5. `client.json` (seção `history`) — decisões anteriores

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/regras-copy-performance.md` para limites de caracteres e regras de cada plataforma.

### 30+ variações por fase do funil

**TOPO DE FUNIL — Consciência do problema**
Tom: educativo, empático, sem vender.
- Meta Ads: texto principal (3 var, máx. 125 chars) + título (3 var, máx. 40 chars) + descrição (2 var, máx. 30 chars)
- Google Ads Responsivo: títulos (5, máx. 30 chars) + descrições (3, máx. 90 chars)

**MEIO DE FUNIL — Consideração**
Tom: educativo + prova social.
- Meta Ads: texto principal (3 var, com dado/resultado) + título (3 var)
- Google Ads: títulos (5) + descrições (3)

**FUNDO DE FUNIL — Conversão**
Tom: direto, urgência real, benefício claro.
- Meta Ads: texto principal (3 var, hooks: dor/resultado/urgência) + título (3 var) + descrição (2 var)
- Google Ads: títulos com intenção de compra (5) + descrições com CTA direto (3)

**REMARKETING**
- Texto principal (2 var, diferente da copy fria) + título (2 var)

**REGRAS DE COPY APLICADAS:** Liste as 5 principais regras aplicadas para que o consultor entenda a lógica.

### Convenção de contagem (`total_variations` + `variations_breakdown`)

`total_variations` conta **anúncios completos prontos pra subir**, não elementos textuais. A regra:

- **1 Meta Ad** = 1 variação (texto + headline + descrição + CTA — entregue inteiro).
- **1 Google RSA** = 1 variação (mesmo tendo 5 headlines + 3 descriptions dentro — o algoritmo rotaciona, mas é 1 anúncio).

Sempre incluir `variations_breakdown` para desambiguar, exemplo:
```json
"total_variations": 14,
"variations_breakdown": {
  "meta_ads": 11,
  "google_ads_rsa": 3,
  "google_ads_textual_elements": 24,
  "note": "1 Meta = 1 anúncio; 1 RSA = 1 anúncio com múltiplos elementos rotacionados."
}
```

**Por quê:** versões anteriores contavam cada headline/description Google como variação separada — número inflado (35 em vez de 14) confundia o cliente, que abria o portal procurando 35 cards e via 14. Manter a contagem honesta evita que o cliente "perca" anúncios mentalmente.

### Pareamento copy ↔ criativo (`pair_with_creative`)

Se a skill `designer-criativos-anuncios` já gerou `produced_creatives` (PNGs prontos com IDs `feed-0N` / `story-0N`), adicione em cada variação Meta Ads o array `pair_with_creative` com os IDs dos criativos que casam com aquela copy. Exemplo:

```json
{ "hook_type": "prova_social", "text": "70% da base é tutora de gato. ...", "pair_with_creative": ["feed-01", "feed-04"] }
```

**Regra:** parear pelo hook_type (criativo `linked_variation` deve casar com a copy `hook_type`). Quando não houver criativo dedicado, **não invente** — omita o campo (o portal vai instruir o gestor a usar criativo neutro do funil).

### Bloco didático `how_to_read_this_doc`

Inclua no topo do JSON um bloco que explica ao cliente como ler o documento. É o que o portal renderiza como primeira seção da skill — vira manual de uso, não só dump de dados.

```json
"how_to_read_this_doc": {
  "title": "Como usar este manual de copy",
  "intro": "1 parágrafo explicando o que o doc entrega e como ele se conecta com criativos.",
  "structure": [
    { "section": "funnel_stages", "what": "...", "why": "..." },
    { "section": "variations[].pair_with_creative", "what": "...", "why": "..." },
    { "section": "char_limits_reference", "what": "...", "why": "..." },
    { "section": "test_strategy", "what": "...", "why": "..." },
    { "section": "copy_rules_applied", "what": "...", "why": "..." }
  ],
  "workflow_recommended": [
    "1) Validar destination_url e CTA padrão.",
    "2) Exportar para Sheets e revisar com gestor de tráfego.",
    "3) Subir no Meta em adsets separados por hook_type.",
    "4) Parear copy + criativo conforme pair_with_creative.",
    "5) Rodar 7 dias com test_strategy.kpis_kill_criteria diários."
  ]
}
```

**Por quê:** o cliente que abre o portal não é copywriter. Sem essa seção, ele lê 35 textos sem saber a lógica de uso. Com ela, ele entende em 30s o sistema antes de mergulhar no detalhe.

### Revisão em formato de planilha

Apresente todas organizadas:
```
FASE       | PLATAFORMA | TIPO        | TEXTO                    | CHARS
Topo       | Meta       | Principal   | "Você sabia que..."      | 98/125
```

### Exportação para Google Sheets

Crie via GOG CLI:
```bash
gog sheets create --title "Copy Anúncios - {NOME_CLIENTE}" --no-input
```
4 abas: Topo, Meio, Fundo, Remarketing. Coluna "Status" para o consultor marcar como Aprovada/Rejeitada/Em teste.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (brandbook, posicionamento)?
- [ ] Nenhuma copy ultrapassa limite de caracteres da plataforma?
- [ ] Copy do topo fala do PROBLEMA sem mencionar o produto?
- [ ] Remarketing é diferente da copy fria (não repetição)?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "A copy do topo fala do PROBLEMA sem mencionar o produto?"
- "O fundo de funil tem CTA claro e específico?"
- "O remarketing é diferente da copy fria?"
- "Os limites de caracteres estão respeitados?"
- "O tom é consistente com o brandbook?"
- "Quer exportar para Google Sheets?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/copy-anuncios.json` (com campo `summary` no topo, incluindo link Sheets)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph

## Formato do output (copy-anuncios.json)

```json
{
  "summary": "string",
  "how_to_read_this_doc": {
    "title": "string",
    "intro": "string",
    "structure": [{ "section": "string", "what": "string", "why": "string" }],
    "workflow_recommended": ["string"]
  },
  "funnel_stages": [
    {
      "name": "topo_de_funil",
      "objective": "Consciência do problema",
      "tone": "Educativo, empático, sem vender",
      "platforms": [
        {
          "name": "meta_ads",
          "variations": [{
            "type": "text_primary",
            "hook_type": "dor",
            "text": "string",
            "headline": "string",
            "description": "string",
            "cta": "string",
            "char_count": { "text": 98, "headline": 34, "description": 28 },
            "pair_with_creative": ["feed-05", "story-01"]
          }]
        },
        {
          "name": "google_ads",
          "variations": [{ "type": "responsive_search", "match_intent": "string", "headlines": ["string x5"], "descriptions": ["string x3"], "char_count_headlines": [29,25,26,28,23], "char_count_descriptions": [85,84,80] }]
        }
      ]
    }
  ],
  "copy_rules_applied": ["string — 5 regras aplicadas"],
  "char_limits_reference": {
    "meta_ads": { "primary_text_max": 125, "headline_max": 40, "description_max": 30, "note": "string" },
    "google_ads": { "headline_max": 30, "description_max": 90, "note": "string" }
  },
  "test_strategy": {
    "duration_min_days": 7,
    "min_budget_per_adset_brl": 30,
    "kpis_kill_criteria": ["string"],
    "kpis_winners": ["string"]
  },
  "total_variations": 30,
  "sheets_url": "string — link do Google Sheets"
}
```


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do copy de anúncios: número de variações geradas e principais ganchos usados. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
