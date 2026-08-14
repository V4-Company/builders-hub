# Checklist Completo de CRO para Landing Pages de PMEs Brasileiras

## Como usar este checklist

Use este checklist como referencia ao auditar landing pages. Nem todos os itens se aplicam a todos os casos — priorize os que tem maior impacto para o segmento e ICP do cliente.

A auditoria segue 5 dimensoes:
1. Performance tecnica
2. Above the fold (hero)
3. Estrutura e conteudo
4. Confianca e credibilidade
5. Mobile e UX

---

## 1. Performance Tecnica

### Core Web Vitals

| Metrica | Bom | Medio | Ruim | Impacto |
|---------|-----|-------|------|---------|
| LCP (Largest Contentful Paint) | <2.5s | 2.5-4s | >4s | Cada segundo extra = -7% conversao |
| CLS (Cumulative Layout Shift) | <0.1 | 0.1-0.25 | >0.25 | Layout pulando = visitante sai |
| INP (Interaction to Next Paint) | <200ms | 200-500ms | >500ms | Clique sem resposta = frustracao |

### PageSpeed Score

| Score | Classificacao | Acao |
|-------|--------------|------|
| 90-100 | Excelente | Manter e monitorar |
| 50-89 | Medio | Otimizar (imagens, JS, CSS) |
| 0-49 | Ruim | Refazer ou otimizacao urgente |

### Checklist tecnico

```
[ ] PageSpeed mobile >= 50 (idealmente >= 70)
[ ] PageSpeed desktop >= 70 (idealmente >= 90)
[ ] LCP < 2.5 segundos
[ ] CLS < 0.1
[ ] SSL (HTTPS) ativo
[ ] Sem erros 404 ou redirects desnecessarios
[ ] Imagens otimizadas (WebP, lazy loading)
[ ] Sem JavaScript blocante na renderizacao
[ ] Fonts carregando rapido (preload ou system fonts)
[ ] Meta tags basicas (title, description, og:image)
[ ] Mobile responsive (nao apenas "funciona" — "fica bom")
[ ] Formulario funcional (testado — envia de verdade)
[ ] Tracking instalado (GA4, Pixel Meta, Tag Manager)
```

### Causas comuns de lentidao em LPs de PMEs

1. **Imagens nao otimizadas** — JPGs de 3MB direto da camera. Solucao: WebP, max 200KB, lazy load
2. **Slider/carrossel pesado** — Plugins de carrossel com JS pesado. Solucao: imagem estatica ou CSS puro
3. **Fonts externas** — Google Fonts sem preload. Solucao: preload ou hospedar localmente
4. **WordPress com 30 plugins** — Cada plugin adiciona JS/CSS. Solucao: remover nao essenciais
5. **Video autoplay** — Video pesado carregando no hero. Solucao: thumbnail + play on click
6. **Hosting ruim** — Shared hosting lento. Solucao: Vercel, Netlify, ou VPS
7. **Chat widgets** — Tawk.to, Intercom carregando JS pesado. Solucao: lazy load ou remover
8. **Animations pesadas** — CSS/JS animations que causam repaints. Solucao: transform/opacity only

---

## 2. Above the Fold (Hero)

O hero e responsavel por 80% da decisao de ficar ou sair. A regra e: em 5 segundos, o visitante precisa saber O QUE e, PARA QUEM e, e O QUE FAZER.

### Checklist do hero

```
[ ] Headline clara (responde "o que + para quem + beneficio")
[ ] Sub-headline que complementa (nao repete)
[ ] CTA visivel sem rolar (botao, nao link)
[ ] CTA com texto acionavel ("Agendar consulta gratis" > "Saiba mais")
[ ] Elemento visual relevante (foto real, nao stock generico)
[ ] Prova social rapida (estrelas, numero de clientes, selo)
[ ] Sem excesso de informacao (max 3 elementos de texto)
[ ] Contraste suficiente entre texto e fundo
[ ] Mobile: tudo acima da dobra em tela de 375px
```

### Erros fatais no hero

| Erro | Por que e fatal | Solucao |
|------|----------------|---------|
| Headline generica ("Bem-vindo") | Nao diz o que faz nem para quem | PUV como headline |
| Slider/carrossel no hero | Ninguem le alem do primeiro slide | Imagem unica com mensagem clara |
| Video autoplay com som | Irrita e faz o visitante fechar | Video mudo ou thumbnail |
| CTA abaixo da dobra | Quem nao rola nunca ve | CTA no hero, sempre |
| Formulario longo no hero | Gera atrito antes de gerar interesse | Formulario curto (nome + telefone) ou CTA para WhatsApp |

