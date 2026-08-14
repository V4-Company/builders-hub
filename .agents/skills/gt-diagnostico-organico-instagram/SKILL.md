---
name: gt-diagnostico-organico-instagram
description: "Diagnostico de conteudo organico no Instagram — cliente vs 2 concorrentes, ultimos 90 dias, via Instagram Graph API + business_discovery. Use quando o operador disser /gt-diagnostico-organico-instagram ou 'analisar conteudo organico' ou 'diagnostico de instagram' ou 'analise de conteudo do cliente'."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
  - geral-pesquisa-mercado
tools: []
week: 2
estimated_time: "45min"
output_file: "gt-diagnostico-organico-instagram.json"
multimodal: true
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Diagnostico de Conteudo Organico — Instagram (POP 2.2)

> **Posição no fluxo:** Semana 2 — comum a todos os modelos. Engagement sempre **normalizado por seguidores** (taxa, não absoluto). Gera ações editoriais guiadas por gaps dos concorrentes.

Voce e um diretor de conteudo digital focado em PMEs brasileiras. Vai rodar um diagnostico comparativo do feed organico do cliente contra 2 concorrentes no Instagram — ultimos 90 dias — usando dados reais da Instagram Graph API (sem necessidade de acesso do cliente), com embed oficial dos posts no portal.

**CAPACIDADE MULTIMODAL:** Voce pode analisar visualmente as mídias baixadas (imagens e thumbnails de vídeo) para complementar a analise quantitativa.

## Pre-requisitos

1. `.credentials/meta-graph-api.json` preenchido com token de longa duracao (60 dias) valido.
   - O token DEVE incluir as permissions: `instagram_basic`, `instagram_manage_insights`, `pages_show_list`, `pages_read_engagement`. Sem `instagram_manage_insights` o endpoint `business_discovery` retorna erro #10.
2. Cliente com conta Instagram Business ou Creator (validar via business_discovery antes).
3. `outputs/geral-pesquisa-mercado.json` presente (usado para selecionar os 2 concorrentes automaticamente).

## Selecao automatica de concorrentes (regra fixa)

1. Ler `outputs/geral-pesquisa-mercado.json` → `competitors[]`
2. Ordenar por `digital_score` DESC
3. Pegar os **TOP 2** com handle Instagram conhecido
4. Validar via `business_discovery` — se algum nao for Business/Creator, cair para o #3, e assim por diante
5. Se o @handle de um concorrente nao estiver mapeado no briefing ou na pesquisa, perguntar ao operador uma unica vez

Nunca deixe o operador decidir manualmente a menos que a regra falhe — padrao e automatico.

## Dados necessarios

1. Leia `client.json` (seção `briefing`) — extraia: NOME_CLIENTE, SEGMENTO, instagram (handle do cliente), ICP resumido, tom de voz
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, dores, linguagem
3. Leia `outputs/geral-posicionamento-estrategico.json` — extraia: PUV, tagline, territorio, tom
4. Leia `outputs/geral-pesquisa-mercado.json` — extraia TOP 2 competitors por `digital_score`

Se faltar o @handle do cliente no briefing, pergunte:

> Qual o @ do Instagram do {NOME_CLIENTE}?

## Execucao

O script empacotado usa `client.json` para descobrir o handle do cliente e os concorrentes. Se esse arquivo não existir na KB do Hub, não o crie só para satisfazer o script: peça os três handles ao operador e faça a coleta pela integração disponível ou trabalhe com uma exportação fornecida, sempre registrando a limitação.

```bash
bash .claude/skills/gt-diagnostico-organico-instagram/scripts/ig_organic_audit.sh squads/{squad}/clientes/{cliente}
```

O script:
1. Lê `.credentials/meta-graph-api.json`, `client.json`, `outputs/geral-pesquisa-mercado.json`
2. Identifica o handle do cliente + 2 concorrentes top do scorecard
3. Chama `business_discovery` para cada um (perfil + posts 90 dias)
4. Calcula metricas publicas (engagement proxy) e classifica por formato/cadencia
5. Salva raw em `squads/{squad}/clientes/{cliente}/cache/ig_organic_audit-{ts}.json`
6. Condensa em `squads/{squad}/clientes/{cliente}/cache/ig_organic_audit-summary.json` — input direto pra skill gerar o output

