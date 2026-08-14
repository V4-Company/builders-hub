---
name: designer-lp-orchestrator
description: Coordenar o pipeline de produção de landing pages por estados, gates humanos e contratos entre skills. Usar para iniciar, retomar ou determinar a próxima etapa segura; não usar para editar design/código, decidir copy/claims/imagens, alterar links ou executar deploy.
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


# LP Orchestrator

## 1. Propósito

Coordenar a sequência operacional da landing page, preservar o estado auditável e impedir que uma etapa avance sem evidência e checkpoint humano. Não realizar o trabalho especializado das skills coordenadas.

Ao executar, ler [references/pipeline-contract.md](references/pipeline-contract.md) integralmente.

## 2. Quando usar

- Para iniciar um novo fluxo de landing page.
- Para retomar trabalho interrompido e localizar o último gate válido.
- Para identificar a próxima skill, evidência ou autorização necessária.

## 3. Quando NÃO usar

- Para editar HTML, CSS, JavaScript, design, Figma ou assets.
- Para decidir ou alterar copy, claims, imagens, preços, métricas ou links.
- Para executar commit, push ou deploy.
- Para contornar um `STOP` emitido por outra skill.

## 4. Pré-condições

1. Ler o `AGENTS.md` raiz e instruções locais.
2. Auditar branch, worktree, cliente, projeto e escopo.
3. Confirmar que plugin e outputs da matriz são somente leitura.
4. Identificar registros existentes de estados e aprovações.
5. Não presumir que uma ação passada autoriza a próxima.

## 5. Entradas

- Pedido atual e escopo autorizado.
- Evidências e saídas das skills do pipeline.
- Aprovações humanas registradas.
- Estado Git e identificação do projeto.
- Outputs estratégicos aprovados da matriz, apenas como entradas.

## 6. Fontes permitidas

- Registros produzidos pelas oito skills locais.
- Confirmações explícitas do responsável.
- Estado Git e arquivos do cliente permitidos pela governança.
- Outputs aprovados da matriz em modo somente leitura.

Referências externas não definem estado nem fatos do projeto.

## 7. Precedência das fontes

- Fatos: confirmação explícita mais recente → `client.json` → base estratégica aprovada → outputs estratégicos aprovados → implementação existente.
- Visual: confirmação explícita mais recente → Manual aprovado mais recente → diagnóstico visual aprovado → assets oficiais → referências externas → implementação existente.
- Copy: copy explicitamente aprovada → output estratégico de landing page aprovado → implementação existente.
- Links: confirmação explícita → implementação existente aprovada.

Uma confirmação recente não apaga o histórico: registrar a decisão e o conflito. Documento especializado posterior pode prevalecer apenas em seu domínio.

## 8. Procedimento

1. Identificar o último estado comprovado por evidência ainda válida.
2. Validar as condições de entrada e saída desse estado no contrato do pipeline.
3. Se houver mudança posterior, invalidar os estados dependentes e retornar ao gate apropriado.
4. Determinar uma única próxima etapa segura.
5. Apresentar escopo, arquivos, ações e checkpoint humano exigidos pela etapa.
6. Invocar conceitualmente a skill responsável; não executar sua função no orquestrador.
7. Para todo `STOP` ou `BLOCKED`, informar obrigatoriamente: condição bloqueadora; evidência, autorização ou informação exata ausente; responsável esperado pela resolução; último estado válido; e próximo gate possível depois da resolução.
8. Interromper em qualquer `STOP`; retomar somente após a condição ser resolvida.
9. Encerrar em `human_approved`. Não criar estado ou caminho para Production.

Estados, em ordem:

```text
source_audited
→ baseline_approved
→ section_authorized
→ implementation_reviewed
→ assets_approved
→ quality_gate_passed
→ preview_authorized
→ human_approved
```

## 9. Saídas esperadas

- Estado atual e evidência que o sustenta.
- Próxima etapa única, skill responsável e pré-condições.
- Checkpoint humano pendente e escopo de autorização.
- Registro de interrupção/retomada e invalidações.
- Para todo bloqueio, identificação precisa da condição, do item ausente, do responsável, do último estado válido e do próximo gate possível.

## 10. Critérios de parada

`STOP` é a ação operacional de interromper a execução porque falta uma pré-condição, evidência ou autorização. `BLOCKED` é o estado ou resultado formal de um gate que não pode ser aprovado. Ausência de autorização para executar produz `STOP`; um quality gate que detecta baseline modificada produz `BLOCKED`. Não criar novos estados do pipeline.

Parar se evidência, dado crítico, fonte, autorização ou estado anterior estiver ausente ou conflitante; se houver mudança inesperada; ou se a próxima ação exceder o escopo. Identificar exatamente o item ausente e nunca usar mensagens vagas como “faltam dados”, “aguardando aprovação” ou “há pendências”. Nunca inventar fatos, claims, depoimentos, links, preços ou métricas para avançar.

## 11. Checkpoints humanos

- Aprovar baseline e fronteira imutável.
- Autorizar uma seção e os arquivos de cada execução.
- Revisar implementação e assets.
- Aceitar o quality gate e seus warnings.
- Autorizar Preview explicitamente.
- Homologar a Preview sem implicar Production.

## 12. Proteções

O `AGENTS.md` raiz prevalece e regras locais não podem enfraquecê-lo. Plugin e outputs da matriz são somente leitura. Não modificar copy, link ou asset sem aprovação, não ler secrets e não agrupar autorizações. Commit/push são separados; Preview exige autorização; Production é proibida.

## 13. Integração com a matriz

Coordenar consumo de outputs aprovados de `ee-s3-landing-page`, Manual de Marca, posicionamento, diagnósticos e revisão. A matriz responde por estratégia e seus artefatos; a unidade responde por baseline, adaptação, assets, quality gate e Preview controlada. Não modificar a matriz nem executar seus fluxos incompatíveis.

## 14. Ferramentas reutilizáveis

- Disponíveis: estado Git, arquivos de evidência existentes e leitura dos contratos locais.
- Planejadas: armazenamento estruturado de estado; não implementado nesta fase.
- Humanas: todas as aprovações e decisões de conflito.
- Proibidas: edição especializada, mutação automática de estado do cliente e qualquer deploy pelo orquestrador.

## 15. Ações proibidas

- Editar design, código, Figma, copy, claims, imagens ou links.
- Escolher silenciosamente entre fontes conflitantes.
- Marcar estado sem evidência ou pular gate.
- Comunicar `STOP` ou `BLOCKED` sem identificar precisamente o item ausente e o responsável pela resolução.
- Executar commit, push, Vercel Preview ou Production.
- Criar o estado `production_authorized`.

## 16. Definição de sucesso

Em qualquer momento, o projeto possui um único estado comprovado, uma próxima ação segura e um checkpoint humano claro; interrupções são retomáveis e nenhum gate ou proteção de release pode ser contornado.
