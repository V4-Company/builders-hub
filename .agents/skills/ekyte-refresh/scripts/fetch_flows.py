#!/usr/bin/env python3
"""
Regenera o cache de fluxos (flows.md) da skill ekyte-task.

Lê o token do MCP oficial direto de ~/.claude/mcp.json (server "ekyte-oficial"),
então NÃO há segredo hardcoded aqui — seguro pra compartilhar via /compartilhar-skill.

Uso:
    python fetch_flows.py [--cache "<path do cache.md>"] [--out "<path do flows.md>"]

Defaults (relativos ao cwd = raiz do repo):
    --cache  "CLIENTES V4/_skill-ekyte/cache.md"
    --out    "CLIENTES V4/_skill-ekyte/flows.md"

O que faz:
  1. Descobre a URL do MCP oficial em ~/.claude/mcp.json.
  2. Parseia os pares (sigla, task_type_id) da seção "Tipos de tarefa" do cache.md.
  3. Pra cada tipo, chama get_task_type_flow e fica com as fases reais (effort/duration > 0).
  4. Escreve flows.md: fluxo por tipo (em ordem, com phaseId) + dicionário mestre fase->phaseId.
"""
import argparse, json, os, re, sys, datetime, urllib.request

def mcp_url():
    p = os.path.expanduser("~/.claude/mcp.json")
    cfg = json.load(open(p, encoding="utf-8"))
    srv = cfg.get("mcpServers", {}).get("ekyte-oficial")
    if not srv or not srv.get("url"):
        sys.exit("ERRO: server 'ekyte-oficial' não encontrado em ~/.claude/mcp.json")
    return srv["url"]

def call(url, name, args):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": name, "arguments": args}}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read().decode()
    msg = json.loads(raw)
    if "error" in msg:
        raise RuntimeError(msg["error"].get("message", "?")[:120])
    return json.loads(msg["result"]["content"][0]["text"])

def parse_types(cache_path):
    """Extrai (sigla, id) de linhas tipo `| CA | `29740` | ...` na seção de tipos."""
    txt = open(cache_path, encoding="utf-8").read()
    # corta a partir do header de tipos pra não pegar workspaces/projetos
    i = txt.find("## Tipos de tarefa")
    scope = txt[i:] if i >= 0 else txt
    seen, types = set(), []
    for sig, tid in re.findall(r"\|\s*\**([A-Z]{1,8})\**\s*\|\s*`?(\d{3,7})`?\s*\|", scope):
        if sig not in seen:
            seen.add(sig); types.append((sig, int(tid)))
    return types

def real_phases(flow):
    out = []
    for fp in flow.get("flowPhases", []):
        if (fp.get("effort") or 0) > 0 or (fp.get("duration") or 0) > 0:
            ph = fp.get("phase", {})
            out.append({"seq": fp.get("sequential"), "phaseId": fp.get("phaseId"),
                        "name": (ph.get("name") or "").strip()})
    out.sort(key=lambda x: x["seq"] or 0)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="CLIENTES V4/_skill-ekyte/cache.md")
    ap.add_argument("--out", default="CLIENTES V4/_skill-ekyte/flows.md")
    a = ap.parse_args()

    url = mcp_url()
    types = parse_types(a.cache)
    if not types:
        sys.exit(f"ERRO: nenhum tipo encontrado em {a.cache}")
    print(f"{len(types)} tipos pra buscar...")

    data, master = [], {}
    for sig, tid in types:
        try:
            flow = call(url, "get_task_type_flow", {"id": tid})
            ph = real_phases(flow)
            data.append({"sigla": sig, "id": tid,
                         "name": (flow.get("name") or "").replace("[00]", "").strip(),
                         "days": flow.get("daysToStart"), "phases": ph})
            for p in ph:
                master.setdefault(p["phaseId"], p["name"])
            print(f"  OK {sig} {tid} -> {len(ph)} fases")
        except Exception as e:
            data.append({"sigla": sig, "id": tid, "error": str(e)[:80], "phases": []})
            print(f"  ERR {sig} {tid}: {e}")

    L = []
    L.append("# Cache ekyte — Fluxos por tipo de tarefa")
    L.append("")
    L.append(f"Gerado {datetime.date.today().isoformat()} via `/ekyte-refresh` → "
             f"`get_task_type_flow` (MCP oficial). Workflow base **Padrão Colli&Co (Oficial)** (3535).")
    L.append("")
    L.append("**O que é:** as fases REAIS (effort/duration > 0) de cada tipo, em ordem, com `phaseId`. "
             "Usado pela `/ekyte-task` pra mostrar o fluxo e resolver `nome da fase → phaseId` ao trocar responsável de etapa.")
    L.append("")
    L.append("**phaseId é global** (compartilhado entre tipos: `1`=Briefing, `5`=Copywriter, `6`=Designer…). "
             "Executor default não fica aqui (varia por workspace) — a skill lê o real via `get_detailed_task` em runtime.")
    L.append("")
    L.append("Refresh: `/ekyte-refresh`.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Fluxo por tipo (fases reais, em ordem)")
    L.append("")
    for t in sorted(data, key=lambda x: x["sigla"]):
        if t.get("error"):
            L.append(f"### {t['sigla']} ({t['id']}) · ⚠️ erro: {t['error']}"); L.append("")
            continue
        if not t["phases"]:
            L.append(f"### {t['sigla']} — {t.get('name','')} ({t['id']}) · sem fases de esforço")
            L.append("Tipo de rotina/sem fluxo de produção. Ler em runtime via `get_detailed_task`.")
            L.append("")
            continue
        L.append(f"### {t['sigla']} — {t.get('name','')} ({t['id']}) · {len(t['phases'])} fases · SLA {t.get('days')}d")
        L.append(" → ".join(f"{p['name']} `#{p['phaseId']}`" for p in t["phases"]))
        L.append("")
    L.append("---")
    L.append("")
    L.append(f"## Dicionário mestre de fases (phaseId → nome) — {len(master)} fases distintas")
    L.append("")
    L.append("Lookup `nome da fase → phaseId` (case-insensitive, match parcial).")
    L.append("")
    L.append("| phaseId | Fase |")
    L.append("|---|---|")
    for pid in sorted(master):
        L.append(f"| {pid} | {master[pid]} |")
    L.append("")

    open(a.out, "w", encoding="utf-8").write("\n".join(L))
    ok = sum(1 for t in data if not t.get("error"))
    print(f"\nOK -> {a.out}: {ok}/{len(data)} tipos, {len(master)} fases distintas")

if __name__ == "__main__":
    main()
