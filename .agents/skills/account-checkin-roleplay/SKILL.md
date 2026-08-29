---
name: account-checkin-roleplay
description: Prepara o account pra reunião de check-in com cliente seguindo ROPRE V2 e roda roleplay realista simulando as personas reais do cliente. Use sempre que o usuário mencionar reunião de check-in, ROPRE, preparar call com cliente, ensaio de reunião, ou disser que tem check-in marcado, amanhã, hoje, essa semana — mesmo que não fale "roleplay" explicitamente. Também use quando o usuário quiser revisar pauta de check-in, treinar resposta a cliente difícil, ou diagnosticar por que check-ins têm saído fracos.
area: account
author: guilhermelippert
version: 1.0.0
---

# Account — Check-in Roleplay

Skill que faz o account chegar 80% pronto pra reunião de check-in **e** ensaiar contra a persona real do cliente antes da call. Ataca a causa raiz do check-in fraco: preparação correndo e zero ensaio.

## O que essa skill produz

1. **Pauta ROPRE V2 personalizada** pro check-in da próxima call (estrutura, pesos por bloco, roteiro narrativo)
2. **Lista de 3–5 ataques esperados** do cliente + script de defesa pra cada
3. **Roleplay realista** — simula as personas do cliente em conversa, dá feedback em tempo real onde o account titubeou
4. **Arquivo em `checkins/`** — salva pauta, ataques e pontos fracos em `checkins/{YYYY-MM-DD}-prep-roleplay.md`
5. **Atualizações na KB** — atualiza `personas-call.md` se aprendeu algo novo, adiciona entrada em `historico-preparacoes.md`

Fora de escopo (fase 2): geração do PPT/HTML formal do check-in.

## Pré-requisito: Mission Control do cliente

A skill ASSUME que existe a pasta `mission-control/` na raiz da KB do cliente, com 5 arquivos centrais:

```
squads/{squad}/clientes/{cliente}/mission-control/
├── okr-quarter.md         # OKRs do quarter atual
├── apostas-vivas.md       # tabela das apostas estratégicas
├── combinados.md          # combinados pendentes/feitos com dono+prazo
├── personas-call.md       # voz, gatilhos, padrões de provocação dos stakeholders
└── historico-checkins.md  # log curto de cada check-in real (1 linha + link)
```

Se não existir ou estiver incompleta → **aborto inteligente** (passo 2 abaixo).

Esta skill tambem pode criar/atualizar `historico-preparacoes.md`, mas esse arquivo nao e pre-requisito. Ele separa ensaios de calls reais para nao poluir `historico-checkins.md`.

Mission Control é mantido por outra skill (`/contexto` estendida) e atualizado a cada run desta skill e da `account-checkin-review`. Cada arquivo é atômico — pode ser atualizado isoladamente.

## Fluxo

### Passo 1 — Identificar cliente e localizar KB

Pergunte qual cliente se o usuário não disser. Localize em `squads/{squad}/clientes/{cliente}/`. Confirme com o usuário antes de seguir.

### Passo 2 — Validar Mission Control (aborto inteligente)

Leia os 5 arquivos. Para cada um que faltar ou estiver vazio, ofereça 3 opções ao account:

- **(a) preencher inline agora** — a skill pergunta os dados na conversa e cria/atualiza o arquivo
- **(b) parar e ir alimentar a KB primeiro** — recomenda rodar `/contexto` se houver kickoff e transcripts recentes
- **(c) seguir mesmo assim** — a skill avisa explicitamente "esse check-in vai sair fraco em [X]" e segue com o que tem

O ato de listar o que falta + oferecer (a) é a pressão saudável que mantém a KB viva ao longo do tempo. Não é defeito — é feature.

### Passo 3 — Coletar dados frescos do período

O account fornece (ou a skill consulta via outras skills se disponíveis):

- **Resultados Meta** (CTR, CPM, CPL, leads — ideal puxar via `v4mos-dados-meta-ads` se existir)
- **Resultados Google**
- **Status dos combinados anteriores** (compara com `combinados.md` — quais foram feitos, quais não, quais estão em andamento)
- **Status das apostas vivas** (de `apostas-vivas.md` — alguma tem prazo de leitura nesse período?)

### Passo 4 — Declarar o modo (TEM vs SEM resultado)

Pergunte ao account: **"Esse check-in é modo TEM resultado ou SEM resultado?"**

**Confronte se houver contradição** com os números: se o account declarou TEM mas o gap vs OKR mostra atraso significativo (ex: -30% ou mais), pergunte: *"Você declarou TEM, mas estamos a {gap}% do alvo do quarter. Tem certeza que é modo TEM? Modo SEM nesse caso te dá um roteiro mais honesto."*

A declaração explícita é o que muda a postura do account na call. Não automatize esse passo.

Se for caso misto (algumas frentes batendo, outras não), trate como SEM no global, mas dentro de R/O destaque as frentes que TÊM resultado pra escalar. O modo SEM não é "tudo perdido" — é "honestidade primeiro, próxima aposta forte depois".

