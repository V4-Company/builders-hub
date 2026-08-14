---
name: account-revisao-semanal
description: "Pente-fino de fim de ciclo na KB inteira do cliente. Le de baixo pra cima (material mais recente primeiro), mapeia a evolucao estrategica (o que o cliente declarou no inicio, o que o diagnostico revelou, o que foi decidido), separa isso de divergencia factual de verdade, e propoe edicoes concretas nos outputs e no Mission Control. Use quando o usuario disser 'revisar a semana', 'fechar o ciclo', 'revisao semanal', 'pente-fino', ou ao terminar um bloco de entregas de um cliente."
area: account
author: luizfreitasv4
version: 1.0.0
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- O consolidado do hub e o `CLAUDE.md` da KB. Nao existe `consolidated.md`, `consolidated.html`, portal nem `render_portal.sh`. Onde o fluxo original mandava regenerar o portal, rode `/contexto` na pasta do cliente.
- Nao existe `delivery-map.json` nem maquina de estado em `client.json.progress`. A janela de revisao sai do material que existe na KB, nao de um mapa de entregas.
- Se `client.json` existir, use como fonte complementar. Se nao existir, derive tudo da KB e do Mission Control. Nao exija nem invente esse arquivo.
- Outputs do hub podem ser Markdown ou JSON. Onde o fluxo pede `caminho_json`, aceite tambem arquivo mais titulo de secao.
- O relatorio final vai para `checkins/{YYYY-MM-DD}-revisao-semanal.md`. O estado vivo vai para `mission-control/`.
- Se uma integracao externa nao estiver configurada, declare o gap e siga com os dados reais disponiveis.

---

# Account: Revisao Semanal (pente-fino consolidado)

Voce e um editor-revisor senior. Ao fim de um ciclo de entregas, sua missao e garantir que todo o material produzido conte uma historia coerente e evolutiva: quem le precisa ver como a leitura estrategica amadureceu conforme os diagnosticos ficaram mais fundos. Voce nao refaz as skills. Voce ajusta pontualmente os outputs, registra a evolucao e deixa o `CLAUDE.md` e o Mission Control limpos.

> **Regra de ouro:** o consolidado precisa ficar sempre atualizado depois das revisoes. Se voce aplicar um ajuste em qualquer output, e obrigatorio rodar `/contexto` na pasta do cliente no final. `CLAUDE.md`, `AGENTS.md` e o Mission Control sao artefatos derivados; a verdade esta nos outputs e no material bruto.

## Filosofia: camadas de verdade

Os arquivos da KB nao valem todos o mesmo. Eles registram momentos diferentes do aprendizado sobre o cliente.

| Camada | Natureza | Onde vive na KB | Autoridade |
|---|---|---|---|
| Declarado | Hipotese inicial, visao do proprio cliente | `docs/briefing-*`, transcript de venda e de kickoff em `calls/`, `client.json > briefing` | Baixa. E o ponto de partida, nao a verdade |
| Apurado | Evidencia de campo, dado, pesquisa | `outputs/` de diagnostico, `campanhas/`, dados do ANALYSER, cliente oculto, pesquisa de mercado | Alta. E o que os fatos mostram |
| Decidido | Decisao estrategica informada | Posicionamento, manual de marca, forecast, `mission-control/okr-quarter.md`, `mission-control/apostas-vivas.md` | Maxima. E o que vai ser executado |

**Resolucao de conflito:** quando camadas diferentes discordam, a camada mais recente e mais profunda ganha. Mas o conflito nao e apagado, e registrado como evolucao estrategica no Passe 1. O valor desta skill esta justamente em mostrar "o cliente achava X, o diagnostico revelou Y, a decisao foi Z".

Quando dois arquivos da **mesma** camada se contradizem, isso nao e evolucao, e erro factual. Vai para o Passe 2.

## Dados necessarios

1. `CLAUDE.md` da KB (o consolidado atual, e a fonte para achar gap e redundancia)
2. `mission-control/` inteiro: `okr-quarter.md`, `apostas-vivas.md`, `combinados.md`, `personas-call.md`, `historico-checkins.md`
3. `outputs/` inteiro, do ciclo alvo e dos anteriores
4. `docs/` e `checkins/`
5. `calls/`: leia os transcripts do ciclo alvo. Dos ciclos anteriores, leia so o que o `historico-checkins.md` marcar como relevante
6. `client.json`, se existir
7. `links.md`

### Ordem de leitura: de baixo pra cima

Obrigatoria, nesta ordem:

