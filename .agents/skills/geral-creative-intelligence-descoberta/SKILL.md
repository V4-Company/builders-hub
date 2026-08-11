---
name: geral-creative-intelligence-descoberta
description: Define briefing, escopo, universo competitivo, fontes, critérios e plano de pesquisa para uma entrega Creative Intelligence. Use sempre no início de benchmark criativo, análise de concorrentes, sala de inteligência ou quando uma lista de players precisa ser validada antes da coleta.
area: geral
author: fabiojoseaiello-alt
version: 1.0.0
---

# Creative Intelligence — Descoberta

Transforme uma intenção ampla em um escopo pesquisável. Esta etapa evita comparar marcas erradas, misturar mercados ou coletar dados que não ajudam uma decisão.

## Entradas

Procure primeiro no contexto disponível:

- objetivo comercial e pergunta estratégica;
- documentos do cliente, onboarding e pesquisas anteriores;
- marca, oferta, segmentos, região e canais;
- concorrentes citados e origem de cada citação;
- acessos e fontes autorizadas;
- prazo, formato de entrega e audiência.

Pergunte apenas pelo que não puder ser descoberto e que mudaria materialmente a pesquisa. Registre premissas para lacunas não bloqueantes.

## Processo

### 1. Formular a decisão

Escreva a frase: “Ao final, esta entrega permitirá decidir…”. Uma entrega pode apoiar posicionamento, repertório criativo, distribuição de formatos, arquitetura de testes ou plano de produção; não presuma que todos são igualmente prioritários.

### 2. Delimitar o recorte

Registre:

- país, estado ou cidade;
- categoria e subcategoria;
- B2B, B2C ou ambos;
- canais e status dos anúncios;
- janela ou data do snapshot;
- frentes comerciais e públicos;
- fontes internas que permanecerão separadas das públicas.

### 3. Construir o registro competitivo

Classifique cada player:

- `baseline`: cliente em foco;
- `priority`: concorrente confirmado pelo cliente ou evidência forte;
- `expanded`: referência adicionada para cobrir um território relevante;
- `watchlist`: player importante sem evidência suficiente no snapshot;
- `excluded`: homônimo, fornecedor, mercado incompatível ou referência descartada.

Para cada player, mantenha nome, slug, aliases, URLs oficiais, papel, origem da indicação, razão de inclusão e status de validação.

### 4. Definir critérios

Especifique antes da coleta:

- como validar páginas oficiais;
- o que conta como anúncio da marca;
- regras de deduplicação;
- taxonomia inicial de frentes, formatos, mensagens e hooks;
- limiares de ciclo, quando aplicáveis;
- métricas que a fonte não oferece.

### 5. Planejar a coleta

Escolha a fonte mais direta disponível. Para cada fonte, registre método principal, fallback, credencial necessária, possível custo, limite e formato bruto esperado.

## Saídas obrigatórias

Crie em `01-descoberta/`:

- `briefing.md`: decisão, contexto, escopo, critérios, limitações iniciais e formato da entrega;
- `scope.json`: configuração legível por máquina;
- `concorrentes.csv`: registro competitivo;
- `source-plan.md`: fonte, método, fallback, risco e saída esperada;
- `handoff.json`: resumo para a coleta.

## Gate de saída

Conclua apenas quando:

- o cliente em foco está identificado;
- o objetivo virou decisão concreta;
- os papéis competitivos estão separados;
- aliases e URLs oficiais foram registrados ou marcados como pendentes;
- critérios de inclusão e exclusão são auditáveis;
- período, região, canais e limitações estão explícitos.

## Exemplo

**Entrada:** “Quero entender como os concorrentes de uma rede de clínicas estão anunciando.”

**Saída esperada:** escopo que separa clínicas locais, redes nacionais e referências aspiracionais; define cidade, especialidades, Meta Ad Library, data do snapshot e quais decisões criativas o benchmark deverá apoiar.
