# Troubleshooting da coleta

Use este guia depois de registrar fonte, endpoint, parâmetros, timestamp, status e mensagem sanitizada. Nunca inclua tokens no diagnóstico.

## Sequência de diagnóstico

1. Confirme que a variável esperada existe sem imprimir o valor.
2. Valide a conta com o teste mínimo do guia de setup.
3. Confira endpoint, versão e método HTTP.
4. Compare o payload com o schema atual da fonte ou Actor.
5. Verifique créditos, limites, concorrência e preço.
6. Reduza o teste para uma URL, termo ou item.
7. Consulte o log do run/job.
8. Faça retry somente para falha transitória.
9. Preserve o erro e use fallback permitido quando aplicável.

## Apify

### `401` ou `403`

Possíveis causas:

- token ausente, inválido ou revogado;
- Actor privado ou sem permissão;
- ID nominal exigindo autenticação;
- recurso pertencente a outra conta.

Ações:

- execute `GET /v2/users/me`;
- confirme a conta e o Actor na Console;
- use header `Authorization: Bearer`;
- não mova o token para a URL como tentativa de correção.

### Run `FAILED`, `TIMED-OUT` ou `ABORTED`

- abra o log do run;
- registre `runId`, status e última mensagem sanitizada;
- valide input schema e tipos;
- reduza itens, páginas, timeout ou memória somente conforme a causa;
- não repita automaticamente uma falha determinística.

### Run `SUCCEEDED`, mas dataset vazio

- revise termos, URLs, país, status e datas;
- valide se a página oficial é a mesma usada pelo Actor;
- confira se o output foi salvo em dataset ou key-value store;
- teste o mesmo input manualmente na Console;
- registre “zero observado” sem concluir ausência definitiva.

### Custo acima do esperado

- pare novos runs;
- confira o modelo de preço do Actor;
- reduza `maxItems`;
- use `maxTotalChargeUsd` quando suportado;
- evite múltiplos aliases redundantes;
- reaproveite dataset existente antes de repetir a coleta.

### Schema mudou

- preserve o payload bruto;
- compare amostras antiga e nova;
- atualize a normalização com versão;
- não substitua campos ausentes por valores inventados;
- execute um teste pequeno antes do lote completo.

Referências: [Apify API v2](https://docs.apify.com/api/v2) e [Run Actor and retrieve data](https://docs.apify.com/academy/api/run-actor-and-retrieve-data-via-api).

## Firecrawl

### `400`

Revise corpo JSON, formatos e parâmetros. Remova opções avançadas e volte ao scrape mínimo.

### `401`

A chave está ausente ou inválida. Refaça o setup e confirme `Authorization: Bearer`.

### `402`

O plano ou os créditos não cobrem a chamada. Não faça loop de retries; informe o bloqueio e peça ajuste do plano ou redução do escopo.

### `408` ou `SCRAPE_TIMEOUT`

- confirme que a URL abre;
- reduza formatos e ações;
- use `waitFor` apenas se necessário;
- aumente o timeout dentro do limite documentado;
- tente uma vez com backoff antes do fallback.

### `429`

- respeite limite de taxa e concorrência do plano;
- reduza paralelismo;
- aplique backoff exponencial com jitter;
- não reinicie o lote inteiro;
- retome a partir do último item concluído.

### `5xx` ou falha de engine

- trate como potencialmente transitório;
- faça poucas tentativas com backoff;
- registre request ID e erro;
- use HTTP direto para página pública simples quando permitido;
- não contorne autenticação, CAPTCHA, paywall ou restrição.

Referências: [Firecrawl API v2](https://docs.firecrawl.dev/api-reference/v2-introduction) e [Scrape](https://docs.firecrawl.dev/api-reference/endpoint/scrape).

## Downloads de mídia

### URL expirou ou retorna `403`

- tente baixar logo após a coleta;
- preserve a URL original e o erro;
- recupere novo payload somente se o custo e o snapshot justificarem;
- não marque o asset como inexistente quando o problema for expiração.

### Mesmo arquivo aparece várias vezes

- deduplique URL dentro do run;
- no processamento, deduplique conteúdo por SHA-256;
- mantenha todos os anúncios relacionados ao mesmo hash.

### Arquivo incompleto

- valide status, MIME type e bytes;
- use download temporário e renomeie somente após conclusão;
- descarte o temporário corrompido;
- registre tentativas e checksum quando disponível.

## Quando usar fallback HTTP

Use somente quando:

- a página é pública e simples;
- a política do site permite acesso;
- não há login, CAPTCHA ou paywall;
- o objetivo é conteúdo básico que HTTP direto consegue fornecer.

Identifique `source: http-fallback`, preserve HTML e status e explique por que Firecrawl não foi usado. O fallback não pode ser apresentado como resultado do provedor principal.

## Quando parar

Interrompa e peça ação do usuário quando:

- credencial ou autorização está ausente;
- créditos precisam ser comprados;
- a fonte mudou termos ou bloqueou o uso pretendido;
- o Actor desapareceu ou exige escolha comercial diferente;
- três tentativas consecutivas repetem a mesma condição não transitória;
- continuar ampliaria custo sem evidência de solução.
