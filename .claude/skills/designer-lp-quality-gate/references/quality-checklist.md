# Checklist do quality gate

Usar este checklist como contrato humano legível. Para cada item, registrar `PASS`, `WARNING`, `BLOCKED` ou `N/A`, o método (`disponível`, `planejado` ou `humano`) e a evidência. Um controle planejado não pode ser marcado como executado.

## Conteúdo

- Copy idêntica à versão explicitamente aprovada ou alteração autorizada registrada.
- Links idênticos aos confirmados e destinos essenciais verificados.
- Claims, preços, métricas, depoimentos e condições comerciais possuem fonte aprovada.
- Nenhum placeholder plausível, fato inventado ou conteúdo externo incorporado.
- Estrutura e sequência comercial preservadas, salvo autorização explícita.
- Conflitos de precedência resolvidos e registrados.

## Design

- Implementação comparada com a baseline imutável.
- Mudanças limitadas à seção e aos arquivos autorizados.
- Tipografia, cores, espaçamento, grid e componentes coerentes com o Manual aprovado.
- Hierarquia visual e ações principais são claras.
- Assimetria, ícones e elementos decorativos possuem função e sistema coerente.
- Revisão estética humana concluída.

## Acessibilidade

- Estrutura de headings é lógica e existe landmark principal.
- Controles são acessíveis por teclado e possuem foco visível.
- Botões, links, formulários e ícones interativos têm nomes acessíveis.
- Imagens informativas têm texto alternativo; decorativas são corretamente ignoradas.
- Contraste e legibilidade foram avaliados.
- Não há dependência exclusiva de cor, hover ou movimento.
- Preferência de movimento reduzido é respeitada quando aplicável.

## Responsividade

- Viewports 390, 768, 1024 e 1440 px foram verificados.
- Não há overflow horizontal não intencional.
- Conteúdo, navegação e CTAs permanecem legíveis e utilizáveis.
- Imagens mantêm proporção, crop intencional e resolução suficiente.
- Quebras de texto não ocultam conteúdo nem alteram significado.
- Estados interativos funcionam com mouse, teclado e toque quando aplicável.

## Código e runtime

- HTML possui semântica válida e referências locais resolvíveis.
- CSS não introduz regra global inesperada ou dependência implícita.
- JavaScript não apresenta erro de sintaxe nem falha observada no console.
- Interações preservam comportamento e progressive enhancement quando aplicável.
- SVGs não contêm IDs conflitantes, conteúdo indevido ou dimensões quebradas.
- Dependências são existentes e autorizadas; nenhuma foi instalada pelo gate.
- Execução local foi comprovada ou a impossibilidade está marcada como bloqueio.

## Assets

- Cada asset usado possui origem e autorização conhecidas.
- Original permanece preservado e derivados são rastreáveis.
- Dimensões, formato, peso, crop, fallback e papel estão documentados.
- `picture`, `srcset` e `sizes` são coerentes quando há variantes responsivas.
- Nenhum stock foi incluído automaticamente.
- Base64 de protótipo está substituído ou explicitamente bloqueado para produção.
- Não há asset quebrado, ausente ou inesperadamente substituído.

## Git e escopo

- Branch corresponde à execução aprovada.
- Worktree foi auditado antes e depois dos testes.
- Somente arquivos e seção autorizados foram alterados.
- Não há arquivo inesperado, secret, cache, temporário ou build gerado.
- `reference/`, plugin e outputs protegidos permanecem intocados.
- `git diff --check` não reporta erro.
- Arquivos untracked foram inspecionados diretamente, pois `git diff --check` não cobre arquivos ainda não adicionados ao índice.
- A inspeção direta de untracked verificou trailing whitespace, tabs acidentais, encoding, arquivos vazios, marcadores `TODO`/`FIXME` não intencionais, headings duplicados quando pertinente e referências ou caminhos obviamente quebrados.
- Nenhum `git add` ou `git add -N` foi executado apenas para viabilizar a auditoria.
- Commit e push não foram realizados sem aprovação separada.

## Release readiness

- Testes locais aplicáveis foram concluídos com evidência.
- Resultado global é `PASS` ou `PASS_WITH_WARNINGS` aceito por humano.
- Warnings possuem responsável, impacto e decisão registrada.
- Branch, commit pretendido e diretório de projeto estão identificados.
- Projeto/equipe Vercel não são presumidos.
- Autorização de Preview ainda será solicitada separadamente.
- Nenhuma ação de Production, domínio ou alias de produção está habilitada.

## Regra de decisão

- `PASS`: todos os itens aplicáveis passaram e não há warnings abertos.
- `PASS_WITH_WARNINGS`: somente riscos não factuais e não estruturais foram aceitos explicitamente por responsável humano.
- `BLOCKED`: baseline alterada ou violada; arquivo criado/modificado fora do escopo autorizado; alteração factual inesperada; copy ou link não autorizado; claim não validado; asset sem autorização quando exigível; erro crítico de responsividade ou acessibilidade; erro de runtime que impeça ou prejudique uso essencial; ou qualquer outra falha crítica ou evidência obrigatória ausente.

Essas condições, assim como mudanças factuais, estruturais, de copy, link, claim, preço, métrica ou asset, nunca podem ser rebaixadas silenciosamente a warning ou `PASS_WITH_WARNINGS`. O gate identifica, classifica e bloqueia; não corrige automaticamente.
