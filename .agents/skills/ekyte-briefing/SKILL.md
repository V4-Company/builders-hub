---
name: ekyte-briefing
description: Monta briefings ricos e estruturados pra tarefas do Ekyte com base em templates locais por sigla, contexto puxado do NotebookLM do cliente, e perguntas ativas estruturadas. Usado como subskill da `/ekyte-task` — recebe pacote {cliente, sigla, tipo, qtd, input, modo} e devolve HTML rico formatado pronto pra entrar no campo `description`/`description_create_task` do Ekyte, com heads e labels em negrito. Pode ser invocada avulsa quando o usuário só quer pensar/estruturar uma demanda sem subir task. Suporta modo 5W1H quando vem planilha de plano de ação.
area: ekyte
author: fabio
version: 1.0.0
user-invocable: true
---

# /ekyte-briefing — Geração de briefing rico pra tasks do Ekyte

Substitui o briefing "uma linha + `<<PREENCHER>>`" da v1 da `/ekyte-task` por um briefing estruturado, profundo e pré-preenchido com contexto do NotebookLM do cliente.

## Regra soberana de formatação Ekyte (atualizada em 2026-06-15)

Briefings enviados ao Ekyte devem ser **HTML rico**, não texto plano. Esta regra substitui qualquer orientação legada neste arquivo que diga para remover HTML ou converter tudo para texto simples.

Padrão obrigatório:
- Seções principais viram heads visuais maiores e em negrito: `<div><strong><span style="font-size: 18px;">ATIVOS DA CAMPANHA</span></strong></div>`.
- Labels de campo ficam em negrito: `<div><strong>Drive do Cliente:</strong> <a href="...">...</a></div>`.
- Listas de entregáveis, guardrails e métricas usam `<ul><li>...</li></ul>`.
- Espaçamento entre blocos usa `<div><br></div>`.
- Não usar `<h1>` ou `<h2>`. CSS inline só é permitido em heads de seção para aumentar fonte (`font-size: 18px`). O Ekyte renderiza melhor com `<div>`, `<strong>`, `<span style="font-size: 18px;">`, `<a>`, `<ul>` e `<li>`.
- Preferir texto ASCII dentro do HTML quando a API retornar acentos quebrados como `?`; visual correto > acento quebrado.
- O campo `briefing_ekyte_text` pode manter esse nome por compatibilidade, mas seu conteúdo deve ser HTML rico.

## Quando usar

**Modo subskill (principal)** — invocada pela `/ekyte-task` no passo 6 da criação de task. Recebe pacote estruturado, devolve briefing em HTML rico formatado pronto.

**Modo avulso** — Fabio chama direto:
- `/ekyte-briefing` + descrição livre
- "me brieffa um CA pro Cliente A com foco em remarketing produto X"
- "preciso pensar essa demanda CRM antes de subir — me ajuda a montar o briefing"

Em modo avulso, a skill devolve o HTML rico formatado para Ekyte **e** o Markdown limpo, e pergunta se Fabio quer subir como task (aí invoca `/ekyte-task`).

## Pré-requisitos

- MCP `ekyte` configurada (pra eventual lookup de tipo de tarefa).
- Cache `clientes/_skill-ekyte/cache.md` populado (workspaces/projetos/tipos).
- `clientes/_skill-ekyte/drives.md` populado (drives dos clientes).
- `clientes/_skill-ekyte/briefing-templates/*.md` presentes (templates por sigla + base + universal + 5W1H).
- Cliente alvo deve ter `clientes/<cliente>/CLAUDE.md` com bloco `## NotebookLM`. Em modo subskill da `/ekyte-task`, a skill deve tentar consultar NotebookLM; se faltar cadastro, pedir cadastro ou autorização explícita do gerente de projetos para seguir sem NotebookLM.
- `notebooklm-py` autenticado (pra `/cs-notebooklm-consulta-cliente` rodar). Se não estiver, pedir login ou autorização explícita do gerente de projetos para seguir sem síntese.

Os dois pré-requisitos de NotebookLM acima só são bloqueantes quando o pacote recebe `notebook_obrigatorio: true`. Tarefas da whitelist operacional chegam com `notebook_obrigatorio: false` e não devem abrir bloqueio de cadastro/login.

## Pacote de entrada (modo subskill)

A `/ekyte-task` passa:

