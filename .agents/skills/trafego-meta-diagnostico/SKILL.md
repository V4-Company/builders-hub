---
name: trafego-meta-diagnostico
description: Gera diagnostico completo de Meta Ads (Facebook + Instagram) via API V4mos — spend, ROAS, top campanhas, ads com quality_ranking ruim queimando dinheiro, breakdown por plataforma (feed/stories/reels), delta W/W e runway de saldo. Use sempre que o usuario pedir "diagnostico Meta", "relatorio Facebook Ads", "como tao as campanhas", "check-in Meta", "saude da conta FB", "ads com problema", ou quando for montar relatorio pra cliente com dados da ultima semana. Exige variaveis de ambiente V4MOS_CLIENT_ID, V4MOS_CLIENT_SECRET, V4MOS_WORKSPACE_ID. Entrega markdown pronto pra copiar/colar em check-in ou PPT. Google Ads fora do escopo (API V4mos ignora filtro de data no Google — bug reportavel).
area: trafego
author: guilhermelippert
version: 1.0.0
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

## Pre-requisitos — variaveis de ambiente

Antes de rodar, confirme que essas 3 variaveis estao setadas:

```bash
echo "V4MOS_CLIENT_ID=$V4MOS_CLIENT_ID"
echo "V4MOS_CLIENT_SECRET=${V4MOS_CLIENT_SECRET:+<set>}"
echo "V4MOS_WORKSPACE_ID=$V4MOS_WORKSPACE_ID"
```

Se alguma estiver vazia, oriente o usuario a adicionar no `~/.zshrc` (Mac) ou `~/.bashrc` (Linux):

```bash
export V4MOS_CLIENT_ID="<uuid fornecido pela V4mos>"
export V4MOS_CLIENT_SECRET="<hex fornecido>"
export V4MOS_WORKSPACE_ID="<uuid do workspace>"
```

Depois: `source ~/.zshrc` (ou abrir novo terminal). Nao aceite creds no prompt — obriga env vars pra evitar vazar no historico/logs.

## Pre-requisito — dependencia Python

```bash
python3 -c "import requests" 2>/dev/null || pip install requests
```

## Fluxo

### Passo 1 — Coletar parametros do usuario

Pergunte (ou inferir do contexto):

1. **Janela em dias** (default 7). Outras opcoes: 1 (ontem), 14, 30.
2. **Data final** (default: ontem, YYYY-MM-DD). Nunca hoje — V4mos tem D-1 sync e Facebook tem D-3 de latencia; hoje sempre incompleto.
3. **Conta especifica?** (default: todas as contas do workspace). Se o usuario trabalha com varios clientes no mesmo workspace, pergunte o `account_id` da conta do cliente especifico (formato `act_1234567890`).

### Passo 2 — Executar o script

```bash
cd "$(dirname "$0")"  # estar na pasta da skill ajuda o python localizar o script
python3 scripts/diagnostico.py --dias 7
```

Flags disponiveis:
- `--dias N` — janela em dias
- `--ate YYYY-MM-DD` — data final (default ontem)
- `--account-id act_XXX` — filtra conta
- `--out path.md` — destino do arquivo (default: `meta-diagnostico-YYYY-MM-DD.md` no cwd)

O script:
1. Valida env vars (sai com codigo 2 se faltar)
2. Faz fetch paginado de `/v1/facebook/accounts`, `/ads/campaigns` (agora e anterior), `/ads/ad` (agora), `/ads/platform` (agora)
3. Respeita rate limit (30 req/min conservador) e retry com backoff em 429
4. Recalcula CTR como `clicks/impressions` — o campo da API vem quebrado (valores >100%)
5. Monta markdown com todas as secoes
6. Salva `.md` + imprime no stdout

### Passo 3 — Apresentar resultado

Apos rodar, mostre ao usuario:
1. Path do arquivo salvo
2. Os **3-5 insights mais relevantes** destacados dentro do relatorio — nao copie o markdown inteiro no chat, isso vira lixo. Destaque:
   - Spend do periodo + delta vs periodo anterior
   - Quantos ads `BELOW_AVERAGE` e quanto queimaram
   - Top 1 campanha por ROAS (se tiver ROAS > 0)
   - Runway se houver saldo configurado
3. Ofereca proximas acoes:
   > "Quer que eu abra o markdown? Gere versao HTML? Mande pro cliente?"

### Passo 4 — Se a skill for usada dentro de pasta de cliente

Se o cwd for uma pasta `clientes/<nome>/`, sugira salvar dentro de `relatorios/`:

```bash
mkdir -p relatorios
python3 .claude/skills/trafego-meta-diagnostico/scripts/diagnostico.py --dias 7 --out relatorios/meta-diagnostico-$(date -v-1d +%Y-%m-%d).md
```

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
