---
name: v4mos-dados-meta-ads
description: Puxa qualquer dado de Meta Ads (Facebook + Instagram) via API V4mos pra um cliente especifico. Use sempre que o usuario pedir dado de Meta Ads — metricas de campanhas, anuncios, keywords, breakdowns por plataforma/regiao/demografia, saldo de conta, ROAS, quality ranking. Aceita perguntas em linguagem natural ("ads que gastaram mais essa semana", "saldo da conta", "ROAS dos ultimos 30 dias") e traduz em fetch certo. Depois de puxar, pergunta ao usuario COMO quer consumir (conversar, HTML, CSV, PDF) e entrega no formato ideal — HTML/PDF delega pra /frontend-design. Credenciais ficam em clientes/<cliente>/.env; se faltar, pergunta e salva.
area: v4mos
author: guilhermelippert
version: 2.0.0
---

# /v4mos-dados-meta-ads

Puxador inteligente de dados Meta Ads via V4mos. Escolhe endpoint + filtros com base na pergunta do usuario, roda o script, entrega no formato que faz sentido.

Substituiu `trafego-meta-diagnostico` (que era rigido, entregava so 1 tipo de relatorio). Agora 1 skill cobre **qualquer** pergunta sobre Meta Ads — basta orquestrar direito.

## Quando usar

Dispara quando o usuario pede qualquer dado de Meta Ads:
- "top campanhas por spend"
- "ads com quality ruim"
- "ROAS dos ultimos 30 dias"
- "saldo da conta"
- "quanto gastei em stories vs feed"
- "diagnostico/overview Meta da semana"
- "exporta CSV das campanhas"
- "gera dashboard do mes"
- "relatorio Meta pro cliente X"

Nao use pra: Google Ads (API V4mos quebrada nisso — ignora filtro de data), GA4 (nao existe na V4mos), CRM (outros prefixos).

## Passo 1 — Identificar o cliente

Antes de qualquer coisa, descubra com qual cliente esta trabalhando:

1. **Se usuario nomeou explicitamente** → usa.
2. **Se cwd dentro de `clientes/<nome>/` ou `bases/<nome>/`** → usa detectado. Confirma: "Esta trabalhando no cliente <nome>?"
3. **Se ambiguo** → liste `ls clientes/ | grep -v _template` e pergunte.
4. **Se cliente nao existe como pasta** → oferece `/novo-cliente` primeiro.

## Passo 2 — Verificar credenciais

O script le automaticamente `clientes/<cliente>/.env`. Se faltar alguma chave e stdin for TTY, o proprio script pergunta e salva. Se voce (Claude) estiver orquestrando sem TTY, faz manualmente:

1. Confere `clientes/<cliente>/.env`:
   ```bash
   cat "clientes/<cliente>/.env" | grep -E "^V4MOS" | sed 's/=.*$/=<set>/'
   ```

2. Se algo faltar, peca ao usuario:
   > "Pra puxar Meta Ads do <cliente> preciso das credenciais V4mos. Pega em:
   > **https://v4marketing.mktlab.app/configuracoes/api-dados**
   > (logado, com workspace do cliente selecionado). Me manda:
   > - Client ID
   > - Client Secret
   > - Workspace ID"

3. Com os valores em mao, edite `clientes/<cliente>/.env` via Edit tool, preservando comentarios.

Reuso: `V4MOS_CLIENT_ID`/`SECRET` sao seus (V4er) — valem pra todos os clientes. So `WORKSPACE_ID` muda.

## Passo 3 — Interpretar o pedido

Traduza a pergunta do usuario em:
- **Endpoint** (alias curto ou path completo)
- **Janela** (`--days N`, ou `--since`/`--until` se periodo especifico)
- **Filtros** (`--where field OP value`)
- **Ordenacao** (`--order-by field --order-dir DESC`)
- **Campos** (`--fields f1,f2,f3` pra enxugar)

Se a pergunta for ambigua (ex: "me mostra as campanhas"), pergunte: janela? ordenado por que? quantas?

## Passo 4 — Executar o script

**De dentro de `clientes/<cliente>/`:**
```bash
python3 .claude/skills/v4mos-dados-meta-ads/scripts/v4mos_meta.py <endpoint> [flags]
```

**De fora:**
```bash
python3 .claude/skills/v4mos-dados-meta-ads/scripts/v4mos_meta.py <endpoint> --cliente <nome> [flags]
```

