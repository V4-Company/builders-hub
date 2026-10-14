# Contrato Markdown da retrospectiva

## Frontmatter obrigatório

Todo arquivo canônico começa com:

```yaml
---
schema_version: "1.0"
module: "nome-do-modulo"
client_id: "identificador-estavel"
period_start: "AAAA-MM-DD"
period_end: "AAAA-MM-DD"
analysis_start: "AAAA-MM-DD"
run_id: "AAAA-MM-DDTHHMMSS-03"
generated_at: "AAAA-MM-DDTHH:MM:SS-03:00"
status: "complete|partial|blocked"
business_model: "inside_sales|ecommerce"
---
```

Campos opcionais: `execution_mode` (`autonomous|interactive`), `parent_run_id` (execução corrigida que originou esta) e `inherited_from` (módulo herdado sem recálculo da execução-mãe).

## Seções universais

1. Escopo
2. Fontes consultadas
3. Cobertura
4. Dados consolidados
5. Análise
6. Evidências
7. Lacunas
8. Conflitos
9. Observações de confiabilidade
10. Output para o próximo módulo

## Profundidade padrão

Use `detail_policy: exhaustive` como premissa da execução. Resumos são cumulativos com a análise detalhada e nunca substituem tabelas, bases ou evidências. Leia `profundidade-entrega.md`.

## Janela de análise

`period_start` e `period_end` descrevem o escopo calendário do arquivo. `analysis_start` marca o primeiro dia válido para julgamento de performance. Leia `janelas-temporais.md`; pré-go-live e testes não entram silenciosamente nos resultados.

## Identificadores

Use IDs estáveis sempre que existirem:

- `source_record_id`
- `lead_id`
- `contact_id`
- `deal_id`
- `conversation_id`
- `seller_id`
- `campaign_id`
- `adset_id` ou `ad_group_id`
- `ad_id`
- `creative_id`
- `product_id` e `variant_id`
- `evidence_id`

Não substitua ID por nome. Nome é dimensão descritiva e fallback de match.

## Formatos

- Datas: ISO 8601.
- Fuso padrão: `America/Sao_Paulo`, salvo configuração do cliente.
- Dinheiro: número decimal canônico mais moeda explícita; apresentação pode usar `R$`.
- Percentuais: informe numerador e denominador na base de evidência.
- Campos ausentes: `sem dado`, nunca zero.
- Divisão por zero: `não aplicável`.

## Árvore canônica

```text
00-manifesto-fontes.md
01-contexto-cliente.md
02-midia.md
03-criativos.md
04-funil-inside-sales.md | 04-ecommerce.md
05-vendedores.md
06-atendimento.md
07-breakeven.md
08-reconciliacao.md
09-evidencias.md
10-achados-gaps.md
11-retrospectiva-final.md
12-handoff-ropre.md
13-drive-handoff.md
decisoes.md
bases/
  cobertura-midia.md
  canais.md
  destinos.md
  campanhas.md
  conjuntos.md
  anuncios.md
  breakdowns.md
  leads-negocios.md
  conversas.md
  produtos.md
assets/criativos/
```

Gere apenas os arquivos aplicáveis. Registre os omitidos e o motivo no manifesto.

Quando houver mídia, `cobertura-midia.md`, `canais.md`, `destinos.md`, `campanhas.md`, `conjuntos.md`, `anuncios.md` e `breakdowns.md` são aplicáveis por definição. Se a fonte não entregar uma dimensão, mantenha o arquivo com status `partial` ou `blocked`; não o omita.

## Tabelas extensas

- Uma linha representa uma entidade ou evento claramente definido.
- Declare a granularidade acima da tabela.
- Não misture linhas de lead, negócio e conversa na mesma tabela.
- Se o volume exceder o limite prático do Markdown, divida em `parte-001.md`, `parte-002.md` e mantenha um índice.
- Não aplique top N para reduzir a entrega. Preserve a tabela integral nas bases ou partes versionadas.
- Preserve links clicáveis para CRM, conversa, campanha, anúncio, criativo e pedido.
- Bases com telefone, e-mail ou conteúdo de conversa ficam em acesso restrito; a narrativa para cliente mascara dados pessoais que não sejam necessários à prova.

### Contrato de `bases/conversas.md`

Uma linha representa uma conversa normalizada. Além dos identificadores aplicáveis, preserve:

- `evaluation_status` e motivo;
- autor e timestamps das mensagens relevantes;
- tempos corrido e útil;
- estado, cadência, `operational_score` e cobertura operacional;
- dimensões comerciais, `commercial_score`, cobertura, status de calibração e `rubric_version`;
- resultado do funil em campos separados;
- severidades P0–P4, confiança e revisão humana;
- links da conversa e do card;
- IDs das mensagens/eventos e `evidence_id`.

Não escreva `commercial_score` definitivo quando a rubrica estiver em rascunho ou calibração. Não produza uma nota única combinando execução, competência e resultado.

## Ledger de decisões

`decisoes.md` é obrigatório em toda execução. Ele registra cada escolha inferida, conflito resolvido por precedência e lacuna, e é a base da validação humana única. O contrato completo está em `modo-autonomo.md`.

## Proveniência

Cada conclusão referencia um ou mais `evidence_id`. Cada evidência registra fonte, timestamp de extração, período, chave de origem e link quando existir.

## Handoff Drive

`13-drive-handoff.md` apenas descreve a publicação. Não publica sem autorização. Deve mapear:

| Arquivo Markdown | Destino | Tipo | Nome/aba | Versão | Status |
|---|---|---|---|---|---|

Narrativa vai para Google Docs; tabelas extensas vão para Google Sheets; assets vão para a pasta versionada do cliente.
