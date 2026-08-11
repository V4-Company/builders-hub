# Fluxograma operacional

Use este fluxo para escolher o ponto de entrada, controlar retornos entre etapas e encerrar a entrega sem repetir trabalho válido.

```text
INÍCIO
  |
  v
[0. Auditar o estado do projeto]
  |-- projeto novo ----------------------------> [1. Descoberta]
  |-- atualização com base válida -----------> [2. Preparar coleta]
  |-- apenas nova leitura dos mesmos dados ----> [4. Diagnóstico]
  '-- apenas interface/QA com dados válidos --> [5. Experiência ou 6. QA]

[1. Descoberta]
  |-- escopo incompleto e bloqueante ----------> solicitar decisão e pausar
  '-- gate válido ----------------------------> [2. Preparar coleta]

[2. Preparar coleta]
  |-- credencial ausente ----------------------> usar fonte pública alternativa
  |                                               ou registrar bloqueio
  |-- custo relevante sem autorização --------> informar volume/custo e pausar
  '-- fontes prontas --------------------------> [3. Coleta]

[3. Coleta]
  |-- erro recuperável ------------------------> corrigir configuração e repetir a fonte
  |-- fonte indisponível ----------------------> registrar limitação e seguir se não bloquear
  |-- novo concorrente em watchlist -----------> registrar; não ampliar escopo automaticamente
  |-- referência ampliada relevante ----------> classificar origem e papel competitivo
  '-- gate válido ----------------------------> [4. Processamento]

[4. Processamento]
  |-- asset ausente/corrompido ----------------> retornar somente o item para [3. Coleta]
  |-- derivado inválido -----------------------> reprocessar somente o item afetado
  '-- gate válido ----------------------------> [5. Diagnóstico]

[5. Diagnóstico]
  |-- conclusão sem evidência ----------------> voltar ao inventário/processamento
  |-- lacuna muda a decisão -------------------> coleta complementar autorizada
  |-- experiência navegável necessária ------> [6. Experiência]
  '-- relatório/dataset suficiente ------------> [7. QA e homologação]

[6. Experiência]
  |-- divergência de contagem -----------------> corrigir dado gerado, não maquiar a interface
  |-- falha de mídia --------------------------> otimizar/substituir derivado preservando a fonte
  '-- build funcional -------------------------> [7. QA e homologação]

[7. QA e homologação]
  |-- falha metodológica ----------------------> [5. Diagnóstico]
  |-- falha de dados --------------------------> [3. Coleta] ou [4. Processamento]
  |-- falha de interface ----------------------> [6. Experiência]
  '-- aprovado --------------------------------> decisão de publicação

[Decisão de publicação]
  |-- autorizada ------------------------------> deploy + smoke test
  '-- não autorizada --------------------------> build/pacote offline
                    |
                    v
[8. Encerramento]
  manifest + README + audit + limitações + status final + próxima atualização
```

## Matriz de decisão

| Situação encontrada | Ação | Pode seguir? |
|---|---|---|
| Falta de informação que não altera a decisão | Registrar premissa e limitação | Sim, como `partial` |
| Falta de informação que invalida o objetivo | Registrar bloqueio e pedir decisão | Não |
| Fonte/API falhou, mas existe alternativa pública equivalente | Trocar a rota e preservar o erro original | Sim |
| Fonte/API falhou sem alternativa equivalente | Documentar cobertura incompleta | Somente se o objetivo continuar válido |
| Novo player aparece durante a pesquisa | Adicionar à watchlist com origem | Não ampliar a coleta sem aprovação |
| Novo asset de item já conhecido | Coletar e processar incrementalmente | Sim |
| Métrica da interface diverge da base | Corrigir o pipeline/dataset | Não antes da correção |
| Deploy não foi autorizado | Entregar build e pacote offline | Sim, sem publicar |

## Regra de retorno

Retorne sempre ao menor ponto capaz de corrigir a falha. Não reinicie toda a esteira quando um asset, uma transcrição, uma métrica ou uma tela puder ser regenerada isoladamente. Registre cada retorno em `status.md` e no `handoff.json` da etapa afetada.

## Critério de encerramento

Feche o fluxo somente quando o gate de QA estiver aprovado e a forma de entrega estiver definida. O encerramento deve informar o snapshot analisado, cobertura, limitações, caminhos dos artefatos, status do deploy e condição para a próxima atualização.
