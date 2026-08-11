---
name: geral-creative-intelligence-maestro
description: Orquestra de ponta a ponta entregas de Creative Intelligence com pesquisa competitiva, coleta de anúncios, processamento audiovisual, diagnóstico estratégico, experiência web interativa, QA e empacotamento. Use sempre que o usuário pedir benchmark criativo completo, sala de inteligência, swipe file navegável, análise de concorrentes com criativos ou uma entrega semelhante ao formato Creative Intelligence Room.
area: geral
author: fabiojoseaiello-alt
version: 1.1.0
---

# Creative Intelligence — Maestro

Conduza uma entrega consultiva rastreável, reutilizável e visual. O produto não é apenas um relatório nem apenas um site: é uma esteira que transforma evidências públicas e materiais do cliente em diagnóstico, direção criativa e experiência navegável.

## Dependências e segurança

- Trabalhe apenas com fontes públicas, materiais fornecidos pelo usuário ou integrações autorizadas.
- Nunca registre tokens, cookies, credenciais ou dados pessoais nos artefatos.
- Antes de usar APIs pagas, confirme que a credencial existe e informe a estimativa de volume quando ela puder gerar custo relevante.
- Não publique, substitua um deploy ou envie arquivos externamente sem autorização explícita. Build e prévia local fazem parte do fluxo normal.
- Preserve payloads brutos e diferencie fato, cálculo, hipótese e recomendação.

## Antes de começar

1. Localize a pasta do cliente/projeto e leia as instruções locais aplicáveis.
2. Leia [references/contrato-do-workflow.md](references/contrato-do-workflow.md) por inteiro.
3. Leia [references/fluxograma.md](references/fluxograma.md) para decidir o ponto de entrada, retornos e a saída adequada.
4. Identifique quais etapas já existem e retome do último gate válido; não repita coleta cara sem necessidade.
5. Crie ou atualize `creative-intelligence/project.json` e `creative-intelligence/status.md`.
6. Registre lacunas que afetam o resultado, mas prossiga com premissas seguras quando elas não forem bloqueantes.

## Workflow

### Gate 1 — Descoberta e escopo

Use `geral-creative-intelligence-descoberta`.

O gate termina quando há:

- objetivo e decisão que a entrega precisa apoiar;
- cliente em foco, mercado, região, período e canais;
- registro de concorrentes com papéis separados: linha de base, núcleo prioritário, expansão e watchlist;
- critérios de inclusão, exclusão e sucesso;
- inventário de fontes e acessos.

Não avance com uma lista de concorrentes sem origem ou sem distinguir nomes citados pelo cliente de referências adicionadas pela análise.

### Gate 2 — Coleta rastreável

Use `geral-creative-intelligence-coleta`.

O gate termina quando:

- páginas oficiais foram validadas;
- resultados brutos foram preservados;
- anúncios e assets têm identificadores e origem;
- homônimos, fornecedores e menções indevidas foram excluídos com justificativa;
- cada fonte tem status, timestamp, parâmetros e erro documentados.

### Gate 3 — Processamento audiovisual

Use `geral-creative-intelligence-processamento`.

O gate termina quando:

- mídias estão deduplicadas por conteúdo;
- vídeos possuem metadados, transcrição ou status de ausência de fala;
- hooks iniciais, perfil de áudio, frente e ciclo estão classificados;
- frames e folhas de contato permitem inspeção visual;
- um índice consolidado liga anúncio, asset, transcrição e evidência.

### Gate 4 — Diagnóstico e direção criativa

Use `geral-creative-intelligence-diagnostico`.

O gate termina quando:

- métricas são reproduzíveis a partir do inventário;
- diferenças entre volume de anúncios, arquivos e conteúdos únicos estão claras;
- padrões quantitativos e códigos visuais estão sintetizados por player;
- o cliente foi comparado ao mercado sem misturar sinais públicos com performance interna;
- existe plano de ação por frente, arquitetura de testes e critérios de decisão.

### Gate 5 — Experiência navegável

Use `geral-creative-intelligence-experiencia`.

O gate termina quando:

- a aplicação consome dados gerados, em vez de duplicar números manualmente;
- o usuário consegue ir do panorama à evidência individual;
- radar, biblioteca, dossiês, hooks, diagnóstico e plano estão integrados;
- identidade, responsividade e acessibilidade foram implementadas;
- vídeos estão otimizados para navegação e apresentação.

### Gate 6 — QA e entrega

Use `geral-creative-intelligence-qa-entrega`.

O gate termina quando:

- build e testes passam;
- contagens da interface batem com o dataset;
- desktop, mobile, filtros, modais, imagens e vídeos foram testados;
- há audit, capturas, pacote de build e instruções de uso;
- limitações metodológicas aparecem na entrega;
- deploy foi feito somente quando autorizado.

## Curadoria padrão

Para uma experiência leve, selecione por player, quando disponível:

1. evidência de maior permanência;
2. teste mais recente;
3. hook falado relevante e não duplicado.

Adapte o critério ao objetivo registrado no escopo. Curadoria é seleção editorial; nunca altere a base analítica para fazer a narrativa caber.

## Gestão de estado e retomada

Atualize `status.md` após cada gate com:

- concluído;
- evidências e caminhos;
- falhas e tentativas;
- decisões e premissas;
- próximo gate;
- bloqueios reais.

Comandos e scripts devem ser idempotentes sempre que possível: reutilize runs, pule assets já baixados e transcrições válidas, e gere novamente apenas artefatos derivados.

## Critério de qualidade final

A entrega está pronta quando outra pessoa consegue:

- rastrear uma conclusão até a fonte;
- entender o que é evidência e o que é hipótese;
- navegar do mercado para um criativo específico;
- transformar o diagnóstico em testes executáveis;
- atualizar o projeto sem reconstruí-lo manualmente;
- apresentar online ou offline sem depender do ambiente de desenvolvimento.

## Exemplo de uso

**Usuário:** “Quero analisar os criativos dos principais concorrentes do cliente X e entregar isso em uma sala interativa.”

**Comportamento:** execute os seis gates, mantenha os contratos de handoff, gere o diagnóstico e só então construa a experiência. Entregue caminhos dos artefatos, resumo executivo, limitações e status do deploy.
