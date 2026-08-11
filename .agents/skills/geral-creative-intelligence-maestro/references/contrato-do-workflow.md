# Contrato do workflow Creative Intelligence

## Estrutura canônica

```text
creative-intelligence/
├── project.json
├── status.md
├── 01-descoberta/
│   ├── briefing.md
│   ├── scope.json
│   └── concorrentes.csv
├── 02-coleta/
│   ├── source-index.json
│   ├── collection-log.json
│   ├── raw/
│   └── concorrentes/<slug>/inventario-ads.json
├── 03-processamento/
│   ├── creative-index.json
│   ├── processing-summary.json
│   └── concorrentes/<slug>/{transcricoes,frames,folhas-de-contato}/
├── 04-diagnostico/
│   ├── benchmark-metricas.json
│   ├── benchmark-inventario.csv
│   ├── diagnostico.md
│   └── plano-de-acao-criativo.md
├── 05-experiencia/
│   ├── app/
│   └── generated-data.json
└── 06-entrega/
    ├── audit.json
    ├── capturas/
    ├── build/
    ├── pacote-offline/
    └── README.md
```

Mantenha nomes equivalentes quando o projeto já possuir convenção estabelecida. Registre o mapeamento em `project.json` em vez de mover arquivos desnecessariamente.

## `project.json`

Inclua no mínimo:

```json
{
  "schema_version": "1.0",
  "project_slug": "cliente-x-creative-intelligence",
  "client_label": "Cliente X",
  "snapshot_date": "YYYY-MM-DD",
  "market": "Brasil",
  "channels": ["Meta Ad Library"],
  "current_gate": 1,
  "paths": {},
  "assumptions": [],
  "blockers": []
}
```

## Handoff mínimo entre módulos

Cada módulo deve devolver:

```json
{
  "module": "nome-do-modulo",
  "status": "complete|partial|blocked",
  "started_at": "ISO-8601",
  "finished_at": "ISO-8601",
  "inputs": [],
  "outputs": [],
  "counts": {},
  "decisions": [],
  "assumptions": [],
  "warnings": [],
  "next_gate": "nome-do-proximo-gate"
}
```

Salve-o como `handoff.json` dentro da etapa. `partial` permite continuar quando a lacuna não invalida a análise; `blocked` exige explicar a condição concreta que impede avanço.

## Vocabulário de evidência

- **Observado:** aparece diretamente na fonte.
- **Calculado:** derivado de dados observados por regra explícita.
- **Inferido:** leitura plausível que precisa ser tratada como hipótese.
- **Recomendado:** decisão proposta para o cliente.
- **Não disponível:** dado que a fonte pública não fornece.

Nunca converta permanência, repetição ou volume público em afirmação de ROAS, vendas, aceitação ou qualidade de lead.

## Identificadores

- Concorrente: `competitor_slug` estável em kebab-case.
- Anúncio: identificador original da fonte, sem sobrescrever.
- Asset: hash de conteúdo ou identificador estável ligado ao hash.
- Criativo curado: `<competitor_slug>-<asset_id>`.
- Execução de coleta: `<fonte>-<YYYYMMDD-HHmmss>`.

## Gates de qualidade

1. **Descoberta:** escopo, fontes e papéis competitivos aprovados ou explicitamente assumidos.
2. **Coleta:** rastreabilidade e validação de página.
3. **Processamento:** vínculo íntegro entre anúncio, asset e análise.
4. **Diagnóstico:** números reproduzíveis e ressalvas visíveis.
5. **Experiência:** dados gerados e navegação funcional.
6. **Entrega:** auditoria, build, instruções e pacote reproduzível.

## Atualização incremental

- Preserve snapshots anteriores.
- Não misture datas de coleta sem sinalização.
- Reutilize assets por hash.
- Reprocesse apenas arquivos novos ou alterados.
- Compare snapshots em camada separada; não sobrescreva a leitura histórica.
