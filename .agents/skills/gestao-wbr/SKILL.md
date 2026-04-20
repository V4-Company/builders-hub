---
name: gestao-wbr
description: Gera o documento completo do WBR (Weekly Business Review) de uma tribo ou operação V4 a partir dos dados do DRE e informações fornecidas pelo gestor. Use sempre que o usuário pedir para montar, preparar ou redigir o WBR da semana, mencionar dados de churn/monetização/NPS/pessoas para apresentar à diretoria, ou quiser atualizar o relatório semanal da operação. A skill monta análise comparativa semana atual vs anterior, FCAs por desvio e tabela de monetização no formato pronto para apresentação.
area: gestao
author: hellenoliveira-sys
version: 2.0.0
---

# gestao-wbr — WBR Weekly Business Review

Gera o documento semanal do WBR de uma tribo ou operação V4, pronto para apresentação à diretoria.

## Contexto

- **Quando é apresentado:** Tipicamente às terças-feiras para a diretoria
- **Dados chegam:** Health Score preenchido pelos coordenadores (geralmente às segundas). Churn, monetização, MRR e NPS vêm do DRE da operação.
- **Objetivo da reunião:** Garantir previsibilidade de retenção e monetização conectando leading indicators → resultado financeiro, sempre gerando FCA (Fato, Causa, Ação) para cada desvio.

## DRE — Fonte de dados automática

**Antes de pedir qualquer número ao gestor**, tente ler o DRE via Google Drive MCP:

- **File ID:** peça ao gestor o ID da planilha de DRE (formato: string alfanumérica do link do Google Sheets)
- **Ferramenta:** `mcp__claude_ai_Google_Drive__read_file_content`

A planilha normalmente tem uma linha por mês/squad. Filtre pelo mês atual e extraia as colunas relevantes para o WBR:

| Dado no WBR | Coluna típica no DRE |
|---|---|
| Churn MRR (R$) | `Churn MRR` |
| Logos perdidas | `Logo Churn` |
| % Logo Churn | `% de Logo Churn` |
| MRR do mês | `MRR Início do Mês` |
| Variável Realizado | `Variável Realizado` |
| Upsell Realizado | `Upsell de Clientes` |
| One Time / Produto | `Escopo Fechado Realizado` |
| Total Monetização | `Total de Monetização Realizada` |
| Meta Monetização | `Meta de Monetização e Variável` |
| NRR | `NRR` |
| LT Médio | `LT Médio dos Projetos` |
| % Projetos Green Flag | `% dos Projetos em Green Flag` |
| Média CSAT | `Média de CSAT` |
| Média NPS | `Média de NPS` |
| % Respostas NPS/CSAT | `% de clientes com CSAT/NPS com respostas` |

Se o DRE não estiver acessível ou os nomes das colunas forem diferentes, adapte ou peça os dados ao gestor.

Após ler o DRE, pergunte ao gestor apenas o que **não está na planilha**: lista de logos perdidas por nome, logos em tratativa, atualizações de pessoas, health score e plano de ação da semana anterior.

## Estrutura do WBR

O documento tem 7 seções obrigatórias:

1. **Indicadores Antecipadores — Health Score** (flags por status e por squad)
2. **Churn MRR** (logos perdidas, downsell, em tratativa)
3. **Monetização** (tabela por categoria + FCA se houver desvio)
4. **NPS/CSAT** (respostas coletadas vs meta + FCA)
5. **Pessoas** (atualizações de saída, risco, desempenho + FCA)
6. **Validação do Plano de Ação** (compromissos da semana anterior)
7. **Encerramento** (o que mudará essa semana + indicador de melhora)

## Como usar esta skill

### Passo 1 — Ler o DRE automaticamente

Use o Google Drive MCP para ler o DRE. Filtre as linhas do mês atual por squad e consolide os totais da tribo/operação.

Se o DRE não estiver acessível, peça os dados ao gestor.

### Passo 2 — Perguntar só o que falta

Com o DRE em mãos, pergunte apenas:
- Lista de logos perdidas por nome (o DRE tem o total, mas não os nomes)
- Logos em tratativa para reversão
- Atualizações de pessoas (desligamentos, riscos, contratações)
- Health Score por squad (se não vier do DRE)
- O que foi comprometido na semana anterior e o que mudou

