---
name: designer-social-media-figma
description: Produz ou atualiza carrosseis e posts estaticos no Figma a partir de briefings mensais do Miro e referencias reais da marca no Drive. Use para executar um social media mensal em lote, incluindo imagens, layouts editaveis e revisao visual, ou para alterar datas especificas de um lote existente.
area: designer
author: lewenzo
version: 1.0.0
---

# Social Media: Miro, Imagens e Figma

Entregue os posts solicitados no Figma escolhido pelo usuario, com conteudo fiel ao Miro e identidade extraida dos materiais daquele cliente. O caso principal e um mes com quatro carrosseis; as quantidades de posts e cards devem vir do escopo e do briefing, nao de um template fixo.

## Dependencias

Descubra as capacidades reais antes de prometer acesso:

- Miro: leitura dos frames mensais e briefings por data.
- Drive ou sistema de arquivos: leitura dos materiais autorizados.
- Figma: leitura, escrita no arquivo existente, upload e renderizacao.
- OpenAI: geracao das capas e estaticos por ferramenta ou integracao autorizada.
- Adobe/Firefly: preferencia para imagens internas, com fallback OpenAI.

No Claude, nao presuma que a assinatura ou o conector Figma inclui geracao OpenAI, Firefly ou escrita no canvas. Consulte as instrucoes atuais das integracoes antes de executar scripts. Esta skill nao substitui sua documentacao nem amplia permissoes.

Publicar posts, criar links publicos, compartilhar arquivos, instalar integracoes ou adotar uma nova API paga precisa fazer parte do escopo. Nao publicar nem abrir PR automaticamente.

## 1. Recuperar Contexto e Coletar o Essencial

Reaproveite dados ja fornecidos. Use o formulario de [entrada e marca](references/entrada-e-marca.md) para perguntar, em uma mensagem, somente o que falta. Fontes, cores, logos, pagina e datas podem ser descobertas nos materiais.

Identifique cliente, mes/ano, Miro, datas, pasta, arquivo/pagina Figma e referencias. Distinga os modos:

- **Criar lote:** produzir os posts do mes autorizado.
- **Atualizar:** reler o Miro e alterar apenas as datas informadas, preservando ajustes manuais.
- **Analisar:** ler e apresentar conclusoes, sem escrever no Figma.

Leia os posts do lote em conjunto. Nao transformar quatro carrosseis em quatro entrevistas. Na ausencia de outra orientacao, crie os novos posts do periodo; se ja houver grupos equivalentes, inspecione-os antes de decidir o que atualizar.

## 2. Ler as Fontes de Verdade

1. Localize o frame do mes no Miro e as datas dentro dele.
2. Extraia copy, enfases, direcoes visuais, notas, CTAs, legendas e numero de cards.
3. Abra o manual e inspecione visualmente criativos recentes: capas, miolos, estaticos e encerramentos.
4. Inspecione logos, produtos, fotos e prints reais disponiveis.
5. Descubra as paginas e a estrutura do Figma usando o link mais recente.

Restrinja as fontes do cliente as pastas de criacao e de materiais compartilhados, normalmente identificadas pelos prefixos 7 e 8, usando os nomes exatos encontrados no caminho fornecido. Nao alterar, mover ou excluir os originais. Outra pasta precisa estar autorizada.

Instrucoes atuais do usuario prevalecem sobre manual antigo. Resolva divergencias sem prioridade clara. Nao inventar dados, claims, cards, precos, depoimentos, logos ou prints.

## 3. Consolidar Manifesto e Direcao Visual

Registre a origem e o estado de cada post/card segundo [manifesto e retomada](references/manifesto-e-retomada.md). Separe copy original de copy aplicada e registre correcoes.

Apresente uma sintese do lote e do padrao observado. Isso e uma atualizacao de andamento, nao uma aprovacao obrigatoria: prossiga quando o escopo estiver autorizado e claro. Aguarde apenas para ambiguidades que impedem a execucao, mudanca substancial de copy ou acao fora do escopo. Continue os posts independentes enquanto resolve uma duvida localizada.

Planeje hierarquia, espaco de texto, formato da imagem, provedor e materiais de cada card. Nao transferir fontes, cores ou encerramento de outro cliente.

## 4. Confirmar Escrita Antes de Gerar o Lote

Conclua a primeira escrita necessaria no destino autorizado antes de gerar um lote caro: secao e grupos dos posts, ou a primeira alteracao real do grupo existente. Retenha os IDs retornados.

Se o acesso for somente leitura, informe a mensagem real do bloqueio de escrita. Nao pedir reconexao para um problema de upload, rede ou fonte. Nao gerar o lote inteiro esperando uma ponte que ainda nao funciona, salvo pedido de imagens independentemente do Figma.

