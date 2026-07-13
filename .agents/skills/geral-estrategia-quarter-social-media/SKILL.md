---
name: geral-estrategia-quarter-social-media
description: Gera um deck HTML com visão de slides (navegação tipo apresentação — setas, pontos e teclado, full-screen) no Design System V4 (Red Command Center: gradiente vermelho/dourado, glass morphism) para apresentar a revisão estratégica trimestral (quarter) de social media de um cliente — vitórias do quarter, números do período com gráfico de evolução, os 3 melhores conteúdos com justificativa de performance, aprendizados, novidades baseadas em pesquisa real de tendências, plano de ação com um slide por ação (cada uma justificada) e metas do próximo quarter, cronograma de responsáveis e riscos. Arquivo único e reutilizável (duplicar e editar a cada novo quarter/cliente), pronto pra abrir no browser ou subir na Vercel. Use sempre que o usuário pedir revisão trimestral de social media, QBR (quarterly business review), apresentação de estratégia por quarter, recap do quarter pro cliente, ou quiser montar o material de uma reunião de fechamento/abertura de trimestre — mesmo que não diga "quarter" ou "trimestral" explicitamente. Ative também quando o usuário disser "preciso apresentar a estratégia do próximo trimestre", "montar o recap do quarter", "apresentação tipo slide pro cliente", "review trimestral de social", "fechamento do Q1/Q2/Q3/Q4" ou similar.
area: geral
author: bhrendacruz-bot
version: 1.2.0
---

# Revisão Estratégica de Quarter — Social Media

Gera um deck HTML único que funciona como apresentação de slides de verdade — não um documento de scroll. Cada seção é uma tela cheia, navegada com setas, pontos ou teclado, igual a uma apresentação feita em Google Slides ou Keynote, mas rodando direto no browser sem depender de nenhuma ferramenta externa.

O deck existe pra dar suporte à reunião onde o account fecha o quarter que passou e abre o próximo com o cliente — vitórias, números, aprendizados, e o plano do trimestre seguinte, tudo amarrado e justificado.

Visualmente segue o Design System V4 (**Red Command Center**) — o mesmo usado em `/geral-relatorio-v4`, `/geral-plano-acao-social-media` e `/account-checkin-resultados`: gradiente vermelho/marrom de fundo, dourado como cor de destaque, cards em glass morphism. Repositório oficial do design system: https://github.com/guilhermeduarte-billions/v4-design-system

---

## Antes de começar: coleta de contexto

Verifique se já existe contexto disponível antes de perguntar tudo:

1. **KB do cliente** — se estiver dentro de `squads/{squad}/clientes/{cliente}/`, leia o `CLAUDE.md`, `AGENTS.md` e `mission-control/` primeiro. OKRs, apostas vivas e histórico de check-in já dizem boa parte do que entra nas seções de vitórias, aprendizados e metas.
2. **Relatórios e check-ins anteriores** — se existir HTML de `/account-checkin-resultados` ou `/geral-relatorio-v4` do período, puxe os números de lá em vez de perguntar de novo.
3. **Se não tiver nada** — conduza a entrevista abaixo, agrupada por bloco. Não despeje 10 perguntas de uma vez.

### O que coletar (uma seção do deck por linha, na ordem em que aparecem no deck)

| Seção do deck | O que perguntar |
|---|---|
| Capa | Nome do cliente, período (ex: Q3 · 2026) |
| Vitórias do Quarter | 3-6 conquistas reais e quantificadas do trimestre |
| Números do Período | Métricas do período (alcance, engajamento, seguidores, cliques, conversões) **e** uma série pra virar gráfico — breakdown mês a mês dentro do trimestre, ou pelo menos o comparativo com o trimestre anterior |
| Melhores Conteúdos | Exatamente **3** posts top performers: descrição do conteúdo (o que o post mostra/fala — sem imagem, é só texto + link), link real pro post no Instagram, os 3 stats (Visualizações, Interações, Seguidores) **e por que esse post performou** (não só o número — a leitura por trás) |
| Aprendizados | O que funcionou, o que não funcionou, o que precisa ajustar |
| Novidades pro Próximo Quarter | Não pergunte isso ao usuário — pesquise de verdade. Veja o passo dedicado abaixo |
| Plano de Ação | Ações concretas pro próximo quarter, e **por que cada uma faz sentido** (dado, aprendizado ou lógica que sustenta a escolha) |
| Metas do Próximo Quarter | Objetivos mensuráveis — usando a mesma categoria/nome já citado nas tags do Plano de Ação |
| Cronograma / Responsáveis | Quem faz o quê, e quando |
| Riscos / Pontos de Atenção | Sazonalidade, dependências externas, gargalos de aprovação, etc. |
| Investimento (opcional) | Só se o quarter envolver budget de mídia paga — fica oculto por padrão no deck |

