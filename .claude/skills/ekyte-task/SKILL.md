---
name: ekyte-task
description: Cria tarefas no Ekyte automaticamente via MCP, com briefing estruturado seguindo o padrão Colli&Co (Oficial). Use quando o Fabio pedir "criar/subir/abrir tarefa(s) no ekyte" — em texto livre ("quero 5 criativos ads pro Cliente I com foco em remarketing") OU apontando aba da planilha de demandas. Sempre mostra preview antes de disparar e bloqueia criação fora dos 8 workspaces conhecidos sem confirmação explícita.
area: ekyte
author: fabio
version: 1.0.0
user-invocable: true
---

# /ekyte-task — Criar tarefas no Ekyte com briefing estruturado

Sobe tarefas no Ekyte via MCP `ekyte`, com briefing oficial puxado do próprio ekyte e título no formato `[NN][SIGLA][IA] Cliente | Demanda`. Substitui o trabalho manual de 15 min por task por preview + 1 confirmação.

## Quando usar

Use quando o Fabio:
- Disser "cria/sobe/abre uma task no ekyte de [tipo] pro [cliente]"
- Pedir lote de tasks ("sobe 5 criativos pro Cliente A")
- Falar "tá na aba [nome] da planilha de demandas, sobe tudo"
- Mencionar `/ekyte-task` ou `ekyte-task`

**Não use** quando o pedido é só consultar dados do ekyte (listar projetos, listar workspaces) — a MCP `ekyte` cobre direto sem precisar dessa skill.

## Pré-requisitos

- MCP `ekyte` configurada em `~/.claude/mcp.json` (já está)
- `clientes/_skill-ekyte/cache.md` — IDs de workspaces, projetos e tipos
- `clientes/_skill-ekyte/sla.md` — tabela de prazos por tipo
- `clientes/_skill-ekyte/flows.md` — **fluxo (fases) por tipo de tarefa** + dicionário `nome da fase → phaseId`. Usado pra mostrar o fluxo e pra trocar o responsável de uma etapa (passos 4.5 e 9.6).

## Os dois MCPs do Ekyte (a partir de 2026-06)

Há **dois servidores MCP do Ekyte** em `~/.claude/mcp.json`:

| Servidor | Prefixo | Uso nesta skill |
|---|---|---|
| `ekyte` (n8n) | `mcp__ekyte__*` | **Criação principal** via `create_task` com `situation=10` — cria já Ativa, sem gerar-tarefas REST. Também leitura, BI e edições pós-criação (`update_task`, `update_task_tags`, etc.). **Desde 2026-06-11 é o api.ekyte.com oficial, não mais n8n.** |
| `ekyte-oficial` (`api.ekyte.com`) | `mcp__ekyte-oficial__*` | Fallback/alternativo para operações não cobertas pelo prefixo `ekyte`. Token fixo na URL, não expira por uso. |

Regra prática: **usar `mcp__ekyte__create_task` com `situation=10`** para criar tasks Prisma — tarefa nasce Ativa diretamente, passo 9.5 (generate-tasks REST) é desnecessário. Para edição pós-criação (mover fase, trocar executor, aplicar tags), usar as tools `mcp__ekyte__update_*`.

**`phaseId` em `create_task`** pode ser qualquer fase do fluxo — não precisa ser Backlog. Usar a fase destino diretamente quando a task deve entrar já em Design (82181) ou outra fase avançada, ex: `phaseId: 82181, executorId: <andré>` com `phaseDueDate: hoje`.

## Fluxo ponta a ponta do cliente até a task briefada

A `/ekyte-task` é a ponta operacional da esteira: ela cria, ativa, ajusta e tagueia a tarefa no Ekyte. Para a task sair realmente briefada, ela deve se apoiar nas skills de base, contexto, NotebookLM e cache. Use este mapa quando o Fabio perguntar "qual fluxo usar" ou quando um cliente novo ainda não tem base suficiente.

### Esteira ideal

```text
/novo-cliente
-> /account-handoff
-> /account-pesquisa-profunda-cliente
-> /contexto
-> /notebooklm-cadastrar, se faltar NotebookLM
-> /ekyte-refresh
-> /ekyte-briefing-refresh
-> /ekyte-task
   -> /ekyte-briefing
      -> /cs-notebooklm-consulta-cliente
   -> preview obrigatório
   -> criar task
   -> ativar task
   -> aplicar responsáveis por etapa, se pedidos
   -> aplicar tags finais
```

### Como cada skill soma

