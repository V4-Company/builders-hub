# Fluxo Ekyte: do cliente novo a task criada

Este documento desenha o fluxo operacional das skills que entram desde o cadastro de um cliente novo ate a criacao de uma task no Ekyte.

## Visao geral

```mermaid
flowchart TD
    A[Cliente novo entra] --> B[/novo-cliente]
    B --> C[Cria pasta clientes/<cliente>]
    C --> D[CLAUDE.md, AGENTS.md, links.md, calls, docs, campanhas, checkins]
    D --> E{NotebookLM informado?}

    E -- Sim --> F[Notebook ID salvo no cliente]
    E -- Nao --> G[/notebooklm-cadastrar quando tiver link]
    G --> F

    D --> H[Adicionar insumos: calls, docs, campanhas, proposta, kickoff]
    H --> I[/contexto]
    I --> J[Atualiza CLAUDE.md, AGENTS.md e mission-control]

    F --> K[/ekyte-briefing-refresh]
    K --> L[Atualiza Drive e backup CRM em clientes/_skill-ekyte]

    L --> M[/ekyte-refresh]
    M --> N[Atualiza cache.md: workspace, projeto vigente, tipos e flows]

    N --> O[/ekyte-task]
    O --> P[Resolve cliente, workspace, projeto, tipo, SLA e titulo]
    P --> Q{Projeto estava no cache?}

    Q -- Nao --> R[Marca projeto_novo: true]
    Q -- Sim --> S[projeto_novo: false]
    R --> T[/ekyte-briefing]
    S --> T

    T --> U[/cs-notebooklm-consulta-cliente]
    U --> V{Consulta funcionou?}

    V -- Sim --> W[Sintese NotebookLM + artefato em contexto-notebook]
    V -- Nao --> X[Pausa: cadastrar/login ou GP autoriza seguir sem NotebookLM]
    X --> Y{GP autorizou seguir sem?}
    Y -- Nao --> U
    Y -- Sim --> Z[Briefing registra: NotebookLM nao consultado por autorizacao do GP]

    W --> AA[Montar briefing com template, Drive, publico/cache e perguntas ativas]
    Z --> AA

    AA --> AB[Preview do briefing]
    AB --> AC[Preview da task]
    AC --> AD{Fabio confirma criacao?}
    AD -- Nao/editar --> AA
    AD -- Sim --> AE[Criar task via MCP Ekyte]
    AE --> AF[Gerar tarefas / ativar]
    AF --> AG[Corrigir datas se necessario]
    AG --> AH[Aplicar responsaveis por etapa, se houver]
    AH --> AI[Aplicar tags: SPRINT GROWTH, SEMANA NN e IA vermelha]
    AI --> AJ[Atualizar cache se descobriu projeto/tipo novo]
```

## Skills que entram no fluxo

| Etapa | Skill | Responsabilidade |
|---|---|---|
| Cadastro inicial | `/novo-cliente` | Cria a pasta do cliente, arquivos-base e links uteis. |
| NotebookLM posterior | `/notebooklm-cadastrar` | Cadastra ou atualiza NotebookLM em cliente ja existente. |
| Memoria operacional | `/contexto` | Le a KB do cliente e gera contexto duradouro + mission-control. |
| Links do briefing | `/ekyte-briefing-refresh` | Atualiza Drive e backups CRM usados pelo briefing. |
| Cache Ekyte | `/ekyte-refresh` | Atualiza workspaces, projetos do trimestre, tipos e fluxos. |
| Orquestracao da task | `/ekyte-task` | Resolve IDs, titulo, prazo, preview, criacao, ativacao e tags. |
| Briefing | `/ekyte-briefing` | Monta o briefing formal com template e contexto. |
| Consulta de contexto | `/cs-notebooklm-consulta-cliente` | Consulta NotebookLM e salva artefato em `contexto-notebook/`. |

## Regra de NotebookLM

Para task Ekyte, o fluxo sempre tenta consultar NotebookLM via `/cs-notebooklm-consulta-cliente`, principalmente quando `projeto_novo: true`.

Se nao houver NotebookLM cadastrado, login valido ou resposta util, o fluxo pausa antes do preview de criacao e pede uma decisao:

1. Cadastrar ou corrigir NotebookLM e tentar de novo.
2. Seguir sem NotebookLM somente com comando explicito do gerente de projetos.

Quando o gerente autoriza seguir sem NotebookLM, o briefing deve registrar:

```text
NotebookLM: nao consultado por autorizacao do gerente de projetos
```

## Contratos importantes

- `/ekyte-task` nao monta `description_create_task` por conta propria.
- `/ekyte-task` chama `/ekyte-briefing` depois de resolver workspace, projeto, tipo, titulo e quantidade.
- `/ekyte-briefing` devolve `briefing_ekyte_text`, em texto plano formatado para o Ekyte.
- HTML nao deve ser enviado no `description_create_task`, porque o Quill do Ekyte via API renderiza tags como texto literal.
- Cache de publico pode preencher campos de publico, mas nao substitui a tentativa de consulta NotebookLM quando o contexto da task exige.
- Projeto que nao estava no cache no inicio do fluxo deve ser marcado como `projeto_novo: true`.

## Resultado esperado

Ao final, a task deve estar:

- Criada no workspace/projeto corretos.
- Ativa, nao presa como "Nao planejada".
- Sem datas de etapa atrasadas.
- Com briefing estruturado.
- Com responsaveis por etapa ajustados quando solicitados.
- Com tags `SPRINT GROWTH`, `SEMANA NN` e `IA` vermelha aplicadas.
