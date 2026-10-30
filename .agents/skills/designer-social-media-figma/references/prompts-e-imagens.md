# Prompts, Provedores e Materiais

## Escolha

| Peca | Preferencia | Recuperacao |
| --- | --- | --- |
| Capa | OpenAI | Resolver acesso ou combinar alternativa, sem troca silenciosa |
| Estatico unico | OpenAI | Mesmo cuidado de imagem e impacto da capa |
| Imagem interna | Adobe/Firefly | OpenAI para falha ou cena complexa |
| Logo, print, produto e encerramento | Material oficial | Localizar o original ou solicitar o material |
| Grafico ou comparacao factual | Dados reais e camadas editaveis | Resolver dados ausentes, sem inventar medidas |

O fallback Adobe para OpenAI faz parte do fluxo. Informe a troca no andamento e no resultado; nao pedir novamente quando essa preferencia ja estiver adotada. Confira as capacidades e permissoes reais do ambiente.

Nao gerar imagens pelo Figma AI por conveniencia quando a preferencia for OpenAI/Adobe. Use Figma para montar o criativo e receber os assets externos.

## Enriquecer o Prompt

Extraia os elementos obrigatorios: personagem, acao, objeto, ambiente, expressao, produto e enquadramento pedido. Eles permanecem no prompt enriquecido.

Melhore somente o tratamento visual e a utilidade para o layout:

- Linguagem editorial ou de produto conforme as referencias do cliente.
- Composicao dinamica, profundidade e hierarquia clara.
- Iluminacao coerente, reflexos e sombras de contato.
- Texturas de pele, tecido e materiais com imperfeicoes naturais.
- Espaco para headline calculado pela quantidade de texto.
- Margem para o recorte final, sem cortar a acao principal.

Nao impor fundo azul, pouca luz, percentual fixo de espaco negativo ou estetica identica a todas as marcas. Uma imagem de estudio pode ser mais adequada que uma cena com pessoas.

```text
Peca e uso: [capa, apoio ou estatico; proporcao e area visivel].
Cena obrigatoria: [personagem, acao, objeto, ambiente e expressao].
Referencia oficial: [arquivo e caracteristica a preservar, quando houver].
Composicao: [hierarquia, angulo, plano, recorte e area para headline].
Tratamento: [identidade, luz, texturas e nivel de realismo].
Restricoes: [sem texto inventado, logo falso, deformacao ou elementos extras].
```

Escreva um prompt por imagem e preserve versoes. Execute chamadas independentes em paralelo quando a ferramenta permitir.

Em uma tela ou embalagem, nao invente informacao comercial legivel. Use o print/produto oficial quando o conteudo for essencial; se necessario, insira o asset real na montagem. Uma tela abstrata nao equivale ao software real e uma embalagem sem marca nao equivale ao produto oficial.

Headlines, corpo e CTAs entram como texto editavel no Figma. Um detalhe fisico legivel pode ser aceito quando exigido pela cena e correto, mas nao deve substituir informacao essencial editavel.

## Inspecao

Abra cada resultado e confira:

1. Acao e expressao fieis ao briefing.
2. Produto correto e caracteristicas coerentes.
3. Maos, rostos, objetos e embalagens inteiros e sem duplicacao.
4. Foco, recorte e espaco para headline.
5. Ausencia de marcas falsas, letras inventadas e artefatos.
6. Tratamento compativel com as referencias, sem aparencia generica.

Corrija ou regenere falhas preservando a cena. Se houver erros repetidos, simplifique somente a composicao; nao abandone o personagem, a acao ou o produto solicitados.

## Arquivos e Upload

Salve a selecao final fora do repo, junto ao manifesto. Preserve originais e crie uma copia de upload ao reduzir tamanho/resolucao. Mantenha transparencia de logos e recortes.

Confira o limite atual da integracao. O limite observado neste fluxo Figma foi 10 MB por asset; HTTP 413 pede uma copia menor, nao reconexao nem uma imagem diferente.

Verifique sucesso, ID alvo e fill antes de marcar a imagem como aplicada. Geracao, arquivo local, upload e imagem no canvas sao estados diferentes.
