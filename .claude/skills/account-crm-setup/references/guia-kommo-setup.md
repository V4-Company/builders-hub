# Guia de Setup Kommo CRM — Pipeline + Automações para PMEs

Referência técnica para configurar o Kommo CRM como padrão V4 Company. Cobre pipeline, campos customizados, Salesbot e integrações.

---

## 1. Visão Geral do Kommo

O Kommo (ex-amoCRM) é o CRM padrão da V4 Company para clientes PME. Pontos fortes:
- Integração nativa com WhatsApp Business
- Salesbot visual (automação sem código)
- Pipeline visual estilo Kanban
- Integração com Meta Lead Ads e Google Ads

### Acesso e contas
- URL: https://www.kommo.com
- Plano recomendado: Avançado (Salesbot ilimitados)
- 1 conta por cliente, gerenciada pelo consultor V4
- WhatsApp Business conectado via integração oficial

---

## 2. Configuração do Pipeline

### Pipeline padrão V4 (adaptar por cliente)

```
Lead Novo → Em Qualificação → Qualificado → Proposta Enviada → Em Negociação → Fechado-Ganho
                                                                                → Fechado-Perdido
```

### Variações comuns por segmento

**Serviços (clínica, escritório, consultoria):**
```
Agendamento Solicitado → Consulta Marcada → Proposta Apresentada → Em Decisão → Fechado
```

**E-commerce com vendedor (high-ticket):**
```
Lead → Contato Inicial → Demonstração → Proposta → Negociação → Venda
```

**Restaurante/Delivery:**
```
Contato → Primeiro Pedido → Cliente Recorrente → VIP
```

### Como criar no Kommo

1. Acesse **Leads** no menu lateral
2. Clique no ícone de engrenagem do pipeline
3. Renomeie as etapas existentes clicando no nome
4. Para adicionar etapa: clique em "+" entre etapas
5. Para remover: arraste a etapa para a lixeira
6. **Importante:** Configure "Fechado-Perdido" com campo obrigatório de motivo

---

## 3. Campos Customizados

### Campos obrigatórios para todos os clientes

| Campo | Tipo | Opções | Onde |
|-------|------|--------|------|
| Origem | Lista | Meta Ads, Google Ads, Indicação, Orgânico, Site, WhatsApp, Outro | Lead |
| Score SDR | Lista | 1★, 2★, 3★, 4★, 5★ | Lead |
| Produto de interesse | Lista | [do briefing] | Lead |
| Temperatura | Lista | Frio, Morno, Quente | Lead |
| Motivo de perda | Texto | — | Lead (obrigatório em Fechado-Perdido) |

### Como criar campos customizados

1. Acesse **Configurações** > **Campos**
2. Clique em **Criar campo**
3. Selecione tipo (lista, texto, número, etc.)
4. Preencha as opções
5. Marque "Obrigatório" se necessário (ex: Motivo de perda)

### Critérios de Score SDR

| Score | Critério | Ação recomendada |
|-------|----------|------------------|
| 1★ | Curiosidade passiva, sem urgência, budget baixo | Régua de nutrição |
| 2★ | Interesse demonstrado, mas sem urgência clara | Régua de nutrição |
| 3★ | Tem o problema, budget indefinido, prazo indefinido | Follow-up manual em 7 dias |
| 4★ | Tem problema + budget + prazo definido | Contato imediato do vendedor |
| 5★ | Pronto para comprar, budget confirmado, urgência alta | Prioridade máxima, atender em minutos |

---

## 4. Salesbot — Régua de Boas-Vindas

### Anatomia do Salesbot

```
TRIGGER (quando dispara)
  └── CONDIÇÃO (se X, então)
       └── AÇÃO (enviar mensagem, mover lead, etc.)
            └── WAIT (esperar X tempo)
                 └── CONDIÇÃO (verificar resposta)
                      └── AÇÃO (próximo passo)
```

### Configuração passo a passo

**1. Criar novo Salesbot:**
- Acesse **Salesbot** no menu lateral
- Clique **Criar novo bot**
- Nomeie: "Boas-Vindas - [Nome do Cliente]"

**2. Configurar trigger:**
- Tipo: "Quando um novo lead é criado"
- Condição adicional: Origem = Meta Ads OU Google Ads OU Site
- (Isso evita disparar para leads de indicação/orgânico que já estão em contato)

**3. Fluxo do Salesbot:**

```
[Trigger: Novo lead criado]
  │
  ├── [Enviar Mensagem 1 via WhatsApp]
  │     "Olá {nome}! Recebi seu interesse em [produto].
  │      Sou [nome], consultor(a) da [empresa].
  │      Em até 2h vou te enviar mais detalhes. 😊"
  │
  ├── [Wait: 24 horas]
  │
  ├── [Condição: Lead respondeu?]
  │     ├── SIM → [Mover para "Em Qualificação"] → [Notificar vendedor]
  │     └── NÃO → [Enviar Mensagem 2]
  │                  "Oi {nome}! Passando pra compartilhar algo
  │                   que pode te ajudar: [conteúdo de valor].
  │                   Quer que eu explique como funciona?"
  │
  ├── [Wait: 48 horas]
  │
  ├── [Condição: Lead respondeu?]
  │     ├── SIM → [Mover para "Em Qualificação"]
  │     └── NÃO → [Enviar Mensagem 3]
  │                  "Oi {nome}, última mensagem!
  │                   Se [resultado] é algo que te interessa,
  │                   é só responder aqui. Se não for o momento,
  │                   sem problema — fico por aqui se precisar. 👋"
  │
  └── [Após Mensagem 3: Mover para "Lead Frio"] → [Entrar na régua de nutrição]
```

