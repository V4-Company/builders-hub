---
name: account-retrospectiva-consolidacao
description: Consolida todos os módulos em uma retrospectiva trimestral única, auditável e pronta para aprovação, preservando rankings, funis, gaps, limitações e evidências. Use no fim da retrospectiva para montar o pacote de validação humana única, processar as respostas e liberar o adaptador do ROPRE.
area: account
author: junioraiellogestaodetrafego-maker
version: 2.0.0
---

# Consolidação da retrospectiva

Leia todos os Markdown da mesma `run_id`, `references/profundidade-entrega.md` e `references/janelas-temporais.md` do maestro. Leia também `references/modo-autonomo.md`. Valide a estrutura durante a execução com `account-retrospectiva-performance-maestro/scripts/validate_retrospectiva.py`.

## Saída

- `11-retrospectiva-final.md`
- `decisoes.md` finalizado como pacote de validação

## Ordem narrativa

1. Escopo, quarter e cobertura.
2. Janelas temporais: pré-operacional, go-live, `analysis_start`, performance e snapshots.
3. Resumo executivo.
4. Projetado versus realizado em janela compatível.
5. Visão geral e canais competindo.
6. Mídia macro até micro.
   - matriz de cobertura;
   - canais e destinos;
   - tabela-mãe de campanhas;
   - tabela-mãe de conjuntos;
   - tabela-mãe de anúncios e criativos;
   - públicos, keywords e breakdowns;
7. Criativos.
8. Funil de inside sales ou e-commerce.
9. Vendedores e atendimento, quando aplicável.
   - execução operacional;
   - competência comercial, versão e status da rubrica;
   - resultado de funil, em bloco separado;
10. Break-even e eficiência econômica.
11. Achados e gaps.
12. Limitações, conflitos, testes e não atribuídos.
13. Decisões assumidas e lacunas, com link para `decisoes.md`.
14. Índice de evidências.

## Política de consolidação

Consolide por integração, não por redução. O resumo executivo abre a leitura, mas o mesmo pacote preserva:

- análise detalhada de todos os módulos;
- tabelas-mãe e rankings integrais;
- todas as entidades, inclusive intermediárias, perdedoras e de zero resultado;
- bases linha a linha;
- conflitos, hipóteses, limitações e evidências.

Não gere um “resumo dos resumos”. Não use top N como substituto. Se houver muitas linhas, divida a base em partes e crie índice. O `11-retrospectiva-final.md` deve conter `## Janelas temporais da retrospectiva`, `## Análise detalhada` e `## Índice de insumos completos`, com links para todos os módulos, bases e assets aplicáveis e contagem de entidades por base.

## Pacote de validação humana

1. Rode `validate_retrospectiva.py <run_dir> --review-ready`. Corrija sozinho as falhas estruturais até passar; falta de dado não se corrige, vira lacuna.
2. Se ainda houver decisões `assumida` ou lacunas `aberta`, apresente a versão como `PRELIMINAR — AGUARDANDO VALIDAÇÃO` e entregue o pacote descrito em `modo-autonomo.md`: status por módulo, achados centrais, decisões críticas e altas uma por linha, contagem das demais, amostra de calibração e links.
3. Processe as respostas: confirmações e aceites atualizam só status e resposta humana; correções e dados novos geram nova `run_id` com `parent_run_id` e recálculo pelo mapa de recálculo. Agrupe as correções da rodada e recalcule uma única vez.
4. Incorpore complementos de texto como `[complemento humano]`.
5. Rode `--approval-ready`. Só quando passar, peça o comando exato `retrospectiva aprovada`. Se o comando chegar antes, responda com os IDs que ainda bloqueiam.
6. Com a aprovação registrada, libere o adaptador `account-ropre-quarter-retrospectiva` sem nova pergunta. Não gere handoff de Drive sem pedido e autorização de escrita.
