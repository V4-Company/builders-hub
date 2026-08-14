# Padrão de Output das Skills — V4 Estruturação IA

Este documento define a **estrutura canônica** que todos os outputs de skill devem seguir para renderizar no portal com hierarquia visual consistente. O objetivo é que o operador e o stakeholder final abram qualquer entregável e encontrem o mesmo ritmo: manchete → KPIs → achados categorizados → ponto de alavancagem destacado → detalhes expansíveis.

---

## Princípios

1. **Manchete antes de texto.** Toda skill abre com uma frase única e específica que resume a conclusão. Não é parágrafo, é headline.
2. **Números em destaque, não escondidos no corpo do texto.** KPIs que importam viram cards. Texto corrido é para contexto, não para fato quantitativo.
3. **Achados categorizados por intenção.** Cada insight é classificado como `vantagem | contexto | ameaca | acao` — o leitor identifica o tom antes de ler.
4. **Ponto de alavancagem visualmente isolado.** Toda skill tem UM ponto onde a conversa com o stakeholder precisa acontecer. Esse ponto ganha hero visual (border, gradient, quote destacada).
5. **Detalhe denso → colapsável.** Listas longas (concorrentes, itens de checklist, fontes) ficam em `<details>` para não afogar a leitura.

---

## Campos obrigatórios no JSON

Todo output de skill DEVE ter estes campos no topo (antes dos campos específicos da skill):

```json
{
  "client_name": "Nome do Cliente",
  "summary": "Resumo em 1-2 frases. Específico, com dados reais. Alimenta o resumo executivo do portal.",

  "summary_headline": "Manchete em 1 linha (max 120 caracteres). A frase que o stakeholder lê primeiro.",

  "summary_highlights": [
    {
      "category": "posicao | competicao | janela | maturidade | oportunidade | risco",
      "label": "Rótulo curto (max 30 char)",
      "value": "Valor em destaque (número, %, status)",
      "subtext": "Contexto em 1 linha (max 60 char)",
      "tone": "green | yellow | red | blue | gray"
    }
  ],

  "summary_key_findings": [
    {
      "category": "vantagem | contexto | ameaca | acao",
      "text": "Achado em 1-2 linhas. Específico, acionável."
    }
  ]
}
```

### Regras dos campos de summary

**`summary_headline`**: É a ÚNICA frase que o stakeholder precisa ler se só tiver 5 segundos. Deve conter o veredito da skill. Exemplos bons:
- ✓ "[Cliente] é o ÚNICO player premium da microrregião com [diferencial declarado] — janela competitiva de 12-18 meses."
- ✗ "Análise de mercado concluída com sucesso."

**`summary_highlights`** (4-6 itens): KPIs visuais. Categorias sugeridas:
- `posicao` — onde o cliente está hoje vs potencial
- `competicao` — quem disputa o mesmo espaço
- `janela` — tempo/urgência
- `maturidade` — estágio atual em algum eixo
- `oportunidade` — tamanho do ganho possível
- `risco` — tamanho da ameaça

Agrupar de 2 em 2 por categoria no renderer (dá layout balanceado 3x2 ou 2x2).

**`summary_key_findings`** (3-5 itens): Achados que embasam a manchete. Categorias:
- `vantagem` (✓ verde) — o que o cliente tem a favor
- `contexto` (i azul) — o que é fato do mercado, neutro
- `ameaca` (! vermelho) — o que pode dar errado
- `acao` (▸ laranja) — o que precisa ser feito

---

## Ponto de Alavancagem (hero block)

Toda skill deve identificar **UM bloco que merece destaque visual especial** — o ponto onde a conversa estratégica precisa acontecer. O nome do campo varia por skill, mas a estrutura é consistente:

```json
{
  "key_leverage_point": {
    "headline": "Frase-manchete do ponto (pode ir como quote)",
    "context": "Contexto em 2-3 linhas explicando o cenário",
    "numbered_reasons": [
      "Razão 1 (parse-friendly, pode começar com texto direto)",
      "Razão 2",
      "Razão 3"
    ],
    "discussion_anchor": "Frase curta sobre POR QUE este é o ponto de conversa com o stakeholder"
  }
}
```

Exemplos por skill:
- `pesquisa-mercado` → `unexploited_opportunity` (whitespace estratégico)
- `persona-icp` → persona principal + dor mais ignorada
- `swot` → combinação força × oportunidade mais assimétrica
- `posicionamento` → PUV vs alternativas descartadas
- `diagnostico-midia` → canal mais subotimizado + upside estimado
- `diagnostico-maturidade` → pilar mais fraco com maior impacto