**4. Variáveis disponíveis no Salesbot:**
- `{nome}` — nome do lead
- `{empresa}` — empresa do lead (se preenchido)
- `{email}` — email do lead
- `{telefone}` — telefone do lead
- Campos customizados via `{campo_customizado}`

---

## 5. Salesbot — Régua de Nutrição

### Trigger
- Lead com score 1-3★
- Parado na mesma etapa há 7+ dias
- Não respondeu régua de boas-vindas

### Fluxo

```
[Trigger: Lead frio parado 7+ dias]
  │
  ├── [Semana 1: Conteúdo de Valor]
  │     WhatsApp: dica prática, dado de mercado
  │     Email: mini-guia ou artigo
  │
  ├── [Wait: 7 dias]
  │
  ├── [Semana 2: Caso de Sucesso]
  │     WhatsApp: história curta de resultado
  │     Email: case study resumido
  │
  ├── [Wait: 7 dias]
  │
  ├── [Semana 3: Diferencial]
  │     WhatsApp: o que diferencia o produto/serviço
  │
  ├── [Wait: 7 dias]
  │
  ├── [Semana 4: Oferta/CTA]
  │     WhatsApp: oferta direta ou convite
  │     Email: oferta com CTA claro
  │
  └── [Condição: Respondeu em algum momento?]
        ├── SIM → [Mover para "Em Qualificação"]
        └── NÃO → [Mover para "Descartado"] + [Tag: "Nutrição concluída sem resposta"]
```

---

## 6. Integrações Essenciais

### WhatsApp Business

1. Acesse **Integrações** > procure "WhatsApp"
2. Existem 2 opções:
   - **WhatsApp Business API** (via provedor como Gupshup, 360dialog): melhor para volume alto, custa mensalidade
   - **WhatsApp Web** (via extensão): gratuito, funciona para volume baixo
3. Para maioria dos clientes PME: WhatsApp Web é suficiente no início
4. Configure para que mensagens recebidas criem leads automaticamente

### Meta Lead Ads

1. Acesse **Integrações** > procure "Facebook"
2. Conecte a conta de anúncios do cliente
3. Mapeie os campos do formulário de lead para os campos do Kommo:
   - Nome → Nome do lead
   - Email → Email
   - Telefone → Telefone
   - Campo customizado → Tag de produto de interesse
4. Configure para criar lead automaticamente na etapa "Lead Novo"
5. Tag automática: "Origem: Meta Ads"

### Google Ads

1. Use integração via Make/Zapier (não há integração nativa direta)
2. Trigger: Google Ads Lead Form submission
3. Ação: Criar lead no Kommo
4. Mapeamento de campos similar ao Meta

---

## 7. Boas Práticas para Mensagens de WhatsApp

### Formatação Kommo WhatsApp
- **Negrito:** `*texto*`
- **Itálico:** `_texto_`
- **Riscado:** `~texto~`
- **Monoespaçado:** `` ```texto``` ``
- **Links:** Cole direto (WhatsApp gera preview)
- **Emojis:** Funcionam normalmente

### Regras de mensagem
- Máximo 3 frases por mensagem (WhatsApp não é email)
- Sempre personalize com nome: `{nome}`
- Horário de envio: 9h-18h dias úteis (respeitar horário comercial)
- Não enviar mais de 1 mensagem por dia (exceto se o lead responder)
- Linguagem coloquial-profissional (WhatsApp é informal)
- CTA claro em cada mensagem (o que a pessoa deve fazer)

### Templates que funcionam

**Boas-vindas:**
```
Oi {nome}! 😊

Recebi seu contato sobre [produto/serviço]. Que bom que nos procurou!

Nos próximos minutos, [vendedor] vai entrar em contato pra entender melhor o que você precisa. Até já!
```

**Follow-up leve:**
```
Oi {nome}! Passando pra compartilhar algo rápido:

[Dica/dado relevante em 1-2 frases]

Se quiser saber como aplicar isso no seu [negócio/caso], é só responder aqui. 👇
```

**Última tentativa:**
```
Oi {nome}! Última mensagem, prometo 😄

Se [resultado/benefício] é algo que te interessa, me responde "quero" que eu explico como funciona.

Se não for o momento, sem problema — fico por aqui se precisar!
```

---

## 8. Checklist de Configuração Completa

- [ ] Pipeline criado com etapas personalizadas
- [ ] Fechado-Perdido com motivo obrigatório
- [ ] Campos customizados criados (Origem, Score, Produto, Temperatura)
- [ ] WhatsApp conectado e testado
- [ ] Salesbot de boas-vindas configurado e ativo
- [ ] Salesbot de nutrição configurado e ativo
- [ ] Integração Meta Lead Ads (se usar Meta)
- [ ] Integração Google Ads via Make/Zapier (se usar Google)
- [ ] Teste completo com lead fictício
- [ ] Vendedor treinado no uso do pipeline
