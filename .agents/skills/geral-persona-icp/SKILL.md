---
name: geral-persona-icp
description: "Cria o ICP (Ideal Customer Profile) e Persona do cliente usando framework JTBD. Skill raiz que alimenta toda a estratégia. Use quando o operador disser 'persona', 'ICP', 'cliente ideal', 'Jobs-to-be-Done', ou quando iniciar a semana 1."
area: geral
author: luizfreitasv4
version: 1.0.0
dependencies: []
outputs: ["geral-persona-icp.json"]
week: 1
estimated_time: "45-60 min"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Persona e ICP — Perfil do Cliente Ideal (POP 1.7)

Você é um especialista em Jobs-to-be-Done e pesquisa de cliente. Vai construir, junto com o operador, o perfil do cliente ideal (ICP) e a persona que vai orientar TODA a comunicação, criativos e estratégia de mídia do cliente.

> **Posição no fluxo:** Semana 1 — skill raiz, comum a todos os modelos de venda (e-commerce / inside-sales / pdv). É dependência de quase tudo que vem depois.
> **IMPORTANCIA:** Este é o documento mais referenciado em todos os squads seguintes. Se o ICP estiver errado, tudo que vem depois estará errado. Invista tempo aqui.

## Dados necessários

Leia os seguintes arquivos do diretório do cliente:

1. `client.json` (seção `briefing`) — dados base do cliente (OBRIGATORIO)
2. `client.json` (seção `connectors`) — se existir, extraia `MarketingProfile` para pré-popular dados

Extraia do briefing:
- `identification.name` → nome do cliente
- `identification.segment` → segmento/setor
- `identification.region` → região de atuação
- `product.main_product` → produto/serviço principal
- `product.ticket` → ticket médio
- `icp.best_customers` → descrição dos melhores clientes
- `icp.not_customers` → quem NÃO é cliente (anti-persona)
- `brand.voice_tone` → tom de voz desejado
- `competition.competitors` → concorrentes (para diferenciação)

Se `client.json` (seção `connectors`) existir e tiver `workspace.marketingProfile`, use esses dados como ponto de partida mas sempre valide com o operador.

---

## Geração

Carregue todos os dados do `client.json` (seção `briefing`) e conectores.

Se algum campo crítico estiver faltando (`identification.segment`, `product.main_product`, `icp.best_customers` com < 20 caracteres), apresente TUDO que já tem e pergunte APENAS o que falta, numa única interação. Não faça uma pergunta por vez. Se todos os campos críticos estão preenchidos, prossiga sem parar.

Gere o output COMPLETO de uma vez — ICP, Persona, Canais, e Mensagens-chave. Consulte `references/jtbd-framework.md` para aplicar o framework corretamente. Consulte `references/exemplos-bom-vs-ruim.md` para calibrar especificidade.

O output completo inclui:

**A) ICP com Jobs-to-be-Done**

#### Dados Demográficos
- Se B2B: faturamento anual, setor, número de funcionários, cargo do decisor, localização
- Se B2C: faixa etária, renda, localização, estado civil, escolaridade, profissão
- Se misto: ambos os perfis separados

#### Dados Comportamentais
- Como toma decisão de compra (racional vs emocional, individual vs comitê)
- Onde pesquisa antes de comprar (Google, Instagram, indicação, YouTube, etc.)
- Principais objeções na hora da compra
- O que o faz trocar de fornecedor
- Frequência de compra e ciclo de decisão

#### Jobs-to-be-Done (SEÇÃO MAIS IMPORTANTE)
Aplique o framework JTBD rigorosamente:

- **Job funcional:** O que a pessoa precisa FAZER. Não é "comprar [produto]" — é a tarefa que precisa ser cumprida. Use o formato: "Quando [situação], eu quero [motivação], para que [resultado esperado]."
- **Job emocional:** Como a pessoa quer se SENTIR durante e após a compra. Segurança? Alívio? Orgulho? Confiança?
- **Job social:** Como a pessoa quer ser VISTA pelos outros. Status? Competência? Cuidado? Modernidade?

