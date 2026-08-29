<!--
PR gerado automaticamente pela skill /compartilhar-skill. Preencha o que faltar.
-->

## Skill sendo compartilhada

**Nome:** `{prefixo}-{slug}`
**Prefixo:** <!-- geral | gt | designer | copy | account | coord | v4mos | google | ga4 | meta | hubspot | kommo | shopify | tray -->
**Autor:** @<!-- seu-github -->
**Versao:** 1.0.0

## O que ela faz

<!-- 1-2 frases claras. Quando dispara. Que resultado entrega. -->

## Como testar

<!-- Passo a passo pro curador reproduzir. Ex: "Rode /skill-nome, responda X, espere Y" -->

## Checklist do contribuidor

- [ ] Nome segue `{prefixo}-{slug}` em kebab-case
- [ ] Frontmatter completo (`name`, `description`, `area`, `author`, `version`)
- [ ] `description` explica quando a skill deve triggerar
- [ ] Skill duplicada em `.claude/skills/` E `.agents/skills/` com conteudo identico
- [ ] Testei a skill pelo menos uma vez com sucesso
- [ ] Sem credenciais, tokens, nomes de clientes reais, ou dados pessoais
- [ ] Exemplos sao genericos ou anonimizados
- [ ] Escrita em portugues brasileiro

## Checklist do curador (eu preencho)

- [ ] Naming ok (regex `^(geral|gt|designer|copy|account|coord|v4mos|google|ga4|meta|hubspot|kommo|shopify|tray)-[a-z0-9-]+$`)
- [ ] Frontmatter valido
- [ ] Conteudo batendo com a descricao
- [ ] Sem conflito com skill existente
- [ ] `.claude/` e `.agents/` identicos
- [ ] `REGISTRY.md` vai regenerar corretamente (auto)

---

_Gerado via `/compartilhar-skill`. Duvidas? Veja [CONTRIBUTING.md](./CONTRIBUTING.md)._
