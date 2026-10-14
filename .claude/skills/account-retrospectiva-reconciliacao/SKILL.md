---
name: account-retrospectiva-reconciliacao
description: Reconcilia mídia, CRM, conversas, GA4 e e-commerce em uma trilha única, resolvendo identidade, first paid touch, UTMs, IDs, links e diferenças entre fontes com confiança explícita. Use depois das coletas especializadas e antes de produzir conclusões da retrospectiva.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.1.0
---

# Reconciliação

Leia `fontes-e-reconciliacao.md` e `contrato-markdown.md` do maestro.

## Saída

- `08-reconciliacao.md`
- atualização das bases com chaves reconciliadas

## Workflow

1. Preserve tabelas e valores brutos.
2. Normalize telefone, e-mail, UTMs, URLs e nomes sem apagar o original.
3. Resolva identidade entre lead, contato, negócio, conversa e pedido.
4. Aplique first paid touch para aquisição.
5. Cruze campanha, conjunto/ad group, anúncio e criativo com NEKT.
6. Classifique cada match e sua confiança.
7. Meça cobertura: atribuídos, não atribuídos, ambíguos, duplicados e sem fonte.
8. Produza tabela de conflitos com impacto analítico.
9. Registre em `decisoes.md` cada conflito material resolvido por precedência (`fonte_oficial`) e cada mapeamento inferido (`atribuicao`), com as duas leituras quando o custo de calcular for baixo.

Não force correspondência. Nome isolado exige revisão. Link, telefone e e-mail podem identificar a pessoa; a campanha ainda precisa de UTM, ID, URL, origem ou mapeamento validado.
