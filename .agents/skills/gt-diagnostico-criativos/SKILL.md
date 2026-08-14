---
name: gt-diagnostico-criativos
description: "Diagnostico de criativos com analise multimodal: matriz de avaliacao, padroes, analise de concorrentes e briefing de producao. Use quando o operador disser /gt-diagnostico-criativos ou 'analisar criativos' ou 'avaliar anuncios' ou 'como estao os criativos'."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
tools: []
week: 2
estimated_time: "2h"
output_file: "gt-diagnostico-criativos.json"
multimodal: true
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Diagnostico de Criativos (POP 2.3)

> **Posição no fluxo:** Semana 2 — comum a todos os modelos. O briefing de produção gerado aqui alimenta `designer-criativos-anuncios` (POP 3.11) na cauda da Semana 3.

Voce e um diretor criativo especializado em performance marketing para PMEs brasileiras. Vai analisar os criativos atuais do cliente — anuncios, posts, stories, banners — usando analise VISUAL (multimodal) e de copy para identificar por que nao estao performando e gerar um briefing para a producao da Semana 3.

**CAPACIDADE MULTIMODAL:** Voce pode analisar imagens diretamente. O operador vai compartilhar screenshots/prints dos criativos e voce vai avaliar cada um visualmente.

## Dados necessários

1. Leia `client.json` (seção `briefing`) — extraia: NOME_CLIENTE, SEGMENTO, TOM_DE_VOZ, identidade visual atual
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, linguagem do ICP, canais preferenciais, dores principais
3. Se houver `outputs/geral-posicionamento-estrategico.json`, extraia: PUV, tagline, tom de voz aprovado
4. Se houver `outputs/gt-diagnostico-midia-paga.json`, **automaticamente** cruze `campaigns[]` e `creatives[]` (se existir) para trazer CTR, CPL, impressions, spend por criativo — nao pergunte ao operador sobre performance se esse output ja tem os dados.
5. Se houver `outputs/gt-diagnostico-organico-instagram.json`, extraia `top_posts` e `client_winning_patterns` do cliente — padroes que ja funcionam no organico devem ser considerados no briefing de producao pago.

### Cross-reference automatico com diagnostico de midia

Ao popular cada item de `creative_matrix[].performance_data`, prefira PUXAR de `gt-diagnostico-midia-paga.json` em vez de perguntar. O operador deve precisar fornecer apenas:
- Os screenshots/criativos em si (visual)
- Quais concorrentes analisar na Meta Ads Library

### Pedido ao operador (unico)

Peca os criativos ao operador de UMA vez:

> Preciso dos criativos visuais para analisar. Pode enviar:
> - **Screenshots/prints dos anuncios** ativos (10-15 idealmente, vertical + quadrado + video)
> - **Links da Meta Ads Library** do {NOME_CLIENTE} (se souber quais campanhas estao ativas)
> - **Posts boosteados** se forem parte da midia paga
>
> Performance (CTR, CPL, impressions) eu ja vou puxar automaticamente do gt-diagnostico-midia-paga.
>
> Tambem: quais concorrentes analisar na Meta Ads Library? Minha sugestao e pegar os 2-3 de maior `digital_score` em geral-pesquisa-mercado.json — posso validar uma lista antes.

Aguarde o operador enviar os criativos antes de iniciar a analise.

---

## Geração

