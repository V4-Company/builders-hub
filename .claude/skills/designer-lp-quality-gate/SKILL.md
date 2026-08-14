---
name: designer-lp-quality-gate
description: Executar o gate integrado de qualidade de uma landing page antes de release, reunindo conteúdo, baseline, visual, acessibilidade, responsividade, código, assets e Git. Usar após implementação e assets revisados; não usar para corrigir silenciosamente problemas, aprovar fatos ou substituir revisão humana.
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


# LP Quality Gate

## 1. Propósito

Emitir uma decisão verificável — `PASS`, `PASS_WITH_WARNINGS` ou `BLOCKED` — sobre a prontidão da cópia de trabalho, sem alterar a implementação durante a avaliação.

Ao executar, ler [references/quality-checklist.md](references/quality-checklist.md) integralmente e registrar cada item aplicável.

## 2. Quando usar

- Depois da revisão da implementação e da aprovação de assets.
- Antes de solicitar autorização para Vercel Preview.
- Novamente após qualquer correção que afete o resultado anterior.

## 3. Quando NÃO usar

- Antes de baseline e escopo estarem aprovados.
- Para validar estratégia ainda não aprovada ou preencher lacunas.
- Para alterar código, copy, links ou assets como efeito colateral.

## 4. Pré-condições

1. Confirmar referência imutável e arquivos autorizados em `src/`.
2. Ter revisão estética humana e assets aprovados.
3. Auditar branch e worktree.
4. Confirmar como a página pode ser executada localmente sem instalar dependências novas.
5. Identificar quais verificações são disponíveis, planejadas, humanas ou proibidas.

## 5. Entradas

- `reference/`, `src/` e escopo autorizado.
- Copy, links, claims e assets aprovados.
- Manual, diagnósticos e output estratégico aplicáveis.
- Evidências de execução local e estado Git.
- Checklist de qualidade desta skill.

## 6. Fontes permitidas

- Implementação e baseline locais.
- Fontes aprovadas do cliente e outputs estratégicos somente leitura.
- Logs locais e resultados reais de ferramentas existentes.
- Avaliação humana documentada.

Não declarar teste executado sem evidência da execução.

## 7. Precedência das fontes

- Fatos: confirmação explícita mais recente → `client.json` → base estratégica aprovada → outputs estratégicos aprovados → implementação existente.
- Visual: confirmação explícita mais recente → Manual aprovado mais recente → diagnóstico visual aprovado → assets oficiais → referências externas → implementação existente.
- Copy: copy explicitamente aprovada → output estratégico de landing page aprovado → implementação existente.
- Links: confirmação explícita → implementação existente aprovada.

Conflitos não resolvidos bloqueiam o gate; documento especializado posterior prevalece apenas no domínio correspondente e com registro.

## 8. Procedimento

1. Ler o checklist e marcar aplicabilidade, método e evidência de cada item.
2. Comparar baseline e implementação para localizar mudanças autorizadas e inesperadas.
3. Conferir copy, links, claims, preços, métricas e estrutura contra fontes aprovadas.
4. Inspecionar HTML, CSS, JavaScript, SVG e assets por integridade, semântica e referências quebradas.
5. Executar apenas comandos locais já disponíveis e permitidos; registrar comando e resultado real.
6. Testar 390, 768, 1024 e 1440 px para layout, overflow, legibilidade e interação.
7. Verificar acessibilidade básica: estrutura semântica, teclado, foco, nomes acessíveis, contraste e texto alternativo.
8. Verificar console e comportamento de runtime, quando houver ambiente local executável.
9. Auditar Git para arquivos inesperados, fora do escopo ou não autorizados.
10. Se houver arquivos untracked, inspecioná-los diretamente: `git diff --check` não os cobre. Verificar trailing whitespace, tabs acidentais, encoding, arquivos vazios, marcadores `TODO`/`FIXME` não intencionais, headings duplicados quando pertinente e referências ou caminhos obviamente quebrados.
11. Não executar `git add` nem `git add -N` para viabilizar a auditoria.
12. Classificar cada achado por severidade e responsável.
13. Emitir resultado sem corrigir durante o gate.

## 9. Saídas esperadas

- Checklist preenchido com evidência, resultado e observação.
- Lista de achados bloqueadores e warnings.
- Relação de mudanças autorizadas e inesperadas.
- Decisão final `PASS`, `PASS_WITH_WARNINGS` ou `BLOCKED`.

`PASS_WITH_WARNINGS` só admite riscos não factuais, não estruturais e aceitos explicitamente. Nenhum critério nominal de `BLOCKED` pode ser rebaixado silenciosamente para `PASS_WITH_WARNINGS`.

## 10. Critérios de parada

Parar com `BLOCKED` diante de qualquer uma destas condições:

- baseline alterada ou violada;
- arquivo criado ou modificado fora do escopo autorizado;
- alteração factual inesperada;
- copy não autorizada;
- link não autorizado;
- claim não validado;
- asset sem autorização quando exigível;
- erro crítico de responsividade;
- erro crítico de acessibilidade;
- erro de runtime que impeça ou prejudique o uso essencial;
- fonte crítica ausente ou impossibilidade de comprovar teste necessário.

## 11. Checkpoints humanos

- Validar fidelidade visual e experiência nos quatro viewports.
- Resolver ou aceitar warnings não bloqueadores.
- Aprovar correções em execução separada e reexecutar o gate.
- Aceitar o resultado antes de encaminhar ao release.

## 12. Proteções

O `AGENTS.md` raiz prevalece. O gate é somente leitura e não modifica plugin, matriz, baseline ou código. Não inventar evidência nem ler secrets. Não autoriza commit, push ou Preview. Production é proibida.

## 13. Integração com a matriz

Compor, sem duplicar, conceitos de `revisor-qualidade`, `validate_output.py`, `page_audit.py` e `page_audit_deep.py`. Esses componentes podem ser consultados e, em execução futura, usados apenas se forem compatíveis e não escreverem dados não autorizados. O gate local adiciona baseline, escopo, Git, runtime e release readiness.

## 14. Ferramentas reutilizáveis

- Disponíveis: Git, `rg` e inspeção estática.
- Disponíveis na matriz: revisores e scripts citados, sem garantia de execução segura neste fluxo.
- Condicionais: executor local e ferramentas nativas do navegador; descobrir e confirmar sua disponibilidade e adequação antes do uso.
- Dependências futuras: Playwright, axe ou equivalentes quando não estiverem presentes e autorizados; não instalar automaticamente.
- Planejadas: screenshot/diff visual, auditor automatizado de links e suíte multi-viewport integrada.
- Humanas: estética, contexto de marca, claims e aceitação de warnings.
- Proibidas: correção automática, instalação de dependências e diagnóstico que escreva em cliente/cache sem aprovação.

## 15. Ações proibidas

- Corrigir código durante o gate ou reclassificar falha para avançar o fluxo.
- Marcar como testado o que foi apenas inspecionado ou planejado.
- Ignorar arquivo inesperado, mudança factual ou estrutural.
- Executar `git add` ou `git add -N` apenas para tornar arquivos untracked visíveis à auditoria.
- Fazer commit, push, Preview ou Production.

## 16. Definição de sucesso

O resultado é reproduzível, cobre todo o checklist aplicável, distingue evidência automática de avaliação humana e impede release diante de qualquer desvio crítico ou não autorizado.