### Passo 3 — Montar o documento com FCAs

Siga o template abaixo. Para cada seção:
- Se há dados → preencha com análise comparativa e FCA
- Se não há dados → marque claramente como pendente

Toda vez que houver desvio relevante (aceleração de churn, meta abaixo, flag subindo, pessoa em risco), escreva um FCA no formato:

**Fato:** o que os números mostram objetivamente
**Causa:** por que isso aconteceu (raiz, não sintoma)
**Ação:** o que será feito, por quem e até quando

## Template do documento

```
# WBR [Nome da Tribo/Operação] — [DATA]

**Objetivo:** Garantir previsibilidade de retenção e monetização conectando leading indicators → resultado financeiro, gerando FCA para cada desvio.

---

## 1. Indicadores Antecipadores — Health Score

[Tabela geral: Status | Semana anterior | Semana atual | Variação]
[Percentuais da carteira]
[Tabela por squad com análise de cada coordenador]

*(Se dados não disponíveis: "Dados disponíveis após preenchimento dos coordenadores")*

---

## 2. Churn MRR

**Logos perdidas no mês ([N]):**
[lista de logos]

**Downsell:** [lista]

**Total churn:** R$[valor]

**Em tratativa (possibilidade de reversão):** [lista]

### FCA Churn MRR
**Fato:** [comparativo semana anterior vs atual]
**Causa:** [raiz do problema]
**Ação:** [o que será feito, responsável, prazo]

---

## 3. Monetização

| Indicador | Realizado | Meta | % |
|---|---|---|---|
| Receita Total | R$X | R$X | X% |
| Upsell (bookado) | R$X | — | X% |
| Upsell (recebido) | R$X | — | — |
| Variáveis | R$X | Meta variável | X% |
| One Time / Produto | R$X | R$X | X% |

[Destaques positivos e pontos críticos]

### FCA [Indicador com desvio]
**Fato:** [o que os números mostram]
**Causa:** [raiz]
**Ação:** [ação, responsável, prazo]

---

## 4. NPS/CSAT

**Respostas coletadas:** [N] de meta [N]

[Análise e ponto de atenção se abaixo da meta]

### FCA NPS/CSAT (se necessário)
**Fato:** [situação]
**Causa:** [raiz]
**Ação:** [ação]

---

## 5. Pessoas

[Lista de situações por pessoa: nome, squad, status, observação]

### FCA Pessoas — [Colaborador] ([Squad])
**Fato:** [situação objetiva]
**Causa:** [raiz]
**Ação:** [próximos passos: data desligamento, plano absorção carteira, contratação]

---

## 6. Validação do Plano de Ação — Semana Anterior

| Compromisso | Status |
|---|---|
| [compromisso] | Concluído / Em andamento / Pendente |

---

## 7. Encerramento — O que mudará essa semana

- [Lista de mudanças comprometidas]

**Indicador que provará melhora:** [métrica específica]
```

## Regras importantes

- **Nunca invente dados.** Se o gestor não forneceu um número, marque como pendente.
- **FCA obrigatório para todo desvio relevante:** churn acelerando, meta abaixo de 50%, flag crítica subindo, pessoa em risco.
- **Análise comparativa sempre que houver dados de duas semanas.** Destaque variações positivas E negativas.
- **Tom direto e executivo.** O documento é lido pela diretoria — sem rodeios, com clareza nos pontos de atenção.
- **Se alguma seção estiver incompleta,** pergunte ao gestor se quer publicar assim ou aguardar os dados.

## Exemplo de uso

**Gestor diz:** "Churn MRR: R$49k — 10 logos perdidas. Monetização total em 80% da meta, variáveis em 143%, one time só 3,6%. NPS: 16 respostas de meta 20. Pessoas: Colaborador A será desligado por desempenho abaixo da média."

**Skill gera:** Documento completo com tabela de monetização, FCA do One Time (gap vs meta), FCA do churn (variação de logos na semana), FCA do Colaborador A (desempenho inviável para a carteira atual), e NPS com ponto de atenção para fechar as respostas restantes.