Não invente números. Se o usuário não tiver um dado (ex: não tem breakdown mensal, ou não rastreia conversões), pergunte ou omita o elemento em vez de preencher com estimativa não sinalizada.

---

## Passo 1 — Pesquisa de tendências (antes de montar Novidades)

O slide de Novidades não é uma lista de achismos — é pesquisa de verdade, aplicada ao cliente específico. Antes de escrever esse slide:

1. **Use a ferramenta de busca (WebSearch)** pra levantar tendências atuais e reais de social media e do setor do cliente. Pesquise por ângulos como: `tendências social media [setor do cliente] [ano]`, `tendências Instagram/TikTok [trimestre] [ano]`, `o que está performando em [formato] agora`. Não se contente com a primeira busca genérica — refine pelo segmento e pelo momento real do cliente.
2. **Cruze cada tendência encontrada com o cliente** — público, posicionamento, recursos de produção disponíveis. Uma tendência que não se aplica ao cliente não entra no slide, por mais relevante que seja em geral.
3. **Selecione 3-5 tendências** que sobreviveram ao filtro acima. Pra cada uma, escreva dois blocos curtos: **o que é** (a tendência em si, com contexto de onde vem) e **como aplicar pro cliente** (a ação prática, específica, não genérica).

Ruim: "usar mais vídeo". Bom: "Conteúdo de processo (behind the scenes de produção) está performando acima de conteúdo polido em [setor] — pro [cliente], isso significa documentar o processo de fabricação real em vez de só mostrar produto finalizado."

Se a busca não trouxer nada de relevante e específico o suficiente, é melhor entregar 3 tendências bem fundamentadas do que 5 genéricas só pra preencher espaço.

---

## Como o deck funciona

Isso não é um relatório de scroll — é uma apresentação navegável. Entenda a mecânica antes de montar o HTML:

- **Cada seção é um slide cheio de tela** (`<section class="slide">`), com transição suave entre eles. Só um slide fica visível por vez (classe `.active`).
- **Header fixo no topo** (`.topbar`) aparece em todo slide, com o nome do cliente e o período (ex: "Metal Comércio · Q3 2026") — cliente e período sempre visíveis, em todas as telas.
- **Navegação por seta** (`.nav-prev` / `.nav-next`) fixa nos cantos inferiores, mais **pontos de progresso** (`.dots`) no centro inferior — clicáveis, indicam em qual slide você está.
- **Teclado:** seta direita ou espaço avança, seta esquerda volta, Home vai pro primeiro slide, End vai pro último.
- **Algumas seções viram mais de um slide.** O Plano de Ação, por exemplo, é um slide por ação — não uma lista dentro de um slide só. O JS de navegação conta automaticamente quantos `.slide` existem no HTML (`.deck-counter` e `.dots` se ajustam sozinhos), então não precisa calcular nem travar a contagem na hora de montar o documento.
- **Slide de Investimento é opcional e fica oculto por padrão.** Um botão no header (`.investimento-toggle`) liga/desliga esse slide — o account só ativa quando o quarter realmente envolve mídia paga, sem precisar editar o HTML.
- **Sem CSS de impressão por enquanto.** O foco de entrega é abrir no browser ou subir como link estático na Vercel (mesmo padrão das pastas `deploy-*` que já existem no projeto).

Toda a navegação roda em JavaScript vanilla, sem framework e sem build — o arquivo final continua sendo um HTML único e autocontido.

---

## Passo 2 — Montar o CSS e o JS (sempre embutidos)

O arquivo final precisa ser autocontido — nenhum link para arquivo externo além do Google Fonts.

1. Copie o conteúdo inteiro de `assets/estrategia-quarter-social-media.css` pra dentro de uma tag `<style>` no `<head>`.
2. Copie o conteúdo inteiro de `assets/estrategia-quarter-social-media.js` pra dentro de uma tag `<script>` logo antes de `</body>`.