- `/novo-cliente`: cria a pasta do cliente em `clientes/<cliente>/` com `CLAUDE.md`, `AGENTS.md`, `links.md`, `.env`, `calls/`, `checkins/`, `docs/` e `campanhas/`. Pode cadastrar NotebookLM, Drive, site e links úteis já na criação.
- `/account-handoff`: primeira leitura da transição vendas → operação. Consome form de kickoff, transcript da reunião comercial e proposta opcional para gerar KB preliminar, riscos, promessas, perguntas de kickoff, Mission Control preliminar e deck HTML.
- `/account-pesquisa-profunda-cliente`: depois que existem dados internos mínimos, consolida esses dados e entrega prompts para Gemini Deep Research sobre cliente, setor, consumidor e concorrência. Entra antes de demandas de copy, campanha, LP e posicionamento.
- `/contexto`: consolida a KB local do cliente. Lê `calls/`, `docs/`, `campanhas/`, `links.md` e atualiza `CLAUDE.md`, `AGENTS.md` e `mission-control/`.
- `/notebooklm-cadastrar`: adiciona ou troca o bloco `## NotebookLM` no `CLAUDE.md` de clientes existentes. Destrava `/cs-notebooklm-consulta-cliente` e, por consequência, `/ekyte-briefing`.
- `/ekyte-refresh`: atualiza `clientes/_skill-ekyte/cache.md` e `flows.md` com workspaces, projetos do trimestre, tipos de tarefa e fases. Destrava `workspace_id`, `project_id`, `task_type_id` e overrides de fase.
- `/ekyte-briefing-refresh`: atualiza `drives.md` e `backups-crm.md`, usados pela `/ekyte-briefing` para preencher links de Drive e planilhas de CRM.
- `/cs-notebooklm-consulta-cliente`: consulta o NotebookLM do cliente com até 5 perguntas direcionadas, salva artefato em `clientes/<cliente>/contexto-notebook/` e devolve síntese executiva.
- `/ekyte-briefing`: monta o briefing rico da task com template por sigla, Drive, NotebookLM, cache de público e perguntas ativas. Não cria task; devolve `briefing_ekyte_text` em HTML rico para o Ekyte.
- `/ekyte-task`: resolve cliente/projeto/tipo/SLA/título, chama `/ekyte-briefing`, mostra preview, cria a task, ativa no Ekyte, corrige etapa se necessário, aplica tags e atualiza cache.

### Regra prática

Se o cliente ainda é novo ou pouco documentado, não trate `/ekyte-task` como primeiro passo. Primeiro criar ou consolidar a base do cliente, cadastrar NotebookLM/Drive, atualizar caches do Ekyte e só então subir a tarefa.

Sem essa fundação, a skill ainda consegue criar uma task, mas a entrega tende a virar "pedido preenchido". Com a cadeia completa, a task nasce com contexto, público, objetivo, referências, riscos e guardrails.

## Fluxo

### 0) Pre-fly check (obrigatório em lotes ≥ 3 tasks)

**Antes** de carregar cache, ler input ou montar preview, fazer um varredura de pendências e reportar TUDO numa mensagem só. Em lotes a maior perda é round-trip — uma pergunta de cada vez transforma 5 min de trabalho em 30 min de chat.

**Princípio chave (lição 2026-05-05):** Fabio responde "pode seguir" pra listas de perguntas abertas — ele delega defaults. Em vez de fazer 5 perguntas, **propor defaults razoáveis inline** e pedir só "confirma ou ajusta?". Bloquear de verdade só pra coisas SEM default seguro.

Checar e propor:
1. **NotebookLM cadastrado** pra cada cliente do lote: `ls clientes/<x>/CLAUDE.md` + grep `## NotebookLM`. **SEM default automático** — se faltar, listar e perguntar: "Cliente D e Cliente F não têm NotebookLM cadastrado. Quer cadastrar agora, ou o gerente de projetos autoriza seguir sem NotebookLM?". Só seguir sem NotebookLM com comando explícito do gerente de projetos.
2. **Quantificação implícita**: se algum item menciona "X por produto", "todos os produtos", "fotos da categoria Y" ou similar — **SEM default seguro** — perguntar explícito: "Essas linhas de fotos viram 1 task com lote de N peças, ou quer que cada linha vire `[N×SKUs]` no título?"
3. **Workspaces fora dos 8 fixos**: **SEM default** — bloquear até confirmação explícita.
4. **Tipos com sigla ambígua** (CA, CJ, GP, MT, AUX, CRM, PMM, RI, SM, EV): **PROPOR default** baseado no contexto da demanda ("vou usar `34435` Configuração de CRM — match óbvio pra Chatwoot. Confirma ou ajusta?"). Não listar as 12 variantes pedindo escolha.
5. **SLA dos tipos sem entrada** na tabela: **PROPOR default** ("AN sem SLA tabelado — vou usar 3 dias úteis. Ok?"). Não perguntar aberto.
6. **Quantidade [NN] quando o lote indica claramente 1-task-1-entrega**: **PROPOR `[01]` direto** sem perguntar.

Formato preferido do pre-fly:
```
Vou seguir com defaults razoáveis:
- #X → tipo Y (justificativa de 1 linha)
- #Z → SLA W (justificativa)
Bloqueando só em: [item sem default seguro]
Confirma ou ajusta?
```

Sair desse passo só com **uma resposta consolidada** do Fabio (pode ser só "pode seguir").

### 1) Carregar contexto (sempre)

Logo no início, ler:
1. `clientes/_skill-ekyte/cache.md` — workspaces, projetos descobertos, tipos
2. `clientes/_skill-ekyte/sla.md` — SLA por sigla
3. `clientes/_skill-ekyte/flows.md` — fases por tipo + `nome da fase → phaseId` (carregar só quando o Fabio especificar responsável por etapa ou pedir o fluxo)

Não chamar a MCP do ekyte sem antes consultar o cache.

### 2) Identificar o modo de input

**Modo A — texto livre no chat:**
Exemplos:
- "cria uma task de criativos ads pro Cliente A com foco em remarketing produto X, 6 peças"
- "sobe 3 LPs pro Cliente C: blackfriday, prospect, retorno"
- "preciso de uma publicação de campanha pra Cliente E amanhã"

Extrair:
- **Cliente** (alias → workspace_id via cache)
- **Sigla/tipo** ("criativos ads" → CA → 29740)
- **Quantidade [NN]** ("3 LPs" → 03; default 01 se não especificado)
- **Demanda específica** (parte que vira o título depois do `|`)
- **Prazo** (default = SLA da tabela; sobrescrever se usuário disser "urgente", "amanhã", "X dias")

