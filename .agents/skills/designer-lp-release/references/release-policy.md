# Política de release de landing pages

## Princípio central

Vercel Preview não é Production. A camada de produção de landing pages encerra sua responsabilidade na preparação e, quando autorizada, na criação de uma Preview isolada para homologação humana.

Production está desabilitada neste fluxo.

## Estados permitidos

- `release_not_ready`: quality gate ausente, inválido ou desatualizado.
- `release_ready`: artefato e destino conferidos; Preview ainda não autorizada.
- `preview_authorized`: responsável autorizou explicitamente uma Preview específica.
- `preview_created`: URL de Preview registrada e aguardando revisão humana.
- `human_approved`: Preview revisada; não implica autorização de Production.
- `blocked`: requisito, identidade ou autorização ausente ou conflitante.

Não existe estado `production_authorized` neste contrato.

## Checklist anterior à Preview

Verificar e registrar:

1. Projeto/cliente e diretório exato da implementação.
2. Branch correta.
3. Commit pretendido e sua relação com os arquivos avaliados.
4. Worktree limpo ou diferenças explicitamente compreendidas e aprovadas.
5. Quality gate atual em `PASS` ou `PASS_WITH_WARNINGS` aceito.
6. Testes locais concluídos.
7. Projeto e equipe Vercel confirmados pelo responsável.
8. `.vercel/project.json`, se existir, coerente com a confirmação e lido sem expor secrets.
9. Ausência de criação automática de projeto.
10. Ausência de flags, scripts ou configurações de Production.
11. Autorização humana explícita para esta Preview, após apresentação do destino e da ação.

Se qualquer item falhar, retornar `blocked` sem deploy.

## Autorizações independentes

- Aprovação de edição não autoriza commit.
- Aprovação de commit não autoriza push.
- Aprovação de push não autoriza Preview.
- Aprovação de Preview não autoriza Production, promoção, domínio ou alias.
- Homologação humana da Preview não cria autorização implícita para Production.

Cada operação exige consentimento explícito no seu próprio contexto.

## Ações permitidas

- Inspecionar estado Git e configurações locais não secretas.
- Preparar o resumo de release sem executar deploy.
- Executar somente a Vercel Preview descrita e autorizada.
- Registrar a URL de Preview e encaminhá-la para revisão humana.

## Ações proibidas

- Executar `vercel --prod` ou qualquer equivalente.
- Promover Preview para Production.
- Criar ou alterar domínio ou alias de produção.
- Selecionar projeto/equipe por inferência.
- Criar projeto Vercel automaticamente.
- Ler, copiar, registrar ou exibir credenciais, tokens ou `.env`.
- Modificar código, copy, link, asset ou configuração durante o release.
- Fazer commit ou push sem autorização específica.

## Mudança após o quality gate

Qualquer alteração no artefato, dependência ou configuração depois do gate invalida a decisão anterior. Retornar ao `designer-lp-quality-gate` antes de solicitar nova autorização de Preview.

## Registro mínimo

Registrar sem secrets:

- data e responsável pela autorização;
- branch, commit e estado do worktree;
- diretório e projeto/equipe confirmados;
- resultado do quality gate;
- ação executada;
- URL da Preview;
- confirmação de que Production, domínio e alias permaneceram intocados.
