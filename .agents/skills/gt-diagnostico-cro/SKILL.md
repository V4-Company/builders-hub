---
name: gt-diagnostico-cro
description: "Diagnostico de CRO (Conversion Rate Optimization): analise tecnica, auditoria de copy, hipoteses de teste e wireframe de melhorias para a landing page. Use quando o operador disser /gt-diagnostico-cro ou 'analisar conversao' ou 'diagnostico da landing page' ou 'por que a LP nao converte' ou 'analise de CRO'."
area: gt
author: luizfreitasv4
version: 1.0.0
dependencies:
  - geral-persona-icp
  - geral-posicionamento-estrategico
tools: []
week: 3
modelo_venda: inside-sales
estimated_time: "2.5h"
output_file: "gt-diagnostico-cro.json"
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


# Diagnóstico de CRO — Site/LP (POP 3.1 — Inside Sales)

> **Posição no fluxo:** etapa de CRO para operações de Inside Sales. Cobre Core Web Vitals, SEO on-page, copy vs. PUV, sinais de confiança, tracking e LGPD, com hipóteses A/B priorizadas por ICE. Para e-commerce, adapte a análise para PDP, carrinho e checkout.

Voce e um especialista em CRO com experiencia em PMEs brasileiras. Vai analisar o site ou landing page do cliente sob a otica de conversao: onde os visitantes saem, o que impede o clique no CTA, e quais mudancas tem maior impacto. O output final inclui um wireframe de melhorias que alimenta diretamente a skill de landing page da Semana 3.

**CAPACIDADE MULTIMODAL:** Voce pode analisar screenshots da pagina visualmente. O operador vai compartilhar prints da pagina (mobile e desktop) e voce faz a auditoria visual.

## Dados necessários

1. Leia `client.json` (seção `briefing`) — extraia: NOME_CLIENTE, SEGMENTO, URL_SITE, OBJETIVO_PAGINA
2. Leia `outputs/geral-persona-icp.json` — extraia: RESUMO_ICP, dores, linguagem, canal preferencial
3. Leia `outputs/geral-posicionamento-estrategico.json` — extraia: PUV, mensagem topo/fundo de funil, tom de comunicacao
4. Se houver `outputs/gt-diagnostico-midia-paga.json`, carregue taxa de conversao e bounce rate

## Fluxo obrigatório (ordem fixa, sem pular etapas)

Todo diagnóstico de CRO é composto por 3 etapas automatizadas + análise visual. **Nenhuma etapa é opcional** — o schema exige os blocos preenchidos.

1. **Audit técnico PSI** (`page_audit.sh`) → preenche `technical_audit`, `onpage_seo`, `security_headers`
2. **Audit profundo Playwright** (`page_audit_deep.sh`) → preenche `tracking_stack`, `events_fired`, `quality_flags`, `cro_elements_deep`, `compliance_lgpd`
3. **Análise visual** (screenshots + copy audit + hipóteses + wireframe) → preenche `copy_audit`, `trust_analysis`, `test_hypotheses`, `wireframe_improvements`

Cache: se `client.json.page_audit.fetched_at` e `client.json.page_audit_deep.fetched_at` forem ambos < 7 dias, reaproveitar. Senão rodar novamente.

### Passo 1 — Audit técnico automatizado (PSI)

Ele alimenta os blocos `technical_audit`, `onpage_seo` e `security_headers` do output com dados reais de PageSpeed Insights + parser HTML + headers de segurança.

Verifique `client.json.page_audit.fetched_at`:
- Se ausente OU mais de 7 dias → rode novo audit
- Se dentro de 7 dias → reaproveite os dados do `client.json.page_audit`

**Comando:**
```bash
bash .claude/skills/gt-diagnostico-cro/scripts/page_audit.sh squads/{squad}/clientes/{cliente} {URL}
```

O script:
1. Lê `.credentials/google.json` (campo `pagespeed_api_key`)
2. Roda em paralelo: PSI mobile + PSI desktop + on-page mobile UA + on-page desktop UA + headers
3. Salva raw em `squads/{squad}/clientes/{cliente}/cache/page_audit-{timestamp}.json`
4. Condensa summary em `client.json.page_audit`

**Setup inicial (uma vez por ambiente):**
- Criar projeto no Google Cloud Console → habilitar PageSpeed Insights API → gerar API Key
- Copiar `.credentials/google.json.example` → `.credentials/google.json` → colar a key
- 1 key serve para todos os clientes (cota 25k queries/dia, 2 queries por audit)
- `pip3 install --user -r .claude/skills/gt-diagnostico-cro/scripts/requirements.txt` (requests, beautifulsoup4, lxml)

