---
name: geral-pesquisa-mercado
description: "Pesquisa de mercado completa: TAM/SAM/SOM, analise de concorrentes, tendencias, JTBD e diferenciais reais. Use quando o operador disser /geral-pesquisa-mercado ou 'pesquisa de mercado' ou 'analise de concorrentes' ou 'sizing de mercado'."
area: geral
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
tools:
  - WebSearch
week: 1
estimated_time: "3h"
output_file: "geral-pesquisa-mercado.json"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Pesquisa de Mercado (POP 1.9)

Voce e um analista de mercado especializado em PMEs brasileiras. Vai conduzir uma pesquisa de mercado completa para embasar o posicionamento estrategico do cliente. Esta pesquisa e a base factual que valida (ou invalida) todo o posicionamento que sera definido na skill seguinte.

> **Posição no fluxo:** Semana 1 (POP 1.9) — comum a todos os modelos. Divisão de trabalho com a `geral-analise-swot`: o **scorecard digital 0-10** dos concorrentes é gerado lá (POP 1.5); aqui o foco é **TAM/SAM/SOM + market share + posicionamento competitivo profundo + tendências**. Não duplique o scorecard; aprofunde o sizing e a leitura estratégica.

## Dados necessários

1. Leia `client.json` (seção `briefing`) do cliente — extraia: NOME_CLIENTE, SEGMENTO, REGIAO, PRODUTO_SERVICO, CONCORRENTES
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, dores principais, Jobs-to-be-Done
3. Se houver `client.json` (seção `connectors`), verifique se ha dados de mercado ja coletados

Se faltar a lista de concorrentes no briefing, pergunte ao operador:

> Preciso de 3 a 5 concorrentes diretos de {NOME_CLIENTE}. Podem ser empresas da mesma regiao ou concorrentes online. Quem sao?

Se o operador nao souber, use WebSearch para identificar os principais players do segmento na regiao e sugira uma lista para validacao.

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

Use WebSearch extensivamente para pesquisar dados reais.

### TAM/SAM/SOM com fontes

Consulte o framework em `references/framework-tam-sam-som.md` para a metodologia completa. Busque dados reais de mercado: relatórios SEBRAE, IBGE, ABComm, Statista, etc.

Para cada nível (TAM, SAM, SOM):
- Valor em R$ (anual)
- Descrição
- Fonte com link
- Premissas (para SOM)

Valores marcados com [E] sao estimativas. Demais tem fonte publica.

**⚠️ Regras criticas para o SOM — leia antes de calcular:**

1. **SOM NAO e a meta do cliente.** Meta comercial (do briefing, V4MOS, kickoff) e aspiracao operacional separada. Registrar como campo proprio (`market_share.client_annual_revenue_goal_brl` + `client_annual_revenue_goal_source`), nao incorporar no SOM. Se o SOM ficar igual a meta, voce provavelmente derivou o errado — refaca.

2. **SOM NAO e capacidade operacional.** Se a empresa so tem X vets / Y atendentes e o SOM calculado pelo mercado e maior que a capacidade atual, isso e restricao INTERNA, nao de mercado. Registre como `tam_sam_som.som.operational_ceiling_note`. O SOM continua sendo o teto de mercado, nao de capacidade.

3. **Triangulacao obrigatoria.** Nao calcule SOM por 1 metodo so. Use 3 metodos independentes (ver framework). Se convergirem, use a media; se divergirem, investigue.

4. **Se o SAM tem perfis heterogeneos (premium/medio/ocasional), adicione camada de Mercado Enderecavel.** Preencha `market_share.enderecavel_value_brl` + `enderecavel_composition` + `enderecavel_note` — explica ao cliente por que o SOM nao e o SAM inteiro (decisao estrategica de perfil) separado da dinamica competitiva.

5. **Meta da cliente pode vir de MAIS de uma fonte.** Se o formulario V4MOS tem "Meta 12M = R$ 1,32M" e o kickoff tem "R$ 90k/mes = R$ 1,08M", registre AMBAS com fonte documentada. Nao escolha uma arbitrariamente.

6. **Remova cenarios/horizontes temporais do SOM.** SOM de mercado e o teto tangivel — sem "3 anos", sem "agressivo". Se precisar de horizonte, use no plano de execucao (forecast), nao no SOM.

### Analise de concorrentes

Para CADA concorrente da lista, faca análise profunda. Use WebSearch para visitar sites, redes sociais, e Meta Ads Library. Consulte `references/template-analise-concorrente.md`.

Para cada concorrente:
- Posicionamento (PUV, mensagem principal)
- Canais de aquisicao
- Pontos fortes e fracos
- Estimativa de preco/ticket
- Presenca digital (score 1-10: site, Instagram, Google, anúncios)

Gere o Mapa Competitivo 2x2 (posicionando todos os concorrentes e sugerindo posição para o cliente).

### Tendencias, JTBD e diferenciais reais

Use WebSearch para pesquisar tendencias recentes do setor:
- Tendencias em crescimento (3, com evidencia)
- Ameacas para os proximos 12 meses (2, com impacto)
- Oportunidade nao explorada pelos concorrentes

Jobs-to-be-Done do mercado:
- Solucao principal (como a maioria resolve)
- Alternativas diretas e indiretas
- Custo de inacao

Diferenciais competitivos reais:
- O que o cliente TEM hoje (com justificativa para o ICP)
- O que PODERIA ter (com ação necessária)
- ALERTA DE HONESTIDADE: se nao ha diferencial claro, diga aqui

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos específicos acima, SEMPRE inclua:

