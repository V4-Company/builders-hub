# Workflow detalhado da retrospectiva de performance

Este documento descreve o workflow atual da família `account-retrospectiva-*`. A retrospectiva é independente: produz fatos, rankings, gaps, hipóteses e evidências. No modo autônomo (padrão), ela roda de ponta a ponta sem paradas intermediárias, registra cada escolha em `decisoes.md` e concentra a validação humana no final. Depois da aprovação, ela libera o adaptador do ROPRE Quarter e, se autorizado, o handoff para o Drive. Detalhes em `modo-autonomo.md`.

## 1. Fluxo ponta a ponta

```mermaid
flowchart TD
    A[Solicitação de retrospectiva] --> B{Modo de entrada}
    B -->|Execução independente| C[Definir cliente e período]
    B -->|ROPRE Quarter| D[Adaptador account-ropre-quarter-retrospectiva]
    D --> C

    C --> CA[Descobrir go-live e primeiro evento real]
    CA --> E[Varrer repositório profissional]
    E --> F[Consultar Flow, Cockpit, NEKT, GrowthPack e Drive autorizados]
    F --> G[Descobrir conexões n8n para CRM, GA4, e-commerce e conversas]
    G --> H[Gerar manifesto de fontes e cobertura]
    H --> I{Há lacuna ou conflito material?}
    I -->|Sim| J[Aplicar escolha mais evidenciada e registrar em decisoes.md]
    I -->|Não| K[Inferir modelo de negócio e registrar]
    J --> K

    K --> L{Inside sales ou e-commerce?}
    L -->|Inside sales| M[Reconstruir funil lead a lead]
    L -->|E-commerce| N[Reconstruir funil de loja e produtos]

    K --> O[Coletar e analisar mídia]
    O --> P[Analisar e baixar criativos via NEKT]
    M --> Q[Auditar conversas e atendimento]
    Q --> R[Comparar vendedores]

    P --> S[Localizar e auditar break-even]
    R --> S
    N --> S
    S --> T{Break-even válido?}
    T -->|Sim| U[Aplicar metas econômicas aos rankings]
    T -->|Não| V[Oferecer criação pelo motor disponível]
    V -->|Criar| U
    V -->|Recusar ou sem premissas| W[Registrar gap crítico]

    U --> X[Reconciliar mídia, CRM, conversas, GA4 e loja]
    W --> X
    X --> Y[Montar ledger de evidências]
    Y --> Z[Consolidar vencedores, perdedores, padrões e gaps]
    Z --> ZA[Preservar módulos, tabelas integrais, bases e evidências]
    ZA --> AA[Gerar retrospectiva final detalhada + índice completo]
    AA --> AR[validate --review-ready]
    AR --> AB[Pacote de validação humana única: decisoes.md]
    AB --> AS{Respostas}
    AS -->|Correção ou dado novo| AT[Nova run_id com parent_run_id e recálculo do módulo afetado]
    AT --> AR
    AS -->|Confirmações e aceites| AU[validate --approval-ready]
    AU -->|Falhou| AB
    AU -->|OK| AC{Comando retrospectiva aprovada?}
    AC -->|Não| AB
    AC -->|Sim| AE[Adaptador ROPRE gera 12-handoff-ropre]
    AE --> AD{Drive solicitado?}
    AD -->|Sim| AF[Gerar manifesto de Drive]
    AD -->|Não| AG[Manter pacote versionado]
    AF --> AH{Autorização explícita para escrever?}
    AH -->|Sim| AI[Publicar Docs, Sheets e assets em nova versão]
    AH -->|Não| AG
```

## 2. Descoberta de contexto e fontes

```mermaid
flowchart TD
    A[Cliente e período recebidos] --> B[Buscar repositório do cliente]
    B --> C[Extrair contexto, playbooks, metas, projeção e histórico]
    C --> D[Consultar plataformas profissionais autorizadas]
    D --> E[Mapear conectores n8n e APIs disponíveis]
    E --> F[Registrar fonte, proprietário, atualização e cobertura temporal]
    F --> G[Detectar fonte congelada, paginação incompleta e conflito]
    G --> H{Contexto mínimo completo?}
    H -->|Sim| I[Gerar 00-manifesto-fontes.md]
    H -->|Não| J[Perguntar somente os campos ausentes]
    J --> K[Validar respostas com o Account]
    K --> I
    I --> L{Manifesto validado?}
    L -->|Não| B
    L -->|Sim| M[Gerar 01-contexto-cliente.md]
```

### Contexto mínimo

