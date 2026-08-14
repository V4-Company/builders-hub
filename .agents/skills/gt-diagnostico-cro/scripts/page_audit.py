#!/usr/bin/env python3
"""
page_audit.py — Auditoria tecnica de URL
Camadas: PageSpeed Insights (mobile+desktop) + On-page parser (mobile+desktop UA) + Security headers.

Uso:
  page_audit.py <url> <output_json> [--api-key KEY] [--skip-psi]

Saida: JSON estruturado com pagespeed, onpage, security.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys
import time
import urllib.parse
from typing import Any

import requests
from bs4 import BeautifulSoup

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
UA_MOBILE = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
UA_DESKTOP = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

OPPORTUNITY_AUDIT_IDS = [
    "render-blocking-resources",
    "unused-css-rules",
    "unused-javascript",
    "modern-image-formats",
    "uses-optimized-images",
    "uses-text-compression",
    "uses-responsive-images",
    "efficient-animated-content",
    "duplicated-javascript",
    "server-response-time",
    "redirects",
    "uses-long-cache-ttl",
    "total-byte-weight",
]


def fetch_pagespeed(url: str, strategy: str, api_key: str | None, retries: int = 2) -> dict[str, Any]:
    params = [
        ("url", url),
        ("strategy", strategy),
        ("category", "performance"),
        ("category", "accessibility"),
        ("category", "best-practices"),
        ("category", "seo"),
        ("locale", "pt-BR"),
    ]
    if api_key:
        params.append(("key", api_key))
    qs = urllib.parse.urlencode(params)
    full_url = f"{PSI_ENDPOINT}?{qs}"

    last_err = None
    for attempt in range(retries + 1):
        try:
            r = requests.get(full_url, timeout=90)
            if r.status_code == 200:
                return parse_psi_response(r.json(), strategy)
            if r.status_code == 429 and attempt < retries:
                time.sleep(2 ** (attempt + 1))
                continue
            if r.status_code >= 500 and attempt < retries:
                time.sleep(2)
                continue
            return {
                "error": f"HTTP {r.status_code}",
                "detail": r.text[:500],
                "strategy": strategy,
            }
        except requests.RequestException as e:
            last_err = str(e)
            if attempt < retries:
                time.sleep(2)
                continue
    return {"error": "request_failed", "detail": last_err, "strategy": strategy}


def parse_psi_response(data: dict, strategy: str) -> dict[str, Any]:
    lh = data.get("lighthouseResult", {}) or {}
    cats = lh.get("categories", {}) or {}
    audits = lh.get("audits", {}) or {}
    le = data.get("loadingExperience", {}) or {}

    def score(cat: str) -> int | None:
        v = (cats.get(cat) or {}).get("score")
        return round(v * 100) if isinstance(v, (int, float)) else None

    def audit_val(name: str, num: bool = True) -> Any:
        a = audits.get(name) or {}
        return a.get("numericValue") if num else a.get("displayValue")

    scores = {
        "performance": score("performance"),
        "accessibility": score("accessibility"),
        "best_practices": score("best-practices"),
        "seo": score("seo"),
    }

    cwv_lab = {
        "lcp_ms": audit_val("largest-contentful-paint"),
        "fcp_ms": audit_val("first-contentful-paint"),
        "tbt_ms": audit_val("total-blocking-time"),
        "cls": audit_val("cumulative-layout-shift"),
        "speed_index_ms": audit_val("speed-index"),
        "tti_ms": audit_val("interactive"),
        "ttfb_ms": audit_val("server-response-time"),
    }

    def field_metric(key: str) -> dict | None:
        m = (le.get("metrics") or {}).get(key)
        if not m:
            return None
        return {"percentile": m.get("percentile"), "category": m.get("category")}

    cwv_field = {
        "lcp": field_metric("LARGEST_CONTENTFUL_PAINT_MS"),
        "inp": field_metric("INTERACTION_TO_NEXT_PAINT"),
        "cls": field_metric("CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "fcp": field_metric("FIRST_CONTENTFUL_PAINT_MS"),
    }
    crux_overall = le.get("overall_category")

    opportunities = []
    for audit_id in OPPORTUNITY_AUDIT_IDS:
        a = audits.get(audit_id) or {}
        s = a.get("score")
        if s is None or (isinstance(s, (int, float)) and s >= 0.9):
            continue
        details = a.get("details") or {}
        savings_ms = details.get("overallSavingsMs") or a.get("numericValue") or 0
        savings_bytes = details.get("overallSavingsBytes")
        opportunities.append(
            {
                "id": audit_id,
                "title": a.get("title"),
                "description": a.get("description"),
                "savings_ms": round(savings_ms) if savings_ms else 0,
                "savings_bytes": savings_bytes,
                "display_value": a.get("displayValue"),
            }
        )
    opportunities.sort(key=lambda x: x.get("savings_ms") or 0, reverse=True)

    # Screenshot final (data URI base64). "final-screenshot" e o viewport do final do load.
    final_ss = audits.get("final-screenshot") or {}
    ss_data = (final_ss.get("details") or {}).get("data")
    # Tamanho do viewport retornado para referencia (mobile=360x, desktop=412x)
    ss_timing = (final_ss.get("details") or {}).get("timing")

    return {
        "strategy": strategy,
        "scores": scores,
        "cwv_lab": cwv_lab,
        "cwv_field": cwv_field,
        "crux_overall_category": crux_overall,
        "opportunities": opportunities,
        "final_screenshot": ss_data,
        "final_screenshot_timing_ms": ss_timing,
        "fetch_time": lh.get("fetchTime"),
    }


def fetch_onpage(url: str, user_agent: str, label: str) -> dict[str, Any]:
    t0 = time.time()
    try:
        r = requests.get(
            url,
            headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml"},
            timeout=30,
            allow_redirects=True,
        )
        elapsed_ms = round((time.time() - t0) * 1000)
    except requests.RequestException as e:
        return {"label": label, "error": str(e)}

    html = r.text or ""
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    def meta(attr: str, name: str) -> str | None:
        tag = soup.find("meta", attrs={attr: name})
        return tag.get("content") if tag and tag.has_attr("content") else None

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None

    canonical_tag = soup.find("link", rel="canonical")
    canonical = canonical_tag.get("href") if canonical_tag else None

    lang = (soup.html.get("lang") if soup.html and soup.html.has_attr("lang") else None)

    og = {}
    twitter = {}
    for m in soup.find_all("meta"):
        prop = m.get("property") or ""
        name = m.get("name") or ""
        content = m.get("content")
        if prop.startswith("og:"):
            og[prop[3:]] = content
        elif name.startswith("twitter:"):
            twitter[name[8:]] = content

    schema_types = []
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            raw = s.string or s.get_text() or ""
            data = json.loads(raw)
            items = data if isinstance(data, list) else [data]
            for it in items:
                if isinstance(it, dict):
                    t = it.get("@type")
                    if isinstance(t, list):
                        schema_types.extend(t)
                    elif t:
                        schema_types.append(t)
        except Exception:
            continue
    schema_types = sorted(set(str(t) for t in schema_types))

    h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
    h2_count = len(soup.find_all("h2"))
    h3_count = len(soup.find_all("h3"))
    h4_count = len(soup.find_all("h4"))

    imgs = soup.find_all("img")
    images_total = len(imgs)
    images_without_alt = sum(1 for i in imgs if not (i.get("alt") or "").strip())

    links = soup.find_all("a", href=True)
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc
    internal = external = nofollow = 0
    for a in links:
        href = a["href"]
        rel = " ".join(a.get("rel") or [])
        if "nofollow" in rel:
            nofollow += 1
        if href.startswith("/") or host in href:
            internal += 1
        elif href.startswith("http://") or href.startswith("https://"):
            external += 1

    viewport = soup.find("meta", attrs={"name": "viewport"}) is not None
    favicon = bool(
        soup.find("link", rel=re.compile(r"(^|\s)(shortcut\s+)?icon(\s|$)", re.I))
        or soup.find("link", rel="apple-touch-icon")
    )

    headers = {k: v for k, v in r.headers.items()}

    return {
        "label": label,
        "status_code": r.status_code,
        "final_url": r.url,
        "response_time_ms": elapsed_ms,
        "html_size_kb": round(len(html.encode("utf-8")) / 1024, 1),
        "title": title,
        "title_length": len(title) if title else 0,
        "meta_description": meta("name", "description"),
        "meta_description_length": len(meta("name", "description") or ""),
        "robots": meta("name", "robots"),
        "canonical": canonical,
        "lang": lang,
        "viewport": viewport,
        "favicon": favicon,
        "h1": h1s,
        "h1_count": len(h1s),
        "h2_count": h2_count,
        "h3_count": h3_count,
        "h4_count": h4_count,
        "images_total": images_total,
        "images_without_alt": images_without_alt,
        "links_total": len(links),
        "links_internal": internal,
        "links_external": external,
        "links_nofollow": nofollow,
        "schema_types": schema_types,
        "og": og,
        "twitter_card": twitter,
        "headers": headers,
    }


def compute_security(onpage_desktop: dict, onpage_mobile: dict, url: str) -> dict[str, Any]:
    headers = (onpage_desktop.get("headers") or onpage_mobile.get("headers") or {})
    h_lower = {k.lower(): v for k, v in headers.items()}

    def hget(key: str) -> str | None:
        return h_lower.get(key)

    is_https = url.startswith("https://")
    if not is_https:
        final = onpage_desktop.get("final_url") or onpage_mobile.get("final_url") or ""
        is_https = final.startswith("https://")

    return {
        "https": is_https,
        "hsts": hget("strict-transport-security"),
        "csp": hget("content-security-policy"),
        "x_frame_options": hget("x-frame-options"),
        "x_content_type_options": hget("x-content-type-options"),
        "referrer_policy": hget("referrer-policy"),
        "content_type": hget("content-type"),
        "content_encoding": hget("content-encoding"),
        "cache_control": hget("cache-control"),
        "server": hget("server"),
    }


def compute_divergences(mob: dict, desk: dict) -> list[str]:
    if mob.get("error") or desk.get("error"):
        return []
    diffs = []
    fields = [("title", "Title"), ("meta_description", "Meta description"), ("canonical", "Canonical"), ("lang", "Lang"), ("h1_count", "H1 count")]
    for key, label in fields:
        a, b = mob.get(key), desk.get(key)
        if a != b:
            diffs.append(f"{label} divergente — mobile: {a!r} · desktop: {b!r}")
    if mob.get("final_url") != desk.get("final_url"):
        diffs.append(f"URL final divergente — mobile: {mob.get('final_url')} · desktop: {desk.get('final_url')}")
    return diffs


def run_audit(url: str, api_key: str | None, skip_psi: bool) -> dict[str, Any]:
    result: dict[str, Any] = {
        "url": url,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    tasks: dict[str, concurrent.futures.Future] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        if not skip_psi and api_key:
            tasks["psi_mobile"] = ex.submit(fetch_pagespeed, url, "mobile", api_key)
            tasks["psi_desktop"] = ex.submit(fetch_pagespeed, url, "desktop", api_key)
        tasks["onpage_mobile"] = ex.submit(fetch_onpage, url, UA_MOBILE, "mobile")
        tasks["onpage_desktop"] = ex.submit(fetch_onpage, url, UA_DESKTOP, "desktop")

        for name, fut in tasks.items():
            try:
                result[name] = fut.result(timeout=120)
            except Exception as e:
                result[name] = {"error": str(e)}

    if skip_psi or not api_key:
        result["pagespeed_skipped"] = True
        result["pagespeed_reason"] = "no_api_key" if not api_key else "skipped_by_flag"

    onpage = {
        "mobile": result.get("onpage_mobile"),
        "desktop": result.get("onpage_desktop"),
        "divergences": compute_divergences(result.get("onpage_mobile") or {}, result.get("onpage_desktop") or {}),
    }
    result["onpage"] = onpage
    for k in ("onpage_mobile", "onpage_desktop"):
        result.pop(k, None)

    result["security"] = compute_security(onpage.get("desktop") or {}, onpage.get("mobile") or {}, url)

    result["pagespeed"] = {
        "mobile": result.pop("psi_mobile", None) if "psi_mobile" in result else None,
        "desktop": result.pop("psi_desktop", None) if "psi_desktop" in result else None,
    }
    if result["pagespeed"]["mobile"] is None and result["pagespeed"]["desktop"] is None:
        result["pagespeed"] = None

    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("output")
    parser.add_argument("--api-key", default=os.environ.get("PSI_API_KEY"))
    parser.add_argument("--skip-psi", action="store_true")
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        print("ERROR: url precisa comecar com http:// ou https://", file=sys.stderr)
        return 2

    result = run_audit(args.url, args.api_key, args.skip_psi)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    psi_m = (result.get("pagespeed") or {}).get("mobile") or {}
    psi_d = (result.get("pagespeed") or {}).get("desktop") or {}
    print(f"[OK] {args.url} -> {args.output}")
    if isinstance(psi_m.get("scores"), dict):
        print(f"  PSI mobile  perf={psi_m['scores'].get('performance')} a11y={psi_m['scores'].get('accessibility')} bp={psi_m['scores'].get('best_practices')} seo={psi_m['scores'].get('seo')}")
    if isinstance(psi_d.get("scores"), dict):
        print(f"  PSI desktop perf={psi_d['scores'].get('performance')} a11y={psi_d['scores'].get('accessibility')} bp={psi_d['scores'].get('best_practices')} seo={psi_d['scores'].get('seo')}")
    op = result.get("onpage") or {}
    mob = op.get("mobile") or {}
    print(f"  On-page     title='{(mob.get('title') or '')[:60]}' h1={mob.get('h1_count')} images_no_alt={mob.get('images_without_alt')}/{mob.get('images_total')}")
    sec = result.get("security") or {}
    print(f"  Security    https={sec.get('https')} hsts={'sim' if sec.get('hsts') else 'nao'} csp={'sim' if sec.get('csp') else 'nao'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
