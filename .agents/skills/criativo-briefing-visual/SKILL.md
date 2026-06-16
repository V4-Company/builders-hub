---
name: criativo-briefing-visual
description: Gera um briefing visual detalhado para criacao de posts, incluindo links de referencias reais do Behance/Pinterest, sugestao de fotos e direcao de arte baseada no contexto do cliente. Use quando o usuario pedir "referencias visuais", "ideias de design", ou "briefing para o post X".
area: criativo
author: v4er
version: 1.0.0
---

# Briefing Visual e Pesquisa de Referências

Essa skill automatiza a pesquisa de inspiração estética e a montagem de briefings de design, garantindo que o designer não precise gastar horas no Pinterest/Behance e já saiba exatamente qual estilo seguir.

## Quando utilizar
Utilize essa skill sempre que o usuário:
- Pedir referências para um post específico.
- Estiver com bloqueio criativo sobre o layout de um criativo.
- Quiser saber como adaptar a identidade de um cliente a uma tendência visual nova.

## Fluxo de Execução

1. **Entenda o Contexto**: Leia o arquivo `CLAUDE.md` do cliente para entender o segmento, as cores institucionais e o tom de voz (Ex: premium, popular, humanizado).
2. **Defina o Tema**: Identifique qual o título ou tema do post que será criado.
3. **Pesquisa Ativa (Mining)**:
   - Use ferramentas de busca ou navegação (como `search_web` ou `browser_subagent`) para pesquisar no Behance e Pinterest.
   - Buscas recomendadas: `[segmento] social media design`, `[estilo] visual identity posts`, `modern [niche] graphic design`.
   - Foque em encontrar **referências reais** (feitas por designers humanos) que passem a autoridade necessária.
4. **Sintetize o Briefing**:
   Entregue ao usuário um relatório estruturado contendo:
   - **🔗 Link da Referência Principal**: O melhor projeto encontrado no Behance/Pinterest.
   - **🎨 Direção de Arte**: Como adaptar as cores e fontes do cliente àquele layout.
   - **📸 Sugestão de Imagem**: Qual tipo de fotografia (estoque, obra, humanizada) deve ser usada e qual a iluminação ideal.
   - **📐 Elementos Gráficos**: Uso de shapes, bordas, glassmorphism ou sombras sugeridos.

## Exemplo de Output
> **Tema:** 3 Sinais de que é hora de sair do MEI
> **Referência:** [Link do Behance]
> **Estilo:** Minimalismo Corporativo com tipografia Bold.
> **Direção:** Use o fundo Cinza Chumbo do cliente. No lugar dos elementos amarelos da referência, utilize o **Vermelho Institucional**. Use a fonte Montserrat Extra Bold para o H1.
> **Imagem:** Foto de um empresário focado em preto e branco com alto contraste.
