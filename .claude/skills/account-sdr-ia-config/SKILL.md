---
name: account-sdr-ia-config
description: "Configuracao do SDR IA no Patagon + integracao Kommo: setup do agente, field mapping, alertas para vendedor e teste com 5 leads simulados. Use quando o operador disser 'configurar patagon', 'setup sdr', 'integrar kommo', 'colocar o agente no ar', ou apos copy-scripts-sdr."
area: account
author: luizfreitasv4
version: 1.0.0
dependencies:
  - copy-scripts-sdr
  - account-crm-setup
outputs: ["account-sdr-ia-config.json"]
week: 4
estimated_time: "4h"
semi_manual: true
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Configuracao do SDR IA (Patagon + Kommo) — POP 3.7

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) a todos os modelos. Coloca o agente do `copy-scripts-sdr` no ar, integrado ao CRM (account-crm-setup). Sobe ao vivo só após validar o scoring com leads reais.

Voce e um guia tecnico para configuracao do agente SDR IA no Patagon com integracao Kommo CRM. Esta skill e SEMI-MANUAL: voce gera as instrucoes passo a passo e o operador executa no Patagon e Kommo. Apos cada etapa, o operador confirma que executou.

> **IMPORTANCIA:** Esta e a skill que coloca o SDR IA no ar. Tudo das semanas anteriores converge aqui. Erro na configuração = leads mal qualificados ou alertas que não chegam.

> **PRE-REQUISITOS:**
> - WhatsApp Business do cliente conectado ao Patagon
> - Kommo CRM configurado com pipeline (account-crm-setup)
> - Scripts SDR aprovados pelo cliente (copy-scripts-sdr)
> - Brandbook com tom de voz aprovado

## Dados necessários

1. `client.json` (seção `briefing`) — NOME_CLIENTE, PRODUTO_SERVICO
2. `outputs/copy-scripts-sdr.json` — TODOS os scripts, perguntas, fluxos, objeções
3. `outputs/account-diagnostico-comercial.json` — critérios 1-5 estrelas, SLA
4. `outputs/designer-manual-marca.json` — TOM_DE_VOZ, nome do agente
5. `outputs/account-crm-setup.json` — pipeline configurado no Kommo

Se alguma dependência não estiver completa:

> BLOQUEIO: A skill {NOME_SKILL} precisa estar completa antes de configurar o SDR IA.
> Execute `/{skill}` antes de continuar.

Confirme com o operador:

> Vamos configurar o SDR IA de {NOME_CLIENTE}.
> - WhatsApp Business conectado ao Patagon? [sim/nao]
> - Kommo configurado com pipeline? [sim/nao]
> - Scripts aprovados pelo cliente? [sim/nao]
> - Vendedor para alertas: Nome e WhatsApp?
>
> Se algum item for "nao", precisamos resolver antes.

---

## Geração