## 5. Produzir e Validar Imagens

Leia [prompts e imagens](references/prompts-e-imagens.md).

- Capas: briefing original, prompt enriquecido, OpenAI e inspecao visual.
- Estaticos unicos: tratamento de peca principal, com impacto de capa.
- Miolo: Adobe/Firefly; OpenAI para cena complexa ou falha do Adobe.
- Produtos, logos, prints e encerramentos especificos: priorizar arquivos oficiais.

A troca de provedor preserva o briefing e a marca. Se OpenAI nao estiver disponivel, resolva o acesso ou a alternativa com o usuario. Nao atribuir resultado a um provedor sem chamada bem-sucedida.

Inspecione cada resultado antes do upload: acao, anatomia, produto, artefatos, enquadramento e espaco para texto. Corrija ou regenere falhas preservando a cena solicitada. Salve selecoes, prompts e origens no diretorio de trabalho do cliente.

## 6. Montar no Figma

Leia [Figma e validacao](references/figma-e-validacao.md). Preserve arquivo e pagina escolhidos; nao criar um arquivo paralelo por conveniencia.

```text
Pagina SOCIAL ou SOCIAL MEDIA
  Secao Social [Mes]
    Grupo 04.11
      Card/frame 1
      Card/frame 2
      Card/frame 3
      Card/frame 4
    Grupo 11.11
      ...
```

As datas e quatro cards sao ilustrativos. A secao segue o nome pedido, o grupo identifica a data e cada frame recebe seu numero. Use dimensoes solicitadas ou presentes nas referencias, normalmente 1080 x 1350 para feed.

Mantenha textos e composicao novos editaveis. Um encerramento aprovado que so exista como imagem pode ser reutilizado integralmente; informe essa limitacao. Nao redesenhar a identidade da pessoa, o perfil ou o CTA, nem achatar os novos cards.

Use fontes exatas, pesos disponiveis, logos oficiais e cores da marca. Organize textos relacionados com auto-layout ou mecanismo equivalente. Decida o miolo pela quantidade de informacao e pela imagem; texto sobre fotografia exige contraste adequado.

## 7. Fazer o Pente Fino

1. Confira datas, contagem, ordem, nomes e dimensoes.
2. Compare a copy aplicada com manifesto e Miro.
3. Leia as fontes realmente aplicadas e confirme as imagens no canvas.
4. Renderize cada carrossel completo e cada estatico; abra as imagens e examine-as.
5. Corrija sobreposicoes, cortes, contraste, letras pequenas, imagens fracas e distribuicao.
6. Renderize novamente o que mudou. A ultima revisao deve corresponder ao estado entregue.

Metadados nao substituem inspecao visual. Geracao concluida nao prova insercao no Figma. Confira sucesso do upload, ID alvo e fill antes de marcar imagem como aplicada.

Nao aumentar ou reescrever copy para preencher vazio. Ajuste tipografia, espacamento, enquadramento e proporcao das imagens conforme a marca. Nao finalizar com placeholders ou imagens ausentes sem declarar a pendencia.

## 8. Entregar e Registrar

Entregue resposta curta com link da secao, pagina, datas, quantidade, provedores usados, verificacoes e pendencias reais. Informe o diretorio dos arquivos e previas.

No Builders Hub, guarde materiais de cliente fora do repo em `G:\Meu Drive\ARQUIVOS CLIENTES\{cliente}\{AAAA-MM}\`, separados por tipo. A KB, quando existir, fica em `squads/{squad}/clientes/{cliente}/`; nao criar cliente fora de squad nem inserir dados privados nesta skill.

Use o feedback para ajustar a regra correspondente. Separe preferencia de um cliente de melhoria geral. Nao alterar criativos aprovados de outros posts para aplicar uma melhoria.

## Exemplo

**Entrada:** "Faca os quatro carrosseis de novembro da Marca Exemplo. Seguem Miro, pasta e Figma. Headlines em Fonte A e textos em Fonte B."

**Execucao:** descobrir lacunas nas referencias; ler os quatro briefings e a identidade; resumir o lote; criar estrutura; gerar e revisar imagens; montar; conferir copy e renderizacoes; corrigir e entregar.

**Saida:** secao mensal com quatro grupos por data, contagens iguais ao briefing, identidade correta, imagens aplicadas e previas revisadas. Adobe falhando aciona OpenAI sem mudar a cena; duvida de copy bloqueia somente o post afetado.

## Avaliacao

Os cenarios de [evals/evals.json](evals/evals.json) verificam lote, atualizacao e recuperacao sem acessar cliente real. Simulacoes e validacao de arquivos nao substituem um novo teste visual em outra conversa. Nao gerar imagens pagas nem alterar arquivos reais apenas para executar esses cenarios.
