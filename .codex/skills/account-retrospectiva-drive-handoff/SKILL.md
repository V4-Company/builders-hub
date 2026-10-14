---
name: account-retrospectiva-drive-handoff
description: Prepara o manifesto versionado para transformar a retrospectiva aprovada em Google Docs, Google Sheets e pasta de assets no Drive do cliente. Use somente depois de `retrospectiva aprovada`, quando o usuário quiser publicar ou deixar o pacote pronto para publicação.
area: account
author: junioraiellogestaodetrafego-maker
version: 1.2.0
---

# Handoff para Drive

Leia `contrato-markdown.md` do maestro.

## Saída

- `13-drive-handoff.md`

## Regras

1. Confirme que `retrospectiva aprovada` está registrada e que `decisoes.md` não tem decisão `assumida` nem lacuna `aberta`. Publique `decisoes.md` junto com o pacote.
2. Resolva a pasta oficial do cliente e crie uma versão nova; nunca sobrescreva histórico.
3. Mapeie narrativa para Google Docs, bases extensas para Google Sheets e assets para subpasta de criativos.
4. Preserve links, IDs, run_id, período e versão.
5. Solicite autorização explícita antes de escrever no Drive.
6. Depois de autorizado, use as skills Google Drive/Docs/Sheets apropriadas.
7. Publique o pacote completo: retrospectiva final, módulos analíticos, todas as bases, ledger de evidências e assets. Não publique somente o resumo executivo.
8. Registre no manifesto a contagem de arquivos, abas, linhas e assets esperados versus publicados; qualquer aplicável omitido mantém status `partial`.

O manifesto deve registrar destino planejado, destino efetivo, IDs dos arquivos criados, status, timestamp, falhas e cobertura do pacote. Até a autorização, ele permanece apenas como plano de publicação em Markdown.