### Headlines que convertem (formulas)

1. **Resultado direto:** "[Resultado] para [ICP] em [prazo]"
   Ex: "30+ leads qualificados por mes para clinicas de estetica"

2. **Dor → Solucao:** "Cansou de [dor]? [Solucao] sem [objecao]"
   Ex: "Cansou de gastar com anuncio sem retorno? Performance real sem contrato de fidelidade"

3. **PUV direta:** "[O que faz] de um jeito [como ninguem faz]"
   Ex: "Implante dental em sessao unica com sedacao — sem medo, sem espera"

4. **Especializacao:** "[Servico] para [nicho especifico]"
   Ex: "Contabilidade exclusiva para e-commerces que faturam R$ 50K-2M/mes"

---

## 3. Estrutura e Conteudo

### Ordem recomendada de secoes

A ordem importa. Cada secao leva o visitante um passo mais perto da conversao.

| # | Secao | Objetivo | Se nao tiver |
|---|-------|----------|--------------|
| 1 | Hero (PUV + CTA) | Captar atencao, dizer o que e | Visitante sai em 5s |
| 2 | Problema/dor | Gerar identificacao ("voce tambem?") | Visitante nao se conecta |
| 3 | Solucao | Mostrar como resolve | Visitante nao entende o valor |
| 4 | Como funciona | Reduzir incerteza (passo a passo) | Visitante tem medo de contratar |
| 5 | Prova social | Gerar confianca (outros ja fizeram) | Visitante nao acredita |
| 6 | Beneficios / diferenciais | Reforcar por que voce e diferente | Visitante compara com concorrente |
| 7 | FAQ | Eliminar objecoes | Visitante sai com dúvida |
| 8 | CTA final | Fechar a conversao | Visitante nao converte |

### Checklist por secao

**Secao Problema/Dor:**
```
[ ] Descreve a dor com palavras do ICP (nao jargao)
[ ] Gera identificacao ("voce ja passou por isso?")
[ ] Nao e exagerada (nao parece manipulacao)
[ ] Conecta com a solucao que vem a seguir
```

**Secao Solucao:**
```
[ ] Mostra o "o que" e o "como" (nao so features)
[ ] Foca em transformacao (antes → depois)
[ ] Usa imagem/video do produto/servico real
[ ] Conecta com a PUV
```

**Secao Como Funciona:**
```
[ ] 3-5 passos simples (nao 10)
[ ] Cada passo cabe em 1 frase
[ ] Mostra que e facil comecar
[ ] Ultimo passo = resultado positivo
```

**Secao Prova Social:**
```
[ ] Depoimentos com nome + foto + cargo/empresa (nao anonimo)
[ ] Depoimentos especificos (mencionam resultado, nao "otimo servico")
[ ] Numero de clientes/projetos/avaliacoes
[ ] Se possivel, video de depoimento
[ ] Se tiver logos de clientes, sao reconheciveis pelo ICP
```

**FAQ:**
```
[ ] 3-5 perguntas (nao 20)
[ ] Inclui objecoes de venda (preco, prazo, garantia)
[ ] Respostas curtas e diretas
[ ] Usa linguagem do ICP
```

---

## 4. Confianca e Credibilidade

Para PMEs, confianca e o maior obstaculo de conversao. O visitante nao conhece a marca e precisa de sinais de que e seguro.

### Hierarquia de sinais de confianca (do mais forte ao mais fraco)

1. **Depoimentos com video** — Mais dificil de falsificar
2. **Avaliacoes Google (link para Google Meu Negocio)** — Verificavel
3. **Depoimentos com nome + foto + empresa** — Crivel
4. **Logos de clientes conhecidos** — Transferencia de confianca
5. **Selos e certificacoes** (ISO, CRO, OAB, etc.) — Autoridade
6. **Numero de clientes / projetos** — Prova de volume
7. **CNPJ e endereco** — Empresa real
8. **Politica de privacidade** — Profissionalismo
9. **Garantia explicita** — Reduz risco percebido
10. **SSL (cadeado)** — Basico, mas ausencia e fatal

### Score de confianca

| Score | Descricao | Conversao tipica |
|-------|-----------|-----------------|
| 1-3 | Sem sinais de confianca. Parece golpe. | <1% |
| 4-5 | Sinais basicos (CNPJ, SSL). Pouco profissional. | 1-3% |
| 6-7 | Profissional. Depoimentos e prova social. | 3-8% |
| 8-9 | Forte confianca. Video, reviews, garantia. | 8-15% |
| 10 | Confianca maxima. Marca conhecida, prova abundante. | 15%+ |

