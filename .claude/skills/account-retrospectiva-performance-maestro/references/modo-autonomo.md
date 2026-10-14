# Modo autônomo com validação final

## Princípio

`execution_mode: autonomous` é o padrão. A retrospectiva roda de ponta a ponta para um cliente sem interromper o humano no meio. Toda escolha que antes exigia gate intermediário vira uma **decisão registrada** em `decisoes.md`, com evidência, alternativas, impacto e módulos que dependem dela.

Autonomia não autoriza silêncio: nenhuma decisão inferida, lacuna ou conflito pode ficar fora de `decisoes.md`. O humano valida tudo de uma vez no final, e somente essa validação libera o adaptador `account-ropre-quarter-retrospectiva`.

Use `execution_mode: interactive` apenas quando o usuário pedir explicitamente as paradas intermediárias. Nesse modo, os gates voltam a acontecer no módulo de origem, mas `decisoes.md` continua obrigatório.

## Únicas paradas antes do fim

1. **Pré-voo:** o cliente não pode ser identificado de forma única (nome ambíguo, mais de um projeto candidato sem critério). Pergunte e só então comece.
2. **Fim da execução:** pacote de validação humana.

Período não informado não é parada: assuma o último quarter calendário fechado e registre a decisão como `janela_temporal`, criticidade `critica`.

## O que continua proibido no modo autônomo

- Escrever em CRM, Drive, Ekyte, planilhas externas ou qualquer sistema do cliente.
- Enviar mensagem, alerta ou e-mail.
- Pedir ou registrar segredo em texto; conector ausente vira lacuna.
- Baixar criativos por fonte diferente do NEKT.
- Iniciar o ROPRE ou o handoff de Drive sem `retrospectiva aprovada`.

Break-even criado pela skill fica como artefato local da execução e decisão `premissa_economica`; nunca é gravado em planilha oficial do cliente.

## Como decidir sem parar

Para cada ponto que antes era gate:

1. Esgote a descoberta: repositório, Cockpit/Flow, GrowthPack, NEKT, CRM, Drive e histórico de execuções anteriores do mesmo cliente.
2. Classifique a base da escolha:
   - **evidenciada**: fonte oficial inequívoca e atual define o valor (ex.: etapa "MQL" no CRM com regra documentada no playbook do cliente);
   - **assumida**: valor inferido de evidência indireta, fonte desatualizada, padrão de execução anterior ou convenção do mercado;
   - **lacuna**: não há base para decidir; o dado fica `sem dado` e o módulo, `partial` ou `blocked`.
3. Aplique a escolha, siga a execução e registre a linha em `decisoes.md` no mesmo momento.
4. Quando houver conflito material entre fontes, aplique a precedência de `fontes-e-reconciliacao.md`, calcule também a alternativa quando for barato e registre o impacto das duas leituras.

Não invente definição. Se nenhuma fonte sugerir MQL, SQL ou venda, registre lacuna; não use convenção genérica como se fosse do cliente.

## Mapa dos antigos gates

| Antigo gate | Tipo da decisão | Comportamento autônomo |
|---|---|---|
| Manifesto de fontes | `fonte_oficial` | Gera manifesto, usa a precedência oficial e registra fontes congeladas, ausentes e conflitantes |
| Modelo de negócio | `modelo_negocio` | Infere por CRM vs. plataforma de loja; registra como `assumida` se não houver cadastro oficial |
| Janela e go-live | `janela_temporal` | Usa o primeiro evento real em produção com tracking funcional; registra marcos divergentes |
| Testes e leads internos | `exclusao_teste` | Exclui só o comprovado por ID; suspeitos ficam na base com `human_review_required` |
| MQL, SQL, oportunidade, orçamento, venda | `definicao_funil` | Usa a definição documentada; sem documento, usa a semântica de etapa do CRM como `assumida` |
| Fonte oficial em conflito | `fonte_oficial` | Aplica precedência e registra as duas leituras |
| Calendário operacional | `calendario_operacional` | Usa horário documentado; sem documento, infere da distribuição de mensagens humanas como `assumida` |
| Fee, verba, MC1 e ticket | `premissa_economica` | Cria break-even local se as premissas forem encontradas; MC1 ausente vira lacuna crítica |
| Rubrica comercial | `rubrica` | Gera rascunho, roda competência como `provisional` e prepara amostra de calibração |
| Mapeamento manual de atribuição | `atribuicao` | Aplica só match confiável; o restante fica `unattributed` |
| Dimensão ou fonte ausente | `lacuna` | Registra fonte esperada, próximo passo e impacto; módulo segue `partial` |

## Contrato de `decisoes.md`

Arquivo canônico na raiz da execução, com o frontmatter padrão e `module: "decisoes"`. O `status` do frontmatter descreve o próprio ledger (`complete` quando todas as decisões foram registradas).

