---
name: designer-lp-design-adapter
description: Adaptar visualmente uma landing page em uma cópia de trabalho autorizada, preservando conteúdo, links, claims e estrutura comercial congelados. Usar por seção, para aplicação de marca, correções visuais ou programas de redesign conduzidos em sucessivas execuções de uma seção; não usar para alterar a página inteira em uma execução, criar estratégia, trocar assets sem aprovação ou editar referência/original.
area: designer
author: nicolaskobayashi-v4
version: 1.0.0
---

## Compatibilidade com o Builders Hub

Esta skill foi portada do repositorio v4-unidade-integrada. As regras abaixo tem precedencia sobre caminhos, zonas e ferramentas citados no corpo original:

- **Posicao no fluxo.** Este pipeline fica a jusante de `designer-landing-page`, que e a porta do hub para `ee-s3-landing-page`. O `designer-landing-page` responde por estrategia, copy e geracao de codigo. Este pipeline responde por baseline, adaptacao, assets, quality gate e release controlada. O passo `vercel --yes --prod` do `designer-landing-page` fica **suspenso** quando o pipeline estiver em uso: release passa por `designer-lp-release`, e Production continua proibida.
- **Governanca.** Onde o corpo cita "o `AGENTS.md` raiz prevalece", leia o `CLAUDE.md` e o `AGENTS.md` da raiz do hub mais o `CLAUDE.md` da KB do cliente. Nenhuma regra local pode enfraquece-los.
- **Zonas somente leitura.** Onde o corpo cita "matriz" e "plugin", leia: `.claude/skills/`, `.agents/skills/` e `REGISTRY.md` sao somente leitura durante o pipeline. `REGISTRY.md` e auto-gerado e nunca se edita a mao.
- **Caminhos.** Trabalhe em `squads/{squad}/clientes/{cliente}/`. A estrutura do projeto e `squads/{squad}/clientes/{cliente}/outputs/landing-pages/<projeto>/`, com `reference/` e `src/` dentro dela.
- **`client.json`.** Opcional no hub. So a KB migrada do EE tem esse arquivo. Se nao existir, derive o contexto de `CLAUDE.md`, `mission-control/`, `docs/` e `links.md`, e nao invente o arquivo.
- **Scripts da matriz.** `validate_output.py`, `page_audit.py`, `page_audit_deep.py` e o agente `revisor-qualidade` **nao existem no hub**. Onde o corpo os cita, declare o gap e faca a verificacao equivalente a mao, registrando o que foi checado e como.
- **Vercel.** O hub nao tem projeto Vercel configurado. Preview exige configurar o projeto antes e autorizacao explicita do usuario na hora. Production permanece proibida por esta skill.
- **Registro.** Decisao, gate aprovado e bloqueio vao para `mission-control/historico-checkins.md` da KB do cliente.
- **Git.** Nunca commite `squads/` nem `bases/`. Sao pessoais e ficam no `.gitignore`.

---


# LP Design Adapter

## 1. Propósito

Transformar a apresentação visual da implementação autorizada com fidelidade à marca e à referência, sem redefinir estratégia, copy, oferta, claims, links ou função comercial.

## 2. Quando usar

- Para executar uma etapa de um programa de redesign completo, sempre limitada a uma seção autorizada.
- Para adaptação de uma única seção por execução.
- Para aplicação de Manual de Marca ou rodada de correções visuais delimitadas.

“Redesign completo” significa um programa composto por sucessivas execuções desta skill, uma seção por vez. Nunca interpretar o programa como autorização para alterar toda a página em uma única execução.

## 3. Quando NÃO usar

- Sem baseline aprovada e seção/arquivos explicitamente autorizados.
- Para escrever estratégia, substituir copy ou decidir claims, preços, métricas e links.
- Para buscar stock automaticamente ou reutilizar identidade, código, estrutura completa ou assets externos.

## 4. Pré-condições

1. Confirmar `source_audited` e `baseline_approved`.
2. Identificar `reference/` somente leitura e `src/` editável.
3. Congelar copy, links, claims e estrutura comercial da seção.
4. Ler Manual de Marca e diagnóstico visual aprovados, quando disponíveis.
5. Apresentar plano e obter autorização explícita para uma seção e arquivos definidos.

## 5. Entradas

- Baseline e cópia de trabalho.
- Copy, links, claims e estrutura comercial aprovados.
- Manual de Marca, diagnóstico visual e assets oficiais aprovados.
- Referências visuais autorizadas e escopo de adaptação.
- Restrições técnicas e viewports-alvo.

## 6. Fontes permitidas

- Fontes internas aprovadas e assets oficiais.
- Output estratégico aprovado como restrição de conteúdo.
- Referências externas apenas como repertório de composição, ritmo e padrões.