## Geracao

Gere o output COMPLETO de uma vez usando o summary do script + outputs de dependencias.

Interpretacoes obrigatorias (nao pular):

### `top_posts` (top 3 por conta)
Para CADA post nos top 3 de CADA uma das 3 contas:
- `permalink` → `embed_url` = `permalink` + `embed/` (o portal vai montar o iframe)
- Caption completa, formato (FEED/REELS/CAROUSEL), likes, comments, engagement_proxy
- **Diagnostico qualitativo**: o que esta funcionando neste post (hook, visual, angulo). 2 frases objetivas.
- Se for concorrente e o cliente NAO tem algo similar, marcar `gap_para_cliente: true` e explicar o que replicar.

### `bottom_posts` (bottom 3 do CLIENTE apenas)
Os 3 piores do cliente por engagement_proxy:
- Mesmo formato dos top_posts
- **Diagnostico de por que quebrou** — hipotese: caption fraca? hora errada? formato errado? falta de hook?

### `format_distribution` e `cadence`
Tabela comparativa das 3 contas. Aponte especificamente onde o cliente esta DESALINHADO com quem performa melhor (ex: concorrente posta 60% em Reels, cliente posta 10%).

### `competitor_patterns_missing` (priorizado)
Padroes recorrentes que aparecem nos concorrentes e NAO aparecem no cliente. Cada item com:
- Descricao do padrao
- Quantos posts dos concorrentes usam
- Por que provavelmente funciona para o ICP do cliente
- Como o cliente poderia implementar

Esta e a parte mais acionavel do relatorio.

### `client_winning_patterns`
Padroes do cliente acima da media — replicar e amplificar.

### `instagram_compliance`
Checagem rapida de aspect ratio, uso de texto em imagem, safe zones de Reels. Usar dados publicos (aspect ratio via media_url, analise visual dos frames extraidos).

### `next_actions`
Lista priorizada de 5-8 acoes (o que mudar, qual formato testar, qual tipo de conteudo replicar). Cada uma com impacto estimado + facilidade.

## Auto-validacao

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais da Graph API (nao inventou numeros)?
- [ ] Nenhum item generico?
- [ ] Schema validou?
- [ ] Top 3 de cada conta tem permalink valido + embed_url?
- [ ] Consistente com ICP e posicionamento?
- [ ] Padroes missing sao acionaveis (nao "melhorar conteudo")?
- [ ] next_actions sao especificos?

Se falhou → regenere silenciosamente.

## Apresentacao e decisoes

Apresente o output COMPLETO ao operador.

- "Os posts top 3 do cliente e concorrentes batem com o que voce observou empiricamente?"
- "Algum padrao dos concorrentes que voce ja sabia que funciona e esta aqui listado?"
- "As proximas acoes sao factiveis no time atual?"
- "Alguma limitacao do cliente que eu nao considerei? (ex: nao pode gravar Reels pra quem tem pouco tempo de filmagem)"

## Finalizacao

1. Salve `squads/{squad}/clientes/{cliente}/outputs/gt-diagnostico-organico-instagram.json` (com `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, history[]
3. Salve também uma versão Markdown do diagnóstico na pasta de outputs compatível com o Hub.
4. Sugira proxima skill:
   - "Diagnostico organico IG concluido. Cliente: {followers} seguidores, {posts_90d} posts/90d. Top formato do cliente: {formato}. Gaps identificados: {numero}."
   - "Este diagnostico alimenta: /designer-criativos-anuncios (padroes que funcionam para o ICP no organico)"
   - "Próximo passo recomendado: consolidar os diagnósticos com /gt-diagnostico-maturidade-digital e fechar com /geral-posicionamento-estrategico."

## Campo obrigatorio: summary

```json
"summary": "Resumo 1-2 frases com nome do cliente, metricas-chave (eng_proxy cliente vs top concorrente), gap principal e acao prioritaria. Sem generico."
```
