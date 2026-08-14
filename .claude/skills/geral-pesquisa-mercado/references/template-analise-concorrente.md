# Template de Analise de Concorrente

Framework para analisar cada concorrente de forma sistematica e acionavel.

## Dimensoes de analise

### 1. Posicionamento e PUV
**O que observar:**
- Headline do site (primeira coisa que o visitante le)
- Tagline ou slogan
- Bio do Instagram
- Descricao do Google Meu Negocio
- Como se descreve em anuncios

**Perguntas-chave:**
- O geral-posicionamento-estrategico e claro em 5 segundos?
- A PUV e especifica ou generica ("qualidade e compromisso")?
- Ele se posiciona por preco, qualidade, especializacao ou conveniencia?

**Red flags de geral-posicionamento-estrategico fraco:**
- "Solucoes completas" sem definir o que
- "Mais de X anos de experiencia" como unico diferencial
- Nenhuma especificidade sobre para quem serve
- Copy generica que serve para qualquer empresa do setor

### 2. Canais de aquisicao
**O que investigar:**
- Google Ads: busque as palavras-chave do setor e veja se o concorrente aparece
- Meta Ads Library: acesse facebook.com/ads/library e busque o nome do concorrente
- Instagram: frequencia de postagem, engajamento, uso de reels/stories
- Google organico: busque o nome + segmento e veja o ranking
- YouTube: tem canal? Que tipo de conteudo?
- Google Meu Negocio: esta otimizado? Quantas avaliacoes?
- Email marketing: inscreveu-se na newsletter? Qual a cadencia?
- WhatsApp: usa como canal de atendimento/venda?

**Classificacao de maturidade por canal:**
| Nivel | Descricao |
|---|---|
| 0 — Ausente | Nao usa o canal |
| 1 — Presente | Tem presenca mas sem estrategia |
| 2 — Ativo | Publica/anuncia regularmente |
| 3 — Otimizado | Boa execucao, testes, segmentacao |
| 4 — Lider | Referencia no canal para o segmento |

### 3. Pontos fortes observados
**Categorias comuns:**
- **Marca forte:** Reconhecimento, tempo de mercado, reputacao
- **Conteudo educativo:** Produz material que gera confianca
- **Prova social:** Muitas avaliacoes, cases, depoimentos
- **Tecnologia:** Site rapido, app, automacoes
- **Atendimento:** Resposta rapida, multi-canal
- **Especializacao:** Foco em nicho especifico
- **Preco competitivo:** Oferta agressiva
- **Distribuicao:** Presenca fisica + digital

**Regra:** Cite EVIDENCIA, nao suposicao. "Site carrega em 1.5s e tem 4.8 estrelas com 230 avaliacoes no Google" > "Parece ter boa presenca digital"

### 4. Pontos fracos observados
**Categorias comuns:**
- **Site lento/desatualizado:** PageSpeed abaixo de 50, design antigo
- **Copy generica:** Nenhum diferencial claro
- **Anuncios fracos:** Criativos sem hook, copy padrao
- **Sem prova social:** Poucas avaliacoes, sem cases
- **Precificacao opaca:** Nao mostra precos, dificulta comparacao
- **Canais abandonados:** Instagram com ultima postagem ha 3 meses
- **Nao segmentado:** Fala para todo mundo (e portanto para ninguem)
- **Sem funil:** Manda trafego direto para homepage, sem LP

**Regra:** So liste fraquezas que podem ser EXPLORADAS pelo seu cliente. "Atendimento ruim" so importa se o seu cliente pode fazer melhor.

### 5. Estimativa de preco/ticket medio
**Como estimar quando nao ha preco publico:**
1. Peca orcamento como cliente oculto (se viavel)
2. Verifique sites de comparacao (ex: Glassdoor para salarios, comparadores setoriais)
3. Procure menções de preço em avaliacoes de clientes
4. Analise o geral-posicionamento-estrategico: premium/mid/value
5. Verifique ofertas em anuncios (ex: "a partir de R$ X")
6. Pergunte ao operador — ele provavelmente sabe o range do mercado

**Formato:** "R$ 2.000-3.000/mes (estimativa baseada em anuncios + geral-posicionamento-estrategico mid-market)"

### 6. Presenca digital — Score 1-10
**Criterios de pontuacao:**

| Score | Descricao |
|---|---|
| 1-2 | Quase inexistente. Site basico ou inexistente. Sem redes ativas. |
| 3-4 | Presente mas fraco. Site funcional, redes com pouca frequencia, sem anuncios. |
| 5-6 | Mediano. Site razoavel, posta nas redes, investe pouco em midia paga. |
| 7-8 | Bom. Site profissional, redes ativas com engajamento, anuncios rodando, Google My Business otimizado. |
| 9-10 | Excelente. Lider digital no segmento/regiao. Conteudo, midia paga, SEO, reviews — tudo bem executado. |

**Detalhe por canal:**
- Site: velocidade, design, mobile, SEO basico, CTA claro
- Instagram: frequencia, engajamento rate, qualidade visual, uso de stories/reels
- Google: ranking para termos do segmento, Google Meu Negocio, avaliacoes
- Anuncios: quantidade ativa, qualidade criativa, variedade de formatos

## Template de output por concorrente

```
CONCORRENTE: [Nome]
Site: [URL]
━━━━━━━━━━━━━━━━━━━

Posicionamento: [frase que resume como se posiciona]
PUV declarada: [o que diz ser o diferencial]
PUV real percebida: [o que de fato diferencia na pratica]

Canais de aquisicao:
  - Google Ads: [nivel 0-4 + observacao]
  - Meta Ads: [nivel 0-4 + observacao]
  - Instagram organico: [nivel 0-4 + observacao]
  - Google organico/SEO: [nivel 0-4 + observacao]
  - Outros: [quais e nivel]

Pontos fortes:
  1. [ponto forte + evidencia]
  2. [ponto forte + evidencia]

Pontos fracos:
  1. [ponto fraco + evidencia]
  2. [ponto fraco + evidencia]

Estimativa de preco: R$ [range] / [periodo]
Fonte da estimativa: [como estimou]

Presenca digital: [score]/10
  - Site: [observacao]
  - Instagram: [seguidores] — [observacao]
  - Google My Business: [avaliacoes] estrelas — [observacao]
  - Anuncios ativos: [sim/nao] — [observacao]
```

## Mapa competitivo 2x2

Apos analisar todos os concorrentes, posicione-os em um mapa 2x2. Os eixos mais comuns para PMEs:

**Eixos recomendados por segmento:**

| Segmento | Eixo X | Eixo Y |
|---|---|---|
| Servicos profissionais | Generalista vs Especialista | Premium vs Acessivel |
| Comercio/varejo | Local vs Online | Preco vs Experiencia |
| Saude/estetica | Tratamento generico vs Nicho | Clinica popular vs Clinica premium |
| Educacao | Presencial vs Digital | Certificacao vs Pratica |
| SaaS | Self-service vs Assistido | Feature-rich vs Simples |
| Alimentacao | Fast food vs Gourmet | Delivery vs Presencial |

**Regra:** Escolha eixos que REVELEM ESPACOS VAZIOS. Se todos os concorrentes estao no mesmo quadrante, o mapa e util porque mostra oportunidade. Se estao espalhados, escolha eixos que agrupem de forma mais reveladora.