### Endpoints (aliases curtos aceitos)

| Alias | Path completo | O que tem |
|---|---|---|
| `accounts` | `/v1/facebook/accounts` | Conta: balance, amount_spent, spend_cap, status |
| `campaigns` | `/v1/facebook/ads/campaigns` | Metricas agregadas por campanha |
| `adset` | `/v1/facebook/ads/adset` | Metricas por conjunto de anuncios |
| `ad` | `/v1/facebook/ads/ad` | Metricas por anuncio + quality/engagement/conversion rankings + website_purchase_roas |
| `creatives` | `/v1/facebook/ads/creatives` | Criativos usados |
| `actions` | `/v1/facebook/ads/actions` | Acoes/conversoes por tipo |
| `demographic` | `/v1/facebook/ads/demographic` | Breakdown idade/genero |
| `platform` | `/v1/facebook/ads/platform` | Breakdown facebook/instagram/messenger + posicao (feed/stories/reels) |
| `region` | `/v1/facebook/ads/region` | Breakdown geografico |

### Flags principais

- `--days N` — janela em dias terminando ontem (atalho comum)
- `--since/--until` — override explicito (YYYY-MM-DD)
- `--account act_XXX` — filtra conta FB
- `--order-by FIELD --order-dir DESC` — ordenacao da API
- `--limit N` — rows por pagina (max 5000)
- `--max N` — cap total apos paginacao
- `--fields f1,f2,f3` — subset de colunas
- `--where 'field OP value'` — filtro client-side; pode repetir (AND); ops: `=`, `!=`, `>`, `<`, `>=`, `<=`, `~` (contains), `^` (startswith)
- `--format json|csv|table|md` — default: `table` no TTY, `json` se pipe ou --out
- `--out path` — salva em arquivo

### Exemplos de comandos

| Pergunta | Comando |
|---|---|
| top 10 campanhas por spend 7d | `v4mos_meta.py campaigns --days 7 --order-by spend --order-dir DESC --max 10` |
| ads com quality ruim na semana | `v4mos_meta.py ad --days 7 --where 'quality_ranking~BELOW' --fields ad_name,spend,ctr_calc,quality_ranking` |
| stories vs feed 30d | `v4mos_meta.py platform --days 30` |
| saldo da conta | `v4mos_meta.py accounts --fields name,balance,amount_spent --format table` |
| exporta mes pra CSV | `v4mos_meta.py ad --days 30 --format csv --out relatorios/ads-mes.csv` |
| ads caros sem resultado | `v4mos_meta.py ad --days 7 --where 'spend>1000' --where 'ctr_calc<0.005'` |

## Passo 5 — Perguntar o objetivo + entregar

**Se o prompt original NAO deixou claro** o que o usuario quer fazer com os dados, pergunte:

> "Peguei os dados (N linhas, periodo X). Como prefere consumir?
>
> 1. **Conversar** — te aponto o que chama atencao, sugiro acoes. Bom pra decidir.
> 2. **HTML** — pra apresentar ou mandar pro cliente. Me diz o objetivo.
> 3. **CSV** — pra Excel ou analise offline.
> 4. **PDF** — documento fechado enviavel.
>
> (Ou me diz o que voce quer e eu adapto.)"

**Se o prompt ja deixou claro** ("gera CSV", "me conta", "quero PPT"), pula a pergunta.

### Opcao 1 — Conversar

Carrega os dados no contexto e analisa. Aponta:
- Anomalias (spend explodiu, CTR caiu, ranking virou vermelho)
- Top performers vs underperformers
- Comparacao com periodo anterior (se rodou duas janelas)
- 2-3 acoes concretas sugeridas

Abre pra perguntas do usuario. Nao gera arquivo.

### Opcao 2 — HTML

Pergunta o **objetivo** antes de renderizar:
- **Apresentacao ao vivo** (board/reuniao) → slide deck 16:9, navegacao setas, Bebas Neue oversized
- **Dashboard executivo** → 1 pagina com KPIs destacados, bom de abrir sempre
- **Relatorio pra enviar** → layout editorial clean, printavel
- **Pra site proprio** → clean, responsivo

