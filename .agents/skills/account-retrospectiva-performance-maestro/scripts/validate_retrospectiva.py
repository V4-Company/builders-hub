#!/usr/bin/env python3
"""Valida estrutura, cobertura de mídia, ledger de decisões e prontidão de uma retrospectiva."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path


REQUIRED_FRONTMATTER = {
    "schema_version",
    "module",
    "client_id",
    "period_start",
    "period_end",
    "analysis_start",
    "run_id",
    "generated_at",
    "status",
    "business_model",
}

CORE_FILES = {
    "00-manifesto-fontes.md",
    "01-contexto-cliente.md",
    "07-breakeven.md",
    "08-reconciliacao.md",
    "09-evidencias.md",
    "10-achados-gaps.md",
    "11-retrospectiva-final.md",
}

MEDIA_BASES = {
    "cobertura-midia.md",
    "canais.md",
    "destinos.md",
    "campanhas.md",
    "conjuntos.md",
    "anuncios.md",
    "breakdowns.md",
}

MEDIA_DIMENSIONS = {
    "overall",
    "canal",
    "rede_subcanal",
    "estrategia",
    "destino",
    "campanha",
    "conjunto",
    "anuncio",
    "criativo",
    "publico_keyword",
    "regiao",
    "genero",
    "idade",
    "dispositivo",
    "posicionamento",
}

VALID_COVERAGE_STATUS = {"complete", "partial", "unavailable", "not_applicable"}

DECISIONS_FILE = "decisoes.md"
DECISION_COLUMNS = {"id", "arquivo", "tipo", "criticidade", "status"}
DECISION_TYPES = {
    "modelo_negocio",
    "janela_temporal",
    "exclusao_teste",
    "definicao_funil",
    "fonte_oficial",
    "calendario_operacional",
    "premissa_economica",
    "rubrica",
    "atribuicao",
    "lacuna",
    "outro",
}
DECISION_CRITICALITY = {"critica", "alta", "media", "baixa"}
DECISION_STATUS = {
    "evidenciada",
    "assumida",
    "aberta",
    "confirmada",
    "corrigida",
    "aceita",
    "resolvida",
}
BLOCKING_DECISION_STATUS = {"assumida", "aberta"}


def normalized(value: str) -> str:
    text = unicodedata.normalize("NFKD", value)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter ausente")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("frontmatter não encerrado")
    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([a-z_]+):\s*[\"']?(.*?)[\"']?\s*$", line)
        if match:
            result[match.group(1)] = match.group(2)
    return result


def parse_coverage(path: Path) -> tuple[dict[str, str], list[str]]:
    rows: dict[str, str] = {}
    errors: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        dimension = normalized(cells[0])
        if dimension in {"dimensao", "dimension"}:
            continue
        if dimension not in MEDIA_DIMENSIONS:
            continue
        status = normalized(cells[2])
        if status not in VALID_COVERAGE_STATUS:
            errors.append(f"cobertura-midia.md: status inválido para {dimension}: {cells[2]}")
            continue
        rows[dimension] = status
    return rows, errors


def target_key(value: str) -> str:
    text = value.strip().strip("`").strip()
    if text.lower().startswith("cobertura-midia:"):
        return "cobertura-midia:" + normalized(text.split(":", 1)[1])
    return text


def parse_decisions(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    header: list[str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            header = None
            continue
        if re.match(r"^\|\s*:?-", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        keys = [normalized(cell) for cell in cells]
        if DECISION_COLUMNS <= set(keys):
            header = keys
            continue
        if header is None:
            continue
        row = dict(zip(header, cells))
        rows.append(row)
        label = row.get("id", "?")
        if normalized(row.get("tipo", "")) not in DECISION_TYPES:
            errors.append(f"{DECISIONS_FILE}: tipo inválido em {label}: {row.get('tipo', '')}")
        if normalized(row.get("criticidade", "")) not in DECISION_CRITICALITY:
            errors.append(
                f"{DECISIONS_FILE}: criticidade inválida em {label}: {row.get('criticidade', '')}"
            )
        if normalized(row.get("status", "")) not in DECISION_STATUS:
            errors.append(f"{DECISIONS_FILE}: status inválido em {label}: {row.get('status', '')}")
    if not rows and not errors:
        errors.append(f"{DECISIONS_FILE}: ledger sem tabela de decisões")
    return rows, errors


def gaps_by_target(rows: list[dict[str, str]]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for row in rows:
        if normalized(row.get("tipo", "")) != "lacuna":
            continue
        result.setdefault(target_key(row.get("arquivo", "")), set()).add(
            normalized(row.get("status", ""))
        )
    return result


def table_has_data(path: Path) -> bool:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or re.match(r"^\|\s*:?-", line):
            continue
        cells = [normalized(cell) for cell in line.strip().strip("|").split("|")]
        if not cells:
            continue
        header_tokens = {
            "canal", "destino", "campanha", "conjunto", "anuncio", "dimensao",
            "periodo", "frente", "nivel", "breakdown", "valor",
        }
        if cells[0] not in header_tokens:
            return True
    return False


def markdown_headings(path: Path) -> set[str]:
    headings: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.add(normalized(match.group(1)))
    return headings


def validate(root: Path, approval_ready: bool = False, review_ready: bool = False) -> list[str]:
    errors: list[str] = []
    top_files = sorted(root.glob("*.md"))
    if not top_files:
        return ["nenhum Markdown canônico encontrado"]

    present = {path.name for path in top_files}
    for required in sorted(CORE_FILES - present):
        errors.append(f"arquivo obrigatório ausente: {required}")

    metadata: dict[Path, dict[str, str]] = {}
    run_ids: set[str] = set()
    markdown_files = sorted(root.rglob("*.md"))
    for path in markdown_files:
        try:
            meta = parse_frontmatter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        metadata[path] = meta
        missing = REQUIRED_FRONTMATTER - set(meta)
        if missing:
            errors.append(
                f"{path.relative_to(root)}: campos ausentes: {', '.join(sorted(missing))}"
            )
        if meta.get("business_model") not in {"inside_sales", "ecommerce"}:
            errors.append(f"{path.relative_to(root)}: business_model inválido")
        if meta.get("status") not in {"complete", "partial", "blocked"}:
            errors.append(f"{path.relative_to(root)}: status inválido")
        if meta.get("run_id"):
            run_ids.add(meta["run_id"])
        period_start = meta.get("period_start", "")
        period_end = meta.get("period_end", "")
        analysis_start = meta.get("analysis_start", "")
        if analysis_start and period_start and period_end:
            if not period_start <= analysis_start <= period_end:
                errors.append(
                    f"{path.relative_to(root)}: analysis_start fora do período declarado"
                )

    if len(run_ids) > 1:
        errors.append("run_id divergente entre arquivos")

    models = {meta.get("business_model") for meta in metadata.values() if meta.get("business_model")}
    if "inside_sales" in models:
        for name in ("04-funil-inside-sales.md", "05-vendedores.md"):
            if name not in present:
                errors.append(f"arquivo obrigatório de inside sales ausente: {name}")
    if "ecommerce" in models and "04-ecommerce.md" not in present:
        errors.append("arquivo obrigatório de e-commerce ausente: 04-ecommerce.md")

    media_in_scope = "02-midia.md" in present or (root / "bases" / "cobertura-midia.md").exists()
    if media_in_scope:
        if "02-midia.md" not in present:
            errors.append("mídia em escopo sem 02-midia.md")
        bases = root / "bases"
        for name in sorted(MEDIA_BASES):
            if not (bases / name).exists():
                errors.append(f"base obrigatória de mídia ausente: bases/{name}")

        coverage_path = bases / "cobertura-midia.md"
        coverage: dict[str, str] = {}
        if coverage_path.exists():
            coverage, coverage_errors = parse_coverage(coverage_path)
            errors.extend(coverage_errors)
            for dimension in sorted(MEDIA_DIMENSIONS - set(coverage)):
                errors.append(f"dimensão ausente na cobertura de mídia: {dimension}")

            media_meta = metadata.get(root / "02-midia.md", {})
            if media_meta.get("status") == "complete":
                incomplete = {
                    dimension: status
                    for dimension, status in coverage.items()
                    if status in {"partial", "unavailable"}
                }
                for dimension, status in sorted(incomplete.items()):
                    errors.append(
                        f"02-midia.md está complete, mas {dimension} está {status}"
                    )

            base_dimension = {
                "canais.md": "canal",
                "destinos.md": "destino",
                "campanhas.md": "campanha",
                "conjuntos.md": "conjunto",
                "anuncios.md": "anuncio",
            }
            for name, dimension in base_dimension.items():
                path = bases / name
                if not path.exists():
                    continue
                if coverage.get(dimension) in {"complete", "partial"} and not table_has_data(path):
                    errors.append(
                        f"bases/{name}: cobertura {coverage.get(dimension)} sem linhas de dados"
                    )

    review_ready = review_ready or approval_ready
    if not review_ready:
        return errors

    phase = "approval-ready" if approval_ready else "review-ready"
    coverage = {}
    if media_in_scope and (root / "bases" / "cobertura-midia.md").exists():
        coverage, _ = parse_coverage(root / "bases" / "cobertura-midia.md")
    incomplete_media = {
        f"cobertura-midia:{dimension}": status
        for dimension, status in coverage.items()
        if status in {"partial", "unavailable"}
    }
    incomplete_modules = {
        path.name: metadata.get(path, {}).get("status") or "sem status"
        for path in top_files
        if path.name != DECISIONS_FILE and metadata.get(path, {}).get("status") != "complete"
    }

    decisions_path = root / DECISIONS_FILE
    decisions: list[dict[str, str]] = []
    if not decisions_path.exists():
        errors.append(f"{phase}: {DECISIONS_FILE} ausente")
    else:
        decisions, decision_errors = parse_decisions(decisions_path)
        errors.extend(f"{phase}: {error}" for error in decision_errors)
    gaps = gaps_by_target(decisions)

    for target, status in sorted({**incomplete_modules, **incomplete_media}.items()):
        if target not in gaps:
            errors.append(f"{phase}: {target} está {status} sem lacuna registrada em {DECISIONS_FILE}")

    final_path = root / "11-retrospectiva-final.md"
    if final_path.exists():
        final_headings = markdown_headings(final_path)
        for required_heading in sorted({
            "analise_detalhada",
            "indice_de_insumos_completos",
            "janelas_temporais_da_retrospectiva",
        }):
            if required_heading not in final_headings:
                errors.append(
                    f"{phase}: 11-retrospectiva-final.md sem seção {required_heading}"
                )

        final_text = final_path.read_text(encoding="utf-8")
        expected_links = [path.name for path in top_files if path.name != final_path.name]
        expected_links.extend(
            str(path.relative_to(root)).replace("\\", "/")
            for path in sorted((root / "bases").glob("*.md"))
        )
        for reference in expected_links:
            if reference not in final_text:
                errors.append(f"{phase}: índice final não referencia {reference}")

    findings_path = root / "10-achados-gaps.md"
    if findings_path.exists():
        findings_headings = markdown_headings(findings_path)
        if "inventario_integral_de_achados" not in findings_headings:
            errors.append(
                f"{phase}: 10-achados-gaps.md sem seção inventario_integral_de_achados"
            )

    if approval_ready:
        for row in decisions:
            status = normalized(row.get("status", ""))
            if status in BLOCKING_DECISION_STATUS:
                errors.append(
                    f"approval-ready: {row.get('id', '?')} está {status} em {DECISIONS_FILE}"
                )
        for target, status in sorted({**incomplete_modules, **incomplete_media}.items()):
            if "aceita" not in gaps.get(target, set()):
                label = target.replace("cobertura-midia:", "dimensão de mídia ")
                errors.append(f"approval-ready: {label} está {status} sem lacuna aceita")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument(
        "--review-ready",
        action="store_true",
        help="Fim da execução autônoma: exige decisoes.md válido, lacuna para todo módulo ou "
        "dimensão incompleta e documento final integral.",
    )
    parser.add_argument(
        "--approval-ready",
        action="store_true",
        help="Inclui --review-ready e bloqueia decisões assumidas, lacunas abertas e módulos "
        "incompletos sem lacuna aceita.",
    )
    args = parser.parse_args()
    errors = validate(
        args.root, approval_ready=args.approval_ready, review_ready=args.review_ready
    )
    if errors:
        print("FALHOU")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
