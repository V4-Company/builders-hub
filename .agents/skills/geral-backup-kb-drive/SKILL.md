---
name: geral-backup-kb-drive
description: Faz backup de uma KB (cliente, squad ou projeto) numa pasta do Google Drive, espelhando a estrutura de pastas e subindo so o que mudou desde a ultima vez. Antes de subir qualquer byte, checa a permissao da pasta destino e recusa se ela estiver publica, e nunca sobe .env, chave ou credencial. Use sempre que o usuario pedir backup, copia de seguranca, "sobe pro Drive", "manda pra pasta do cliente no Drive", quiser espelhar uma KB fora do repositorio, ou sincronizar o que mudou numa KB que ja tem backup — mesmo que ele nao fale a palavra "backup".
area: geral
author: luizfreitasv4
version: 1.0.0
---

# Backup de KB no Google Drive

KB de cliente vive gitignored no hub, ou seja, **fora do git nao existe copia**. Se a maquina morrer, morre junto o transcript que ninguem mais tem. Backup no Drive resolve isso — desde que a copia nao vire um vazamento.

E ai mora o unico risco real desta skill. Uma pasta de KB nao e homogenea: transcript de call e material de trabalho, mas `mission-control/personas-call.md` e a leitura de como negociar com cada pessoa do cliente, `checkins/*-review.md` diz onde a propria agencia falhou, e `.env` tem credencial. Copiar a pasta inteira sem olhar para onde ela vai transforma backup em publicacao.

Por isso o fluxo abaixo checa o destino **antes** de subir, e nao depois.

## Setup

Precisa do conector Google Drive conectado. Use as operacoes atuais do conector:

- `get_profile` — identifica o dominio do usuario autenticado
- `get_file_metadata` — resolve pasta, pais e permissoes
- `search` ou `list_folder` — encontra itens existentes no pai correto
- `create_folder` — recria a arvore de pastas
- `upload_file` — envia um arquivo local novo sem conversao
- `update_file` — substitui os bytes de um arquivo existente, preservando ID e revisoes

Nao use `create_file`: essa operacao cria Docs, Sheets ou Slides nativos e nao serve
para guardar os bytes originais de `.md`, `.pdf`, `.docx` e outros arquivos da KB.

Se o MCP nao estiver conectado, pare e oriente o usuario a conectar em Configuracoes → Conectores. Nao tente contornar com `gdrive` CLI ou upload manual.

## Passo 1 — Definir origem e destino

**Origem.** Se o usuario nao disse qual KB, liste `squads/*/clientes/*/` e `bases/*/` e pergunte. Se ele estiver trabalhando numa KB no contexto da conversa, use essa e confirme numa linha.

**Destino.** Peca o link da pasta do Drive. O ID e o trecho depois de `/folders/`:

```
https://drive.google.com/drive/folders/1AbC...XyZ?usp=sharing
                                       ^^^^^^^^^^ o ID
```

Rode `get_file_metadata` no ID para confirmar que existe e que e pasta
(`file_or_folder: folder` ou MIME `application/vnd.google-apps.folder`). Mostre o
nome da pasta ao usuario — e barato e evita subir 50 arquivos no lugar errado. O
conector confirma a escrita na primeira criacao ou upload; nao invente um campo de
capacidade que a resposta nao trouxe.

## Passo 2 — Checar a permissao do destino (a trava)

Rode `get_profile` para descobrir o dominio do usuario. Depois rode
`get_file_metadata` na pasta destino **e em cada pasta acima dela**, seguindo
`parent_ids` ate a raiz. Solicite metadados de `permissions`, `parents`, MIME e nome.
Permissao no Drive pode ser herdada: uma pasta aparentemente restrita dentro de uma
pasta aberta pode continuar exposta.

Procure por uma entrada assim:

```json
{"role": "reader", "type": "anyone"}
```

`type: anyone` significa que qualquer pessoa com o link le, sem login. Um link de pasta costuma ficar assim sem ninguem decidir isso: o Drive oferece "qualquer pessoa com o link" na hora de copiar, e quem so queria mandar o endereco para um colega aceita sem ler.

**Se achar `type: anyone` em qualquer nivel, pare.** Nao suba nada. Diga ao usuario, em texto curto:

- qual pasta esta aberta (a destino ou qual das pastas acima)
- que qualquer pessoa com o link le
- os arquivos daquela KB que ficariam expostos, nomeando 3 ou 4 concretos
- como fechar: Drive → botao direito na pasta → Compartilhar → em "Acesso geral", trocar "Qualquer pessoa com o link" por "Restrito"

Depois espere. Nao suba "so a parte segura" para adiantar, e nao remova a permissao
sozinho — mexer na regra de compartilhamento do Drive de outra pessoa pode quebrar
um link que o time usa. Quando o usuario disser que fechou, **rode
`get_file_metadata` de novo e confirme** antes de seguir.