```json
{
  "cliente": "Cliente A",
  "cliente_alias": "cliente-a",
  "sigla": "CA",
  "task_type_name": "Criativo Ads",
  "task_type_id": "29740",
  "qtd": 9,
  "titulo": "[09][CA][IA] Cliente A | Remarketing produto X",
  "input_livre": "cria 9 CAs pro Cliente A com foco em remarketing produto X",
  "modo": "texto_livre",   // ou "planilha_demandas" ou "5w1h"
  "projeto_novo": false,
  "notebook_obrigatorio": true,
  "motivo_isencao_notebook": null,
  "planilha_5w1h_url": null,  // preenchido se modo=5w1h
  "planilha_demanda_row": null  // preenchido se modo=planilha_demandas
}
```

## Fluxo

### 1) Carregar contexto inicial

Em paralelo (independentes):
- Ler `clientes/_skill-ekyte/drives.md` → mapa cliente → drive_link
- Ler `clientes/_skill-ekyte/backups-crm.md` (se sigla é CRM-relacionada)
- Ler `clientes/<cliente>/CLAUDE.md` → extrair Notebook ID do bloco `## NotebookLM`
- Carregar `clientes/_skill-ekyte/briefing-templates/_header-universal.md`
- Carregar template específico da sigla (ex: `CA.md`). Se sigla é criativa (CA/LP/RV), carregar também `_base-criativo.md`.

### 2) Decidir modo de operação

Antes de decidir o modo de entrada, respeitar a classificação recebida da `/ekyte-task`:

- `notebook_obrigatorio: true` → seguir os passos 3 a 5 e consultar `/cs-notebooklm-consulta-cliente`.
- `notebook_obrigatorio: false` → pular os passos 3, 3.5, 4 e 4.5; registrar `motivo_isencao_notebook`; montar briefing operacional a partir da descrição, links de Drive/backup e template. Não exigir NotebookLM cadastrado nem login.
- Campo ausente → assumir `true`. A falha segura é consultar.
- `projeto_novo: true` → forçar `notebook_obrigatorio: true`, exceto projetos internos de timesheet/rotina administrativa sem contexto de cliente.

Whitelist aceita para `notebook_obrigatorio: false`: otimização de campanhas recorrente; atualização de Growth Pack recorrente; apontamento de horas/timesheet; atendimento/comunicação recorrente; envio recorrente de NPS/CSAT; atualização administrativa interna recorrente sem decisão estratégica. Qualquer análise, criação, implementação, tracking, CRM, automação, projeção, campanha, público, pesquisa ou planejamento exige NotebookLM.

**Modo `texto_livre`** (default): segue fluxo padrão.

**Modo `5w1h`**: input contém link de planilha 5W1H + skill validou cabeçalho. Pula `_base-criativo.md`, carrega `_5w1h.md` e usa como layout principal. Skill abre a planilha (WebFetch) e extrai os 6W.

**Modo `planilha_demandas`**: input veio da planilha de demandas (já manipulada pela `/ekyte-task`). Skill recebe o `planilha_demanda_row` com colunas `descricao`, `Tags`, etc — usa `descricao` como base e enriquece via NotebookLM.

### 3) Cache de sessão NotebookLM

Verificar se já tem síntese cacheada pro cliente nesta conversa:

```
sessao_notebook_cache = {
  "Cliente A": { "sintese": "...", "ts": "2026-04-30 10:15", "perguntas": [...] }
}
```

- **Cache HIT** (cliente já consultado): reusar síntese.
- **Cache MISS** OU primeira task do cliente na sessão: seguir pro passo 3.5 antes de invocar NotebookLM.

### 3.5) Cache persistente de público (TTL 90d)

Antes de invocar `/cs-notebooklm-consulta-cliente`, checar `clientes/<cliente>/publicos-cache.md`. Formato e regras: ver [_publicos-cache-template.md](../../../clientes/_skill-ekyte/_publicos-cache-template.md).

1. **Identificar a linha/categoria** a partir do título/input:
   - Produto explícito no título (`Saint Tropez`, `Cliente A Baby`) → mapear pra linha conhecida.
   - Sinal contextual sem produto (`remarketing produto X`) → perguntar ao Fabio qual linha.
   - Cliente sem segmentação (Cliente C, Cliente D) → linha `Geral`.

2. **Abrir `publicos-cache.md`** do cliente. Buscar bloco `## <linha>` (match case-insensitive, ignora acentos).