Nunca referencie esses arquivos como `<link>` ou `<script src="...">` — o HTML final precisa abrir sozinho, sem depender da pasta da skill.

### Font — Google Fonts no `<head>`

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wdth,wght@75..100,500;75..100,700&display=swap" rel="stylesheet">
```

Essa é a variante **variável** da fonte (eixo `wdth`), não a estática — é o que faz o `font-stretch: 75%` dos títulos funcionar e dar a leitura condensada característica do Red Command Center. Se usar a versão estática da fonte, os títulos perdem esse efeito.

### Como adicionar imagens (logo, prints, etc.)

A logo da V4 no header (`.brand-logo`) já vem como `<img src="https://...">` apontando pro avatar oficial do canal da V4 no YouTube — funciona porque essa URL está hospedada e acessível publicamente. Use o mesmo princípio pra qualquer outra imagem que precisar entrar no deck (ex: se o account decidir usar print de post numa versão futura). Três formas, em ordem de preferência conforme o caso:

1. **URL já hospedada** (mais simples) — se a imagem já está em algum lugar público (Drive com link público, CDN, Instagram), só usa a URL direto no `src`. É o que fizemos com a logo. Risco: se o link sumir ou mudar, a imagem quebra no deck.
2. **Pasta de imagens ao lado do HTML** — se for fazer deploy na Vercel (pasta `deploy-*`) ou manter o arquivo numa pasta do cliente, crie uma pasta `images/` do lado do `.html` e referencie como `src="images/post1.jpg"`. Funciona bem porque a pasta inteira viaja junto — só não é mais "um arquivo só".
3. **Base64 inline** (mais portátil, mais pesado) — converte a imagem pra base64 e cola direto no `src="data:image/png;base64,...."`. O HTML continua sendo um arquivo único de verdade, sem nenhuma dependência externa, mas o arquivo fica maior. Use quando portabilidade total importa mais que o tamanho do arquivo.

---

## Passo 3 — Estrutura do HTML

Use essa ordem fixa de slides. IDs batem com as classes do CSS — não troque os nomes, é o que permite o account achar e editar rápido depois.

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Revisão de Quarter · {Cliente} · {Período}</title>
  <!-- Google Fonts aqui -->
  <style>/* CSS completo de assets/estrategia-quarter-social-media.css aqui */</style>
</head>
<body>

  <header class="topbar">
    <div class="brand">
      <img class="brand-logo" src="https://yt3.googleusercontent.com/q3RC0cQqUO1Kjlw3spaUn30KRr8HH6e6mWDjsnRJnP7bj2Vhqx4blPLtByZGwS-rvxDpUAzM=s900-c-k-c0x00ffffff-no-rj" alt="V4">
      <!-- EDITAR: nome do cliente e período -->
      Metal Comércio · Q3 2026
    </div>
    <div class="deck-meta">
      <span class="deck-counter">01 / 11</span>
      <button class="investimento-toggle">+ Mostrar investimento</button>
    </div>
  </header>

  <main class="deck">

    <!-- SLIDE 0 — CAPA -->
    <section class="slide slide-capa active" id="capa">
      <!-- EDITAR: título e metadados da capa -->
      <h1>Revisão de Quarter de Social Media.</h1>
      <div class="capa-meta">
        <div>Cliente<strong>Metal Comércio</strong></div>
        <div>Período<strong>Q3 · 2026</strong></div>
      </div>
    </section>

    <!-- SLIDE 1 — VITÓRIAS DO QUARTER -->
    <section class="slide" id="vitorias">
      <div class="slide-eyebrow">Seção 1 · Fechamento do quarter</div>
      <h2>Vitórias do quarter.</h2>
      <p class="slide-sub"><!-- EDITAR: uma frase de contexto sobre o que esse trimestre representou --></p>
      <div class="slide-body">
        <div class="grid-3">
          <!-- EDITAR: 3-6 cards, um por conquista. Sempre quantificada -->
          <div class="card accent">
            <div class="card-title">ROAS recorde: 4.2x</div>
            <div class="card-text">Melhor resultado de mídia paga desde o início da conta.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 2 — NÚMEROS DO PERÍODO -->
    <section class="slide" id="numeros">
      <div class="slide-eyebrow">Seção 2 · Performance</div>
      <h2>Números do período.</h2>
      <div class="slide-body">
        <div class="grid-4">
          <!-- EDITAR: só inclua os campos que o cliente acompanha -->
          <div class="kpi-card">
            <div class="kpi-value red">128k</div>
            <div class="kpi-label">Alcance</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-value">4.8%</div>
            <div class="kpi-label">Engajamento</div>
          </div>
        </div>
        <!-- EDITAR: gráfico mostra evolução mês a mês da métrica mais relevante (ex: alcance).
             width em % é relativo ao maior valor do trimestre. Se não tiver breakdown mensal,
             troque os labels por "Quarter anterior" / "Este quarter" -->
        <div class="bar-chart">
          <div class="bar-row">
            <div class="bar-label">Mês 1</div>
            <div class="bar-track"><div class="bar-fill" style="width:58%">38k</div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">Mês 2</div>
            <div class="bar-track"><div class="bar-fill" style="width:74%">46k</div></div>
          </div>
          <div class="bar-row">
            <div class="bar-label">Mês 3</div>
            <div class="bar-track"><div class="bar-fill" style="width:100%">62k</div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 3 — MELHORES CONTEÚDOS (sempre 3, com ranking e justificativa) -->
    <section class="slide" id="conteudos">
      <div class="slide-eyebrow">Seção 3 · Top performers</div>
      <h2>Melhores conteúdos.</h2>
      <div class="slide-body">
        <div class="grid-3">
          <!-- EDITAR: exatamente 3 cards. Sem imagem — só descrição do conteúdo + link pro post real no
               Instagram + os 3 stats (Visualizações, Interações, Seguidores) + justificativa.
               Não invente posts nem número — se não tiver um dos 3 stats pro post, omita aquele post-stat -->
          <div class="card post-card">
            <span class="post-rank">1</span>
            <div class="card-title"><!-- tema do post --></div>
            <div class="card-text"><!-- descricao do conteudo: o que o post mostra/fala, nao numero --></div>
            <a class="post-link" href="" target="_blank" rel="noopener">Ver no Instagram ↗</a>
            <div class="post-stats">
              <div class="post-stat"><div class="post-stat-value"><!-- ex: 22k --></div><div class="post-stat-label">Visualizações</div></div>
              <div class="post-stat"><div class="post-stat-value"><!-- ex: 1.840 --></div><div class="post-stat-label">Interações</div></div>
              <div class="post-stat"><div class="post-stat-value"><!-- ex: +96 --></div><div class="post-stat-label">Seguidores</div></div>
            </div>
            <div class="post-justificativa"><strong>Por que performou:</strong> <!-- a leitura por tras do numero --></div>
          </div>
          <div class="card post-card">
            <span class="post-rank">2</span>
            <div class="card-title"></div>
            <div class="card-text"></div>
            <a class="post-link" href="" target="_blank" rel="noopener">Ver no Instagram ↗</a>
            <div class="post-stats">
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Visualizações</div></div>
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Interações</div></div>
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Seguidores</div></div>
            </div>
            <div class="post-justificativa"><strong>Por que performou:</strong> </div>
          </div>
          <div class="card post-card">
            <span class="post-rank">3</span>
            <div class="card-title"></div>
            <div class="card-text"></div>
            <a class="post-link" href="" target="_blank" rel="noopener">Ver no Instagram ↗</a>
            <div class="post-stats">
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Visualizações</div></div>
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Interações</div></div>
              <div class="post-stat"><div class="post-stat-value"></div><div class="post-stat-label">Seguidores</div></div>
            </div>
            <div class="post-justificativa"><strong>Por que performou:</strong> </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 4 — APRENDIZADOS -->
    <section class="slide" id="aprendizados">
      <div class="slide-eyebrow">Seção 4 · Leitura do quarter</div>
      <h2>Aprendizados.</h2>
      <div class="slide-body">
        <div class="grid-3">
          <div class="card accent">
            <div class="card-title">O que funcionou</div>
            <div class="card-text"><!-- EDITAR --></div>
          </div>
          <div class="card">
            <div class="card-title">O que não funcionou</div>
            <div class="card-text"><!-- EDITAR --></div>
          </div>
          <div class="card">
            <div class="card-title">O que ajustar</div>
            <div class="card-text"><!-- EDITAR --></div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 5 — NOVIDADES PRO PRÓXIMO QUARTER (vem do Passo 1, pesquisa real) -->
    <section class="slide" id="novidades">
      <div class="slide-eyebrow">Seção 5 · Olhando pra frente</div>
      <h2>Novidades para o próximo quarter.</h2>
      <p class="slide-sub">Tendências reais, pesquisadas e aplicadas ao momento específico do cliente.</p>
      <div class="slide-body">
        <div class="grid-2">
          <!-- EDITAR: 3-5 cards, cada um com a tendência pesquisada (Passo 1) + aplicação pro cliente -->
          <div class="card">
            <div class="card-title"><!-- nome da tendência --></div>
            <div class="trend-block">
              <div class="trend-label">O que é</div>
              <div class="trend-text"><!-- a tendência, com contexto de onde vem --></div>
            </div>
            <div class="trend-block">
              <div class="trend-label">Como aplicar pro cliente</div>
              <div class="trend-text"><!-- ação prática, específica --></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDES 6.N — PLANO DE AÇÃO (um slide por ação, com justificativa. Vem antes de Metas) -->
    <section class="slide" id="plano-acao-1">
      <div class="slide-eyebrow">Seção 6 · Plano de ação · Ação 1 de 2</div>
      <div class="acao-numero">1</div>
      <h2>Migração de perfis para fotos reais.</h2>
      <div class="tags-row"><span class="tag red">Crescimento de seguidores</span></div>
      <div class="slide-body">
        <div class="grid-2">
          <div class="card">
            <div class="card-title">O que vamos fazer</div>
            <div class="card-text">Substituir fotos de banco de imagem por fotos reais da equipe e do espaço físico, em todos os perfis ativos.</div>
          </div>
          <div class="card accent">
            <div class="card-title">Por que essa ação</div>
            <!-- EDITAR: a justificativa precisa vir de dado, aprendizado, lógica real ou benchmark de mercado — não genérica -->
            <div class="card-text">Feed com cara de banco de imagem já lê como datado. Grandes marcas estão migrando pra um feed com imagens mais conceituais e legendas que dissertam sobre os temas em vez de só ilustrar produto — usando a imagem como ponto de partida pro storytelling, não como o conteúdo em si. Já temos marcas de referência do segmento aplicando esse formato ativamente — não é mais tendência futura. Fotos reais da equipe e do espaço aproximam a marca desse padrão e geram mais conexão do que o que está no ar hoje.</div>
          </div>
        </div>
      </div>
    </section>

    <section class="slide" id="plano-acao-2">
      <div class="slide-eyebrow">Seção 6 · Plano de ação · Ação 2 de 2</div>
      <div class="acao-numero">2</div>
      <h2>Fluxo direcionado para WhatsApp via funil de vendas.</h2>
      <div class="tags-row"><span class="tag red">Conversão</span></div>
      <div class="slide-body">
        <!-- EDITAR: essa ação descreve um processo de várias etapas, então vira um fluxo visual
             (.flow-diagram) em vez de só texto — 2 a 4 passos, cada um com etapa + o que acontece ali -->
        <div class="flow-diagram">
          <div class="flow-step">
            <div class="flow-step-label">1 · Atração</div>
            <div class="flow-step-title">Posts no feed</div>
            <div class="flow-step-text">Atração mora no feed, não só em Stories — é onde alcança quem ainda não segue o perfil</div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="flow-step-label">2 · Interesse</div>
            <div class="flow-step-title">Stories com CTA</div>
            <div class="flow-step-text">Reforça a oferta e direciona pro link</div>
          </div>
          <div class="flow-arrow">→</div>
          <div class="flow-step">
            <div class="flow-step-label">3 · Conversão</div>
            <div class="flow-step-title">WhatsApp comercial</div>
            <div class="flow-step-text">Time comercial assume a conversa</div>
          </div>
        </div>
        <div class="grid-2">
          <div class="card">
            <div class="card-title">O que vamos fazer</div>
            <div class="card-text">Criar sequência de conteúdo (Stories + Reels) que direciona o público pro WhatsApp comercial, com CTA explícito em cada etapa do fluxo acima.</div>
          </div>
          <div class="card accent">
            <div class="card-title">Por que essa ação</div>
            <div class="card-text">312 cliques no link do quarter passado não converteram em mensagem — falta um caminho direto e guiado até o WhatsApp.</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 7 — METAS DO PRÓXIMO QUARTER (vem depois do Plano de Ação) -->
    <section class="slide" id="metas">
      <div class="slide-eyebrow">Seção 7 · Próximo trimestre</div>
      <h2>Metas do próximo quarter.</h2>
      <p class="slide-sub">As tags abaixo retomam as mesmas categorias usadas no plano de ação.</p>
      <div class="slide-body">
        <div class="grid-3">
          <!-- EDITAR: o label da meta precisa repetir o nome da tag usada no plano de ação -->
          <div class="kpi-card">
            <div class="kpi-value red">+15%</div>
            <div class="kpi-label">Crescimento de seguidores</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-value red">+8%</div>
            <div class="kpi-label">Conversão</div>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 8 — CRONOGRAMA / RESPONSÁVEIS -->
    <section class="slide" id="cronograma">
      <div class="slide-eyebrow">Seção 8 · Quem faz o quê</div>
      <h2>Cronograma e responsáveis.</h2>
      <div class="slide-body">
        <!-- EDITAR: um list-row por ação do plano -->
        <div class="list-row">
          <div class="list-main">
            <div class="list-title">Migração de perfis para fotos reais</div>
          </div>
          <div class="list-tags">
            <span class="tag white">Responsável: Designer</span>
            <span class="tag white">Prazo: até 15/08</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SLIDE 9 — RISCOS / PONTOS DE ATENÇÃO -->
    <section class="slide" id="riscos">
      <div class="slide-eyebrow">Seção 9 · Atenção</div>
      <h2>Riscos e pontos de atenção.</h2>
      <div class="slide-body">
        <!-- EDITAR: tag "Alto" em vermelho só pra risco real. Não exagere -->
        <div class="list-row">
          <div class="list-main">
            <div class="list-title">Sazonalidade de fim de ano</div>
            <div class="list-detail">Queda histórica de engajamento orgânico em dezembro pode impactar a meta de alcance.</div>
          </div>
          <div class="list-tags"><span class="tag danger">Alto</span></div>
        </div>
      </div>
    </section>

    <!-- SLIDE 10 — INVESTIMENTO (opcional, oculto por padrão) -->
    <section class="slide slide-investimento slide-disabled" id="investimento">
      <div class="slide-eyebrow">Seção 10 · Mídia paga</div>
      <h2>Investimento.</h2>
      <p class="slide-sub">Só ative essa seção se o quarter envolver budget de mídia paga — use o botão no header.</p>
      <div class="slide-body">
        <div class="grid-3">
          <!-- EDITAR: linhas de orçamento por linha de investimento -->
          <div class="kpi-card">
            <div class="kpi-value red">R$ 12.000</div>
            <div class="kpi-label">Budget previsto</div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <button class="nav-arrow nav-prev" aria-label="Slide anterior">‹</button>
  <button class="nav-arrow nav-next" aria-label="Próximo slide">›</button>
  <div class="dots"></div>

  <script>/* JS completo de assets/estrategia-quarter-social-media.js aqui */</script>
</body>
</html>
```