**Modo B — aba da planilha:**
Quando o Fabio disser "tá na aba `<nome>`" ou similar, ler:
- URL: `https://docs.google.com/spreadsheets/d/1SAWHbC3dog5_IrwCYY1_buF5yGtV_lMTiXL_v9iGrns/edit`
- Usar WebFetch com prompt pedindo: "lista todas as linhas da aba `<nome>` com colunas sequencial, titulo, data inicio, data entrega, tipo de tarefa (id), email executor, esforço, descricao, Qtd Peças, Tags, Fase"
- Cada linha vira 1 task. A planilha já tem o `task_type_id` numérico, datas em ISO, email do executor — **não precisa inferir IDs**.

### 3) Resolver workspace e projeto

**Workspace:**
- Procurar o cliente no cache (8 fixos + apelidos + workspaces internos)
- Se ambíguo (ex: usuário disse só "Cliente B" mas cache tem variações): perguntar qual
- Se não estiver nos 8 fixos NEM nos internos conhecidos: PARAR e pedir confirmação explícita ("Esse cliente não está na sua lista habitual. Confirma criar mesmo?"). **Workspaces internos recorrentes** (V4 Company / Billions Timesheet, qualquer setup interno V4 que o Fabio usa toda semana) ficam no cache na seção "Workspaces internos" e NÃO disparam essa confirmação.

**Projeto (Q vigente):**
- Padrão de nome: `<Cliente> | Q2/2026` (Q2 ativo até virar trimestre)
- Se já tem `project_id` no cache para esse workspace + período: usar
- Se não tem: marcar `projeto_novo: true` no pacote da task, chamar MCP `ekyte.listar_projetos_tool` com `workspace_id`, `created_from` = início do trimestre, `created_to` = fim do trimestre. Encontrar projeto cujo nome contém `Q2/2026`. Salvar no cache.
- Se aparecer >1 match: perguntar qual

**Regra de projeto novo:** quando o `project_id` não estava no cache no início do fluxo, tratar como projeto novo para a geração do briefing. Projeto novo **sempre** exige fluxo formal `/ekyte-briefing` + `/cs-notebooklm-consulta-cliente`; não usar modo inline rápido, briefing manual, nem script que não tenha síntese NotebookLM por task/cliente.

### 4) Resolver tipo de tarefa (sigla → task_type_id)

- Se o Fabio falou em palavras ("criativos ads"): mapear pra sigla (CA) e buscar no cache.
- Se a sigla tem 1 só ID: usar.
- Se a sigla tem múltiplos (CA, CJ, GP, MT, AUX, CRM, PMM, RI, SM): **desambiguação obrigatória** — listar opções e perguntar qual.
- Se não achar a sigla no cache: chamar `ekyte.listar_tipos_de_tarefas_tool({"name_type_task": "<termo>", "parameters1_Value": "3535"})` (workflow Padrão Colli&Co), filtrar resultado, perguntar.

**Caso especial WEB:** se o pedido é "demanda web", usar o título com `[WEB]` no slot da sigla. Tipo de tarefa = "Personalizada". Se ainda não temos `task_type_id` da Personalizada no cache, perguntar ao Fabio qual ID usar e salvar.

### 4.5) Fluxo da tarefa e responsável por etapa

Cada tipo tem um **fluxo de fases** (ex: CA = Briefing → Copywriter → Designer → … → Monitoramento), e cada fase tem um **executor default** que vem do tipo/workspace. Por padrão **não mexemos nisso** — a task nasce com os executores default do tipo. Só agimos quando o Fabio **especifica** um responsável pra uma etapa.

- **De onde vem o fluxo:** `clientes/_skill-ekyte/flows.md` lista, por sigla, as fases reais (com `phaseId`) em ordem, mais um dicionário mestre `nome da fase → phaseId`. O `phaseId` é global (compartilhado entre tipos: `1`=Briefing, `5`=Copywriter, `6`=Designer…). Se o tipo não estiver no `flows.md` (ou aparecer como "sem fases de esforço"), buscar em runtime com `mcp__ekyte-oficial__get_task_type_flow({"id": <task_type_id>})` e filtrar as fases com `effort`/`duration > 0`.

- **Quando o Fabio especifica responsável por etapa** — gatilhos como "o briefing fica com a Marina", "design com o João", "copy com fulano", "manda pro Pedro na publicação". Capturar isso como uma lista de overrides `{fase → pessoa}` por task. Resolver:
  - **fase → phaseId**: match (case-insensitive, parcial) no fluxo do tipo em `flows.md`. Se ambíguo (ex: "aprovação" casa com várias), perguntar qual.
  - **pessoa → userId (GUID)**: `mcp__ekyte-oficial__list_all_users_with_profile({"textSearch": "<nome>"})`. Se >1 match, desambiguar. Guardar o GUID.

- **Não aplicar agora** — só registrar os overrides. A troca de executor acontece **depois** da criação+ativação, no passo 9.6 (o `update_task_executor` precisa da task já existindo). Mostrar os overrides no preview (passo 8).

Se o Fabio **não** falar nada de responsável por etapa, pular 4.5 e 9.6 inteiros — comportamento idêntico ao de antes.

### 5) Montar o título

```
[NN][SIGLA][IA] Cliente | Demanda específica
```

Onde:
- `NN` = quantidade em 2 dígitos (`01`, `09`, `15`)
- `SIGLA` = sigla do tipo (CA, LP, PC, RV, GP…) ou `WEB` para personalizadas
- `[IA]` = sempre, marca que foi gerada via skill
- `Cliente` = nome curto do cliente (sem `[BILLIONS]`, sem brackets)
- `Demanda específica` = parte livre, descritiva

