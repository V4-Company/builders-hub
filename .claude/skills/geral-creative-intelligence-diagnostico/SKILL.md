---
name: geral-creative-intelligence-diagnostico
description: Transforma uma base processada de Creative Intelligence em benchmark competitivo, leitura visual, padrões de hooks, comparação cliente versus mercado e plano de ação criativo. Use sempre que o usuário pedir diagnóstico de criativos, códigos visuais concorrentes, oportunidades por frente ou uma arquitetura de testes baseada em evidências.
area: geral
author: fabiojoseaiello-alt
version: 1.0.0
---

# Creative Intelligence — Diagnóstico

Produza uma leitura executiva que permaneça ligada às evidências. O objetivo é transformar inventário em decisões, sem confundir sinais públicos com performance real.

## Entradas

- escopo e registro competitivo;
- inventários incluídos e excluídos;
- `03-processamento/creative-index.json`;
- cobertura, erros e taxonomia;
- dados internos, somente se autorizados e em camada separada.

## Princípios

- Diferencie observado, calculado, inferido e recomendado.
- Compare bases equivalentes e sinalize diferenças de cobertura.
- Zero resultado significa “não observado no snapshot”, não ausência definitiva.
- Permanência e repetição podem sugerir investimento continuado; não comprovam ROAS, vendas ou aprovação.
- Números da aplicação e do relatório devem ser derivados da mesma base.

## Processo

### 1. Consolidar métricas

Calcule por player:

- anúncios brutos, incluídos e excluídos;
- assets e conteúdos únicos;
- vídeos únicos e cobertura de transcrição;
- distribuição por formato, frente, mensagem, hook e áudio;
- idade mediana e máxima;
- testes, maturação, longevos e veteranos;
- páginas e marcas associadas.

### 2. Analisar visualmente

Use frames, folhas de contato e criativos completos para descrever:

- sujeito dominante e cenário;
- primeiro impacto visual;
- presença humana e papel do personagem;
- demonstração, transformação, bastidor ou prova;
- texto em tela, densidade e timing;
- ritmo, montagem, enquadramento, estética e repetição;
- coerência entre promessa, imagem e CTA.

Evite adjetivos vagos como “bonito” ou “premium” sem indicar quais códigos visuais sustentam a leitura.

### 3. Criar dossiês por player

Cada dossiê deve conter:

- papel no benchmark;
- dimensão e qualidade da amostra;
- territórios e frentes dominantes;
- formatos, hooks e códigos visuais;
- sinais de ciclo;
- evidências representativas;
- aprendizado utilizável;
- ressalvas.

### 4. Comparar cliente e mercado

Mostre:

- forças já existentes;
- lacunas de mensagem, prova, formato e sistema de variações;
- territórios saturados e subexplorados;
- referências que podem ser adaptadas sem copiar;
- ativos proprietários do cliente.

### 5. Recomendar execução

Estruture por frente comercial:

- territórios prioritários;
- públicos e tensões;
- hooks para testar;
- estruturas de vídeo;
- códigos visuais e provas necessárias;
- matriz de variações;
- sprint de produção e ativação;
- métricas do hook até a venda.

Uma matriz mínima pode cruzar três hooks, duas durações, dois CTAs, duas aberturas visuais e versões com fala ou texto. Ajuste ao orçamento e à capacidade do cliente.

### 6. Curar a experiência

Selecione evidências que cubram contraste e aprendizado. Padrão por player, quando disponível:

1. maior permanência;
2. teste mais recente;
3. hook falado relevante e distinto.

Registre `selection_reason` e não apresente a curadoria como amostra estatística aleatória.

## Saídas obrigatórias

Crie em `04-diagnostico/`:

- `benchmark-metricas.json`;
- `benchmark-inventario.csv`;
- `diagnostico.md`;
- `dossies/<slug>.md` ou estrutura equivalente;
- `plano-de-acao-criativo.md`;
- `curadoria.json`;
- `metodologia-e-limitacoes.md`;
- `handoff.json`.

## Gate de saída

- todas as contagens podem ser recalculadas;
- dossiês registram tamanho e limitações da amostra;
- códigos visuais têm evidências concretas;
- cliente e mercado usam o mesmo critério público;
- dados internos não foram misturados silenciosamente;
- plano de ação contém execução, não apenas inspiração;
- criativos curados possuem razão de seleção.

## Estrutura do resumo executivo

1. decisão apoiada;
2. três a cinco achados;
3. o que o cliente já faz bem;
4. principal lacuna sistêmica;
5. oportunidades por frente;
6. próximos testes;
7. limitações do snapshot.