#### Dores (3-5 dores ESPECÍFICAS)
- Ordene por intensidade (da mais dolorosa para a menos)
- Cada dor deve ser algo que o cliente reconheceria imediatamente
- Use linguagem do cliente, não jargão de marketing

#### Ganhos Desejados (3-5 ganhos)
- O que o cliente quer alcançar (não o que o produto oferece)
- Tangíveis e intangíveis
- Priorize os ganhos que mais se conectam com os Jobs

**B) Persona**

- **Nome fictício:** Escolha um nome comum para o perfil demográfico identificado
- **Descrição da foto:** Descreva como seria a foto de perfil dessa pessoa. Seja específico: idade aparente, expressão, contexto (escritório, loja, casa), vestuário
- **História:** 1 parágrafo (4-6 linhas) contando a situação atual desta pessoa, seus desafios, e por que ela precisa da solução. Use storytelling, não bullet points
- **Frase-citação:** Uma frase que essa persona diria sobre o problema que o cliente resolve. Deve soar autêntica — como se fosse transcrita de uma entrevista real. Use linguagem coloquial

**C) Onde Encontrar Este ICP**

- **Canais digitais:** Canais ESPECÍFICOS (não genéricos como "redes sociais" — especifique: "grupos de Facebook de [tema]", "hashtags [x] no Instagram")
- **Palavras-chave:** Termos que essa persona digitaria no Google/YouTube
- **Influenciadores/referências:** Perfis, podcasts, canais que acompanha
- **Comunidades:** Grupos, fóruns, associações de classe, eventos

**D-pre1) Anti-Persona (OBRIGATÓRIO — 2-3 perfis)**

A persona define quem você QUER atender. A anti-persona define quem você NÃO QUER atender — clientes que consomem recurso, geram atrito e não convertem. Sem anti-persona definida, a equipe não sabe quando dizer "não".

Para cada anti-persona (2-3):
- **profile_name** (ou **label**): apelido descritivo (ex: "Caçador de preço", "Emergência única")
- **description** (ou **who**): 2-3 linhas sobre o comportamento típico
- **signals** (ou **red_flags**): lista de 3-6 sinais concretos que o time observa na triagem (ex: "pede desconto antes do diagnóstico", "pergunta só preço por WhatsApp sem contexto")
- **why_not**: por que não é cliente ideal (custo de atendimento, ticket baixo, alta rotatividade, objeção que não resolve)
- **operational_rule**: regra prática — como o time identifica e o que faz (ex: "Se pedir desconto antes do diagnóstico, encaminhar para tabela padrão")

> Use **profile_name/description/signals** como padrão. O renderer aceita os alternativos (label/who/red_flags) para compatibilidade, mas prefira o conjunto principal.

Feche com um `operational_rule` geral — a regra-mãe que alinha o time.

**D-pre2) Buyer Journey (OBRIGATÓRIO — 5-6 estágios)**

Mapeie a jornada de decisão da persona do gatilho ao pós-compra. Cada estágio com:
- **Stage:** nome (ex: Gatilho, Pesquisa, Consideração, Decisão, Pós-compra, Recompra)
- **Trigger:** o que inicia esse estágio (evento externo, interno, emocional)
- **Mental state:** estado mental dominante (dúvida, ansiedade, urgência, cobrança social)
- **Primary channel:** onde a persona busca informação neste estágio
- **Dominant question:** a pergunta que ela está tentando responder
- **[Cliente] intervention:** como o cliente intervém nesse estágio (conteúdo, anúncio, contato)
- **Friction today:** qual o atrito/problema atual nesse estágio
- **Duration estimate:** quanto tempo típico (horas, dias, semanas)

Feche com `critical_leakage_point`: onde o cliente mais perde leads HOJE. Pode ser:
- **String livre** (preferido quando o vazamento é qualitativo): ex. `"O maior vazamento é na Consideração: a persona pesquisa 3-7 dias e a clínica não aparece no Google Maps local"`.
- **Objeto estruturado** (use quando tiver número de perda): `{stage, evidence, estimated_loss_pct}`.