### Passo 5 — Montar a pauta ROPRE V2

A estrutura completa, na ordem:

```
Ritual+ → Onde paramos → R → O → P+R(Apostas Vivas) → E → Combinados
```

**Ritual+** estende o oficial com uma re-âncora rápida de OKR (30s). Antes do "posso seguir o protocolo?", o account fala: *"Nosso alvo do quarter é {X}. Estamos no mês {N} de 3."* Isso pré-carrega o cérebro do cliente — o R que vem depois é julgado contra o alvo, não no vácuo.

**Pesos por bloco e modo** (pauta de ~45min):

| Bloco | Modo TEM | Modo SEM | O que fazer |
|---|---|---|---|
| Onde paramos | 3min | 5min | Status dos combinados anteriores. Modo SEM: enfatizar o que NÓS cumprimos (estabelece moral antes do banho frio). |
| R Resultados | 15min | 8min | Vitórias + aprendizados. Modo SEM: corte a conversa fiada de vitória menor. Honestidade. |
| O Objetivos | 5min | 5min | OKRs. Comece pelo melhor, depois o pior com plano. Modo SEM: sem maquiar — "estamos atrás. Aqui está por quê." |
| P+R Apostas Vivas | 8min | **18min** | Status das apostas, quais morreram, quais nasceram. Modo SEM: **vira o coração da call**. |
| E Entregas | 8min | **2min** | Modo SEM: lista mínima, sem teatro. Esconder atrás de E é o pecado do garçom. |
| Combinados | 6min | 7min | Decisões com dono+prazo. Modo SEM: **inclui commitment do cliente** (criativo, oferta, autorização). |

Para cada bloco, a skill produz:
- **Que dados/slides apresentar**
- **Roteiro narrativo** (o que falar, em prosa que o account possa adaptar)
- **Pontos críticos** (o que NÃO esquecer)
- **Onde o cliente provavelmente vai atacar** (extraído de `personas-call.md`)

### Passo 6 — Roleplay realista

Leia `personas-call.md` pra carregar voz, gatilhos e padrões de provocação dos stakeholders. Simule **as personas reais do cliente** — não um cliente genérico chato.

**Sem nível de agressividade ajustável** — vai direto no realista. Treino fácil é teatro e não prepara pro cliente real.

**Se `personas-call.md` estiver vazio** (cliente nunca teve check-in salvo), ofereça os 4 arquétipos abaixo e peça pro account marcar quais se parecem com cada stakeholder do cliente:

- **Decisor agressivo** — sócio/CEO, provoca, quer escalar verba, questiona métricas, traz tese de mercado
- **Operacional cético** — gestor da operação do cliente, foco em qualidade de lead, pede microajustes em LP/criativo
- **Estrategista** — discute tese, posicionamento, mercado, oferta — quer debater estratégia mais que números
- **Passivo** — silencioso, só aprova; o desafio é fazê-lo se posicionar (senão vira cliente que cancela do nada)

Account pode marcar múltiplos arquétipos se a call tem mais de uma persona. Salve a escolha em `personas-call.md` pra próximas execuções (com data e nota: "arquétipo inicial declarado pelo account; refinar com base nas próximas calls").

**Loop de roleplay:**

1. Skill apresenta um bloco da pauta como se fosse o account na call (narração curta).
2. Skill assume a voz da persona e provoca/pergunta.
3. Account responde.
4. Skill dá feedback explícito: *"Resposta forte"* ou *"Resposta fraca em {X}, tente assim: {script}"*.
5. Próxima provocação. Repete por bloco.

A skill deve fazer pelo menos **3–5 provocações no total**, distribuídas pelos blocos onde a persona costuma atacar. Concentre nas dores históricas extraídas dos transcripts anteriores.

### Passo 7 — Atualizar a KB

Após o roleplay:

- Se aprendeu algo novo da persona (gatilho novo, frase recorrente, padrão), atualize `personas-call.md`.
- Adicione entrada em `historico-preparacoes.md`: `[YYYY-MM-DD] preparação rodada — modo: {TEM/SEM} — pontos fracos identificados: {breve}`. Se o arquivo nao existir, crie com titulo `# Histórico de Preparações de Check-in`.

Use `Edit` (não `Write`) pra preservar histórico.

### Passo 8 — Entregar o pacote final

Devolva ao account:

1. **Pauta ROPRE V2 em markdown** — pode ser printado, colado no slide, ou usado como roteiro mental
2. **Lista de 3–5 ataques esperados + scripts de defesa** — pra o account memorizar antes da call
3. **Resumo de pontos fracos do ensaio** — onde titubeou, o que treinar de novo se sobrar tempo
4. **Recomendação de próxima ação** — ex: "rodar de novo daqui 2h se sentir que não fixou", ou "tá pronto, vai com confiança"

Tambem salve esse pacote em `checkins/{YYYY-MM-DD}-prep-roleplay.md`. Se `checkins/` nao existir, crie. Nao salve pauta/ensaio em `calls/`; `calls/` e so para transcript bruto.

## Apostas Vivas — schema obrigatório

