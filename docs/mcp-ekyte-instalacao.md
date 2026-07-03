# Instalacao do MCP oficial do Ekyte

Guia baseado na documentacao oficial ([developers.ekyte.com/docs/mcp](https://developers.ekyte.com/docs/mcp/)) para conectar o MCP do Ekyte no Claude Code.

## Passo 1 — Gerar o token de acesso

1. Entre na plataforma Ekyte com seu usuario.
2. Va em **Configuracoes** (cadastro de usuario).
3. Localize o campo **Token de Acesso para MCP** e gere/copie o token.

O token e pessoal — as acoes feitas via MCP ficam registradas na sua conta, e as tools so acessam os dados que a empresa autenticada tem permissao de ver.

## Passo 2 — Montar a URL do servidor

```
https://api.ekyte.com/mcp?token=SEU_TOKEN_AQUI
```

Troque `SEU_TOKEN_AQUI` pelo token gerado no Passo 1. **Nunca** commite essa URL com o token real em nenhum arquivo do repositorio.

## Passo 3 — Registrar no Claude Code

Adicione o servidor no `~/.claude/mcp.json` (formato padrao de MCP server via HTTP):

```json
{
  "mcpServers": {
    "ekyte-oficial": {
      "url": "https://api.ekyte.com/mcp?token=SEU_TOKEN_AQUI"
    }
  }
}
```

**Nota:** a documentacao oficial do Ekyte nao publica um exemplo pronto de configuracao para Claude Desktop/Claude Code — o bloco acima segue o formato padrao de servidor MCP via URL/HTTP. Se o Ekyte mudar o transporte (SSE, streamable-http, etc), ajuste conforme a mensagem de erro ao conectar.

Alternativa via CLI (sem editar o JSON na mao):

```bash
claude mcp add ekyte-oficial "https://api.ekyte.com/mcp?token=SEU_TOKEN_AQUI"
```

## Passo 4 — Validar a conexao

1. Reinicie o Claude Code (ou rode `/mcp` para ver os servidores conectados).
2. Confirme que `ekyte-oficial` aparece como conectado.
3. Teste com uma tool simples, ex: `list_projects` ou `list_workspaces`, para confirmar que o token tem acesso aos dados esperados.

## Escopo e permissoes

- O token valida permissoes pelo **perfil do usuario** dentro do Ekyte — mesmas regras de visibilidade da UI se aplicam via MCP.
- A empresa autenticada so enxerga dados que ela tem permissao de acessar (nao ha vazamento cross-empresa).
- Se o token expirar ou for revogado, gere um novo em Configuracoes e atualize o `mcp.json`.

## Skills que dependem desse MCP

As skills do Ekyte no hub (`ekyte-task`, `ekyte-briefing`, `ekyte-refresh`, `ekyte-briefing-refresh`, `ekyte-templates-refresh`, `gestao-ekyte-rename-tasks`, `gestao-ekyte-tags`) assumem que o servidor `ekyte-oficial` (ou equivalente) ja esta configurado e conectado antes de rodar. Sem o MCP, essas skills nao conseguem criar/listar/atualizar tarefas.
