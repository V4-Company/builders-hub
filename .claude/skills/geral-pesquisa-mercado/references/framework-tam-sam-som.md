# Framework TAM/SAM/SOM para PMEs Brasileiras

## O que e cada metrica

### TAM (Total Addressable Market)
Mercado total disponivel. O tamanho do mercado inteiro se voce pudesse atender 100% dele.

**Para PMEs brasileiras, o TAM geralmente e:**
- O faturamento total do segmento no Brasil
- Ou o numero total de empresas no segmento x ticket medio anual

### SAM (Serviceable Addressable Market)
Mercado enderecavel. A fatia do TAM que voce PODE atingir considerando restricoes reais.

**Filtros comuns para PMEs:**
- Regiao geografica (cidade, estado, regiao)
- Porte do cliente (micro, pequena, media)
- Perfil de cliente (B2B vs B2C, segmento especifico)
- Canal de distribuicao disponivel
- Capacidade operacional atual

### SOM (Serviceable Obtainable Market)
Mercado obtenivel. A fatia do SAM que a empresa realisticamente consegue capturar dada sua oferta, posicionamento e a concorrencia real.

**Duas leituras possiveis — escolha uma e seja explicito:**

**(a) SOM de mercado (recomendado para diagnostico estrategico):** teto tangivel de captura, sem horizonte temporal e sem restricao de capacidade interna. Representa o potencial que o mercado permite a uma empresa plenamente consolidada no seu nicho. Util para discussao estrategica com a cliente — mostra quanto ela PODE atingir se toda a execucao for correta.

**(b) SOM operacional (mais conservador):** fatia capturavel em horizonte definido (12-24 meses) considerando capacidade atual, budget de marketing e ciclo de venda. Util para forecast de curto prazo e metas operacionais.

**Premissas realistas para PMEs:**
- Para SOM de mercado: share tipico 3-8% do SAM para empresa de nicho bem posicionada; 8-15% para lider do quadrante premium com diferenciacao real; 15-25% para dominante estrutural.
- Para SOM operacional: 1-5% do SAM para empresas novas, 5-15% para empresas estabelecidas, em horizonte de 12-24m.
- **NUNCA derive o SOM da meta comercial do cliente.** Meta do cliente e aspiracao operacional, nao metrica de mercado. Ver secao dedicada abaixo.

---

## Camada intermediaria: MERCADO ENDERECAVEL

O TAM/SAM/SOM classico tem 3 camadas, mas muitas vezes uma 4a camada pedagogica — o **Mercado Enderecavel** — ajuda a separar duas barreiras diferentes que senao se misturam.

### O que e

Subset do SAM onde a oferta da empresa e RELEVANTE, dada a decisao estrategica de perfil. Nao e todo o SAM — exclui segmentos que a empresa decide NAO perseguir (commodity, ocasional, fora do ICP).

### Quando usar

- Quando o SAM tem perfis de consumidor muito heterogeneos (premium vs medio vs ocasional/commodity)
- Quando a empresa explicitamente NAO compete em parte do SAM (decisao de posicionamento)
- Quando o ratio SOM/SAM fica baixo (5-15%) e isso poderia parecer "empresa captura pouco" — mas na verdade ela nao mira o SAM inteiro por desenho

### Como calcular

```
Mercado Enderecavel = SAM × % do SAM relevante a oferta da empresa
Razao SOM/Enderecavel = quanto a empresa captura DO QUE ela persegue
```

Ratio SOM/Enderecavel e metrica mais honesta para medir performance competitiva:
- 20-40% = empresa lider do seu nicho
- 10-20% = empresa competitiva mas nao dominante
- <10% = empresa com grande espaco para crescer dentro do seu proprio quadrante

### Separa duas barreiras distintas

Sem essa camada, SAM → SOM mistura:
1. **Barreira de escolha estrategica** (SAM → Enderecavel): empresa decide nao competir em partes do SAM
2. **Barreira competitiva** (Enderecavel → SOM): dentro do perfil alvo, empresa disputa com concorrentes

Com a camada separada, fica visivel O QUE a empresa escolheu deixar de fora vs O QUE a concorrencia disputa dela.

### Exemplo (hipotético)

