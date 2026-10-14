---
name: account-retrospectiva-criativos
description: Audita criativos do quarter, baixa assets pelo NEKT, relaciona copy, formato, hook, promessa, prova, CTA e métricas de mídia, e prepara materiais rastreáveis para o deck. Use quando a retrospectiva precisar explicar quais anúncios e padrões criativos performaram melhor ou pior.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.2.0
---

# Retrospectiva de criativos

Use somente NEKT para inventário, preview e download dos assets. Se o NEKT não entregar, registre lacuna em `decisoes.md` com o input manual necessário e siga; não troque de fonte silenciosamente.

## Saídas

- `03-criativos.md`
- `assets/criativos/`
- atualização de `bases/anuncios.md`

## Coleta e processamento

1. Baixe todos os criativos ativos e os top performers históricos disponíveis no período.
2. Preserve asset original e crie derivados necessários para apresentação.
3. Nomeie por canal, campaign_id, ad_id e hash; elimine duplicatas por hash.
4. Extraia copy, legenda, headline, CTA e destino.
5. Para imagem, aplique OCR quando útil.
6. Para vídeo, extraia poster/thumbnail e transcrição; identifique hook inicial.
7. Classifique formato, ângulo, dor, desejo, promessa, prova, oferta e CTA.
8. Cruze tags com CPM, CTR, CPC, CPL, CPMQL, CPSQL, CPVenda, ROAS, hook e hold rate.
9. Preserve uma linha por combinação anúncio × conjunto e uma visão consolidada do mesmo criativo entre conjuntos.
10. Registre para cada anúncio `ad_id`, `creative_id`, preview, asset, copy, formato, destino e status de coleta, ainda que parte dos campos esteja indisponível.

## Guardrails

- Não confunda correlação criativa com causalidade.
- Compare criativos com objetivo, público, veiculação e amostra compatíveis.
- Preserve link do preview, IDs e fonte de cada asset.
- Não marque o módulo como `complete` se previews/assets dos anúncios com investimento não tiverem cobertura medida.
- Nunca reduza a entrega apenas aos top performers; mantenha anúncios com gasto e zero resultado para provar perdedores e desperdício.
