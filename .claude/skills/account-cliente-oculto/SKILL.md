---
name: account-cliente-oculto
description: "Simulacao de cliente oculto: cria perfil de comprador ficticio, operador executa no canal real, IA analisa a conversa e gera relatorio com nota 0-10. Use quando o operador disser 'cliente oculto', 'mystery shopping', 'testar atendimento', 'simular compra', ou na Semana 3 do modelo Inside Sales (POP 3.2)."
area: account
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
outputs: ["account-cliente-oculto.json"]
week: 3
modelo_venda: inside-sales
estimated_time: "1.5h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Cliente Oculto (POP 3.2 — Inside Sales)

Voce e um especialista em avaliacao de experiencia de compra e mystery shopping. Vai criar um cenario de simulacao realista para testar o atendimento comercial do cliente e, apos a execucao pelo operador, analisar a conversa gerando um relatorio detalhado com nota e recomendacoes.

> **Posição no fluxo:** Semana 3, cabeça do modelo **Inside Sales** (POP 3.2). Roda **antes** do Diagnóstico Comercial (3.3) — é um input independente que mede a realidade do atendimento; o comercial usa esses achados. Mínimo 3-5 simulações em horários variados.

## Dados necessários

1. `client.json` (seção `briefing`) — NOME_CLIENTE, PRODUTO_SERVICO, CANAL_CONTATO
2. `outputs/geral-persona-icp.json` — RESUMO_ICP, perfil demografico, comportamento
3. `outputs/account-diagnostico-comercial.json` — **se já existir** (opcional; normalmente o cliente oculto roda antes do comercial)
4. `client.json` (seção `connectors`) — dados adicionais de canais

Confirme com o operador:

> Vamos criar e executar um cliente oculto para {NOME_CLIENTE}.
> Canal principal: {CANAL — WhatsApp / formulario / email / Instagram DM}
> Correto? IMPORTANTE: voce (operador) vai executar a simulacao manualmente. Eu crio o roteiro e depois analiso.

---

## Geração

Gere o output COMPLETO de uma vez: perfil do comprador + script da simulação. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/criterios-avaliacao-cliente-oculto.md` para os criterios de avaliação.

### Perfil do comprador simulado

- Nome fictício, contexto plausível e específico
- Urgência (alta/média/baixa) com motivo
- Budget declarado (como/quando mencionar)
- Objeção principal (alinhada ao diagnóstico)
- Nível de conhecimento do produto

### Script da simulação

**Mensagem de abertura:** como o ICP real enviaria
**Mensagens de acompanhamento:** se não houver resposta (30min, 2h)
**4 perguntas para fazer ao longo da conversa:** cada uma testando uma dimensão (conhecimento do produto, objeção de preço, urgência/follow-up, personalização)
**Comportamento do comprador:** atraso de resposta, cautela, objeção de preço na proposta, "vou pensar" para testar follow-up

Apresente ao operador e peça validação de que é realista.

### Execução (MANUAL pelo operador)

> **ATENCAO: Esta etapa e MANUAL.** Voce (operador) executa a simulação seguindo o roteiro.
>
> **Instrucoes:**
> 1. Use numero/conta que NÃO esteja associado a V4 ou ao seu nome
> 2. Siga o roteiro mas adapte naturalmente
> 3. Anote tempos exatos de cada resposta
> 4. Documente TODA a conversa (print ou cópia)
> 5. NÃO revele que é teste
> 6. Se pedirem dados sensíveis, invente dados fictícios
>
> Cole aqui o histórico completo com horários quando terminar.

Aguarde o operador executar e colar o histórico.

### Análise da conversa e relatório

Após receber o histórico, analise e gere o relatório:

**Nota geral: X/10** (EXCELENTE 9-10 / BOM 7-8 / REGULAR 5-6 / RUIM 3-4 / CRITICO 0-2)

**7 critérios avaliados:**
1. Tempo de primeira resposta (meta: < 5 min)
2. Qualidade da abordagem inicial
3. Identificação de necessidade
4. Conhecimento do produto
5. Tratamento de objeção de preço
6. CTA e tentativa de avançar o funil
7. Follow-up após conversa

Para cada: nota 0-10 + observação + evidência (trecho da conversa).

**Pontos fortes** (com evidência)
**Pontos críticos** (em ordem de impacto, com: problema, impacto estimado, como o SDR IA vai resolver)

**Impacto estimado do SDR IA:**
- Tempo de resposta: de {atual} para < 5 segundos
- Taxa de contato: de {atual}% para {projeção}%
- Taxa de qualificação: de {atual}% para {projeção}%
- Impacto financeiro: +R${valor}/mês

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais (não inventou)?
- [ ] Perfil é realista (time não perceberá que é teste)?
- [ ] Critérios de avaliação são justos e baseados em evidência?
- [ ] Impacto do SDR IA é realista (não exagerado)?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o relatório COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "O relatorio reflete fielmente o que voce observou?"
- "Algum detalhe que interpretei errado?"
- "Os pontos criticos estao na ordem certa de impacto?"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/account-cliente-oculto.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira a próxima skill com base nas dependências do frontmatter e no estado da KB
   - "Cliente oculto concluido. Nota: {X}/10. Pontos criticos: {lista}."
   - Sugira: `/account-diagnostico-comercial` (3.3) — usa estes achados para cravar o gargalo e calibrar a qualificação.

**NOTA:** O relatório pode ser compartilhado com o cliente como evidência do valor do SDR IA. O contraste "antes vs depois" é poderoso.
