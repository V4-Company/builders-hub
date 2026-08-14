# Regras de Copy para Performance — Limites e Boas Práticas por Plataforma

Referência técnica para garantir que toda copy respeite limites de caracteres, regras de política e padrões de alta performance.

---

## Meta Ads (Facebook + Instagram)

### Limites de caracteres

| Campo | Limite técnico | Recomendado | Nota |
|-------|---------------|-------------|------|
| Texto principal (primary text) | 2.200 chars | 125 chars | Após 125, texto é truncado com "...ver mais" |
| Título (headline) | 255 chars | 40 chars | Truncado em mobile após ~40 chars |
| Descrição (description) | 255 chars | 30 chars | Só aparece no feed desktop, truncada em mobile |
| Nome do botão CTA | Pré-definido | — | Saiba mais / Cadastre-se / Comprar / Fale conosco / etc. |

### Regras de política (que causam reprovação)

- **Afirmações pessoais diretas:** "Você está acima do peso?" → REPROVADO. Use "Muitas pessoas enfrentam dificuldade para..."
- **Antes/depois:** Imagens de transformação física → REPROVADO em quase todos os casos
- **Promessas absolutas:** "Garantimos 100% de resultado" → REPROVADO. Use "Nosso compromisso é..."
- **Referência a atributos pessoais:** Raça, orientação, religião, condição financeira → REPROVADO
- **Menção à plataforma:** "Viu esse anúncio no Facebook?" → REPROVADO
- **Caps lock excessivo:** "OFERTA IMPERDÍVEL SOMENTE HOJE" → Pode ser reprovado ou ter alcance limitado
- **Emojis no título:** Pode reduzir alcance (depende do período, Meta varia)

### O que funciona em Meta Ads Brasil

1. **Hook nos primeiros 3-5 palavras** — é o que aparece antes do truncamento
2. **Pergunta na primeira frase** — gera curiosidade e engajamento
3. **Números específicos** — "347 clientes em BH" > "centenas de clientes"
4. **Emojis com parcimônia** — 1-2 no texto principal, 0 no título
5. **CTA no texto + no botão** — redundância intencional funciona
6. **Copy curta para fundo de funil** — quem já conhece não precisa de educação
7. **Copy média para topo** — educa e gera interesse, mas não enrola

### Estrutura de texto principal (Meta)

**Topo de funil (educativo):**
```
[Pergunta ou dado impactante]
[1-2 frases de contexto/empatia]
[CTA leve: "Saiba mais no link"]
```

**Meio de funil (prova social):**
```
[Resultado concreto de cliente]
[Como foi alcançado em 1 frase]
[CTA: "Veja como funciona"]
```

**Fundo de funil (conversão):**
```
[Oferta direta com benefício]
[Urgência real ou escassez]
[CTA forte: "Fale com a gente agora"]
```

---

## Google Ads (Search — Responsive Search Ads)

### Limites de caracteres

| Campo | Limite | Quantidade |
|-------|--------|-----------|
| Título (headline) | 30 caracteres cada | Até 15 títulos (mín. 3) |
| Descrição | 90 caracteres cada | Até 4 descrições (mín. 2) |
| URL de exibição (paths) | 15 caracteres cada | 2 paths |

### Como o responsivo funciona

O Google combina seus títulos e descrições automaticamente. Por isso:
- **Cada título deve funcionar sozinho** (não depender de outro para fazer sentido)
- **Não repita a mesma mensagem** em títulos diferentes (Google penaliza redundância)
- **Fixe (pin)** apenas se necessário: Título 1 fixo = nome da marca ou oferta principal
- **Diversifique os hooks:** dor, resultado, autoridade, oferta, CTA

### Regras de política Google Ads

- **Pontuação excessiva:** "Melhor preço!!!" → REPROVADO. Máx. 1 ponto de exclamação por anúncio
- **Caps lock:** "MELHOR PREÇO" → REPROVADO. Use capitalização normal
- **Superlativos sem prova:** "O melhor do Brasil" → Precisa de certificação de terceiros
- **Marca registrada:** Usar nome de concorrente → Pode ser contestado
- **Símbolos não padrão:** Setas unicode (→, ►) → Podem ser reprovadas
- **Espaçamento abusivo:** "M E L H O R" → REPROVADO

### O que funciona em Google Ads Brasil

1. **Palavra-chave no Título 1** — corresponde à busca do usuário
2. **Número no Título 2** — "R$ 99/mês" ou "Em 7 dias" (específico)
3. **CTA na Descrição 1** — "Solicite um orçamento gratuito"
4. **Prova social na Descrição 2** — "+500 clientes em SP"
5. **Paths descritivos** — exemplo.com/orcamento/gratuito
6. **Extensões** — sempre adicione: sitelinks, callouts, snippets, preço

### Tipos de título por intenção

**Informacional (topo):**
- "O que é [serviço] e por que importa"
- "Guia completo de [tema]"
- "[Número] dicas para [resultado]"

**Comercial (meio):**
- "[Serviço] em [Cidade] - Orçamento"
- "Compare opções de [serviço]"
- "[Número] clientes confiam em nós"

**Transacional (fundo):**
- "Contrate [serviço] - Sem contrato"
- "[Serviço] a partir de R$ [valor]"
- "Orçamento grátis em 24h"

---

## Regras universais de copy de performance

### 1. Hierarquia de hooks (do mais ao menos efetivo)

1. **Dor específica do ICP** — "Perdendo leads por falta de follow-up?"
2. **Resultado com número** — "340 restaurantes já economizam R$ 3.000/mês"
3. **Curiosidade/pergunta** — "Você sabia que 73% dos leads não recebem resposta em 24h?"
4. **Prova social** — "Avaliado com 4.9★ por +200 clientes"
5. **Urgência real** — "Últimas 5 vagas para onboarding em abril"
6. **Oferta direta** — "Diagnóstico gratuito: descubra por que seus anúncios não convertem"

### 2. Fórmulas de copy comprovadas

**PAS (Problem → Agitation → Solution):**
Problema: "Seus leads somem depois do primeiro contato?"
Agitação: "Cada lead ignorado é dinheiro jogado fora. E quanto mais demora, menos vale."
Solução: "Automatize o follow-up com [produto]. Resposta em segundos, 24/7."

**AIDA (Attention → Interest → Desire → Action):**
Atenção: "R$ 12.000 em comissões economizadas"
Interesse: "A Cantina Mineira trocou o iFood por delivery próprio"
Desejo: "Sem comissão, sem intermediário, ticket 35% maior"
Ação: "Monte seu delivery direto em 7 dias"

**BAB (Before → After → Bridge):**
Antes: "Dependendo 100% de indicação para novos clientes"
Depois: "30 leads qualificados por mês no seu WhatsApp"
Ponte: "[Produto] conecta você aos clientes que já buscam o que você vende"

### 3. Checklist antes de aprovar

- [ ] Limite de caracteres respeitado em TODAS as variações
- [ ] Hook nos primeiros 3-5 palavras
- [ ] Nenhuma copy do topo menciona produto/marca
- [ ] Fundo de funil tem urgência REAL (não fake)
- [ ] Remarketing é diferente da copy fria
- [ ] Tom consistente com designer-manual-marca (vocabulário, tratamento)
- [ ] Nenhuma violação de política de plataforma
- [ ] Mínimo 30 variações no total
- [ ] Cada variação testa um hook/ângulo diferente (não paráfrases do mesmo)
