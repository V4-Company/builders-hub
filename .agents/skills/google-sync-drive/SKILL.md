---
name: google-sync-drive
description: Sincroniza uma pasta do Google Drive com a KB de um cliente, trazendo apenas o que é novo ou mudou desde a última execução. Converte Google Docs, Sheets e Slides em markdown, coloca cada arquivo no lugar certo da KB e mantém um estado em JSON para que a próxima rodada seja incremental. Use quando o usuário rodar /google-sync-drive, disser que quer atualizar a KB com o que veio do Drive, que o cliente mandou arquivo novo no Drive, ou perguntar se tem coisa nova lá.
area: google
author: luizricardo
version: 1.0.0
---

# Google Drive: sync incremental para a KB

Traz do Drive só o que mudou, converte para markdown e organiza na KB. Não é sync de disco: roda quando você chama.

## Pré-requisitos

O conector do Google Drive precisa estar autenticado. Se as ferramentas `mcp__claude_ai_Google_Drive__*` não aparecerem, o usuário precisa conectar em claude.ai, em Settings e Connectors.

O cliente precisa ter `docs/mapa-drive.md` com o ID da pasta raiz. Se não tiver, este é o primeiro sync: rode o Passo 1 e crie o mapa.

## Passo 1: descobrir o escopo

Leia `docs/mapa-drive.md` do cliente e pegue o ID da pasta raiz.

Se o arquivo não existir, peça o link da pasta ao usuário, extraia o ID de `/folders/{ID}`, e confirme com `get_file_metadata` antes de seguir.

Percorra a árvore com `search_files` usando `parentId = '{ID}'`. Repita para cada subpasta encontrada, até não sobrar pasta. Junte tudo numa lista com id, título, mimeType, modifiedTime e o caminho da pasta.

Não use `fullText contains` para descobrir arquivo: a busca por parentId é exata e não traz lixo de outras pastas.

## Passo 2: comparar com o estado anterior

Leia `docs/.drive-sync.json`. O formato é:

```json
{
  "raiz": "ID_DA_PASTA",
  "ultimaSync": "2026-07-30T20:00:00Z",
  "arquivos": {
    "FILE_ID": {
      "titulo": "...",
      "modifiedTime": "2026-07-24T13:37:29Z",
      "destino": "campanhas/lps-operacao/copy-lp-....md",
      "acao": "importado"
    }
  }
}
```

Classifique cada arquivo do Drive:

- **Novo**: o id não está no estado.
- **Mudou**: o id está, mas o `modifiedTime` do Drive é maior que o guardado.
- **Igual**: nada a fazer, não toque no arquivo da KB.
- **Sumiu**: está no estado e não veio na varredura. Não apague nada da KB. Marque como `"acao": "removido no drive"` e avise o usuário.

Se o estado não existir, trate tudo como novo, mas antes verifique duplicata (Passo 3).

## Passo 3: não importar duplicata

Antes de importar qualquer coisa, confira se o conteúdo já existe na KB com outro nome. Dois testes baratos:

- Tamanho em bytes igual a algum arquivo já existente em `calls/` ou `docs/`.
- Título muito parecido com arquivo existente.

Já aconteceu de o transcript do kickoff estar no Drive como `.txt` e na KB como `.md`, com exatamente o mesmo tamanho. Importar de novo teria criado uma segunda cópia divergente.

Quando encontrar duplicata, registre no estado com `"acao": "duplicata"` e o caminho do arquivo que já existe.

## Passo 4: importar

Para Google Docs, Sheets e Slides use `read_file_content` com `includeComments: true`. Os comentários costumam conter as decisões de revisão e são a parte mais valiosa. Coloque-os numa seção própria no topo do markdown, com autor e data.

Para PDF, .docx e .xlsx use `read_file_content` também.

Para imagem e outros binários use `download_file_content`. Faça isso apenas quando o usuário pedir explicitamente: arquivo grande em base64 é lento e caro. O padrão é pular binário e listar o que ficou de fora.

Onde colocar cada coisa, seguindo a convenção da KB:

| Tipo de material | Destino |
|---|---|
| Copy de landing page, anúncio, roteiro | `campanhas/{campanha}/` |
| Transcript de reunião | `calls/` |
| Documento de estratégia, pesquisa, briefing | `docs/` |
| Identidade visual, key visual, paleta | `docs/identidade-visual/` |
| Imagem de campanha | `campanhas/{campanha}/assets/` |

Se não houver campanha óbvia, pergunte em vez de inventar pasta.

No cabeçalho de cada arquivo importado, registre origem, id do arquivo no Drive, data de modificação lá e data de importação. Sem isso ninguém sabe se o que está na KB é a versão atual.

## Passo 5: atualizar estado e mapa

Reescreva `docs/.drive-sync.json` com o estado novo. Atualize a tabela de inventário em `docs/mapa-drive.md`.

## Passo 6: relatório

Diga em texto corrido, sem enfeite:

- Quantos arquivos novos entraram e onde.
- Quais mudaram e o que mudou de fato, não só que mudou.
- O que foi pulado e por quê: duplicata, binário, formato não suportado.
- O que sumiu do Drive.

Se nada mudou, diga isso em uma linha e pare.

## Regras

- Nunca sobrescreva arquivo da KB que foi editado à mão depois da última sync. Compare a data de modificação local com a `ultimaSync`. Se for mais nova, pare e pergunte.
- Nunca apague arquivo da KB porque sumiu do Drive.
- Não invente conteúdo para arquivo que não conseguiu ler. Registre como falha.
- Converta travessão em vírgula, dois-pontos ou parênteses no material importado. É padrão da casa e vale inclusive quando o original do cliente usa travessão.
- Português brasileiro.
- Pasta compartilhada aparece em "Compartilhados comigo" e funciona normalmente por parentId. Não é preciso mover nada.

## Limite conhecido

Isto não é sync automático. O Drive não notifica este ambiente quando um arquivo muda, então nada acontece até alguém rodar o comando. Se o usuário quiser de fato automático, o caminho é o Google Drive para Desktop, que sincroniza a pasta no disco em tempo real, e aí esta skill passa a servir só para normalizar o que chegou.
