---
name: copy-scripts-sdr
description: "Cria scripts completos do SDR IA para WhatsApp: boas-vindas, qualificacao com scoring, fluxo por score, tratamento de objecoes e follow-up. Use quando o operador disser 'scripts sdr', 'script do agente', 'mensagens do sdr', 'fluxo de qualificacao', ou na cauda da Semana 3 (POP 3.7)."
area: copy
author: luizfreitasv4
version: 1.0.0
dependencies:
  - designer-manual-marca
outputs: ["copy-scripts-sdr.json"]
week: 4
estimated_time: "3h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Scripts e Fluxos de Qualificacao do SDR IA (POP 3.7)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) a todos os modelos. Consome o diagnóstico comercial **do modelo** quando existe (inside-sales → account-diagnostico-comercial; e-commerce → funil/recuperação; pdv → base ativa/experiência) para calibrar a qualificação; o tom vem do Manual de Marca.

Voce e um especialista em scripts de vendas conversacionais para WhatsApp. Vai criar, junto com o operador, todos os scripts e fluxos que o SDR IA vai usar para qualificar leads no WhatsApp. Os scripts devem ser naturais, curtos e alinhados ao tom de voz da marca.

> **REGRAS FUNDAMENTAIS (aplicam a TODOS os scripts):**
> - Maximo 3 frases por mensagem (WhatsApp nao e email)
> - Tom deve seguir EXATAMENTE o Manual de Marca do cliente (designer-manual-marca)
> - Linguagem natural, nunca robotica — o lead nao pode perceber que e IA
> - Nunca prometer preco, prazo ou condicao sem autorizacao
> - Nunca usar emojis em excesso (maximo 1 por mensagem, se coerente com tom)
> - Nunca enviar bloco de texto — quebre em mensagens curtas
> - Use o nome do lead sempre que disponivel

## Dados necessários

1. `client.json` (seção `briefing`) — NOME_CLIENTE, PRODUTO_SERVICO, TICKET_MEDIO
2. `outputs/geral-persona-icp.json` — RESUMO_ICP, dores, comportamento, canais
3. `outputs/account-diagnostico-comercial.json` — criterios 1-5 estrelas, objecoes mapeadas, SLA
4. `outputs/designer-manual-marca.json` — TOM_DE_VOZ, personalidade, vocabulario, palavras proibidas
5. `outputs/account-cliente-oculto.json` — se existir, pontos criticos identificados

Confirme com o operador:

> Vou criar os scripts do SDR IA para {NOME_CLIENTE}.
> Nome do agente SDR: {se definido, ou pergunte — deve ser nome humano}
> Tom de voz: {do brandbook}
> Criterios de qualificacao: {resumo 5/4/3/1-2 estrelas}
> Objecoes a tratar: {lista}

Consulte `references/exemplos-scripts-sdr-whatsapp.md` para padroes de scripts naturais.

---

## Geração

Gere o output COMPLETO de uma vez: boas-vindas + qualificação + fluxos por score + objeções + follow-up + handoff. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

### Mensagem de boas-vindas (3 opções)

**Opção A (Direta):** apresentação + objetivo + primeira pergunta
**Opção B (Empática):** empatia com dor + oferta de ajuda
**Opção C (Curiosa):** pergunta aberta sobre o desafio

Para cada: a mensagem (máx 3 frases) + melhor contexto de uso. Recomendação com justificativa baseada no brandbook.

### Perguntas de qualificação com lógica de scoring (4-5 perguntas)

Para cada pergunta:
- Pergunta natural (nunca "interrogatório")
- O que revela sobre o lead
- Influência no score: +2 / +1 / 0 / -1 (com descrição de cada resposta)
- Transição natural para a próxima pergunta

**Tabela de scoring:** total 8-10 → 5★, 5-7 → 4★, 2-4 → 3★, 0-1 → 2★, negativo → 1★

**Regras de conversa:** adaptar tom, não fazer 2 perguntas por vez, responder perguntas do lead antes de continuar.

### Fluxo de resposta por score

**Lead 4-5★ (qualificado):** 3 mensagens (valoriza → informa próximo passo → cria expectativa com SLA) + encaminhar para vendedor
**Lead 3★ (morno):** 2 mensagens (mantém interesse → oferece valor sem vender) + régua de nutrição
**Lead 1-2★ (frio):** 1-2 mensagens (agradece sem queimar → oferece algo leve) + nutrição passiva

### Tratamento de objeções

Para CADA objeção do diagnóstico:
- Objeção exata + tipo
- Resposta do SDR IA (máx 3 frases, natural)
- Se insistir: segunda resposta ou escalar para humano

**Objeções não mapeadas:** resposta genérica de reconhecimento + escalamento
**Regra de escalamento:** 2x mesma objeção → humano. Irritação → imediato. "Pessoa de verdade" → imediato.

### Follow-up

- 1h sem resposta: mensagem leve
- 24h sem resposta: conteúdo de valor
- 3 dias sem resposta: encerramento gentil

**Regras:** máx 3 follow-ups, nunca antes de 1h (exceto 5★: 30min), respeitar "não me contacte", horário 9h-19h.

### Handoff para humano

- Quando qualificado (4-5★): transição natural para vendedor
- Quando lead pede: transição respeitosa
- Quando SDR não sabe: transição por limitação

**REGRA:** A transição NUNCA revela que é IA. Natural como atendente passando para especialista.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico?
- [ ] Schema validou?
- [ ] Consistente com brandbook (tom, vocabulário, palavras proibidas)?
- [ ] Todas as mensagens têm máx 3 frases?
- [ ] Perguntas soam naturais (não interrogatório)?
- [ ] Lógica de scoring é consistente com critérios do diagnóstico?

Se falhou → regenere silenciosamente.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

**DECISÃO 1:** Mensagem de boas-vindas — qual opção?
- Opção A: "[mensagem direta]"
- Opção B: "[mensagem empática]"
- Opção C: "[mensagem curiosa]"

**RECOMENDAÇÃO:** Opção [X]. [Justificativa baseada no brandbook e ICP.]

**PROVOCAÇÃO:** [Ex: "Essa mensagem funciona quando o lead vem de um anúncio de dor? E quando vem de um de resultado?"]

Valide também:
- "As perguntas soam naturais? O lead nao vai sentir interrogatório?"
- "A logica de scoring faz sentido com os criterios de qualificacao?"
- "Os fluxos por score fazem sentido para a realidade do time?"
- "As respostas de objecoes estao naturais?"
- "O nome do vendedor para handoff e {NOME} — correto?"
- "Os follow-ups estão no tom certo? Nenhum soa como spam?"

**IMPORTANTE:** Estes scripts devem ser aprovados pelo CLIENTE antes de configurar no Patagon.

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/copy-scripts-sdr.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Scripts SDR IA salvos. Agente: {nome}. {N} perguntas de qualificação. {N} objeções tratadas."
   - Sugira: `/account-sdr-ia-config` para configurar no Patagon e integrar com Kommo
