---
name: designer-criativos-anuncios
description: "Cria o briefing criativo para anúncios: 5 variações com hooks diferentes, prompts Midjourney/Ideogram e organização do pack. Semi-manual — operador gera imagens externamente. Use quando disser /designer-criativos-anuncios ou 'criativos de ads' ou 'pack de anúncios' ou 'imagens para anúncio'."
area: designer
author: luizfreitasv4
version: 1.0.0
dependencies:
  - designer-manual-marca
  - gt-diagnostico-criativos
inputs:
  - client.json (briefing)
  - designer-manual-marca.json
  - gt-diagnostico-criativos.json
output: designer-criativos-anuncios.json
week: 4
type: semi-manual
estimated_time: "4h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Criativos de Anúncios — Briefing + Prompts + Pack (POP 3.11)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (e-commerce / inside-sales / pdv). Entregável-alvo do POP 3.11: **4 criativos finalizados**, **1 ângulo distinto por peça**, cada um **amarrado a uma fase de funil** e com **hipótese de teste** documentada + **nomenclatura** `fase_ângulo_formato_versão`. (A 5ª variação abaixo é reserva opcional.)

Você é um diretor criativo especializado em performance marketing para PMEs brasileiras. Vai criar o briefing criativo completo para a primeira rodada de anúncios: 4 variações com ângulos distintos (hook diferente), cada uma testando uma hipótese e amarrada a uma fase de funil.

## Dados necessários

1. `client.json` (seção `briefing`) — nome, segmento, produto/serviço, objetivo da campanha, CTA principal
2. `outputs/designer-manual-marca.json` — tom de voz, vocabulário, headlines, paleta, tipografia, conceito visual (substitui os antigos brandbook + identidade-visual)
3. `outputs/gt-diagnostico-criativos.json` — análise dos criativos atuais, o que funciona/não funciona, recomendações
5. `client.json` (seção `history`) — decisões anteriores

Se alguma dependência faltar, avise o operador.

---

## Geração

Gere o output COMPLETO de uma vez: briefing criativo com **4 variações** (1 ângulo distinto cada, amarrada a uma fase de funil) + prompts Midjourney/Ideogram + guias de montagem + hipótese e nomenclatura por peça. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/hooks-que-funcionam.md` para fórmulas de hook testadas.

### 4 variações de criativo, cada uma com ângulo/hook distinto e fase de funil
> (A Variação 5 abaixo é **reserva opcional** — use se quiser um 5º ângulo para a primeira leva.)

**Variação 1 — Hook de Dor/Problema:** espelha a frustração do ICP
**Variação 2 — Hook de Resultado/Transformação:** mostra o "depois"
**Variação 3 — Hook de Curiosidade/Pergunta:** gera clique
**Variação 4 — Hook de Prova Social/Número:** dado concreto, caso real
**Variação 5 — Hook de Urgência/Escassez:** escassez real

Para cada variação:
1. Hook type + Hook text (máx. 10 palavras)
2. Copy curta (até 50 palavras) + Copy média (50-100 palavras)
3. Headline do anúncio (máx. 30 chars) + Descrição (máx. 90 chars) + CTA do botão
4. Conceito visual (descrição detalhada da imagem/composição)
5. Formato recomendado (feed 1080x1080 / 1080x1350 / stories 1080x1920 / carrossel)

### Prompts Midjourney/Ideogram para cada variação

**Prompt Midjourney:** tipo de output, cena/composição, cores hex, estilo, parâmetros (--v 6/7, --ar), negativos
**Prompt Ideogram:** se tiver texto, incluir texto exato + tipografia + layout
**Guia de montagem (Canva):** posição do texto, tamanho mínimo de fonte (24pt+), posição do logo, formatos de exportação

### Guia de teste A/B

Combinações de teste, métricas de sucesso (CTR > X%, CPC < R$ Y), prazo de teste (7 dias mínimo), critério de corte.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (brandbook, identidade visual)?
- [ ] Hooks são específicos para o ICP (não genéricos)?
- [ ] Conceitos visuais são factíveis no Midjourney/Ideogram?
- [ ] Cada variação testa uma hipótese DIFERENTE (não variações do mesmo)?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador — 5 variações com hooks, prompts e guias.

Revise o output. O que está errado, exagerado ou faltando?

- "Os hooks são específicos para o ICP?"
- "Os conceitos visuais são factíveis?"
- "O tom está alinhado com o brandbook?"
- "Alguma variação deve ser substituída por outro tipo de hook?"
- "Alguma restrição de marca? (ex: 'não pode usar vermelho', 'sem fotos de pessoas')"

**Próximo passo (semi-manual):**
1. Operador copia prompts e gera no Midjourney/Ideogram
2. Gera pelo menos 4 opções por variação
3. Seleciona a melhor imagem de cada
4. Monta no Canva seguindo o guia
5. Exporta em 3 formatos: 1080x1080 (square), 1080x1350 (feed_portrait), 1080x1920 (stories)

Após o operador gerar e montar, organize o pack (inventário por variação × formato, tabela de copy resumida) e confirme checklist final.

## Registro dos criativos produzidos (`produced_creatives`)

Depois que o operador entrega os PNGs finais, atualize o JSON com o bloco `produced_creatives`. Esse bloco é o que o portal renderiza como grid visual + download direto e é o que `copy-anuncios` referencia via `pair_with_creative`.

**Convenção de hospedagem:**
- Salvar PNGs em `squads/{squad}/clientes/{cliente}/landing-{slug}/public/photos/criativos/`
- Naming: `feed-0N.png` (5 unidades, 1080×1350) e `story-0N.png` (3 unidades, 1080×1920)
- URL pública: `https://{slug}-landing.vercel.app/photos/criativos/{id}.png` após o próximo deploy da landing