Estrutura:

1. `## Estado da execução` — status de cada módulo, resultado de `--review-ready`, contagens por criticidade e status.
2. `## Ledger de decisões` — tabela única, uma linha por decisão ou lacuna.
3. `## Amostra de calibração da rubrica` — quando houver frente comercial sem rubrica calibrada.
4. `## Como responder` — instruções de resposta ao humano.

Tabela obrigatória:

| id | arquivo | tipo | criticidade | decisão aplicada | base e evidência | alternativas | impacto se errada | recalcula a partir de | status | resposta humana |
|---|---|---|---|---|---|---|---|---|---|---|

- `id`: `D-001` para decisões, `L-001` para lacunas.
- `arquivo`: arquivo da execução afetado (`04-funil-inside-sales.md`) ou dimensão de mídia no formato `cobertura-midia:regiao`.
- `tipo`: `modelo_negocio`, `janela_temporal`, `exclusao_teste`, `definicao_funil`, `fonte_oficial`, `calendario_operacional`, `premissa_economica`, `rubrica`, `atribuicao`, `lacuna` ou `outro`.
- `criticidade`: `critica` (muda conclusão central ou julgamento econômico), `alta` (muda ranking ou funil de uma frente), `media` (muda leitura secundária), `baixa` (cosmético ou de cobertura).
- `status`:
  - `evidenciada` — não bloqueia aprovação;
  - `assumida` — bloqueia até `confirmada` ou `corrigida`;
  - `aberta` — lacuna; bloqueia até `aceita` ou `resolvida`;
  - `confirmada`, `corrigida`, `aceita`, `resolvida` — estados finais.
- Todo módulo com status diferente de `complete` e toda dimensão de mídia `partial` ou `unavailable` precisa de ao menos uma linha `lacuna` apontando para ele.

Ordene a tabela por criticidade e, dentro dela, pela ordem de execução dos módulos.

## Mapa de recálculo

Correção humana nunca edita números da execução existente. Ela gera nova `run_id` com `parent_run_id`, herda os módulos anteriores ao ponto de recálculo (atualizando `run_id` e registrando `inherited_from`) e recalcula do primeiro módulo afetado até o final.

| Tipo corrigido | Recalcular a partir de |
|---|---|
| `modelo_negocio` | `02-midia.md` |
| `janela_temporal`, `exclusao_teste` | `02-midia.md` |
| `definicao_funil`, `atribuicao` | `02-midia.md` |
| `fonte_oficial` | primeiro módulo que consome a fonte |
| `calendario_operacional`, `rubrica` | `06-atendimento.md` |
| `premissa_economica` | `07-breakeven.md` |
| `lacuna` resolvida com dado novo | módulo da lacuna |

`08-reconciliacao.md`, `09-evidencias.md`, `10-achados-gaps.md`, `11-retrospectiva-final.md` e `decisoes.md` são sempre recalculados depois de qualquer correção. Confirmação simples (`ok`) e aceite de lacuna não geram nova execução: atualize apenas a coluna de status e resposta humana.

## Pacote de validação humana

Ao fim da execução autônoma:

1. Rode `validate_retrospectiva.py <run_dir> --review-ready` e corrija sozinho as falhas estruturais.
2. Apresente ao humano, em mensagem curta:
   - status geral e status por módulo;
   - os 3 a 5 achados centrais com `evidence_id`;
   - decisões `critica` e `alta` pendentes, uma por linha, com a escolha aplicada e o impacto se estiver errada;
   - contagem das pendências `media` e `baixa`, lacunas abertas e amostra de calibração;
   - link para `decisoes.md` e `11-retrospectiva-final.md`.
3. Aceite respostas no formato:
   - `D-003 ok` — confirma;
   - `D-004 corrigir: <novo valor>` — corrige e agenda recálculo;
   - `L-002 aceitar` — aceita a lacuna nominalmente;
   - `L-005 dado: <valor, arquivo ou acesso>` — resolve a lacuna e agenda recálculo;
   - `confirmar pendentes média e baixa` — confirma em lote somente essas criticidades;
   - `retrospectiva aprovada` — aprovação final.
4. Agrupe as correções da mesma rodada e recalcule uma única vez.
5. Rode `--approval-ready`. Só peça `retrospectiva aprovada` quando ele passar.

`retrospectiva aprovada` enviada com pendências bloqueantes não é aceita: responda listando os IDs que ainda bloqueiam.

## Depois da aprovação

`retrospectiva aprovada` registrada e `--approval-ready` OK liberam o adaptador `account-ropre-quarter-retrospectiva` sem nova pergunta. O handoff de Drive continua opcional e exige autorização própria de escrita.