**Se o usuario insistir em subir com a pasta aberta**, e decisao dele: registre em uma frase o que fica exposto, suba apenas o nivel MATERIAL do Passo 3, e nunca o nivel INTERNO nem os segredos.

**Falha fechada.** Se `source_visibility_status` vier como `access_not_verified`, ou
se a lista de permissoes necessaria nao vier, nao trate a pasta como restrita. Pare
antes do upload. Ofereca trocar por uma pasta cuja visibilidade seja verificavel ou,
com confirmacao explicita do usuario, seguir somente no modo Material. Nunca envie o
nivel Interno quando a visibilidade nao puder ser comprovada.

**Olhe tambem quem tem acesso nominal.** Liste os e-mails fora do dominio obtido por
`get_profile` e permissoes do tipo `domain`. Acesso externo ou para todo o dominio
nao prova vazamento publico, mas impede o modo Espelho por padrao. Use Material ou
peca uma pasta restrita ao time.

## Passo 3 — Classificar os arquivos

Rode o script, que faz a varredura, a classificacao e a comparacao com o backup anterior de uma vez:

```bash
python3 <pasta-da-skill>/scripts/plano-backup.py <caminho-da-kb> \
  --destino <id-da-pasta> --modo espelho
```

Passe sempre `--destino`. Se o manifesto local pertencer a outra pasta do Drive, o
script ignora os hashes antigos e marca tudo como novo; sem isso, um destino vazio
poderia parecer atualizado por engano. Escolha `--modo material` depois do Passo 4.

Ele devolve JSON com tres listas — `segredos`, `interno`, `material` — e, para cada arquivo, se mudou desde o ultimo backup. Os tres niveis:

**SEGREDO — nunca sobe, em nenhum modo, nem se o usuario pedir.** `.env`, `.env.*`,
`credentials.json`, `token.json`, `service-account*.json`, `*.pem`, `*.key`, links
simbolicos e lixo de sistema (`.DS_Store`, `Thumbs.db`, `.gitkeep`). `.env.example`
tambem fica fora: normalmente nao tem segredo, mas nao e dado operacional da KB. Se
o usuario pedir para subir credencial, ofereca um gerenciador de segredos.

**INTERNO — analise da agencia sobre o cliente, nao material do cliente.** `mission-control/`, `checkins/`, `CLAUDE.md`, `AGENTS.md`, `client.json`, e qualquer arquivo cujo nome contenha `analise-`, `review`, `sabatina` ou `diagnostico-interno`. Isso descreve como o cliente negocia, onde ele e fragil e onde a agencia falhou. Vai para o Drive so quando a pasta e restrita ao time.

**MATERIAL — o trabalho em si.** `calls/`, `docs/`, `outputs/`, `campanhas/`, `relatorios/`, `links.md`, `README.md`. Transcript e entregavel: sao o que de fato se perde se a maquina morrer, e o que o cliente ja viu ou ja disse.

Se aparecer arquivo que nao cai em nenhuma regra, o script marca como `naoclassificado` e **voce pergunta ao usuario** em vez de chutar. Regra nova aprendida vira uma linha no script.

## Passo 4 — Escolher o modo

- **Espelho** (`interno` + `material`): pasta restrita ao time. E o backup de verdade, o que voce quer na maioria das vezes.
- **Material** (so `material`): pasta que o cliente ou um parceiro enxerga.

Se a pasta e comprovadamente restrita ao time, proponha Espelho e siga. Se ha acesso
externo, de dominio amplo ou visibilidade desconhecida, so siga em Material depois de
deixar essa limitacao clara. Uma confirmacao basta; nao transforme isso numa entrevista.

## Passo 5 — Espelhar a estrutura

Recrie no destino a mesma arvore de pastas da KB, com os mesmos nomes — `calls/`, `docs/comercial/`, e assim por diante. Estrutura igual dos dois lados e o que permite conferir a olho se o backup esta completo e restaurar sem adivinhar.

Para cada pasta do campo `pastas` do plano, procure o nome exato dentro do pai exato.
Use `search` com um filtro equivalente a `'<parent_id>' in parents and name =
'<nome>' and trashed = false`, ou use `list_folder` e filtre a resposta. Escape
apostrofos no nome ao montar a consulta.

- nenhum resultado: crie com `create_folder(name, parent_folder)`
- um resultado que seja pasta: reaproveite o ID
- mais de um resultado, ou um arquivo com aquele nome: pare nesse ramo e pergunte
  qual usar; nao escolha por data

Criar `calls` uma segunda vez nao da erro no Drive: ficam duas pastas com o mesmo
nome e o backup se parte em duas.

Guarde o ID de cada pasta criada — voce vai precisar como `parentId` dos arquivos.

## Passo 6 — Subir so o que mudou

Para cada arquivo do plano com `mudou: true`, resolva o arquivo remoto nesta ordem:

1. Se o manifesto traz um `id`, confirme com `get_file_metadata` que ele ainda
   existe e corresponde ao destino esperado.