Referências externas nunca autorizam copiar identidade, código, estrutura integral, conteúdo ou assets.

## 7. Precedência das fontes

- Fatos: confirmação explícita mais recente → `client.json` → base estratégica aprovada → outputs estratégicos aprovados → implementação existente.
- Visual: confirmação explícita mais recente → Manual aprovado mais recente → diagnóstico visual aprovado → assets oficiais → referências externas → implementação existente.
- Copy: copy explicitamente aprovada → output estratégico de landing page aprovado → implementação existente.
- Links: confirmação explícita → implementação existente aprovada.

Registrar todo conflito e interromper o trecho afetado. Documento especializado posterior pode prevalecer apenas em seu domínio e com decisão registrada.

## 8. Procedimento

1. Selecionar o modo: etapa de programa de redesign completo, adaptação por seção, aplicação de marca ou rodada de correções visuais.
2. Se o modo for redesign completo, registrar o programa geral apenas como roteiro; não tratá-lo como autorização de escrita.
3. Delimitar arquivos, seletores, componentes e conteúdo que não podem mudar.
4. Comparar `reference/` e `src/` antes da edição e registrar diferenças preexistentes.
5. Traduzir Manual e diagnóstico em decisões explícitas de tipografia, cor, espaçamento, grid, hierarquia e componentes.
6. Tratar benchmarks como repertório, nunca como template.
7. Adaptar somente a seção autorizada em `src/`.
8. Manter copy, links, claims, preços, métricas e ordem comercial congelados.
9. Se não houver fotografia oficial aprovada, manter solução sem foto; não inserir stock.
10. Usar ícones de forma sistemática e coerente; evitar ilustrações improvisadas.
11. Permitir assimetria apenas quando controlada por grid, hierarquia e comportamento responsivo.
12. Remover ou não criar decoração sem função comunicacional.
13. Verificar visualmente 390, 768, 1024 e 1440 px, comparando com a referência.
14. Submeter a seção à revisão estética humana antes de encerrar a execução.
15. Exigir nova autorização para a seção seguinte; a aprovação atual nunca se propaga automaticamente.

## 9. Saídas esperadas

- Alteração limitada à área `src/`, aos arquivos e à seção autorizados.
- Registro das decisões visuais e dos itens preservados.
- Comparação com baseline e lista de desvios intencionais.
- Pendências encaminhadas a assets, qualidade ou decisão humana.
- Em programa de redesign completo, registro da etapa concluída sem autorizar as seções seguintes.

## 10. Critérios de parada

Parar se a fidelidade visual, copy, links, claims, assets ou estrutura comercial não puderem ser preservados; se faltar fonte visual crítica; ou se a mudança exigir outro arquivo/seção. Não inventar solução factual nem ampliar escopo.

## 11. Checkpoints humanos

- Aprovar modo, seção, arquivos e plano antes da escrita.
- Aprovar qualquer exceção de conteúdo ou asset antes da mudança.
- Realizar revisão estética e responsiva antes do quality gate.

## 12. Proteções

O `AGENTS.md` raiz prevalece. Plugin, matriz, original e `reference/` são somente leitura. Uma execução modifica no máximo uma seção. Não alterar copy, links ou assets sem aprovação. Não ler secrets. Commit/push e Preview têm aprovações separadas; Production é proibida.

## 13. Integração com a matriz

Consumir `ee-s3-landing-page`, Manual de Marca, posicionamento, diagnósticos aprovados e padrões de copy como restrições e repertório. Esta skill estende a camada visual operacional; não substitui estratégia, não reescreve outputs e não executa deploys ou mutações sugeridos pela matriz.

## 14. Ferramentas reutilizáveis

- Disponíveis: inspeção estática de HTML/CSS/JS e Git diff.
- Condicionais: renderização local; descobrir primeiro se o projeto possui mecanismo utilizável e autorizado antes de propor seu uso.
- Planejadas: comparação visual automatizada e tokens normalizados, ainda não implementados.
- Humanas: revisão estética, confirmação de marca e aceitação de desvios.
- Proibidas: instalação automática de frameworks, busca automática de stock e edição do Figma original.

## 15. Ações proibidas

- Editar `reference/`, original, plugin ou outputs não autorizados.
- Inventar claims, depoimentos, preços, métricas, links ou conteúdo.
- Copiar identidade, código, estrutura completa ou assets de terceiros.
- Inserir imagem genérica para preencher ausência de fotografia.
- Fazer commit, push ou deploy.

## 16. Definição de sucesso

A seção autorizada apresenta adaptação visual coerente e responsiva, mantém integralmente o conteúdo e a função aprovados, possui desvios rastreáveis e passa pela revisão estética humana sem tocar os originais.
