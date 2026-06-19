---
name: geral-social-media-system
description: Sistema completo de gestão de social media — conduz workflows de briefing, geração de copy com frameworks (AIDA, PAS, Storytelling, Prova Social) e rastreamento de resultados direto no chat, E gera/atualiza o arquivo HTML da ferramenta de gestão visual. Use sempre que o usuário mencionar social media, briefing de conteúdo, geração de copy, gestão de clientes de social, resultado de post, calendário editorial, ou quiser o arquivo HTML da ferramenta. Ative também quando o contexto for criar ou planejar qualquer conteúdo para redes sociais, mesmo que o usuário não diga "social media" explicitamente.
area: geral
author: bhrendacruz-bot
version: 1.0.0
---

# Social Media System — V4

Sistema central de gestão de social media da V4. Opera em dois modos que podem ser combinados na mesma sessão.

---

## Modo 1: Workflows via Conversa

Conduza cada etapa do processo de social media diretamente no chat, sem precisar abrir o HTML.

### 1. Gestão de Clientes

Quando o usuário quiser registrar ou consultar um cliente, colete:
- **Nome** do cliente
- **Segmento**: Fitness/Saúde · Distribuição · Alimentos/Bebidas · E-commerce · Serviços · Outros
- **Plataformas**: Instagram, TikTok, LinkedIn, YouTube, etc.
- **Objetivo principal** (o que ele quer alcançar com social media)

Apresente o resumo formatado e confirme antes de salvar.

---

### 2. Briefing Inteligente

Quando o usuário quiser criar um briefing, colete os campos abaixo em sequência (não despeje todos de uma vez — pergunte de forma conversacional):

| Campo | O que perguntar |
|---|---|
| Cliente | Qual dos cadastrados, ou novo? |
| Tipo de conteúdo | Post Feed, Stories, Reels/TikTok, Carrossel, Link Post |
| Objetivo | Awareness, Engagement, Conversão, Retenção, Educação |
| Contexto estratégico | Por que estamos criando? Que problema resolvemos? O que diferencia o cliente? |
| Mensagem principal | O que queremos que o público sinta ou faça? |
| Tom de voz | Profissional, Amigável, Criativo, Urgente, Educativo |
| Público-alvo | Quem vai ver esse conteúdo? |
| Pontos de atenção | O que NÃO fazer? Palavras/tons a evitar? |

Gere o briefing neste formato exato:

```
📋 BRIEFING ESTRUTURADO — [NOME DO CLIENTE]
────────────────────────────────────────────

🎯 OBJETIVO DO CONTEÚDO
[objetivo]

📖 CONTEXTO ESTRATÉGICO
[contexto]

💬 MENSAGEM PRINCIPAL
"[mensagem]"

👥 PÚBLICO-ALVO
[publico]

🎨 TOM DE VOZ
[tom]

📱 TIPO DE CONTEÚDO
[tipo]

⚠️ PONTOS DE ATENÇÃO
[avisos ou "Nenhum aviso específico"]

────────────────────────────────────────────
✅ Briefing gerado em [data]
```

---

### 3. Gerador de Copy

Quando o usuário quiser gerar copy, pergunte:
1. **Framework**: AIDA, PAS, Storytelling ou Prova Social
2. **Formato**: Curta (até 30 palavras), Média (até 150), Longa (até 300), CTA puro
3. **Cliente** (contexto de marca e tom de voz)
4. **Ideia/Produto/Serviço** a promover
5. **Detalhes importantes**: benefícios, diferenciais, números, promoções

Gere **3 variações** usando o framework escolhido. Depois de cada variação, explique em uma linha a lógica que você usou.

#### Frameworks — referência rápida

**AIDA** (Atenção → Interesse → Desejo → Ação)
Capture atenção com gancho forte, construa interesse com benefícios concretos, crie desejo com emoção ou resultado e feche com CTA direto.

**PAS** (Problema → Agitação → Solução)
Nomeie a dor do público com precisão, amplifique a consequência de não resolver, apresente a solução como alívio imediato.

**Storytelling** (Personagem → Conflito → Resolução)
Apresente personagem com quem o público se identifica, mostre o conflito/dor real, revele a transformação possível.

**Prova Social** (Resultado → Evidência → CTA)
Comece com resultado real ou número, valide com voz do cliente/depoimento/dado, convide para o mesmo resultado.

---

### 4. Rastreamento de Resultados

Quando o usuário quiser registrar um resultado, colete:
- **Cliente** e **data**
- **Conteúdo/Campanha** (tipo e nome)
- **Métrica principal** e **resultado** (número ou %)
- **O que funcionou?** (padrão identificado)
- **Próximos passos** (o que replicar, testar ou melhorar)

Depois de registrar, faça uma análise de 2-3 linhas: o que esse resultado revela sobre o que funciona pra esse cliente? Que padrão está se consolidando?

---

## Modo 2: Ferramenta HTML

Quando o usuário pedir o arquivo da ferramenta, quiser abrir o sistema no browser, ou quiser atualizar o HTML:

Leia o arquivo em `assets/social-media-system.html` e:
- **Entregar**: forneça o caminho do arquivo ou copie o conteúdo completo
- **Atualizar**: aplique as modificações pedidas diretamente no arquivo e confirme o que mudou
- **Melhorar**: se o usuário pedir nova seção, campo, framework ou funcionalidade, implemente e entregue a versão atualizada

O HTML usa localStorage para persistência — nenhuma dependência externa, abre direto no browser.

---

## Como combinar os dois modos

O usuário pode, na mesma sessão:
1. Criar um briefing via conversa (Modo 1)
2. Pedir pra você atualizar o HTML para incluir esse cliente/briefing (Modo 2)

Se o usuário não especificar o modo, conduza pelo workflow de conversa — é mais rápido para o dia a dia. Ofereça o HTML só quando ele pedir ou quando o output for claramente visual/para compartilhar.

---

## Gatilhos de ativação

Ative esta skill quando o usuário mencionar:
- Briefing, pauta, calendário de conteúdo
- Copy, legenda, caption, CTA
- Social media, redes sociais, Instagram, TikTok, LinkedIn
- Resultado de post, métricas de engajamento, performance de campanha
- Cliente de social, gestão de social media
- AIDA, PAS, Storytelling, Prova Social (frameworks de copy)
- "ferramenta HTML", "abrir o sistema", "arquivo .html"
