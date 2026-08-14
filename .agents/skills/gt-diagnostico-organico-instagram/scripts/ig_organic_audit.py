#!/usr/bin/env python3
"""
ig_organic_audit.py — Coleta publica via Instagram Graph API + business_discovery.

Uso:
  python3 ig_organic_audit.py <client_dir>

Le:
  .credentials/meta-graph-api.json  (token longo + ig_business_account_v4)
  <client_dir>/client.json          (briefing.instagram = @handle do cliente)
  <client_dir>/outputs/geral-pesquisa-mercado.json  (escolhe top 2 concorrentes por digital_score)

Grava:
  <client_dir>/cache/ig_organic_audit-<ts>.json         (raw por conta)
  <client_dir>/cache/ig_organic_audit-summary.json      (input direto para a skill)
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

GRAPH_BASE = "https://graph.facebook.com/v21.0"
DAYS_WINDOW = 90
TOP_N = 3
BOTTOM_N = 3


def log(msg):
    print(f"[ig_audit] {msg}", flush=True)


def die(msg, code=1):
    print(f"[ig_audit] ERRO: {msg}", file=sys.stderr, flush=True)
    sys.exit(code)


def find_credentials(client_dir: Path) -> Path:
    d = client_dir.resolve()
    for _ in range(6):
        candidate = d / ".credentials" / "meta-graph-api.json"
        if candidate.exists():
            return candidate
        if d.parent == d:
            break
        d = d.parent
    die("meta-graph-api.json nao encontrado subindo a partir de " + str(client_dir))


def http_get(url: str, retries: int = 3, backoff: float = 1.5):
    last_err = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "v4-ig-audit/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            last_err = f"HTTP {e.code}: {body[:400]}"
            if e.code in (500, 502, 503, 504):
                time.sleep(backoff ** i)
                continue
            raise RuntimeError(last_err)
        except Exception as e:
            last_err = str(e)
            time.sleep(backoff ** i)
    raise RuntimeError(last_err or "http_get falhou")


def clean_handle(h: str) -> str:
    if not h:
        return ""
    h = h.strip()
    m = re.search(r"instagram\.com/([^/?#]+)", h)
    if m:
        h = m.group(1)
    return h.lstrip("@").strip("/").strip()


def call_business_discovery(ig_user_id: str, target_username: str, token: str, since_iso: str):
    """
    Uma unica chamada retorna perfil + posts recentes (limit=50).
    Inclui paginacao manual via next cursor.
    """
    fields = (
        "business_discovery.username(" + target_username + "){"
        "id,username,name,biography,profile_picture_url,website,followers_count,"
        "follows_count,media_count,"
        "media.limit(50){id,caption,media_type,media_product_type,media_url,"
        "permalink,thumbnail_url,timestamp,like_count,comments_count,children{media_type,media_url}}"
        "}"
    )
    url = f"{GRAPH_BASE}/{ig_user_id}?fields={urllib.parse.quote(fields)}&access_token={token}"
    payload = http_get(url)
    bd = payload.get("business_discovery")
    if not bd:
        raise RuntimeError(f"business_discovery vazio para @{target_username}: {json.dumps(payload)[:400]}")

    # Paginacao: tentamos uma segunda pagina se tiver
    posts = (bd.get("media") or {}).get("data") or []
    after = ((bd.get("media") or {}).get("paging") or {}).get("cursors", {}).get("after")
    pages = 1
    # Filtro 90d — se a ultima ja eh mais antiga, nao precisa paginar
    def oldest_ts(items):
        if not items: return None
        return min(p.get("timestamp","") for p in items)

    while after and pages < 5:
        last_old = oldest_ts(posts)
        if last_old and last_old < since_iso:
            break
        fields2 = (
            "business_discovery.username(" + target_username + "){"
            "media.after(" + after + ").limit(50){id,caption,media_type,media_product_type,media_url,"
            "permalink,thumbnail_url,timestamp,like_count,comments_count,children{media_type,media_url}}"
            "}"
        )
        url2 = f"{GRAPH_BASE}/{ig_user_id}?fields={urllib.parse.quote(fields2)}&access_token={token}"
        try:
            nxt = http_get(url2)
        except Exception as e:
            log(f"paginacao parou: {e}")
            break
        nbd = nxt.get("business_discovery") or {}
        nposts = (nbd.get("media") or {}).get("data") or []
        if not nposts:
            break
        posts.extend(nposts)
        after = ((nbd.get("media") or {}).get("paging") or {}).get("cursors", {}).get("after")
        pages += 1

    bd["_all_media"] = posts
    return bd


def classify_format(p: dict) -> str:
    mt = (p.get("media_type") or "").upper()
    mpt = (p.get("media_product_type") or "").upper()
    if mpt == "REELS":
        return "REELS"
    if mt == "CAROUSEL_ALBUM":
        return "CAROUSEL"
    if mt == "VIDEO":
        return "VIDEO"
    if mt == "IMAGE":
        return "FEED_IMAGE"
    return mt or "UNKNOWN"


def post_summary(p: dict, username: str, followers: int):
    caption = p.get("caption") or ""
    likes = p.get("like_count") or 0
    comments = p.get("comments_count") or 0
    eng = 0.0
    if followers and followers > 0:
        eng = round((likes + 3 * comments) / followers * 100, 3)
    permalink = p.get("permalink") or ""
    embed = permalink.rstrip("/") + "/embed/" if permalink else ""
    caption_clean = caption.replace("\n", " ").strip()
    hashtags = re.findall(r"#\w+", caption)
    mentions = re.findall(r"@\w+", caption)
    cta_markers = ["clique", "acesse", "agende", "whatsapp", "link", "bio", "chama", "reserve", "confira"]
    has_cta = any(m in caption.lower() for m in cta_markers)
    return {
        "username": username,
        "post_id": p.get("id"),
        "permalink": permalink,
        "embed_url": embed,
        "media_type": p.get("media_type"),
        "format": classify_format(p),
        "thumbnail_url": p.get("thumbnail_url") or p.get("media_url"),
        "media_url": p.get("media_url"),
        "timestamp": p.get("timestamp"),
        "caption": caption_clean[:1200],
        "caption_length": len(caption),
        "hashtags_count": len(hashtags),
        "mentions_count": len(mentions),
        "has_cta": has_cta,
        "like_count": likes,
        "comments_count": comments,
        "engagement_proxy": eng,
    }


def weekday_name(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][dt.weekday()]
    except Exception:
        return ""


def hour_bucket(ts: str) -> str:
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return f"{dt.hour:02d}h"
    except Exception:
        return ""


def aggregate_account(raw_bd: dict, handle: str, since_dt: datetime):
    posts_all = raw_bd.get("_all_media") or []
    since_iso = since_dt.isoformat()
    posts_90d = [p for p in posts_all if (p.get("timestamp") or "") >= since_iso]
    followers = raw_bd.get("followers_count") or 0
    enriched = [post_summary(p, handle, followers) for p in posts_90d]

    counts = {"FEED_IMAGE": 0, "CAROUSEL": 0, "REELS": 0, "VIDEO": 0}
    for e in enriched:
        counts[e["format"]] = counts.get(e["format"], 0) + 1

    # Cadencia
    weeks = max(1, round(DAYS_WINDOW / 7))
    posts_per_week = round(len(enriched) / weeks, 2)

    wd = {}
    hr = {}
    for e in enriched:
        d = weekday_name(e.get("timestamp") or "")
        h = hour_bucket(e.get("timestamp") or "")
        if d: wd[d] = wd.get(d, 0) + 1
        if h: hr[h] = hr.get(h, 0) + 1

    preferred_weekday = max(wd.items(), key=lambda x: x[1])[0] if wd else None
    preferred_hour = max(hr.items(), key=lambda x: x[1])[0] if hr else None

    # Engajamento
    likes_avg = round(sum(e["like_count"] for e in enriched) / len(enriched), 1) if enriched else 0
    comm_avg = round(sum(e["comments_count"] for e in enriched) / len(enriched), 1) if enriched else 0
    eng_avg = round(sum(e["engagement_proxy"] for e in enriched) / len(enriched), 3) if enriched else 0

    # Melhor formato por engajamento
    by_fmt = {}
    for e in enriched:
        by_fmt.setdefault(e["format"], []).append(e["engagement_proxy"])
    best_format = None
    if by_fmt:
        best_format = max(
            by_fmt.items(),
            key=lambda kv: (sum(kv[1]) / len(kv[1])) if kv[1] else 0
        )[0]

    account = {
        "username": handle,
        "name": raw_bd.get("name"),
        "biography": raw_bd.get("biography"),
        "profile_picture_url": raw_bd.get("profile_picture_url"),
        "website": raw_bd.get("website"),
        "followers_count": followers,
        "follows_count": raw_bd.get("follows_count"),
        "media_count_total": raw_bd.get("media_count"),
        "posts_90d": len(enriched),
        "permalink": f"https://www.instagram.com/{handle}/",
    }

    top = sorted(enriched, key=lambda e: e["engagement_proxy"], reverse=True)[:TOP_N]
    bottom = sorted(enriched, key=lambda e: e["engagement_proxy"])[:BOTTOM_N]

    return {
        "account": account,
        "counts": counts,
        "cadence": {
            "posts_per_week": posts_per_week,
            "preferred_weekday": preferred_weekday,
            "preferred_hour": preferred_hour,
        },
        "engagement": {
            "avg_likes": likes_avg,
            "avg_comments": comm_avg,
            "avg_engagement_proxy": eng_avg,
            "best_format_by_engagement": best_format,
        },
        "top_posts": top,
        "bottom_posts": bottom,
        "all_posts_90d": enriched,
    }


def pick_competitors(pesquisa_path: Path, briefing_competitor_handles: dict, top_n: int = 2):
    """
    Le outputs/geral-pesquisa-mercado.json, ordena por digital_score DESC,
    retorna lista de (nome, handle) dos top_n com handle conhecido.
    handle pode vir de digital_details.instagram ou de briefing_competitor_handles (override).
    """
    if not pesquisa_path.exists():
        die(f"Nao encontrei {pesquisa_path} — rode geral-pesquisa-mercado antes")
    data = json.loads(pesquisa_path.read_text(encoding="utf-8"))
    comps = data.get("competitors") or []
    comps_sorted = sorted(comps, key=lambda c: c.get("digital_score") or 0, reverse=True)
    picked = []
    for c in comps_sorted:
        name = c.get("name", "")
        name_lc = name.lower()
        handle_raw = ""
        # 1) Override manual — substring match case-insensitive (a chave pode ser parte do nome)
        for k, v in briefing_competitor_handles.items():
            if not k:
                continue
            if k in name_lc or name_lc.startswith(k):
                handle_raw = v
                break
        # 2) Extracao do campo instagram do digital_details
        if not handle_raw:
            ig_field = ((c.get("digital_details") or {}).get("instagram") or "")
            m = re.search(r"@([A-Za-z0-9._]+)", ig_field)
            if m:
                handle_raw = m.group(1)
        if handle_raw:
            picked.append({"name": name, "handle": clean_handle(handle_raw), "digital_score": c.get("digital_score")})
        if len(picked) >= top_n:
            break
    return picked


def main():
    if len(sys.argv) < 2:
        die("Uso: ig_organic_audit.py <client_dir>")
    client_dir = Path(sys.argv[1])
    if not client_dir.exists():
        die(f"client_dir {client_dir} nao existe")

    cred_path = find_credentials(client_dir)
    cred = json.loads(cred_path.read_text(encoding="utf-8"))
    token = cred.get("access_token_long") or cred.get("access_token_short")
    ig_user_id = cred.get("ig_business_account_v4")
    if not token or not ig_user_id:
        die("Credenciais incompletas: falta access_token ou ig_business_account_v4")

    client_json_path = client_dir / "client.json"
    if not client_json_path.exists():
        die(f"{client_json_path} nao existe")
    client_json = json.loads(client_json_path.read_text(encoding="utf-8"))

    briefing = client_json.get("briefing") or {}
    client_handle_raw = (
        (briefing.get("identification") or {}).get("instagram")
        or briefing.get("instagram")
        or ""
    )
    if not client_handle_raw:
        # procura recursivamente por chave "instagram"
        def find_ig(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == "instagram" and isinstance(v, str) and v.strip():
                        return v
                    r = find_ig(v)
                    if r: return r
            elif isinstance(obj, list):
                for x in obj:
                    r = find_ig(x)
                    if r: return r
            return None
        client_handle_raw = find_ig(briefing) or ""

    client_handle = clean_handle(client_handle_raw)
    if not client_handle:
        die("Handle do Instagram do cliente nao encontrado em client.json (briefing.identification.instagram)")

    # Override manual via env var CMP_HANDLES (formato: "Nome1=@handle1;Nome2=@handle2")
    manual = {}
    env = os.environ.get("CMP_HANDLES", "").strip()
    if env:
        for pair in env.split(";"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                manual[k.strip().lower()] = clean_handle(v)

    # Concorrentes: top 2 por digital_score em geral-pesquisa-mercado
    pesquisa_path = client_dir / "outputs" / "geral-pesquisa-mercado.json"
    competitors = pick_competitors(pesquisa_path, manual, top_n=2)
    if len(competitors) < 1:
        die("Nao consegui identificar 2 concorrentes com handle de Instagram — use CMP_HANDLES para override")

    log(f"Cliente: @{client_handle}")
    for c in competitors:
        log(f"Concorrente: @{c['handle']} (digital_score={c['digital_score']})")

    since_dt = datetime.now(timezone.utc) - timedelta(days=DAYS_WINDOW)
    since_iso = since_dt.isoformat()

    accounts = []

    # Cliente
    log(f"Chamando business_discovery para @{client_handle}...")
    client_bd = call_business_discovery(ig_user_id, client_handle, token, since_iso)
    client_agg = aggregate_account(client_bd, client_handle, since_dt)
    client_agg["_role"] = "client"
    accounts.append(client_agg)

    # Concorrentes
    for c in competitors:
        try:
            log(f"Chamando business_discovery para @{c['handle']}...")
            bd = call_business_discovery(ig_user_id, c["handle"], token, since_iso)
            agg = aggregate_account(bd, c["handle"], since_dt)
            agg["_role"] = "competitor"
            agg["account"]["competitor_source_name"] = c["name"]
            agg["account"]["digital_score"] = c["digital_score"]
            accounts.append(agg)
        except Exception as e:
            log(f"Falha em @{c['handle']}: {e}")

    # Raw
    cache_dir = client_dir / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    raw_path = cache_dir / f"ig_organic_audit-{ts}.json"
    raw_path.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "period": {
                    "start": since_dt.date().isoformat(),
                    "end": datetime.now(timezone.utc).date().isoformat(),
                    "days": DAYS_WINDOW,
                },
                "client_handle": client_handle,
                "accounts": accounts,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    log(f"Raw salvo em {raw_path}")

    # Summary — insumo direto para a skill gerar o output
    def acc_lite(a):
        return {
            "role": a["_role"],
            "account": a["account"],
            "counts": a["counts"],
            "cadence": a["cadence"],
            "engagement": a["engagement"],
            "top_posts": a["top_posts"],
            "bottom_posts": a["bottom_posts"],
        }

    summary = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "period": {
            "start": since_dt.date().isoformat(),
            "end": datetime.now(timezone.utc).date().isoformat(),
            "days": DAYS_WINDOW,
        },
        "client": acc_lite(accounts[0]),
        "competitors": [acc_lite(a) for a in accounts[1:]],
        "raw_cache_file": str(raw_path.relative_to(client_dir.parent.parent)) if raw_path.is_absolute() else str(raw_path),
    }

    summary_path = cache_dir / "ig_organic_audit-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Summary salvo em {summary_path}")

    # Breve resumo no stdout
    print()
    print("=== RESUMO ===")
    for a in accounts:
        acc = a["account"]
        eng = a["engagement"]
        print(f"@{acc['username']:<30} followers={acc.get('followers_count')} posts_90d={acc.get('posts_90d')} eng={eng['avg_engagement_proxy']}% best={eng['best_format_by_engagement']}")
    print()


if __name__ == "__main__":
    main()
