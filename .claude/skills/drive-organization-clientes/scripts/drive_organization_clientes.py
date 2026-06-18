from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

FOLDER_MIME = "application/vnd.google-apps.folder"
FOLDER_ID_RE = re.compile(r"(?:/folders/|id=)?([a-zA-Z0-9_-]{20,})")


MONTHS = [
    "01. Janeiro",
    "02. Fevereiro",
    "03. Marco",
    "04. Abril",
    "05. Maio",
    "06. Junho",
    "07. Julho",
    "08. Agosto",
    "09. Setembro",
    "10. Outubro",
    "11. Novembro",
    "12. Dezembro",
]


def year_months() -> dict[str, dict]:
    return {"2026": {month: {} for month in MONTHS}}


DEFAULT_STRUCTURE: dict[str, Any] = {
    "01. Onboarding": {
        "01. Acessos": {},
        "02. Kickoff, QNP e DMD": {},
        "03. Diagnostico e Growth Storm": {},
        "04. Planejamento Inicial": {},
        "05. OKRs e Metas": {},
        "06. Playbook": {},
    },
    "02. Estrategia": {
        "01. Planejamentos": {},
        "02. ICP, Personas e Ofertas": {},
        "03. Funil, Jornada e CRM": {},
        "04. Calendario Comercial": {},
        "05. Replanejamentos": {},
    },
    "03. Gestao e Check-ins": {
        "01. ROPRE": year_months(),
        "02. Retrospectivas": {},
        "03. Auditorias": {},
        "04. Atas e Combinados": {},
        "05. Relatorios": {},
    },
    "04. Operacao de Marketing": {
        "01. Midia e Trafego": {
            "01. Planos de Midia": {},
            "02. Growth Pack": {},
            "03. Checklists e UTMs": {},
            "04. Notas e Recibos de Plataformas": {},
        },
        "02. CRM e Automacoes": {
            "01. Backups": {},
            "02. Fluxos": {},
            "03. Integracoes": {},
            "04. Bases e Exportacoes": {},
        },
        "03. Landing Pages e Sites": {},
        "04. Social Media": {},
    },
    "05. Copy": {
        "01. Manual de Copy": {},
        "02. Swipe File": {},
        "03. Copys": year_months(),
        "04. Briefings": {},
    },
    "06. Design": {
        "01. Identidade Visual": {},
        "02. Swipe File": {},
        "03. KVs e Referencias": {},
        "04. Criativos": year_months(),
        "05. E-commerce e Site": {},
        "06. Arquivos Editaveis": {},
    },
    "07. Campanhas": year_months(),
    "08. Compartilhada com Cliente": {
        "01. Entregas Finais": {},
        "02. Materiais Recebidos": {},
        "03. Aprovacoes": {},
        "04. Fotos, Videos e Banco de Imagens": {},
    },
    "09. Administrativo": {
        "01. Contratos e Propostas": {},
        "02. Financeiro": {},
        "03. Notas e Recibos": {},
        "04. Dados Sensiveis": {},
    },
}


def find_workspace_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "scripts" / "google_drive_folders.py").exists():
            return path
    raise SystemExit("Nao encontrei scripts/google_drive_folders.py no workspace.")


def authed_session():
    root = find_workspace_root(Path.cwd().resolve())
    sys.path.insert(0, str(root / "scripts"))
    from google_drive_folders import authed_session as get_session  # type: ignore

    return root, get_session()


def parse_folder_id(value: str) -> str:
    match = FOLDER_ID_RE.search(value)
    if not match:
        raise SystemExit(f"Nao consegui extrair ID de pasta de: {value}")
    return match.group(1)


def drive_get(session, url: str, params: dict) -> dict:
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_folder(session, folder_id: str) -> dict:
    return drive_get(
        session,
        f"https://www.googleapis.com/drive/v3/files/{folder_id}",
        {"fields": "id,name,webViewLink,createdTime,modifiedTime", "supportsAllDrives": "true"},
    )