Exemplos:
- `[09][CA][IA] Cliente A | Remarketing produto X`
- `[01][LP][IA] Cliente C | Página obrigado transceivers`
- `[03][WEB][IA] Cliente B | Ajustes header e footer site institucional`

### 6) Montar o briefing (description) — **delegado pra `/ekyte-briefing`**

A partir de 2026-04-30, a montagem de briefing é responsabilidade da skill `/ekyte-briefing`. Esta skill (`/ekyte-task`) **não** monta mais o `description_create_task` por conta própria.

**Regra obrigatória a partir de 2026-06-15:** toda task criada pela `/ekyte-task` precisa passar pelo fluxo formal `/ekyte-briefing`. A consulta `/cs-notebooklm-consulta-cliente` é o **default obrigatório** para toda tarefa que não estiver na whitelist operacional abaixo. Não decidir pela quantidade de texto da OBS, pelo tipo de projeto ou por parecer uma demanda simples: se não estiver explicitamente isenta, consulta NotebookLM.

**Whitelist operacional sem NotebookLM:**
- Otimização de campanhas recorrente.
- Atualização de Growth Pack/GrowthPack recorrente.
- Apontamento de horas/timesheet.
- Atendimento/comunicação recorrente de rotina.
- Envio recorrente de NPS/CSAT.
- Atualização administrativa interna recorrente, sem decisão estratégica e sem necessidade de contexto do cliente.

**Regra de dúvida:** se houver qualquer componente de análise, criação, implementação, tracking, CRM, automação, projeção, campanha, público, pesquisa, planejamento ou decisão sobre o cliente, **não é exceção** e deve consultar NotebookLM. Projeto novo continua exigindo consulta mesmo que a descrição pareça operacional. Se faltar NotebookLM, login ou resposta válida numa tarefa não isenta, parar antes do preview de criação e pedir decisão: cadastrar/corrigir NotebookLM ou o gerente de projetos autorizar explicitamente seguir sem NotebookLM.

**Como invocar:** depois de resolver workspace, projeto, sigla e tipo (passos 3-4), montar o pacote de entrada e chamar `/ekyte-briefing`:

```json
{
  "cliente": "Cliente A",
  "cliente_alias": "cliente-a",
  "sigla": "CA",
  "task_type_name": "Criativo Ads",
  "task_type_id": "29740",
  "qtd": 9,
  "titulo": "[09][CA][IA] Cliente A | Remarketing produto X",
  "input_livre": "<input original do Fabio>",
  "modo": "texto_livre",          // ou "planilha_demandas" ou "5w1h"
  "projeto_novo": false,
  "notebook_obrigatorio": true,   // false somente para whitelist operacional
  "motivo_isencao_notebook": null,
  "planilha_5w1h_url": null,
  "planilha_demanda_row": null    // preenchido se modo=planilha_demandas
}
```

A `/ekyte-briefing` faz: carrega template da sigla, lê Drive em `drives.md`, consulta o NotebookLM quando `notebook_obrigatorio: true`, faz perguntas ativas em lote ao Fabio, monta briefing em Markdown e converte para HTML rico aceito pelo Ekyte. Quando `notebook_obrigatorio: false`, registra a isenção e monta o briefing com a descrição operacional, links de rotina e caches aplicáveis.

**Devolve:**
```json
{
  "briefing_ekyte_text": "<div><strong>Tarefa:</strong> ...</div><div><br></div>...",
  "briefing_markdown": "BRIEFING — ...",
  "campos_pendentes": [],
  "notebook_consultado": true,
  "notebook_isento": false,
  "notebook_artefato": "clientes/cliente-a/contexto-notebook/2026-04-30-1015-...md"
}
```

A `/ekyte-task` injeta `briefing_ekyte_text` direto em `description_create_task`/`description` na chamada de criação. **Não converter para texto plano e não remover HTML**.

**Importante (atualizado 2026-06-15):** o padrão atual de briefing no Ekyte é HTML rico simples. Seções principais devem virar `<div><strong><span style="font-size: 18px;">HEAD</span></strong></div>`, labels devem virar `<strong>Label:</strong>` no tamanho normal, links devem usar `<a>`, e listas devem usar `<ul><li>`. Não usar Markdown bruto nem `<h1>/<h2>`. CSS inline só é permitido nas heads para aumentar fonte. Se a API quebrar acentos, preferir texto ASCII dentro do HTML.

**Modo planilha de demandas (Modo B antigo):** quando o input vem da aba da planilha (`https://docs.google.com/.../edit`), a `/ekyte-task` extrai a linha (`descricao`, `task_type_id`, `email`, etc) e passa pra `/ekyte-briefing` com `modo: "planilha_demandas"` + `planilha_demanda_row` preenchido. Se a coluna `descricao` for substancial, a `/ekyte-briefing` usa como base e enriquece via NotebookLM. Se for vazia/genérica, monta do template normal.

**Modo 5W1H:** quando Fabio menciona link de planilha 5W1H ("plano de ação"), passar `modo: "5w1h"` + `planilha_5w1h_url`. A `/ekyte-briefing` valida o cabeçalho e usa layout 5W1H.

### 7) Calcular prazo e datas de etapa

Consultar `sla.md`:
- Tipo na tabela → `current_due_date_create_task` = hoje + SLA
- Tipo NÃO na tabela → perguntar no preview, ou usar default genérico (3 dias úteis) se o usuário disser "padrão"
- Usuário disse "urgente" / "amanhã" / data específica → sobrescrever

`phase_start_date_create_task` = sempre hoje.

**Regra crítica de datas no Ekyte (aprendizado 2026-06-02):**

