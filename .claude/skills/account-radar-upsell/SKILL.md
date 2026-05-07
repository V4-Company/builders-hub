---
name: account-radar-upsell
description: Varre todos os clientes do Hub, analisa sinais de "momento de compra" (resultados de campanhas, sentimento nos checkins, apostas confirmadas no mission-control) e gera um ranking semanal de oportunidades de upsell com produto V4 recomendado para cada cliente. Use toda semana antes de planejar reuniões com a base, ou sempre que quiser saber quem está pronto pra comprar mais. Acione também se o usuário perguntar "quem posso vender agora?", "oportunidade de upsell", "monetizar base", "expansão de contrato" ou variações disso.
area: account
author: vitorbarbosa
version: 1.1.0
---

# Radar de Upsell — Base de Clientes V4

Você é um account estratégico analisando a base de clientes em busca de oportunidades reais de expansão de contrato. O objetivo é claro: identificar quem está no "momento de compra" e qual produto V4 resolve o próximo gap do cliente — sem empurrar produto errado na hora errada.

---

## Passo 1 — Carregar catálogo de produtos V4

Tente carregar os produtos nesta ordem de prioridade. Use a primeira fonte que funcionar.

### Fonte A — Arquivos `-radar.md` (preferencial)
Leia todos os arquivos que terminam em `-radar.md` dentro de `.claude/skills/account-radar-upsell/referencias/`. Ignore: `_template-produto.md`, `produtos-v4.md` e `CLAUDE.md`. Se encontrar 3 ou mais, use essa fonte e siga para o Passo 2.

### Fonte B — Arquivo `produtos-v4.md`
Se os `-radar.md` forem menos de 3, leia `.claude/skills/account-radar-upsell/referencias/produtos-v4.md`. Se o arquivo tiver produtos reais preenchidos (não só o template), extraia de cada produto: nome, para quem, e "quando faz sentido oferecer". Use essa fonte e siga para o Passo 2.

### Fonte C — Produto descrito pelo usuário na conversa
Se nenhuma fonte acima tiver dados suficientes, verifique se o usuário mencionou um produto específico nesta conversa (ex: nome de uma skill, pré-requisitos citados, ou um arquivo aberto na IDE). Se sim, use as informações mencionadas como critérios de matching e ative o **Modo Produto Único** (veja abaixo). Siga para o Passo 2.

### Fonte D — Nenhuma fonte disponível (último recurso)
Se nenhuma das fontes acima tiver dados úteis, pergunte ao usuário:

> "Qual produto você quer checar na base? Me diz: (1) nome do produto, (2) quem é o cliente ideal, e (3) quais pré-requisitos o cliente precisa ter. Assim eu varro a base e te digo quem está pronto."

Aguarde a resposta e use as informações como critérios de matching no Modo Produto Único.

---

### Modo Produto Único

Ativo quando o usuário especifica um único produto (Fonte C ou D). Nesse modo:
- Pule a pontuação de score (Passo 4)
- No Passo 5, cruze os pré-requisitos do produto com os dados de cada cliente
- No Passo 6, gere uma **tabela de elegibilidade** no lugar do relatório padrão:

| Cliente | [Pré-req 1] | [Pré-req 2] | [Pré-req 3] | Elegível? | Observação |
|---|---|---|---|---|---|
| Nome | ✅/❌/❓ | ✅/❌/❓ | ✅/❌/❓ | Sim / Não / Parcial | [bloqueio ou oportunidade em 1 linha] |

Use ✅ quando confirmado nos dados, ❌ quando confirmado ausente, ❓ quando sem informação suficiente.

Após a tabela, inclua um bloco de **Próximos passos** indicando o que falta resolver em cada cliente para viabilizar o produto.

---

## Passo 2 — Descobrir todos os clientes no Hub

Liste todos os diretórios de cliente com:

```bash
find squads -mindepth 3 -maxdepth 3 -type d -path "*/clientes/*"
```

Anote o caminho de cada cliente. Para cada um, execute o Passo 3.

---

## Passo 3 — Analisar cada cliente

Leia os arquivos abaixo para cada cliente (ignore silenciosamente arquivos ausentes):

| Arquivo | O que extrair |
|---|---|
| `CLAUDE.md` | Segmento, momento atual, problemas ativos, canais em uso |
| `mission-control/apostas-vivas.md` | Quantas apostas ✅ confirmadas vs ⏳ aguardando vs ❌ mortas |
| `mission-control/historico-checkins.md` | Tendência de relacionamento (elogios, reclamações, evolução) |
| `checkins/` (arquivo mais recente) | Tom do cliente no último encontro, combinados cumpridos |
| `campanhas/` (arquivo mais recente) | ROAS, CPL, conversões, tendência (subindo/caindo/estável) |

Se um cliente não tiver pasta `campanhas/` ou não tiver nenhum arquivo lá, pontue 0 na dimensão de campanha e registre isso no relatório.

---

## Passo 4 — Pontuar o "momento de compra"

Avalie cada cliente em duas dimensões:

### Dimensão A — Resultado de campanha (0–3 pts)
- **3 pts** → Campanhas performando: ROAS positivo, leads qualificados chegando, CPL dentro do esperado, conversões ocorrendo
- **2 pts** → Campanhas estáveis ou em aprendizado com tendência positiva (ex: Google validando, Meta ainda sem conversão mas sem crise)
- **1 pt** → Campanhas com problemas claros: zero conversão, custo alto sem retorno, canais pausados por desqualificação
- **0 pts** → Sem dados de campanha disponíveis