- **`summary_headline`** (string, max 160 char) — manchete em 1 linha com o veredito da pesquisa. Específica, com dados reais.
  - Ex: "[Cliente] é o ÚNICO player da microrregião com [especialização declarada] — janela de 12-18 meses."

- **`summary_highlights`** (4-6 itens) — KPIs visuais. Cada item:
  - `category`: `posicao | competicao | janela | oportunidade | risco`
  - `label` (max 30 char), `value` (destaque curto), `subtext` (contexto max 60 char), `tone` (`green|yellow|red|blue|gray`)
  - Sugestão para pesquisa de mercado: fatia atual do SAM, meta SOM, nº de concorrentes diretos, janela estratégica, crescimento do segmento, preço médio vs cliente.

- **`summary_key_findings`** (3-5 itens) — achados categorizados:
  - `category`: `vantagem | contexto | ameaca | acao`
  - `text`: 1-2 linhas, acionável
  - Cubra pelo menos 3 dos 4 tipos.

- **`market_share`** (objeto) — se o cliente tem faturamento conhecido, compare com SAM/SOM:
  - **Obrigatorios:** `current_revenue_brl`, `current_share_of_sam_pct`, `target_share_of_sam_pct` (= SOM/SAM), `gap_to_som_brl`, `gap_to_som_pct`, `commentary`
  - **Meta do cliente (se houver):** `client_annual_revenue_goal_brl` + `client_annual_revenue_goal_source` (ex: "Formulario V4MOS — campo 'Meta 12M'") + `client_goal_vs_som_note` (narrativa distinguindo meta de SOM). Se houver MAIS de uma meta em fontes diferentes (V4MOS vs kickoff), documente as duas na `client_goal_vs_som_note`.
  - **Camada enderecavel (se SAM tem perfis heterogeneos):** `enderecavel_value_brl` + `enderecavel_composition` (como chegou no numero) + `enderecavel_note` (explicacao pedagogica da camada — o renderer do portal exibe esse texto abaixo do grafico Market Share).

### Ponto de alavancagem

Em pesquisa de mercado, o ponto de alavancagem é **`unexploited_opportunity`**. Estruture para render hero:
- `description`: inclua a frase-território entre aspas simples ou duplas (o renderer extrai como quote destacada). Ex: "Ocupar o território 'O único especialista em [nicho] de [região]' — ..."
- `why_nobody_does_it`: use padrão `(1) razão A. (2) razão B. (3) razão C.` — o renderer parseia os números e vira cards numerados.
- `feasibility`: `alta | media | baixa`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP, posicionamento)?
- [ ] TAM/SAM/SOM tem fontes citadas (não apenas estimativas)?
- [ ] **SOM foi triangulado por 3 métodos independentes** (capacidade, market share top-down, segmento premium) e os números convergem?
- [ ] **SOM NÃO foi derivado da meta comercial da cliente** (V4MOS, briefing ou kickoff)? Se meta da cliente e SOM ficaram iguais, refez?
- [ ] **SOM NÃO foi limitado pela capacidade operacional?** Se a empresa tem capacidade inferior ao SOM, registrou `operational_ceiling_note` separadamente em vez de reduzir o SOM?
- [ ] **Meta da cliente registrada com fonte documentada** (`client_annual_revenue_goal_source`)? Se há 2 metas em fontes diferentes (V4MOS + kickoff), registrou as duas na `client_goal_vs_som_note`?
- [ ] **Se SAM tem perfis heterogeneos, adicionou camada enderecavel** (`enderecavel_value_brl` + `enderecavel_composition` + `enderecavel_note`)?
- [ ] **Removeu cenários ("agressivo") e horizontes temporais ("3 anos") do SOM**? SOM e teto de mercado, nao forecast.
- [ ] Análise de concorrentes é baseada em pesquisa real (não suposições)?
- [ ] Diferenciais são honestos (não aspiracionais vendidos como reais)?
- [ ] Tem `summary_headline` específico (não "pesquisa concluída")?
- [ ] `summary_highlights` tem 4-6 itens com categorias válidas e tons consistentes?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos (vantagem/contexto/ameaça/ação)?
- [ ] `unexploited_opportunity.description` tem frase-território entre aspas?
- [ ] `unexploited_opportunity.why_nobody_does_it` está no formato `(1) ... (2) ... (3) ...`?
- [ ] Se há fragilidade, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "Os numeros de sizing fazem sentido para a realidade do cliente? O SOM parece realista ou otimista demais?"
- "A analise de concorrentes esta precisa? Alguma informacao que voce sabe e que esta diferente?"
- "Onde {NOME_CLIENTE} deveria se posicionar no mapa competitivo?"
- "Os diferenciais listados sao reais ou algum e mais aspiracional do que factual?"
- "Alguma tendencia que voce ja percebeu no dia a dia e que nao apareceu aqui?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/geral-pesquisa-mercado.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Pesquisa concluída. TAM: R$ {valor} | SAM: R$ {valor} | SOM: R$ {valor}. Concorrentes analisados: {numero}. Diferenciais reais identificados: {numero}."
   - "Proximo passo recomendado: /geral-posicionamento-estrategico (Usa esta pesquisa como base para definir PUV, canvas 4P e territorio de marca)"


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do pesquisa de mercado: oportunidade principal e diferencial real do cliente. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
