---
name: account-retrospectiva-ecommerce
description: Reconstrói a retrospectiva de e-commerce por canal, campanha, produto, categoria, SKU e funil do site, cruzando mídia, GA4, plataforma de loja, pedidos, receita, ticket, margem e estoque. Use em todo cliente de e-commerce durante a retrospectiva do quarter.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.1.0
---

# Retrospectiva de e-commerce

Leia `modelos-negocio.md`, `fontes-e-reconciliacao.md`, `metricas-e-rankings.md` e `contrato-markdown.md` do maestro.

## Saídas

- `04-ecommerce.md`
- `bases/produtos.md`
- `bases/pedidos.md` quando houver granularidade segura

## Workflow

1. Cruze NEKT, GA4 e plataforma de e-commerce.
2. Separe tráfego pago, não pago e total.
3. Declare pedido, compra aprovada, venda faturada, cancelamento e reembolso, e registre cada definição em `decisoes.md` como `definicao_funil` (`evidenciada` ou `assumida`).
4. Reconcilie investimento, pedidos, vendas e receita por origem.
5. Analise canal, campanha, destino, categoria, produto, SKU e variante.
6. Compare sessões, taxa de conversão, ticket, receita, ROAS e CPVenda.
7. Inclua margem, estoque, cancelamento e reembolso quando disponíveis.
8. Identifique produtos com muito tráfego e baixa conversão, pouco tráfego e alta conversão, alto ticket e contribuição relevante.

Não aplique o funil pago às sessões orgânicas. Mostre divergências entre GA4, plataforma e atribuição de mídia em vez de somá-las.
