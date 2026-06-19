---
name: geral-relatorio-v4
description: Gera relatórios executivos HTML completos seguindo o Design System V4 (Red Command Center) — tokens, componentes e linguagem editorial corretos, arquivo HTML pronto para abrir no browser. Use sempre que o usuário pedir relatório, report, diagnóstico, auditoria, análise executiva, dashboard, tabela de dados ou qualquer output visual em HTML para cliente ou gestão, mesmo que não cite "design system", "V4" ou "template" explicitamente. Também use quando o usuário compartilhar dados brutos e pedir pra "montar algo visual" ou "transformar em relatório".
area: geral
author: bhrendacruz-bot
version: 1.0.0
---

# Gerador de Relatório Executivo V4

Você vai gerar um arquivo HTML completo seguindo o Design System V4 (**Red Command Center**). O output deve ser um arquivo pronto para abrir direto no browser, sem dependências externas — CSS inline, sem links para arquivos locais.

Repositório oficial do design system: https://github.com/guilhermeduarte-billions/v4-design-system

---

## Passo 1 — Entender o pedido

Antes de gerar qualquer código, levante o que não foi dito:

- **Dados/conteúdo:** quais números, tabelas, listas ou insights o relatório precisa mostrar?
- **Cliente ou área:** qual o recorte? (ex: "Billions", "Coordenação Ariel", "Q2 2026")
- **Período:** qual o recorte temporal?
- **Conclusão principal:** o que o leitor precisa decidir ou entender depois de ler?
- **Seções necessárias:** de-para, pendências por responsável, tabelas operacionais?

Se o usuário já colou os dados, extraia essas respostas diretamente. Não pergunte o que já está ali.

---

## Passo 2 — Escolher o preset

| Situação | Preset |
|---|---|
| Relatório, auditoria, diagnóstico, tabela, análise, documento para mandar | **HTML estático** (único arquivo) |
| Dashboard vivo, simulador, dinâmica, weekly interativa, componentes com estado | **TypeScript/Vite** |

Na dúvida, use HTML estático. É mais simples de entregar.

---

## Passo 3 — Gerar o HTML

### Estrutura obrigatória

Todo relatório V4 segue essa ordem:

1. **Header sticky** — logo V4 + âncoras de navegação
2. **Hero em duas colunas** — conclusão executiva + veredito numérico
3. **Cards métricos** (4 no máximo) — placar de leitura rápida
4. **Callout executivo** — mensagem que precisa virar ação
5. **Seções operacionais** — tabelas de-para, listas por coordenação/responsável
6. **Método e fontes** — no final

Use só as seções que fizerem sentido para os dados do usuário. Não crie seção sem conteúdo real.

### CSS — embed completo (sempre inline)

Cole o CSS abaixo no `<style>` do `<head>`. Não referencie arquivos externos.

