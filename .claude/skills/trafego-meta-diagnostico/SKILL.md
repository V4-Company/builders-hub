---
name: trafego-meta-diagnostico
description: Gera diagnostico completo de Meta Ads (Facebook + Instagram) via API V4mos — spend, ROAS, top campanhas, ads com quality_ranking ruim queimando dinheiro, breakdown por plataforma (feed/stories/reels), delta W/W e runway de saldo. Use sempre que o usuario pedir "diagnostico Meta", "relatorio Facebook Ads", "como tao as campanhas", "check-in Meta", "saude da conta FB", "ads com problema", ou quando for montar relatorio pra cliente com dados da ultima semana. Le credenciais de clientes/<cliente>/.env (ou bases/<projeto>/.env) por padrao, com fallback pra env vars do shell. Se faltar credencial, orienta onde pegar (https://app.v4mkt.com). Entrega markdown pronto pra copiar/colar em check-in ou PPT. Google Ads fora do escopo (API V4mos ignora filtro de data no Google — bug reportavel).
area: trafego
author: guilhermelippert
version: 1.1.0
---

# /trafego-meta-diagnostico

Puxa Meta Ads do V4mos pra um periodo (default 7 dias) e gera um relatorio markdown com KPIs, deltas W/W, top campanhas, ads problematicos e breakdown de plataforma. Feito pra ser usado diariamente em check-in ou relatorio semanal de cliente.

## Quando usar

Dispara quando o usuario diz:
- "diagnostico Meta dos ultimos X dias"
- "relatorio Facebook Ads"
- "como tao as campanhas da semana"
- "check-in Meta pro cliente Y"
- "quais ads ta com problema"
- "ROAS da semana" (no contexto Meta)
- "saude da conta Facebook"
- "quanto tem de saldo" (no contexto V4mos/FB)

Se o usuario pedir dados Google/Analytics, explique que essa skill e **Meta only** (Google Ads na V4mos ignora o filtro de data, entao a gente nao arrisca numero errado).

## Passo 1 — Identificar o cliente

Antes de qualquer coisa, descubra com qual cliente voce esta trabalhando. Ordem:

1. **Se o usuario nomeou explicitamente** ("diagnostico Meta do cliente X"): use esse nome.
2. **Se o cwd ja esta dentro de `clientes/<nome>/` ou `bases/<nome>/`**: use o nome detectado. Mencione: "Detectei que voce ta dentro da pasta do cliente <nome>. Uso ele?"
3. **Se nao esta claro**: liste os clientes disponiveis (`ls clientes/ | grep -v _template`) e pergunte: "Qual cliente?"

Se o cliente nao existir como pasta ainda, sugira: "Nao encontrei `clientes/<nome>/`. Quer criar com `/novo-cliente` primeiro?"

## Passo 2 — Verificar credenciais no `.env` do cliente

O padrao do Builders Hub e: cada cliente tem seu proprio `.env` em `clientes/<nome>/.env` (copiado de `.env.example` pelo `/novo-cliente`). Esse arquivo e gitignored — fica so local.

Confira o conteudo:

```bash
test -f "clientes/<nome>/.env" && cat "clientes/<nome>/.env" | grep -E "^V4MOS" | sed 's/=.*$/=<set>/' || echo "arquivo nao existe"
```

Deve ter 3 chaves **preenchidas**:
- `V4MOS_CLIENT_ID` — suas credenciais V4er (pode reusar entre clientes)
- `V4MOS_CLIENT_SECRET` — idem
- `V4MOS_WORKSPACE_ID` — **especifico do cliente** (cada cliente tem um workspace diferente no V4mkt)

### Se faltar alguma chave

Oriente o usuario passo a passo:

> "Faltam credenciais V4mos no `clientes/<nome>/.env`. Onde pegar:
> 
> 1. Acesse **https://app.v4mkt.com** logado com sua conta V4
> 2. Selecione o workspace deste cliente (V4 Marketing Operating System)
> 3. Va em **Settings > API / Integracoes > gerar client credentials**
> 4. Copie `client_id`, `client_secret` e o `workspace_id` do cliente
> 5. Abre `clientes/<nome>/.env` e preenche as linhas vazias
> 
> Se nao encontrar o caminho no painel, fala com **matheus.netto@v4company.com** (contato do time de API V4mos).
> 
> Depois de preencher, roda a skill de novo."

`V4MOS_CLIENT_ID`/`SECRET` sao os mesmos em todos os clientes (sao suas credenciais V4er). So o `WORKSPACE_ID` muda por cliente. Se o usuario ja tem as 2 primeiras em outro `.env` ou no `~/.zshrc`, pode reusar.

### Alternativa: env vars do shell

Se o usuario preferir setar `V4MOS_CLIENT_ID` e `V4MOS_CLIENT_SECRET` no `~/.zshrc` (uma vez, vale pra todos os clientes):

```bash
echo 'export V4MOS_CLIENT_ID="..."' >> ~/.zshrc
echo 'export V4MOS_CLIENT_SECRET="..."' >> ~/.zshrc
source ~/.zshrc
```

Nesse caso, o `.env` do cliente so precisa do `V4MOS_WORKSPACE_ID`. O script mistura as duas fontes (shell vence pra CLIENT_ID/SECRET, arquivo vence pra WORKSPACE_ID).

## Pre-requisito — dependencia Python

```bash
python3 -c "import requests" 2>/dev/null || pip install requests
```

## Fluxo

### Passo 3 — Coletar parametros do periodo

Pergunte (ou inferir do contexto):

1. **Janela em dias** (default 7). Outras opcoes: 1 (ontem), 14, 30.
2. **Data final** (default: ontem, YYYY-MM-DD). Nunca hoje — V4mos tem D-1 sync e Facebook tem D-3 de latencia; hoje sempre incompleto.
3. **Conta especifica?** (default: todas as contas do workspace). Se o workspace tem varias contas FB, pergunte o `account_id` especifico (formato `act_1234567890`).

### Passo 4 — Executar o script

**Se o cwd ja esta dentro de `clientes/<nome>/`:**

```bash
mkdir -p relatorios
python3 .claude/skills/trafego-meta-diagnostico/scripts/diagnostico.py \
  --dias 7 \
  --out "relatorios/meta-diagnostico-$(date -v-1d +%Y-%m-%d).md"
```

**Se estiver no root do builders-hub ou fora da pasta do cliente:**

```bash
python3 .claude/skills/trafego-meta-diagnostico/scripts/diagnostico.py \
  --cliente "<nome-do-cliente>" \
  --dias 7
```

O script vai:
1. Ler `clientes/<cliente>/.env` pra pegar `V4MOS_WORKSPACE_ID` (prioridade)
2. Mesclar com `V4MOS_CLIENT_ID`/`SECRET` do shell (se setados no ~/.zshrc)
3. Se qualquer chave faltar, imprime erro com link pra V4mkt e sai com exit=2
4. Fazer fetch paginado de `/v1/facebook/accounts`, `/ads/campaigns` (agora e anterior), `/ads/ad` (agora), `/ads/platform` (agora)
5. Respeitar rate limit (30 req/min conservador) e retry com backoff em 429
6. Recalcular CTR como `clicks/impressions` (campo da API vem quebrado)
7. Montar markdown com todas as secoes + salvar no `--out` (ou `meta-diagnostico-YYYY-MM-DD.md` no cwd se nao especificar)

Flags disponiveis:
- `--cliente NOME` — nome da pasta em `clientes/` (nao precisa se cwd ja ta dentro)
- `--dias N` — janela em dias (default 7)
- `--ate YYYY-MM-DD` — data final (default ontem)
- `--account-id act_XXX` — filtra conta FB especifica do workspace
- `--out path.md` — destino do arquivo

### Passo 5 — Apresentar resultado

Apos rodar, mostre ao usuario:
1. Path do arquivo salvo
2. Os **3-5 insights mais relevantes** destacados dentro do relatorio — nao copie o markdown inteiro no chat, isso vira lixo. Destaque:
   - Spend do periodo + delta vs periodo anterior
   - Quantos ads `BELOW_AVERAGE` e quanto queimaram
   - Top 1 campanha por ROAS (se tiver ROAS > 0)
   - Runway se houver saldo configurado
3. Ofereca proximas acoes:
   > "Quer que eu abra o markdown? Gere versao HTML? Mande pro cliente?"

Isso mantem o historico de diagnosticos por cliente.

## Interpretacao dos outputs — guia pro Claude apresentar

### Quality ranking
A API Facebook retorna graduacoes finas — nao so 3 niveis:
- `ABOVE_AVERAGE` (🟢): acima da mediana do leilao
- `AVERAGE` (🟡): mediano
- `BELOW_AVERAGE_10`, `BELOW_AVERAGE_20`, `BELOW_AVERAGE_35` (🔴): graduacoes do pior tercil. `_35` significa o ad ta no bottom 35% do leilao — custa mais caro pra entregar a mesma coisa.
- `UNKNOWN` (⚪): pouca impressao pra calcular (ad novo ou pouco rodado)

O script filtra a secao "⚠️ Ads BELOW_AVERAGE" com prefix match, entao pega todas as graduacoes ruins juntas.

### ROAS 0 nao significa ROAS ruim
`website_purchase_roas` **so captura compras online**. Campanhas de lead-gen, trafego, engajamento vao aparecer com ROAS=0 — nao e bug, e escopo. Se o cliente so tem lead-gen, o ROAS nao e metrica util aqui; use CPL (custo por lead) via `/ads/actions`.

### CTR recalculado
A API V4mos retorna `ctr` com valores >100% (bug conhecido). O script recalcula como `clicks / impressions`. **Nao use o campo ctr da resposta cru**.

### Runway de saldo
Formula simples: `balance / (spend_periodo / dias)`. Assume que o ritmo atual continua. Nao substitui analise de pacing com lamas de campanha.

## Limitacoes conhecidas

1. **Google Ads fora**: a API V4mos ignora `dateStart`/`dateEnd` em todos os endpoints Google testados. Entregar numero errado e pior que nao entregar. Se quiser cobrir Google, apontar pra API direta do Google Ads ou esperar fix do V4mos (reportavel via matheus.netto@v4company.com).
2. **D-3 de latencia**: dados de ontem podem estar incompletos. Para certeza 100%, use janela de 3-7 dias atras.
3. **Sync 1x/dia**: numeros mudam so uma vez por dia (madrugada SP).
4. **Cache 30min**: o V4mos guarda resposta por 30min. Rodar 2x em sequencia retorna igual.
5. **5000 rows/pagina**: workspaces grandes com muitas contas podem precisar de paginacao longa. A skill pagina automaticamente.

## Pos-processamento opcional

Se o usuario pedir PPT/HTML a partir do markdown, ele pode:
- Invocar `/frontend-design` apontando pro arquivo md gerado
- Ou invocar uma skill futura `cs-checkin-ppt` (se existir) com o md como input

Nao misture isso dentro dessa skill — essa skill entrega markdown e ponto.