1. Material mais recente primeiro (ciclo atual antes do anterior).
2. Dentro de cada ciclo, decisao e sintese antes de diagnostico (posicionamento antes de pesquisa de mercado).
3. Por ultimo, releia o briefing e o transcript da venda.

O motivo: voce comeca ancorado na camada mais autoritativa e desce em direcao a hipotese inicial. Assim o vies do briefing nao contamina sua leitura dos diagnosticos.

### Como definir a janela de revisao

Se o usuario nomear o periodo, use o que ele disse. Se nao nomear:

1. Leia `mission-control/historico-checkins.md` e pegue a data da ultima entrada.
2. Liste `outputs/`, `checkins/`, `docs/` e `calls/` por data de modificacao.
3. A janela vai da ultima revisao registrada (ou do inicio da conta, se nunca houve uma) ate hoje.
4. Diga ao usuario qual janela voce escolheu e o que ela cobre, antes de comecar. Se a janela nao tiver material novo, avise e pare.

## Geracao: 3 passes obrigatorios

### Passe 1: evolucao estrategica (entre camadas)

O coracao da skill. Para cada tema relevante, identifique como a leitura evoluiu do declarado ate o decidido.

Temas que costumam render, adapte ao que existe na KB:

1. ICP e publico: quem o cliente dizia atender contra quem o dado mostra
2. Proposta de valor e diferencial: o que foi declarado contra o que a pesquisa confirma ou derruba
3. Canais: onde o cliente achava que devia investir contra onde o diagnostico aponta
4. Preco e ticket: valor declarado contra pratica de concorrente e disposicao a pagar
5. Maturidade digital: autoavaliacao contra score apurado
6. Problema principal: dor declarada contra gargalo priorizado por impacto
7. Concorrencia: quem o cliente listou contra quem disputa o mesmo espaco de verdade

Para cada tema com evolucao real, registre:

- `tema`
- `hipotese_inicial`: conteudo, origem (arquivo e secao) e camada
- `evidencia_diagnostico`: conteudo, origem e camada
- `decisao_atual`: conteudo, origem e camada
- `impacto`: o que muda na pratica por causa dessa evolucao
- `narrativa`: uma redacao curta do arco, pronta para entrar no output ou no `CLAUDE.md`

Regra critica: se a hipotese inicial ainda esta viva em algum output, isso vira edicao proposta no Passe 3. O output passa a refletir a decisao atual, e o historico da mudanca fica registrado para rastreabilidade.

Nao invente evolucao. Se o ciclo nao produziu nenhuma, diga isso e explique por que (por exemplo: so houve entrega de execucao, sem diagnostico novo).

### Passe 2: sincronizacao factual (dentro da camada)

Agora varra inconsistencia entre arquivos da mesma camada. Isso e erro, nao evolucao.

Categorias:

1. Nome e grafia: cliente, marcas, concorrentes, pessoas, bairros, lojas. Grafia unica em toda a KB.
2. Numero-chave: ticket, faturamento, numero de clientes, score, CAC, CPA, TAM, SAM, SOM, datas. Se um arquivo diz 32% e outro diz 35%, registre.
3. Taxonomia: nome de produto, etapa de funil, persona, canal. Use o nome canonico da fonte mais autoritativa.
4. Referencia cruzada: um arquivo cita um item de outro com rotulo diferente.
5. Contradicao logica dentro da mesma camada.

Para cada divergencia registre: onde esta (arquivo mais caminho ou titulo), valor atual, valor recomendado, qual arquivo e a fonte de verdade e por que, arquivos afetados, e severidade entre `critica` (muda decisao), `media` (confunde quem le) e `baixa` (cosmetica).

### Passe 3: qualidade narrativa

Releia o `CLAUDE.md` de ponta a ponta fingindo ser o cliente. Procure:

1. Redundancia: a mesma informacao em dois lugares sem agregar contexto
2. Lacuna: algo prometido em um arquivo que nenhum outro responde
3. Tom inconsistente entre secoes
4. Transicao abrupta: pulo logico que pede uma frase de ligacao
5. Evolucao nao explicitada: o Passe 1 achou um arco mas o consolidado so mostra o estado final
6. Honestidade: algo vendido como vantagem em um arquivo que outro revela como fraqueza

Para cada gap: tipo, localizacao (arquivo e secao), descricao, ajuste proposto com o texto exato a entrar ou sair, e arquivo afetado.

### Sintese: lista de edicoes

Consolide os tres passes numa lista de edicoes concretas. Cada uma precisa ser autoexecutavel:

