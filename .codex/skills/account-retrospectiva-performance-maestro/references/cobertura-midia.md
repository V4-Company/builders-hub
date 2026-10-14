# Cobertura obrigatória de mídia

Este contrato impede que uma retrospectiva resumida esconda dimensões, entidades ou métricas ausentes.

## Matriz obrigatória

Crie `bases/cobertura-midia.md` antes da análise. Inclua exatamente estas dimensões:

```text
overall
canal
rede_subcanal
estrategia
destino
campanha
conjunto
anuncio
criativo
publico_keyword
regiao
genero
idade
dispositivo
posicionamento
```

Para cada dimensão registre:

| dimensão | aplicável | status | fonte esperada | fonte usada | cobertura temporal | entidades esperadas | entidades coletadas | cobertura % | métricas disponíveis | métricas ausentes | causa | próximo passo | evidência |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|---|---|

Status aceitos:

- `complete`: período completo e todas as entidades aplicáveis coletadas;
- `partial`: período, entidades ou campos incompletos;
- `unavailable`: fonte aplicável não entregou o dado;
- `not_applicable`: dimensão realmente não existe no canal/estratégia, com justificativa.

Nunca use `not_applicable` apenas porque o conector não trouxe o campo.

## Bases obrigatórias quando houver mídia

- `bases/canais.md` — geral, canal, rede/subcanal e investimento.
- `bases/destinos.md` — estratégia, objetivo e destino.
- `bases/campanhas.md` — uma linha por campanha e janela comparável.
- `bases/conjuntos.md` — uma linha por conjunto/ad group e janela comparável.
- `bases/anuncios.md` — uma linha por anúncio × conjunto; inclua também a consolidação do criativo entre conjuntos.
- `bases/breakdowns.md` — público/keyword, região, gênero, idade, dispositivo e posicionamento.
- `bases/cobertura-midia.md` — matriz de cobertura e reconciliação.

Base sem dados continua existindo com status `blocked` ou `partial`, schema, motivo e solicitação de fonte. Não omita o arquivo.

## Colunas mínimas do funil

Campanha, conjunto e anúncio preservam, quando aplicáveis:

```text
period_start, period_end, channel, network, strategy, objective, destination,
campaign_id, campaign_name, adset_id/ad_group_id, adset_name,
ad_id, ad_name, creative_id, creative_name,
audience/keyword, region, gender, age, device, placement,
spend, impressions, clicks, CPM, CTR, CPC,
leads, CPL, MQL, CPMQL, SQL, CPSQL,
opportunities, CPO, budgets, CPBudget,
sales, CPVenda, revenue, ROAS,
source, evidence_id, match_rule, confidence, maturity_status
```

Campo indisponível permanece como `sem dado`; zero é reservado a contagem comprovadamente nula.

## Inventário e reconciliação

1. Pagine o período inteiro.
2. Inclua 100% das entidades que tiveram investimento, mesmo com zero resultado ou zero conversão.
3. Conte entidades esperadas e coletadas em cada nível.
4. Reconcilie investimento geral → canal → campanha → conjunto → anúncio.
5. Use como tolerância padrão o maior entre R$ 1,00 e 1% do investimento do nível pai. Diferença superior exige conflito explícito.
6. Reconcilie leads e eventos de funil por fonte; não force equivalência entre eventos nativos diferentes.
7. Preserve IDs. Quando ausentes, registre o match por nome, regra e confiança.

## Gate de completude

O módulo de mídia só pode ser `complete` quando:

- a matriz contém todas as 15 dimensões;
- todas as dimensões aplicáveis estão `complete`;
- 100% das campanhas, conjuntos e anúncios com investimento aparecem nas bases;
- investimento está reconciliado dentro da tolerância ou o conflito foi resolvido;
- rankings usam as bases completas e mostram o funil inteiro;
- ausências de métricas estão explicitadas, sem zero inventado;
- fontes, período, extração e evidências estão registrados.

Se qualquer item falhar, use `partial` ou `blocked`, solicite o dado e impeça o gate `--approval-ready`.