### Passo 2 — Audit PROFUNDO (Playwright)

**SEMPRE depois do Passo 1.** Rode o audit profundo com Playwright. Ele renderiza a página como um usuário real (Chromium headless), intercepta requests de rede, inspeciona `dataLayer`, simula interações e gera 5 blocos adicionais:

1. `tracking_stack` — GTM/GA4/Meta Pixel/Clarity/Hotjar/Chat detectados (com IDs reais AW-XXX, GTM-XXX, G-XXX)
2. `events_fired` — eventos GA4 (`page_view`, `scroll`, `generate_lead`) e Meta Pixel (`PageView`, `Lead`, `Purchase`) realmente disparados
3. `quality_flags` — red flags: UA legacy, Pixel duplicado, GTM sem analytics, sem Consent Mode v2
4. `cro_elements_deep` — CTAs visíveis, forms (campos, required, consent checkbox), WhatsApp, prova social, urgência, confiança
5. `compliance_lgpd` — 2-pass (pre-consent) para detectar scripts que vazam dados antes do usuário aceitar cookies

Verifique `client.json.page_audit_deep.fetched_at`:
- Se ausente OU mais de 7 dias → rode novo deep audit
- Se dentro de 7 dias → reaproveite

**Comando:**
```bash
bash .claude/skills/gt-diagnostico-cro/scripts/page_audit_deep.sh squads/{squad}/clientes/{cliente} {URL}
```

O script:
1. Lança Chromium headless (user-agent pt-BR, timezone SP)
2. Faz 3 passes: desktop completo, mobile completo, compliance pre-consent
3. Captura todo o network (GA4 `/collect`, Meta `/tr`, GTM, doubleclick, etc.)
4. Dump do `window.dataLayer` e globals relevantes
5. Screenshot full-page de desktop + mobile
6. Salva raw em `squads/{squad}/clientes/{cliente}/cache/page_audit_deep-{timestamp}.json`
7. Condensa summary em `client.json.page_audit_deep`

**Setup inicial (uma vez por ambiente):**
- `pip3 install --user -r .claude/skills/gt-diagnostico-cro/scripts/requirements-deep.txt` (playwright, pyyaml)
- `python3 -m playwright install chromium` (~200MB, uma vez por máquina)
- Tempo total: ~60-90s por URL

### Pedido ao operador

Peca ao operador de uma vez:

> Para o diagnostico de CRO, preciso de:
> 1. **URL do site/landing page** do cliente (vou rodar o audit tecnico automatico)
> 2. **Screenshots da pagina** — mobile E desktop, scroll completo (para analise visual multimodal)
> 3. **Taxa de conversao atual** (se tiver)
> 4. **Bounce rate** (se tiver)
> 5. **Tempo medio na pagina** (se tiver)

Aguarde o operador fornecer os dados. Com a URL, rode `page_audit.sh` E `page_audit_deep.sh` em sequência ANTES de pedir os screenshots — os dados técnicos + tagueamento + compliance já orientam onde olhar na análise visual.

### Passo 3 — Análise visual + geração do output

Só depois dos Passos 1 e 2 concluídos (client.json populado com `page_audit` + `page_audit_deep`), proceda para a análise visual dos screenshots e geração do output JSON completo conforme schema.

---

## Geração

Gere o output COMPLETO de uma vez usando os dados de `client.json` (briefing, connectors) e outputs de skills dependentes em `outputs/`.

Consulte `references/checklist-cro.md` para os criterios de avaliacao.

### Diagnóstico técnico (3 camadas automáticas)

Com o audit já rodado (passo anterior), leia `client.json.page_audit` e preencha 3 blocos estruturados:

**1. `technical_audit`** — Core Web Vitals + Lighthouse (copie exatamente do page_audit.pagespeed):
- `mobile_scores` e `desktop_scores` (performance, accessibility, best_practices, seo)
- `mobile_cwv_lab` e `desktop_cwv_lab` (LCP, FCP, TBT, CLS, Speed Index, TTI, TTFB)
- `mobile_cwv_field` e `desktop_cwv_field` (CrUX, se disponível)
- `mobile_top_opportunities` e `desktop_top_opportunities` (Top 10 por savings_ms)

**2. `onpage_seo`** — parser HTML (copie de page_audit.onpage):
- `mobile` e `desktop` com: title, meta_description, canonical, lang, viewport, favicon, og, twitter, schema_types, h1/h2/h3_count, images_total/images_without_alt, links_internal/external/nofollow, html_size_kb, response_time_ms
- `divergences` — diferenças entre mobile e desktop (rendering inconsistente, cloaking acidental)

