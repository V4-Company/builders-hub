---
name: account-retrospectiva-performance-maestro
description: Orquestra uma retrospectiva trimestral auditável e orientada a dados para clientes de inside sales ou e-commerce, cruzando contexto, mídia, criativos, CRM, atendimento, vendedores, GA4, e-commerce, metas e break-even. Use sempre que o usuário pedir retrospectiva do quarter, melhores e piores campanhas, canais, públicos, anúncios, funil, atendimento, produtos, projetado versus realizado ou insumos comprovados para iniciar um ROPRE Quarter. Roda de ponta a ponta por cliente sem paradas intermediárias, registra cada decisão assumida e concentra a validação humana no final, antes de liberar o adaptador do ROPRE.
area: account
author: junioraiellogestaodetrafego-maker
version: 2.0.0
---

# Account Retrospectiva de Performance — Maestro

Orquestre a retrospectiva como workflow independente. Ela explica **o que aconteceu, o que funcionou, o que falhou e onde estão os gaps**. O ROPRE decide depois como agir, priorizar e planejar.

## Contratos obrigatórios

Antes de executar, leia completamente:

- `references/modo-autonomo.md`
- `references/contrato-markdown.md`
- `references/fontes-e-reconciliacao.md`
- `references/metricas-e-rankings.md`
- `references/cobertura-midia.md` quando mídia fizer parte do escopo
- `references/profundidade-entrega.md`
- `references/janelas-temporais.md`
- `references/modelos-negocio.md`
- `references/atendimento.md` quando houver operação comercial ou ferramenta conversacional
- `references/qualidade-comercial.md` quando houver operação comercial ou ferramenta conversacional
- `references/qa.md` antes de finalizar

## Escopo

- Modelos aceitos: `inside_sales` e `ecommerce`.
- Período é parâmetro obrigatório e pode ser qualquer intervalo.
- Quarter calendário e janela de performance são conceitos separados. Descubra go-live, primeiro evento real e mudanças estruturais; julgue performance somente a partir de `analysis_start` conforme `references/janelas-temporais.md`.
- Comparação obrigatória: projetado versus realizado.
- Comparações opcionais: período versus período, quarter versus quarter, canal versus canal, campanha versus campanha e destino versus destino.
- Saída canônica: somente Markdown e assets binários referenciados. JSON/CSV podem existir como cache interno, nunca como entrega canônica.
- Profundidade padrão: `exhaustive`. Resumo executivo é uma camada adicional, nunca substituta dos módulos, tabelas-mãe, bases ou evidências.

## Modo de execução

`execution_mode: autonomous` é o padrão: a execução roda do primeiro ao último módulo sem perguntar nada no meio. A única parada antes do fim é o pré-voo, quando o cliente não puder ser identificado de forma única. Use `execution_mode: interactive` somente se o usuário pedir paradas intermediárias.

## Descoberta e decisões registradas

1. Varra o repositório profissional do cliente.
2. Consulte, quando autorizados, Flow, Cockpit, NEKT, GrowthPack e Drive.
3. Use conexões n8n para CRM, GA4, e-commerce e ferramenta conversacional quando disponíveis.
4. Gere o manifesto de fontes antes de analisar.
5. Determine quarter, pré-operacional, go-live técnico e primeiro evento real antes de calcular performance.
6. Onde antes havia sabatina ou gate, aplique a escolha mais bem evidenciada, siga em frente e registre a linha em `decisoes.md` conforme `references/modo-autonomo.md`.

MQL, SQL, venda, horário comercial, margem, fee e metas variam por cliente: descubra, aplique e registre como `evidenciada`, `assumida` ou lacuna. Não invente definição sem base; sem base, é lacuna.

## Ordem de execução

1. `account-retrospectiva-contexto-fontes`
2. `account-retrospectiva-midia`
3. `account-retrospectiva-criativos`
4. Para inside sales:
   - `account-retrospectiva-funil-inside-sales`
   - `account-retrospectiva-atendimento`, quando houver dados conversacionais
   - `account-retrospectiva-vendedores`
5. Para e-commerce: `account-retrospectiva-ecommerce`
6. `account-retrospectiva-breakeven`
7. `account-retrospectiva-reconciliacao`
8. `account-retrospectiva-evidencias`
9. `account-retrospectiva-achados-gaps`
10. `account-retrospectiva-consolidacao`
11. `account-retrospectiva-drive-handoff`

Módulo sem fonte suficiente gera lacuna em `decisoes.md` e a execução continua nos demais módulos, mas ele não recebe status `complete`. Dado de mídia ausente nunca autoriza resumo substitutivo: aplique o gate de cobertura de `references/cobertura-midia.md`, registre fonte esperada e próximo passo (conector, API, export ou input manual) e mantenha a retrospectiva como `partial` até a lacuna ser resolvida ou aceita nominalmente na validação final.

