---
name: geral-creative-intelligence-experiencia
description: Constrói uma Creative Intelligence Room navegável a partir de dados e criativos analisados, com radar, biblioteca, dossiês, hooks, diagnóstico e plano de ação. Use sempre que um benchmark criativo precisar virar site, data room, swipe file interativo ou apresentação web responsiva e atualizável.
area: geral
author: fabiojoseaiello-alt
version: 1.0.0
---

# Creative Intelligence — Experiência

Transforme o diagnóstico em uma experiência de decisão. A interface deve levar do panorama à evidência e da evidência à ação, sem esconder metodologia ou criar números paralelos.

## Entradas

- identidade e materiais oficiais do cliente;
- `04-diagnostico/benchmark-metricas.json`;
- `04-diagnostico/curadoria.json`;
- dossiês, plano de ação e metodologia;
- vídeos, pôsteres e transcrições processados;
- objetivo, audiência e contexto de apresentação.

## Stack padrão

Prefira uma aplicação estática simples, portátil e de baixo risco:

- Vite;
- TypeScript;
- CSS customizado;
- dataset JSON gerado;
- assets locais otimizados.

Use framework adicional apenas quando a complexidade real justificar. Quando disponível, `geral-frontend-design` pode apoiar a direção e implementação visual, mantendo os contratos desta skill.

## Arquitetura de informação

Inclua, quando houver conteúdo:

1. **Hero executivo:** pergunta, snapshot e dimensão da base.
2. **Radar competitivo:** players, papéis, volume e ciclo.
3. **Biblioteca:** criativos curados com busca, filtros e ordenação.
4. **Dossiê:** leitura por player e ligação com suas evidências.
5. **Player:** vídeo, pôster, hook, transcrição, copy, ciclo e fonte.
6. **Laboratório de hooks:** padrões, incidência e aplicação.
7. **Diagnóstico:** cliente versus mercado.
8. **Direção criativa:** frentes, conceitos e variações.
9. **Plano operacional:** sprint, entregáveis e métricas.
10. **Metodologia:** critérios, snapshot e limitações.

O usuário deve conseguir responder “por quê?” abrindo a evidência correspondente.

## Dados e atualização

- Gere `generated-data.json` por script a partir dos artefatos analíticos.
- Não copie contagens manualmente para HTML ou TypeScript.
- Valide o schema antes do build.
- Preserve `source_id`, `competitor_slug`, `asset_id` e `selection_reason`.
- Faça atualização incremental: dados novos devem entrar pela geração, não por edição manual da interface.

## Sistema visual

Construa uma identidade específica para o cliente e para o contexto de inteligência:

- extraia paleta, tipografia, logo, contraste e tom dos materiais oficiais;
- converta decisões em tokens CSS;
- escolha uma metáfora visual coerente, como command center, atlas, observatório ou editorial;
- use hierarquia clara, densidade controlada e estados consistentes;
- deixe os criativos serem a principal matéria visual;
- evite aparência de template genérico ou “dashboard padrão”.

Documente tokens, componentes, grid, responsividade e comportamento. Não use imagem de marca sem origem ou autorização.

## Mídia

- gere pôster para cada vídeo;
- otimize para H.264/AAC e `faststart` quando compatível;
- use resolução suficiente para leitura sem inflar a entrega;
- carregue vídeo sob demanda;
- indique ausência de áudio ou transcrição;
- ofereça fallback quando a mídia não puder ser reproduzida.

## Interação e acessibilidade

- filtros devem ser combináveis e reversíveis;
- modais devem fechar por botão, fundo e `Escape`;
- preserve foco e bloqueio de scroll nas camadas;
- forneça textos alternativos e rótulos acessíveis;
- respeite `prefers-reduced-motion`;
- suporte teclado e telas a partir de 320 px;
- mantenha contraste e tamanhos legíveis em ambiente de apresentação.

## Pacote offline

Prepare a aplicação para funcionar sem o ambiente de desenvolvimento:

- build estático;
- servidor local simples;
- iniciador de um clique quando o sistema permitir;
- caminhos relativos;
- versão compacta opcional com vídeos mais comprimidos;
- README com instruções.

## Saídas obrigatórias

Crie em `05-experiencia/`:

- `app/` com fonte editável;
- script de geração de dados;
- `generated-data.json`;
- documentação do sistema visual;
- build local reproduzível;
- pacote offline preliminar;
- `handoff.json`.

## Gate de saída

- interface e relatório usam o mesmo dataset;
- todas as seções têm objetivo claro;
- evidências abrem a partir das conclusões;
- vídeos e imagens usam caminhos válidos;
- identidade é específica e documentada;
- desktop e mobile são utilizáveis;
- metodologia está acessível;
- um comando reproduz o build.

## Exemplo

**Entrada:** benchmark com 15 players e 35 criativos curados.

**Saída esperada:** uma sala interativa de marca própria, filtros por player/frente/ciclo, dossiês, player com hook e transcrição, síntese visual e plano operacional, alimentada por JSON gerado.