2. Sem ID valido, procure o nome exato dentro do pai exato. Se houver um unico
   arquivo, reaproveite-o. Se houver dois, pergunte; nao sobrescreva no escuro.
3. Se nao houver arquivo, use `upload_file` com o caminho local absoluto em
   `file_uri`, `file_name`, o MIME do plano e `parent_folder_id`.
4. Se houver arquivo, use `update_file` com `fileId`, o caminho local absoluto em
   `file_uri` e o MIME. Isso preserva o ID e o historico de revisoes do Drive.

O fluxo de `upload_file`/`update_file` envia os bytes originais. Nao transforme texto
em Google Doc, nao gere base64 e nao use `textContent`. Se o conector recusar um
arquivo por tamanho ou tipo, registre o erro daquele arquivo e continue com os
demais; nao invente um limite antes da tentativa.

Suba em ordem de pasta, em lotes pequenos, e reporte o progresso. Atualize a entrada
do manifesto somente depois de cada retorno `success: true`. Uma falha nao pode
derrubar os outros arquivos.

## Passo 7 — Manifesto e relatorio

Grave `.backup-drive.json` na raiz da KB com o que subiu:

```json
{
  "pasta_destino": "1AbC...XyZ",
  "nome_destino": "BACKUP - NOME DO CLIENTE",
  "modo": "espelho",
  "ultimo_backup": "2026-08-29T19:30:00Z",
  "arquivos": {
    "calls/2026-08-27-call.md": {"id": "1Zz...", "sha": "a3f9...", "subido_em": "2026-08-29T19:30:00Z"}
  }
}
```

E o manifesto que torna a proxima rodada incremental — sem ele, todo backup re-sobe
os arquivos. Preserve entradas anteriores que nao participaram desta rodada e grave
o arquivo de forma atomica depois dos uploads bem-sucedidos. Ele fica dentro da KB,
que ja e gitignored, entao nao vaza para o repo. Ele proprio **nunca sobe** para o
Drive.

Feche com um relatorio curto: quantos arquivos subiram, quantos ja estavam atualizados, quais foram pulados e por que, e o link da pasta. Nomeie os pulados — "3 arquivos internos ficaram de fora porque o modo e Material" e informacao que o usuario precisa para confiar no backup.

## Exemplo completo

**Usuario:** "sobe tudo da KB do cliente X pra essa pasta aqui: drive.google.com/drive/folders/1AbC...XyZ — serve de backup"

**A skill:**

1. Confirma a origem (`squads/alpha/clientes/cliente-x/`, 53 arquivos) e resolve o destino: pasta `BACKUP - CLIENTE X`.
2. Checa permissoes da pasta e das duas acima. **Acha `{"role":"reader","type":"anyone"}` na pasta destino.** Para.
3. Reporta: "A pasta esta publica — qualquer um com o link le. Num backup Espelho,
   ficariam expostos `mission-control/personas-call.md`, os reviews internos e o
   contrato assinado. O `.env` continuaria bloqueado pela skill. Para fechar: botao
   direito → Compartilhar → Acesso geral → Restrito."
4. Usuario fecha e avisa. A skill **reconfirma pela API** e ve que o `anyone` sumiu.
5. Roda o script: 4 segredos, 11 internos, 38 material, 0 nao classificados.
6. Pasta restrita ao time → propoe **Espelho** (49 arquivos).
7. Cria `calls/`, `checkins/`, `docs/` (com `comercial/`, `entrevistas/`, `marca/`), `mission-control/`, `outputs/`.
8. Envia os 49 arquivos pelos caminhos locais, sem conversao e sem base64.
9. Grava o manifesto e reporta: "49 subiram, 4 ficaram de fora (`.env`, `.env.example`, `.DS_Store`, `.gitkeep`). Link: ..."

**Uma semana depois:** "atualiza o backup do cliente X". A skill le o manifesto,
compara os hashes, encontra 6 arquivos alterados e 1 novo, atualiza os 6 IDs
existentes e cria 1 arquivo. O historico de revisoes continua no Drive.

## Notas

- **Nao suba manifesto nem `.git`.** O manifesto e estado local; `.git` nao existe dentro de KB gitignored, mas se aparecer, ignore.
- **Nao siga links simbolicos.** Eles podem apontar para fora da KB e ampliar o escopo sem o usuario perceber.
- **Backup nao e sincronia.** Arquivo apagado na KB continua no Drive, de proposito — apagar por engano e o cenario que o backup existe para cobrir. Se o usuario quiser limpar, ele pede e voce mostra a lista antes.
- **Rode depois de `/contexto`.** E quando a KB acabou de mudar e o backup vale mais.
- **A trava do Passo 2 nao e formalidade.** Ela ja pegou uma pasta que estava publica sem ninguem ter decidido isso — o link foi gerado para compartilhar com um colega e o Drive abriu para a internet junto.