---

## 5. Mobile e UX

### Estatisticas que importam
- 75-85% do trafego de Meta Ads em PMEs brasileiras e mobile
- Se a LP nao funciona em mobile, voce perde 3/4 do investimento
- Visitante mobile tem menos paciencia (thumb scroll rapido)

### Checklist mobile

```
[ ] Layout 100% responsivo (nao apenas "encolhido")
[ ] Texto legivel sem zoom (min 16px)
[ ] Botoes grandes o suficiente para polegar (min 44x44px)
[ ] CTA fixo na tela (sticky button) ou facilmente acessivel
[ ] Formulario simples (max 3 campos em mobile)
[ ] Nao tem popup que bloqueia a tela inteira em mobile
[ ] Imagens redimensionadas para mobile (nao carrega desktop-size)
[ ] WhatsApp link funciona (abre o app diretamente)
[ ] Telefone clicavel (tel: link)
[ ] Scroll suave (sem travamentos)
```

### Erros de UX mais comuns em LPs de PMEs

1. **Formulario longo** — Nome, email, telefone, cidade, como conheceu, mensagem. Solucao: nome + telefone (ou so WhatsApp)
2. **CTA generico** — "Enviar" em vez de "Agendar minha consulta gratis"
3. **Multiplos CTAs conflitantes** — "Agendar" + "Ver precos" + "Baixar e-book" + "Seguir no Instagram". Solucao: 1 CTA principal
4. **Informacao demais** — Pagina com 10 secoes e 5000 palavras. Solucao: cortar pela metade
5. **Pop-up agressivo** — Abre antes do visitante ler qualquer coisa. Solucao: exit intent ou scroll-trigger
6. **Sem WhatsApp** — PME brasileira sem WhatsApp e como loja sem porta. Obrigatorio.
7. **Fundo escuro com texto claro** — Cansa a leitura em scroll longo. Solucao: fundo claro, texto escuro
8. **Auto-play de audio/video** — Irrita e faz fechar. Solucao: mudo ou click-to-play

---

## Priorizacao de melhorias (ICE Framework)

Para priorizar hipoteses de teste, use o framework ICE:

| Criterio | Descricao | Score 1-5 |
|----------|-----------|-----------|
| **Impact** | Quanto impacto na conversao se funcionar? | 1 (minimo) - 5 (enorme) |
| **Confidence** | Quao confiante estou que vai funcionar? | 1 (chute) - 5 (certeza) |
| **Ease** | Quao facil e implementar? | 1 (dificil) - 5 (trivial) |

**Score ICE = (I + C + E) / 3**

**Priorizacao:**
- ICE >= 4.0 → P1 (fazer primeiro)
- ICE 3.0-3.9 → P2 (fazer depois)
- ICE < 3.0 → P3 (backlog)

### Melhorias de alto impacto (quase sempre P1)

1. **Reescrever headline do hero** (I:5, C:4, E:5 = 4.7)
2. **Mudar texto do CTA** (I:4, C:4, E:5 = 4.3)
3. **Adicionar prova social no hero** (I:4, C:4, E:4 = 4.0)
4. **Reduzir campos do formulario** (I:4, C:5, E:5 = 4.7)
5. **Adicionar WhatsApp flutuante** (I:4, C:4, E:5 = 4.3)

### Melhorias de medio impacto (geralmente P2)

1. **Otimizar PageSpeed** (I:3, C:4, E:3 = 3.3)
2. **Adicionar secao FAQ** (I:3, C:3, E:4 = 3.3)
3. **Melhorar depoimentos** (I:3, C:3, E:3 = 3.0)
4. **Adicionar secao "como funciona"** (I:3, C:3, E:3 = 3.0)
5. **Exit intent popup** (I:3, C:3, E:4 = 3.3)

---

## Benchmarks de conversao por tipo de LP

| Tipo de LP | Conversao mediana | Boa | Excelente |
|---|---|---|---|
| Lead gen B2B (formulario) | 3-5% | 5-10% | 10-15% |
| Lead gen B2C (formulario) | 5-10% | 10-20% | 20%+ |
| Lead gen (WhatsApp CTA) | 8-15% | 15-25% | 25%+ |
| E-commerce (produto) | 1-2% | 2-4% | 4%+ |
| Agendamento online | 5-10% | 10-20% | 20%+ |
| Download de material | 15-25% | 25-40% | 40%+ |

**NOTA:** CTA de WhatsApp geralmente converte 2-3x mais que formulario para PMEs brasileiras. O atrito e muito menor (1 clique vs preencher campos).
