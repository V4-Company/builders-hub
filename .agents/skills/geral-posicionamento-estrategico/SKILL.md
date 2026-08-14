---
name: geral-posicionamento-estrategico
description: "Canvas de posicionamento estrategico completo: PUV, 4Ps, territorio de marca e taglines. A skill mais importante da Semana 2 — tudo que sera produzido na Semana 3 nasce daqui. Use quando o operador disser /geral-posicionamento-estrategico ou 'definir posicionamento' ou 'PUV' ou 'proposta de valor' ou 'canvas de posicionamento'."
area: geral
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-pesquisa-mercado
  - geral-persona-icp
  - geral-analise-swot
tools: []
week: 2
estimated_time: "2.5h"
output_file: "geral-posicionamento-estrategico.json"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Canvas de Posicionamento Estrategico (POP 2.5)

> **Posição no fluxo:** Semana 2 — síntese final, comum a todos os modelos. Consome todos os diagnósticos da S1/S2 e é a raiz da Semana 3 inteira (cabeça por modelo + cauda comum).

Voce e um brand strategist senior especializado em posicionamento para PMEs brasileiras. Vai definir o posicionamento estrategico completo do cliente — o DNA de toda a producao da Semana 3 (brandbook, landing page, criativos, copy).

**IMPORTANCIA:** Esta e a skill mais critica do processo. Se o posicionamento for generico, TUDO que vier depois sera generico. Se for afiado e verdadeiro, toda a producao ganha forca.

## Dados necessários

1. Leia `client.json` (seção `briefing`) — extraia: NOME_CLIENTE, SEGMENTO, PRODUTO_SERVICO, marca_valores
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, dores, desejos, linguagem, Jobs-to-be-Done
3. Leia `outputs/geral-pesquisa-mercado.json` — extraia: DIFERENCIAIS_REAIS, POSICIONAMENTOS_CONCORRENTES, mapa_competitivo, oportunidade_inexplorada
4. Leia `outputs/geral-analise-swot.json` — extraia: RESUMO_SWOT (forcas + oportunidades prioritarias)

Se algum input critico estiver faltando, alerte o operador e sugira completar a dependencia primeiro.

Antes de gerar, confirme com o operador a direcao estrategica (se não encontrar estas informações no client.json):
- "Diferencial mais forte que voce sente no dia a dia — dos que mapeamos, qual o cliente elogia mais?"
- "Onde quer estar no mapa competitivo? O espaco vazio identificado faz sentido?"
- "Restricao de posicionamento — algo que o cliente NAO quer ser associado?"
- "Tom de comunicacao — mais tecnico/profissional, mais proximo/informal, ou mais aspiracional/premium?"

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

### Mapa de posicionamento 2x2

Posicione concorrentes e a posição recomendada para o cliente num mapa com eixos estratégicos (ex: Generalista → Especialista × Acessível → Premium). Justifique a posição recomendada.

### 3 Declarações de posicionamento

Gere 3 opções com direções diferentes usando o formato clássico:
> "Para **[ICP]**, **{NOME_CLIENTE}** e o **[categoria]** que **[beneficio principal]** porque **[razao para acreditar]**."

Para cada opção: aposta (o que prioriza) + risco (onde pode falhar).

### PUV (Proposta Unica de Valor)

Baseada na direção escolhida pelo operador (ou na recomendada). Inclua teste de qualidade:
- É verdadeira? (diferencial real, não aspiracional)
- É específica? (não serve para nenhum concorrente)
- É relevante? (resolve a dor principal do ICP)
- É memorável? (o ICP consegue repetir)
- É diferente? (nenhum concorrente diz isso)

### Canvas de Posicionamento (4Ps Estrategico)

Consulte `references/exemplos-puv.md` e `references/canvas-4p-guide.md`.

**PRODUTO:** Transformação entregue + antes/depois concreto + limitações honestas
**PREÇO:** Posicionamento (premium/mid/value) + justificativa na comunicação + ancoragem
**PRAÇA (CANAIS):** Canal principal + justificativa + canal secundário + canais a evitar (com motivo)
**PROMOÇÃO:** Tom e estilo + mensagem topo de funil + mensagem fundo de funil

