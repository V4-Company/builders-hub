# Setup do Firecrawl para Creative Intelligence

Use este guia quando a coleta precisar ler sites com Firecrawl e `FIRECRAWL_API_KEY` ainda não estiver disponível ou validada.

## 1. Criar a conta e obter a chave

1. Acesse o [Firecrawl](https://www.firecrawl.dev/) e crie ou entre em uma conta.
2. Abra a área de [API Keys](https://www.firecrawl.dev/app/api-keys) no dashboard.
3. Crie ou copie uma chave da equipe que pagará os créditos.
4. Não cole a chave em chat, código, documentação, URL, commit ou screenshot.
5. Configure-a como `FIRECRAWL_API_KEY` seguindo [configuracao-segura.md](configuracao-segura.md).

A referência oficial informa que todas as chamadas usam `Authorization: Bearer` e que a chave é obtida no dashboard: [Firecrawl API v2 — Introduction](https://docs.firecrawl.dev/api-reference/v2-introduction).

## 2. Escolher o endpoint

Use o endpoint mínimo adequado ao objetivo:

- `scrape`: uma página conhecida;
- `map`: descoberta de URLs de um domínio;
- `crawl`: várias páginas do site;
- `search`: busca na web com conteúdo;
- `extract` ou JSON estruturado: somente quando a estrutura adicional for necessária.

Para validar site, título, descrição, texto e links sociais, comece com `scrape`. Não execute `crawl` quando uma ou poucas páginas resolvem o problema, porque isso aumenta custo, tempo e ruído.

## 3. Testar a chave

O teste abaixo faz um scrape real e pode consumir crédito. Execute apenas depois de confirmar o plano:

```powershell
$headers = @{
  Authorization = "Bearer $env:FIRECRAWL_API_KEY"
  "Content-Type" = "application/json"
}
$body = @{
  url = "https://example.com"
  formats = @("markdown")
  onlyMainContent = $true
} | ConvertTo-Json
$result = Invoke-RestMethod -Method Post -Uri "https://api.firecrawl.dev/v2/scrape" -Headers $headers -Body $body
$result.success
```

Resultado esperado: HTTP `200` e `success: true`. Preserve apenas a resposta necessária ao teste; não registre headers.

Referência do endpoint: [Scrape](https://docs.firecrawl.dev/api-reference/endpoint/scrape).

## 4. Configuração inicial recomendada

Para leitura de site oficial:

```json
{
  "url": "https://example.com",
  "formats": ["markdown", "links"],
  "onlyMainContent": true,
  "removeBase64Images": true,
  "blockAds": true,
  "timeout": 30000
}
```

Adicione `waitFor`, localização, proxy, ações ou timeout maior somente quando houver evidência de que a página precisa deles. Parâmetros adicionais podem afetar tempo, custo e comportamento.

## 5. Fluxo de preservação

Para cada chamada, registre sem segredos:

- endpoint e versão;
- URL solicitada;
- parâmetros;
- timestamp;
- status HTTP e `success`;
- request/job ID retornado;
- conteúdo bruto ou referência ao arquivo;
- custo/créditos quando disponíveis;
- fallback utilizado;
- erro e tentativa.

Salve em `02-coleta/raw/firecrawl/<run-id>/` e consolide o status em `collection-log.json`.

## 6. Fallback

Se Firecrawl falhar:

1. registre código, mensagem e parâmetros;
2. consulte [troubleshooting.md](troubleshooting.md);
3. faça retry apenas quando a falha for transitória;
4. para página pública simples, use HTTP direto como fallback permitido;
5. identifique o resultado como `http-fallback`, sem fingir que veio do Firecrawl;
6. não contorne login, paywall, CAPTCHA ou restrição de acesso.

## 7. Critério de setup concluído

- `FIRECRAWL_API_KEY` existe apenas no ambiente seguro;
- um scrape mínimo retorna `200` e `success: true`;
- endpoint e parâmetros foram escolhidos pelo menor escopo necessário;
- créditos e limites foram verificados;
- resposta e log não contêm a chave;
- fallback e política de retry estão definidos.