Na frente comercial, mantenha execução operacional, competência comercial e resultado de funil como julgamentos separados. Localize a rubrica aprovada do cliente; se não houver, gere o rascunho a partir de `assets/rubrica-comercial-cliente.md`, permita a análise operacional e marque a competência como `provisional` até a calibração humana.

## Diretório da execução

Use:

```text
checkins/quarter/{ano}/Q{n}/retrospectiva-performance/{run_id}/
```

`run_id` segue `AAAA-MM-DDTHHMMSS-03`. Nunca sobrescreva uma execução anterior.

## Validação humana única

Os pontos abaixo continuam exigindo validação humana, mas no modo autônomo ela acontece de uma vez, no pacote final de `decisoes.md`:

- tipo de negócio quando não for comprovável;
- definições de MQL, SQL, oportunidade, orçamento e venda;
- fonte oficial em conflito material;
- fee, verba e MC1 usados no break-even;
- seguir sem dado crítico (aceite nominal de lacuna);
- `retrospectiva aprovada`, que libera o adaptador do ROPRE.

Publicação externa no Drive tem autorização própria, separada da aprovação.

Correção humana nunca edita a execução existente: gere nova `run_id` com `parent_run_id` e recalcule a partir do primeiro módulo afetado, conforme o mapa de recálculo de `references/modo-autonomo.md`.

## Gate obrigatório de granularidade

Quando houver mídia, não consolide antes de existir `bases/cobertura-midia.md`. A cobertura deve declarar, uma a uma, as dimensões geral, canal, rede/subcanal, estratégia, destino, campanha, conjunto/ad group, anúncio, criativo, público/keyword, região, gênero, idade, dispositivo e posicionamento.

Exija as bases aplicáveis de canais, destinos, campanhas, conjuntos, anúncios e breakdowns. Inclua todas as entidades com investimento no período, inclusive as que tiveram zero conversão. Um ranking resumido nunca substitui a tabela-mãe.

Não aplique top N como recorte da entrega. Gere rankings integrais e preserve também intermediários, perdedores, zero resultado, não atribuídos, amostra insuficiente e não avaliáveis. Se o Markdown ficar extenso, divida em partes com índice; não descarte linhas.

Ao fim da execução autônoma, execute:

```text
validate_retrospectiva.py <run_dir> --review-ready
```

Ele exige `decisoes.md` válido e garante que todo módulo não `complete` e toda dimensão de mídia `partial` ou `unavailable` tenham lacuna registrada. Corrija sozinho as falhas estruturais e só então apresente o pacote de validação.

Depois das respostas humanas, execute:

```text
validate_retrospectiva.py <run_dir> --approval-ready
```

Ele bloqueia decisões `assumida` e lacunas `aberta`. Módulo `partial` ou `blocked` só passa com lacuna `aceita` nominalmente. Não peça o comando `retrospectiva aprovada` enquanto esse gate falhar; mostre exatamente quais IDs, dimensões, métricas, entidades ou fontes ainda bloqueiam.

A aprovação da retrospectiva não substitui a aprovação da rubrica comercial. Para publicar score definitivo de competência, registre a versão calibrada, o aprovador e os resultados da amostra.

## Depois da aprovação

`retrospectiva aprovada` registrada com `--approval-ready` OK libera o adaptador `account-ropre-quarter-retrospectiva` sem nova pergunta: ele gera `12-handoff-ropre.md` e os arquivos do ROPRE. Se a retrospectiva veio do ROPRE, devolva o controle ao `account-ropre-quarter-maestro`. Se foi execução independente, encerre informando que o handoff está pronto para iniciar o ROPRE Quarter. O handoff de Drive só acontece se o usuário pedir e autorizar a escrita.

## Guardrails

- NEKT é a fonte de mídia e dos assets de criativos. Não use fonte alternativa para baixar criativos sem aprovação.
- Use first paid touch como atribuição oficial de aquisição.
- Preserve valor bruto, valor normalizado, regra de match e confiança.
- Nunca esconda não atribuídos, conflitos ou baixa cobertura.
- Um ranking mostra o funil inteiro; a métrica de ordenação não apaga as etapas seguintes.
- Não transforme correlação em causa. Marque causa não comprovada como hipótese.
- Não dilua pós-go-live com dados pré-operacionais. Preserve onboarding e implantação como contexto, exclua testes comprovados e documente a coorte válida.
- Não crie plano, dono, prioridade ou prazo: entregue achados e gaps para o ROPRE.

Consulte `references/workflow-detalhado.md` para a visão ponta a ponta e para os fluxos específicos de descoberta, inside sales, e-commerce, evidências e handoff.