```css
:root {
  --bg-base: #FF2A1A;
  --bg-depth: #3B0000;
  --bg-deep-red: #A10F14;
  --text-primary: #FFFFFF;
  --text-muted: rgba(255,255,255,0.72);
  --accent-gold: #FFD48A;
  --accent-yellow: #FFF200;
  --surface-glass: rgba(255,255,255,0.12);
  --surface-glass-soft: rgba(255,255,255,0.08);
  --surface-glass-strong: rgba(255,255,255,0.18);
  --line: rgba(255,255,255,0.14);
  --safe: #63D471;
  --care: #FFD166;
  --danger: #FF8A80;
  --shadow: 0 18px 50px rgba(18,0,0,0.28);
  --blur: 18px;
  --radius-card: 28px;
  --radius-table: 18px;
  --radius-pill: 999px;
}
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; background: var(--bg-depth); }
body {
  margin: 0; min-height: 100vh;
  color: var(--text-primary);
  font-family: "IBM Plex Sans", sans-serif;
  font-weight: 500;
  background:
    radial-gradient(circle at 18% 10%, rgba(255,242,0,0.22), transparent 24rem),
    radial-gradient(circle at 88% 18%, rgba(255,212,138,0.16), transparent 20rem),
    linear-gradient(145deg, var(--bg-base) 0%, var(--bg-deep-red) 42%, var(--bg-depth) 100%);
  overflow-x: hidden;
}
body::before {
  content: ""; position: fixed; inset: 0; pointer-events: none; opacity: 0.22;
  background-image: linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.08) 1px, transparent 1px);
  background-size: 54px 54px;
  mask-image: linear-gradient(to bottom, black, transparent 78%);
}
a { color: inherit; text-decoration: none; }
img { max-width: 100%; display: block; }
.topbar {
  position: sticky; top: 0; z-index: 10;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
  padding: 14px clamp(18px,4vw,52px);
  background: rgba(59,0,0,0.58);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(var(--blur));
}
.brand { display: flex; align-items: center; gap: 12px; min-width: max-content; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-gold); font-size: 12px; font-weight: 700; }
.brand-mark { display: inline-flex; align-items: center; justify-content: center; width: 126px; height: 36px; background: transparent; }
.nav-pills { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }
.nav-pills a, .pill { display: inline-flex; align-items: center; gap: 8px; padding: 9px 13px; border-radius: var(--radius-pill); border: 1px solid var(--line); background: var(--surface-glass-soft); color: var(--text-primary); font-size: 12px; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }
.report-shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 52px 0 76px; }
.hero { display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 28px; align-items: stretch; margin-bottom: 28px; }
.hero-card, .glass { border: 1px solid var(--line); background: linear-gradient(135deg, var(--surface-glass-strong), var(--surface-glass-soft)); border-radius: var(--radius-card); box-shadow: var(--shadow); backdrop-filter: blur(var(--blur)); }
.hero-card { position: relative; overflow: hidden; padding: clamp(28px,5vw,54px); }
.hero-watermark::after { content: attr(data-watermark); position: absolute; right: -18px; bottom: -48px; font-size: clamp(92px,18vw,220px); font-weight: 700; font-stretch: 75%; letter-spacing: -0.12em; color: rgba(255,255,255,0.08); line-height: 0.9; }
.eyebrow { color: var(--accent-gold); font-size: 12px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 18px; }
h1, h2, h3, .metric-number { margin: 0; font-family: "IBM Plex Sans", sans-serif; font-weight: 700; font-stretch: 75%; letter-spacing: -0.055em; }
h1 { max-width: 780px; font-size: clamp(36px,7vw,76px); line-height: 0.92; }
h2 { font-size: clamp(30px,5vw,54px); line-height: 0.98; }
h3 { font-size: 30px; line-height: 1; }
.hero p, .section-head p, .muted { color: var(--text-muted); }
.hero p { position: relative; z-index: 1; max-width: 760px; margin: 22px 0 0; font-size: 19px; line-height: 1.45; }
.verdict { display: flex; flex-direction: column; justify-content: space-between; gap: 18px; padding: 28px; }
.verdict strong { display: block; color: var(--accent-yellow); font-size: clamp(42px,7vw,86px); line-height: 0.86; font-weight: 700; font-stretch: 75%; letter-spacing: -0.08em; }
.cards { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 14px; margin: 18px 0 28px; }
.metric { padding: 22px; border: 1px solid var(--line); border-radius: var(--radius-card); background: var(--surface-glass); box-shadow: var(--shadow); backdrop-filter: blur(var(--blur)); }
.metric-label { color: var(--accent-gold); font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; }
.metric-number { margin-top: 12px; font-size: clamp(36px,6vw,64px); line-height: 0.92; }
.metric small { display: block; margin-top: 12px; color: var(--text-muted); font-size: 13px; line-height: 1.4; }
section { scroll-margin-top: 92px; margin-top: 26px; }
.section-head { display: flex; justify-content: space-between; align-items: end; gap: 18px; margin-bottom: 14px; }
.section-head p { max-width: 580px; margin: 8px 0 0; font-size: 14px; line-height: 1.45; }
.callout { padding: 24px; border: 1px solid rgba(255,138,128,0.44); border-radius: var(--radius-card); background: linear-gradient(135deg,rgba(255,138,128,0.2),rgba(59,0,0,0.34)); box-shadow: var(--shadow); }
.table-card { overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius-table); background: rgba(59,0,0,0.26); box-shadow: var(--shadow); backdrop-filter: blur(var(--blur)); }
table { width: 100%; border-collapse: collapse; font-size: 14px; }
th, td { padding: 14px 16px; text-align: left; border-bottom: 1px solid var(--line); vertical-align: top; }
th { color: var(--accent-gold); font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; background: rgba(59,0,0,0.26); }
tr:last-child td { border-bottom: 0; }
td:first-child { font-weight: 700; }
.delta-up, .safe { color: var(--safe); font-weight: 700; }
.care { color: var(--care); font-weight: 700; }
.danger { color: var(--danger); font-weight: 700; }
.gold { color: var(--accent-gold); }
details { border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,0.08); overflow: hidden; }
details + details { margin-top: 10px; }
summary { cursor: pointer; padding: 16px 18px; color: var(--accent-gold); font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; list-style: none; }
summary::-webkit-details-marker { display: none; }
.list { display: grid; gap: 8px; padding: 0 18px 18px; color: var(--text-muted); font-size: 14px; line-height: 1.42; }
.item { display: grid; grid-template-columns: 1fr auto; gap: 12px; align-items: center; padding: 11px 12px; border-radius: 14px; background: rgba(59,0,0,0.24); border: 1px solid rgba(255,255,255,0.08); }
.tag { display: inline-flex; align-items: center; justify-content: center; min-width: max-content; padding: 6px 9px; border-radius: var(--radius-pill); border: 1px solid var(--line); color: var(--text-primary); font-size: 11px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; background: rgba(255,255,255,0.1); }
.tag.good { color: var(--safe); }
.tag.bad { color: var(--danger); }
@media (max-width: 900px) {
  .hero, .cards { grid-template-columns: 1fr; }
  .topbar { align-items: flex-start; flex-direction: column; }
  .nav-pills { justify-content: flex-start; }
  .section-head { align-items: flex-start; flex-direction: column; }
  table { min-width: 760px; }
  .table-card { overflow-x: auto; }
  .item { grid-template-columns: 1fr; }
}
```