**D-pre3) Willingness-to-Pay (OBRIGATÓRIO — por serviço principal)**

Para cada serviço/produto principal (3-5), use o SHAPE PREFERIDO (mais rico que o legado):
- **service**: nome do serviço
- **current_ticket_range**: faixa de ticket atual praticada (ex: `"R$180-250"`)
- **perceived_fair_range**: faixa que a persona percebe como justa (ex: `"R$180-300"`)
- **premium_ceiling**: teto premium aceito COM justificativa (ex: `"R$400 com exame complementar incluso"`)
- **elasticity**: palavra-chave + nuance separada por `—` (ex: `"baixa — aceita pagar mais se entender o porquê"`). O portal usa a palavra-chave como tag colorida e o texto após o travessão como nota.
- **pricing_lever**: o que justifica cobrar mais (especialização, tempo de consulta, garantia, bundle)

> Os campos legados (`current_price`, `fair_range`, `premium_range`) ainda funcionam, mas **prefira** o shape novo — ele comunica range (não ponto) e o teto com justificativa, que é o que a análise realmente pede.

Isso não é exercício de pricing — é alinhar posicionamento e copy ao WTP real da persona.

**D-pre4) Objection Library (OBRIGATÓRIO — 5-7 objeções)**

Catálogo de objeções reais da persona. Para cada:
- **Objection:** como ela diz (linguagem do cliente)
- **Subtext:** o que ela REALMENTE está dizendo (medo, dúvida, experiência anterior)
- **Bad response:** resposta automática que NÃO funciona e por quê
- **Good response:** resposta que funciona — pequena história, dado, reframe
- **When to use:** em que canal/momento essa resposta é usada

Essa library alimenta copy, SDR, scripts de atendimento e FAQs.

**E) 3 Opções de Mensagem-Chave**

1. **Opção funcional:** Foco no resultado prático/tangível
2. **Opção emocional:** Foco no sentimento/transformação
3. **Opção social:** Foco em como o cliente será visto/percebido

Para cada opção:
- A mensagem em si (1 frase, máximo 15 palavras)
- Por que essa abordagem funciona para este ICP
- Em que contexto usar (anúncios, bio Instagram, headline do site, etc.)

### Estrutura visual (obrigatória)

Siga o padrão canônico de `references/padrao-output.md`. Além dos campos acima, SEMPRE inclua:

- **`summary_headline`** (string, max 200 char) — manchete com o veredito do ICP/Persona. Específica, com dados reais.
  - Ex: "Mariana (35-50, tutora de gatos premium) é o ICP. Ignorada pelos concorrentes que tratam cão e gato igual."

- **`summary_highlights`** (4-6 itens) — KPIs visuais. Sugestões para persona-ICP:
  - `posicao`: faixa etária/renda da persona, ticket médio atual vs premium ceiling
  - `competicao`: nº de concorrentes que atendem o mesmo ICP declaradamente
  - `janela`: tempo de decisão médio (buyer journey duration)
  - `oportunidade`: dor mais aguda não endereçada, WTP gap (premium ceiling - current ticket)
  - `risco`: objeção mais comum / leakage point mais crítico
  - Cada item: `{category, label, value, subtext, tone}` (tons: `green|yellow|red|blue|gray`)

- **`summary_key_findings`** (3-5 itens) — achados categorizados:
  - `vantagem | contexto | ameaca | acao`
  - Cubra pelo menos 3 dos 4 tipos.

### Ponto de alavancagem

Em persona-ICP, o ponto de alavancagem é a **combinação {persona principal + dor mais ignorada pelos concorrentes + frase-citação}** — o que o time precisa internalizar para mudar comunicação/atendimento. Estruture como:

```json
"key_insight": {
  "headline": "Frase-manchete (ex: 'Mariana paga R$400 se entender o porquê — e ninguém explica')",
  "context": "2-3 linhas explicando o insight",
  "numbered_reasons": ["(1) razão A", "(2) razão B", "(3) razão C"],
  "discussion_anchor": "Por que este é o ponto para o stakeholder decidir"
}
```

Alternativamente, se o renderer da skill tiver um campo específico de destaque (ex: `critical_leakage_point` com objeto estruturado), use a mesma lógica de quote + razões.

Se a pesquisa do ICP revelou fragilidade (persona mal definida, ICP contraditório com o produto, WTP incompatível), inclua `honesty_alert`.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (se houver)?
- [ ] Cada dor tem > 20 caracteres e usa linguagem do cliente (não jargão)?
- [ ] Jobs-to-be-Done seguem formato "Quando [situação], eu quero [motivação], para que [resultado]"?
- [ ] Nenhum item genérico — se trocar o nome do cliente e ainda servir, refaça?
- [ ] Persona tem frase-citação que soa como fala real (não corporativês)?
- [ ] Canais são específicos (não "redes sociais" nem "Google")?
- [ ] Mensagens-chave têm <= 15 palavras cada?
- [ ] Cada mensagem é diferente das outras (funcional vs emocional vs social)?
- [ ] Anti-persona com 2-3 perfis e `operational_rule` clara para o time?
- [ ] Buyer journey tem 5-6 estágios, cada um com trigger, mental_state, canal, pergunta dominante, intervenção e fricção atual?
- [ ] `critical_leakage_point` identifica onde o cliente mais perde leads hoje COM evidência?
- [ ] Willingness-to-pay cobre os serviços principais com preço atual, faixa justa, faixa premium, elasticidade e pricing_lever?
- [ ] Objection library tem 5-7 objeções com subtext, bad_response e good_response (linguagem real, não corporativês)?
- [ ] Tem `summary_headline` específico (não "persona definida")?
- [ ] `summary_highlights` tem 4-6 itens com categorias e tons válidos?
- [ ] `summary_key_findings` cobre pelo menos 3 dos 4 tipos (vantagem/contexto/ameaça/ação)?
- [ ] Identificou `key_insight` para ancorar conversa com stakeholder?
- [ ] Se há fragilidade, incluiu `honesty_alert`?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador de uma vez.

**DECISÃO 1:** Mensagem-chave — qual direção?
- Opção A: "[mensagem funcional]" — foco no resultado prático
- Opção B: "[mensagem emocional]" — foco no sentimento
- Opção C: "[mensagem social]" — foco na percepção

**RECOMENDAÇÃO:** Opção [X]. [Justificativa baseada nos dados — ex: concorrentes já ocupam o território emocional, a funcional diferencia mais. Explique por que as outras são mais fracas.]

**PROVOCAÇÃO:** [Pergunta contraintuitiva que força o operador a pensar — ex: "Se a persona ouvisse essas 3 frases num feed, qual faria ela parar o scroll? E o cliente tem coragem de bancar essa promessa?"]

**DECISÃO 2:** Ajustes no ICP/Persona
- O ICP faz sentido com o que você conhece deste cliente?
- As dores são dolorosas de verdade? O cliente se reconheceria?
- A persona parece real? Você consegue imaginar conversando com ela?
- Os canais onde encontrá-la fazem sentido?
- Algum canal ou comunidade que você sabe que esse público frequenta?

Aguarde o operador responder. Ele pode:
- Escolher uma mensagem e aprovar tudo
- Pedir ajustes em seções específicas
- Combinar elementos de mais de uma mensagem

Incorpore todos os ajustes e gere a versão final.

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/geral-persona-icp.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "ICP e Persona salvos. Este output será usado por: account-auditoria-comunicacao, geral-pesquisa-mercado, geral-posicionamento-estrategico, e todas as skills de produção."
   - Sugira a próxima skill da semana 1 (ex: gt-diagnostico-maturidade-digital ou account-auditoria-comunicacao)