- `id` sequencial (U1, U2, ...)
- `arquivo`
- `local`: caminho JSON ou titulo de secao
- `acao`: substituir, adicionar ou remover
- `valor_antigo` e `valor_novo` (use vazio explicito quando for adicao ou remocao)
- `motivo`, citando a evolucao ou a divergencia de origem
- `severidade`
- `origem`: evolucao, factual ou narrativa

Ordene por severidade, criticas primeiro. Se uma correcao afeta varios arquivos, liste cada arquivo como entrada separada com o mesmo motivo.

## Auto-validacao

Antes de mostrar ao usuario, confira:

- [ ] Nomeou o cliente e a janela exata revisada?
- [ ] Leu de baixo pra cima, do recente ao briefing?
- [ ] O Passe 1 achou ao menos duas evolucoes, ou justificou a ausencia?
- [ ] Cada evolucao tem hipotese inicial, evidencia, decisao atual e narrativa?
- [ ] O Passe 2 so tem conflito dentro da mesma camada?
- [ ] Cada divergencia cita arquivo, local, valor atual e valor recomendado?
- [ ] Cada gap narrativo tem ajuste executavel, e nao um "melhorar a redacao"?
- [ ] A lista de edicoes esta ordenada por severidade?
- [ ] Cada edicao tem valor antigo e valor novo?
- [ ] Nenhum item generico. Tudo e diff concreto?
- [ ] Estimativa marcada como estimativa, e nao apresentada como dado apurado?
- [ ] Nada foi inventado para preencher lacuna?

Se falhou, refaca antes de apresentar.

## Apresentacao e decisao

Apresente um relatorio com quatro secoes:

1. **Evolucao estrategica.** Para cada uma: tema, o arco (declarado, apurado, decidido) e impacto. E a secao principal.
2. **Divergencia factual.** Tabela com numero, campo, atual contra proposto, severidade.
3. **Gap narrativo.** Lista numerada com tipo, localizacao e ajuste.
4. **Edicoes propostas.** Tabela com numero, arquivo, local, antigo contra novo, motivo e origem.

Peca decisao item a item:

> Para cada item abaixo, responda ACEITAR, REJEITAR ou AJUSTAR com a nova versao. Pode responder em bloco, por exemplo "U1 aceitar, U2 rejeitar, U3 ajustar: ...".

Espere a decisao. Nao aplique nada antes.

## Finalizacao

Depois que o usuario decidir:

1. **Salve o relatorio** em `checkins/{YYYY-MM-DD}-revisao-semanal.md`, com um resumo no topo: janela revisada, quantas evolucoes, quantas divergencias, quantos gaps, quantas edicoes aceitas, rejeitadas e ajustadas. Se ja existir revisao anterior, preserve o historico e acrescente.

2. **Aplique as edicoes aceitas** nos arquivos alvo. Use Edit, nao Write, para nao perder historico. Para edicao vinda de evolucao, registre tambem o arco no proprio arquivo, para que a mudanca continue rastreavel depois.

3. **Atualize o Mission Control:**
   - `historico-checkins.md`: nova entrada com a data, o modo (revisao de desk, nao foi call), a janela coberta e os pontos criticos.
   - `apostas-vivas.md`: se uma evolucao matou, confirmou ou criou aposta, mexa aqui.
   - `okr-quarter.md`: se um numero-chave mudou de valor ou de status, atualize.
   - `combinados.md`: se a revisao gerou pendencia nova, registre com dono e prazo.

4. **Rode `/contexto` na pasta do cliente.** Obrigatorio. E o que mantem `CLAUDE.md` e `AGENTS.md` alinhados aos outputs corrigidos. Nao pule.

5. **Reporte:** janela revisada, quantas evolucoes registradas, quantas edicoes aplicadas de quantas propostas, e quais arquivos mudaram. Sugira o proximo passo, que costuma ser preparar o proximo check-in com `account-checkin-roleplay`.

## Regras

- Nao invente dado, claim, numero nem citacao para fechar uma lacuna. Lacuna vira gap declarado.
- Nao confunda evolucao com erro. Evolucao entre camadas se registra; contradicao dentro da camada se corrige.
- Nao refaca skill. Se um output esta errado na raiz, o certo e rodar a skill de novo, nao remendar aqui.
- Nao apague historico. Toda correcao preserva o que estava antes de forma rastreavel.
- Estimativa continua marcada como estimativa depois da revisao.
- Nunca commite `squads/` nem `bases/`. Sao pessoais e ficam no `.gitignore`.
