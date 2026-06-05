#!/usr/bin/env python3
"""Cria apontamento de horas em task do Ekyte via API interna do app."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path


API_ROOT = "https://api.ekyte.com/api"


def load_dotenv(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def find_env_path() -> Path | None:
    explicit = os.environ.get("EKYTE_ENV_PATH")
    if explicit:
        return Path(explicit)

    cwd = Path.cwd().resolve()
    candidates = [cwd, *cwd.parents]
    script_path = Path(__file__).resolve()
    candidates.extend([script_path.parent, *script_path.parents])

    seen: set[Path] = set()
    for base in candidates:
        if base in seen:
            continue
        seen.add(base)
        candidate = base / "CLIENTES V4" / "_skill-ekyte" / ".env"
        if candidate.exists():
            return candidate
    return None


def config() -> tuple[str, str]:
    env_path = find_env_path()
    file_env = load_dotenv(env_path) if env_path else {}
    token = os.environ.get("EKYTE_TOKEN") or file_env.get("EKYTE_TOKEN")
    company_id = os.environ.get("EKYTE_COMPANY_ID") or file_env.get("EKYTE_COMPANY_ID") or "3597"
    if not token:
        raise SystemExit(
            json.dumps(
                {
                    "ok": False,
                    "error": "EKYTE_TOKEN ausente. Configure em CLIENTES V4/_skill-ekyte/.env ou na variavel de ambiente.",
                },
                ensure_ascii=False,
            )
        )
    return token, company_id


def request_json(method: str, url: str, token: str, body: object | None = None) -> tuple[int, object | None]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Origin": "https://app.ekyte.com",
        "Referer": "https://app.ekyte.com/",
    }
    data = None
    if body is not None:
        data = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if not raw:
                return resp.status, None
            try:
                return resp.status, json.loads(raw)
            except json.JSONDecodeError:
                return resp.status, raw
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed: object = json.loads(raw) if raw else None
        except json.JSONDecodeError:
            parsed = raw
        raise RuntimeError(json.dumps({"http_status": exc.code, "body": parsed}, ensure_ascii=False)) from exc


def parse_hhmm(value: str) -> tuple[int, int]:
    try:
        hour_s, minute_s = value.strip().split(":", 1)
        hour = int(hour_s)
        minute = int(minute_s)
    except Exception as exc:
        raise ValueError(f"Hora invalida: {value}. Use HH:MM.") from exc
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError(f"Hora invalida: {value}. Use HH:MM.")
    return hour, minute


def minutes_between(start: str, end: str) -> int:
    sh, sm = parse_hhmm(start)
    eh, em = parse_hhmm(end)
    total = (eh * 60 + em) - (sh * 60 + sm)
    if total <= 0:
        raise ValueError("Intervalo precisa ter duracao positiva e nao pode cruzar meia-noite sem ajuste manual.")
    return total


def iso_at(day: str, hhmm: str) -> str:
    parse_hhmm(hhmm)
    datetime.strptime(day, "%Y-%m-%d")
    return f"{day}T{hhmm}:00"


def active_entries_for_task(entries: object, task_id: int, start_iso: str, end_iso: str) -> list[dict]:
    if not isinstance(entries, list):
        return []
    matches = []
    for item in entries:
        if not isinstance(item, dict):
            continue
        if item.get("ctcTaskId") != task_id:
            continue
        if item.get("status") == 30 or item.get("canceledIn"):
            continue
        if item.get("startDate") == start_iso and item.get("endDate") == end_iso:
            matches.append(item)
    return matches


def main() -> int:
    parser = argparse.ArgumentParser(description="Aponta horas em uma task do Ekyte.")
    parser.add_argument("--task-id", required=True, type=int)
    parser.add_argument("--date", default=date.today().isoformat(), help="Data YYYY-MM-DD. Padrao: hoje do sistema.")
    parser.add_argument("--start", required=True, help="Hora inicial HH:MM.")
    parser.add_argument("--end", required=True, help="Hora final HH:MM.")
    parser.add_argument("--comment", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Permite duplicar apontamento identico.")
    args = parser.parse_args()

    token, company_id = config()
    effort = minutes_between(args.start, args.end)
    start_iso = iso_at(args.date, args.start)
    end_iso = iso_at(args.date, args.end)

    task_url = f"{API_ROOT}/companies/{company_id}/ctc-tasks/{args.task_id}"
    _, task = request_json("GET", task_url, token)
    if not isinstance(task, dict) or not task.get("id"):
        raise SystemExit(json.dumps({"ok": False, "error": "Task nao encontrada."}, ensure_ascii=False))

    workspace_id = task.get("workspaceId")
    payload = {
        "typeTimeTracking": 2,
        "startDate": start_iso,
        "startDateTime": args.start,
        "endDate": end_iso,
        "endDateTime": args.end,
        "effort": effort,
        "comment": args.comment,
        "workspaceId": workspace_id,
        "type": 1,
        "ctcTaskId": args.task_id,
        "ctcTaskTypeId": task.get("ctcTaskTypeId"),
        "phaseId": task.get("phaseId"),
        "ticketId": None,
        "ticketPhaseId": None,
        "planningId": None,
        "planId": None,
        "modeOverlap": True,
    }

    query = urllib.parse.urlencode({"textSearch": str(args.task_id), "startDate": args.date, "endDate": args.date})
    verify_url = f"{API_ROOT}/companies/{company_id}/time-trackings/data/details?{query}"
    _, before = request_json("GET", verify_url, token)
    duplicates = active_entries_for_task(before, args.task_id, start_iso, end_iso)
    if duplicates and not args.force:
        print(
            json.dumps(
                {
                    "ok": False,
                    "blocked": "duplicate",
                    "message": "Ja existe apontamento ativo identico para esta task e intervalo.",
                    "existing_ids": [item.get("id") for item in duplicates],
                    "task_id": args.task_id,
                    "title": task.get("title"),
                    "date": args.date,
                    "start": args.start,
                    "end": args.end,
                    "effort": effort,
                },
                ensure_ascii=False,
            )
        )
        return 2

    if args.dry_run:
        safe_payload = dict(payload)
        print(
            json.dumps(
                {
                    "ok": True,
                    "dry_run": True,
                    "task_id": args.task_id,
                    "title": task.get("title"),
                    "workspace_id": workspace_id,
                    "workspace": (task.get("workspace") or {}).get("name"),
                    "payload": safe_payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    create_url = f"{API_ROOT}/companies/{company_id}/workspaces/{workspace_id}/time-trackings"
    status, created = request_json("POST", create_url, token, payload)
    created_id = created if isinstance(created, int) else None

    _, after = request_json("GET", verify_url, token)
    verified = False
    verified_item = None
    if isinstance(after, list):
        for item in after:
            if not isinstance(item, dict):
                continue
            if created_id and item.get("id") != created_id:
                continue
            if item.get("ctcTaskId") == args.task_id and item.get("startDate") == start_iso and item.get("endDate") == end_iso:
                verified = True
                verified_item = item
                break

    print(
        json.dumps(
            {
                "ok": status == 200 and bool(created_id) and verified,
                "http_status": status,
                "created_id": created_id,
                "verified": verified,
                "task_id": args.task_id,
                "title": task.get("title"),
                "workspace_id": workspace_id,
                "workspace": (task.get("workspace") or {}).get("name"),
                "date": args.date,
                "start": args.start,
                "end": args.end,
                "effort": effort,
                "verified_item": verified_item,
            },
            ensure_ascii=False,
        )
    )
    return 0 if status == 200 and bool(created_id) and verified else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        raise SystemExit(1)

