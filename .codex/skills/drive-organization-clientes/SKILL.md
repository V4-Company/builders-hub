---
name: drive-organization-clientes
description: "Organiza Drives de clientes no Google Drive: analisa estrutura de pastas, diagnostica duplicidades e cria o esqueleto padrao de cliente. Use quando o usuario pedir para analisar pasta de Drive de cliente, subir estrutura padrao, organizar pastas de cliente, criar arvore de onboarding/estrategia/check-ins/operacao/copy/design/campanhas/compartilhada/administrativo, ou repetir esse fluxo para qualquer cliente sem depender de memoria da conversa."
---

# Drive Organization Clientes

Use esta skill para auditar ou criar a estrutura padrao de pastas em Drives de clientes.

## Fluxo

1. Identifique o link ou ID da pasta raiz do cliente.
   - Se o usuario mencionar o nome do cliente e o workspace tiver cache de Drives, procure em `CLIENTES V4/_skill-ekyte/drives.md`.
   - Se nao houver link confiavel, peca o link antes de modificar qualquer coisa.
2. Rode uma analise antes de criar ou reorganizar:
   ```powershell
   python <skill>/scripts/drive_organization_clientes.py analyze "<link-ou-id>" --depth 4
   ```
3. Explique o que existe na raiz e a diferenca para o padrao.
4. Para criar a estrutura, primeiro rode dry-run:
   ```powershell
   python <skill>/scripts/drive_organization_clientes.py create "<link-ou-id>"
   ```
5. So depois rode com `--apply` quando a intencao do usuario for clara:
   ```powershell
   python <skill>/scripts/drive_organization_clientes.py create "<link-ou-id>" --apply
   ```
6. Verifique a raiz apos criar e informe quantas pastas foram criadas/reaproveitadas e onde ficou o log.

## Regras de seguranca operacional

- Nao mover, renomear ou apagar arquivos/pastas existentes sem pedido explicito.
- Nao criar estrutura em uma pasta se o link parecer provisiorio ou errado; confirme quando a raiz tiver poucos itens, nome inesperado ou muitos arquivos soltos.
- Reaproveitar pastas existentes somente quando o nome bater exatamente.
- Preferir nomes ASCII no esqueleto para evitar problemas de encoding em automacoes: `Estrategia`, `Gestao`, `Operacao`, `Midia`, `Trafego`, `Automacoes`, `Relatorios`, `Aprovacoes`.
- Guardar logs em `_tmp/` do workspace quando possivel.

## Estrutura padrao

Para ver o arquetipo completo com objetivo de cada area, regras de uso e criterios de organizacao, leia `references/arquetipo-estrutura.md`.

```text
01. Onboarding
02. Estrategia
03. Gestao e Check-ins
04. Operacao de Marketing
05. Copy
06. Design
07. Campanhas
08. Compartilhada com Cliente
09. Administrativo
```

O script cria subpastas para acessos, kickoff, planejamento, ROPRE mensal de 2026, operacao de midia/CRM, copy/design por meses, campanhas por meses, entregas finais, materiais recebidos e administrativo.

## Dependencias

O script espera rodar dentro deste workspace ou de outro que tenha:

- `scripts/google_drive_folders.py`
- `google-drive-token.json`
- `google-chat-credentials.json` se for preciso renovar autenticacao

Ele usa a sessao autenticada existente e a API do Google Drive. Nao inclua tokens ou credenciais dentro da skill.