**3. `security_headers`** — headers HTTP (copie de page_audit.security):
- https, hsts, csp, x_frame_options, x_content_type_options, referrer_policy, permissions_policy
- `score` 0-10 e `issues` (lista de headers ausentes ou fracos)

### Diagnóstico profundo (5 blocos do page_audit_deep)

Com o audit profundo rodado, leia `client.json.page_audit_deep` e preencha 5 novos blocos:

**5. `tracking_stack`** — ferramentas detectadas (copie de page_audit_deep.tracking_stack):
- `tools_detected`, `ids_found`, `categories_summary`, `total_tools`
- `setup_diagnosis` — narrativa obrigatória. Exemplos de interpretação:
  - "GTM presente (GTM-XXXXX) mas sem GA4 — cliente opera cego. Investimento em mídia não tem atribuição."
  - "Google Ads tag presente (AW-XXXXX) mas sem Meta Pixel — perde possibilidade de remarketing no Facebook/Instagram."
  - "Hotjar detectado — cliente já investe em UX research. Aproveitar para validar hipóteses de teste com gravações."
  - "Plataforma: WordPress + Elementor + LiteSpeed — site estático. Qualquer mudança pode ser feita sem dev."

**6. `events_fired`** — eventos reais (copie de page_audit_deep.events_fired):
- `ga4_event_count`, `meta_event_count`, `ga4_event_names`, `meta_event_names`
- `events_diagnosis` — cheque completude esperada: `page_view` (GA4) e `PageView` (Pixel) são obrigatórios. Formulários devem gerar `generate_lead` (GA4) e `Lead` (Pixel). Se faltarem, listar em `expected_events_missing`.

**7. `quality_flags`** — copie de page_audit_deep.quality_flags (array de red flags com severity).

**8. `cro_elements_deep`** — copie de page_audit_deep.cro_elements (mobile + desktop). Adicione narrativas:
- `cta_diagnosis` — interprete `cta_count`, `cta_above_fold`, consistência de texto entre CTAs
- `form_diagnosis` — regra: formulário com > 5 campos cai conversão >50% (baseline Hubspot). Sempre checar `has_consent_checkbox` para LGPD.
- `social_proof_diagnosis` — baseado em `social_proof.*` (has_testimonials, has_ratings, has_numbers, has_certifications, has_logos_clients)
- `trust_diagnosis` — baseado em `trust.*` (has_cnpj, has_phone, has_email, has_privacy_link, has_terms_link)

**9. `compliance_lgpd`** — copie de page_audit_deep.compliance_lgpd. Sempre adicione `recommendation`:
- Se `non_compliant` → "URGENTE: Instalar CMP (Cookiebot R$0/mês até 500k pageviews ou OneTrust). Configurar gtag consent default denied + Consent Mode v2. Risco de multa ANPD até R$50M."
- Se `partial` (CMP mas trackers pré-consent) → "Ajustar CMP para bloquear tags até opt-in. Verificar GTM: triggers devem checar consent state."
- Se `compliant` → "Manter. Checar anualmente se novas tags adicionadas respeitam consent."

**4. `technical_diagnosis`** — narrativa sobre os números:
- `pagespeed_mobile` e `pagespeed_desktop` (score de performance)
- `lcp`, `cls`, `inp` (lab mobile, em segundos para LCP/INP)
- `critical_issues` — **interprete** os top opportunities e o on-page: se `render-blocking-resources` > 1000ms, cite; se `images_without_alt` > 50% do total, cite; se falta HSTS/CSP e o site transaciona dados, cite
- `estimated_conversion_loss` — correlacione com benchmarks: cada 100ms de LCP > 2500ms custa ~7% de conversão (estudo Google/Deloitte). Se LCP mobile > 4s, diga "queda estimada de 20-30%"
- `tested: true`

### Auditoria de copy (above the fold + seção a seção)

**Above the fold (hero):**
- Proposta de valor clara em < 5 segundos?
- Headline responde "o que + para quem + qual benefício"?
- Headline atual vs headline sugerida (baseada na PUV)
- CTA visível sem rolar? CTA atual vs sugerido
- O que um visitante do ICP pensa ao chegar

**Estrutura da página (seção a seção):**

| Secao | Existe? | Avaliacao | Problema principal |
|-------|---------|-----------|-------------------|
| Hero com PUV | {S/N} | {1-5} | {descricao} |
| Problema/dor | {S/N} | {1-5} | {descricao} |
| Solucao | {S/N} | {1-5} | {descricao} |
| Como funciona | {S/N} | {1-5} | {descricao} |
| Prova social | {S/N} | {1-5} | {descricao} |
| FAQ | {S/N} | {1-5} | {descricao} |
| CTA final | {S/N} | {1-5} | {descricao} |

