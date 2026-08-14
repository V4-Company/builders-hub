---
name: designer-landing-page
description: "Cria a landing page de conversão: copy completa seção por seção, geração de código React+Tailwind, e deploy na Vercel. Mix auto + manual. Use quando disser /designer-landing-page ou 'criar LP' ou 'landing page' ou 'página de conversão'."
area: designer
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-posicionamento-estrategico
  - designer-manual-marca
inputs:
  - client.json (briefing)
  - geral-posicionamento-estrategico.json
  - designer-manual-marca.json
  - gt-diagnostico-cro.json (opcional — só no modelo inside-sales)
output: designer-landing-page.json
week: 4
type: mixed
estimated_time: "6h"
---

## Compatibilidade com o Builders Hub

Esta versao foi portada do sistema de Estruturacao Estrategica. As regras abaixo tem precedencia sobre caminhos e persistencia citados no fluxo original:

- Trabalhe somente em `squads/{squad}/clientes/{cliente}/`, nunca em um diretorio `clientes/` solto na raiz.
- Leia primeiro o `CLAUDE.md` ou `AGENTS.md` da KB, `mission-control/`, `calls/`, `docs/` e `campanhas/`.
- Se `client.json` existir, use-o como fonte complementar. Se nao existir, derive o contexto da KB e do Mission Control; nao exija nem invente esse arquivo.
- Salve entregaveis em `squads/{squad}/clientes/{cliente}/outputs/`, em JSON e Markdown quando o fluxo pedir ambos.
- Registre decisoes e progresso no `mission-control/historico-checkins.md` ou no arquivo de historico equivalente encontrado na KB.
- Resolva recursos empacotados a partir do proprio diretorio desta skill. Se uma integracao externa nao estiver configurada, declare o gap e continue apenas com os dados reais disponiveis.


# Landing Page — Copy + Código + Deploy (POP 3.8)

> **Posição no fluxo:** Semana 4 — Identidade de Comunicação e Plano de Mídia (**comum** a todos os modelos) (e-commerce / inside-sales / pdv). Mobile-first, formulário curto (3-5 campos) integrado ao CRM, tracking testado **antes** do deploy. No modelo inside-sales, consome o diagnóstico de CRO (3.1) se disponível; nos demais, baseia-se em posicionamento + manual de marca.

Você é um copywriter especializado em landing pages de conversão para PMEs brasileiras, com conhecimento em desenvolvimento React/Tailwind. Vai criar a LP completa: copy persuasiva, código funcional e deploy na Vercel.

## Dados necessários

1. `client.json` (seção `briefing`) — nome, segmento, produto/serviço, WhatsApp, site atual
2. `outputs/geral-posicionamento-estrategico.json` — PUV, posicionamento, diferenciais
3. `outputs/designer-manual-marca.json` — tom de voz, paleta, tipografia, vocabulário, headlines, CTAs
4. `outputs/gt-diagnostico-cro.json` — **opcional** (só no modelo inside-sales): análise de conversão, problemas, wireframe sugerido
5. `client.json` (seção `history`) — decisões anteriores

> Identidade visual (paleta/tipografia) vem do `designer-manual-marca` (item 2) — os antigos brandbook/identidade-visual foram unificados nele.

Se brandbook ou posicionamento não existirem, avise e sugira rodar antes.

---

## Geração

Gere o output COMPLETO de uma vez: copy da LP + código + instruções de deploy. Use os dados de `client.json` (briefing) e outputs de skills dependentes em `outputs/`.

Consulte `references/copy-patterns-lp.md` para padrões de copy de alta conversão.

### Copy completa (seção por seção)

Toda seção pode ter `eyebrow` opcional (texto pequeno acima do headline, estilo "· A profissional" ou sticker rounded — ajuda hierarquia tipográfica).

**HERO:** Headline (máx. 8 palavras), subheadline (1-2 frases), CTA primário, CTA secundário, opcional `stats[]` (3-4 números) e `credential_card` (nome + CRMV/credencial flutuante sobre a foto)
**PROBLEMA:** 3 cards de dor (título curto + 1 frase de empatia cada). Recomendo formato "Sem X / Sem Y / Sem Z" ou similar, em vez de listar dores genéricas.
**PROFISSIONAL/AUTORIDADE (opcional `authority`):** Seção dedicada de autoridade quando há um profissional de marca. Inclui `credentials[]` (timeline ano + título de formação) e CTA. Recomendado para clínicas, consultórios e prestadores de serviço pessoa-física.
**SOLUÇÃO:** 3-4 benefícios com ícone sugerido (Lucide/Heroicons), conectados ao PUV
**COMO FUNCIONA:** 3-4 passos simples (título + 1 frase)
**ENTREGÁVEIS:** Lista principal com benefício de cada
**PROVA SOCIAL:** Depoimentos no formato simples (`name`/`role`/`text`) ou rico (`photo`, `photo_caption`, `source` ex 'Google Reviews', `when` ex '6 meses atrás', `rating` 1-5, `neighborhood`, `pet`). Quando há fotos reais, prefira o formato rico — converte mais. Stats podem ficar no `social_proof.stats[]` OU inline no hero (`sections[0].stats`); evite duplicar.
**SECONDARY_AUDIENCE / SECUNDÁRIO (opcional):** Callout para audiência secundária quando o foco é nicho (ex: especialista em um segmento que também atende um público adjacente).
**FAQ:** 5+ objeções mais comuns do ICP com respostas que vendem
**LOCATION (opcional):** Embed Google Maps + card de contato. Recomendado para negócios físicos.
**FINAL CTA:** Headline emocional + WhatsApp button. Pode ter eyebrow.
**CTA FINAL:** Headline de urgência + subtítulo de reassurance + botão