```
SAM: R$ 34M (todo o mercado regional do segmento)
  ├─ Premium:                  R$ 17,1M (50% do gasto) ← a empresa compete aqui
  ├─ Medio regular:            R$ 10,2M (30% do gasto) ← parte upgrade para a empresa
  └─ Ocasional/commodity:      R$  6,7M (20% do gasto) ← a empresa NAO compete

Mercado Enderecavel: R$ 20M (premium completo + 20% do medio que upgrade)
SOM: R$ 7M (35% do enderecavel — empresa lider do quadrante)
```

Razao SOM/SAM = 20,6% (parece baixa)
Razao SOM/Enderecavel = 35% (captura real do que ela persegue — lider de nicho)

### Quando NAO usar

- Quando a empresa mira todo o SAM indiferentemente (ex: commodity puro)
- Quando o SAM e homogeneo (sem subsegmentos claros de gasto)
- Quando adicionar a camada complica a comunicacao sem agregar clareza estrategica

---

## SOM vs Capacidade Operacional vs Meta Comercial — tres metricas distintas

Confundir essas tres e erro comum. Separe-as explicitamente:

### SOM (metrica de mercado)
Teto tangivel de captura dado posicionamento + competicao. INDEPENDENTE de capacidade interna ou prazo da empresa.

### Capacidade operacional (restricao interna)
Teto de producao dada a estrutura atual (equipe, instalacoes, agenda). Se SOM > capacidade, a diferenca flagga necessidade de expansao futura (contratar, 2a unidade, etc).

**Exemplo:**
- SOM de mercado: R$ 7M
- Capacidade atual (3 vets, 1 unidade): R$ 5,4M em regime de agenda cheia
- Gap: R$ 1,6M exigem expansao (2a unidade ou ampliacao)

Registrar como `operational_ceiling_note` separado do SOM. Nunca reduzir o SOM pela capacidade — SOM e sobre mercado, nao sobre a empresa.

### Meta comercial do cliente (aspiracao operacional)
Numero que a cliente registrou no V4MOS, no briefing ou no kickoff como meta de faturamento. **Isso NAO e SOM.**

Se a meta aparecer como "R$ 1,32M ano que vem", ela e uma aspiracao operacional da cliente — pode estar abaixo do SOM (cliente conservadora), acima do SOM (cliente otimista), ou alinhada. **Nao confundir.**

**Regra critica:** registrar a meta do cliente como campo separado (`client_annual_revenue_goal_brl`) com fonte documentada (`client_annual_revenue_goal_source`), e comparar com o SOM na narrativa — nao incorporar no calculo do SOM.

**Fontes tipicas de meta da cliente (podem divergir entre si):**
- Formulario V4MOS (campo "Meta 12M" preenchido pela cliente) → ambicao dela
- Kickoff da V4 (meta mensal negociada com o executor) → versao operacional, as vezes mais conservadora
- Plano de ROI / Rollout → meta intermedia

Se houver duas metas em fontes diferentes, documente as DUAS separadamente. Nao escolha uma arbitrariamente.

---

## Triangulacao metodologica para SOM robusto

Nao chegue a um numero de SOM por um metodo so. **Triangule com 3 metodos independentes** — se os tres convergirem em uma faixa, o numero e defensavel. Se divergirem muito, algo esta errado.

### Metodo 1 — Capacidade operacional plenamente madura (bottom-up da estrutura)

Responde: "qual o teto produtivo da empresa em agenda cheia + ticket otimizado?"

Para servicos presenciais (clinicas, consultorios, restaurantes):
```
Capacidade = (unidades produtivas) × (consultas/atendimentos por dia) × (dias uteis/mes) × 12
Receita total = Capacidade × ticket medio × fator de servicos complementares
  (fator tipico: 1/0.6 = 1.67 se consulta e 60% da receita; ajuste por modelo)
```

**Exemplo hipotético:**
- 3 profissionais × 2.400 atendimentos/ano = 7.200 atendimentos
- × R$ 450 ticket medio = R$ 3,24M em atendimentos
- ÷ 0,6 (atendimentos = 60% da receita) = R$ 5,4M teto operacional

### Metodo 2 — Market share top-down (benchmark de nicho)

Responde: "qual fatia do SAM regional uma empresa de nicho similar tipicamente captura quando plenamente consolidada?"

Use benchmarks:
- Generalista mediana: 1-3%
- Diferenciada com posicionamento claro: 3-5%
- Lider do quadrante de nicho: **5-12%**
- Dominante estrutural (ex: hospital 24h em cidade pequena): 15-25%

Aplique o % apropriado ao SAM.

