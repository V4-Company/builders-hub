---
name: criativo-construtor-de-site
description: Constrói um site de marketing completo e de alta qualidade para um cliente de qualquer nicho — da coleta de conteúdo real e definição de escopo até a validação por screenshot, iterando contra um dev server. Use sempre que o usuário quiser criar, refazer, montar ou "subir" um site, landing page, one-page, hotsite ou presença web para um cliente, negócio ou projeto, mesmo que ele só diga "faz um site pra X", "refaz o site da empresa Y", "preciso de uma página pro meu produto" ou descreva um nicho querendo site. Orquestra a skill ui-ux-pro-max e usa Vite + React + TypeScript + Tailwind + Framer Motion + react-router.
area: criativo
author: esdras-onlaine
version: 1.2.0
---

# Construtor de Site

Constrói um site de marketing completo para um cliente de **qualquer nicho**, com processo repetível e barra de qualidade fixa — sem clonar o visual de nenhum cliente anterior.

A skill **não reinventa design** (orquestra a `ui-ux-pro-max`) e mantém consistência via **arquivos de contexto do projeto**: grava o conteúdo real e o design-system em `dados-reais.md` + `design-system.md` (e um `CLAUDE.md` enxuto no root do site), pra dar as regras **uma vez** e o agente aplicar em todas as páginas — sem re-perguntar a cada seção.

**Stack travada:** Vite + React + TypeScript + Tailwind v3 + **Framer Motion** (`motion`) + **react-router-dom** (multipágina) + `lucide-react`. O que muda por cliente é a marca, o conteúdo, o escopo e as seções; a stack não.

## Pré-requisitos (skills)

Esta skill **orquestra**, não reimplementa design. Antes de usar, garanta que estas skills estão no ambiente:

- **`ui-ux-pro-max`** — **obrigatória**. É ela que define o sistema de design (estilo, paleta OKLCH, par de fontes, padrões de UX) no passo 3, via `search.py --design-system`. **Não faz parte do Builders Hub** — instale à parte a partir do marketplace de skills. Sem ela, o passo de marca não roda.
- **`frontend-design`** — **já incluída no hub** (skill base). Usada só pra um componente isolado genuinamente novo; não precisa instalar à parte.
- **`deploy-to-vercel`** — **opcional**, só pro deploy final (passo 7). Também vem de fora do hub.

## Quando usar
- "Faz um site pra [negócio]", "refaz o site da [empresa]", "preciso de uma landing pro [produto]".
- Refatorar/redesenhar um site existente de um cliente.

## Quando NÃO usar
- Só auditoria de UX de algo pronto → `ui-ux-pro-max`. Componente isolado → `frontend-design`. App com backend/auth/dashboard → é produto, não site de marketing.

---

## Pré-voo (cheque antes de começar)
Confirme o que está disponível e tenha plano B — **não trave no meio**:
- **Firecrawl** (raspar site/redes atuais): se indisponível, peça o conteúdo e as fotos ao usuário.
- **Playwright MCP** (screenshots de validação): se indisponível, peça pro usuário olhar a tela e descrever.
- **Pillow (Python)** e **Node**: necessários pra imagens e build; se faltar, instale/avise.

## Ferramentas que a skill orquestra

| Etapa | Ferramenta | Pra quê |
|---|---|---|
| Coletar | **Firecrawl** (`firecrawl_map` → `firecrawl_scrape` **seletivo**) | Mapear o site atual e raspar **só** as páginas que definem arquitetura + as com assets — não tudo |
| Coletar | **Read** (docs/PDF/planilhas) | Material enviado: briefing, portfólio, catálogo |
| Coletar | **WebSearch** / `firecrawl_search` | Fatos reais do nicho/local **com fonte** quando o material é raso — nunca inventar |
| Definir | **AskUserQuestion** | Fechar tipo/escopo de entrega e aprovar arquitetura/garfos com opções (preview) |
| Contexto | **Arquivos do projeto** (`dados-reais.md`, `design-system.md`, `CLAUDE.md`) | Persistir conteúdo + regras de design; o agente lê e fica consistente sem re-perguntar |
| Curar/otimizar fotos | **Pillow** (folha de contato + **batch** WebP) | Identificar fotos; converter em lote pra WebP |
| Marca | **`ui-ux-pro-max`** (`search.py --design-system`) | **Um passe** de estilo/paleta/tipografia/UX |
| Construir | **Vite + React + TS + Tailwind + Framer Motion + react-router + lucide** | Site multipágina, animações/reveals, rotas |
| Iterar/validar | **`npm run dev` (HMR)** + **Playwright** (screenshot **cirúrgico**) | Iterar em segundos; screenshot só do que mudou |
| Entregar | **PowerShell/Bash**; `deploy-to-vercel` | `build`+`preview` no final; deploy opcional |
| (opcional) Escalar | **subagents** | Construir páginas independentes em paralelo num site grande |

