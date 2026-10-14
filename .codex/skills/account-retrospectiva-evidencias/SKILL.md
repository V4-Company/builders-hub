---
name: account-retrospectiva-evidencias
description: Monta a base probatória da retrospectiva com IDs, fontes, links, timestamps, regras de cálculo e amostras auditadas para sustentar qualquer conclusão diante do cliente. Use depois da reconciliação e antes de consolidar achados e gaps.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.1.0
---

# Evidências

## Saída

- `09-evidencias.md`

## Ledger

Crie uma linha por evidência:

| evidence_id | tipo | entidade | source_record_id | fonte | período | extraído_em | regra/cálculo | link | confiança |
|---|---|---|---|---|---|---|---|---|---|

Inclua links para campanha, anúncio, criativo, lead, negócio, conversa, card, pedido e documento quando existirem.

## Auditoria

- Feche totais e cobertura por fonte.
- Confira amostra de matches exatos, normalizados e manuais.
- Confira amostra de conversas classificadas como sem atendimento, sem resposta e sem follow-up.
- Confira todas as flags P0 e uma amostra estratificada das demais severidades.
- Nas avaliações comerciais, confira IDs das mensagens, trechos mínimos, versão da rubrica, cobertura e estado de calibração.
- Confirme que conteúdo não transcrito não recebeu penalidade dependente do conteúdo.
- Confira campanhas vencedoras em cada lente contra a tabela-mãe.
- Confira se todas as campanhas, conjuntos e anúncios com investimento aparecem nas bases, inclusive os que tiveram zero resultado.
- Reconcilie investimento entre canal, campanha, conjunto e anúncio e registre diferença absoluta e percentual.
- Confira a matriz de cobertura de mídia e rejeite dimensões omitidas sem status, justificativa e próximo passo.
- Registre limitações de API, paginação, sincronização e período.

Toda conclusão final deve citar `evidence_id`. Sem evidência, rotule como hipótese ou input humano.