### Logo V4 — usar SVG inline

Para o relatório ser independente, use a logo V4 como SVG inline no header (não como `<img src="...">`). O SVG oficial da logo branca está disponível no repositório: `assets/v4-company-logo-branca-oficial.svg`. Ou use o placeholder abaixo com o nome da marca em texto até o usuário fornecer o SVG:

```html
<div class="brand">
  <span style="font-size:16px; font-weight:900; color:#FFD48A; letter-spacing:-0.03em;">V4</span>
  Nome do relatório
</div>
```

Se o usuário tiver acesso ao repositório do design system, instrua a copiar o SVG para a pasta do projeto e referenciar como `./assets/v4-company-logo-branca-oficial.svg`.

### Font — Google Fonts no `<head>`

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wdth,wght@75..100,500;75..100,700&display=swap" rel="stylesheet">
```

---

## Regras de conteúdo — não pule

**Título do hero:** Nome o recorte real. Não use título genérico.
- Bom: "Análise de Healthscore — Billions · Maio 2026"
- Ruim: "Dashboard de acompanhamento"

**Subtítulo/parágrafo do hero:** A conclusão vai aqui, não no título. O título localiza; o parágrafo decide.

**Veredito:** Um número ou status que o leitor entende em 3 segundos.

**Cards:** Máximo 4. Número grande, label dourado, leitura curta embaixo.

**Callout:** Só uma mensagem por relatório. A que mais precisa virar ação.

**Cores semânticas:**
- `safe` (verde) → avanço real, meta batida
- `care` (amarelo) → atenção, risco moderado
- `danger` (vermelho claro) → gap real, pendência crítica, queda

Não use `danger` para tudo. Se tudo é urgente, nada é urgente.

**Details/toggle:** Use para listas longas por coordenação, responsável ou dimensão. Não abra tudo por padrão se houver mais de 3 grupos.

---

## Entrega

Salve o arquivo como `relatorio-[cliente-ou-tema]-[periodo].html` na pasta do projeto do usuário. Se não tiver pasta definida, pergunte onde salvar ou salve na pasta atual.

Informe o usuário: "Arquivo salvo em `[caminho]`. Abra direto no browser — não precisa de servidor."

---

## Exemplo de estrutura HTML mínima

```html
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Análise de [tema] — [cliente]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wdth,wght@75..100,500;75..100,700&display=swap" rel="stylesheet">
  <style>
    /* [cole o CSS completo aqui] */
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <!-- logo SVG inline ou texto -->
      Nome do relatório
    </div>
    <nav class="nav-pills">
      <a href="#geral">Geral</a>
      <!-- âncoras para as seções existentes -->
    </nav>
  </header>

  <main class="report-shell">
    <!-- 1. Hero -->
    <section class="hero" id="geral">
      <div class="hero-card hero-watermark" data-watermark="V4">
        <div class="eyebrow">Recorte · Período</div>
        <h1>Análise de [tema] — [cliente ou área].</h1>
        <p>A leitura principal: o que os dados mostram e qual decisão precisam orientar.</p>
      </div>
      <aside class="verdict glass">
        <div>
          <div class="eyebrow">Veredito executivo</div>
          <strong>[número ou status]</strong>
          <span>Contexto do veredito.</span>
        </div>
        <div class="pill">Status atual</div>
      </aside>
    </section>

    <!-- 2. Cards -->
    <div class="cards">
      <div class="metric">
        <div class="metric-label">Label</div>
        <div class="metric-number">42</div>
        <small>Leitura curta.</small>
      </div>
      <!-- repita até 4 -->
    </div>

    <!-- 3. Callout -->
    <section class="callout">
      <div class="eyebrow">Mensagem para gestão</div>
      <h2>O insight que precisa virar ação.</h2>
      <p>Direto: o que está acontecendo e o que precisa mudar.</p>
    </section>

    <!-- 4. Seções operacionais (adapte ao conteúdo) -->

    <!-- 5. Método -->
    <section id="metodo">
      <div class="section-head">
        <div><div class="eyebrow">Método</div><h2>Como essa leitura foi feita.</h2></div>
      </div>
      <div class="table-card">
        <table>
          <tbody>
            <tr><td>Fonte</td><td class="muted">Fonte, recorte, data e limitações.</td></tr>
          </tbody>
        </table>
      </div>
    </section>
  </main>
</body>
</html>
```
