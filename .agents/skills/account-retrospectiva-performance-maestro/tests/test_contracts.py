#!/usr/bin/env python3
"""Testes sintéticos dos contratos da família de retrospectiva."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
MAESTRO = HERE.parent
VALIDATOR_PATH = MAESTRO / "scripts" / "validate_retrospectiva.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_retrospectiva", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def document(
    module: str,
    business_model: str,
    run_id: str = "2026-09-29T120000-03",
    status: str = "complete",
    body: str = "# Teste\n\n## Evidências\n\n- evidence_id: EV-001",
) -> str:
    return f'''---
schema_version: "1.0"
module: "{module}"
client_id: "cliente-teste"
period_start: "2026-07-01"
period_end: "2026-09-30"
analysis_start: "2026-07-01"
run_id: "{run_id}"
generated_at: "2026-09-29T12:00:00-03:00"
status: "{status}"
business_model: "{business_model}"
---

{body}
'''


DECISION_HEADER = (
    "| id | arquivo | tipo | criticidade | decisão aplicada | base e evidência | alternativas "
    "| impacto se errada | recalcula a partir de | status | resposta humana |\n"
    "|---|---|---|---|---|---|---|---|---|---|---|"
)


def decision_row(
    identifier: str,
    target: str,
    kind: str,
    status: str,
    criticality: str = "alta",
) -> str:
    return (
        f"| {identifier} | `{target}` | {kind} | {criticality} | valor aplicado | EV-001 "
        f"| alternativa | impacto | 02-midia.md | {status} | |"
    )


def write_decisions(root: Path, model: str, rows: list[str] | None = None) -> None:
    rows = rows if rows is not None else [
        decision_row("D-001", "04-funil-inside-sales.md", "definicao_funil", "evidenciada")
    ]
    body = (
        "# Decisões\n\n## Estado da execução\n\nTeste.\n\n## Ledger de decisões\n\n"
        + DECISION_HEADER + "\n" + "\n".join(rows)
        + "\n\n## Como responder\n\n- `D-001 ok`"
    )
    (root / "decisoes.md").write_text(document("decisoes", model, body=body), encoding="utf-8")


def set_status(path: Path, status: str) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace('status: "complete"', f'status: "{status}"', 1), encoding="utf-8")


def write_core(root: Path, model: str, status: str = "complete") -> None:
    write_decisions(root, model)
    files = {
        "00-manifesto-fontes.md": "contexto-fontes",
        "01-contexto-cliente.md": "contexto-cliente",
        "07-breakeven.md": "breakeven",
        "08-reconciliacao.md": "reconciliacao",
        "09-evidencias.md": "evidencias",
        "10-achados-gaps.md": "achados-gaps",
        "11-retrospectiva-final.md": "consolidacao",
    }
    if model == "inside_sales":
        files["04-funil-inside-sales.md"] = "funil-inside-sales"
        files["05-vendedores.md"] = "vendedores"
    else:
        files["04-ecommerce.md"] = "ecommerce"
    for name, module in files.items():
        body = "# Teste\n\n## Evidências\n\n- evidence_id: EV-001"
        if name == "10-achados-gaps.md":
            body += "\n\n## Inventário integral de achados\n\n- Achado completo."
        (root / name).write_text(document(module, model, status=status, body=body), encoding="utf-8")

    references = "\n".join(
        f"- [{name}]({name})"
        for name in sorted({*files, "decisoes.md"})
        if name != "11-retrospectiva-final.md"
    )
    final_body = (
        "# Retrospectiva final\n\n"
        "## Janelas temporais da retrospectiva\n\nQuarter e performance.\n\n"
        "## Análise detalhada\n\nAnálise integral.\n\n"
        "## Índice de insumos completos\n\n"
        f"{references}"
    )
    (root / "11-retrospectiva-final.md").write_text(
        document("consolidacao", model, status=status, body=final_body), encoding="utf-8"
    )


def coverage_body(partial_dimension: str | None = None, omit: str | None = None) -> str:
    dimensions = [
        "overall", "canal", "rede_subcanal", "estrategia", "destino",
        "campanha", "conjunto", "anuncio", "criativo", "publico_keyword",
        "regiao", "genero", "idade", "dispositivo", "posicionamento",
    ]
    lines = [
        "# Cobertura",
        "",
        "| dimensão | aplicável | status | fonte | cobertura |",
        "|---|---|---|---|---|",
    ]
    for dimension in dimensions:
        if dimension == omit:
            continue
        status = "partial" if dimension == partial_dimension else "complete"
        lines.append(f"| {dimension} | sim | {status} | NEKT | 100% |")
    return "\n".join(lines)


def write_media(root: Path, status: str = "complete", partial_dimension: str | None = None, omit: str | None = None) -> None:
    model = "inside_sales"
    (root / "02-midia.md").write_text(document("midia", model, status=status), encoding="utf-8")
    bases = root / "bases"
    bases.mkdir()
    (bases / "cobertura-midia.md").write_text(
        document("base-cobertura-midia", model, status=status, body=coverage_body(partial_dimension, omit)),
        encoding="utf-8",
    )
    fixtures = {
        "canais.md": "| canal | investimento |\n|---|---:|\n| Meta | 100 |",
        "destinos.md": "| destino | investimento |\n|---|---:|\n| formulário | 100 |",
        "campanhas.md": "| campanha | investimento |\n|---|---:|\n| C1 | 100 |",
        "conjuntos.md": "| conjunto | investimento |\n|---|---:|\n| A1 | 100 |",
        "anuncios.md": "| anúncio | investimento |\n|---|---:|\n| AD1 | 100 |",
        "breakdowns.md": "| breakdown | valor | investimento |\n|---|---|---:|\n| gênero | feminino | 100 |",
    }
    for name, table in fixtures.items():
        (bases / name).write_text(
            document(f"base-{name.removesuffix('.md')}", model, status=status, body=f"# Base\n\n{table}"),
            encoding="utf-8",
        )
    final_path = root / "11-retrospectiva-final.md"
    final_text = final_path.read_text(encoding="utf-8")
    base_refs = "\n".join(f"- [bases/{name}](bases/{name})" for name in sorted({"cobertura-midia.md", *fixtures}))
    final_path.write_text(final_text + "\n" + base_refs + "\n- [02-midia.md](02-midia.md)\n", encoding="utf-8")


def test_validator() -> None:
    validator = load_validator()
    for model in ("inside_sales", "ecommerce"):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_core(root, model)
            assert validator.validate(root) == []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        (root / "extra.md").write_text(document("extra", "inside_sales", "run-b"), encoding="utf-8")
        assert "run_id divergente entre arquivos" in validator.validate(root)


def test_media_gate() -> None:
    validator = load_validator()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        (root / "02-midia.md").write_text(document("midia", "inside_sales"), encoding="utf-8")
        errors = validator.validate(root)
        assert "base obrigatória de mídia ausente: bases/conjuntos.md" in errors
        assert "base obrigatória de mídia ausente: bases/anuncios.md" in errors

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        write_media(root)
        assert validator.validate(root) == []
        assert validator.validate(root, approval_ready=True) == []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        write_media(root, omit="posicionamento")
        assert "dimensão ausente na cobertura de mídia: posicionamento" in validator.validate(root)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        write_media(root, status="complete", partial_dimension="anuncio")
        assert "02-midia.md está complete, mas anuncio está partial" in validator.validate(root)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales", status="partial")
        errors = validator.validate(root, approval_ready=True)
        assert any(error.startswith("approval-ready:") for error in errors)


def test_exhaustive_delivery_gate() -> None:
    validator = load_validator()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        (root / "11-retrospectiva-final.md").write_text(
            document("consolidacao", "inside_sales", body="# Resumo\n\nSomente resumo."),
            encoding="utf-8",
        )
        errors = validator.validate(root, approval_ready=True)
        assert any("sem seção analise_detalhada" in error for error in errors)
        assert any("sem seção indice_de_insumos_completos" in error for error in errors)
        assert any("sem seção janelas_temporais_da_retrospectiva" in error for error in errors)
        assert any("índice final não referencia" in error for error in errors)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, "inside_sales")
        (root / "10-achados-gaps.md").write_text(
            document("achados-gaps", "inside_sales", body="# Achados\n\nSomente top 3."),
            encoding="utf-8",
        )
        errors = validator.validate(root, approval_ready=True)
        assert "approval-ready: 10-achados-gaps.md sem seção inventario_integral_de_achados" in errors


def test_decision_ledger_gates() -> None:
    validator = load_validator()
    model = "inside_sales"

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, model)
        (root / "decisoes.md").unlink()
        assert "review-ready: decisoes.md ausente" in validator.validate(root, review_ready=True)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, model)
        set_status(root / "05-vendedores.md", "partial")
        errors = validator.validate(root, review_ready=True)
        assert (
            "review-ready: 05-vendedores.md está partial sem lacuna registrada em decisoes.md"
            in errors
        )

        write_decisions(root, model, [
            decision_row("D-001", "04-funil-inside-sales.md", "definicao_funil", "assumida", "critica"),
            decision_row("L-001", "05-vendedores.md", "lacuna", "aberta"),
        ])
        assert validator.validate(root, review_ready=True) == []
        errors = validator.validate(root, approval_ready=True)
        assert "approval-ready: D-001 está assumida em decisoes.md" in errors
        assert "approval-ready: L-001 está aberta em decisoes.md" in errors
        assert "approval-ready: 05-vendedores.md está partial sem lacuna aceita" in errors

        write_decisions(root, model, [
            decision_row("D-001", "04-funil-inside-sales.md", "definicao_funil", "confirmada", "critica"),
            decision_row("L-001", "05-vendedores.md", "lacuna", "aceita"),
        ])
        assert validator.validate(root, approval_ready=True) == []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, model)
        write_media(root, status="partial", partial_dimension="regiao")
        errors = validator.validate(root, review_ready=True)
        assert any("cobertura-midia:regiao está partial sem lacuna registrada" in e for e in errors)
        assert any("02-midia.md está partial sem lacuna registrada" in e for e in errors)

        write_decisions(root, model, [
            decision_row("L-001", "02-midia.md", "lacuna", "aceita"),
            decision_row("L-002", "cobertura-midia:regiao", "lacuna", "aceita", "media"),
        ])
        assert validator.validate(root, approval_ready=True) == []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_core(root, model)
        write_decisions(root, model, [
            decision_row("D-001", "04-funil-inside-sales.md", "palpite", "talvez"),
        ])
        errors = validator.validate(root, review_ready=True)
        assert "review-ready: decisoes.md: tipo inválido em D-001: palpite" in errors
        assert "review-ready: decisoes.md: status inválido em D-001: talvez" in errors


def test_rules() -> None:
    refs = MAESTRO / "references"
    atendimento = (refs / "atendimento.md").read_text(encoding="utf-8")
    cobertura = (refs / "cobertura-midia.md").read_text(encoding="utf-8")
    profundidade = (refs / "profundidade-entrega.md").read_text(encoding="utf-8")
    fontes = (refs / "fontes-e-reconciliacao.md").read_text(encoding="utf-8")
    metricas = (refs / "metricas-e-rankings.md").read_text(encoding="utf-8")
    qualidade = (refs / "qualidade-comercial.md").read_text(encoding="utf-8")
    janelas = (refs / "janelas-temporais.md").read_text(encoding="utf-8")
    autonomo = (refs / "modo-autonomo.md").read_text(encoding="utf-8")
    assert "7 ou mais follow-ups" in atendimento
    assert "próxima abertura" in atendimento
    assert "first_paid_touch" in fontes
    assert "Nome isolado apenas como candidato" in fontes
    assert "Não use volume mínimo global" in metricas
    assert "CPVenda" in metricas
    assert "15 dimensões" in cobertura
    assert "100% das entidades" in cobertura
    assert "zero resultado" in cobertura
    assert "bases/conjuntos.md" in cobertura
    assert "Consolidar` significa integrar" in profundidade
    assert "Não limite a entrega a top 3" in profundidade
    assert "Índice de insumos completos" in profundidade
    assert "publica o pacote, não apenas o resumo" in profundidade
    assert "três camadas independentes" in qualidade
    assert "Não gere uma nota única" in qualidade
    assert "20 a 30 conversas" in qualidade
    assert "80% de concordância" in qualidade
    assert "100% de captura" in qualidade
    assert "7 ou mais follow-ups" in qualidade
    assert "evidência explícita" in qualidade
    assert "Nunca armazene tokens" in qualidade
    assert "quarter_window" in janelas
    assert "pre_operational_window" in janelas
    assert "performance_window" in janelas
    assert "smoke tests" in janelas
    assert "execution_mode: autonomous" in autonomo
    assert "Únicas paradas antes do fim" in autonomo
    assert "Não invente definição" in autonomo
    assert "parent_run_id" in autonomo
    assert "## Mapa de recálculo" in autonomo
    assert "libera o adaptador" in autonomo


def main() -> int:
    test_validator()
    test_media_gate()
    test_exhaustive_delivery_gate()
    test_decision_ledger_gates()
    test_rules()
    print("OK: contratos, cobertura macro-micro, ledger de decisoes, aprovacao, atendimento e rankings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