- cliente, projeto, período e comparações desejadas;
- quarter calendário, go-live técnico, primeiro evento real, `analysis_start` e eventuais relançamentos;
- inside sales ou e-commerce;
- oferta, público, região, canais e destinos;
- CRM ou plataforma de loja, GA4 e ferramenta conversacional;
- vendedores e papéis;
- MQL, SQL, oportunidade, orçamento e venda;
- horário comercial, fuso, finais de semana, feriados e exceções;
- verba, fee, margem, ticket, metas, projeção e break-even;
- calendário, sazonais, onboardings, roadmap e funcionalidades do próximo ciclo.

## 3. Mídia e criativos

```mermaid
flowchart TD
    A[NEKT como fonte detalhada de mídia] --> B[Paginar período completo]
    B --> C[Fechar investimento total]
    C --> D[Comparar canais]
    D --> E[Estratificar rede e estratégia]
    E --> F[Estratificar destino]
    F --> G[Estratificar campanha]
    G --> H[Estratificar conjunto ou ad group]
    H --> I[Estratificar anúncio]
    I --> J[Estratificar público, keyword e breakdowns]
    J --> JA[Preencher matriz das 15 dimensões]
    JA --> JB[Gerar bases completas, inclusive zero resultado]
    JB --> JC[Reconciliar investimento entre níveis]
    JC --> K[Recalcular métricas canônicas]
    K --> L[Aplicar projetado, meta, histórico e break-even]
    L --> M[Gerar rankings por CPL, MQL, SQL, venda e ROAS]
    M --> N[Exibir o funil inteiro em cada ranking]

    I --> O[Obter preview, copy e asset pelo NEKT]
    O --> P{Formato do criativo}
    P -->|Imagem| Q[OCR e classificação de mensagem]
    P -->|Vídeo| R[Thumbnail, transcrição, hook e hold]
    P -->|Texto, search ou carrossel| S[Extrair headline, peças e CTA]
    Q --> T[Classificar ângulo, dor, desejo, promessa, prova, oferta e CTA]
    R --> T
    S --> T
    T --> U[Cruzar tags criativas com mídia e funil]
    U --> V[Salvar assets rastreáveis para o deck]
```

### Hierarquia analítica

```text
Geral
└── Canal
    └── Rede ou estratégia
        └── Destino
            └── Campanha
                └── Conjunto ou ad group
                    └── Anúncio ou criativo
                        └── Público, keyword e breakdowns
```

Os destinos ficam comparáveis dentro de contexto compatível: site, landing page, formulário nativo, WhatsApp e outros. Os rankings não escolhem um único “campeão universal”; cada lente ordena por uma métrica e preserva o restante do funil.

O resumo só é escrito depois das bases. Se campanha, conjunto, anúncio, público ou breakdown estiver ausente, a matriz identifica a lacuna, a skill solicita fonte/API/export/input manual e o módulo permanece `partial`.

## 4. Inside sales: funil, atendimento e vendedores

```mermaid
flowchart TD
    A[Extrair CRM no período] --> B[Normalizar leads, contatos, negócios e etapas]
    B --> C[Resolver duplicidades sem apagar o bruto]
    C --> D[Aplicar definições validadas de MQL, SQL, oportunidade, orçamento e venda]
    D --> E[Atribuir aquisição por first paid touch]
    E --> F[Calcular funil, custos, taxas, ciclo e maturação]

    F --> G[Vincular ferramenta conversacional por IDs, telefone e e-mail]
    G --> H{Conversa vinculada com segurança?}
    H -->|Não| I[Marcar not_located e preservar na base]
    H -->|Sim| J[Separar lead, humano, bot, IA e sistema]
    J --> K{Existe mídia ou anexo relevante?}
    K -->|Sim| L[Transcrever quando autorizado e possível]
    K -->|Não| M[Continuar com mensagens disponíveis]
    L --> N{Conteúdo ficou avaliável?}
    N -->|Não| O[Marcar not_evaluable_untranscribed_media nas dimensões afetadas]
    N -->|Sim| M

    M --> P[Calcular SLA em tempo útil]
    P --> Q[Classificar resposta, conexão, pendência e abandono]
    Q --> R[Medir 7 ou mais follow-ups em até 7 dias]
    R --> S[Reconciliar tarefa versus ação e etapa versus conversa]
    S --> T[Calcular execução operacional e cobertura]

    T --> U{Rubrica comercial aprovada e calibrada?}
    U -->|Não| V[Gerar ou atualizar rascunho da rubrica]
    V --> W[Classificar competência como provisional]
    U -->|Sim| X[Avaliar competência por dimensão]
    X --> Y[Calcular score comercial e cobertura]

    I --> Z[Registrar evidências e estado de cobertura]
    O --> Z
    W --> Z
    Y --> Z
    Z --> AA[Manter resultado de funil separado]
    AA --> AB[Comparar vendedores com controle de carteira e qualidade do lead]
    AB --> AC[Rankings separados de execução, competência e resultado]
```

### As três camadas de julgamento