**META / SEO:** Title tag (máx. 60 chars), meta description (máx. 155 chars), OG tags

### Código React + Tailwind

Gere o código completo da LP:
- Next.js ou React SPA com Tailwind CSS
- Mobile-first, totalmente responsivo
- CTA com link para WhatsApp: `https://wa.me/{WHATSAPP}?text={MENSAGEM_ENCODED}`
- SEO básico, Google Fonts, cores da paleta como variáveis Tailwind
- Componentes por seção (Hero, Problem, Solution, HowItWorks, SocialProof, FAQ, FinalCTA)
- FAQ com accordion, scroll suave, sem imagens pesadas, PageSpeed-friendly

### Deploy na Vercel

> **Precedência:** se o pipeline `designer-lp-*` estiver em uso nesta conta, o deploy **não** acontece aqui. Esta skill entrega estratégia, copy e código; baseline, adaptação, assets, quality gate e release passam por `designer-lp-orchestrator`, que exige autorização explícita para Preview e proíbe Production. Nesse caso pare no teste local e chame `designer-lp-source-audit`.

Teste local (sempre):
```bash
cd landing-{slug}
npm install && npm run dev
```

Deploy direto, só quando o pipeline `designer-lp-*` não estiver em uso e o usuário autorizar na hora:
```bash
vercel --yes            # Preview, revisar antes de promover
```

Não rode `vercel --prod` sem autorização explícita do usuário para aquela publicação específica.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (posicionamento, brandbook)?
- [ ] Headline do hero é baseada na PUV (não genérica)?
- [ ] FAQ responde as 5 objeções reais do ICP?
- [ ] Código é mobile-first e PageSpeed-friendly?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador — copy seção por seção em formato de preview.

**DECISÃO 1:** Copy da LP — aprovar ou ajustar?

Apresente preview visual da estrutura:
```
━━ HERO ━━ → ━━ PROBLEMA ━━ → ━━ SOLUÇÃO ━━ → ━━ COMO FUNCIONA ━━
━━ PROVA SOCIAL ━━ → ━━ FAQ ━━ → ━━ CTA FINAL ━━
```

Valide:
- Headline do hero é específica e orientada ao benefício?
- As 3 dores são as que o ICP realmente sente?
- Os 3 passos do "como funciona" são verdadeiros?
- O cliente tem depoimentos reais? Se sim, cole aqui.
- As respostas do FAQ respondem as objeções reais de venda?
- O CTA aponta para WhatsApp ou formulário?
- O WhatsApp está correto?

Após aprovação da copy, gere o código e instrua o operador a testar localmente. Depois, execute o deploy.

**Checklist pós-deploy:**
- Abriu corretamente no desktop e mobile?
- PageSpeed > 90?
- WhatsApp CTA funciona?
- Meta tags corretas?

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/designer-landing-page.json` (com campo `summary` no topo, incluindo URL de deploy)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph

## Formato do output (designer-landing-page.json)

```json
{
  "sections": [
    { "name": "hero", "headline": "string", "subheadline": "string", "cta_primary": "string", "cta_secondary": "string" },
    { "name": "problem", "headline": "string", "cards": [{ "title": "string", "body": "string" }] },
    { "name": "solution", "headline": "string", "benefits": [{ "icon": "string", "title": "string", "body": "string" }] },
    { "name": "how_it_works", "headline": "string", "steps": [{ "number": 1, "title": "string", "body": "string" }] },
    { "name": "deliverables", "headline": "string", "items": [{ "title": "string", "benefit": "string" }] },
    { "name": "final_cta", "headline": "string", "subheadline": "string", "cta": "string" }
  ],
  "faq": [{ "question": "string", "answer": "string" }],
  "social_proof": {
    "testimonials": [{ "name": "string", "role": "string", "text": "string" }],
    "stats": [{ "number": "string", "label": "string" }]
  },
  "meta": { "title": "string", "description": "string", "og_title": "string", "og_description": "string", "og_type": "website" },
  "deploy_url": "string",
  "whatsapp_link": "string"
}
```


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do landing page: proposta central da página e número de seções criadas. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
