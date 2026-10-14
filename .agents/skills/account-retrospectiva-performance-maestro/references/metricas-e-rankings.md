# Métricas e rankings

## Fórmulas canônicas

```text
CPM = investimento / impressões * 1.000
CTR = cliques no link / impressões
CPC = investimento / cliques no link
CPL = investimento / leads
CPMQL = investimento / MQLs
CPSQL = investimento / SQLs
CPO = investimento / oportunidades
CPOrçamento = investimento / orçamentos
CPVenda = investimento / vendas atribuídas
ROAS = receita atribuída / investimento
Hook rate = reproduções de 3 segundos / impressões
Hold rate = visualizações de 15 segundos / reproduções de 3 segundos
```

Para vídeo menor que 15 segundos, use conclusão do vídeo dividida por reproduções iniciadas e rotule a fórmula.

Guarde métricas nativas, mas recalcule as canônicas para comparação. Use `CPVenda`, não `CPV`, para evitar ambiguidade com custo por visualização.

## Macro até micro

Leia também `cobertura-midia.md`. A hierarquia abaixo é um contrato de coleta, não apenas uma sugestão narrativa.

Analise nesta ordem:

```text
overall
→ canal
→ rede/subcanal
→ estratégia
→ destino
→ campanha
→ conjunto/ad group
→ anúncio
→ criativo
→ público/keyword
→ região, gênero, idade, dispositivo e posicionamento
```

Estratégias e destinos incluem prospecção, remarketing, marca, formulário nativo, landing page, site, WhatsApp e app.

Cada nível aplicável gera uma base completa ou uma linha explícita de indisponibilidade na matriz de cobertura. Não substitua campanha, conjunto ou anúncio por uma seleção de top performers.

## Ranking de campanha

Crie uma tabela-mãe com o funil completo e múltiplas lentes de ordenação:

- investimento;
- leads e CPL;
- MQLs e CPMQL;
- SQLs e CPSQL;
- oportunidades e custo;
- orçamentos e custo;
- vendas e CPVenda;
- receita e ROAS.

Uma campanha pode vencer em CPL e perder em CPMQL ou CPVenda. Nunca esconda isso. Investigue quebras posteriores: qualidade, timing, follow-up, vendedor, ciclo, atribuição e maturação da coorte.

Repita a tabela-mãe para conjuntos e anúncios. Inclua entidades com investimento e zero resultado. Para anúncios, apresente tanto anúncio × conjunto quanto o criativo consolidado entre conjuntos.

Ordene a tabela integral por cada lente relevante. Top 3/5/10 pode aparecer como destaque, mas nunca substitui as linhas restantes nem remove entidades intermediárias, perdedoras, inconclusivas ou de zero resultado.

## Julgamento contextual

Não use volume mínimo global como veredito principal. Contextualize por:

- verba planejada e realizada;
- meta do custo;
- histórico no GrowthPack e NEKT;
- break-even;
- maturação do ciclo;
- volume economicamente possível.

```text
eventos_esperados = investimento_realizado / custo_meta
cumprimento_volume = eventos_realizados / eventos_esperados
desvio_custo = (custo_realizado - custo_meta) / custo_meta
indice_eficiencia = custo_meta / custo_realizado
```

Separe dois julgamentos:

- resultado contra plano: superou, bateu, não bateu, sem meta;
- confiança: alta, média, baixa, amostra insuficiente.

Baixa amostra reduz a força da generalização, mas não apaga o desvio contra uma meta financiada e executada.

## Comparabilidade

Compare entidades com objetivo, período, destino, definição de conversão e atribuição compatíveis. Campanha de awareness não perde por CPL; campanha de venda não vence apenas por CTR.

Leia `janelas-temporais.md`. Quando o go-live acontecer dentro do quarter, calcule rankings a partir de `analysis_start`; dados anteriores aparecem apenas em uma lente pré-operacional separada. Exclua testes comprovados e não compare janela pós-go-live parcial com meta trimestral integral sem proporcionalidade ou meta oficial compatível.
