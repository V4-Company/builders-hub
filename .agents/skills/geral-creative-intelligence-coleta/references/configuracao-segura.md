# Configuração segura de credenciais

Este guia se aplica a todas as fontes usadas pela skill de coleta.

## Regras

- Use somente credenciais pertencentes ao usuário, equipe ou projeto autorizado.
- Nunca grave tokens em `SKILL.md`, scripts, notebooks, JSON de saída, screenshots ou mensagens.
- Nunca use o `.env` de outro cliente ou um caminho absoluto legado.
- Não passe tokens na query string quando o provedor aceitar header Bearer.
- Não imprima variáveis de ambiente, headers ou objetos de configuração completos.
- Se houver suspeita de exposição, interrompa a coleta e faça rotação da chave no provedor.

## Variáveis padronizadas

```text
APIFY_API_TOKEN
FIRECRAWL_API_KEY
```

Scripts devem ler primeiro o ambiente do processo:

```python
import os

apify_token = os.getenv("APIFY_API_TOKEN")
firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
```

Se a variável obrigatória estiver ausente, encerre com uma mensagem que contenha apenas o nome da variável — nunca o valor.

## Opção A — ambiente temporário do processo

É a opção mais segura para execução pontual. Defina a variável na sessão do terminal sem persistir em arquivo. Evite escrever o valor diretamente em comandos que ficam no histórico; prefira o gerenciador de segredos do ambiente ou entrada protegida.

Ao fechar o processo ou terminal, a credencial deixa de estar disponível.

## Opção B — `.env` local do projeto

Use somente quando os scripts suportarem explicitamente um `.env` local.

Estrutura:

```text
projeto/
├── .env
├── .env.example
└── .gitignore
```

`.env.example` pode conter apenas nomes vazios:

```dotenv
APIFY_API_TOKEN=
FIRECRAWL_API_KEY=
```

O `.gitignore` deve conter:

```gitignore
.env
.env.*
!.env.example
```

Antes de qualquer commit ou pacote, confirme que `.env` não está rastreado nem incluído no ZIP.

## Resolução do arquivo de ambiente

Quando um script aceitar `--env-file`, a ordem recomendada é:

1. variável já presente no processo;
2. arquivo passado explicitamente por `--env-file`;
3. `.env` na raiz do projeto atual;
4. falha clara informando a variável ausente.

Nunca faça busca recursiva por `.env`, nunca suba diretórios indefinidamente e nunca aponte para pastas de outros clientes.

## Headers

Use:

```python
headers = {"Authorization": f"Bearer {token}"}
```

Não registre `headers` em logs. Para auditoria, registre apenas:

```json
{
  "provider": "apify",
  "authentication": "bearer-env",
  "credential_variable": "APIFY_API_TOKEN",
  "credential_present": true
}
```

## Logs e erros

Antes de persistir uma resposta ou exceção:

- remova query strings que contenham tokens;
- masque valores com padrões de chave conhecidos;
- não salve request headers;
- não copie comandos completos que incluam credenciais;
- mantenha apenas status, endpoint sem segredo, request ID e mensagem sanitizada.

## Pacotes e builds

Exclua:

- `.env` e variantes;
- arquivos de sessão;
- perfis de navegador;
- caches de autenticação;
- logs brutos com headers;
- configurações locais que contenham chave.

Faça uma busca por nomes de variáveis e prefixos conhecidos antes da entrega. A busca deve localizar referências e placeholders; revise manualmente qualquer ocorrência com valor preenchido.

## Rotação

Rotacione a chave quando:

- foi enviada em chat ou e-mail sem proteção;
- apareceu em commit, log, screenshot ou URL;
- foi reutilizada por projeto não autorizado;
- uma pessoa ou máquina perdeu a autorização;
- o provedor ou a política interna exigir.

Depois da rotação, atualize somente o ambiente seguro e repita o teste mínimo do respectivo setup.
