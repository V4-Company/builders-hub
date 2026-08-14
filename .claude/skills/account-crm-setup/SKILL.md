---
name: account-crm-setup
description: "Configura o CRM Kommo com pipeline personalizado, réguas de boas-vindas e nutrição, e testa com lead fictício. Semi-manual — operador executa no Kommo. Use quando disser /account-crm-setup ou 'configurar CRM' ou 'setup Kommo' ou 'automação de leads'."
area: account
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
inputs:
  - client.json (briefing)
  - geral-persona-icp.json
  - designer-manual-marca.json
output: account-crm-setup.json
week: 4
type: semi-manual
estimated_time: "4h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# CRM Setup — Pipeline + Réguas de Automação (POP 3.6)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (e-commerce / inside-sales / pdv). É "Implementação **ou** Otimização" — comece classificando o cenário de partida. O pipeline reflete o processo definido nos diagnósticos do modelo; o CRM **espelha** o processo (não o contrário).

Você é um consultor especializado em automação comercial para PMEs brasileiras, com experiência em Kommo CRM. Vai classificar o cenário do cliente, criar/otimizar o pipeline personalizado, templates de mensagem para as réguas de automação (boas-vindas e nutrição), e guiar o operador na configuração — incluindo migração/limpeza de base e governança.

### Cenário de partida (classifique primeiro)
- **Cenário A — do zero:** sem CRM. Implementar do zero.
- **Cenário B — subutilizado:** CRM existe mas mal usado. Reconfigurar + adotar.
- **Cenário C — otimização:** CRM em uso. Otimizar sem ruptura (esgotar otimização antes de propor troca de ferramenta).

## Dados necessários

1. `client.json` (seção `briefing`) — nome, segmento, produto/serviço, processo comercial atual, WhatsApp, CRM atual (se houver)
2. `outputs/geral-persona-icp.json` — ICP, dores, objeções, linguagem
3. `outputs/designer-manual-marca.json` — tom de voz, vocabulário (se existir — melhora qualidade)
4. `client.json` (seção `history`) — decisões anteriores

---

## Geração

Gere o output COMPLETO de uma vez: pipeline + réguas + guia de configuração + checklist de teste. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/guia-kommo-setup.md` para referência de configuração.

### Pipeline de vendas (personalizado)

Etapas baseadas no processo comercial do cliente:
```
[Etapa 1] → [Etapa 2] → ... → [Fechado-Ganho / Fechado-Perdido]
```
Personalize nomes conforme o processo real (ex: "Orçamento Solicitado" em vez de "Proposta Enviada").

### Tags e propriedades

- Origem: Meta Ads | Google Ads | Indicação | Orgânico | Site | WhatsApp
- Score SDR: 1-5 estrelas
- Produto de interesse: [do briefing]
- Temperatura: Frio | Morno | Quente

### Régua 1 — Boas-vindas (3 mensagens automáticas)

*Mensagem 1 (imediata):* Boas-vindas + confirmação + próximo passo. Máx 3 frases.
*Mensagem 2 (24h sem resposta):* Follow-up leve + conteúdo de valor + CTA suave. Máx 3 frases.
*Mensagem 3 (48h sem resposta):* Última tentativa + pergunta direta + abertura de saída. Máx 3 frases.

### Régua 2 — Nutrição (4 touchpoints em 30 dias)

Para leads score 1-3 estrelas:
*Semana 1:* Conteúdo de valor (WhatsApp + Email) — educativo
*Semana 2:* Caso de sucesso / prova social (WhatsApp + Email) — inspiracional
*Semana 3:* Diferencial do produto (WhatsApp) — educativo + pitch leve
*Semana 4:* Oferta / CTA direto (WhatsApp + Email) — direto, urgência real

### Guia de configuração Kommo (passo a passo)

**PASSO 1:** Criar pipeline (Settings > Pipeline). Renomear etapas.
**PASSO 2:** Configurar tags e campos customizados.
**PASSO 3:** Configurar Salesbot (boas-vindas) — trigger, condições, mensagens com delays.
**PASSO 4:** Configurar Salesbot (nutrição) — trigger por score, 4 ações com delays de 7 dias.
**PASSO 5:** Conectar WhatsApp Business. Testar envio.

### Migração e limpeza de base (Cenários B e C)

Se já existe base/CRM:
- **Migrar base ativa primeiro**, histórico depois — nunca tudo de uma vez.
- **Deduplicar, padronizar e enriquecer** antes de importar (sem lixo).
- Mapear campos antigos → novos; registrar o que não migra e por quê.

### Governança e adoção

- **Campos obrigatórios** por etapa (origem, score, motivo de perda como lista fechada, próximo follow-up).
- **Dashboards operacionais** (funil, SLA, motivos de perda).
- **Treinamento + documento de governança** + plano de adoção (o CRM só vale se o time usar).

### Checklist de teste

**TESTE 1: PIPELINE** — criar lead manual, mover por etapas, verificar tags
**TESTE 2: RÉGUA DE BOAS-VINDAS** — criar lead, verificar 3 mensagens com timings
**TESTE 3: RÉGUA DE NUTRIÇÃO** — criar lead score baixo, verificar sequência
**TESTE 4: INTEGRAÇÃO WHATSAPP** — enviar teste, verificar formatação e histórico
**TESTE 5: CENÁRIO REAL** — submeter formulário, verificar pipeline + tags + salesbot

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP)?
- [ ] Mensagens de boas-vindas têm máximo 3 frases cada (WhatsApp)?
- [ ] Régua de nutrição endereça a objeção principal do ICP?
- [ ] Pipeline reflete o processo real (não genérico)?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador — pipeline, réguas, guia e checklist.

Revise o output. O que está errado, exagerado ou faltando?

- "O pipeline reflete o processo real de vendas? Nomes das etapas fazem sentido?"
- "As tags cobrem todas as origens de leads?"
- "O tom das mensagens está natural e alinhado com a marca?"
- "As mensagens de boas-vindas são curtas o suficiente para WhatsApp?"
- "A régua de nutrição endereça a objeção principal do ICP?"

**Próximo passo (semi-manual):**
O operador executa a configuração no Kommo seguindo o guia passo a passo. Após configurar, executa o checklist de teste. Se algum teste falhar, ajude a debugar.

## Finalização

Operador aprova (com ou sem ajustes, após testes passarem).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/account-crm-setup.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph

## Formato do output (account-crm-setup.json)

```json
{
  "pipeline_stages": [{ "order": 1, "name": "Lead", "description": "string", "auto_actions": ["string"] }],
  "tags": { "origin": ["string"], "score": ["string"], "products": ["string"], "temperature": ["string"] },
  "welcome_sequence": [{ "order": 1, "timing": "imediata", "channel": "whatsapp", "message": "string" }],
  "nurture_sequence": [{ "week": 1, "channel": "whatsapp + email", "message_type": "string", "whatsapp_message": "string", "email_subject": "string", "email_body": "string" }],
  "test_checklist": [{ "test": "Pipeline", "steps": ["string"], "passed": null }]
}
```


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do setup do CRM: número de etapas do pipeline e réguas configuradas. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