### Metodo 3 — Segmento premium por nicho (bottom-up do mercado)

Responde: "de dentro do SAM, qual fatia corresponde ao nicho-alvo da empresa, e quanto desse nicho ela pode capturar?"

Passos:
1. Decomponha o SAM por perfil de gasto (premium vs medio vs ocasional)
2. Identifique qual fatia corresponde ao ICP alvo (ex: premium humanizado)
3. Dentro do nicho-alvo, estime captura realista (30-60% se lider, 15-30% se competitivo)

### Convergencia

Se Metodo 1 → R$ X, Metodo 2 → R$ Y, Metodo 3 → R$ Z e `X ≈ Y ≈ Z`, a faixa e defensavel. Use o ponto medio como SOM.

Se divergirem muito (ex: X=R$1M, Y=R$5M, Z=R$3M), investigue:
- Capacidade pode estar bloqueando crescimento → plano de expansao
- Benchmark de market share pode estar errado → recalibrar
- Segmento alvo pode estar mal definido → revisar ICP

---

## Segmentacao heterogenea do SAM

SAM calculado como "media simples × populacao" esconde heterogeneidade que muda tudo. Em setores de servico:

| Segmento | % tipico dos consumidores | % do gasto total | Gasto medio anual |
|---|---|---|---|
| Premium humanizado | 15-20% | 40-55% | 3-10× a media do SAM |
| Medio regular | 30-40% | 25-35% | ~= media do SAM |
| Ocasional/commodity | 40-50% | 10-20% | 1/3 a 1/2 da media |
| Subsistencia / nao-consumo | 3-8% | <5% | negligivel |

**Implicacoes:**
1. Se a empresa mira **premium humanizado**, o verdadeiro mercado enderecavel pode ser 40-55% do SAM, nao 15-20% (porque cada consumidor premium gasta muito mais)
2. Se o SAM foi calculado com media simples (R$ X por domicilio), o numero subestima o mercado para empresas premium. Considere recalibrar ou usar a camada enderecavel.
3. **No premium humanizado**, o mix entre sub-segmentos (ex: gato vs cao no pet) pode divergir do mix nacional. Ex: Gen Z/Millennial humanizado tende a ter mais gatos que a media brasileira.

## Metodologias de estimativa

### Top-Down (do macro para o micro)
1. Comece com dados macro do setor (IBGE, SEBRAE, associacoes)
2. Aplique filtros de regiao e perfil
3. Estime o share obtenivel

**Quando usar:** Quando ha dados setoriais publicos disponiveis.

**Fontes confiáveis:**
- IBGE — Pesquisa Anual de Servicos, CEMPRE, PNAD
- SEBRAE — Estudos setoriais, DataSEBRAE
- ABComm — E-commerce brasileiro
- ABRASEL — Alimentacao fora do lar
- ABES — Software brasileiro
- Statista — Dados globais com recorte Brasil
- Euromonitor — Mercados de consumo
- BNDES — Relatorios setoriais

### Bottom-Up (do micro para o macro)
1. Estime o numero de potenciais clientes na regiao
2. Multiplique pelo ticket medio
3. Aplique taxa de conversao realista

**Quando usar:** Quando o segmento e muito nicho ou nao ha dados macro.

**Exemplo:**
```
Clientes potenciais na regiao: 500 empresas
Ticket medio mensal: R$ 2.000
Conversao realista: 5% no primeiro ano
SOM = 500 x R$ 2.000 x 12 x 5% = R$ 600.000/ano
```

### Mista (recomendada)
1. Use top-down para TAM e SAM
2. Use bottom-up para SOM
3. Valide cruzando os dois

## Erros comuns ao estimar mercado para PMEs

### Erro 1: TAM inflado
**Errado:** "O mercado de saude no Brasil e R$ 700 bilhoes"
**Correto:** "O mercado de clinicas de estetica no Brasil fatura R$ 12 bilhoes" (segmento especifico)

### Erro 2: SAM sem filtros reais
**Errado:** "Nosso SAM e 50% do TAM"
**Correto:** "Filtrando por Grande Porto Alegre, clinicas com 2-10 funcionarios, com presenca digital: 1.200 clinicas, R$ 3.6 bilhoes"

### Erro 3: SOM otimista demais
**Errado:** "Vamos capturar 20% do SAM no primeiro ano"
**Correto:** "Com 3 vendedores e R$ 5K/mes em midia, estimamos converter 25 clientes novos em 12 meses"

