# Setup da Apify para Creative Intelligence

Use este guia quando a coleta precisar executar um Actor da Apify e `APIFY_API_TOKEN` ainda não estiver disponível ou validado.

## 1. Criar a conta e obter o token

1. Acesse a [Apify Console](https://console.apify.com/) e crie ou entre em uma conta.
2. Abra **Settings → API & Integrations**. A documentação oficial também aponta a página [API & Integrations](https://console.apify.com/account#/integrations).
3. Copie o token da conta que pagará e será proprietária das execuções.
4. Não cole o token em chat, código, documentação, URL, commit ou screenshot.
5. Configure-o como `APIFY_API_TOKEN` seguindo [configuracao-segura.md](configuracao-segura.md).

Fonte oficial: [Get started with Apify API](https://docs.apify.com/api/v2/getting-started).

## 2. Validar a credencial sem executar Actor

A Apify oferece `GET /v2/users/me` para validar autenticação. No PowerShell, com a variável já definida:

```powershell
$headers = @{ Authorization = "Bearer $env:APIFY_API_TOKEN" }
$account = Invoke-RestMethod -Method Get -Uri "https://api.apify.com/v2/users/me" -Headers $headers
$account.data.username
```

Resultado esperado: HTTP `200` e identificação da conta. Não imprima o objeto inteiro se ele trouxer dados que não são necessários ao diagnóstico.

## 3. Escolher um Actor

Não fixe um Actor para todos os projetos. Actors do Store são produtos mantidos por terceiros e podem mudar preço, schema, disponibilidade ou política.

Para escolher:

1. Pesquise no [Apify Store](https://apify.com/store) pela fonte necessária.
2. Confirme que a coleta pretendida é permitida e usa dados públicos ou autorizados.
3. Leia README, input schema, changelog, avaliações, última atualização e permissões.
4. Verifique o modelo de preço e quais limites podem ser impostos.
5. Confirme que o output contém identificadores, página, texto, datas, formatos e URLs de mídia necessários.
6. Execute manualmente um teste pequeno na Console antes da automação.
7. Registre `actor_id`, URL, data de validação, versão/build e campos usados em `source-plan.md`.

Um Actor legado pode servir como pista, mas nunca como dependência silenciosa. Revalide-o no Store antes de cada novo template ou após mudança de schema.

## 4. Testar com custo controlado

Faça o primeiro run com:

- um único player;
- uma única URL ou termo;
- status e país definidos;
- menor limite de itens que ainda permita validar o schema;
- `maxItems` ou `maxTotalChargeUsd` quando o Actor e o endpoint aceitarem esses controles.

Antes de executar, informe ao usuário quando houver cobrança relevante. A execução ocorre na conta associada ao token.

## 5. Fluxo da API

O fluxo assíncrono padrão é:

1. `POST /v2/actors/{actorId}/runs` com o input JSON;
2. guardar `runId` e `defaultDatasetId`;
3. acompanhar `GET /v2/actor-runs/{runId}`;
4. após `SUCCEEDED`, ler `GET /v2/datasets/{datasetId}/items`;
5. preservar input, run, dataset, logs e custos conhecidos.

Autentique pelo header, não pelo query string:

```http
Authorization: Bearer <APIFY_API_TOKEN>
```

O header reduz o risco de o token aparecer em histórico e logs de URL. Veja [Apify API v2](https://docs.apify.com/api/v2) e [Run Actor](https://docs.apify.com/api/v2/act-runs-post).

## 6. Configuração que deve ir para o projeto

Registre dados não secretos em `source-plan.md` ou `scope.json`:

```json
{
  "provider": "apify",
  "actor_id": "owner~actor-name",
  "country": "BR",
  "status": "active",
  "max_items": 50,
  "validated_at": "YYYY-MM-DD",
  "input_schema_notes": []
}
```

O token nunca entra nesse JSON.

## 7. Critério de setup concluído

- `APIFY_API_TOKEN` existe apenas no ambiente seguro;
- `GET /users/me` retorna `200`;
- Actor e preço foram revisados;
- teste pequeno produziu dataset compatível;
- run e dataset foram preservados;
- custo e limites foram documentados;
- nenhum segredo apareceu nos artefatos.