- Task nova nunca pode nascer atrasada.
- O SLA entra no campo **"Concluir tarefa até"** (`current_due_date_create_task`).
- A etapa atual precisa ficar com **"Executar etapa até" = data de subida** (hoje), mesmo quando a tarefa tem SLA longo.
- Depois de criar e rodar "Gerar tarefas", conferir a resposta/listagem: se a etapa atual apareceu atrasada ou com data anterior a hoje, corrigir antes de encerrar. O Ekyte pode redistribuir fases para trás a partir do prazo final em tipos como LP/CA; não aceite esse estado como final.

### 8) Preview obrigatório

Antes de chamar `criar_tarefa_tool`, mostrar pra Fabio:

```
📋 PREVIEW — Task #1 de N

Workspace: Cliente A (id: 999001)
Projeto: Cliente A | Q2/2026 (id: <X>)
Tipo: [CA] Criativo Ads (id: 29740)
Responsável: seu.usuario@v4company.com
Início: 2026-04-28
Prazo: 2026-05-09 (SLA CA = 11 dias)

Título: [09][CA][IA] Cliente A | Remarketing produto X

Briefing:
<<resumo do briefing — primeiras 5 linhas>>
[ver completo abaixo]

Responsável por etapa (só quando especificado — passo 4.5):
  • Briefing (#1) → Marina Souza
  • Designer (#6) → João Pedro
  (demais fases ficam com o executor default do tipo)

Após criação: vou disparar `generate-tasks` no projeto pra
sair de "Não planejada" → "Ativa" automaticamente (passo 9.5),
e trocar o executor das etapas acima (passo 9.6).

---

Confirma criação + geração? (sim/não/editar)
```

Se for lote (modo B com planilha): mostrar tabela resumida (linha | título | tipo | prazo) e pedir aprovação **única** pro lote, OU "1 a 1" se o Fabio preferir.

**Nunca** dispara `criar_tarefa_tool` sem ver o "sim".

### 8.4) Modo Inline Rápido — desativado como bypass de briefing

O modo inline rápido antigo **não pode mais pular** `/ekyte-briefing`. Quando lote é **3-5 tasks** + a coluna `OBS/Descrição` da planilha já tem texto substancial (objetivo claro, link de transcrição/referência), usar isso como `planilha_demanda_row.descricao` e chamar `/ekyte-briefing` normalmente com `modo: "planilha_demandas"`.

Regra prática:
- Lote ≤5 + OBS substancial + cliente conhecido → `/ekyte-briefing` formal, usando a OBS como base e enriquecendo via NotebookLM/cache.
- Lote ≤5 + OBS vazia/genérica OU cliente/projeto novo → `/ekyte-briefing` formal obrigatório, tentando `/cs-notebooklm-consulta-cliente`; seguir sem NotebookLM só com autorização explícita do gerente de projetos.
- Lote ≥6 → modo script Python (8.5), mas o script só pode gerar textos depois que a síntese NotebookLM da `/ekyte-briefing` existir para cada cliente/linha relevante.

Motivo: briefing de task Ekyte não pode nascer só da OBS ou de interpretação manual quando existe NotebookLM do cliente. A OBS acelera o preenchimento; ela não substitui consulta.

Validado em 2026-05-05 com lote de 5 tasks (Cliente C x2 + Cliente D x3): 5 criações em paralelo, ~30s.

#### 8.4.1) Público vem do cache persistente, mas não substitui briefing

Lição 2026-05-14: a v1 do modo inline pulava NotebookLM totalmente — campo público acabava saindo "a consultar" ou genérico. Conflito direto com a regra [public sempre vem do NotebookLM](../../../memory/feedback_publico_notebook.md).

**Resolução:** a `/ekyte-briefing` consulta `clientes/<cliente>/publicos-cache.md` antes de montar briefing. Layout e TTL: ver [_publicos-cache-template.md](../../../clientes/_skill-ekyte/_publicos-cache-template.md). Cache de público pode evitar repetir pergunta de público, mas não elimina a obrigação de chamar `/ekyte-briefing`; em projeto novo, também não elimina a consulta `/cs-notebooklm-consulta-cliente`.

Fluxo:

1. **Identificar a linha** de cada task do lote (Colchões adultos / Cliente A Baby / Geral / etc).
2. **Para cada linha distinta no lote**, abrir o cache uma vez:
   - **HIT** (< 75d) → usa direto para público. O briefing formal ganha bloco "Público" preenchido (avatar + faixa + sexo + consciência + ganchos) com marcador `[do cache: <linha> · <N>d]`. Se `projeto_novo: true`, ainda consultar NotebookLM para contexto geral da task.
   - **STALE** (75-90d) → pergunta no pre-fly: `⚠️ cache de público da linha "Cliente A Baby" tem 78d. Atualizar antes do lote? (sim/não)`. Sem resposta = HIT silencioso.
   - **MISS** (≥ 90d OU inexistente) → invocar `/cs-notebooklm-consulta-cliente` **uma única vez por linha do lote**, com 1 pergunta dirigida só de público (não as 5 padrão). ~1min/linha. Após resposta, escrever bloco no cache.
3. **Não consultar NotebookLM mais de uma vez por linha por lote.** Se 4 tasks são todas "Colchões adultos", consulta roda 1x (no MISS) e as 4 reusam.

Quando MISS rola, o cache populado fica disponível pras próximas sessões — paga o investimento em 2-3 lotes. Mesmo com cache, a saída final precisa vir da `/ekyte-briefing`.

### 8.5) Modo Lote — script Python (≥6 tasks)