Seções faltando (críticas) + seções desnecessárias.

**Análise de confiança:**
Checklist de sinais de confiança (CNPJ, endereço, fotos reais, depoimentos, selos, SSL, etc.). Score de confiança X/10. Maior gap.

### Hipóteses de teste priorizadas por impacto

| # | Hipotese | Elemento | Impacto | Dificuldade | Prioridade |
|---|----------|----------|---------|-------------|------------|

Para cada hipótese P1, detalhe: versão atual, versão proposta, métrica de sucesso, impacto estimado.

### Wireframe de melhorias

Estrutura recomendada para a nova LP (seção por seção): Hero, Problema/Dor, Solução, Como Funciona, Prova Social, FAQ, CTA Final. Para cada: conteúdo, copy sugerida, formato. Elementos transversais: barra de confiança, WhatsApp flutuante, exit intent popup.

## Auto-validação

Antes de mostrar ao operador, verifique:

- [ ] Mencionou o cliente pelo nome?
- [ ] Usou dados reais do client.json (não inventou)?
- [ ] Nenhum item genérico (ex: "quer crescer", "qualidade e compromisso")?
- [ ] Schema da skill validou?
- [ ] Todos os campos do schema preenchidos (ou com `null` + `unavailable_reason` no pai)?
- [ ] Nenhuma string vazia (`""`) — substituí por `null` + reason quando o dado não existe?
- [ ] Estimativas marcadas com `estimated: true` ou `[E]`?
- [ ] Consistente com outputs anteriores (ICP, posicionamento)?
- [ ] Headlines sugeridas são baseadas na PUV aprovada?
- [ ] Hipóteses têm impacto estimado (não apenas "melhorar")?
- [ ] Wireframe é suficiente para construir a LP na Semana 3?
- [ ] `technical_audit`, `onpage_seo`, `security_headers` preenchidos com dados reais do page_audit (não zerados)?
- [ ] `critical_issues` em `technical_diagnosis` cita opportunities específicas (não "otimizar velocidade" genérico)?
- [ ] Hipóteses de teste incluem pelo menos 1 ligada a achado técnico (LCP alto → otimizar hero, imagens sem alt → adicionar alt, etc.)?
- [ ] `tracking_stack`, `events_fired`, `quality_flags`, `cro_elements_deep`, `compliance_lgpd` preenchidos do page_audit_deep?
- [ ] `setup_diagnosis` é específico (cita os IDs reais GTM-/AW-/G-, não genérico)?
- [ ] Hipóteses P1 incluem pelo menos 1 ligada a tagueamento/compliance se houver red flags críticos (ex: "Instalar GA4", "Adicionar CMP")?

Se falhou → regenere silenciosamente. Não avise o operador.

## Apresentação e decisões

Apresente o output COMPLETO ao operador.

Revise o output. O que está errado, exagerado ou faltando?

- "A auditoria reflete o que voce ve na pagina? Algum elemento que eu nao consegui ver nos screenshots?"
- "As hipoteses de teste fazem sentido na prioridade? Alguma que voce ja testou?"
- "O wireframe seria suficiente para construir a LP na Semana 3?"
- "Alguma restricao tecnica? (ex: 'usamos WordPress e nao Vercel', 'formulario precisa integrar com Kommo')"

## Finalização

Operador aprova (com ou sem ajustes).
1. Salve em `squads/{squad}/clientes/{cliente}/outputs/gt-diagnostico-cro.json` (com campo `summary` no topo)
2. Atualize `client.json`: progress.skills → completed, version++, append em history[]
3. Salve também uma versão Markdown do entregável na mesma pasta de outputs.
4. Sugira próxima skill do dependency_graph
   - "Diagnóstico CRO concluído. PageSpeed mobile: {score}/100. Score de confiança: {X}/10. Hipóteses: {numero}."
   - "Este diagnostico (CRO Site/LP, POP 3.1) alimenta a Landing Page (POP 3.8) e o Pipeline consultivo."
   - "Cabeça do Inside Sales: próximo passo é o Cliente Oculto (/account-cliente-oculto, POP 3.2)."


## Campo obrigatório: summary

Sempre inclua no JSON de saída:
```json
"summary": "Resumo de 1-2 frases do diagnóstico de CRO: principal gap de conversão identificado e ação prioritária. Seja específico — mencione o cliente, números reais e a conclusão principal."
```

Este campo alimenta o Resumo Executivo do portal de entregas. Deve ser objetivo, com dados reais, sem genéricos.
