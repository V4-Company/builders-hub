# Atendimento comercial

## Escopo da retrospectiva

Somente relatório e evidência. Não enviar alertas, criar tarefas ou escrever no CRM.

Inclua conversas e negócios ganhos, perdidos e abertos que pertençam ao período analisado. Janela de maturação explica o status; não elimina registros.

## Relógio útil

Calcule tempo corrido e tempo útil, mas avalie o time apenas pelo calendário operacional validado do cliente:

- fuso;
- horário por dia da semana;
- finais de semana trabalhados;
- feriados nacionais, estaduais, municipais e exceções;
- recessos e pausas.

Lead recebido fora do expediente começa seu SLA na próxima abertura. Nunca penalize o time pelas horas em que não opera.

## Estados mínimos

- não localizado;
- recebido fora do expediente;
- sem primeiro atendimento;
- primeiro atendimento dentro ou fora do SLA útil;
- lead respondeu;
- conexão realizada;
- aguardando contato humano;
- handoff sem atendimento humano;
- vendedor deixou lead sem resposta;
- somente primeiro contato;
- follow-up insuficiente;
- cadência cumprida;
- conversa encerrada com motivo;

`Não localizado` é estado de cobertura. Ele continua na base e nunca é tratado como falha do vendedor sem outra evidência.

## Cadência

Primeiro contato não conta como follow-up. A cadência padrão é **7 ou mais follow-ups em até 7 dias**. Mensagens consecutivas da mesma tentativa contam como um toque; mensagens automáticas, sistema e mudança de etapa não contam.

Calcule:

- `followups_7d`;
- dias distintos com tentativa;
- maior intervalo sem tentativa;
- cadência cumprida, incompleta ou ausente;
- conversão por quantidade de follow-ups;
- resultado por vendedor.

## Qualidade

Leia `qualidade-comercial.md`. Avalie conforme projeto, público, produto e serviço. Separe fala da IA, bot, sistema, lead e humano. Verifique abertura, entendimento da necessidade, qualificação, clareza, personalização, objeções, próximo passo, tom, promessa indevida e encerramento.

Não misture execução operacional, competência comercial e resultado de funil. Use a rubrica versionada do cliente e marque competência como `provisional` enquanto ela não estiver calibrada.

Áudio, vídeo e anexos contam como interação. Transcreva quando autorizado para avaliar conteúdo; se não for possível, declare `not_evaluable_untranscribed_media` nas dimensões dependentes do anexo.

Toda classificação aponta para conversa/card e trechos de evidência, respeitando o limite de exposição de dados pessoais.