Quando o lote for ≥6 tasks, montar briefing na chat custa contexto e fica frágil. **Default a partir de 6:** gerar os textos via script Python parametrizado, mas somente depois de rodar `/ekyte-briefing` e obter síntese NotebookLM por cliente/linha relevante. O script reaproveita a síntese e os templates; ele não substitui a consulta.

Estrutura recomendada:
1. Criar pasta de trabalho `<workspace_user>/briefings-ekyte-<YYYY-MM-DD>/`.
2. Escrever `gerar_briefings.py` que define funções reaproveitáveis por padrão de demanda (ex: `web_pdp(cliente, ws_id, proj_id)`, `fotos(filename, qtd_por_sku, total_skus, ...)`) e chama essas funções pra cada task. Saída: 1 `.docx` por task (use `python-docx`).
3. Escrever `extrair_textos.py` que converte os .docx em HTML rico simples para Ekyte (`<div>`, `<strong>`, `<span style="font-size: 18px;">` somente em heads, `<a>`, `<ul>`, `<li>`; sem `<h1>/<h2>`). **Pular o bloco "Metadados (Ekyte)"** — esses dados já vão nos campos próprios da MCP. Salva tudo num `_briefings_textos.json` chave→HTML.
4. Disparar as MCP `criar_tarefa_tool` em paralelo (várias por mensagem) com `description_create_task` lendo do JSON gerado a partir da síntese aprovada.

Vantagens medidas (lote de 25 em 2026-05-04):
- Estrutura uniforme (toda task cobre Objetivo / Contexto / Escopo / Entregáveis / Perguntas / Referências).
- Reaproveitamento de padrão (8 fotos Cliente A = 1 função × 6 chamadas, não 6 briefings escritos à mão).
- Os .docx ficam de subproduto pro Fabio revisar antes do disparo se quiser.

### 9) Chamar a MCP

Após confirmação, chamar `ekyte.criar_tarefa_tool` com os 8 campos:

```json
{
  "workspace_id_create_task": "999001",
  "ctc_task_type_id_create_task": "29740",
  "user_email_create_task": "seu.usuario@v4company.com",
  "title_create_task": "[09][CA][IA] Cliente A | Remarketing produto X",
  "description_create_task": "<HTML rico formatado do briefing>",
  "current_due_date_create_task": "2026-05-09",
  "ctc_task_project_id_create_task": "<id do projeto>",
  "phase_start_date_create_task": "2026-04-28"
}
```

Reportar sucesso/erro de cada criação. Se erro: parar, mostrar a mensagem, não tentar a próxima sem aprovação.

### 9.5) Gerar tarefas (sair de "Não planejada" → "Ativa") — revisado 2026-06-17

> **Quando pular este passo:** se a task foi criada via `mcp__ekyte__create_task` com `situation=10`, ela já nasce Ativa — este passo inteiro pode ser ignorado. Confirmar com `list_tasks` filtrando `situation=10` se houver dúvida.

O passo abaixo é necessário apenas quando a criação foi feita pelo fluxo legado n8n (`criar_tarefa_tool`), que cria a task como **"Não planejada"** e exige ativação project-level via REST.

**Após ativar, validar datas de etapa:** na resposta do `generate-tasks` ou em listagem posterior, toda task criada nesta execução precisa ter a etapa atual sem atraso. A coluna **"Executar etapa até"** deve ser hoje (data da subida). A coluna **"Concluir tarefa até"** deve seguir o SLA/prazo final. Se o Ekyte gerar fase inicial no passado, corrigir imediatamente via ferramenta/API de edição de task/fase antes de finalizar o relatório.

> **Nota (MCP oficial):** o servidor `ekyte-oficial` expõe `create_task` com `situation=10` (cria já Ativa) e `update_task_phase` (move uma task específica de fase). Não substituem o "Gerar tarefas" project-level — são alternativas por-task que exigem montar o `flow`/`phaseId` na criação. Por ora mantemos a criação via `ekyte` (n8n) + ativação REST; o oficial fica como caminho de **edição/correção** pós-criação. Reavaliar migrar a criação inteira pro oficial quando o `flow` estiver mapeado no cache.

**Endpoint:**
```
POST https://api.ekyte.com/api/v2/companies/{company_id}/projects/{project_id}/generate-tasks
Headers:
  Authorization: Bearer <EKYTE_TOKEN>
  Content-Type: application/json
Body: []
```

**Atenção ao body:** é **array vazio `[]`**, não objeto `{}`. Mandar `{}` retorna 422 com `"requires a JSON array"`. O backend é .NET e desserializa em `System.Int64[]`. `[]` ativa **todas** as "Não planejadas" do projeto de uma vez — não é por-task, é por-projeto.

**Pegadinha crítica do 500 (descoberta 2026-05-16):** se o projeto **não tem mais tasks "Não planejada"** (já foram ativadas manualmente OU outra chamada generate-tasks rodou antes), o endpoint retorna **HTTP 500 com body vazio** — não 200, não 204, não erro descritivo. Isso **não é erro de verdade**, é "nada pra ativar". Sempre validar via listagem antes/depois.

**Implementação no fluxo (sempre seguir nesta ordem):**

1. **Pré-check via MCP — task já está ativa?**
   Pra cada task criada no passo 9, chamar `listar_tarefas_tool` com:
   - `project_id` = projeto da task
   - `created_from` / `created_to` = data de hoje
   - `status_list_task` = `10` (ativas)

   Se a task aparece na resposta com `situation: 10`, ela **já está ativa** — outro fluxo (Fabio manual, ou generate-tasks anterior do lote) já cuidou. **Pular essa task silenciosamente.** Não chamar o REST.

