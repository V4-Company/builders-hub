# Qualidade comercial auditável

## Princípio

Julgue o atendimento em três camadas independentes. Não gere uma nota única que misture execução, competência e resultado, porque um bom vendedor pode receber uma carteira ruim e uma venda pode acontecer apesar de um atendimento fraco.

1. **Execução operacional**: velocidade útil, resposta, conexão, pendências, cadência, follow-up e higiene de CRM/tarefas.
2. **Competência comercial**: abertura, descoberta, qualificação, proposta de valor, objeções, próximo passo, tom e conformidade.
3. **Resultado de funil**: MQL, SQL, oportunidade, orçamento, venda, receita, ticket e ciclo. Resultado é desfecho, não prova isolada de qualidade.

Mostre as três camadas lado a lado e relacione-as apenas como associação observada. Trate qualquer explicação causal como hipótese até existir evidência suficiente.

## Pré-requisitos do cliente

Descubra primeiro no repositório, Flow, Cockpit, NEKT, GrowthPack e Drive. Sabatine somente o que permanecer ausente, conflitante ou desatualizado:

- produto ou serviço, ticket, ciclo e público;
- ICP e regras de MQL, SQL, oportunidade, orçamento e venda;
- etapas e SLAs úteis do funil;
- perguntas obrigatórias de descoberta e qualificação;
- argumentos permitidos, promessas proibidas e regras de compliance;
- objeções recorrentes e respostas esperadas;
- próximo passo esperado por etapa;
- tom de voz, critérios de desqualificação e encerramento;
- papéis de SDR, closer, farmer e full-cycle;
- calendário operacional e regras de follow-up.

Registre tudo numa rubrica versionada baseada em `assets/rubrica-comercial-cliente.md`. Nunca armazene tokens, chaves de API ou credenciais na rubrica ou nos arquivos da skill.

## Estados de avaliabilidade

Classifique cada conversa antes de julgá-la:

| Estado | Uso |
|---|---|
| `evaluable` | Há conversa humana e evidência suficiente para as dimensões aplicáveis. |
| `not_located` | Nenhuma conversa foi vinculada com segurança. Não equivale a lead não atendido. |
| `not_evaluable_no_human` | Há registro, mas não há interação humana avaliável. |
| `not_evaluable_untranscribed_media` | O conteúdo relevante está em áudio, vídeo ou anexo sem transcrição disponível. |
| `human_review_required` | Evidência conflitante, ambígua, incompleta ou risco crítico que exige validação. |

Anexos, áudios e vídeos enviados pelo lead ou vendedor contam como resposta no fluxo operacional. Para julgar o conteúdo, transcreva-os quando autorizado e tecnicamente possível. Se não houver transcrição, não aplique penalidade dependente daquele conteúdo; registre a limitação.

## Evidência mínima

Toda classificação deve apontar para:

- `evidence_id`;
- `conversation_id`, `lead_id`, `deal_id` e `seller_id`, quando existirem;
- IDs das mensagens ou eventos;
- autor normalizado: `lead|humano|bot|ia|sistema`;
- timestamps originais e normalizados;
- link da conversa e do card;
- trecho mínimo necessário, com dados pessoais mascarados na narrativa;
- regra aplicada, versão da rubrica e nível de confiança;
- origem do dado e timestamp de extração.

Exija evidência explícita para afirmar fechamento, pagamento, aceite, agendamento confirmado, objeção resolvida ou mudança equivalente de etapa. Não deduza fechamento por tom positivo. Etapas intermediárias podem usar eventos concretos definidos na rubrica, mas qualquer divergência entre conversa e CRM permanece um achado para revisão, nunca uma alteração automática.

## Score operacional

Use estes pesos apenas como padrão inicial. A rubrica aprovada do cliente pode substituí-los:

| Dimensão | Peso padrão | Exemplos de evidência |
|---|---:|---|
| SLA de primeiro atendimento em tempo útil | 25 | entrada, início do SLA, primeira resposta humana |
| Conexão e resposta efetiva | 15 | resposta do lead, contato conectado, handoff humano |
| Ausência de pendência indevida | 20 | última mensagem, responsável pela próxima ação, promessa vencida |
| Cadência e follow-up | 25 | 7 ou mais follow-ups em até 7 dias; primeiro contato excluído |
| Higiene de etapa e tarefas | 15 | etapa coerente, tarefa versus ação, negócio parado |

Para dimensões não aplicáveis, calcule o percentual sobre os pesos aplicáveis e mostre `peso_aplicável`, `peso_avaliado` e cobertura. Não trate dado ausente como zero.

## Score de competência comercial

Use estes pesos apenas como ponto de partida, depois calibre com o contexto do cliente:

| Dimensão | Peso padrão | O que observar |
|---|---:|---|
| Abertura e personalização | 10 | contexto, identificação, adequação ao canal e ao lead |
| Descoberta de necessidade | 15 | perguntas, dor, cenário, impacto e motivação |
| Qualificação | 20 | critérios de ICP/MQL/SQL, autoridade, capacidade, timing e fit definidos pelo projeto |
| Proposta de valor | 15 | ligação entre necessidade e solução, clareza e especificidade |
| Tratamento de objeções | 15 | reconhecimento, investigação, resposta e validação |
| Próximo passo | 15 | ação, responsável, data e confirmação coerentes com a etapa |
| Tom e conformidade | 10 | cordialidade, precisão, ausência de pressão ou promessa proibida |

Cada dimensão recebe `atende|parcial|não_atende|não_aplicável|não_avaliável`, justificativa e evidência. A pontuação numérica pode ser exibida somente quando a rubrica estiver calibrada e a cobertura for informada. Antes disso, marque `provisional` e privilegie a classificação dimensional.

## Resultado de funil

Mantenha em campos separados:

- perfil: MQL ou não, com regra usada;
- etapas atingidas e respectivas datas;
- SQL, oportunidade, orçamento e venda;
- receita, ticket, ciclo e motivo de perda;
- canal, campanha, conjunto, anúncio, destino e vendedor atribuídos;
- maturação do ciclo e status ainda em aberto.

Use o resultado para investigar padrões, não para reescrever retroativamente a nota de execução ou competência.

## Severidade dos achados

A severidade organiza a revisão humana; não cria ações no CRM:

- **P0 — crítico**: lead elegível sem resposta após o SLA útil crítico; retorno explicitamente prometido e vencido; tarefa concluída sem ação correspondente; três ou mais mensagens do lead sem resposta; promessa proibida ou risco grave de compliance.
- **P1 — alto**: primeira resposta fora do SLA relevante; lead aguardando humano; conversa abandonada; ausência completa de follow-up quando exigido.
- **P2 — médio**: cadência insuficiente, personalização baixa, etapa parada, divergência conversa versus CRM, objeção mal trabalhada ou reunião sem confirmação.
- **P3 — melhoria**: oportunidade clara de descoberta, clareza, próximo passo ou follow-up contextual.
- **P4 — perfil ou cobertura**: lead fora do perfil sem triagem adequada, conversa não localizada ou conteúdo não avaliável.

Use os SLAs úteis do cliente; não aplique limites corridos genéricos. Nunca penalize sábado, domingo, feriado ou horário fechado quando o cliente não opera nesses períodos.

## Reconciliações adicionais

- Detecte duplicidade por telefone, e-mail, IDs e proximidade temporal; preserve todos os IDs e escolha uma entidade canônica sem apagar o histórico.
- Compare tarefa com ação observada: tarefa concluída sem mensagem/ligação/reunião; ação executada com tarefa ainda aberta; promessa sem tarefa ou próximo passo.
- Compare etapa do CRM com evidência conversacional. Registre divergência e confiança; não mova o card.
- Inclua negócios ganhos, perdidos e abertos que pertençam ao período. Use filtros de janela apenas para declarar maturação, nunca para fazê-los desaparecer.

## Calibração por cliente

Não é necessário treinar ou fazer fine-tuning do modelo para iniciar. É necessário calibrar a rubrica:

1. Monte a primeira versão com o playbook, ICP, funil, produto e critérios do cliente.
2. Selecione de 20 a 30 conversas variadas: boas, medianas, ruins, ganhas, perdidas, sem resposta, com áudio, diferentes vendedores e etapas.
3. Um humano de referência classifica as conversas e registra as evidências esperadas.
4. A skill avalia a mesma amostra sem ver os rótulos humanos.
5. Compare dimensão, severidade e evidência; ajuste definições e exemplos, não apenas pesos.
6. Aprove a versão quando houver pelo menos 80% de concordância geral e 100% de captura dos casos críticos P0 da amostra.
7. Registre aprovador, data, amostra e limitações; incremente `rubric_version` a cada mudança material.
8. Em cada retrospectiva, revise 5% a 10% da amostra e todos os P0. Se a concordância cair, volte a calibrar.

Sem rubrica calibrada, execute normalmente a análise operacional objetiva. A avaliação de competência comercial fica `provisional` e não pode sustentar sozinha ranking definitivo, acusação individual ou conclusão sobre causa da conversão.

## Saída por conversa

Registre no mínimo:

- identificadores e links;
- vendedor, papel e fila/inbox;
- origem, campanha e status MQL;
- `evaluation_status` e motivo;
- tempos corrido e útil;
- estado operacional e `operational_score` com cobertura;
- dimensões de competência, `commercial_score`, cobertura e `rubric_version`;
- resultado de funil separado;
- flags P0–P4;
- evidências, confiança e status de revisão humana.
