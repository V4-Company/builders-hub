# Fontes, precedência e reconciliação

## Varredura

Consulte tudo que estiver autorizado e for profissional do cliente:

1. Repositório local do cliente.
2. Flow e Cockpit para identidade, escopo, contrato, equipe e contexto.
3. GrowthPack para visão macro, metas e projetado versus realizado.
4. NEKT para mídia, breakdowns, previews e assets de criativos.
5. CRM, GA4, e-commerce e ferramenta conversacional por conexões disponíveis, inclusive n8n.
6. Drive para documentos oficiais, projeções, breakeven, backups e histórico.
7. Input humano validado como fallback.

## Fonte oficial por assunto

- Contexto e contrato: Flow/Cockpit/documento oficial.
- Projetado versus realizado macro: GrowthPack ou forecast oficial aprovado.
- Entrega de mídia: NEKT.
- MQL, SQL, oportunidade, orçamento e venda: CRM.
- Receita faturada: financeiro/e-commerce/CRM conforme definição validada.
- Sessões e eventos web: GA4.
- Produto, pedido, cancelamento e reembolso: plataforma de e-commerce.
- Conversas e mensagens: ferramenta conversacional; timeline comercial complementar no CRM.
- Criativo em veiculação e asset: NEKT.

Conflito material não é resolvido silenciosamente. Mostre as fontes, impacto e recomendação; peça decisão humana quando mudar a conclusão.

## Atribuição oficial

Use `first_paid_touch`: a campanha que adquiriu o lead permanece ligada a MQL, SQL, oportunidade, orçamento e venda. Last paid touch é auxiliar e nunca substitui a origem oficial.

Hierarquia de atribuição:

1. IDs persistidos: campaign, adset/ad group, ad, gclid, fbclid.
2. UTMs normalizadas.
3. URL de entrada, formulário ou destino com parâmetros.
4. Origem e campanha registradas no CRM.
5. Nome exato ou normalizado.
6. Mapeamento manual validado.
7. `unattributed`.

## Resolução de identidade

Antes de atribuir mídia, descubra se registros pertencem à mesma pessoa:

1. ID compartilhado.
2. Telefone normalizado.
3. E-mail normalizado.
4. Nome combinado com telefone ou e-mail.
5. Link do lead, contato, negócio, conversa ou card.
6. Nome isolado apenas como candidato para revisão.

Nunca atribua campanha apenas porque duas pessoas têm o mesmo nome.

## Confiança do match

Use:

- `exact_id`
- `exact_utm`
- `exact_phone`
- `exact_email`
- `exact_link`
- `exact_name`
- `normalized_name`
- `composite_match`
- `manual_validated`
- `name_only_review`
- `unmatched`

Preserve `raw_value`, `normalized_value`, `match_rule`, `matched_record_id`, `confidence` e `review_status`.
