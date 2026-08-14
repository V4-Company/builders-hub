---
name: designer-lp-baseline-prepare
description: Preparar uma baseline imutável e uma cópia de trabalho isolada para uma landing page após auditoria aprovada. Usar antes da primeira alteração de implementação; não usar sem fonte inequívoca, autorização de escrita ou possibilidade de preservar a referência sem sobrescrita.
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


# LP Baseline Prepare

## 1. Propósito

Criar a fronteira imutável entre a referência aprovada e a implementação editável, permitindo comparação e recuperação sem tocar o original.

## 2. Quando usar

- Depois de `designer-lp-source-audit` concluir que a fonte está pronta.
- Antes de qualquer adaptação visual, de assets ou de código.
- Quando ainda não existir uma referência congelada e uma cópia de trabalho isolada.

## 3. Quando NÃO usar

- Quando a auditoria estiver bloqueada ou houver versões conflitantes.
- Para reorganizar outputs existentes ou transformar uma referência em área editável.
- Sem aprovação explícita dos caminhos e das operações de escrita.

## 4. Pré-condições

1. Ter relatório de fonte aprovado e implementação de origem inequívoca.
2. Auditar branch, worktree, arquivos-alvo e instruções locais.
3. Apresentar plano com origem, `reference/`, `src/` e operações exatas.
4. Confirmar que os caminhos são novos e isolados.
5. Obter aprovação explícita antes de criar ou copiar qualquer arquivo.

## 5. Entradas

- Implementação aprovada pela auditoria.
- Caminho novo do projeto, preferencialmente `outputs/landing-pages/<project>/`.
- Lista de arquivos necessários à execução.
- Hashes, estado Git e confirmação humana da versão de origem.

## 6. Fontes permitidas

- Implementação existente aprovada e seus assets oficiais.
- Histórico Git para registrar versão de origem.
- Outputs estratégicos aprovados apenas para conferência.

Não incorporar material externo novo durante a preparação da baseline.

## 7. Precedência das fontes

- Fatos: confirmação explícita mais recente → `client.json` → base estratégica aprovada → outputs estratégicos aprovados → implementação existente.
- Visual: confirmação explícita mais recente → Manual de Marca aprovado mais recente → diagnóstico visual aprovado → assets oficiais → referências externas → implementação existente.
- Copy: copy explicitamente aprovada → output estratégico de landing page aprovado → implementação existente.
- Links: confirmação explícita → implementação existente aprovada.

Registrar todo conflito descoberto nesta etapa, invalidar a prontidão e retornar à auditoria; não o resolver durante a cópia. Posicionamento, CRO, diagnóstico ou outro output estratégico não substituem silenciosamente a copy específica aprovada da landing page.

## 8. Procedimento

1. Validar novamente que origem e destinos correspondem ao plano aprovado.
2. Confirmar que `reference/` e `src/` não contêm arquivos preexistentes.
3. Registrar origem, caminho relativo, hash, timestamp de preparação e função de cada arquivo.
4. Em execução autorizada, copiar a implementação aprovada para `reference/` sem transformação.
5. Validar a cópia de referência por hash e contagem.
6. Criar `src/` como cópia de trabalho separada, preservando estrutura necessária.
7. Validar que `reference/` e `src/` começam equivalentes.
8. Marcar `reference/` como fronteira somente leitura no relatório operacional.
9. Registrar diferenças preexistentes, se houver, e bloquear em vez de normalizá-las.

Estrutura recomendada:

```text
outputs/landing-pages/<project>/
├── reference/  # cópia congelada, nunca editada
└── src/        # única área autorizável para implementação
```

## 9. Saídas esperadas

- Baseline congelada em caminho novo e isolado.
- Cópia de trabalho inicialmente equivalente.
- Manifesto humano com origem, caminho, hash, timestamp e função.
- Registro de autorização e validação pós-cópia.

## 10. Critérios de parada

Parar se qualquer destino existir, se hashes não coincidirem, se houver risco de sobrescrita, se a origem mudar durante a operação ou se faltar autorização. Não improvisar nomes, conteúdo, links ou assets.

## 11. Checkpoints humanos

- Aprovar caminhos, lista de arquivos e operação de cópia.
- Confirmar o manifesto e a imutabilidade de `reference/`.
- Autorizar separadamente a primeira seção a ser alterada em `src/`.

## 12. Proteções

O `AGENTS.md` raiz prevalece. Nunca modificar origem, outputs existentes, plugin ou `reference/`. Cada execução altera no máximo uma seção autorizada na etapa posterior. Não ler secrets. Commit, push e Vercel Preview exigem aprovações próprias; Production é proibida.

## 13. Integração com a matriz

Consumir a implementação indicada por `designer-lp-source-audit` e outputs aprovados da matriz como evidência. Esta skill cria uma proteção operacional nova; não altera contratos, outputs ou scripts da matriz e não herda comandos de deploy ou mutação do cliente.

## 14. Ferramentas reutilizáveis

- Disponíveis: `Get-FileHash`, `git status`, `git diff --no-index` e listagem nativa de arquivos.
- Planejadas: manifesto gerado por ferramenta própria, ainda não implementado.
- Humanas: confirmação da versão e autorização de caminho.
- Proibidas: sincronização destrutiva, formatação automática da referência e scaffolding que adicione arquivos não aprovados.

## 15. Ações proibidas

- Sobrescrever, mover, renomear, reformatar ou otimizar a origem ou `reference/`.
- Usar um output atual como diretório editável.
- Incluir arquivos além dos aprovados.
- Fazer mudanças visuais, de copy, link ou asset nesta etapa.

## 16. Definição de sucesso

Referência e trabalho ficam fisicamente separados, verificáveis e inicialmente equivalentes, com origem e autorização rastreáveis e nenhuma alteração no original.
