---
name: geral-postar-conteudo-meta
description: Agenda posts estáticos e Reels de um lote de conteúdo social direto no Meta Business Suite (Facebook + Instagram), de verdade, via automação de browser real conectado à sessão logada do cliente. Use sempre que o usuário tiver uma pasta de vídeos/imagens + um documento de copy pra agendar/publicar no Facebook ou Instagram, mencionar "agendar posts", "postar no Meta Business Suite", "programar reels", "automatizar publicação de calendário de conteúdo", ou pedir pra você "postar" um lote de criativos aprovados. Não é a skill certa pra gerenciar campanhas de anúncios pagos (use notfair:meta-ads ou adkit pra isso) — é especificamente sobre conteúdo orgânico agendado no Planner.
area: geral
author: juan
version: 1.0.0
---

# Postar conteúdo social no Meta Business Suite

Pega um lote de conteúdo (vídeos + estáticos + doc de copy) e agenda os posts de verdade no Meta Business Suite, via Playwright conectado por CDP num Chrome real já aberto (não headless) — assim a sessão logada do cliente é reaproveitada, sem precisar automatizar login.

## Antes de começar — pergunte, não assuma

Esta skill é usada por pessoas diferentes, em máquinas diferentes, com clientes diferentes. **Nunca assuma nenhum destes pontos** — pergunte diretamente (pode usar uma pergunta de múltipla escolha ou texto livre, o importante é não adivinhar):

1. **Nome do cliente.** Curto, sem espaço/acento (ex: `ClienteExemplo`, `ClinicaXYZ`) — vai isolar o perfil de automação desse cliente dos outros, pra não misturar logins.
2. **Onde estão os arquivos de mídia** no computador da pessoa (pasta com os vídeos/imagens do lote).
3. **Qual perfil do Chrome já está logado** na conta do Meta Business Suite desse cliente. Oriente a pessoa a: abrir o Chrome normal dela (o que já usa pra entrar nesse cliente), digitar `chrome://version` na barra de endereço, e te passar o valor de **"Profile Path"** — só a última pasta do caminho (ex: `Profile 3`, `Default`).
4. **Se já existe um perfil de automação pra esse cliente** (pergunte se essa pessoa já rodou essa skill antes pra esse cliente nessa máquina). Se não existe, ela vai precisar **logar manualmente uma vez** — você nunca deve tentar logar por ela nem pedir senha/2FA. Só oriente e espere ela confirmar que logou.
5. **Regras de cronograma**: cadência (todo dia? um dia sim um dia não? datas fixas?), horário(s), se pula fim de semana, e a partir de quando começa. Depois de definidas, **valide contra o calendário real** (rode algo como `date -d <data> +%A` — nunca assuma que "amanhã" cai num dia útil sem checar).

Só depois de ter essas respostas, siga pro passo a passo.

## Passo a passo

### 1. Mapear arquivo ↔ post

Os nomes de arquivo quase nunca batem com o número/nome do post no doc de copy. **Abra cada imagem/vídeo e compare visualmente** com o headline/tema de cada post antes de montar o plano — não assuma pela ordem alfabética ou numérica do nome do arquivo. Erro aqui é o mais comum e o mais fácil de não perceber até tarde (ver item 7 de `references/gotchas-tecnicos.md`).

### 2. Limpar a legenda (se aplicável)

Se o doc de copy do usuário tiver convenções específicas (ex: label "CTA:" antes do call-to-action, travessões `–`/`—` no meio das frases), pergunte se ele quer que você limpe isso antes de postar — não aplique regras de limpeza que não foram pedidas. Um padrão comum que já apareceu: remover a label "CTA:" (o texto vira só mais uma frase no fim da legenda) e trocar travessões por vírgula/ponto/dois-pontos.

### 3. Calcular o cronograma

Com as regras confirmadas no passo "antes de começar", gere as datas concretas e valide cada uma contra o dia da semana real. Se cair em dia que deveria ser pulado (fim de semana, por exemplo), ajuste e avise o usuário do ajuste.

### 4. Gerar o plano.json

Ver `references/plano-exemplo.json` pro formato exato. Por post: número, tema, tipo (`ESTATICO`/`VIDEO`), ação no Meta Business Suite (`Criar post`/`Criar Reel`), nome do arquivo, data (`YYYY-MM-DD`), dia da semana, hora (`HH:MM`), legenda já limpa, hashtags. Salvar num arquivo acessível (ex: pasta do cliente/campanha do usuário).

### 5. Preparar o Chrome com debug remoto

**Primeira vez com esse cliente nessa máquina** (depois de já ter o nome do perfil Chrome via `chrome://version`):
```
scripts\setup_perfil_automacao.bat NOME_CLIENTE "NOME_DO_PERFIL_CHROME_JA_LOGADO"
```
Isso cria um perfil de automação isolado pra esse cliente, copiando os dados essenciais (sem cache) do perfil real, e abre o Chrome nele. **A sessão não vem logada automaticamente** (cookies não sobrevivem à cópia — ver item 2 de `references/gotchas-tecnicos.md`) — a pessoa precisa logar manualmente ali, uma vez só, e confirmar que a página/conta certa do Meta Business Suite está selecionada.

**Já configurado antes:**
```
scripts\abrir_chrome_automacao.bat NOME_CLIENTE
```
Fecha qualquer Chrome aberto e reabre o perfil de automação desse cliente, já logado, com a porta de debug ativa.

Confirmar que funcionou: `curl -s http://127.0.0.1:9222/json/version` deve devolver um JSON com a versão do Chrome. Se não responder, ver item 1 de `references/gotchas-tecnicos.md`.

### 6. Rodar o script, post por post

```
python scripts\postar_conteudo.py --plan <plano.json> --media-dir <pasta> --post <numero>
```
Sem `--confirm`: monta tudo (upload, legenda, agendamento) e **para antes de publicar**, salvando uma prévia em `preview_post<N>.png`. **Sempre mostrar essa prévia pro usuário e confirmar antes de publicar de fato** — publicar em conta real de cliente é uma ação visível externamente e difícil de desfazer, então essa confirmação não é opcional.

Depois de aprovado, rodar de novo com `--confirm` (não continua de onde parou — refaz o fluxo inteiro e desta vez clica em Programar de verdade):
```
python scripts\postar_conteudo.py --plan <plano.json> --media-dir <pasta> --post <numero> --confirm
```

Repetir pra cada post do lote. O próprio Meta mostra um popup de confirmação ("Seu post foi programado" / "Reel programado") depois de cada `--confirm` bem-sucedido — essa é a fonte da verdade, não precisa reabrir o calendário pra conferir (ver item 8 de `references/gotchas-tecnicos.md` sobre por que isso é arriscado).

## Quando algo quebrar

Ler `references/gotchas-tecnicos.md` — cobre os 9 problemas reais já encontrados (porta de debug não sobe, login não sobrevive a cópia de perfil, upload de arquivo grande, botões duplicados no Meta, etc.), cada um com sintoma, causa e a solução que já está embutida nos scripts.

## Limites conhecidos

- Não automatiza login (nunca deve pedir senha/2FA ao usuário nem tentar preencher esses campos).
- Assume Windows + Google Chrome instalado no caminho padrão (`C:\Program Files\Google\Chrome\Application\chrome.exe`).
- Um perfil de automação por cliente evita conflito de sessão entre clientes diferentes, mas ainda depende da pessoa ter, ela mesma, acesso de login à conta do Meta Business Suite daquele cliente.