| Camada | Responde a quê? | Exemplos | Pode virar ranking? |
|---|---|---|---|
| Execução operacional | O processo foi executado? | SLA útil, resposta, conexão, pendência, follow-up, tarefa e etapa | Sim, com cobertura explícita |
| Competência comercial | A conversa foi bem conduzida para este projeto? | descoberta, qualificação, valor, objeções, próximo passo, tom | Sim, somente com rubrica calibrada |
| Resultado de funil | O que aconteceu depois? | MQL, SQL, oportunidade, orçamento, venda, receita e ciclo | Sim, separado das duas notas |

Não existe score total combinando as três camadas.

### Calibração da competência comercial

```mermaid
flowchart TD
    A[Reunir playbook, ICP, produto, funil e compliance] --> B[Gerar rubrica draft]
    B --> C[Selecionar 20 a 30 conversas variadas]
    C --> D[Humano de referência rotula dimensões, severidade e evidências]
    D --> E[Skill avalia a mesma amostra sem ver os rótulos]
    E --> F[Comparar concordância e falhas críticas]
    F --> G{Concordância geral de 80% ou mais e captura P0 de 100%?}
    G -->|Não| H[Ajustar definições, exemplos e pesos]
    H --> E
    G -->|Sim| I[Aprovar e versionar a rubrica]
    I --> J[Usar score comercial definitivo]
    J --> K[Revisar 5% a 10% e todos os P0 a cada retrospectiva]
    K --> L{Concordância caiu?}
    L -->|Sim| H
    L -->|Não| J
```

## 5. E-commerce

```mermaid
flowchart TD
    A[Coletar NEKT] --> D[Reconciliação por origem]
    B[Coletar GA4] --> D
    C[Coletar plataforma de e-commerce] --> D
    D --> E[Separar pago, não pago e total]
    E --> F[Definir pedido, aprovação, faturamento, cancelamento e reembolso]
    F --> G[Fechar investimento, pedidos, vendas e receita]
    G --> H[Analisar canal, campanha e destino]
    H --> I[Analisar categoria, produto, SKU e variante]
    I --> J[Cruzar sessões, conversão, ticket, receita, ROAS e CPVenda]
    J --> K[Adicionar margem, estoque, cancelamento e reembolso]
    K --> L[Comparar com projetado, meta, histórico e break-even]
    L --> M[Identificar padrões de tráfego, conversão, ticket e contribuição]
```

## 6. Break-even e julgamento de performance

```mermaid
flowchart TD
    A[Procurar break-even no repositório, GrowthPack e Drive] --> B{Atual para o último quarter?}
    B -->|Sim| C[Auditar fee, verba, MC1, ticket, modelo e funil]
    B -->|Não| D[Oferecer criação ao Account]
    D -->|Aceita| E[Detectar motor Jean e motor local]
    E --> F[Confirmar fee, verba e MC1]
    F --> G[Calcular break-even e funil inverso]
    D -->|Recusa ou faltam premissas| H[Registrar gap crítico]
    C --> I[Gerar referências econômicas]
    G --> I
    I --> J[Comparar CPL, CPMQL, CPSQL, CPVenda, ROAS e receita]
    H --> K[Usar apenas outra meta validada e declarar limitação]
```

O julgamento de “bom” ou “ruim” considera meta, verba, histórico, custo esperado, maturação e break-even do próprio cliente. Não existe volume mínimo global que funcione para todos.

## 7. Reconciliação e atribuição

```mermaid
flowchart TD
    A[Preservar valores brutos] --> B[Normalizar telefone, e-mail, URL, UTM e nomes]
    B --> C[Resolver lead, contato, negócio, conversa e pedido]
    C --> D{Existe ID persistido ou UTM original?}
    D -->|Sim| E[Atribuir first paid touch]
    D -->|Não| F[Tentar origem, URL e mapeamento validado]
    F --> G{Match confiável?}
    G -->|Sim| E
    G -->|Não| H[Manter não atribuído ou ambíguo]
    E --> I[Cruzar campanha, conjunto, anúncio e criativo com NEKT]
    H --> I
    I --> J[Classificar regra e confiança do match]
    J --> K[Medir atribuídos, não atribuídos, ambíguos e duplicados]
    K --> L[Registrar conflitos e impacto analítico]
```

Telefone e e-mail ajudam a identificar a pessoa. Eles não provam sozinhos qual campanha adquiriu o lead; a campanha exige ID, UTM, URL, origem ou mapeamento previamente validado.

## 8. Evidência, consolidação e publicação