2. **Ler `clientes/_skill-ekyte/.env`** (formato em `.env.example`). Se arquivo não existe, avisar Fabio:
   ```
   ⚠️ clientes/_skill-ekyte/.env não cadastrado. Tasks criadas vão ficar como
   'Não planejada' até você gerar manualmente no Ekyte.

   Pra cadastrar o token (~3 min):
   1. F12 em app.ekyte.com → aba Network → no filtro digita 'api.ekyte'
   2. Clica em "Gerar tarefas" em qualquer projeto (força uma request real)
   3. Na request POST que aparece, aba Headers → copia o valor de
      'authorization: Bearer eyJhbGc...'
   4. Cola só o JWT (sem 'Bearer ') em EKYTE_TOKEN= no .env

   Quer cadastrar agora? (sim/não)
   ```
   Se "não", pular passo 9.5 inteiro e seguir pro 10. **Não insistir** depois — Fabio sabe que pode gerar manual no Ekyte web.

3. **Agrupar tasks criadas (que ainda não estão ativas) por `ctc_task_project_id_create_task`**. Lote de 5 tasks em projetos diferentes = até 5 chamadas; 10 tasks todas no mesmo Q2 do Cliente A = 1 chamada.

4. **Pra cada `project_id` único**, disparar:
   ```bash
   curl -X POST "$EKYTE_API_BASE/companies/$EKYTE_COMPANY_ID/projects/<project_id>/generate-tasks" \
     -H "Authorization: Bearer $EKYTE_TOKEN" \
     -H "Content-Type: application/json" \
     -H "Origin: https://app.ekyte.com" \
     -H "Referer: https://app.ekyte.com/" \
     -d '[]'
   ```

5. **Tratamento de resposta:**
   - **200 OK** → reportar `✅ Projeto <nome> ativado`. Re-listar via MCP só pra confirmar contagem.
   - **500 com body vazio** → **não é erro de verdade.** Provavelmente projeto não tinha mais "Não planejada" no momento da chamada (Fabio gerou em paralelo via UI, ou já foi ativado). Re-listar via MCP `listar_tarefas_tool` filtrando o `project_id` + criadas hoje + `status_list_task: 10`. Se a task aparece ativa, reportar `✅ Projeto <nome>: tasks já ativas (500 é falso erro do Ekyte quando não há "Não planejada")`. Se não aparece, aí sim é erro real — escalar.
   - **401 Unauthorized** → token expirou. Avisar:
     ```
     ❌ Token EKYTE_TOKEN expirou. As tasks foram criadas mas ficaram como 'Não planejada'.

     Renovar (~2 min):
     1. F12 em app.ekyte.com → Network → filtro 'api.ekyte'
     2. Clica em "Gerar tarefas" em qualquer projeto
     3. Copia o header 'authorization: Bearer eyJhbGc...' da request POST
     4. Cola só o JWT (sem 'Bearer ') em EKYTE_TOKEN= no .env

     Token NÃO está em localStorage — só vem via Network durante interação real.
     ```
     Não tentar refresh automático.
   - **Outros erros** → reportar status + body, não interromper outras chamadas, avisar no relatório final.

6. **Relatório consolidado** após todas as chamadas:
   ```
   ✅ 4 tasks criadas
   ✅ Ativas: Cliente A | Q2/2026 (2 tasks), Cliente C | Q2/2026 (2 tasks)
   ```

   Se alguma falhou de verdade:
   ```
   ✅ 4 tasks criadas
   ✅ Ativas: Cliente A | Q2/2026 (2 tasks)
   ⚠️ NÃO ativadas: Cliente C | Q2/2026 (2 tasks) — token expirado, renova e retenta
   ```

**Token TTL:** JWT do Ekyte vale ~180 dias. Quando 401, renovar via Network (NÃO localStorage — Ekyte usa httpOnly cookie + JWT no header só durante requests). Capturar via Console JS / localStorage **não funciona** — única forma é interceptar Network durante ação real na UI.

### 9.6) Trocar responsável de etapa (só se especificado no passo 4.5)

Roda **depois** da criação+ativação (9/9.5), e **só** se o Fabio especificou responsável por etapa. Sem overrides, pular.

Via MCP **oficial** (`ekyte-oficial`) — sem JWT manual, token fixo na URL. Pra cada override `{fase → pessoa}` da task:

1. **Pegar o `taskId` real** da task recém-criada/ativada. Se não tiver em mãos, achar via `mcp__ekyte-oficial__list_tasks` filtrando projeto + criadas hoje + título, ou `get_detailed_task` pra confirmar as fases reais.

2. **Confirmar o `phaseId`** da fase: do `flows.md` (passo 4.5) ou das fases reais da task via `get_detailed_task`. A fase precisa existir no fluxo da task.

3. **Aplicar:**
   ```
   mcp__ekyte-oficial__update_task_executor(
     taskId: <id>,
     phaseId: <phaseId da fase>,
     patchDoc: [{"op":"replace","path":"/executorId","value":"<userId GUID>"}]
   )
   ```
   > O schema do `patchDoc` não detalha o campo; o path `/executorId` segue a estrutura do fluxo (`executorId` por fase) e a convenção do `update_task`. **Confirmar no 1º uso** — se a API rejeitar, inspecionar `get_detailed_task` pra ver o nome exato do campo e ajustar este passo + esta nota.
   > Se a fase for a **etapa atual** da task, o Ekyte troca também o executor corrente da task (comportamento documentado da tool).

4. **Relatório** — somar ao consolidado do 9.5:
   ```
   👤 Responsáveis ajustados:
      • #9342321 Briefing → Marina Souza ✅
      • #9342321 Designer → João Pedro ✅
   ```
   Se uma troca falhar, reportar a fase + erro e seguir as outras (não abortar o lote).