O contador no header (`.deck-counter`) e os pontos (`.dots`) são gerados/atualizados pelo JS automaticamente a partir do número real de `.slide` no HTML — não precisa contar na mão, é só o valor inicial antes do script rodar. Adicione ou remova slides de Plano de Ação (`plano-acao-1`, `plano-acao-2`, `plano-acao-3`...) conforme o número real de ações do quarter, atualizando o "Ação X de N" no eyebrow de cada uma.

---

## Regras de conteúdo

- **Sem tabelas.** Cronograma e riscos usam `.list-row` — visualmente mais limpo numa tela de apresentação e mais fácil de ler de longe numa reunião.
- **Vitórias sempre quantificadas.** "ROAS de 4.2x" e não "bons resultados". "847 seguidores novos" e não "crescimento expressivo".
- **Melhores Conteúdos são sempre 3 — nem mais, nem menos, e sem imagem.** Cada um leva o número de ranking (1, 2, 3), descrição do conteúdo (não número), link real pro post no Instagram, os 3 stats fixos (Visualizações, Interações, Seguidores) e uma justificativa separada de tudo isso: os stats dizem o quanto performou, a justificativa diz o porquê. Se faltar um dos 3 stats pra um post específico, omita só aquele `post-stat` — não invente. Se o usuário só tiver 2 posts com dado real, pergunte pelo terceiro antes de inventar.
- **Ações que descrevem um processo viram fluxo visual, não só texto.** Quando uma ação do Plano de Ação envolve várias etapas (funil, jornada do cliente, sequência de conteúdo), use `.flow-diagram` — passos conectados por seta, 2 a 4 no máximo — pra dar ao cliente uma leitura tipo mapa mental da proposta, mais rápida do que parágrafo corrido. Ações de etapa única (ex: "migração de fotos") não precisam de fluxo — só o `grid-2` de "O que vamos fazer" / "Por que essa ação" já basta.
- **A etapa de atração de um funil mora no feed, não em Stories.** Stories alcança majoritariamente quem já segue o perfil; quem ainda não segue descobre pelo feed (Explorar, hashtags, indicação do algoritmo). Se o primeiro passo de um `.flow-diagram` for sobre atrair gente nova, o formato é post de feed — Stories entra depois, na etapa de interesse/nutrição de quem já chegou.
- **Gráfico de Números do Período não pode ter dado inventado.** Use breakdown mensal real quando existir; na falta dele, use o comparativo trimestre atual vs anterior; na falta dos dois, omita o gráfico e mantenha só os KPIs.
- **Novidades vêm de pesquisa real (Passo 1), não de generalização.** "Postar mais Reels" não é tendência, é genérico. A tendência tem nome, contexto de onde vem, e uma aplicação específica pro cliente.
- **Plano de Ação vem antes de Metas no deck — e cada ação é o próprio slide.** A justificativa de cada ação precisa vir de algo real: um dado do próprio cliente (ex: algo que apareceu no slide de Aprendizados), ou um benchmark de mercado (ex: pra onde marcas de referência do segmento estão migrando e por quê). Nunca "porque é uma boa prática" sem nenhum lastro. Se for usar benchmark de mercado, é o mesmo cuidado do Passo 1: precisa ser uma leitura real, não um achismo genérico.
- **A rastreabilidade entre Plano de Ação e Metas é pelo nome da tag**, não pela ordem das seções — a categoria citada na tag de cada ação (ex: "Crescimento de seguidores") precisa reaparecer como label de uma meta.
- **Riscos com tag "Alto" (`.tag.danger`) só quando for real.** É a única tag que usa a cor de alarme (`--danger`, coral) em vez do dourado padrão — se tudo é urgente, nada é urgente, então use com critério.
- **Não invente dado.** Se faltar número, pergunte ou omita o elemento — nunca preencha com estimativa sem sinalizar.
- **Sem dados pessoais sensíveis.** Não inclua credenciais, tokens ou URLs privadas no HTML.
- **Design System V4 (Red Command Center).** Fundo em gradiente vermelho/marrom, dourado (`--accent-gold`) como cor de destaque em labels/números/bordas, cards sempre em glass morphism (`border` + gradiente translúcido + `backdrop-filter: blur`). Não improvise paleta nova — os tokens já estão prontos no CSS.