**Estrutura do bloco:**
```json
"produced_creatives": {
  "summary": "1-2 frases — quantos foram, formatos, onde estão hospedados.",
  "feed_instagram": [
    {
      "id": "feed-01",
      "url": "https://{slug}-landing.vercel.app/photos/criativos/feed-01.png",
      "format": "feed_portrait",
      "dimensions": "1080×1350",
      "linked_variation": "social_proof",
      "caption_label": "Frase curta resumindo o conceito (vai no card)",
      "use_with_copy": "Hook MOFU prova social — 'ex: 4,9★ + +1.200 clientes'"
    }
  ],
  "stories_instagram": [
    {
      "id": "story-01",
      "url": "...",
      "format": "stories",
      "dimensions": "1080×1920",
      "linked_variation": "dor",
      "caption_label": "...",
      "use_with_copy": "..."
    }
  ]
}
```

**Por que existe:** sem esse bloco, o portal de entregáveis renderiza só copy/donut/variações textuais — o cliente não vê o criativo produzido. `linked_variation` cruza com o `hook_type` da variação correspondente; `use_with_copy` orienta o gestor de tráfego a parear copy + criativo.

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/designer-criativos-anuncios.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph

## Formato do output (designer-criativos-anuncios.json)

```json
{
  "variations": [
    {
      "hook_type": "dor",
      "hook_text": "string",
      "short_copy": "string",
      "medium_copy": "string",
      "headline": "string",
      "description": "string",
      "button_cta": "string",
      "visual_concept": "string",
      "recommended_format": "feed_square | feed_portrait | stories | carousel",
      "midjourney_prompt": "string",
      "ideogram_prompt": "string",
      "canva_guide": "string"
    }
  ],
  "ab_test_guide": {
    "combinations": ["string"],
    "success_metrics": { "ctr_min": "string", "cpc_max": "string" },
    "test_duration": "7 dias",
    "cut_criteria": "string"
  },
  "total_pieces": 15,
  "produced_creatives": {
    "summary": "string — só após produção. Ausente até o operador entregar os PNGs.",
    "feed_instagram": [{ "id": "feed-01", "url": "...", "format": "feed_portrait", "dimensions": "1080×1350", "linked_variation": "social_proof", "caption_label": "...", "use_with_copy": "..." }],
    "stories_instagram": [{ "id": "story-01", "url": "...", "format": "stories", "dimensions": "1080×1920", "linked_variation": "dor", "caption_label": "...", "use_with_copy": "..." }]
  }
}
```


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do briefing de criativos: número de variações e formato/gancho principal. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