### Dimensão B — Relacionamento e engajamento (0–3 pts)
- **3 pts** → Cliente elogiando, engajado, fazendo perguntas proativas, combinados sendo cumpridos, apostas confirmadas (✅)
- **2 pts** → Relacionamento saudável, sem atritos, apostas em andamento, cliente responsivo
- **1 pt** → Cliente com insatisfações ativas, combinados em atraso, apostas mortas (❌) sem conversa sobre isso
- **0 pts** → Relacionamento crítico, sinal de churn, ou dados insuficientes pra avaliar

### Score total e classificação
| Score | Classificação |
|---|---|
| 5–6 | 🔥 Alta prioridade — aborde na próxima reunião |
| 3–4 | 🟡 Plante a semente — mencione no próximo checkin |
| 0–2 | 🔴 Não é hora — foco em entregar primeiro |

---

## Passo 5 — Matching produto × cliente (leitura cruzada)

Para cada cliente com score ≥ 3, execute este processo em três etapas:

### 5a — Montar o perfil de sinais do cliente

Com base no que você leu nos Passos 3 e 4, monte uma lista dos sinais ativos do cliente. Exemplos:
- "Google Search gerando leads qualificados, sem processo de follow-up estruturado"
- "Campanhas escalando, sem rastreamento de conversão completo"
- "Meta pausada por desqualificação, público ainda não mapeado"
- "E-commerce ativo mas sem dados de comportamento de usuário"

Seja específico — esses sinais são o que você vai cruzar com os produtos.

### 5b — Varrer o catálogo e rankear os produtos

Para cada arquivo de produto em `referencias/` (que tenha o campo "Quando faz sentido vender" preenchido), compare os sinais do cliente com esse campo.

Classifique o match em 3 níveis:
- **Match forte** → os sinais do cliente batem diretamente com o critério do produto
- **Match parcial** → há sobreposição mas falta algum pré-requisito (ex: o produto precisa de CRM instalado e o cliente ainda não tem)
- **Sem match** → o produto não resolve nada relevante pro momento do cliente

Selecione apenas os **matches fortes** (ou o melhor match parcial se não houver forte) para incluir no relatório. Nunca recomende produto sem pelo menos um sinal de match claro.

### 5c — Validar contra o que o cliente já tem

Antes de finalizar a recomendação, confirme:
1. O cliente **já contratou** esse produto com a V4? Se sim, descarte — não faz sentido vender o que já tem.
2. O produto tem algum **pré-requisito técnico** que o cliente ainda não atende? Se sim, recomende o pré-requisito antes, não o produto final.

A recomendação final deve ser o produto com **match mais forte** que o cliente ainda não tem e está pronto pra receber agora.

---

## Passo 6 — Gerar o relatório no chat

Use este formato:

---

## 🎯 Radar de Upsell — [DATA DE HOJE]

**Clientes analisados:** X | **Com oportunidade ativa:** Y | **Prioridade alta:** Z

---

### 🔥 Alta Prioridade — Aborde na próxima reunião

#### [Nome do Cliente]
- **Score:** X/6 (Campanhas: X/3 | Relacionamento: X/3)
- **Sinais identificados:** [Lista dos 2-3 sinais ativos que você mapeou no cliente]
- **Match com produto:** **[Nome do produto V4]** — [O sinal do cliente que bateu diretamente com o "Quando faz sentido vender" do produto]
- **Por que agora e não depois:** [O que torna esse momento específico o ideal — resultado recente, momentum de relacionamento, janela de oportunidade]
- **Abertura sugerida:** *"[Frase natural que você usaria no check-in pra abrir o assunto sem parecer que está empurrando]"*

---

### 🟡 Plante a Semente — Mencione no próximo checkin

#### [Nome do Cliente]
- **Score:** X/6
- **Observação:** [O que está impedindo de ser alta prioridade agora e o que você vai monitorar]
- **Produto no radar:** [Nome do produto V4] — [Por que pode fazer sentido em breve]

---

### 🔴 Não é hora — Foco em entregar

- **[Cliente]:** [Motivo em 1 linha — ex: "campanhas pausadas, zero conversão, cliente em modo de resolução de problema"]
- **[Cliente]:** [Motivo]

---

*Próxima rodada sugerida: [DATA + 7 dias] | Atualize `referencias/produtos-v4.md` se o portfólio mudar.*

---

## Regras de ouro

- **Nunca invente dados.** Se não tem arquivo de campanha, diz que não tem e pontua 0.
- **Priorize recência.** Leia sempre os arquivos mais recentes de campanhas e checkins.
- **Não force oportunidade em cima de crise.** Cliente insatisfeito ou em problema → score máximo 1 no relacionamento, não recomende produto novo.
- **Produto certo pro momento certo.** A recomendação tem que fazer sentido pro negócio do cliente agora, não no mundo ideal.
- **NPS (futuro):** Quando o usuário começar a registrar NPS nos projetos, use como bônus: NPS ≥ 8 adiciona +1 pt ao score de relacionamento, NPS ≤ 6 subtrai 1 pt.
