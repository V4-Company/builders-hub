---
name: account-retrospectiva-funil-inside-sales
description: Reconstrói o funil de inside sales lead a lead, com MQL, conexão, SQL, oportunidade, orçamento, venda, receita, UTMs e maturação. Use em retrospectivas de clientes com CRM e operação comercial, antes das análises de vendedores e atendimento.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.2.0
---

# Funil de inside sales

Leia `modelos-negocio.md`, `fontes-e-reconciliacao.md`, `janelas-temporais.md` e `contrato-markdown.md` do maestro.

## Saídas

- `04-funil-inside-sales.md`
- `bases/leads-negocios.md`

## Workflow

1. Descubra as definições do cliente para MQL, SQL, oportunidade, orçamento e venda, aplique a mais bem evidenciada e registre cada uma em `decisoes.md` como `definicao_funil`. Sem base para uma etapa, registre lacuna; não invente regra.
2. Aplique `analysis_start`; mantenha pré-go-live fora das taxas de performance.
3. Extraia leads, contatos, negócios, estágios, timestamps, vendedor, valor, origem e links.
4. Identifique e exclua testes comprovados por ID; preserve-os numa base de exclusões. Se a fonte agregada não permitir exclusão, declare impacto máximo e mantenha `partial`.
5. Preserve data de criação e fechamento; declare qual rege cada análise.
6. Resolva duplicidades sem apagar registros brutos.
7. Aplique first paid touch e mantenha não atribuídos.
8. Calcule volume, taxas, custos e tempo entre etapas.
9. Analise por canal, campanha, destino, vendedor, região e período.
10. Considere ciclo e maturação antes de chamar uma campanha de pior.

## Funil

Use as etapas reais do cliente. A cadeia de referência é:

```text
lead → MQL → conexão → SQL → oportunidade → orçamento/proposta → venda → receita
```

Conexão pode ocorrer antes de MQL. Se a ordem gerar taxa impossível, trate como problema de semântica ou denominador, mostre as duas leituras e registre decisão `definicao_funil` de criticidade alta.