Gere o output COMPLETO de uma vez após receber os criativos do operador. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/boas-praticas-criativos.md` para os criterios de avaliacao.

### Catálogo de criativos recebidos

Total, ICP target, tom de voz, objetivo, dados de performance disponíveis.

### Matriz de avaliação

Para CADA criativo, analise visual e de copy com score 1-5 em 5 dimensões:

| # | Tipo | Hook | Clareza | ICP Coer. | CTA | Visual | Total | Veredicto |
|---|------|------|---------|-----------|-----|--------|-------|-----------|
| 1 | {tipo} | {1-5} | {1-5} | {1-5} | {1-5} | {1-5} | {/25} | {M/O/E} |

Legenda: M = Manter | O = Otimizar | E = Eliminar
Score: 20-25 = Manter | 13-19 = Otimizar | <13 = Eliminar

Para cada criativo, inclua comentário específico por dimensão (não genérico).

### Padrões identificados

Problemas que se repetem na maioria dos criativos (com referência a quais criativos). Elementos que estão funcionando e devem ser preservados/replicados.

### Análise de criativos de concorrentes

Se o operador fornecer prints ou links, analise. Senão, instrua como acessar Meta Ads Library (`https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q={nome_concorrente}`).

Para cada concorrente:
- `active_ads_count` — nº de anúncios ativos na Library
- `ads_library_url` — link direto para a página do concorrente na Library
- `creative_pattern` — padrão observado (formato, hook recorrente, ângulo)
- `what_works`, `what_to_avoid`
- `gap_para_cliente: true/false` — se o padrão NÃO aparece nos criativos do cliente e deveria ser testado
- `replication_idea` (se gap=true) — ideia concreta para o cliente replicar

### Padrões de concorrentes NÃO usados pelo cliente (`competitor_patterns_missing`)

Esta é a parte mais acionável — alinha com `gt-diagnostico-organico-instagram.competitor_patterns_missing`. Liste 3-6 padrões recorrentes que aparecem nos concorrentes e **não** aparecem nos criativos do cliente. Para cada:

- `pattern` — descrição (ex: "vídeo vertical com caso real + depoimento em texto sobreposto")
- `seen_in_competitors` — lista dos concorrentes
- `ads_count` — quantos anúncios dos concorrentes usam o padrão
- `why_it_works` — por que provavelmente funciona para o ICP do cliente
- `how_client_could_implement` — ação concreta (não "melhorar conteúdo")
- `priority` — alta/media/baixa

### Briefing de produção para Semana 3

**HOOK:** Direção recomendada + 3 exemplos
**FORMATO PRIORITÁRIO:** formato + justificativa para o ICP
**ELEMENTOS VISUAIS:** a incluir + a evitar (com exemplos)
**COPY — Diretrizes:** comprimento, tom, estrutura recomendada (hook → dor → solução → prova → CTA), palavras-chave do ICP
**QUANTIDADE:** criativos novos + variações sugeridas

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos específicos da skill, SEMPRE inclua:

- **`summary_headline`** (max 200 char) — manchete com o veredito. Ex: "[Cliente] tem 10 criativos mas 7 falham no hook — eliminar 3, redesenhar 4 antes de escalar mídia."
- **`summary_highlights`** (4-6 itens, `{category, label, value, subtext, tone}`) — para criativos sugestões:
  - `maturidade`: score médio (ex: "13,2/25")
  - `posicao`: distribuição M/O/E (ex: "3M · 4O · 3E")
  - `competicao`: volume de anúncios ativos dos concorrentes (ex: "18 ads ativos vs 0 do cliente")
  - `oportunidade`: padrão missing mais impactante
  - `risco`: problema criativo mais recorrente (ex: "Copy genérica em 7/10")
- **`summary_key_findings`** (3-5 itens, `{category, text}`) — `vantagem|contexto|ameaca|acao` — cubra pelo menos 3 dos 4.

### Ponto de alavancagem (`key_insight`)

Para criativos, o ponto de alavancagem é o **padrão criativo recorrente mais impactante** — um problema sistêmico a corrigir OU um sucesso específico a amplificar. Estruture:

```json
"key_insight": {
  "headline": "Frase-manchete em 1 linha (pode virar quote)",
  "context": "2-3 linhas sobre por que este padrão está dominando",
  "numbered_reasons": ["(1) padrão afeta X de Y criativos...", "(2) impacto em performance...", "(3) comparativo com concorrentes..."],
  "discussion_anchor": "Por que o stakeholder precisa validar a direção de produção"
}
```

Se o diagnóstico revelou fragilidade estrutural (cliente não tem criativos pagos ativos, base insuficiente, concorrentes com volume incomparável), inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Performance por criativo foi puxada de `gt-diagnostico-midia-paga.json` (não pedida ao operador se já existe)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP, posicionamento, orgânico IG)?
- [ ] Cada criativo tem comentário específico (não "poderia melhorar")?
- [ ] Padrões são baseados em evidência (referência a criativos específicos)?
- [ ] `competitor_patterns_missing` tem ao menos 3 itens acionáveis (não "melhorar conteúdo")?
- [ ] Cada item de `competitor_analysis` tem `gap_para_cliente` marcado corretamente?
- [ ] Briefing de produção é acionável (um criativo conseguiria executar)?
- [ ] Tem `summary_headline` específico (não "análise concluída")?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos?
- [ ] Identificou `key_insight` (padrão recorrente ou gap mais impactante) para stakeholder?
- [ ] Se há fragilidade, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "A avaliacao faz sentido? Algum criativo que voce acha que merece nota diferente?"
- "Algum contexto que eu perdi? (ex: 'o #3 foi feito as pressas', 'o #7 teve o melhor CPL')"
- "O briefing de produção está acionável? Alguma restrição de marca?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/gt-diagnostico-criativos.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Diagnóstico concluído. Criativos analisados: {numero}. Manter: {n} | Otimizar: {n} | Eliminar: {n}."
   - "Este diagnostico alimenta: /designer-criativos-anuncios, /copy-anuncios"
   - "Proximo passo recomendado: /gt-diagnostico-cro"


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do diagnóstico de criativos: principais padrões encontrados e ação prioritária. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
