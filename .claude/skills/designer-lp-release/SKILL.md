---
name: designer-lp-release
description: Preparar uma landing page aprovada para release controlado e, somente com autorização explícita, habilitar uma Vercel Preview. Usar após quality gate válido; não usar para Production, domínio, alias de produção, projeto não confirmado ou deploy automático.
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


# LP Release

## 1. Propósito

Verificar a identidade exata do artefato e todas as aprovações necessárias antes de uma eventual Vercel Preview, mantendo Production tecnicamente e processualmente fora do fluxo.

Ao executar, ler [references/release-policy.md](references/release-policy.md) integralmente.

## 2. Quando usar

- Depois de `quality_gate_passed`.
- Para preparar o pacote de evidências de release.
- Para executar uma Preview somente após autorização humana explícita e específica.

## 3. Quando NÃO usar

- Com quality gate `BLOCKED`, expirado por novas mudanças ou warnings não aceitos.
- Para Production, alias de produção, domínio ou promoção de Preview.
- Sem confirmação de projeto, equipe, diretório, branch e commit.
- Para criar projeto Vercel por inferência ou aceitar configuração desconhecida.

## 4. Pré-condições

1. Ter `PASS` ou `PASS_WITH_WARNINGS` aceito por responsável humano.
2. Confirmar que testes locais foram concluídos.
3. Auditar branch, commit pretendido e worktree.
4. Identificar destino de Preview sem fazer deploy.
5. Obter autorização explícita separada para commit, push e Preview conforme cada operação necessária.

## 5. Entradas

- Relatório mais recente do quality gate e suas evidências.
- Diretório exato da implementação.
- Branch, commit pretendido e estado do worktree.
- Projeto e equipe Vercel confirmados pelo responsável.
- Metadados locais `.vercel/project.json`, se existirem, sem secrets.
- Autorizações humanas com escopo e momento.

## 6. Fontes permitidas

- Estado local do Git e arquivos de configuração não secretos.
- Quality gate aprovado e registros de autorização.
- Confirmações explícitas do responsável.
- Painel ou CLI Vercel somente quando a execução de Preview for autorizada.

Não inferir destino por nome de pasta, histórico de outro cliente ou configuração semelhante.

## 7. Precedência das fontes

- Fatos: confirmação explícita mais recente → `client.json` → base estratégica aprovada → outputs estratégicos aprovados → implementação existente.
- Visual: confirmação explícita mais recente → Manual de Marca aprovado mais recente → diagnóstico visual aprovado → assets oficiais → referências externas → implementação existente.
- Copy: copy explicitamente aprovada → output estratégico de landing page aprovado → implementação existente.
- Links: confirmação explícita → implementação existente aprovada.

Registrar todo conflito de precedência. Para destino de release, vale apenas confirmação explícita do projeto/equipe e configuração local coerente. Qualquer conflito bloqueia; posicionamento, CRO, diagnóstico ou outro output estratégico não substituem silenciosamente a copy específica aprovada da landing page.

## 8. Procedimento

1. Confirmar que o relatório do quality gate corresponde ao estado atual dos arquivos.
2. Verificar branch, commit pretendido, worktree e diferenças desde o gate.
3. Confirmar o diretório exato que seria enviado.
4. Confirmar projeto e equipe Vercel com o responsável.
5. Se `.vercel/project.json` existir, conferir identidade do projeto sem expor tokens; divergência bloqueia.
6. Confirmar que não haverá criação automática de projeto, domínio ou alias.
7. Confirmar que nenhuma opção, script ou configuração aciona Production.
8. Preparar um resumo com artefato, destino, evidências, warnings aceitos e comando proposto.
9. Solicitar autorização explícita de Vercel Preview imediatamente antes da ação.
10. Somente depois da autorização, executar exclusivamente a Preview aprovada.
11. Registrar URL de Preview e evidência de que nenhum domínio/alias de produção foi alterado.
12. Encaminhar a URL para revisão humana; não promover o deploy.

## 9. Saídas esperadas

- Checklist de release e identidade do artefato.
- Destino de Preview confirmado, ou estado `BLOCKED`.
- Comando/ação de Preview proposto antes da execução.
- Se autorizado, URL de Preview e registro de revisão pendente.

## 10. Critérios de parada

Parar se houver arquivo alterado após o gate, worktree inesperado, projeto/equipe/diretório não confirmado, configuração divergente, autorização ambígua ou qualquer indício de Production. Falta de dado crítico sempre produz `STOP`.

## 11. Checkpoints humanos

- Aceitar warnings do quality gate, se houver.
- Autorizar commit e push separadamente, se necessários.
- Confirmar projeto, equipe e diretório.
- Autorizar explicitamente a Vercel Preview.
- Revisar a Preview antes de qualquer decisão posterior.

## 12. Proteções

O `AGENTS.md` raiz prevalece. Plugin, matriz, original e baseline são somente leitura. Preview não equivale a Production. Production, domínio e alias de produção permanecem proibidos. Não ler nem exibir tokens ou secrets.

## 13. Integração com a matriz

Consumir outputs e validações aprovados da matriz, mas rejeitar comandos incompatíveis, inclusive qualquer `vercel --prod` ou mutação de cliente/cache. Esta skill estende a matriz com gates locais de destino, Git e aprovação; não altera os componentes matriciais.

## 14. Ferramentas reutilizáveis

- Disponíveis: Git e inspeção local de configuração não secreta.
- Condicional: Vercel CLI somente se já disponível, destino confirmado e Preview explicitamente autorizada.
- Planejadas: verificador dedicado de release; não implementado nesta fase.
- Humanas: confirmação de destino, autorização e homologação da Preview.
- Proibidas: `vercel --prod`, promoção, domínio, alias de produção e criação automática de projeto.

## 15. Ações proibidas

- Executar Production direta ou indiretamente.
- Usar `vercel --prod`, promover Preview ou configurar domínio/alias de produção.
- Fazer deploy para projeto ou equipe não confirmados.
- Criar projeto Vercel automaticamente.
- Tratar autorização de escrita, commit ou push como autorização de Preview.

## 16. Definição de sucesso

O artefato e o destino estão inequivocamente identificados, todos os gates foram respeitados e, quando expressamente autorizada, somente uma Preview isolada é criada para revisão humana, sem efeito em Production.