Cada aposta em `apostas-vivas.md` tem 4 campos:

| Aposta (o que cremos) | Por quê apostamos | Como mata (sinal + prazo) | Plano B se morrer |
|---|---|---|---|
| Tese específica e testável | Evidência ou hipótese que sustenta | Métrica + threshold + data limite | Próxima ação concreta se a aposta cair |

**Limite:** 3 a 5 apostas vivas simultâneas. Menos que 3 = você não está testando nada, só executando. Mais que 5 = ninguém consegue acompanhar critério de morte de cada uma.

## Output exemplo (modo TEM, anonimizado)

```markdown
# Check-in Cliente X — 2026-05-08
**Modo:** TEM resultado | **Quarter:** Q2 (mês 2 de 3) | **Personas ativas:** Decisor agressivo + Operacional cético

## 0. Ritual de abertura (2min)
- Tech check + saudação V4
- Re-âncora OKR: "alvo Q2 = 200 contratos; mês 2 de 3"
- "Posso seguir o protocolo?"

## 1. Onde paramos (3min)
**Combinados da última call:**
- [✓] Designer entrega 3 vídeos novos até 18/04
- [✗] Cliente grava depoimento — pendente
- [→] Em andamento: nova LP para frente Y

**Provoque:** "{Operacional}, o depoimento que combinamos ficou pra essa semana?"

## 2. Resultados (15min)
[dados, comparativo MoM, vitórias do período]

## 3. Objetivos (5min)
[OKR melhor → OKR pior + plano de ação]

## 4. Apostas Vivas (8min)
| Aposta | Status | Próximo passo |
| LP > formulário nativo | CONFIRMADA — CPL R$45 vs R$67 | Escalar 30% verba |
| Persona A converte > Persona B | EM TESTE — leitura dia 25/04 | Manter split |
| Frente Z escala em maio | NASCENDO — primeiros testes | Definir orçamento inicial |

## 5. Entregas (8min)
[lista breve + matriz esforço×resultado se houver pedido novo]

## 6. Combinados (6min)
**Vão pra mission-control/combinados.md:**
- [ ] Account valida criativo X até 12/05
- [ ] Cliente grava depoimento até 15/05
- [ ] Definir verba Q3 na próxima call

---

## ATAQUES ESPERADOS

### Ataque 1 (Decisor agressivo): "CTR baixou. Não dá pra subir CPM e ter mais alcance?"
**Defesa:** "CTR baixo isolado não preocupa — é correlato do filtro de público. Se subirmos CPM, atingimos gente menos qualificada e CPL real piora. O que faz sentido testar é {ação concreta}."

### Ataque 2 (Decisor agressivo): "Quero estourar verba na frente Y."
**Defesa:** "Faz sentido escalar, mas a aposta atual ainda está em janela de leitura até dia 25. Proposta: subimos {Y}% por 2 semanas e medimos. Se CPL se mantém, dobra. Se piora, volta."

### Ataque 3 (Operacional cético): "Os leads do form nativo estão vindo sem telefone — não consigo abordar."
**Defesa:** "Identificamos isso semana passada. Já fizemos o ajuste no form X. Vamos monitorar essa semana; se persistir, plano B é Y."

---

## PONTOS FRACOS DO ENSAIO
- Titubeou no ataque 1 — falta de confiança no argumento técnico de CTR. Treinar mais 1x.
- Resposta de "estourar verba" foi defensiva. Reformular pra propositiva: oferecer caminho, não só negar.
```

## Quando o output deve mudar

- **Cliente novo / sem histórico:** ofereça arquétipos de persona, peça contexto adicional (kickoff, planejamento), avise que a primeira call vai ser mais exploratória.
- **Quarter close / fechamento de trimestre:** estenda o bloco O (Objetivos) — discussão estratégica do trimestre todo, não só do mês. Pesos: O ganha 5min extra, R perde 5min.
- **Cliente em risco de churn:** modo SEM com Combinados forçando commitment do cliente (sem isso ele só assiste e cancela). Skill deve flagar isso explicitamente no início do output.

## Princípio central — garçom vs médico

Doutrina V4: garçom anota pedidos e relata tarefas. Médico investiga, diagnostica, prescreve. Esta skill existe pra fazer o account chegar como médico, não como garçom.

Se a pauta gerada está cheia de "tarefas entregues" e pouca diagnose, **a skill falhou**. Volte e reescreva o bloco R/E forçando narrativa de "o que isso significa pro negócio do cliente".

## Conexão com outras skills

- **`/contexto`** (estendido) — cria/atualiza Mission Control. Pré-requisito desta skill.
- **`account-checkin-review`** — roda DEPOIS da call real, atualiza `combinados.md`, `apostas-vivas.md`, `historico-checkins.md`, `personas-call.md`. Fecha o ciclo. Preparações ficam em `historico-preparacoes.md`.
- **`v4mos-dados-meta-ads`** — puxa dados Meta frescos pro Passo 3 se disponível.
- **`account-handoff`** — roda no início da relação com cliente, gera o input zero do Mission Control (OKR do quarter, primeiras apostas).