### Territorio de marca

Consulte `references/territorio-de-marca.md`.
- Em 3 palavras: o que a marca representa
- O que significa na prática
- Territórios dos concorrentes (para diferenciação)
- Por que o território escolhido está disponível

### 3 opções de tagline

Para cada: tom + justificativa + melhor uso (site, assinatura, anúncios).

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos acima, SEMPRE inclua:

- **`summary_headline`** (max 200 char) — manchete com o veredito do posicionamento. Ex: "[Cliente] ocupa '[Território Premium do nicho]' — território único na microrregião com janela de 12-18 meses".
- **`summary_highlights`** (4-6 itens, `{category, label, value, subtext, tone}`) — sugestões:
  - `posicao`: território de 3 palavras escolhido
  - `competicao`: território ocupado pelo concorrente #1 (contraste)
  - `janela`: tempo até concorrência relevante chegar
  - `oportunidade`: ICP principal + ticket esperado
  - `risco`: pior cenário de posicionamento forçado
- **`summary_key_findings`** (3-5 itens, `{category, text}`) — `vantagem|contexto|ameaca|acao`.

### Ponto de alavancagem

Em posicionamento, o ponto de alavancagem é o **território × janela de oportunidade** — o espaço competitivo disponível combinado com o tempo que o cliente tem para ocupá-lo antes da concorrência chegar. Estruture em `key_insight`:
```json
"key_insight": {
  "headline": "Frase sobre território + janela (ex: 'Território [Especialista do nicho] está vago por 12-18 meses')",
  "context": "2-3 linhas sobre por que ninguém ocupou ainda e por que a janela é finita",
  "numbered_reasons": ["(1) evidência de que está vago", "(2) o que fecha a janela", "(3) o que o cliente ganha ao ocupar primeiro"],
  "discussion_anchor": "Por que o stakeholder precisa agir AGORA e não esperar validação"
}
```

Se o território escolhido é aspiracional (diferencial ainda não construído), ou a janela é curtíssima e exige decisão imediata, inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP, pesquisa de mercado, SWOT)?
- [ ] PUV passa nos 5 testes de qualidade?
- [ ] Cada declaração de posicionamento é diferente das outras (não variações do mesmo)?
- [ ] Território de marca não está ocupado por concorrente?
- [ ] Tem `summary_headline` específico?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos?
- [ ] Identificou `key_insight` (território × janela)?
- [ ] Se território é aspiracional ou janela curtíssima, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

**DECISÃO 1:** Direção de posicionamento — qual das 3 declarações?
- Opção A: "[nome da direção]" — "[declaração]"
- Opção B: "[nome da direção]" — "[declaração]"
- Opção C: "[nome da direção]" — "[declaração]"

**RECOMENDAÇÃO:** Opção [X]. [Justificativa baseada nos dados da pesquisa de mercado e SWOT, não opinião genérica.]

**PROVOCAÇÃO:** [Ex: "Essa direção implica abandonar o público Y. O cliente está pronto pra essa escolha?"]

**DECISÃO 2:** Tagline — qual direção?
- Opção A: "[tagline]"
- Opção B: "[tagline]"
- Opção C: "[tagline]"

**RECOMENDAÇÃO:** Opção [X]. [Justificativa baseada no território de marca e tom de voz.]

**PROVOCAÇÃO:** [Ex: "Essa tagline funciona em outdoor ou só em contexto digital?"]

Valide também:
- O canvas 4P está alinhado com a realidade do cliente?
- O que "não entregamos" está honesto?
- O tom de comunicação soa como o cliente falaria?
- As 3 palavras do território representam como o cliente quer ser percebido?

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/geral-posicionamento-estrategico.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Posicionamento concluído. PUV: '{puv}'. Tagline: '{tagline}'. Território: {3 palavras}."
   - "Este posicionamento é a raiz da Semana 3 inteira: a cabeça do modelo de venda + a cauda comum (/designer-manual-marca, /designer-landing-page, /copy-anuncios, /designer-criativos-anuncios, forecast)."
   - "Proximo passo recomendado: /gt-diagnostico-midia-paga ou /gt-diagnostico-criativos"


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do posicionamento: PUV definida e território de marca escolhido. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