---

## Princípios inegociáveis

1. **Feche o TIPO e o ESCOPO da entrega ANTES de construir.** "Faz um site pra X" não é one-page. Padrão p/ cliente contratado = **site institucional multipágina**. Analise, recomende, e **pergunte o que foi combinado comercialmente / a expectativa** — a skill não infere isso. (Erro nº 1 num build real: saiu LP no lugar de site.)
2. **Conteúdo real, nunca inventar.** Vem do cliente (KB, material, site/redes). Faltou contexto do nicho → **pesquise e cite a fonte**. Sem dado → pendência declarada. Demos (inclusive de ChatGPT) servem só de estrutura.
3. **Contexto em arquivo, não na cabeça.** Grave o conteúdo em `dados-reais.md` e o design em `design-system.md` (+ `CLAUDE.md` enxuto, ~100 linhas). Assim você define as regras **uma vez** e não re-pergunta design a cada seção. Mantenha enxuto (evita "context rot").
4. **Nada de placeholder em produção.** Falta foto → estado "Foto em breve" desenhado + lista do que falta. Real do acervo > interina do acervo > placeholder declarado.
5. **Orquestre, não duplique.** Um passe de `ui-ux-pro-max` define o sistema; reconsulte só pra um **componente genuinamente novo**.
6. **Decisões de garfo são do usuário.** Bifurcações (tipo de entrega, paleta, navbar, blog) → **2–4 opções com preview** (AskUserQuestion). Se ele estiver, na sua leitura, errado, **questione com argumento**.
7. **Itere contra o dev server.** Construa com **`npm run dev` (HMR)** — segundos por mudança. `build`+`preview` é só pra **validação final / compartilhar / deploy** (e evita o estouro de memória do rolldown que vem do rebuild a cada troca).
8. **Screenshot é caro — use cirúrgico.** Valide com Playwright **só a página/seção que mudou**; varredura completa (desktop 1440 + mobile 375) só num **marco de review**.
9. **Checkpoints certos.** Obrigatórios: escopo (GATE), direção de marca, review final. O resto **agrupe** — construa um lote de páginas e revise junto; não peça aprovação por seção.
10. **Estude o site atual** (`firecrawl_map`) e derive a **arquitetura** — não achate em LP. Avise o **tamanho/esforço** depois de aprovar (ex.: "9 páginas + 40 obras = build grande").
11. **A11y e mobile desde o começo.** Foco de teclado, focus-trap em modal, `aria`, toque ≥44px, hover nunca como única via, teste 375px.
12. **Não trave o gosto de um cliente** e **otimize imagens** (WebP ~1600px/q82, `lazy`).

---

## Fluxo

### 1. Coletar (enxuto) → `dados-reais.md`
Read no material do cliente; `firecrawl_map` pra ver as páginas e `firecrawl_scrape` **seletivo** nas que importam (arquitetura + assets); WebSearch p/ fatos do nicho com fonte. **Consolide o conteúdo real em `dados-reais.md`** (enxuto). Se o Firecrawl estiver fora, peça ao usuário.

### 2. Definir entrega + arquitetura (GATE — não pule)
Apresente análise e **peça aprovação** antes de codar: tipo de entrega (padrão multipágina; **pergunte o combinado**), mapa de páginas derivado do site atual + objetivo, e o **porquê**. Use AskUserQuestion se houver alternativas. Aprovado → diga o tamanho/esforço.

