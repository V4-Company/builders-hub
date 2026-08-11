---
name: geral-creative-intelligence-processamento
description: Processa assets de uma base Creative Intelligence com deduplicação, metadados, transcrição, hooks iniciais, frames, folhas de contato e classificações auditáveis. Use sempre que houver vídeos ou imagens coletados de anúncios que precisem virar um índice criativo analisável e pronto para benchmark.
area: geral
author: fabiojoseaiello-alt
version: 1.0.0
---

# Creative Intelligence — Processamento

Converta mídia bruta em evidências comparáveis. Preserve o vínculo entre anúncio, arquivo e análise; um anúncio pode conter vários assets e o mesmo conteúdo pode aparecer em anúncios diferentes.

## Dependências recomendadas

- FFmpeg ou biblioteca equivalente para metadados, frames e otimização;
- `faster-whisper` ou transcritor autorizado para fala;
- biblioteca de imagem para folhas de contato;
- SHA-256 para deduplicação determinística.

Se uma dependência não existir, documente a limitação e produza os artefatos possíveis sem inventar resultados.

## Entradas

- `02-coleta/concorrentes/<slug>/inventario-ads.json`;
- assets locais e referências originais;
- taxonomia e limiares de `01-descoberta/scope.json`;
- data do snapshot.

## Processo

### 1. Indexar e deduplicar

- calcule hash do conteúdo de cada arquivo;
- agrupe arquivos idênticos;
- mantenha todos os IDs de anúncio relacionados;
- distinga `raw_ads`, `unique_assets`, `unique_content_assets`, `unique_videos` e `unique_content_videos`;
- não use nome de arquivo como prova de unicidade.

### 2. Ler metadados

Registre tipo, bytes, duração, largura, altura, orientação, codec quando disponível e presença de áudio. Erros devem ficar associados ao asset.

### 3. Transcrever áudio

- transcreva no idioma adequado ao recorte;
- preserve segmentos temporais;
- capture a fala dos primeiros cinco segundos;
- diferencie “sem faixa de áudio”, “sem fala detectável” e erro de transcrição;
- registre modelo, idioma detectado e confiança quando disponíveis;
- trate transcrição como material analítico sujeito a revisão.

### 4. Extrair leitura visual

- gere frames nos tempos 0, 1 e 3 segundos, ajustando quando o vídeo for menor;
- produza pôster representativo;
- monte folhas de contato por player;
- registre abertura visual, presença humana, espaço, produto, texto em tela e transformação quando essa taxonomia fizer parte do escopo.

### 5. Classificar

Classifique por regras explícitas e passíveis de revisão:

- frente comercial;
- formato;
- perfil de áudio;
- tipo de hook;
- tags de mensagem;
- ciclo observado.

Limiar padrão para um snapshot de anúncios ativos, se o escopo não definir outro:

- até 14 dias: `teste`;
- 15 a 29 dias: `maturacao`;
- 30 a 89 dias: `longevo`;
- 90 dias ou mais: `veterano`.

Esses rótulos descrevem idade observada; não comprovam performance.

### 6. Tornar incremental

- pule hashes já processados com versão compatível;
- preserve registros válidos;
- reprocesse quando modelo, taxonomia ou arquivo mudar;
- salve progresso por asset para que interrupções não invalidem o lote inteiro.

## Saídas obrigatórias

Crie em `03-processamento/`:

- `creative-index.json` ligando anúncio, asset, hash e análise;
- `processing-summary.json` com cobertura e erros;
- `concorrentes/<slug>/asset-deduplicacao.json`;
- `concorrentes/<slug>/transcricoes/transcricoes-analiticas.json`;
- `concorrentes/<slug>/frames/`;
- `concorrentes/<slug>/folhas-de-contato/`;
- `handoff.json`.

## Gate de saída

- nenhum criativo analisado perdeu o vínculo com a origem;
- contagens de anúncio, arquivo e conteúdo único estão separadas;
- cobertura de transcrição e erros estão quantificados;
- “sem fala” não foi confundido com “sem áudio”;
- frames e folhas de contato estão legíveis;
- classificações guardam regra ou versão;
- reexecução não duplica resultados.

## Exemplo

**Entrada:** inventário com 300 anúncios e 470 URLs de mídia.

**Saída esperada:** índice deduplicado por hash, vídeos transcritos, hooks de 0–5 segundos, frames comparáveis, cobertura por player e base pronta para calcular o benchmark.