3. **Decidir HIT/STALE/MISS:**
   - **HIT** (idade < 75d): pré-preencher campos 3-9 do `_base-criativo.md` (consciência, faixa, sexo, ganchos) + avatar/ofertas/restrições/tom-de-voz com os valores do cache. Marcar no preview: `[do cache: <linha> · <N>d]`. Cache cobre público; não substitui a consulta NotebookLM quando `projeto_novo: true` ou quando ainda não existe síntese de sessão para o cliente.
   - **STALE** (75d ≤ idade < 90d): usa o cache **mas** mostra aviso no preview da pergunta ativa: `⚠️ cache de público da linha "<X>" tem <N>d (expira em <M>d). Quer atualizar antes de seguir? (sim/não, default não)`. Resposta sim = força MISS path. Não/silêncio = HIT silencioso.
   - **MISS** (idade ≥ 90d OU bloco inexistente OU arquivo inexistente): segue pro passo 4 (NotebookLM completo). Após sucesso da consulta, **escrever o bloco no cache** (passo 4.5).

4. **Modo planilha com OBS robusta:** se o pacote de entrada veio da `/ekyte-task` com descrição substancial, usar a OBS como base do briefing, não como substituta do NotebookLM. HIT de cache pode dispensar apenas a pergunta específica de público; MISS/STALE-com-update invoca `/cs-notebooklm-consulta-cliente` para atualizar público. Se `projeto_novo: true`, rodar consulta NotebookLM atual mesmo com cache HIT.

### 4) Invocar `/cs-notebooklm-consulta-cliente`

Compor as 5 perguntas dirigidas pelo tipo da task (cada template tem suas próprias na seção "Pré-preenchimento via NotebookLM").

Tarefa enviada:
```
"vou montar briefing de [tipo] (sigla [sigla]) pro [cliente]. preciso saber: [resumo das 5 perguntas]"
```

A skill `/cs-notebooklm-consulta-cliente` faz o trabalho pesado: decompõe, dispara, agrega, salva artefato. Retorna síntese estruturada.

**Se a `/cs-notebooklm-consulta-cliente` retornar erro** (sessão expirada, cliente sem NotebookLM, etc):
- Em modo subskill da `/ekyte-task`: pausar e pedir decisão. Cliente sem NotebookLM cadastrado → pedir `/notebooklm-cadastrar` ou comando explícito do gerente de projetos para seguir sem NotebookLM; sessão expirada → pedir `notebooklm login` ou comando explícito para seguir sem síntese.
- Em modo subskill com `projeto_novo: true`: a tentativa de consulta NotebookLM é obrigatória. Se falhar, só continuar com autorização explícita do gerente de projetos, registrando no briefing que foi criado sem síntese NotebookLM.
- Em modo avulso: avisar Fabio e perguntar se ele quer seguir sem síntese apenas como rascunho.

Cachear síntese em memória (sessão).

### 4.5) Popular cache persistente de público (após sucesso do passo 4)

Se o passo 3.5 deu MISS/STALE-com-update e o passo 4 (NotebookLM) retornou síntese válida, **escrever bloco no cache** antes de seguir pro 5:

1. Abrir/criar `clientes/<cliente>/publicos-cache.md` (formato em [_publicos-cache-template.md](../../../clientes/_skill-ekyte/_publicos-cache-template.md)).
2. Se já existe bloco `## <linha>`: **substituir inteiro** (preserva os demais blocos do arquivo).
3. Se não existe: **acrescentar ao final** do arquivo.
4. Atualizar header "Última escrita: YYYY-MM-DD".
5. Campos a gravar (NotebookLM silencioso em algum = `_não documentado_`, **nunca fabricar**):
   - `ult_consulta`, `expira` (ult_consulta + 90d), `fonte` (URL do notebook)
   - `Avatar` (texto narrativo 2-4 linhas)
   - `Faixa etária dominante` (bins)
   - `Sexo` (Masculino|Feminino|Ambos)
   - `Nível de consciência` (1-5 com labels)
   - `Ganchos com tração documentada` (lista)
   - `Ofertas que já rodaram`, `Restrições documentadas`, `Tom de voz`

Esse cache fica disponível pras próximas sessões (modo inline rápido da `/ekyte-task` consome direto sem precisar invocar essa skill).

### 5) Pré-preenchimento dos campos do template

Com a síntese em mãos, varrer o template da sigla e pré-preencher campos onde a síntese tem informação.

Marcar campos pré-preenchidos com `[sugerido pelo NotebookLM, confirma?]` no preview de pergunta. Se Fabio aceitar tudo, vira valor final; se editar, vai a edição.

### 6) Pergunta ativa em lote

Listar **todas** as perguntas do template em uma só rodada, numeradas. Pré-preenchidos aparecem com a sugestão visível.