O renderer aplica:
- Border verde 2px + gradient sutil
- Selo "Whitespace Estratégico · Discussão com Stakeholder" no topo
- Pill de viabilidade/urgência à direita
- Quote/headline em card branco isolado
- Razões numeradas em 3 círculos
- Footer "💬 Momento de validar com a stakeholder"

---

## Alerta de honestidade

Se a pesquisa/análise revelou fragilidade do cliente (não há diferencial real, ICP mal definido, mercado saturado, etc.), inclua:

```json
{
  "honesty_alert": "Texto explicando a fragilidade encontrada e o que precisa ser feito antes de seguir."
}
```

Esse campo renderiza em box amarelo/vermelho após os achados. **Nunca omita** se a realidade justifica. O valor do sistema depende de não vender aspiracional como real.

---

## Instrução para a IA da skill

Em cada `SKILL.md`, incluir esta seção na geração:

> ### Estrutura visual (obrigatória)
>
> Além dos campos específicos desta skill, gere SEMPRE:
>
> - `summary_headline` — manchete em 1 linha com o veredito
> - `summary_highlights` — 4-6 KPIs categorizados (`posicao|competicao|janela|maturidade|oportunidade|risco`) com `{label, value, subtext, tone}`
> - `summary_key_findings` — 3-5 achados categorizados (`vantagem|contexto|ameaca|acao`)
> - `honesty_alert` se houver fragilidade
>
> Identifique o **ponto de alavancagem** desta skill (o bloco que merece hero visual) e estruture-o com headline + contexto + razões numeradas + discussion anchor.
>
> Consulte `references/padrao-output.md` para especificação completa.

E na auto-validação:

> - [ ] Tem `summary_headline` específico (não "análise concluída")?
> - [ ] `summary_highlights` tem 4-6 itens com categorias válidas?
> - [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos (vantagem/contexto/ameaça/ação)?
> - [ ] Identificou o ponto de alavancagem para discussão com stakeholder?
> - [ ] Se há fragilidade, incluiu `honesty_alert`?

---

## Completude (regra crítica)

**Todo campo definido no schema da skill é obrigatório no output.** Não omitir campos — o renderer assume que os campos do schema existem e quebra/fica vazio silenciosamente quando faltam.

Se um dado **não pode ser obtido** (GA4 não instalado, conector não conectado, cliente não sabe, etc.), preencher com `null` E adicionar `unavailable_reason` no objeto pai:

```json
{
  "current_conversion_rate": null,
  "current_bounce_rate": null,
  "avg_time_on_page": null,
  "unavailable_reason": "GA4 não instalado no site — métricas de analytics não coletadas nesta auditoria"
}
```

Para arrays vazios legitimamente (ex: nenhum competidor identificado), preencher com `[]` e adicionar uma nota no campo irmão `{campo}_note`:

```json
{
  "competitors": [],
  "competitors_note": "Nenhum concorrente direto identificado na microrregião após busca em Google Maps + Instagram."
}
```

Para valores **estimados** (sem fonte pública), adicionar flag `[E]` no texto OU campo `estimated: true` no objeto:

```json
{ "tam_brl": 450000000, "estimated": true, "estimation_basis": "IBGE população × SEBRAE ticket médio" }
```

**Nunca** deixar string vazia (`""`), zero falso (`0` quando não é zero real), ou omitir o campo. Essas três formas são invisíveis para o renderer e geram o bug "coluna vazia".

Valide o JSON contra o `schema.json` empacotado na skill e corrija campos ausentes ou `null` sem `unavailable_reason`.

### Checklist adicional de auto-validação

> - [ ] Todos os campos do schema estão presentes (preenchidos ou com `null` + `unavailable_reason`)?
> - [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
> - [ ] Arrays vazios legítimos têm `{campo}_note` explicando por quê?
> - [ ] Estimativas marcadas com `estimated: true` ou `[E]`?

---

## Tons de voz

- `green` — oportunidade/vantagem/confirmado
- `yellow` — atenção/potencial/médio
- `red` — risco/ameaça/fraco
- `blue` — contexto/informativo/neutro
- `gray` — desativado/aspiracional/ausente

Usar tons consistentemente: nunca pintar ameaça de verde ou vantagem de vermelho para "chamar atenção". O tom é semântico.

---
