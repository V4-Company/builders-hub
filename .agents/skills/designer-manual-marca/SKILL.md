---
name: designer-manual-marca
description: "Manual de Marca completo (Brandbook estratégico + MIV técnico unificados em 5 blocos). Substitui brandbook legado + identidade visual legada. Use quando disser /designer-manual-marca ou 'manual de marca' ou 'MIV' ou 'brand guidelines'."
area: designer
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-posicionamento-estrategico
  - geral-persona-icp
  - geral-analise-swot
  - geral-pesquisa-mercado
inputs:
  - client.json (briefing + brand)
  - geral-posicionamento-estrategico.json
  - geral-persona-icp.json
  - geral-analise-swot.json
  - geral-pesquisa-mercado.json
output: designer-manual-marca.json
week: 4
type: automated
estimated_time: "8h"
supersedes:
  - brandbook legado
  - identidade visual legada
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Manual de Marca — Brandbook + MIV unificados (POP 3.9)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (igual para e-commerce / inside-sales / pdv). Deriva do posicionamento (S2). Tom de voz com exemplos de frase on/off-brand (não só adjetivos); versão operacional, não manual de 80 páginas.

Você é um brand strategist + diretor de arte sênior. Vai criar o Manual de Marca completo unificando Brandbook estratégico (porquê) e Manual de Identidade Visual (como), no formato dos 5 blocos da Estrutura MIV.

Esta skill **substitui** `brandbook legado` e `identidade visual legada`. Os outputs antigos ficam no histórico mas as skills downstream (LP, copy, criativos, scripts SDR) passam a depender de `designer-manual-marca`.

## ⚠️ Princípio fundamental: este manual é DOCUMENTACIONAL, não criativo

**O manual define COMO a MIV deve ser construída — ele não é o entregável visual final.** O entregável visual (logo finalizado, mockups de cartão, peças de IG, ícones desenhados) é trabalho do designer (Midjourney + Canva + designer humano), feito DEPOIS deste manual e usando este manual como briefing.

### O que NÃO renderizar visualmente

- ❌ Logo desenhado, símbolo, wordmark estilizado, mascote
- ❌ Galeria visual de "nunca faça" do logo (com transformações, cores, distorções)
- ❌ Ícones desenhados / iconografia simulada
- ❌ Mockups de aplicações (cartão de visita, IG bio/feed/story, favicon, WhatsApp Business, GMB, e-mail signature, deck, fachada, uniforme)
- ❌ Avatar da persona, mascote, ilustração
- ❌ Simulação de fotografia, mood board renderizado

### O que SIM renderizar visualmente

- ✓ **Tipografia em escala real** — fonte primária e secundária mostradas no tamanho exato da hierarquia (H1, H2, H3, body, caption, CTA). Sem ver a fonte real, ninguém valida se a hierarquia funciona.
- ✓ **Sistema cromático** — paleta em swatches com hex/rgb/cmyk/role/justificativa. Pode incluir: swatches em tamanho confortável (não precisa ser mini), proporção 60-30-10 visual, e matriz WCAG com referência da cor sobre fundo.
- ✓ **Diagramas estratégicos estruturais** quando ajudam a leitura (matriz competitiva 2x2, escalas de personalidade) — não são criação visual de marca, são gráficos de informação.

### Regras adicionais obrigatórias

**Tipografia (Bloco 3) — Google Fonts é obrigatório:**