Formato:

```
📋 BRIEFING: [09][CA][IA] Cliente A | Remarketing produto X

Pra montar o briefing, responde as perguntas abaixo. Pode responder tudo de uma vez,
em qualquer formato — se ficar dúvida, eu pergunto de novo só do que ficou solto.

NotebookLM consultado em 2026-04-30 10:15. Síntese disponível e usei pra
pré-preencher [N] campos. Você confirma ou ajusta abaixo.

──────────────────────────────────────────────

1) Tema/Produto: [sugerido: "Remarketing produto X — colchões mola ensacada R$ 2.5k+"]
2) Motivação: [sugerido: "Reativar carrinho abandonado e visitantes de PDP"]
3) Condição/Oferta (opcional):
4) Observações relevantes (opcional):
5) Objetivo (1-6, multi):
   1) Alcance  2) WhatsApp  3) Cadastro  4) Vídeo  5) Remarketing  6) Compra
   [sugerido: 5,6]
... (continua até a última)
```

Fabio responde. Skill interpreta — aceita formatos variados (números, texto livre, "ok pra todos os sugeridos").

**Se Fabio responder "ok" / "tudo ok pelos sugeridos"**: skill aceita os pré-preenchidos e pergunta só os campos sem sugestão.

### 7) Validar campos universais

Antes de montar o briefing final:

- **Drive do Cliente:** já lido em `drives.md`. Se cliente é DOM (sem Drive) ou não mapeado, perguntar e oferecer `/ekyte-briefing-refresh`.
- **NotebookLM:** já lido do CLAUDE.md.
- **KV** (sigla criativa): se Fabio não passou KV no input nem na pergunta ativa, perguntar agora ("KV específico pra essa campanha? cole o link ou diga 'usa KV padrão do Drive'"). Se "padrão do Drive", colocar `KV padrão (ver pasta Drive)`.
- **Referência:** se passou no input, usar. Senão, omitir.
- **Pra CRM:** Planilha Backup, Ferramenta, Acesso (perguntas A, B, C do `CRM.md`).

### 8) Montar Markdown completo

Ordem de composição:

```
BRIEFING — {{cliente_uppercase}} — {{tipo_uppercase}}
Tarefa: {{titulo}}

[bloco _header-universal.md preenchido]

[se sigla criativa: bloco _base-criativo.md preenchido]
[se modo 5w1h: bloco _5w1h.md no lugar do _base-criativo.md]

[bloco específico da sigla preenchido — CA.md / LP.md / etc]
```

### 9) Conversor Markdown → HTML rico formatado (Ekyte)

**Regra atual (2026-06-15):** converter Markdown/briefing final para HTML rico antes de enviar ao Ekyte. Ignorar instruções legadas que mandem remover HTML, `strong`, links ou listas.

Mapa de conversão obrigatório:
- Título/linha de tarefa: `<div><strong>Tarefa:</strong> ...</div>`
- Head de seção: `<div><strong><span style="font-size: 18px;">NOME DA SEÇÃO</span></strong></div>`
- Label de campo: `<div><strong>Nome do Campo:</strong> valor</div>`
- Link: `<a href="URL" target="_blank">URL</a>`
- Lista: `<ul><li>item</li></ul>`
- Separador/linha em branco: `<div><br></div>`

Exemplo mínimo:

```html
<div><strong>Tarefa:</strong> [01][PRI-A][IA] Cliente | Demanda</div>
<div><br></div>
<div><strong><span style="font-size: 18px;">ATIVOS DA CAMPANHA</span></strong></div>
<div><strong>Drive do Cliente:</strong> <a href="https://drive.google.com/..." target="_blank">https://drive.google.com/...</a></div>
<div><strong>NotebookLM:</strong> <a href="https://notebooklm.google.com/..." target="_blank">https://notebooklm.google.com/...</a></div>
<div><br></div>
<div><strong><span style="font-size: 18px;">OBJETIVO</span></strong></div>
<div>Texto do objetivo.</div>
<div><br></div>
<div><strong><span style="font-size: 18px;">ENTREGÁVEIS ESPERADOS</span></strong></div>
<ul><li>Entregável 1.</li><li>Entregável 2.</li></ul>
```

**Observação legada:** o bloco abaixo registra o comportamento antigo de texto plano. Ele fica como histórico, mas **não deve ser usado** para novas tasks.