### 3. Marca → `design-system.md` (um passe)
Invoque `ui-ux-pro-max` → estilo + paleta (OKLCH) + par de fontes. **Grave em `design-system.md`** (tokens + padrões de seção) e materialize no `index.css`/`tailwind.config`. Itere cor/fonte com o usuário (é garfo). Daqui pra frente, construa a partir desse arquivo.

### 4. Scaffold + dev server
Vite+React+TS, Tailwind v3, `motion`, `react-router-dom` (rotas aprovadas), `lucide-react`. Suba **`npm run dev`** e itere contra ele.

### 5. Construir (em lote, do design-system)
Página a página / seção a seção, lendo `design-system.md` (não re-perguntando à ui-ux-pro-max). Folha de contato pra curar fotos; **converta em batch** pra WebP. Garfos → opções com preview. Blog/artigo = **padrão editorial** (~68ch). Em site grande, páginas independentes podem ir pra **subagents** em paralelo.

### 6. Validar e iterar (cirúrgico)
HMR mostra na hora; **screenshot só do que mudou** (truque: desligar animação + rolar pra disparar reveals) → auditoria a11y/mobile → mostra um **lote** ao usuário → ajusta.

### 7. Entregar
**Aí sim** `npm run build` + `preview` (`--host` libera na rede). Deploy (Vercel + rewrite SPA) opcional. Declare o que é WIP.

---

## Playbook de arquitetura por objetivo

A **hero + prova social + CTA + rodapé** são quase universais; o miolo muda. Em multipágina, cada bloco pode virar **página**.

| Objetivo | Páginas/seções | CTA |
|---|---|---|
| Lead B2B (serviço, indústria) | Home, A Empresa, **1 página por serviço**, Equipamentos, Cases/Obras (filtrável), Trabalhe Conosco, Contato | Solicitar orçamento |
| Reserva (hotelaria, eventos) | Acomodações/ingressos, experiências, galeria, localização | Reservar |
| Trial (SaaS, app) | Features, como funciona, planos, FAQ | Começar grátis |
| Compra (e-commerce) | Produtos, benefícios, reviews, garantia | Comprar |
| Conteúdo (blog, mídia) | Destaque editorial, grade, newsletter | Assinar |

Sempre: prova social real, rodapé/contato completo, blog (editorial) se o cliente produz conteúdo. Form sem backend pode montar a mensagem e abrir o **WhatsApp** do cliente.

---

## Anti-padrões
- Achatar o site numa LP quando o combinado é multipágina; construir antes de aprovar escopo/arquitetura.
- **Iterar com `build`+`preview`** em vez de dev/HMR; **screenshotar tudo** a cada passo; re-perguntar design por seção.
- Inventar dado; placeholder/foto genérica como real; reescrever o que a `ui-ux-pro-max` já sabe; decidir garfo de gosto sozinho.
- Travar no meio quando um MCP cai (degrade — veja Pré-voo).

---

## Exemplo (build real, mineração B2B)
"Faz um site pra [empresa], objetivo orçamento; tenho uma demo do ChatGPT só de estrutura." → Read da demo + `firecrawl_map`/scrape seletivo do site atual + WebSearch dos termos técnicos; conteúdo real em `dados-reais.md`. **GATE:** "isso parece **site institucional multipágina**, não LP — o que foi combinado?" → confirma site completo; aprova arquitetura (Home, Empresa, 1 página/serviço, Equipamentos, Obras, Trabalhe Conosco, Contato) + esforço. `ui-ux-pro-max` → industrial bold em `design-system.md` (sem seguir a logo legada, decisão do usuário). Scaffold + `npm run dev`. Folha de contato + WebP batch; constrói em lote; form abre WhatsApp. Screenshot cirúrgico + auditoria → mostra lote → ajusta. No final, build+preview.

## Receitas concretas
Comandos em **`references/recipes.md`** (scaffold + dev server, tokens OKLCH, batch WebP, folha de contato, pesquisa de nicho, Firecrawl seletivo, screenshot cirúrgico, arquivos de contexto, build/preview, deploy SPA).