---

## Passo 4 — Salvar e entregar

Salve como `estrategia-quarter-{cliente}-{periodo}.html`, por exemplo `estrategia-quarter-metal-comercio-q3-2026.html`.

- Se estiver em contexto de cliente: salve em `squads/{squad}/clientes/{cliente}/checkins/`.
- Se não: pasta atual, ou pergunte onde salvar.

Informe o usuário: "Arquivo salvo em `{caminho}`. Abre direto no browser, navega com as setas, pontos ou teclado (← →). Não precisa de servidor — se quiser mandar link pro cliente, dá pra subir como deploy estático na Vercel."

### Reutilização

Esse arquivo é o molde do trimestre. No próximo quarter, duplique o HTML, renomeie pro novo período e edite os textos — a estrutura, o CSS e o JS de navegação continuam os mesmos. Ajuste só a quantidade de slides de Plano de Ação conforme o número real de ações daquele ciclo. Não recrie o deck do zero a cada ciclo.

---

## Conexão com outras skills

- **Antes:** se o usuário só tem dados soltos de performance, sugira primeiro `/account-checkin-resultados` ou `/geral-relatorio-v4` pra consolidar os números, e depois trazer pra cá.
- **Depois:** quando o plano de ação do próximo quarter estiver aprovado pelo cliente, oriente `/geral-plano-acao-social-media` pra detalhar o calendário editorial e a pauta de conteúdo mês a mês.
- **Antes de tudo isso existir:** se o cliente ainda não tem arquétipo, pilares e tom de voz definidos, a base estratégica vem de `/geral-estrategia-social-media`.
