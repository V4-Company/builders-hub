# Contrato do pipeline de landing pages

## Fluxo exato

```text
client-knowledge-sync (quando necessário)
→ designer-lp-source-audit
→ designer-lp-baseline-prepare
→ designer-lp-design-adapter
→ designer-lp-asset-pipeline
→ designer-lp-quality-gate
→ designer-lp-release
→ revisão humana
```

`client-knowledge-sync` é condicional e não cria um estado próprio no pipeline da landing page. Nenhuma etapa autoriza implicitamente a seguinte.

## Contrato de estados

### `source_audited`

- Responsável: `designer-lp-source-audit`.
- Entrada: fontes acessíveis em modo somente leitura.
- Saída exigida: implementação e fontes identificadas, lacunas e conflitos registrados.
- Gate humano: confirmar a implementação candidata.
- STOP: fonte crítica ausente, versão ambígua ou conflito não resolvido.

### `baseline_approved`

- Responsável: `designer-lp-baseline-prepare`.
- Entrada: `source_audited` e plano de caminhos aprovado.
- Saída exigida: `reference/` imutável, `src/` separado e manifesto conferido.
- Gate humano: aprovar baseline e fronteira de proteção.
- STOP: destino existente, hash divergente ou risco de sobrescrita.

### `section_authorized`

- Responsáveis: humano e `designer-lp-design-adapter`.
- Entrada: baseline aprovada e proposta delimitada.
- Saída exigida: uma seção, arquivos e operações explicitamente autorizados.
- Gate humano: autorização anterior à escrita.
- STOP: escopo genérico, conteúdo não congelado ou múltiplas seções.

### `implementation_reviewed`

- Responsável: `designer-lp-design-adapter`.
- Entrada: `section_authorized`.
- Saída exigida: implementação local concluída e revisão estética/responsiva humana.
- Gate humano: aceitar fidelidade visual e itens preservados.
- STOP: perda visual, alteração de copy/link/claim ou asset não autorizado.

### `assets_approved`

- Responsável: `designer-lp-asset-pipeline`.
- Entrada: implementação revisada e assets identificados.
- Saída exigida: origem, direitos, derivados, comportamento responsivo e fallbacks aprovados.
- Gate humano: aprovar seleção e transformações.
- STOP: origem/direito desconhecido, original ausente ou stock não autorizado.

### `quality_gate_passed`

- Responsável: `designer-lp-quality-gate`.
- Entrada: implementação e assets aprovados.
- Saída exigida: `PASS` ou `PASS_WITH_WARNINGS` aceito, com evidências atuais.
- Gate humano: revisão e aceitação de warnings.
- STOP: `BLOCKED`, teste crítico ausente ou mudança inesperada.

### `preview_authorized`

- Responsáveis: humano e `designer-lp-release`.
- Entrada: quality gate válido e destino confirmado.
- Saída exigida: autorização explícita para uma Preview específica.
- Gate humano: confirmar projeto, equipe, diretório e ação.
- STOP: autorização ambígua, worktree mudou ou qualquer risco de Production.

### `human_approved`

- Responsável: revisor humano.
- Entrada: Preview criada de forma autorizada ou artefato local apresentado para homologação.
- Saída exigida: decisão de homologação registrada.
- Estado terminal deste contrato.
- Não autoriza Production.

Não existe `production_authorized`.

## Interrupção, invalidação e retomada

- `STOP` é a ação operacional de interromper a execução porque uma pré-condição, evidência ou autorização está ausente.
- `BLOCKED` é o estado ou resultado formal de um gate que não pode ser aprovado.
- Ausência de autorização para executar produz `STOP`; quality gate com baseline modificada produz `BLOCKED`.
- Nenhuma dessas definições cria novo estado no pipeline.
- Ao receber `STOP` ou `BLOCKED`, manter o último estado comprovado e informar obrigatoriamente: condição bloqueadora; evidência, autorização ou informação exata ausente; responsável esperado pela resolução; último estado válido; e próximo gate possível depois da resolução.
- Não usar mensagens vagas como “faltam dados”, “aguardando aprovação” ou “há pendências”.
- Retomar pela etapa bloqueada depois de evidência ou autorização nova.
- Mudança em fonte invalida auditoria e todos os estados dependentes.
- Mudança em baseline invalida autorização de seção e estados posteriores.
- Mudança em implementação ou asset invalida quality gate e release.
- Mudança após o quality gate exige nova execução do gate.
- Não pular estados nem converter silêncio em aprovação.

## Responsabilidades da matriz

- Produzir e manter estratégia aprovada.
- Fornecer `client.json`, base estratégica, posicionamento e diagnósticos.
- Produzir output estratégico de landing page e Manual de Marca quando aplicáveis.
- Oferecer revisores e validadores como componentes consultáveis.
- Permanecer somente leitura para a camada local durante esta fase.

## Responsabilidades da unidade

- Sincronizar conhecimento operacional somente quando necessário e autorizado.
- Auditar fontes e escolher a implementação com evidência.
- Proteger a baseline em cópia isolada.
- Adaptar uma seção autorizada sem alterar estratégia ou conteúdo congelado.
- Governar assets e derivados.
- Executar quality gate integrado e registrar evidências reais.
- Preparar e, apenas com autorização, criar Vercel Preview.
- Manter Production desabilitada.

## Limites de integração

- Outputs da matriz podem ser consumidos; nunca modificados por este pipeline.
- Instruções matriciais de mutação de cliente, cache, deploy ou Production não são herdadas.
- Componentes matriciais podem ser citados e compostos conceitualmente sem copiar instruções inteiras.
- O `AGENTS.md` raiz prevalece em todas as etapas.
- Commit, push, Preview e qualquer escrita possuem autorizações distintas e limitadas.