def list_child_folders(session, folder_id: str) -> list[dict]:
    folders: list[dict] = []
    page_token = None
    while True:
        params = {
            "q": f"'{folder_id}' in parents and mimeType = '{FOLDER_MIME}' and trashed = false",
            "fields": "nextPageToken,files(id,name,webViewLink,createdTime,modifiedTime)",
            "pageSize": 1000,
            "orderBy": "name_natural",
            "includeItemsFromAllDrives": "true",
            "supportsAllDrives": "true",
        }
        if page_token:
            params["pageToken"] = page_token
        data = drive_get(session, "https://www.googleapis.com/drive/v3/files", params)
        folders.extend(data.get("files", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            return folders


def list_top_items(session, folder_id: str) -> list[dict]:
    data = drive_get(
        session,
        "https://www.googleapis.com/drive/v3/files",
        {
            "q": f"'{folder_id}' in parents and trashed = false",
            "fields": "files(id,name,mimeType,webViewLink,modifiedTime)",
            "pageSize": 1000,
            "orderBy": "name_natural",
            "includeItemsFromAllDrives": "true",
            "supportsAllDrives": "true",
        },
    )
    return data.get("files", [])


def build_tree(session, folder: dict, depth: int, max_depth: int) -> dict:
    children = list_child_folders(session, folder["id"])
    node = {
        "id": folder["id"],
        "name": folder["name"],
        "webViewLink": folder.get("webViewLink"),
        "createdTime": folder.get("createdTime"),
        "modifiedTime": folder.get("modifiedTime"),
        "childFolderCount": len(children),
        "children": [],
        "truncated": depth >= max_depth and bool(children),
    }
    if depth < max_depth:
        node["children"] = [build_tree(session, child, depth + 1, max_depth) for child in children]
    return node


def count_nodes(node: dict) -> int:
    return 1 + sum(count_nodes(child) for child in node.get("children", []))


def count_truncated(node: dict) -> int:
    return int(bool(node.get("truncated"))) + sum(count_truncated(child) for child in node.get("children", []))


def render_node(node: dict, level: int = 0) -> list[str]:
    indent = "  " * level
    suffix = f" ({node['childFolderCount']} subpastas)" if node["childFolderCount"] else ""
    if node.get("truncated"):
        suffix += " [continua]"
    lines = [f"{indent}- {node['name']}{suffix}"]
    for child in node.get("children", []):
        lines.extend(render_node(child, level + 1))
    return lines


def create_folder(session, parent_id: str, name: str) -> dict:
    response = session.post(
        "https://www.googleapis.com/drive/v3/files",
        params={"fields": "id,name,webViewLink", "supportsAllDrives": "true"},
        json={"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def ensure_tree(session, parent_id: str, tree: dict, path: str, apply: bool, log: list[dict]) -> None:
    existing = {item["name"]: item for item in list_child_folders(session, parent_id)}
    for name, children in tree.items():
        current_path = f"{path}/{name}".strip("/")
        if name in existing:
            folder = existing[name]
            action = "exists"
        elif apply:
            folder = create_folder(session, parent_id, name)
            action = "created"
        else:
            folder = {"id": None, "webViewLink": None}
            action = "would_create"
        log.append({"action": action, "path": current_path, "id": folder.get("id"), "link": folder.get("webViewLink")})
        if action == "would_create":
            log_missing_children(children, current_path, log)
        else:
            ensure_tree(session, folder["id"], children, current_path, apply, log)


def log_missing_children(tree: dict, path: str, log: list[dict]) -> None:
    for name, children in tree.items():
        current_path = f"{path}/{name}".strip("/")
        log.append({"action": "would_create", "path": current_path, "id": None, "link": None})
        log_missing_children(children, current_path, log)


def command_analyze(args) -> None:
    root_path, session = authed_session()
    folder_id = parse_folder_id(args.target)
    root = get_folder(session, folder_id)
    tree = build_tree(session, root, 0, args.depth)
    top_items = list_top_items(session, folder_id)
    report = {
        "root": tree,
        "summary": {
            "foldersListedIncludingRoot": count_nodes(tree),
            "truncatedBranchesAtDepth": count_truncated(tree),
            "maxDepthBelowRoot": args.depth,
            "topLevelItems": len(top_items),
            "topLevelFolders": sum(1 for item in top_items if item["mimeType"] == FOLDER_MIME),
            "topLevelFiles": sum(1 for item in top_items if item["mimeType"] != FOLDER_MIME),
        },
        "topLevelItems": top_items,
    }
    out_dir = root_path / "_tmp"
    out_dir.mkdir(exist_ok=True)
    stamp = date.today().isoformat()
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", root["name"]).strip("-")
    json_path = out_dir / f"drive-organization-{safe_name}-depth{args.depth}-{stamp}.json"
    md_path = out_dir / f"drive-organization-{safe_name}-depth{args.depth}-{stamp}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_lines = [
        f"# Estrutura do Drive - {root['name']}",
        "",
        f"Link: {root.get('webViewLink')}",
        f"Pastas listadas: {report['summary']['foldersListedIncludingRoot']} | Ramos com mais niveis: {report['summary']['truncatedBranchesAtDepth']}",
        f"Itens na raiz: {report['summary']['topLevelItems']} ({report['summary']['topLevelFolders']} pastas, {report['summary']['topLevelFiles']} arquivos)",
        "",
    ]
    for child in tree["children"]:
        md_lines.extend(render_node(child))
    md_path.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"json={json_path}")
    print(f"markdown={md_path}")


def command_create(args) -> None:
    root_path, session = authed_session()
    folder_id = parse_folder_id(args.target)
    root = get_folder(session, folder_id)
    log = [{"action": "root", "path": root["name"], "id": root["id"], "link": root.get("webViewLink")}]
    ensure_tree(session, folder_id, DEFAULT_STRUCTURE, root["name"], args.apply, log)
    out_dir = root_path / "_tmp"
    out_dir.mkdir(exist_ok=True)
    stamp = date.today().isoformat()
    safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "-", root["name"]).strip("-")
    mode = "applied" if args.apply else "dry-run"
    output = out_dir / f"drive-organization-{safe_name}-{mode}-{stamp}.json"
    output.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {}
    for item in log:
        counts[item["action"]] = counts.get(item["action"], 0) + 1
    print(" ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    print(f"log={output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analisa e cria estrutura padrao de Drive para clientes.")
    sub = parser.add_subparsers(dest="command", required=True)
    analyze = sub.add_parser("analyze")
    analyze.add_argument("target", help="Link ou ID da pasta raiz do Drive")
    analyze.add_argument("--depth", type=int, default=4)
    analyze.set_defaults(func=command_analyze)
    create = sub.add_parser("create")
    create.add_argument("target", help="Link ou ID da pasta raiz do Drive")
    create.add_argument("--apply", action="store_true", help="Cria as pastas de fato. Sem isso, faz dry-run.")
    create.set_defaults(func=command_create)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
