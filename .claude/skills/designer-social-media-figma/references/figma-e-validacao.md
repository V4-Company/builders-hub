# Figma: Montagem, Recuperacao e Revisao

## Destino e Primeira Escrita

Use o link mais recente, extraia a chave e descubra as paginas. Distinga equipe, projeto, arquivo, pagina, secao e grupo por data.

Se a integracao oferecer sessao de arquivo, abra uma para a tarefa e reuse o identificador. Consulte as instrucoes atuais de escrita: ferramentas e APIs podem mudar entre ambientes.

Inspecione antes de criar. Em atualizacoes, leia o grupo e seus ajustes manuais; nao recriar o carrossel inteiro para uma mudanca localizada.

Crie secao e grupos somente se ausentes e posicione-os em area livre. Use placeholders temporarios para trabalho em andamento e retire-os ao concluir.

Registre IDs criados/alterados. Numa retomada, confira IDs ou hierarquia antes de repetir a criacao; uma chamada interrompida pode ter escrito parte do conteudo. Se ainda houver incerteza, leia o canvas.

Quatro carrosseis no mes nao significam quatro cards em cada um. A contagem vem do briefing. Nomeie a secao como pedido, os grupos por data e os frames por numero.

## Composicao

- Separe imagem, headline, corpo, destaque, anotacao, logo e CTA em camadas.
- Descubra e carregue familia e pesos exatos; confira o que foi efetivamente aplicado.
- Use auto-layout ou fluxo equivalente para textos relacionados. Mantenha artboards e areas de imagem com tamanho estavel.
- Meca o fim real do texto antes de posicionar foto, nota e rodape. Nao presumir altura fixa para uma copy que pode quebrar linhas.
- Ajuste proporcoes ao conteudo; fotos pequenas e vazios excessivos podem enfraquecer a composicao.
- Use setas vetoriais ou assets adequados, com traco manual quando houver esse padrao. Nao usar glifo que vira emoji ou quadrado.
- Garanta contraste onde o texto aparece. Use base solida, tratamento localizado ou outro layout quando a foto nao permitir leitura.

Capas precisam de foco, imagem marcante e headline com hierarquia. Estaticos exigem o mesmo cuidado de peca principal: foto grande ou imagem de estudio quando briefing e referencias pedirem isso. Nao aplicar automaticamente o modelo de texto e foto pequena do miolo.

Escolha foto em bloco ou ao fundo conforme cena, copy e referencias. Uma comparacao factual pode usar fotos oficiais e rotulos editaveis em vez de uma fotografia generica.

Reaproveite encerramentos aprovados. Quando so houver versao raster, ela pode ser o asset completo daquele card. Identifique essa excecao e mantenha os novos cards em camadas editaveis.

## Upload

Se houver upload direcionado a nos, crie os alvos e preserve a ordem entre arquivo, URL e ID. Consuma cada URL conforme a ferramenta. Nao guardar URLs temporarias como se fossem assets finais.

Confira tamanho e MIME. Use `FIT` ou equivalente para logos e produtos inteiros; recorte fotos para preencher areas, conferindo rostos, maos, objeto e acao no resultado.

Quando a integracao permitir, reuse o hash de imagem dentro do arquivo para logo e encerramento, evitando uploads repetidos. Confirme o fill de cada alvo antes de concluir.

## Revisao Estrutural

Registre evidencias de:

- Secao, datas e IDs dos frames.
- Quantidade igual ao manifesto, ordem e nomes numerados.
- Dimensoes corretas e ausencia de duplicatas.
- Copy nova editavel e fontes corretas.
- Imagens preenchidas e placeholders removidos.
- Texto dentro dos limites e sem colisao com imagem ou rodape.

Limites geometricos detectam overflow, mas nao garantem composicao. Destaques e setas podem ter intersecoes intencionais; examine antes de classificar como erro.

## Revisao Visual

Renderize os carrosseis completos em resolucao que permita ler o miolo e abra cada imagem. Resposta contendo apenas ID, URL ou metadados nao prova que a imagem foi visualizada.

Se `node.screenshot()` nao devolver imagem visivel ao agente, use screenshot/exportacao, baixe a URL temporaria e abra o arquivo. Nao afirmar QA visual sem ver o resultado.

Confira cena principal, copy, acentos, numeros, CTAs, hierarquia, leitura, enquadramento, contraste, distribuicao e consistencia da marca. Corrija localmente e renderize os posts afetados novamente. Quando passar e nada mais mudar, encerre a verificacao; nao repetir screenshots identicos.

## Recuperacao Pela Causa

| Falha | Acao |
| --- | --- |
| Adobe falha sem imagem | Registrar e usar o fallback OpenAI |
| Figma somente leitura | Informar bloqueio real e resolver escrita para a etapa dependente |
| HTTP 413 | Preparar copia menor e obter nova URL quando necessario |
| Arquivo Drive indisponivel | Tentar hidratacao/leitura limitada ou conector autorizado |
| Fonte/peso indisponivel | Conferir familia e estilos; resolver acesso ou perguntar por alternativa |
| Erro de script | Usar sinal de retry seguro; ler a arvore se houver incerteza sobre a escrita |
| Imagem nao aparece | Conferir transferencia, alvo e fill; nao regenerar por erro de upload |
| Pedido somente de analise | Executar leituras e nao corrigir o arquivo |

Nao repetir a mesma operacao indefinidamente sem resolver a causa. Se permanecer bloqueado, informe estado real, assets prontos e dependencia especifica; continue as partes independentes.