Depois invoca `/frontend-design` passando:
- Os dados brutos (JSON)
- O objetivo escolhido
- Identidade V4 como base (Bebas Neue + Montserrat, #1a1a1a/#fff/#e50914)

O rendering HTML fica **100% na /frontend-design** — essa skill nao tem codigo de UI.

Salva o `.html` em `clientes/<cliente>/relatorios/` se aplicavel.

### Opcao 3 — CSV

Direto: `--format csv --out relatorios/meta-<data>.csv`. Mostra path e abre.

### Opcao 4 — PDF

Pipeline: dados → HTML via `/frontend-design` → Chrome headless:

```bash
google-chrome --headless --disable-gpu --print-to-pdf=<output>.pdf file://<html>
# ou em Mac com Chrome instalado:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --headless --disable-gpu --print-to-pdf=<output>.pdf file://<html>
```

Se Chrome nao estiver instalado, oferece fallback: "Gerei o HTML em X. Abre no navegador e usa Ctrl+P > Salvar PDF."

## Workflows comuns (presets)

### "Diagnostico Meta semana" (substitui v1.2.0)

Cadeia de 4 fetches + analise:

```bash
# 1. Contas (saldo + spend total)
v4mos_meta.py accounts --format json --out /tmp/accounts.json

# 2. Campanhas periodo atual + anterior (W/W delta)
v4mos_meta.py campaigns --days 7 --format json --out /tmp/camp-now.json
v4mos_meta.py campaigns --since $(date -v-14d +%F) --until $(date -v-8d +%F) --format json --out /tmp/camp-prev.json

# 3. Ads com ranking ruim
v4mos_meta.py ad --days 7 --where 'quality_ranking~BELOW' --format json --out /tmp/ads-bad.json

# 4. Breakdown plataforma
v4mos_meta.py platform --days 7 --format json --out /tmp/plat.json
```

Depois Claude analisa os 4 JSONs e entrega conforme passo 5 (conversar / HTML / CSV / PDF).

### "Relatorio mensal cliente"

Similar mas com `--days 30`. Output default: HTML relatorio pra enviar via /frontend-design.

### "Auditoria criativos"

```bash
v4mos_meta.py ad --days 30 --order-by spend --order-dir DESC --max 50 \
  --fields ad_name,spend,ctr_calc,cpm,quality_ranking,engagement_rate_ranking,conversion_rate_ranking,website_purchase_roas \
  --format table
```

Identifica criativos caros com metricas ruins. Sugere pausar/renovar.

## Gotchas importantes

### CTR vem quebrado da API
O campo `ctr` retornado pela V4mos vem com valores >100% em varias linhas (bug). O script calcula `ctr_calc = clicks / impressions` automaticamente em endpoints que tem os dois campos. **Use `ctr_calc`, nao `ctr`** em filtros e outputs.

### Quality ranking tem graduacoes finas
A API retorna `BELOW_AVERAGE_10`, `BELOW_AVERAGE_20`, `BELOW_AVERAGE_35` (pior tercil) — nao so `BELOW_AVERAGE`. Use filtro com `~BELOW` pra pegar todas as graduacoes ruins juntas.

### ROAS so captura compras online
`website_purchase_roas` **nao conta leads/conversoes custom**. Campanhas lead-gen vao aparecer com ROAS=0 — nao e bug, e escopo do campo. Pra lead-gen use endpoint `actions` com filtros especificos.

### Account status tem significados
- `ACTIVE` — pode rodar
- `DISABLED`, `UNSETTLED` — bloqueada (verificar saldo)
- `CLOSED`, `PENDING_REVIEW` — problema administrativo

## Limitacoes

- **D-3 de latencia** do proprio Facebook + **sync diario V4mos** (madrugada SP). Dados de hoje sempre incompletos; do dia anterior podem ainda faltar ultimas horas. Padrao seguro: pedir dados ate 3 dias atras pra garantir fechamento.
- **Cache 30min** do V4mos — dois fetches seguidos retornam igual.
- **100 req/min** por credencial. Script dorme 2s entre requests (30 req/min conservador).
- **5000 rows/pagina max** — paginacao automatica.
- Google Ads e Google Analytics: **fora de escopo**. API V4mos ignora filtro de data no Google.

## Debug

- `--format json` pra ver estrutura crua
- `--limit 1 --max 1` pra testar autenticacao sem baixar muito
- Exit 2 + mensagem de credencial faltando → conferir `.env`
- HTTP 500 em alguns endpoints (raro) → tratado como 0 rows
- Se resultado ficar estranho, checar se a API honrou `--order-by` ou se precisa reordenar client-side (alguns endpoints ignoram `orderBy`)
