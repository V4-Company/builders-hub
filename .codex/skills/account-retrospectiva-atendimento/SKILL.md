---
name: account-retrospectiva-atendimento
description: Audita retrospectivamente todas as conversas comerciais, classificando atendimento, SLA útil, conexão, abandono, resposta pendente, follow-up, cadência e qualidade comercial calibrada com evidência por lead. Use quando o cliente tiver Chatwoot, Blip, Digitalize, WhatsApp, Kommo ou outra ferramenta conversacional conectada.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.2.0
---

# Retrospectiva de atendimento

Leia no maestro `references/atendimento.md`, `references/qualidade-comercial.md`, `references/fontes-e-reconciliacao.md` e `references/contrato-markdown.md`. Quando disponível, reutilize a máquina de estados de `monitor-leads-atendimento`.

## Descoberta

1. Identifique a ferramenta no contexto existente.
2. Se não estiver registrada, procure nas conexões n8n, CRM e documentos do cliente. Sem acesso, registre lacuna em `decisoes.md` com a conexão necessária e siga; nunca peça segredo em texto.
3. Valide conta, inbox/canal e cobertura.
4. Localize a rubrica comercial aprovada do cliente. Se não existir, crie um rascunho a partir de `assets/rubrica-comercial-cliente.md` do maestro, execute a análise operacional e mantenha a competência comercial como `provisional` até calibrar. Selecione automaticamente a amostra de 20 a 30 conversas variadas para calibração e coloque-a em `decisoes.md`, seção `## Amostra de calibração da rubrica`.
5. Calendário operacional sem documento: infira o expediente pela distribuição de mensagens humanas e registre decisão `calendario_operacional` como `assumida`.

## Saídas

- `06-atendimento.md`
- `bases/conversas.md`

## Base obrigatória

Uma linha por conversa ou atendimento, com lead, contato, negócio, vendedor, campanha, MQL, timestamps, tempos corrido e útil, estado, cadência, link da conversa/card e `evidence_id`.

Separe formalmente:

- execução operacional, com score e cobertura;
- competência comercial por dimensão, score somente quando calibrado, cobertura e `rubric_version`;
- resultado do funil, sem incorporá-lo às notas anteriores;
- severidade P0–P4, confiança e status de revisão humana.

Nunca gere uma nota total que misture essas três camadas. Sem conversa, sem humano ou sem transcrição suficiente, use o estado de avaliabilidade correspondente em vez de inventar julgamento.

Separe IA, bot, sistema, lead e humano. Mensagem automática não conta como atendimento humano. Áudio, vídeo e anexo contam como resposta operacional; conteúdo só pode ser julgado quando transcrito. Sem match seguro é `not_located`, nunca `não atendido`.

Reconcilie tarefa versus ação e etapa do CRM versus evidência da conversa. Exija evidência explícita para fechamento e demais eventos críticos. Registre divergências; não altere card, etapa ou tarefa.

Use `scripts/business_time.py` para calcular SLA quando os timestamps e o calendário operacional estiverem disponíveis.

O escopo é relatório. Não envie alerta, não crie tarefa e não escreva no CRM.