⚠️ **DESCOBERTA 2026-04-30:** O Quill do Ekyte **não interpreta tags HTML** quando o conteúdo é enviado via API REST (campo `description_create_task`). Tags como `<div>`, `<h1>`, `<blockquote>`, `<strong>`, `<a>`, `<ul>` aparecem como **texto literal** no editor — não viram rich text. O Quill só interpreta HTML quando recebe via clipboard de fonte rich-text (ex: colado de um Google Doc) ou quando o usuário clica nos botões da toolbar.

**Conclusão: enviar via API = texto plano formatado.** O Ekyte renderiza isso em fonte monospace dentro de uma caixa estilo code block (fundo escurecido), preservando quebras de linha, bullets, emojis numerados, etc. Fica perfeitamente legível e organizado — só não tem cores nem `<h1>` rich.

Função `md_to_ekyte_plain(md_string) -> string`:

```
Regras (aplicadas linha-a-linha):

ESTRUTURA (preservar como texto):
1. Linha em branco                     → linha em branco (\n)
2. Linha começando com "## "           → "<emoji-numerado> TÍTULO EM CAIXA ALTA" (substitui ## por emoji ou só CAIXA ALTA)
3. Linha começando com "### "          → "TÍTULO Sub-seção:" (sem caixa alta)
4. Linha começando com "- " ou "* "    → "• texto"
5. Texto comum                         → mantém como está
6. **negrito**                         → REMOVER asteriscos, manter texto plano (texto monospace já dá ênfase visual)
7. *itálico*                           → REMOVER asteriscos, manter texto plano
8. [texto](url)                        → "texto: url"  OU  só "url" se texto for vazio/redundante
9. URLs soltas                         → manter como estão (Quill detecta e converte em link clicável automaticamente)

CONVENÇÕES VISUAIS (já que não temos cor/negrito):
- Cabeçalhos de seção principais: usar emojis numerados pré-fixos (1️⃣, 2️⃣, 3️⃣...) seguido de TÍTULO EM CAIXA ALTA
- Sub-seções: TÍTULO em caixa alta + ":" no fim, sem emoji
- Avisos / proibições: prefixar com ⚠️
- Listas/produtos: numeração explícita "1. ", "2. ", etc.
- Bullets: "•" (caractere unicode, mais limpo que "-")
- Separadores entre seções: linha em branco dupla ou linha de "─" se quiser destacar
```