### Erro 4: Fontes genericas
**Errado:** "Segundo pesquisas, o mercado cresce 10% ao ano"
**Correto:** "Segundo o SEBRAE (Perfil dos Pequenos Negocios, 2025), o segmento de beleza e estetica cresceu 8.3% no ultimo ano"

### Erro 5: SOM derivado da meta da cliente
**Errado:** "SOM = triplicar o faturamento atual de R$650K para R$2M em 3 anos"
**Correto:** "SOM de mercado: R$ 7M (20% do SAM, metrica independente da ambicao da empresa). Meta da cliente registrada separadamente: R$ 1,32M/ano (18,9% do SOM — fonte: Formulario V4MOS)"

O SOM precisa ser uma metrica de MERCADO, nao de ambicao interna. Se voce esta usando o numero que a cliente disse como meta, voce perdeu a oportunidade de mostrar a ela o potencial real do mercado — que tipicamente e MAIOR que ela imagina.

### Erro 6: SOM = capacidade operacional
**Errado:** "Ela so tem 1 veterinaria trabalhando, entao o SOM dela e R$ 1,5M (teto produtivo)"
**Correto:** "SOM de mercado: R$ 7M (o mercado permite). Capacidade atual: R$ 1,5M (a empresa produz). Gap de R$ 5,5M = necessidade de expansao futura."

Capacidade e restricao INTERNA, nao de mercado. Deve ser registrada separadamente como `operational_ceiling_note` e NUNCA usada para reduzir o SOM.

### Erro 7: SOM sem triangulacao
**Errado:** "Calculei SOM como 5% do SAM, apenas."
**Correto:** "Triangulei tres metodos: (1) capacidade operacional R$5,4M; (2) market share 10% do SAM = R$3,4M; (3) segmento premium 40% captura = R$3,8M. Convergencia em R$3,5M, usado como SOM."

Um metodo so e chute. Tres metodos independentes que convergem e diagnostico.

### Erro 8: Conflacao entre SOM e "meta 12m"
**Errado:** "SOM em 12 meses e R$ 1,2M (igual a meta do cliente)"
**Correto:** SOM e teto de mercado sem amarra temporal rigida; meta comercial e aspiracao operacional, pode ter horizonte de 12 ou 24 meses.

Se registrar SOM, seja claro sobre a leitura escolhida (mercado vs operacional). Se registrar meta do cliente, registrar com fonte (V4MOS, kickoff, etc).

## Heuristicas por segmento

| Segmento | TAM Brasil estimado | Ticket medio mensal PME | Fontes recomendadas |
|---|---|---|---|
| Odontologia | R$ 45 bi | R$ 1.500-5.000 | CFO, ANS, SEBRAE |
| Clinicas estetica | R$ 12 bi | R$ 2.000-8.000 | ABIHPEC, SEBRAE |
| Imobiliarias | R$ 170 bi | R$ 3.000-10.000 | SECOVI, CRECI |
| Restaurantes | R$ 230 bi | R$ 1.000-3.000 | ABRASEL, ANR |
| Academias | R$ 12 bi | R$ 1.500-4.000 | IHRSA, ACAD |
| E-commerce moda | R$ 55 bi | R$ 2.000-5.000 | ABComm, Neotrust |
| Advocacia | R$ 80 bi | R$ 2.000-6.000 | OAB, CNJ |
| Contabilidade | R$ 25 bi | R$ 800-2.500 | CFC, FENACON |
| Educacao/cursos | R$ 40 bi | R$ 1.500-5.000 | ABED, MEC |
| SaaS B2B | R$ 30 bi | R$ 3.000-15.000 | ABES, Gartner |

**ATENCAO:** Esses valores sao heuristicas para referencia. Sempre busque dados atualizados e cite a fonte especifica.

## Template de apresentacao

```
TAM: R$ [valor]
[Descricao em 1 frase]
Fonte: [nome] ([ano]) — [link se disponivel]

SAM: R$ [valor]
[Descricao em 1 frase]
Filtros: [lista de filtros aplicados]
Calculo: [como chegou no numero]

SOM: R$ [valor] (12 meses)
[Descricao em 1 frase]
Premissas: [lista de premissas]
Calculo: [detalhamento]

Metodologia: [top-down / bottom-up / mista]
Confianca: [alta / media / baixa]
```
