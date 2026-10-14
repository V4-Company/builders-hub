# Janelas temporais da retrospectiva

## Regra central

A retrospectiva pertence ao quarter solicitado, mas o julgamento de performance começa somente quando o projeto entrou em operação comparável.

Registre três janelas separadas:

1. `quarter_window`: início e fim do quarter calendário;
2. `pre_operational_window`: descoberta, onboarding, estruturação, testes, aprovações e implantação anteriores ao go-live;
3. `performance_window`: do primeiro dia/evento real após o go-live até o último dia completo disponível.

O pré-operacional continua na retrospectiva como contexto e entregas. Não o misture ao denominador de CPL, CPMQL, CPSQL, CPVenda, ROAS, conversão, vendedor ou atendimento.

## Descoberta do corte

Localize e reconcilie:

- aprovação do go-live;
- ativação técnica;
- primeiro investimento real;
- primeiro lead, pedido ou evento real;
- estabilização da integração;
- relançamentos ou mudanças estruturais dentro do quarter.

Se as datas divergirem, use como `analysis_start` o primeiro evento real em produção com tracking funcional. Preserve as demais datas como marcos. Conflito material ou dúvida sobre produção versus teste exige validação humana.

Normalize timestamps para o fuso do cliente antes de determinar o dia. Um evento em UTC no dia anterior pode pertencer ao dia operacional seguinte no CRM.

## Testes e transição

- Exclua smoke tests, leads internos, pedidos de teste e reprocessamentos técnicos dos resultados de performance.
- Preserve-os em uma base de exclusões com ID, motivo, regra, evidência e revisor.
- Não exclua por nome suspeito sem prova; marque `human_review_required`.
- Se a fonte agregada não permitir retirar testes, mantenha o resultado `partial` e declare o impacto máximo possível.

## Metas e comparações

- Não compare uma janela pós-go-live parcial com a meta integral do quarter sem ajuste.
- Use meta proporcional ao tempo/verba quando a premissa permitir, ou a meta mensal/coorte oficialmente aprovada.
- Rotule janelas diferentes: quarter, pós-go-live, janela fechada de mídia, coorte de CRM e snapshot.
- Campanhas só competem quando as janelas e eventos são compatíveis.

## Saída obrigatória

O manifesto e a retrospectiva final contêm `## Janelas temporais da retrospectiva` com:

| janela/marco | início | fim | uso analítico | fonte | confiança |
|---|---|---|---|---|---|

Todo Markdown canônico registra `analysis_start` no frontmatter. Para projeto já operacional antes do quarter, `analysis_start` é igual a `period_start`. Para bases com recorte mais estreito, use o primeiro dia realmente contido naquela base.