**Exemplo de output bem formatado (referência: o briefing que renderizou bem na #2783891 quando colado):**

```
BRIEFING — CLIENTE A — CRIATIVO ADS
Tarefa: [22][CA][IA] Cliente A | Fotos ambientalizadas linha de colchões adultos

🔗 ATIVOS DA CAMPANHA

Drive do Cliente: https://drive.google.com/drive/folders/...
NotebookLM: https://notebooklm.google.com/notebook/...
⚠️ NotebookLM compartilhado entre Cliente A e Cliente B — esta task é Cliente A.

1️⃣ DIRECIONAMENTO DA CAMPANHA

Tema/Produto: Colchões — linha adulta completa do e-commerce
Motivação: Renovar banco de imagens dos PDPs
Observações Relevantes:
• Escopo é a linha adulta — excluir Cliente A Baby e Cama Cliente A Pet
• 2 variações de cena por produto (total 22 peças)

2️⃣ OBJETIVO

• Compra (uso primário: PDP)
Nota: não é mídia paga, é foto editorial pra PDP
```

**O que NÃO fazer no padrão atual:**
- Não enviar Markdown bruto com `**`, `##`, `[]()` esperando que o Ekyte converta.
- Não enviar texto plano seco quando houver heads, labels ou listas.
- Não usar `<h1>` ou `<h2>`.
- Não usar CSS inline em texto corrido ou labels; usar `style="font-size: 18px;"` somente nas heads de seção.
- Enviar HTML rico simples com `<div>`, `<strong>`, `<span>`, `<a>`, `<ul>` e `<li>`.

### 10) Preview da `/ekyte-briefing` (modo subskill)

Mostrar pra Fabio o briefing **renderizado em Markdown** (mais legível no chat) **antes** de devolver pra `/ekyte-task`:

```
📋 BRIEFING MONTADO — [09][CA][IA] Cliente A | Remarketing produto X

[markdown completo aqui — Fabio lê, edita ou aprova]

──────────────────────────────────────────────
Confirma? (sim / editar campo X / regerar do zero)
```

Se Fabio aprovar, skill devolve **HTML rico formatado para Ekyte** pra `/ekyte-task` (que cuida do preview da task em si e da chamada MCP).

Se modo avulso (não foi chamada pela `/ekyte-task`), perguntar se quer subir como task ("quer que eu invoque a /ekyte-task pra subir? sim/não").

### 11) Devolver pra /ekyte-task

Output estruturado:

```json
{
  "briefing_ekyte_text": "<div><strong>Tarefa:</strong> ...</div><div><br></div>...",
  "briefing_markdown": "BRIEFING — CLIENTE A...",
  "campos_pendentes": [],
  "notebook_consultado": true,
  "notebook_isento": false,
  "motivo_isencao_notebook": null,
  "notebook_cache_usado": false,
  "projeto_novo": false,
  "notebook_artefato": "clientes/cliente-a/contexto-notebook/2026-04-30-1015-briefing-criativo-ca.md"
}
```

A `/ekyte-task` injeta `briefing_ekyte_text` em `description_create_task` e segue o fluxo dela (preview de task, confirmação, MCP).

## Guardrails

1. **Cache de sessão NotebookLM é por cliente, não por sigla.** Sobreusar síntese de CA pra LP do mesmo cliente está OK — síntese trata do cliente, não do tipo. Mas pra cliente diferente, sempre re-consultar.

2. **Nunca fabricar dados.** Se NotebookLM disse 'NAO ENCONTRADO' pra avatar, **não** inventar avatar. Pré-preenchimento só usa o que veio literalmente da síntese. Se síntese silenciou, campo fica vazio e vai pra pergunta ativa.

3. **Perguntas ativas em lote única.** Não fragmentar em 12 perguntas separadas — faz UMA mensagem com todas, Fabio responde uma vez. Salvo se ele pedir uma por uma.

4. **Modo 5W1H só ativa com link explícito + validação.** Não detectar 5W1H "no chute" porque o input parece um plano. Sem link explícito, modo é texto_livre.

5. **Ekyte via API deve receber HTML rico simples.** Atualizado em 2026-06-15 após validação real em task: `<div>`, `<strong>`, `<span style="font-size: 18px;">`, `<a>`, `<ul>` e `<li>` renderizam melhor que texto plano. Cabeçalhos de seção devem sair maiores e em negrito; labels devem sair em negrito no tamanho normal. Não usar Markdown bruto nem `<h1>/<h2>`.

6. **Cliente sem NotebookLM cadastrado** (CLAUDE.md sem bloco `## NotebookLM`): em modo subskill da `/ekyte-task`, pausar e pedir cadastro ou autorização explícita do gerente de projetos para seguir sem NotebookLM. Se autorizado, marcar no briefing: `NotebookLM: não consultado por autorização do gerente de projetos`. Não tentar adivinhar contexto.

7. **Cliente sem Drive em `drives.md`** (Cliente H atualmente): perguntar no preview e oferecer `/ekyte-briefing-refresh` pra persistir.

8. **Não chamar MCP do Ekyte.** Esta skill **não** sobe nada — só monta briefing. A subida é da `/ekyte-task`.

9. **Cache de público não é compartilhado entre clientes**, mesmo quando NotebookLM é compartilhado (Cliente A+Cliente B). Cada cliente tem seu `publicos-cache.md` — público é por marca, não por notebook.

10. **MISS de cliente sem NotebookLM cadastrado**: não cachear nada. Briefing de task Ekyte só segue se o gerente de projetos autorizar explicitamente seguir sem NotebookLM; o `publicos-cache.md` **não é criado** pra esse cliente até que ele tenha NotebookLM.

11. **NotebookLM é default; isenção é whitelist.** Nunca inferir isenção porque a OBS está detalhada ou a tarefa parece fácil. Campo ausente ou classificação ambígua significa `notebook_obrigatorio: true`.

## Como invocar

- `/ekyte-briefing` — modo avulso, Fabio chama direto.
- Invocação automática pela `/ekyte-task` no passo 6 do fluxo dela.

## O que NÃO fazer

- Não chamar `criar_tarefa_tool` (responsabilidade da `/ekyte-task`).
- Não escrever briefing genérico de "uma linha" (motivo da skill existir).
- Não inventar avatar/oferta/restrição se NotebookLM não retornou.
- Não pular perguntas obrigatórias do template (Tema/Motivação são obrigatórios pra criativos).
- Não usar `<h1>`/`<h2>`/`<p>`; usar `<div>`, `<strong>`, `<span style="font-size: 18px;">` para heads, `<a>`, `<ul>` e `<li>`.
- Não rodar NotebookLM em paralelo (cara é browser automation lenta — sequencial).
