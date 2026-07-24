# Gotchas técnicos (por que o script é do jeito que é)

Ler isto quando algo der errado no meio da automação — cada item explica o sintoma, a causa real e a solução já embutida no script/scripts `.bat`.

## 1. Porta de debug do Chrome não sobe

**Sintoma:** `curl http://127.0.0.1:9222/json/version` não responde (conexão recusada), mesmo com o Chrome aberto e `--remote-debugging-port=9222` na linha de comando do processo.

**Causa:** Chrome moderno (a partir de ~v136) **ignora silenciosamente** `--remote-debugging-port` quando o `--user-data-dir` resolvido é o diretório "de verdade" (o `User Data` default da instalação) — proteção contra apps maliciosos anexarem debugger no navegador real do usuário. Só funciona se o `--user-data-dir` apontar pra um diretório **diferente** do default.

**Solução:** os scripts `setup_perfil_automacao.bat`/`abrir_chrome_automacao.bat` sempre usam `--user-data-dir=...\ChromeAutomationProfile_<Cliente>` (nunca o default), então isso já vem resolvido — só usar os scripts, não abrir o Chrome manualmente sem essa flag.

## 2. Perfil de automação abre sem login (mesmo tendo copiado o perfil real)

**Sintoma:** copiou a pasta do perfil real pro perfil de automação, mas a sessão do Facebook/Instagram não veio junto — cai na tela de login.

**Causa:** o Chrome criptografa cookies de um jeito vinculado ao caminho/instalação específica ("app-bound encryption"). Uma cópia crua da pasta de perfil não decripta certo no caminho novo.

**Solução:** não tem workaround de cópia — **é preciso logar manualmente, uma vez só**, dentro do próprio perfil de automação (depois que ele já existe, com a porta de debug ativa). Depois disso a sessão fica salva ali normalmente, como qualquer perfil comum do Chrome, sem precisar mexer em cookies de novo.

## 3. PowerShell corta o comando de abrir o Chrome em pedaços errados

**Sintoma:** ao montar o comando de `Start-Process -ArgumentList` manualmente (fora dos `.bat` prontos), argumentos com espaço (`"User Data"`, `"Profile 10"`) ficam truncados, e o Chrome abre um perfil em branco.

**Causa:** `Start-Process -ArgumentList` não coloca aspas automaticamente em cada elemento da lista — se o valor tem espaço e você não escapou as aspas manualmente dentro da string, o PowerShell quebra no espaço.

**Solução:** usar os `.bat` prontos (que já lidam com isso via `cmd.exe`/`start`), em vez de montar o comando via PowerShell na mão.

## 4. Upload de vídeo grande trava ou dá erro "Cannot transfer files larger than 50Mb"

**Sintoma:** `file_chooser.set_files(caminho)` ou `locator.set_input_files(caminho)` falha com esse erro exato pra vídeos grandes (a maioria passa de 50MB facilmente).

**Causa:** Playwright, quando conectado via `connect_over_cdp` (em vez de ter lançado o navegador ele mesmo), trata a conexão como "não colocalizada" e tenta transferir o conteúdo do arquivo inteiro em base64 pelo protocolo — o que tem um teto de 50MB.

**Solução:** o script usa CDP puro pra contornar isso (`upload_media_raw_cdp()`): registra um listener no evento `Page.fileChooserOpened` (que devolve um `backendNodeId` direto, sem precisar ler o arquivo), e chama `DOM.setFileInputFiles` com esse id — isso manda o próprio Chrome ler o arquivo do disco local, sem limite de tamanho. Funciona pra qualquer tamanho de arquivo, então o script usa esse caminho sempre (até pra imagens pequenas), evitando dois caminhos de código diferentes.

## 5. Botões "Avançar"/"Programar" clicam no elemento errado (setinha de carrossel)

**Sintoma:** clicar no botão "Avançar" (ou "Programar") não avança o wizard do Reel — em vez disso, só troca as miniaturas sugeridas de capa.

**Causa:** o Meta Business Suite tem **dois elementos com o mesmo texto acessível** na tela ao mesmo tempo: o botão real do rodapé, e a setinha de "próxima página" do carrossel de miniaturas sugeridas (que por acaso também se chama "Avançar"/"Programar" pra leitor de tela). `get_by_role("button", name="Avançar")` encontra os dois.

**Solução:** a função `click_widest()` sempre pega o elemento **mais largo** entre os que casam o texto — o botão real do rodapé é bem maior que a setinha do carrossel.

## 6. Botão "Próximo mês" do calendário não é encontrado por nenhum seletor "normal"

**Sintoma:** `locator("[aria-label='Próximo mês']")` ou `locator("button", has_text=...)` não encontram nada, mesmo com a seta "›" visível na tela ao lado do nome do mês.

**Causa:** o texto "Próximo mês" existe no DOM como texto puro dentro de uma `<div>` sem `role="button"` nem `aria-label` — é um padrão de acessibilidade "screen-reader-only" (texto sem tamanho visual, sobreposto à seta visual de verdade). Um clique por coordenada de tela funciona (a seta está lá visualmente), mas selecionar por atributo não acha o elemento certo.

**Solução:** `composer.get_by_text("Próximo mês", exact=True).click(force=True)` — `force=True` ignora o check de visibilidade do Playwright (que bloquearia o clique num elemento de tamanho zero) e ainda assim dispara o evento de clique real no elemento certo.

## 7. Mapeamento arquivo ↔ post errado (imagem/vídeo publicado não bate com a legenda)

**Sintoma:** o preview no Meta mostra uma imagem/vídeo diferente do que o número do post sugeria.

**Causa:** os nomes dos arquivos de mídia quase nunca batem com a numeração dos posts no doc de copy (ex: `post 15.png` pode ser na verdade o conteúdo do "POST 12" do doc). Isso não é um bug do script — é erro de leitura humana/IA ao montar o `plano.json`.

**Solução:** sempre abrir cada imagem/vídeo e comparar visualmente com o headline/tema de cada POST no doc **antes** de gerar o plano, e sempre rodar o script primeiro **sem `--confirm`** pra conferir o preview antes de publicar de fato.

## 8. Clicar numa célula vazia do calendário do Planner abre um rascunho novo

**Sintoma:** ao tentar conferir visualmente se os posts foram agendados clicando no calendário, abre um "Criar post" em branco, pré-preenchido com a data/hora daquele espaço.

**Causa:** é uma feature de "criação rápida" do próprio Meta Business Suite — clicar em espaço vazio de um dia/hora cria um rascunho novo naquele horário.

**Solução:** não usar cliques no calendário como forma de auditar se os posts foram agendados — a fonte da verdade é o popup de confirmação que o próprio Meta mostra depois de "Programar" ("Seu post foi programado" / "Reel programado"). Se abrir um rascunho em branco sem querer: fechar pelo **X do modal** (não o botão "Cancelar" de trás, que fica coberto/bloqueado pelo modal), depois "Cancelar" no composer.

## 9. Acentos saem corrompidos no terminal do Windows

**Sintoma:** `print()` com texto acentuado (ex: "não", "mês") solta `UnicodeEncodeError` ou imprime `?`/`�` no console.

**Causa:** o console do Windows por padrão usa a codepage `cp1252`, que não cobre todos os caracteres UTF-8.

**Solução:** rodar o script com `PYTHONIOENCODING=utf-8` na frente do comando quando for inspecionar saída de texto acentuado, ou simplesmente confiar nos screenshots (`preview_post<N>.png`) em vez do texto impresso no terminal pra conferir conteúdo.