**Guardrail:** nunca trocar executor de fase que o Fabio não pediu. Default do tipo é sagrado — só sobrescrever o que foi explicitamente especificado.

### 9.7) Aplicar somente a tag IA

Ao final de toda criação via `/ekyte-task`, depois de criar, ativar, corrigir datas de etapa e aplicar overrides de responsável, adicionar somente:

- `IA` **em vermelho** (resolver `tagId` pela lista/cache de tags; se houver mais de uma tag `IA`, usar a vermelha)

Regra de aplicação:

1. Resolver o `tagId` da tag `IA` vermelha. Buscar por nome exato `IA` e conferir a cor/metadado visual. Se a tag `IA` existir mas não for vermelha, avisar no relatório e não usar a tag errada. Se não existir tag `IA` vermelha e a API disponível permitir criação/edição de tags, criar/ajustar para vermelho antes de aplicar; se não permitir, pedir ao Fabio para criar a tag vermelha e deixar claro que a task ficou sem essa tag.
2. Ler as tags atuais da task.
3. Fazer merge: tags atuais + `IA` vermelha. **Não adicionar `SPRINT GROWTH`, `SEMANA NN` nem qualquer outra tag automática.**
4. Aplicar a lista completa via MCP oficial `update_task_tags` quando disponível. Se usar REST, endpoint:
   `PUT /api/v2/companies/{company_id}/ctc-tasks/{task_id}/tags`
   com body:
   ```json
   [{"ctcTaskId": 9500983, "tagId": "<IA_VERMELHA>"}]
   ```

**Nunca substituir tags preexistentes sem merge.** O endpoint de tags substitui a lista inteira. Em task nova sem tags anteriores, a lista final deve conter somente `IA` vermelha.

### 10) Atualizar cache

Sempre que descobrir um `project_id` novo (ou um `task_type_id` confirmado de tipo Personalizada), atualizar `clientes/_skill-ekyte/cache.md` antes de encerrar. Se descobrir o fluxo de um tipo que não estava em `flows.md` (buscado em runtime no 4.5), salvar lá também. Refresh total dos fluxos: re-rodar o fetch de `get_task_type_flow` por tipo (ainda não embutido no `/ekyte-refresh` — wire pendente).

---

## Guardrails (não-negociáveis)

1. **Lock de cliente por sessão.** Se o Fabio começou trabalhando "Cliente A", não criar tasks em outro workspace sem confirmação explícita ("acabamos com Cliente A, agora estou indo pra Cliente C").

2. **Desambiguação obrigatória** em:
   - Cliente com >1 match (rara, mas possível com nomes parecidos)
   - Sigla com >1 task_type_id (CA, CJ, GP, MT, AUX, CRM, PMM, RI, SM)
   - Projeto com >1 match para o período pedido

3. **Preview obrigatório** antes de cada criação. Sem exceção. Mesmo no modo B em lote, exibir resumo + esperar "ok".

4. **Workspace fora dos 8** → PARAR e pedir confirmação explícita. A conta é master Collie, blast radius alto.

5. **Erro = parar.** Se uma criação falhar (HTTP error, timeout, schema rejeitado), pausar o fluxo e reportar. Não seguir pra próxima task do lote sem aprovação.

6. **Sem auto-execução.** Mesmo que o Fabio diga "confia, manda tudo", insistir no preview da primeira task pelo menos.

7. **Gerar tarefas é parte obrigatória do fluxo.** Toda task criada deve sair de "Não planejada" no final da execução. Se token expirou ou `.env` não existe, **avisar explicitamente** que as tasks ficaram em rascunho — Fabio não pode descobrir isso depois.

8. **Nunca entregar task atrasada.** Antes de encerrar, validar individualmente que nenhuma task criada caiu em "Atrasado". O campo "Executar etapa até" precisa ser a data de criação/subida; o SLA só controla "Concluir tarefa até". Se houver backdating automático do Ekyte, corrigir antes de considerar a execução concluída. Uma task ainda atrasada é falha pendente, não sucesso.

9. **Somente tag IA.** Toda task criada pela skill deve receber somente a tag automática `IA` em vermelho. Não adicionar `SPRINT GROWTH`, `SEMANA NN` ou qualquer outra tag automática. Preservar tags que já existiam na task por merge; em task nova sem tags anteriores, o resultado final é apenas `IA`.

10. **Token Ekyte é sensível.** Nunca logar/imprimir o valor de `EKYTE_TOKEN` nas mensagens pro Fabio (mesmo truncado). Só dizer "token presente/ausente/expirado".

---

## Como invocar

- `/ekyte-task` — usuário chama explicitamente
- Detectar automaticamente quando o Fabio:
  - Disser "cria/sobe/abre uma task/tarefa no ekyte"
  - Mencionar uma sigla `[CA]`, `[LP]`, etc. seguida de cliente
  - Apontar aba da planilha de demandas pra subida em lote

## O que NÃO fazer

- Não inventar `task_type_id`, `workspace_id` ou `project_id`. Se não está no cache, buscar ou perguntar.
- Não criar workspace, projeto ou tipo novos por conta própria. Skill v1 só **cria task**, nunca infraestrutura.
- Não pular o preview, mesmo que o Fabio peça pressa.
- Não escrever briefing do zero quando o tipo tem template oficial — sempre usar o template e preencher.
- Não tentar aplicar tag nativa na chamada de criação da MCP — o schema não expõe. Marcar IA pelo título `[IA]` e aplicar a tag `IA` vermelha no pós-criação, via passo 9.7.
