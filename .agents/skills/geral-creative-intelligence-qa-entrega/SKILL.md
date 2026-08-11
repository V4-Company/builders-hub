---
name: geral-creative-intelligence-qa-entrega
description: Audita, testa, empacota e prepara para publicação uma Creative Intelligence Room e seus artefatos analíticos. Use sempre na etapa final de benchmark interativo, antes de apresentar, enviar ZIP, gerar pacote offline ou fazer deploy, e também quando o usuário pedir revisão de qualidade de uma sala já existente.
area: geral
author: fabiojoseaiello-alt
version: 1.0.0
---

# Creative Intelligence — QA e Entrega

Feche a cadeia entre dado, narrativa e interface. O QA precisa detectar tanto erros técnicos quanto contradições metodológicas antes que cheguem à apresentação.

## Entradas

- handoffs dos gates anteriores;
- dataset gerado e base analítica;
- aplicação e build;
- assets e pacote offline;
- critérios de sucesso definidos na descoberta.

## 1. Auditoria de dados

Valide programaticamente:

- contagens por player e totais;
- anúncios incluídos e excluídos;
- IDs únicos e relações anúncio–asset;
- caminhos de mídia existentes;
- cobertura de pôster, vídeo e transcrição;
- datas e limiares de ciclo;
- schema do dataset;
- razões de curadoria;
- ausência de segredos e caminhos privados no build.

Compare números exibidos com os artefatos de `04-diagnostico/`; não aceite divergência explicada apenas como “ajuste visual”.

## 2. Build e smoke test

- instale dependências de forma reprodutível;
- execute checagem de tipos, testes e build;
- sirva o build, não apenas o modo de desenvolvimento;
- capture console, falhas de rede e arquivos ausentes;
- confirme que caminhos relativos funcionam no pacote offline.

## 3. QA funcional

Teste ao menos:

- navegação e âncoras;
- busca, filtros, ordenação e limpeza de estado;
- abertura e fechamento de dossiê;
- abertura, reprodução e fechamento de mídia;
- troca de frentes do plano;
- links para fontes e metodologia;
- estados vazios;
- teclado e `Escape`;
- restauração de scroll e foco.

## 4. QA visual

Capture desktop e mobile para:

- hero;
- radar;
- biblioteca;
- hooks;
- diagnóstico/direção;
- dossiê;
- player;
- plano operacional;
- metodologia.

Verifique:

- overflow horizontal;
- textos cortados ou sobrepostos;
- contraste e legibilidade;
- imagens quebradas;
- aspect ratio de pôsteres e vídeos;
- densidade de informação;
- redução de movimento;
- consistência de estados ativos, foco e hover.

Faça inspeção das capturas; gerar screenshots sem revisá-las não constitui QA.

## 5. QA metodológico

Confirme que a entrega:

- mostra data e recorte do snapshot;
- explica fontes e filtros;
- distingue ausência observada de ausência real;
- não trata permanência como performance comprovada;
- separa dados públicos e internos;
- identifica curadoria editorial;
- permite rastrear achados até evidências.

## 6. Empacotamento

Gere:

- build estático;
- ZIP do build;
- pacote offline de um clique;
- versão compacta se o volume de vídeo prejudicar transporte;
- `README.md` com execução, atualização, limitações e troubleshooting;
- checksum e inventário dos arquivos principais quando útil.

Não inclua caches, perfis de navegador, `node_modules`, credenciais ou dados temporários.

## 7. Publicação

Somente com autorização explícita:

- confirme projeto e conta de destino;
- valide variáveis e arquivos ignorados;
- publique uma versão de preview quando apropriado;
- faça smoke test na URL final;
- registre URL, timestamp, commit/build e status;
- não sobrescreva produção diferente sem confirmação.

## Saídas obrigatórias

Crie em `06-entrega/`:

- `audit.json` com asserts e resultados;
- `capturas/`;
- `build/` ou referência ao build validado;
- `pacote-offline/`;
- arquivos ZIP;
- `README.md`;
- `delivery-manifest.json`;
- `handoff.json` final.

## Critérios mínimos de aprovação

- build concluído sem erro;
- zero imagem quebrada;
- zero caminho de mídia ausente entre os itens curados;
- zero overflow horizontal nas larguras testadas;
- contagens coerentes com o dataset;
- dossiê e mídia funcionais;
- desktop e mobile revisados visualmente;
- ressalvas metodológicas presentes;
- pacote offline executável;
- publicação, se houver, validada na URL final.

## Resposta final ao usuário

Informe:

1. resultado e formato entregue;
2. caminhos e URL, se autorizada;
3. contagens principais;
4. testes executados;
5. limitações e pendências;
6. como atualizar a base.
