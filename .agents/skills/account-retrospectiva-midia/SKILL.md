---
name: account-retrospectiva-midia
description: Coleta e analisa mídia do quarter em visão macro e micro, comparando canais, estratégias, destinos, campanhas, conjuntos, anúncios, públicos e breakdowns pelo funil completo. Use em toda retrospectiva de performance com Google, Meta ou outro canal pago conectado ao NEKT.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.3.0
---

# Retrospectiva de mídia

Leia os contratos `metricas-e-rankings.md`, `cobertura-midia.md`, `fontes-e-reconciliacao.md`, `janelas-temporais.md` e `contrato-markdown.md` do maestro.

## Fonte

Use NEKT para entrega de mídia. GrowthPack serve ao macro e às metas, não substitui o detalhe do NEKT. Pagine todas as consultas e registre cobertura.

## Saídas

- `02-midia.md`
- `bases/cobertura-midia.md`
- `bases/canais.md`
- `bases/destinos.md`
- `bases/campanhas.md`
- `bases/conjuntos.md`
- `bases/anuncios.md`
- `bases/breakdowns.md`

## Análise

1. Separe quarter, pré-go-live e performance; calcule KPIs e rankings somente a partir de `analysis_start`.
2. Reconcilie investimento total e por canal.
3. Compare Google, Meta e demais canais pelo resultado completo.
4. Estratifique rede, estratégia, destino, campanha, conjunto/ad group, anúncio e público/keyword.
5. Inclua região, idade, gênero, dispositivo e posicionamento quando disponíveis.
6. Separe formulário nativo, landing page, site, WhatsApp e outros destinos.
7. Recalcule CPM, CTR, CPC, CPL, CPMQL, CPSQL, CPVenda e ROAS conforme disponibilidade.
8. Para vídeo, inclua hook rate, hold rate e conclusão.
9. Gere rankings por lentes diferentes, sempre mostrando o funil inteiro.
10. Inclua todas as entidades com investimento, mesmo quando leads, MQL, SQL ou vendas forem zero.
11. Reconcilie investimento e contagens entre geral, canal, campanha, conjunto e anúncio; registre diferença absoluta, percentual e causa.
12. Preencha a matriz de cobertura dimensional antes de escrever qualquer resumo executivo.

Não compare objetivos incompatíveis. Campanha sem maturação suficiente continua visível com confiança reduzida.
Não use agregado do quarter que misture pré e pós-go-live como resultado do projeto. Mostre-o somente como contexto separado.

## Gate de completude

- Ranking não substitui base completa.
- Não marque o módulo como `complete` sem 100% das entidades com investimento inventariadas em campanha, conjunto e anúncio.
- Não marque como `complete` se uma dimensão aplicável estiver `partial` ou `unavailable`.
- Métrica ausente é `sem dado`, nunca zero, e deve aparecer na matriz de cobertura com fonte solicitada e próximo passo. Toda dimensão `partial` ou `unavailable` gera uma lacuna `cobertura-midia:<dimensão>` em `decisoes.md`.
- Se NEKT estiver indisponível, tente a conexão autorizada e registre lacuna em `decisoes.md` com o export/API ou input manual necessário. Fontes alternativas podem sustentar análise numérica somente com proveniência e confiança explícitas; assets e previews seguem o contrato do NEKT.
- IDs ausentes exigem match por nome documentado; não omita a coluna de ID.

## Output

Mostre geral → canal → rede/estratégia → destino → campanha → conjunto → anúncio/criativo → público/keyword → breakdowns. Cada vencedor ou perdedor aponta para evidência e referência de meta, histórico ou break-even. Vincule a narrativa às bases completas.