Gere o output COMPLETO de uma vez: guia de configuração Patagon + integração Kommo + alertas + teste com 5 leads. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/guia-patagon-kommo.md` para detalhes técnicos.

### Configuração do agente no Patagon (passo a passo)

**PASSO 1:** Criar agente (nome, descrição)
**PASSO 2:** Configurar persona (personalidade completa, tom de voz, regras: máx 3 frases, nunca revelar IA, etc.)
**PASSO 3:** Configurar mensagem de boas-vindas (colar mensagem aprovada)
**PASSO 4:** Configurar perguntas de qualificação (Q1-Q5, abertas, obrigatórias)
**PASSO 5:** Configurar regras de scoring (critérios por estrela + ação para cada score)
**PASSO 6:** Configurar tratamento de objeções (cada objeção + resposta + genérica)
**PASSO 7:** Configurar follow-ups (1h, 24h, 3d + máx 3)
**PASSO 8:** Configurar handoff (mensagem de transferência + destinatário)
**PASSO 9:** Salvar (NÃO ativar ainda — esperar testes)

### Integração Patagon → Kommo

**PASSO 1:** Conectar (Settings → Integrations → Kommo, API key)
**PASSO 2:** Field mapping (nome, telefone, score, produto, UTMs, histórico, resumo)
**PASSO 3:** Configurar pipeline destino (score 4-5★ → Qualificados, 3★ → Nutrição, 1-2★ → Frios)
**PASSO 4:** Tags automáticas (por score e por origem/UTM)
**PASSO 5:** Testar conexão (enviar lead teste, verificar campos e tags)

### Alertas para vendedor

**PASSO 1:** Definir destinatários (vendedor principal + backup)
**PASSO 2:** Template do alerta (nome, score, interesse, resumo, link Kommo, SLA)
**PASSO 3:** Condições de disparo (score >= 4★, qualificação concluída, dentro do horário comercial)
**PASSO 4:** Escalamento (se vendedor não responder em X min → backup → mensagem automática ao lead)
**PASSO 5:** Relatório diário opcional

### Teste com 5 leads simulados

**Lead 1 — 5★ (quente):** urgente, decisor, com budget → resultado esperado: score 5★, alerta, Kommo "Qualificado"
**Lead 2 — 4★ (qualificado):** interessado, sem urgência → resultado esperado: score 4★, alerta
**Lead 3 — 3★ (morno):** curioso, pesquisando → resultado esperado: score 3★, sem alerta, "Nutrição"
**Lead 4 — 1-2★ (frio):** não é ICP → resultado esperado: score baixo, tag "Frio"
**Lead 5 — Com objeção forte:** interessado + objeção de preço → testar tratamento

**Checklist por lead:**
- [ ] Resposta < 5 segundos
- [ ] Boas-vindas correta
- [ ] Qualificação na ordem
- [ ] Score correto
- [ ] Kommo com campos preenchidos
- [ ] Tag correta
- [ ] Etapa do pipeline correta
- [ ] Alerta enviado (se 4-5★)
- [ ] Tom consistente com brandbook
- [ ] Nada pareceu robótico

**Tabela de resultados:**

| Lead | Score esperado | Score real | Kommo OK | Alerta OK | Tempo | Status |
|------|---------------|------------|----------|-----------|-------|--------|

Se houver falhas: instruções de debug (score incorreto, campo não mapeado, alerta não chegou, tom inconsistente).

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Todos os scripts aprovados foram incluídos nas instruções?
- [ ] Field mapping cobre todos os campos necessários?
- [ ] SLA nos alertas é consistente com o diagnóstico comercial?
- [ ] 5 cenários de teste cobrem todos os fluxos (5★, 4★, 3★, 1-2★, objeção)?

Se falhou → regenere silenciosamente.

## Apresentação e decisões

Apresente o output COMPLETO ao operador — guia completo de configuração.

O operador executa cada etapa sequencialmente no Patagon e Kommo. Após cada bloco, confirma execução:

1. "Agente criado no Patagon? Alguma tela diferente?"
2. "Integração Kommo funcionando? Lead teste chegou com campos?"
3. "Alertas configurados? Vendedor recebeu teste?"
4. "5 testes executados — resultados?"

Se todos os testes passaram → go-live. Se houver falhas → debug e reteste.

## Finalização

Operador aprova (todos os testes passam).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/account-sdr-ia-config.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. **Ative o agente no Patagon** (com aprovação do operador e do cliente)
5. Informe:
   - "SDR IA configurado, testado e no ar!"
   - "Recomendações pós go-live:"
   - "  1. Monitorar os primeiros 20 leads reais (ajustar scoring se necessário)"
   - "  2. Coletar feedback do vendedor sobre qualidade dos leads"
   - "  3. Revisar métricas após 7 dias: qualificação, SLA, conversão"
   - "  4. Ajustar scripts com base nos dados reais"

**ALERTA:** O agente está no ar. Leads reais sendo qualificados. Monitore de perto nas primeiras 48h.
