# QA da retrospectiva

## Checklist estrutural

- Todos os arquivos têm frontmatter e `run_id` idêntico.
- Período e modelo de negócio são consistentes.
- `analysis_start` existe em todos os arquivos e pertence ao intervalo declarado.
- Quarter, pré-operacional, go-live técnico, primeiro evento real e janela de performance estão separados.
- Testes e reprocessamentos foram excluídos com evidência ou permanecem como conflito `partial`.
- Arquivos aplicáveis existem; omitidos estão justificados.
- Nenhuma entrega canônica depende de JSON ou CSV oculto.
- Links de evidência estão preservados.
- A execução anterior não foi sobrescrita.
- `11-retrospectiva-final.md` contém `## Análise detalhada` e `## Índice de insumos completos`.
- O índice referencia todos os módulos, bases, partes e assets aplicáveis, com contagem de entidades.

## Checklist analítico

- Projetado versus realizado existe ou há gate humano registrado.
- Meta e realizado usam janela compatível; qualquer proporcionalidade está documentada.
- Fórmulas canônicas foram recalculadas.
- Rankings mostram funil completo.
- `bases/cobertura-midia.md` contém as 15 dimensões obrigatórias.
- Canais, destinos, campanhas, conjuntos, anúncios e breakdowns possuem bases próprias.
- Todas as entidades com investimento aparecem nas bases, inclusive as de zero resultado.
- Investimento foi reconciliado entre geral, canal, campanha, conjunto e anúncio dentro da tolerância documentada.
- Ranking e narrativa apontam para a tabela-mãe; top performers não substituem o inventário completo.
- Rankings integrais preservam intermediários, perdedores, zero resultado, não atribuídos e inconclusivos; top N aparece apenas como leitura adicional.
- Dados, análise, interpretação, hipóteses e evidências permanecem disponíveis; não existe “resumo do resumo” como única entrega.
- Campanha, conjunto e anúncio mostram o funil completo e têm rankings por lentes diferentes.
- Público/keyword, região, gênero, idade, dispositivo e posicionamento foram coletados ou marcados individualmente como `partial`, `unavailable` ou `not_applicable` com justificativa.
- IDs, previews, assets, copy e métricas de vídeo têm cobertura explícita.
- MQL/SQL/venda usam definições validadas.
- First paid touch e não atribuídos estão explícitos.
- Métricas são julgadas por meta, verba, histórico e break-even.
- A maturação do ciclo foi considerada.
- Fatos, hipóteses e inputs humanos estão separados.

## Checklist de atendimento

- SLA usa horas úteis do cliente.
- Primeiro contato não foi contado como follow-up.
- Cadência usa 7 ou mais follow-ups em 7 dias.
- Mensagens automáticas não contam como atendimento humano.
- Não localizado não foi classificado como não atendido.
- Conversas não localizadas e conteúdos não avaliáveis permaneceram na base com estado explícito.
- Áudios, vídeos e anexos foram transcritos ou tiveram a limitação declarada, sem penalidade de conteúdo inventada.
- Execução operacional, competência comercial e resultado de funil aparecem separados; não existe nota única combinada.
- A versão, o status e a cobertura da rubrica comercial estão explícitos.
- Score definitivo de competência aparece apenas com rubrica calibrada.
- Toda flag P0–P4 referencia evidência e regra aplicada.
- Fechamento, pagamento, aceite e agendamento confirmado usam evidência explícita.
- Tarefa versus ação e etapa do CRM versus conversa foram reconciliadas sem alteração automática.
- A calibração, quando executada, usou de 20 a 30 conversas variadas, pelo menos 80% de concordância geral e 100% de captura dos P0 da amostra.

## Checklist do modo autônomo

- `decisoes.md` existe, tem frontmatter e a tabela do ledger com as colunas obrigatórias.
- Toda definição de funil, premissa econômica, janela, exclusão de teste, calendário e conflito resolvido por precedência tem linha no ledger.
- Todo módulo não `complete` e toda dimensão de mídia `partial` ou `unavailable` têm lacuna registrada.
- Nenhuma definição foi inventada sem base; sem base, é lacuna.
- `--review-ready` retornou `OK` antes de apresentar o pacote.
- Correções geraram nova `run_id` com `parent_run_id`; a execução anterior permanece intacta.
- `--approval-ready` só passa sem decisões `assumida` e sem lacunas `aberta`.

## Checklist de publicação

- `validate_retrospectiva.py <run_dir> --approval-ready` retornou `OK`.
- `retrospectiva aprovada` está registrada.
- O manifesto Drive é versionado.
- O manifesto Drive cobre retrospectiva final, módulos analíticos, todas as bases, evidências e assets; não somente o resumo.
- Publicação externa tem autorização explícita.
- Continuação para o ROPRE foi escolhida pelo usuário.