```mermaid
flowchart TD
    A[Bases reconciliadas] --> B[Criar evidence_id por prova]
    B --> C[Registrar fonte, chave, período, extração, regra, link e confiança]
    C --> D[Auditar totais e amostras]
    D --> E{Conclusão possui evidência?}
    E -->|Não| F[Rotular como hipótese ou input humano]
    E -->|Sim| G[Rotular como fato ou gap comprovado]
    F --> H[Gerar 10-achados-gaps.md]
    G --> H
    H --> HA[Manter rankings integrais e todas as entidades]
    HA --> I[Gerar 11-retrospectiva-final.md com análise detalhada e índice]
    I --> J[Revisão e complementação humana]
    J --> K{Retrospectiva aprovada?}
    K -->|Não| J
    K -->|Sim| L[Congelar run_id aprovado]
    L --> M{Handoff escolhido}
    M -->|ROPRE| N[Gerar 12-handoff-ropre.md]
    M -->|Drive| O[Gerar 13-drive-handoff.md]
    M -->|Nenhum| P[Encerrar pacote]
    O --> Q{Escrita autorizada?}
    Q -->|Sim| R[Docs para narrativa, Sheets para bases e pasta para assets]
    Q -->|Não| P
```

## 9. Arquivos produzidos

| Ordem | Arquivo | Módulo responsável | Quando aparece |
|---:|---|---|---|
| 00 | `00-manifesto-fontes.md` | contexto e fontes | Sempre |
| 01 | `01-contexto-cliente.md` | contexto e fontes | Sempre |
| 02 | `02-midia.md` | mídia | Quando houver mídia |
| 03 | `03-criativos.md` | criativos | Quando houver criativos |
| 04 | `04-funil-inside-sales.md` | funil inside sales | Inside sales |
| 04 | `04-ecommerce.md` | e-commerce | E-commerce |
| 05 | `05-vendedores.md` | vendedores | Inside sales |
| 06 | `06-atendimento.md` | atendimento | Quando houver dados conversacionais |
| 07 | `07-breakeven.md` | break-even | Sempre, mesmo que registre gap |
| 08 | `08-reconciliacao.md` | reconciliação | Sempre |
| 09 | `09-evidencias.md` | evidências | Sempre |
| 10 | `10-achados-gaps.md` | achados e gaps | Sempre |
| 11 | `11-retrospectiva-final.md` | consolidação | Sempre |
| 12 | `12-handoff-ropre.md` | adaptador ROPRE | Somente se o usuário iniciar o planejamento |
| 13 | `13-drive-handoff.md` | handoff Drive | Somente se solicitado após aprovação |
| — | `decisoes.md` | todos os módulos | Sempre; é o pacote de validação humana |

Bases aplicáveis:

- `bases/cobertura-midia.md`;
- `bases/canais.md`;
- `bases/destinos.md`;
- `bases/campanhas.md`;
- `bases/conjuntos.md`;
- `bases/anuncios.md`;
- `bases/breakdowns.md`;
- `bases/leads-negocios.md`;
- `bases/conversas.md`;
- `bases/produtos.md`;
- `bases/pedidos.md`;
- `assets/criativos/`.

## 10. Gates e responsabilidades humanas

No modo autônomo, todos os gates abaixo, exceto escrita no Drive, são validados de uma vez no pacote final de `decisoes.md`. Nenhum interrompe a execução no meio.

| Gate | Por que existe | Quem valida |
|---|---|---|
| Manifesto de fontes | Evita analisar fonte errada, congelada ou incompleta | Account ou responsável pelos dados |
| Modelo e definições de funil | MQL, SQL e venda variam por cliente | Account e liderança comercial |
| Fonte oficial em conflito | Impede soma ou escolha arbitrária | Dono do dado |
| Fee, verba e MC1 | Sustentam o break-even | Account ou responsável financeiro |
| Rubrica comercial | Torna o julgamento aderente ao projeto | Liderança comercial ou Account |
| Calibração da rubrica | Impede score subjetivo não validado | Humano de referência |
| Retrospectiva aprovada | Congela o pacote antes de planejar ou publicar | Usuário responsável |
| Escrita no Drive | É uma ação externa e versionada | Usuário responsável |
| Liberação do adaptador ROPRE | Acontece automaticamente com `retrospectiva aprovada` | Usuário responsável |

## 11. Limites do workflow

- A retrospectiva não cria tarefas, não muda etapas, não envia alertas e não escreve no CRM.
- A retrospectiva não define prioridade, responsável ou prazo; entrega os insumos para o ROPRE.
- Credenciais ficam em conectores ou variáveis seguras, nunca em Markdown ou dentro da skill.
- Ausência de fonte vira lacuna explícita; não vira zero nem conclusão inventada.
- Correlação entre atendimento, mídia e venda não vira causalidade sem prova.
- Toda execução é versionada em `checkins/quarter/{ano}/Q{n}/retrospectiva-performance/{run_id}/` e nunca sobrescreve o histórico.
