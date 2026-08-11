---
name: geral-creative-intelligence-coleta
description: Coleta e normaliza sites, páginas oficiais, anúncios e assets para projetos Creative Intelligence, preservando payloads brutos, parâmetros, logs e validação de marca. Use sempre que uma entrega precisar puxar evidências competitivas públicas, inventariar anúncios ou atualizar um snapshot de benchmark criativo.
area: geral
author: fabiojoseaiello-alt
version: 1.1.0
---

# Creative Intelligence — Coleta

Construa uma base reproduzível. A coleta deve permitir refazer números, explicar exclusões e atualizar o snapshot sem depender da memória de quem executou.

## Pré-requisitos

- Leia `01-descoberta/scope.json`, `concorrentes.csv` e `source-plan.md`.
- Leia [references/configuracao-segura.md](references/configuracao-segura.md) antes de configurar qualquer credencial.
- Se a fonte escolhida for Apify e a conta ou chave ainda não estiver pronta, leia [references/setup-apify.md](references/setup-apify.md) por inteiro.
- Se a fonte escolhida for Firecrawl e a conta ou chave ainda não estiver pronta, leia [references/setup-firecrawl.md](references/setup-firecrawl.md) por inteiro.
- Em caso de falha de autenticação, crédito, limite, Actor, scrape ou download, leia [references/troubleshooting.md](references/troubleshooting.md).
- Valide credenciais por variáveis de ambiente; não abra, imprima nem exponha valores secretos.
- Use apenas o ambiente do projeto atual. Nunca carregue `.env` de outro cliente ou de um caminho legado fixo.
- Confirme antes de iniciar operações externas de custo material.
- Reutilize runs preservados quando parâmetros e snapshot forem compatíveis.

## Estratégia de fontes

Priorize fontes oficiais e APIs adequadas. Um stack comum pode combinar:

- leitura de sites para título, posicionamento e links sociais;
- biblioteca pública de anúncios ou coletor autorizado;
- páginas oficiais para confirmar identidade;
- download das URLs de mídia enquanto estiverem válidas.

Quando uma ferramenta falhar, registre o erro e use fallback permitido, como leitura HTTP direta de uma página pública. Não contorne autenticação, paywall, bloqueio técnico ou restrição de acesso.

## Processo

### 1. Validar identidade

Para cada player:

- confirme domínio, página e aliases;
- compare nome da página, URL e sinais do site oficial;
- marque correspondência como `official`, `probable`, `ambiguous` ou `excluded`;
- preserve a razão da decisão.

### 2. Executar e preservar

Salve por execução:

- input e parâmetros;
- timestamp, fonte e versão do coletor;
- identificador do run/dataset;
- payload bruto;
- status, duração, custo conhecido e erros;
- contagem retornada antes de filtros.

### 3. Normalizar anúncios

Mantenha, quando disponível:

- identificador original;
- página, texto, headline, descrição e CTA;
- datas, status, país e plataforma;
- formato e URLs originais;
- URL da biblioteca;
- payload bruto ou referência a ele;
- decisão de inclusão e justificativa.

Não altere o identificador original. Normalize encoding e espaços apenas nos campos derivados.

### 4. Baixar assets

- deduplique downloads por URL durante a mesma execução;
- use nomes determinísticos;
- registre `local_path`, bytes, MIME type, hash quando calculado e erro;
- mantenha referências de todos os anúncios que usam o mesmo asset;
- não descarte variações DCO ou carrossel antes do processamento.

### 5. Filtrar falsos positivos

Exclua de métricas, sem apagar do bruto:

- homônimos;
- fornecedores que apenas citam o local ou marca;
- páginas não oficiais fora do escopo;
- mercados ou regiões incompatíveis;
- itens sem vínculo verificável.

## Saídas obrigatórias

Crie em `02-coleta/`:

- `source-index.json`;
- `collection-log.json`;
- `raw/<fonte>/<run-id>/`;
- `concorrentes/<slug>/inventario-ads.json`;
- `concorrentes/<slug>/inventario-ads.csv`;
- `concorrentes/<slug>/assets/`;
- `concorrentes/<slug>/coleta-resumo.json`;
- `handoff.json`.

## Gate de saída

Valide:

- bruto preservado e normalizado ligado à origem;
- parâmetros e data do snapshot registrados;
- páginas ambíguas separadas;
- contagens bruta, incluída e excluída disponíveis;
- erros não ocultos;
- assets e caminhos locais referenciados no inventário;
- execução incremental possível.

## Exemplo

**Entrada:** registro com dez concorrentes e Meta Ad Library como canal.

**Saída esperada:** inventário por player, payloads brutos, assets locais, log consolidado e lista explícita dos resultados excluídos por página incompatível.
