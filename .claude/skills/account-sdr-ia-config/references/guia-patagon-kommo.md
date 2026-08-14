# Guia de Configuracao: Patagon AI + Kommo CRM

Guia tecnico passo a passo para configurar um agente SDR IA no Patagon com integracao ao Kommo CRM. Escrito para operadores que podem nao ter experiencia tecnica profunda.

---

## Visao Geral da Arquitetura

```
Lead envia mensagem no WhatsApp
        |
        v
  [Patagon AI Agent]
  - Recebe mensagem
  - Executa fluxo de qualificacao
  - Atribui score 1-5 estrelas
  - Trata objecoes
  - Envia follow-ups
        |
        v
  [Integracao Patagon → Kommo]
  - Cria contato no Kommo
  - Preenche campos mapeados
  - Aplica tags automaticas
  - Move para etapa correta do pipeline
        |
        v
  [Alerta para Vendedor]
  - Se score >= 4: WhatsApp para vendedor
  - Se score < 4: regua automatica
```

---

## Parte 1: Patagon AI — Configuracao do Agente

### 1.1 Acesso e Criacao

1. Acesse [app.patagon.ai](https://app.patagon.ai)
2. Faca login com a conta do operador
3. No dashboard, clique em **"+ Novo Agente"**
4. Preencha:
   - **Nome do agente:** Nome humano (ex: "Ana da Empresa X"). Esse nome aparece para o lead.
   - **Descricao:** Texto interno para identificacao (ex: "SDR IA - Qualificacao WhatsApp")
   - **Canal:** WhatsApp Business
   - **Numero:** Selecione o numero do cliente (deve estar previamente conectado)

### 1.2 Conectar WhatsApp Business

**Pre-requisito:** O cliente precisa ter um numero de WhatsApp Business. Numero pessoal NAO funciona.

1. No Patagon: **Settings → Channels → WhatsApp**
2. Clique em **"Conectar WhatsApp"**
3. Escaneie o QR code com o WhatsApp Business do cliente
4. Aguarde a confirmacao de conexao (pode levar ate 2 minutos)
5. Teste enviando uma mensagem do seu celular para o numero conectado
6. Se o Patagon mostrar a mensagem recebida, a conexao esta OK

**Problemas comuns:**
- QR code expirado: atualize a pagina e escaneie novamente
- Numero ja conectado em outro servico: desconecte primeiro
- WhatsApp Business API vs App: ambos funcionam, mas API tem mais recursos

### 1.3 Configurar Personalidade do Agente

No Patagon, va em **Agent Settings → Personality/Instructions**.

O campo de instrucoes e onde voce define COMO o agente se comporta. Cole o texto gerado pela skill copy-scripts-sdr, adaptado para o formato do Patagon.

**Estrutura recomendada das instrucoes:**

```
IDENTIDADE:
Voce e [NOME_AGENTE], [funcao] da [EMPRESA].
Seu trabalho e atender pessoas que entram em contato pelo WhatsApp.

PERSONALIDADE:
[Descricao do tom de voz baseada no designer-manual-marca]
- Ex: "Voce e amigavel, direta e profissional. Usa linguagem simples."
- Ex: "Voce nao usa gíria, mas tambem nao e formal demais."

REGRAS ABSOLUTAS:
1. Maximo 3 frases por mensagem
2. Use o nome da pessoa sempre que possivel
3. Nunca prometa preco, prazo ou condicao especifica
4. Se nao souber responder, passe para [NOME_VENDEDOR]
5. Nunca revele que e uma inteligencia artificial
6. Nunca use mais de 1 emoji por mensagem
7. Responda sempre em portugues brasileiro

CONHECIMENTO DO PRODUTO:
[Resumo do produto/servico]
[Principais beneficios]
[O que NAO pode prometer]

PROCESSO:
1. Cumprimente e se apresente
2. Faca as perguntas de qualificacao (uma por vez)
3. Classifique o lead
4. Se qualificado: encaminhe para vendedor
5. Se nao qualificado: ofereça conteudo e nutra
```

### 1.4 Configurar Fluxo de Qualificacao

No Patagon: **Agent Settings → Conversation Flow**

Aqui voce define as perguntas que o agente faz em sequencia:

1. **Adicione cada pergunta** como um "step" no fluxo
2. Para cada pergunta, configure:
   - **Texto da pergunta:** A pergunta exata
   - **Tipo:** "Aberta" (o lead responde livremente)
   - **Obrigatoria:** Sim (o agente deve obter resposta antes de avancar)
   - **Regras de score:** Como a resposta influencia a classificacao
3. **Ordene** as perguntas na sequencia definida pela skill copy-scripts-sdr
4. **Configure transicoes:** O que o agente diz entre uma pergunta e outra

**Dica:** Nao use perguntas de multipla escolha no WhatsApp. Perguntas abertas soam mais naturais. O agente de IA interpreta a resposta.

### 1.5 Configurar Regras de Scoring

No Patagon: **Agent Settings → Scoring Rules**

Configure os criterios de cada faixa de score:

| Score | Criterios | Acao automatica |
|-------|-----------|-----------------|
| 5 estrelas | Todos os sinais positivos presentes | Alerta imediato + Kommo "Qualificados" |
| 4 estrelas | Maioria dos sinais positivos | Alerta + Kommo "Qualificados" |
| 3 estrelas | Sinais mistos | Kommo "Nutricao" + regua |
| 2 estrelas | Poucos sinais positivos | Kommo "Frios" + tag |
| 1 estrela | Sinais de desqualificacao | Kommo "Frios" + despedida |

**Como o Patagon calcula o score:**
O Patagon usa IA para interpretar as respostas do lead e classificar conforme os criterios que voce definiu. Quanto mais especificos os criterios, mais precisa a classificacao.

**Exemplo de criterio bem escrito:**
"Lead 5 estrelas: demonstra necessidade urgente (prazo definido), e o decisor ou tem autonomia, orcamento compativel com ticket medio, e ja pesquisou alternativas."

**Exemplo de criterio mal escrito:**
"Lead bom." (vago demais, o agente nao sabe como classificar)

### 1.6 Configurar Respostas para Objecoes

No Patagon: **Agent Settings → Objection Handling**

Para cada objecao, adicione:
1. **Trigger:** A objecao como o lead a expressa (pode ter variações)
2. **Resposta:** O script do SDR IA para essa objecao
3. **Se insistir:** Segunda resposta ou escalamento

**Dica:** Adicione variações da mesma objecao. Ex: "ta caro", "achei caro", "nao tenho dinheiro pra isso", "meu orcamento e menor" podem ser agrupadas como objecao de preco.

### 1.7 Configurar Follow-ups

No Patagon: **Agent Settings → Follow-ups**

1. **Ative follow-ups automaticos**
2. Configure cada intervalo:
   - Apos 1 hora sem resposta: [mensagem]
   - Apos 24 horas sem resposta: [mensagem]
   - Apos 3 dias sem resposta: [mensagem — ultimo]
3. **Max follow-ups:** 3 (nao mais que isso)
4. **Horario permitido:** Definir janela de horario comercial

### 1.8 Configurar Handoff para Humano

No Patagon: **Agent Settings → Human Handoff**

1. **Mensagem de transicao:** A mensagem que o agente envia ao lead antes de transferir
2. **Destinatario:** Nome e WhatsApp do vendedor
3. **Triggers de handoff:**
   - Score 4-5 estrelas (apos qualificacao)
   - Lead pede para falar com humano
   - Agente nao consegue responder (2 tentativas)
   - Lead demonstra frustacao
4. **Contexto enviado ao vendedor:** Resumo da conversa, score, dados coletados

---

## Parte 2: Kommo CRM — Integracao

### 2.1 Obter API Key do Kommo

1. No Kommo: **Settings → Integrations**
2. Clique em **"API"**
3. Se nao houver chave, clique em **"Generate API Key"**
4. Copie a chave (ela sera usada no Patagon)
5. **IMPORTANTE:** Guarde a chave em local seguro. Nao compartilhe.

### 2.2 Conectar no Patagon

1. No Patagon: **Settings → Integrations → Kommo**
2. Clique em **"Conectar"**
3. Cole a API key do Kommo
4. Clique em **"Testar Conexao"**
5. Se mostrar "Conexao bem sucedida", avance
6. Se der erro, verifique: a chave esta correta? O Kommo esta ativo?

### 2.3 Field Mapping (Mapeamento de Campos)

Apos conectar, configure o mapeamento:

**Campos padrao (ja existem no Kommo):**

| Campo Patagon | Campo Kommo | Notas |
|---------------|-------------|-------|
| Nome do lead | Nome | Campo padrao, obrigatorio |
| Telefone | Telefone | Campo padrao |
| Email | Email | Se coletado |

**Campos personalizados (criar no Kommo primeiro):**

Para criar campos personalizados no Kommo:
1. Va em **Settings → Fields**
2. Clique em **"Add Field"**
3. Preencha nome e tipo
4. Salve

Campos personalizados recomendados:

| Nome do campo | Tipo | Descricao |
|---------------|------|-----------|
| Score | Tag | Score 1-5 estrelas |
| Produto Interesse | Texto | Produto que o lead demonstrou interesse |
| Origem (UTM Source) | Texto | De onde o lead veio |
| Midia (UTM Medium) | Texto | Canal de midia |
| Campanha (UTM Campaign) | Texto | Nome da campanha |
| Resumo SDR | Texto longo | Resumo da qualificacao pelo SDR IA |

**Campo de notas:**

O historico da conversa completa deve ser salvo como nota no contato:
1. No mapeamento, selecione "Historico da conversa"
2. Mapeie para "Nota automatica" no Kommo
3. Isso cria uma nota no contato com toda a conversa

### 2.4 Configurar Pipeline de Destino

No mapeamento, defina para qual etapa do pipeline cada score vai:

1. **Score 4-5 estrelas:** Etapa "Qualificados" (ou equivalente)
2. **Score 3 estrelas:** Etapa "Nutricao" (ou equivalente)
3. **Score 1-2 estrelas:** Etapa "Frios" (ou equivalente)

**NOTA:** As etapas do pipeline devem existir no Kommo. Se nao existirem, crie antes:
1. No Kommo: **Pipeline → Edit Pipeline**
2. Adicione as etapas necessarias
3. Salve

### 2.5 Configurar Tags Automaticas

No Patagon, na secao de integracao Kommo:

1. **Tags por score:**
   - 5 estrelas: "Lead Quente", "5 estrelas"
   - 4 estrelas: "Lead Qualificado", "4 estrelas"
   - 3 estrelas: "Lead Morno", "Nutricao"
   - 1-2 estrelas: "Lead Frio"

2. **Tags por origem (UTM):**
   Configure regras baseadas no UTM source:
   - Se `utm_source` contem "google" → tag "Google Ads"
   - Se `utm_source` contem "meta" ou "facebook" → tag "Meta Ads"
   - Se `utm_source` contem "instagram" → tag "Instagram Organico"
   - Se `utm_source` contem "indicacao" → tag "Indicacao"

---

## Parte 3: Alertas para Vendedor

### 3.1 Configurar no Patagon

No Patagon: **Settings → Alerts**

1. Clique em **"New Alert"**
2. **Condicao de disparo:**
   - Tipo: "Lead qualificado"
   - Score minimo: 4 estrelas
   - Momento: apos qualificacao concluida
3. **Canal:** WhatsApp
4. **Destinatario:** Numero do vendedor
5. **Template:** Use o template definido na skill

### 3.2 Template do Alerta

O alerta deve conter tudo que o vendedor precisa para agir rapidamente:

```
LEAD QUALIFICADO: [Nome do lead]
Score: [X] estrelas
Interesse: [Produto que demonstrou interesse]
Resumo: [2 frases sobre o que o lead precisa]
Ver no Kommo: [link direto para o contato]
SLA: responder em [X] minutos
```

### 3.3 Escalamento

Configure o que acontece se o vendedor nao responder:

1. **Timer 1:** Apos [SLA] minutos sem resposta do vendedor
   - Acao: enviar alerta para backup
   - Tag no Kommo: "SLA Violado"

2. **Timer 2:** Apos [SLA x 2] minutos sem resposta de ninguem
   - Acao: enviar mensagem automatica ao lead (desculpando a demora)
   - Tag no Kommo: "Atendimento Atrasado"

---

## Parte 4: Testes

### 4.1 Checklist Pre-Teste

Antes de testar, verifique:

- [ ] Agente criado no Patagon com todas as configuracoes
- [ ] WhatsApp Business conectado
- [ ] Instrucoes de personalidade preenchidas
- [ ] Perguntas de qualificacao configuradas
- [ ] Regras de scoring definidas
- [ ] Respostas de objecoes adicionadas
- [ ] Follow-ups configurados
- [ ] Handoff configurado
- [ ] Integracao Kommo ativa e testada
- [ ] Field mapping completo
- [ ] Tags automaticas configuradas
- [ ] Alertas configurados
- [ ] Vendedor informado sobre os testes

### 4.2 Protocolo de Teste

Para cada lead simulado:

1. **Envie a mensagem inicial** de um numero diferente
2. **Aguarde a resposta** do agente (deve ser < 5 segundos)
3. **Siga o roteiro** do perfil de teste (quente, morno, frio, etc.)
4. **Responda as perguntas** conforme o perfil
5. **Verifique no Patagon:** score atribuido
6. **Verifique no Kommo:** contato criado, campos preenchidos, tag aplicada, etapa correta
7. **Verifique no WhatsApp do vendedor:** alerta recebido (se aplicavel)
8. **Registre o resultado**

### 4.3 O que verificar em cada teste

| Item | Como verificar | Criterio de sucesso |
|------|---------------|---------------------|
| Tempo de resposta | Cronometrar | < 5 segundos |
| Mensagem de boas-vindas | Ler a mensagem | Igual ao configurado |
| Perguntas na ordem | Acompanhar a conversa | Sequencia correta |
| Tom de voz | Avaliar linguagem | Consistente com designer-manual-marca |
| Score | Verificar no Patagon | Corresponde ao perfil |
| Kommo — contato | Verificar no CRM | Contato criado |
| Kommo — campos | Verificar campos | Todos preenchidos |
| Kommo — tag | Verificar tags | Tag correta aplicada |
| Kommo — etapa | Verificar pipeline | Etapa correta |
| Alerta | Verificar WhatsApp vendedor | Recebido (se 4-5 estrelas) |

### 4.4 Problemas Comuns e Solucoes

| Problema | Causa provavel | Solucao |
|----------|---------------|---------|
| Agente nao responde | WhatsApp desconectado | Reconectar no Patagon |
| Score incorreto | Criterios vagos | Reescrever criterios com mais especificidade |
| Lead nao aparece no Kommo | API key invalida | Gerar nova key no Kommo |
| Campos vazios no Kommo | Mapeamento incompleto | Revisar field mapping |
| Tag errada | Regra de tag incorreta | Corrigir condicoes de tag |
| Alerta nao chega | Numero errado ou fora do horario | Verificar numero e horario |
| Tom robotico | Instrucoes muito rigidas | Flexibilizar instrucoes, adicionar exemplos |
| Agente revela que e IA | Instrucoes incompletas | Adicionar regra explicita de nao revelar |
| Follow-up de madrugada | Horario comercial nao configurado | Definir janela de horario |

---

## Parte 5: Pos Go-Live

### 5.1 Primeiras 48 horas

Monitore de perto:
- Quantos leads entraram?
- Scores atribuidos estao fazendo sentido?
- Vendedor esta recebendo alertas e respondendo no SLA?
- Algum lead reclamou ou demonstrou estranheza?
- Tom de voz esta consistente?

### 5.2 Primeira semana

Colete metricas:
- Leads qualificados vs total: X%
- SLA cumprido: X%
- Leads que pediram humano: X%
- Objecoes mais frequentes (novas que nao estavam mapeadas?)
- Feedback do vendedor sobre qualidade dos leads

### 5.3 Ajustes comuns apos go-live

1. **Criterios de scoring muito frouxos:** Muitos leads 4-5 estrelas que nao sao bons → apertar criterios
2. **Criterios muito rígidos:** Poucos leads qualificados, vendedor ocioso → afrouxar
3. **Nova objecao apareceu:** Adicionar no Patagon
4. **Tom nao esta bom:** Ajustar instrucoes de personalidade
5. **Follow-up nao funciona:** Testar diferentes abordagens
