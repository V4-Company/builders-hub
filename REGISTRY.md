# Builders Hub — Registry

**18 skills**

> Catálogo auto-gerado por `scripts/build-registry.py`. Não edite à mão — rode `/sync-hub` ou envie PR pela `/compartilhar-skill`.

## Índice

- [🛠 Base (setup/fluxo)](#base) (8)
- [🌐 Geral](#geral) (5)
- [🤝 Account](#account) (4)
- [🔌 Integrações / Fontes](#fontes) (1)
  - [🔌 V4mos](#v4mos) (1)

## 🛠 Base (setup/fluxo)

<a id="base"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `compartilhar-skill` | Empacota uma skill local e abre Pull Request no Builders Hub publico automaticamente. Use quando o usuario... | — | — |
| `contexto` | Le todos os arquivos em uma KB (cliente, squad ou projeto), gera CLAUDE.md e AGENTS.md, e quando for client... | — | — |
| `criador-de-skills` | Cria skills novas e melhora skills existentes no Builders Hub. Use quando o usuario quiser criar uma skill... | — | — |
| `novo-cliente` | Cria uma nova pasta de cliente dentro de um squad com estrutura padrao, CLAUDE.md/AGENTS.md iniciais, links... | — | — |
| `novo-projeto` | Cria uma nova pasta de projeto com estrutura padrao em bases/. Use quando o usuario rodar /novo-projeto ou... | — | — |
| `novo-squad` | Cria uma nova pasta de squad em squads/ com README de membros e estrutura padrao. Pergunta nome do squad e... | — | — |
| `onboarding` | Configura todo o ambiente do usuario pra trabalhar com IA na V4 via o Builders Hub — valida e conserta git... | — | — |
| `sync-hub` | Atualiza o Builders Hub local puxando as skills mais recentes do repo publico, mostra diff do que mudou des... | — | — |

## 🌐 Geral

<a id="geral"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `geral-backup-kb-drive` | Faz backup de uma KB (cliente, squad ou projeto) numa pasta do Google Drive, espelhando a estrutura de past... | @luizfreitasv4 | 1.0.0 |
| `geral-brainstormar-sobre-minha-funcao` | Entrevista o usuario sobre seu trabalho para descobrir como usar IA no dia a dia dele. Configura agenda, an... | @guilhermelippert | 1.0.0 |
| `geral-discovery-produto` | Conduz discovery completo de produto com base em documentos, reuniões, mercado e canais atuais, separando f... | @luizfreitasv4 | 1.0.0 |
| `geral-frontend-design` | Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the... | @guilhermelippert | 1.0.0 |
| `geral-sabatina` | Entrevista o usuario de forma implacavel sobre cada aspecto de um plano ou design ate atingir entendimento... | @guilhermelippert | 1.0.0 |

## 🤝 Account

<a id="account"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `account-checkin-review` | Pos-call de check-in. Le o transcript do Gemini Notes (ou texto colado) da call que acabou e atualiza o Mis... | @guilhermelippert | 1.0.0 |
| `account-checkin-roleplay` | Prepara o account pra reunião de check-in com cliente seguindo ROPRE V2 e roda roleplay realista simulando... | @guilhermelippert | 1.0.0 |
| `account-handoff` | Primeira skill que o account roda quando recebe um cliente novo de vendas. Le form de kickoff + transcript... | @guilhermelippert | 1.0.0 |
| `account-pesquisa-profunda-cliente` | Pesquisa profunda de cliente para KB acionavel. PREMISSA OBRIGATORIA - dados do cliente ja na pasta (no min... | @guilhermelippert | 1.5.0 |

## 🔌 Integrações / Fontes

<a id="fontes"></a>

_Skills que puxam dados de integrações externas. Reutilizáveis por outras skills._

## 🔌 V4mos

<a id="v4mos"></a>

| Skill | O que faz | Autor | v |
|---|---|---|---|
| `v4mos-dados-meta-ads` | Puxa qualquer dado de Meta Ads (Facebook + Instagram) via API V4mos pra um cliente especifico. Use sempre q... | @guilhermelippert | 2.1.0 |

---

_Quer contribuir? Roda `/compartilhar-skill`. Mais detalhes em [CONTRIBUTING.md](./CONTRIBUTING.md)._