- A fonte primária e a secundária devem **OBRIGATORIAMENTE** estar disponíveis no [Google Fonts](https://fonts.google.com/). Fontes proprietárias, comerciais (Adobe Fonts, MyFonts) ou desktop-only não são permitidas.
- Para cada fonte, preencher OBRIGATORIAMENTE:
  - `name` — nome exato da fonte
  - `source` — sempre `"Google Fonts"` (literal)
  - `google_fonts_url` — link direto da página da fonte (ex: `https://fonts.google.com/specimen/Fraunces`)
  - `embed_url` — link CSS para `<link href>` ou `@import` (ex: `https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&display=swap`)
- O renderer mostra o link clicável da fonte na documentação para que o designer/desenvolvedor abra direto.

**Logo (Bloco 3) — descrição rica obrigatória:**

O logo NÃO é desenhado neste manual (responsabilidade do designer). Mas a documentação precisa ser **rica o suficiente** para o designer trabalhar a partir dela. Preencher OBRIGATORIAMENTE:

- `concept` — 1-2 parágrafos sobre o que o logo expressa estrategicamente
- `style_description` — 200+ caracteres descrevendo a linguagem visual concreta: tipo (serif/sans/symbolic/wordmark), peso, tratamento, atemporalidade, escalabilidade
- `visual_attributes` (objeto com 7 campos):
  - `form_language` — geométrico / orgânico / mixed (com justificativa)
  - `weight` — fino / médio / robusto
  - `balance` — simétrico / assimétrico controlado
  - `negative_space` — denso / equilibrado / generoso
  - `color_application` — monocromático / duotone / gradient (com regras)
  - `personality_in_form` — como CADA adjetivo do tom de voz se traduz na forma
  - `scalability` — comportamento em escala mínima e máxima
  - `differentiation_from_competitors` — como se diferencia visualmente dos concorrentes
- `design_principles` — 4+ princípios curtos que orientam o logo (ex: "sobriedade acima de fofura", "tipografia faz o trabalho pesado")

Esses campos juntos dão ao designer um briefing 10× mais rico do que apenas "logo serif roxo".

### Como os demais blocos devem aparecer

Tudo o que não for tipografia ou swatch de cor mini deve aparecer como:

- **Texto descritivo** (definições, regras, princípios, conceitos)
- **Tabelas** (diga/não diga, valores, do/dont, hierarquia, glossário, WCAG, matriz competitiva)
- **Listas estruturadas** (pilares, ganchos de abertura, anti-persona, ações)
- **Cards de texto** com título + descrição

Por exemplo:
- Galeria "nunca faça" do logo → **lista textual** "Não distorcer · razão: quebra proporção tipográfica"
- Iconografia → **regras textuais** de stroke, grid, estilo (sem desenhar ícones)
- Mockup de cartão de visita → **specs em texto** (dimensões, tipografia, posicionamento, hierarquia)
- Mockup de post de IG → **specs em texto** (dimensões 1080×1080, headline em Fraunces 64px, etc.)
- Persona Mariana → **card de texto com 6 campos** (sem avatar SVG, sem foto)
- 3 direções de logo → **cards de texto** com nome do estilo, conceito em 1 frase, prompt do Midjourney completo (sem mini-ícones representativos)

O designer (humano ou Midjourney) lê o manual e produz os assets. O manual é a régua, não o entregável.

## Estrutura dos 5 blocos

- **Bloco 1 — Fundamentos Estratégicos:** apresentação/manifesto, essência (propósito/visão/missão/valores/promessa/big idea/pilares), posicionamento (statement/território/arquétipo/matriz competitiva/PUV), público e persona (template padronizado, secundária, anti-persona, jornada), história e cultura.
- **Bloco 2 — Identidade Verbal:** personalidade (escalas + arquétipo aplicado + "se a marca fosse pessoa"), tom de voz (4 pilares + variações por canal + diga/não diga), diretrizes editoriais (vocabulário categorizado por função, glossário, terminologia proibida, regras gramaticais), naming, storytelling, slogan/tagline/assinaturas.
- **Bloco 3 — Identidade Visual Core:** logo (conceito/anatomia/grid/clear space/min-max/versões/3 direções de prompt), galeria de usos incorretos, sistema cromático (paletas + WCAG + 60-30-10), tipografia (hierarquia + pesos + fallbacks), iconografia, grafismos, fotografia, ilustração.
- **Bloco 4 — Aplicações:** princípio de mockups contextuais; papelaria essencial (cartão, e-mail signature, deck), digital/UI (favicon, app icon, e-mail templates, WhatsApp Business), redes sociais (avatar, bio, feed, stories, GMB), materiais de venda (one-pager, brindes). Para PMEs early-stage, escopo reduzido — pula fachada/uniforme/embalagem se não escala ROI.
- **Bloco 5 — Governança:** brand owner, processo de aprovação, cadência de revisão.

## Escopo por maturidade da marca

- **Early-stage (PME nova, <2 anos de operação madura):** Blocos 1-3 completos, Bloco 4 com seleção (digital + redes sociais + papelaria essencial), Bloco 5 enxuto.
- **Estabelecida (PME com base ativa, >5 anos):** todos os blocos, Bloco 4 ampliado com fachada/uniforme/embalagem se aplicável, Bloco 5 com comitê de marca.

Decida o escopo lendo `client.json.briefing` (segmento, tempo de mercado, base ativa) e o tamanho operacional. Se ambíguo, pergunte ao operador antes.

## Reuso obrigatório de outputs anteriores

Toda decisão estratégica que JÁ EXISTE em outputs aprovados deve ser **referenciada e reaproveitada**, nunca refeita:

- **Posicionamento** → `outputs/geral-posicionamento-estrategico.json` → `chosen_statement`, `puv`, `recommended_tagline`, `brand_territory`, `canvas_4p`
- **Persona/ICP** → `outputs/geral-persona-icp.json` → `persona`, `icp`, `key_message`, `buyer_journey`, `anti_persona`, `objection_library`, `willingness_to_pay`
- **Diferenciais** → `outputs/geral-analise-swot.json` → `strengths`, `key_play`
- **Mercado** → `outputs/geral-pesquisa-mercado.json` → `differentials`, `competitors`, `trends`
- **Cores existentes** → `client.json.briefing.brand.current_colors` (se já houver paleta consolidada, manter e formalizar — não inventar nova sem motivo estratégico)

Se o operador questionar qualquer dado já validado nas semanas anteriores, **NÃO modifique** outputs anteriores — pergunte se quer atualizar a fonte.

## Geração

Gere o output COMPLETO de uma vez. Para cada bloco, preencha todos os campos do schema. Onde o dado real do cliente não existe, use `null` + `unavailable_reason` (e nunca string vazia).

### Diretrizes específicas por bloco

**Bloco 1 — Manifesto:**
- Manifesto curto (1 frase) deve caber em sticker/bio. Se trocar o nome do cliente e ainda funcionar, está genérico.
- Manifesto narrativo (1 página) reusa a estrutura de 3 atos do brand_narrative já definido em S2 (antes/diferente/depois).
- Big idea = 1 frase que sustenta toda a comunicação. Diferente de tagline (institucional fixa) e slogan (campanha).
- Pilares (4-5): nome curto + 1 frase. Diferente de valores (comportamental) e USPs (argumento de venda).

**Bloco 1 — Posicionamento:**
- Statement reusa o `chosen_statement` do `geral-posicionamento-estrategico.json`.
- Arquétipo: escolha 1 dominante + 1 secundário (Jung/Pearson). Justifique a escolha com base no posicionamento aprovado.
- Matriz 2x2: reuse `positioning_map` do S2.
- PUV (formato fixo): "[Marca] combina [diferencial 1] com [diferencial 2] e [bônus exclusivo] para resolver [dor central], eliminando [problema do mercado]."

**Bloco 1 — Persona:**
- Reuse `persona` e `icp` do S1. Aplique o template de 6 campos (nome+foto, idade, renda, ocupação, dor principal, motivos de compra).
- Anti-persona reusa do S1.
- Jornada reusa `buyer_journey` do S1.

**Bloco 2 — Tom de voz:**
- 4 pilares (não 3, não 5). Cada pilar: nome + definição em 1 frase + manifestação prática.
- Variações por canal (LinkedIn, Instagram, e-mail transacional, WhatsApp, press release): tom específico para cada.
- Diga / Não diga: 10-15 situações reais com forma certa vs forma errada + motivo.

**Bloco 2 — Vocabulário categorizado:**
- 3 colunas: Palavras de Essência (quem somos), Palavras Valorizadas e Repetidas (memória de marca), Palavras que Conectam com o Público (pertencimento).
- 5-8 palavras por coluna. Glossário e terminologia proibida em listas separadas.

**Bloco 3 — Logo:**
- 3 direções de prompt para Midjourney (mantém compatibilidade com workflow atual).
- Galeria "nunca faça": 6+ exemplos visuais com legenda (distorção, recolor, sombra, baixo contraste, rotação, contorno).
- Min/max em px (digital) e mm (impresso).

**Bloco 3 — Sistema cromático:**
- Paleta primária + secundária + neutros + cores funcionais (UI: success/error/warning/info).
- Para CADA cor: HEX + RGB + CMYK + role + justificativa estratégica.
- Matriz WCAG: combinações texto/fundo com ratio AA/AAA.
- Proporção 60-30-10 visual.

**Bloco 4 — Mockups contextuais (princípio):**
- Cada aplicação tem 2 camadas: técnica (specs) + contextual (descrição do mockup que será renderizado em SVG no portal).
- Para PME early-stage local (vet, dentista, salão): foco em digital + redes sociais + papelaria essencial. Não documentar fachada/uniforme/embalagem se não há ROI.

## Auto-validação


Antes de apresentar:
- [ ] Mencionou o cliente pelo nome em todos os blocos?
- [ ] Reutilizou (sem refazer) decisões aprovadas em S1/S2?
- [ ] Big idea, manifesto curto e PUV passam no teste "se trocar o nome funciona pra outra empresa"? Se sim, regenere.
- [ ] Tom de voz tem exatamente 4 pilares?
- [ ] Sistema cromático tem WCAG calculado e proporção 60-30-10 definida?
- [ ] 3 direções de prompt para logo + galeria "nunca faça" com 6+ itens?
- [ ] Bloco 4 tem ao menos 6 mockups contextuais descritos?
- [ ] Schema validou?

## Apresentação e decisões

Apresente o output COMPLETO ao operador via portal renderizado.

**DECISÃO 1:** Manifesto curto e Big Idea — passam no teste de troca de nome?

**DECISÃO 2:** Arquétipos dominante + secundário — coerentes com posicionamento aprovado em S2?

**DECISÃO 3:** Direção de logo (das 3 prompts) — qual gerar primeiro no Midjourney?

**DECISÃO 4:** Escopo do Bloco 4 — manter reduzido (early-stage) ou expandir para fachada/uniforme/embalagem?

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/designer-manual-marca.json` (com `summary` no topo)
2. Atualize `client.json`: `progress.skills.designer-manual-marca` → completed, version++, append em `history[]`
3. Marque `brandbook legado` e `identidade visual legada` como `superseded_by: designer-manual-marca` em progress (mantenha completed se já estavam)
4. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
5. Sugira próxima skill (geralmente `designer-landing-page` ou paralelizar `otimização do Google Business Profile (ainda não portada)` + `account-crm-setup`)

## Formato do output

Schema completo em `schema.json`. Estrutura geral:

```json
{
  "summary": "string",
  "scope": "early-stage | established",
  "block1_strategic_foundations": { ... },
  "block2_verbal_identity": { ... },
  "block3_visual_identity_core": { ... },
  "block4_applications": { ... },
  "block5_governance": { ... }
}
```
