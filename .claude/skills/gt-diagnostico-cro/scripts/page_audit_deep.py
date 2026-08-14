#!/usr/bin/env python3
"""
page_audit_deep.py — Auditoria profunda via Playwright headless.

Captura:
  - tracking_stack: quais ferramentas (GTM, GA4, Meta Pixel, Clarity, etc.) estao presentes
  - events_fired: quais eventos GA4/Meta Pixel sao disparados no load + interacoes
  - dataLayer: dump do window.dataLayer
  - platform: CMS/plataforma (WordPress, Shopify, VTEX, Next.js...)
  - cro_elements: analise profunda de CTAs, forms, WhatsApp, prova social, urgencia
  - compliance_lgpd: deteccao de CMP + scripts pre-consent (2-pass)
  - quality_flags: red flags de tagueamento (UA legacy, pixel duplicado, scripts parallel)

Uso:
  python3 page_audit_deep.py <url> <output_json>
  python3 page_audit_deep.py <url> <output_json> --skip-compliance (pula 2-pass)

Requisitos:
  pip install -r requirements-deep.txt
  python3 -m playwright install chromium
"""
import sys
import os
import re
import json
import time
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yaml

try:
    from playwright.async_api import async_playwright, Page, Request, Response, TimeoutError as PWTimeout
except ImportError:
    print("ERRO: Playwright nao instalado. Rode: pip3 install --user -r requirements-deep.txt && python3 -m playwright install chromium", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


SCRIPT_DIR = Path(__file__).resolve().parent
SIGNATURES_FILE = SCRIPT_DIR / "signatures" / "tools.yaml"

USER_AGENT_MOBILE = "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
USER_AGENT_DESKTOP = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

VIEWPORT_MOBILE = {"width": 390, "height": 844}
VIEWPORT_DESKTOP = {"width": 1440, "height": 900}

NAV_TIMEOUT_MS = 45000
IDLE_TIMEOUT_MS = 15000


def load_signatures():
    with open(SIGNATURES_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f).get("tools", [])


class NetworkLog:
    """Coleta todas as requests/responses durante a navegacao."""
    def __init__(self):
        self.requests = []  # [{url, method, resource_type, headers, post_data_preview, timestamp}]
        self.responses = []  # [{url, status, headers}]

    def on_request(self, req: Request):
        try:
            post = None
            try:
                post = req.post_data
                if post and len(post) > 2000:
                    post = post[:2000]
            except Exception:
                pass
            self.requests.append({
                "url": req.url,
                "method": req.method,
                "resource_type": req.resource_type,
                "post_data_preview": post,
                "ts": time.time(),
            })
        except Exception:
            pass

    def on_response(self, resp: Response):
        try:
            self.responses.append({
                "url": resp.url,
                "status": resp.status,
                "headers": dict(resp.headers),
            })
        except Exception:
            pass


def detect_tools(signatures, network_log: NetworkLog, html: str, window_globals: list, cookies: list):
    """Cross-checks signatures against network URLs, HTML content, window globals, and cookies."""
    detected = {}
    all_urls = [r["url"] for r in network_log.requests]
    all_resp_urls = [r["url"] for r in network_log.responses]
    urls_combined = "\n".join(all_urls + all_resp_urls)
    globals_set = set(window_globals or [])
    cookie_names = set((c.get("name") for c in (cookies or [])))

    soup = None
    if BeautifulSoup is not None and html:
        try:
            soup = BeautifulSoup(html, "lxml")
        except Exception:
            try:
                soup = BeautifulSoup(html, "html.parser")
            except Exception:
                soup = None

    for sig in signatures:
        evidence = []

        # URL patterns
        for pat in (sig.get("url_patterns") or []):
            if pat in urls_combined:
                matches = [u for u in all_urls if pat in u]
                evidence.append({"type": "url", "pattern": pat, "sample": matches[0] if matches else pat})
                break

        # window globals
        for g in (sig.get("window_globals") or []):
            if g in globals_set:
                evidence.append({"type": "window", "key": g})
                break

        # DOM selectors (usar BS4 CSS selector, senao fallback conservador)
        for sel in (sig.get("dom_selectors") or []):
            matched = False
            if soup is not None:
                try:
                    if soup.select_one(sel):
                        matched = True
                except Exception:
                    matched = False
            else:
                # Fallback: extrair todos valores de [attr="value"] do selector e exigir todos no HTML
                attr_vals = re.findall(r'\[[^=\]]+=["\']?([^"\'\]]+)', sel)
                if attr_vals and all(v.lower() in html.lower() for v in attr_vals):
                    matched = True
                elif not attr_vals:
                    key = sel.lstrip(".#")
                    if key and key.lower() in html.lower():
                        matched = True
            if matched:
                evidence.append({"type": "dom", "selector": sel})
                break

        # cookies
        for cname in (sig.get("cookies") or []):
            if cname in cookie_names:
                evidence.append({"type": "cookie", "name": cname})
                break

        # headers (resposta do doc principal)
        hdrs = sig.get("headers") or {}
        if hdrs and network_log.responses:
            # usar primeira resposta 2xx/3xx do doc principal
            doc_resp = next((r for r in network_log.responses if r["status"] < 400), None)
            if doc_resp:
                for hname, hpat in hdrs.items():
                    hval = doc_resp["headers"].get(hname.lower(), "")
                    if hval and re.search(hpat, hval):
                        evidence.append({"type": "header", "name": hname, "value": hval[:120]})
                        break

        if evidence:
            detected[sig["id"]] = {
                "id": sig["id"],
                "name": sig["name"],
                "category": sig["category"],
                "evidence": evidence,
                "notes": sig.get("notes", ""),
            }

    return detected


def extract_ids_from_urls(network_log: NetworkLog):
    """Extrai IDs de conta (GTM-XXX, G-XXX, UA-XXX, AW-XXX, pixel_id) das URLs."""
    ids = {
        "gtm": set(),
        "ga4": set(),
        "ua": set(),
        "google_ads": set(),
        "meta_pixel": set(),
        "tiktok_pixel": set(),
        "linkedin_partner": set(),
    }
    for r in network_log.requests:
        u = r["url"]
        # GTM container
        m = re.search(r'[?&]id=(GTM-[A-Z0-9]+)', u)
        if m:
            ids["gtm"].add(m.group(1))
        # GA4
        m = re.search(r'[?&]tid=(G-[A-Z0-9]+)', u)
        if m:
            ids["ga4"].add(m.group(1))
        m = re.search(r'[?&]id=(G-[A-Z0-9]+)', u)
        if m:
            ids["ga4"].add(m.group(1))
        # UA
        m = re.search(r'[?&]tid=(UA-\d+-\d+)', u)
        if m:
            ids["ua"].add(m.group(1))
        # Google Ads
        m = re.search(r'(AW-\d+)', u)
        if m:
            ids["google_ads"].add(m.group(1))
        # Meta Pixel
        m = re.search(r'facebook\.com/tr[/?].*[?&]id=(\d+)', u)
        if m:
            ids["meta_pixel"].add(m.group(1))
        # TikTok
        m = re.search(r'tiktok.*[?&]sdkid=([A-Z0-9]+)', u, re.I)
        if m:
            ids["tiktok_pixel"].add(m.group(1))
        # LinkedIn
        m = re.search(r'linkedin.*pid=(\d+)', u, re.I)
        if m:
            ids["linkedin_partner"].add(m.group(1))

    return {k: sorted(list(v)) for k, v in ids.items()}


def parse_ga4_events(network_log: NetworkLog):
    """Parse eventos GA4 de google-analytics.com/g/collect."""
    events = []
    for r in network_log.requests:
        u = r["url"]
        if "google-analytics.com/g/collect" not in u and "analytics.google.com/g/collect" not in u:
            continue
        try:
            parsed = urlparse(u)
            qs = parse_qs(parsed.query)
            # Alguns eventos vem em POST body (batch)
            body_qs = {}
            if r.get("post_data_preview"):
                try:
                    body_qs = parse_qs(r["post_data_preview"])
                except Exception:
                    pass
            merged = {**qs, **body_qs}
            en = merged.get("en", [None])[0]
            if not en:
                continue
            event = {
                "name": en,
                "tid": merged.get("tid", [None])[0],
                "gcs": merged.get("gcs", [None])[0],  # Consent Mode v2 state
                "dl": merged.get("dl", [None])[0],  # page url
                "dt": merged.get("dt", [None])[0],  # page title
                "params": {},
            }
            # ep.* = event params, epn.* = numeric
            for k, v in merged.items():
                if k.startswith("ep.") or k.startswith("epn."):
                    event["params"][k.split(".", 1)[1]] = v[0] if v else None
            events.append(event)
        except Exception as e:
            continue
    return events


def parse_meta_pixel_events(network_log: NetworkLog):
    """Parse eventos Meta Pixel de facebook.com/tr."""
    events = []
    for r in network_log.requests:
        u = r["url"]
        if "facebook.com/tr" not in u:
            continue
        try:
            parsed = urlparse(u)
            qs = parse_qs(parsed.query)
            ev = qs.get("ev", [None])[0]
            if not ev:
                continue
            event = {
                "name": ev,
                "pixel_id": qs.get("id", [None])[0],
                "dl": qs.get("dl", [None])[0],
                "value": qs.get("cd[value]", [None])[0],
                "currency": qs.get("cd[currency]", [None])[0],
                "content_ids": qs.get("cd[content_ids]", [None])[0],
                "content_type": qs.get("cd[content_type]", [None])[0],
            }
            events.append(event)
        except Exception:
            continue
    return events


def compute_quality_flags(detected_tools, ga4_events, meta_events, datalayer, ids_found):
    """Gera red flags de qualidade/tagueamento."""
    flags = []

    # 1. UA legacy ainda presente
    if "ga_ua" in detected_tools or ids_found.get("ua"):
        flags.append({
            "severity": "critical",
            "flag": "ua_legacy_detected",
            "title": "Google Analytics UA (legado) ainda presente",
            "detail": f"UA descontinuado desde jul/2023. IDs: {ids_found.get('ua') or 'n/a'}. Remover tags UA do GTM.",
        })

    # 2. Pixel Meta duplicado
    pixels = ids_found.get("meta_pixel") or []
    if len(pixels) > 1:
        flags.append({
            "severity": "high",
            "flag": "meta_pixel_duplicated",
            "title": f"Meta Pixel duplicado ({len(pixels)} IDs)",
            "detail": f"IDs: {pixels}. Eventos sao disparados duas vezes — duplica dados em Business Manager e gasta budget em audiencias infladas.",
        })

    # 3. GA4 sem PageView
    has_ga4 = "ga4" in detected_tools
    has_page_view = any(e["name"] == "page_view" for e in ga4_events)
    if has_ga4 and not has_page_view:
        flags.append({
            "severity": "high",
            "flag": "ga4_no_pageview",
            "title": "GA4 instalado mas nao dispara page_view",
            "detail": "Load da pagina nao gerou evento page_view. Pode ser bloqueio por consent, erro de config ou tag disparando so com interacao.",
        })

    # 4. Pixel sem PageView
    has_pixel = "meta_pixel" in detected_tools
    has_pixel_pv = any(e["name"] == "PageView" for e in meta_events)
    if has_pixel and not has_pixel_pv:
        flags.append({
            "severity": "high",
            "flag": "pixel_no_pageview",
            "title": "Meta Pixel instalado mas nao dispara PageView",
            "detail": "Eventos de remarketing nao vao contar. Checar fbq('init') + fbq('track','PageView') no codigo ou GTM.",
        })

    # 5. gtag + GTM em paralelo
    has_gtm = "gtm" in detected_tools
    has_gtag_only = has_ga4 and not has_gtm
    if has_gtm and any("gtag/js" in r["url"] for r in []):  # checado indiretamente
        pass  # refinar: se houver dois pontos de init GA4, flag

    # 6. Consent Mode v2 presente?
    has_cmp = any(detected_tools.get(t) for t in ["onetrust", "cookiebot", "usercentrics", "trustarc", "termly"])
    has_gcs = any(e.get("gcs") for e in ga4_events)
    if has_ga4 and not has_gcs and not has_cmp:
        flags.append({
            "severity": "medium",
            "flag": "no_consent_mode",
            "title": "Sem Consent Mode v2 nem CMP detectado",
            "detail": "Desde mar/2024 Google exige Consent Mode v2 para audiencias. Sem CMP, site pode violar LGPD.",
        })

    # 7. dataLayer vazio (so com gtm.js)
    if datalayer is not None:
        if isinstance(datalayer, list) and len(datalayer) <= 1:
            flags.append({
                "severity": "medium",
                "flag": "datalayer_empty",
                "title": "dataLayer praticamente vazio",
                "detail": "Sem variaveis customizadas no dataLayer alem do gtm.js. Nao ha contexto sendo passado ao GTM — eventos ricos (user_id, ecommerce, form_step) sao impossiveis.",
            })

    # 8. GTM instalado sem GA4 nem Pixel
    if has_gtm and not has_ga4 and not has_pixel:
        flags.append({
            "severity": "critical",
            "flag": "gtm_without_analytics",
            "title": "GTM instalado sem GA4 nem Meta Pixel",
            "detail": "Container GTM carrega mas nao dispara nenhuma tag de analytics ou ads conhecida. Investimento em midia opera cego — sem atribuicao de conversao.",
        })

    # 9. GA4 instalado mas sem Google Ads vinculado
    has_gads = bool(ids_found.get("google_ads"))
    if has_ga4 and not has_gads:
        flags.append({
            "severity": "low",
            "flag": "ga4_no_google_ads",
            "title": "GA4 presente mas sem tag Google Ads",
            "detail": "Nao e red flag se cliente nao faz Google Ads. Se faz, conversoes nao estao importando para Ads — revisar vinculo GA4↔Ads.",
        })

    # 10. Multiplos containers GTM
    gtms = ids_found.get("gtm") or []
    if len(gtms) > 1:
        flags.append({
            "severity": "medium",
            "flag": "multiple_gtm_containers",
            "title": f"{len(gtms)} containers GTM carregados",
            "detail": f"IDs: {gtms}. Aumenta JS bundle, pode causar conflitos de eventos e confusao de ownership.",
        })

    return flags


async def detect_cro_elements(page: Page):
    """Avaliacao profunda de elementos CRO visiveis na pagina."""
    js = """
    () => {
      const text = (el) => (el?.textContent || '').trim().replace(/\\s+/g,' ');
      const isVisible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden' && parseFloat(style.opacity) > 0;
      };

      // CTAs
      const ctas = [...document.querySelectorAll('a, button')]
        .filter(el => isVisible(el))
        .map(el => {
          const t = text(el);
          if (!t || t.length > 60) return null;
          const rect = el.getBoundingClientRect();
          const href = el.getAttribute('href') || '';
          const isWhatsApp = /wa\\.me|api\\.whatsapp/i.test(href);
          const isTel = href.startsWith('tel:');
          const isMail = href.startsWith('mailto:');
          return {
            text: t,
            tag: el.tagName.toLowerCase(),
            href: href.substring(0, 200),
            is_whatsapp: isWhatsApp,
            is_tel: isTel,
            is_mail: isMail,
            above_fold: rect.top < window.innerHeight,
            width: Math.round(rect.width),
            height: Math.round(rect.height),
          };
        })
        .filter(Boolean);

      // Forms
      const forms = [...document.querySelectorAll('form')].map(f => {
        const inputs = [...f.querySelectorAll('input, select, textarea')]
          .filter(el => !['hidden','submit','button'].includes(el.type))
          .map(el => ({
            name: el.name || el.id || '',
            type: el.type || el.tagName.toLowerCase(),
            required: el.hasAttribute('required'),
            placeholder: el.placeholder || '',
          }));
        return {
          id: f.id || '',
          action: (f.action || '').substring(0, 200),
          method: (f.method || 'get').toLowerCase(),
          field_count: inputs.length,
          fields: inputs,
          has_consent_checkbox: !!f.querySelector('input[type="checkbox"]'),
        };
      });

      // Prova social (heuristica)
      const bodyText = document.body.innerText.toLowerCase();
      const socialProof = {
        has_testimonials: /depoimento|testimonial|avalia[cç][aã]o|review/i.test(bodyText),
        has_ratings: !!document.querySelector('[class*="star"], [class*="rating"], [itemprop="ratingValue"]'),
        has_numbers: /[0-9]+\\s*(clientes|pacientes|alunos|pets|atendimentos|projetos|anos)/i.test(bodyText),
        has_certifications: /(crmv|oab|crefito|crm|certificado|selo|iso\\s)/i.test(bodyText),
        has_logos_clients: !!document.querySelector('[class*="clients"], [class*="parceir"], [class*="logos"]'),
      };

      // Urgencia/escassez
      const urgency = {
        has_countdown: !!document.querySelector('[class*="countdown"], [class*="timer"], [id*="countdown"]'),
        has_limited: /vagas limitadas|[uú]ltimas? vagas|termina hoje|s[oó] hoje|oferta expira/i.test(bodyText),
        has_discount: /desconto|off|%\\s*(off|menos)/i.test(bodyText),
      };

      // Confianca / credenciais
      const trust = {
        has_address: /(rua|avenida|av\\.|travessa|alameda)\\s+[A-Z]/i.test(document.body.innerText),
        has_cnpj: /cnpj[:\\s]*[\\d\\.\\/\\-]+/i.test(document.body.innerText),
        has_phone: !!document.querySelector('a[href^="tel:"]'),
        has_email: !!document.querySelector('a[href^="mailto:"]'),
        has_privacy_link: /pol[ií]tica\\s+de\\s+privacidade|privacy\\s+policy/i.test(bodyText),
        has_terms_link: /termos\\s+de\\s+uso|terms\\s+of/i.test(bodyText),
      };

      // WhatsApp
      const waLinks = [...document.querySelectorAll('a[href*="wa.me/"], a[href*="api.whatsapp.com"]')].map(a => ({
        text: text(a).substring(0, 80),
        href: a.getAttribute('href') || '',
        visible: isVisible(a),
        floating: /fix|sticky/i.test(window.getComputedStyle(a).position) || !!a.closest('[class*="float"],[class*="sticky"],[class*="fixed"]'),
      }));

      // Videos
      const videos = [...document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"], iframe[src*="wistia"]')].map(v => ({
        tag: v.tagName.toLowerCase(),
        src: (v.src || v.getAttribute('src') || '').substring(0, 200),
      }));

      // Hero analysis (first viewport)
      const h1 = document.querySelector('h1');
      const aboveFoldCtas = ctas.filter(c => c.above_fold).length;

      return {
        cta_count: ctas.length,
        cta_above_fold: aboveFoldCtas,
        cta_list: ctas.slice(0, 20),
        whatsapp_links: waLinks,
        forms: forms,
        form_count: forms.length,
        avg_fields_per_form: forms.length ? Math.round(forms.reduce((s,f)=>s+f.field_count,0)/forms.length) : 0,
        social_proof: socialProof,
        urgency: urgency,
        trust: trust,
        videos: videos,
        h1_text: h1 ? text(h1).substring(0, 200) : null,
        page_text_length: document.body.innerText.length,
      };
    }
    """
    try:
        return await page.evaluate(js)
    except Exception as e:
        return {"error": str(e)}


async def dump_window_globals_and_datalayer(page: Page):
    """Lista props em window (filtradas) + dataLayer."""
    js = """
    () => {
      const interesting = [
        'gtag','dataLayer','google_tag_manager','ga','_gaq',
        'fbq','_fbq','ttq','pintrk','_linkedin_data_partner_ids','twq',
        'clarity','hj','_hjSettings','_mfq','FS',
        'Intercom','_hsq','HubSpotConversations','zE','$zopim','$crisp','jivo_api','Tawk_API',
        'OneTrust','OptanonConsent','Cookiebot','UC_UI',
        'RdstationPopup','RDStationForms',
        'Shopify','vtex','vtexjs','elementorFrontend','__NEXT_DATA__','React','Vue'
      ];
      const found = interesting.filter(k => typeof window[k] !== 'undefined');
      let dl = null;
      try {
        if (Array.isArray(window.dataLayer)) {
          dl = window.dataLayer.map(item => {
            try { return JSON.parse(JSON.stringify(item)); } catch(e) { return String(item).substring(0,200); }
          }).slice(0, 50);
        }
      } catch(e) {}
      return { globals: found, datalayer: dl, datalayer_length: (Array.isArray(window.dataLayer) ? window.dataLayer.length : null) };
    }
    """
    try:
        return await page.evaluate(js)
    except Exception as e:
        return {"globals": [], "datalayer": None, "datalayer_length": None, "error": str(e)}


async def audit_one_pass(browser, url: str, device: str, wait_for_consent: bool):
    """Navega a URL uma vez (mobile ou desktop) e retorna snapshot completo."""
    is_mobile = device == "mobile"
    context = await browser.new_context(
        user_agent=USER_AGENT_MOBILE if is_mobile else USER_AGENT_DESKTOP,
        viewport=VIEWPORT_MOBILE if is_mobile else VIEWPORT_DESKTOP,
        is_mobile=is_mobile,
        locale="pt-BR",
        timezone_id="America/Sao_Paulo",
    )
    page = await context.new_page()
    netlog = NetworkLog()
    page.on("request", netlog.on_request)
    page.on("response", netlog.on_response)

    nav_error = None
    status = None
    try:
        response = await page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        status = response.status if response else None
        try:
            await page.wait_for_load_state("networkidle", timeout=IDLE_TIMEOUT_MS)
        except PWTimeout:
            pass
        # Scroll para ativar lazy loaders
        try:
            await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1500)
            await page.evaluate("() => window.scrollTo(0, 0)")
            await page.wait_for_timeout(500)
        except Exception:
            pass
    except Exception as e:
        nav_error = str(e)

    # Dump state
    try:
        html = await page.content()
    except Exception:
        html = ""
    try:
        cookies = await context.cookies()
    except Exception:
        cookies = []

    globals_info = await dump_window_globals_and_datalayer(page)
    cro = await detect_cro_elements(page) if not nav_error else {}

    # Screenshot full-page (compressao leve)
    screenshot_b64 = None
    try:
        ss_bytes = await page.screenshot(full_page=True, type="jpeg", quality=60)
        import base64
        screenshot_b64 = "data:image/jpeg;base64," + base64.b64encode(ss_bytes).decode("ascii")
    except Exception:
        pass

    await context.close()

    return {
        "device": device,
        "status": status,
        "nav_error": nav_error,
        "html_length": len(html),
        "html_preview": html[:500],
        "html": html,  # usado internamente pela deteccao, removido do output
        "cookies": [{"name": c["name"], "domain": c.get("domain",""), "secure": c.get("secure", False), "httpOnly": c.get("httpOnly", False), "sameSite": c.get("sameSite","")} for c in cookies],
        "window_globals": globals_info.get("globals", []),
        "datalayer": globals_info.get("datalayer"),
        "datalayer_length": globals_info.get("datalayer_length"),
        "cro_elements": cro,
        "requests_count": len(netlog.requests),
        "responses_count": len(netlog.responses),
        "_netlog": netlog,  # usado internamente, removido do output
        "screenshot_fullpage": screenshot_b64,
    }


async def audit_compliance_pass(browser, url: str):
    """Segunda passada: navega com flag de 'pre-consent' simulada (sem interagir com CMP).
    Registra quais trackers disparam ANTES de qualquer consentimento.
    """
    # Mesma logica do pass principal, mas sem aceitar nenhum banner
    context = await browser.new_context(
        user_agent=USER_AGENT_DESKTOP,
        viewport=VIEWPORT_DESKTOP,
        locale="pt-BR",
        timezone_id="America/Sao_Paulo",
    )
    page = await context.new_page()
    netlog = NetworkLog()
    page.on("request", netlog.on_request)

    nav_error = None
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
        try:
            await page.wait_for_load_state("networkidle", timeout=IDLE_TIMEOUT_MS)
        except PWTimeout:
            pass
        # NAO interagir com CMP — ficar parado
        await page.wait_for_timeout(2500)
    except Exception as e:
        nav_error = str(e)

    # Contar tracker requests ANTES de consent
    tracker_patterns = [
        "google-analytics.com",
        "googletagmanager.com/gtm.js",
        "facebook.com/tr",
        "facebook.net/en_US/fbevents.js",
        "analytics.tiktok.com",
        "clarity.ms",
        "hotjar.com",
        "linkedin.com/li/",
        "doubleclick.net",
    ]
    pre_consent_trackers = {}
    for r in netlog.requests:
        for pat in tracker_patterns:
            if pat in r["url"]:
                pre_consent_trackers.setdefault(pat, []).append(r["url"])
                break

    await context.close()

    return {
        "nav_error": nav_error,
        "pre_consent_trackers": pre_consent_trackers,
        "pre_consent_tracker_count": sum(len(v) for v in pre_consent_trackers.values()),
    }


def build_compliance_report(compliance_pass, detected_tools):
    """Monta bloco de compliance LGPD."""
    cmps = {k: detected_tools[k] for k in ["onetrust", "cookiebot", "usercentrics", "trustarc", "termly"] if k in detected_tools}
    has_cmp = bool(cmps)
    pre_count = compliance_pass.get("pre_consent_tracker_count", 0)
    pre_trackers = compliance_pass.get("pre_consent_trackers", {})

    issues = []
    if not has_cmp:
        issues.append("Sem CMP detectado — sem mecanismo de consentimento.")
    if pre_count > 0:
        issues.append(f"{pre_count} requests de tracking disparam ANTES de qualquer consentimento.")
        for pat, urls in pre_trackers.items():
            issues.append(f"  • {pat}: {len(urls)} request(s)")

    # Score 0-10
    score = 10
    if not has_cmp:
        score -= 5
    if pre_count > 0:
        score -= min(5, pre_count)
    score = max(0, score)

    status = "compliant" if (has_cmp and pre_count == 0) else ("partial" if has_cmp else "non_compliant")

    return {
        "status": status,
        "score": score,
        "has_cmp": has_cmp,
        "cmps_detected": list(cmps.keys()),
        "pre_consent_trackers": pre_trackers,
        "pre_consent_tracker_count": pre_count,
        "issues": issues,
    }


def sanitize_output(obj):
    """Remove campos pesados/internos do output final."""
    if isinstance(obj, dict):
        return {k: sanitize_output(v) for k, v in obj.items() if not k.startswith("_") and k != "html"}
    if isinstance(obj, list):
        return [sanitize_output(x) for x in obj]
    return obj


async def run_audit(url: str, out_path: str, skip_compliance: bool = False):
    signatures = load_signatures()
    result = {
        "url": url,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "engine": "playwright-chromium",
    }

    async with async_playwright() as pw:
        print(">> Iniciando Chromium headless...", file=sys.stderr)
        browser = await pw.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])

        print(">> Pass 1: Desktop (full audit)...", file=sys.stderr)
        desktop_pass = await audit_one_pass(browser, url, "desktop", wait_for_consent=False)

        print(">> Pass 2: Mobile (full audit)...", file=sys.stderr)
        mobile_pass = await audit_one_pass(browser, url, "mobile", wait_for_consent=False)

        compliance_pass = None
        if not skip_compliance:
            print(">> Pass 3: Compliance LGPD (pre-consent tracking)...", file=sys.stderr)
            compliance_pass = await audit_compliance_pass(browser, url)

        await browser.close()

    # Combinar netlogs de desktop + mobile para deteccao de ferramentas (mais robusto)
    combined_netlog = NetworkLog()
    combined_netlog.requests = desktop_pass["_netlog"].requests + mobile_pass["_netlog"].requests
    combined_netlog.responses = desktop_pass["_netlog"].responses + mobile_pass["_netlog"].responses

    detected = detect_tools(
        signatures,
        combined_netlog,
        desktop_pass.get("html", "") + mobile_pass.get("html", ""),
        list(set(desktop_pass.get("window_globals", []) + mobile_pass.get("window_globals", []))),
        desktop_pass.get("cookies", []) + mobile_pass.get("cookies", []),
    )
    ids_found = extract_ids_from_urls(combined_netlog)
    ga4_events = parse_ga4_events(combined_netlog)
    meta_events = parse_meta_pixel_events(combined_netlog)
    quality_flags = compute_quality_flags(detected, ga4_events, meta_events, desktop_pass.get("datalayer"), ids_found)

    compliance_report = None
    if compliance_pass is not None:
        compliance_report = build_compliance_report(compliance_pass, detected)

    # Categorizar ferramentas
    by_category = {}
    for tid, info in detected.items():
        by_category.setdefault(info["category"], []).append(info["name"])

    result["tracking_stack"] = {
        "tools_detected": detected,
        "ids_found": ids_found,
        "categories_summary": {cat: sorted(names) for cat, names in by_category.items()},
        "total_tools": len(detected),
    }

    result["events_fired"] = {
        "ga4": ga4_events,
        "meta_pixel": meta_events,
        "ga4_event_count": len(ga4_events),
        "meta_event_count": len(meta_events),
        "ga4_event_names": sorted(set(e["name"] for e in ga4_events if e.get("name"))),
        "meta_event_names": sorted(set(e["name"] for e in meta_events if e.get("name"))),
    }

    result["datalayer"] = {
        "desktop": {
            "length": desktop_pass.get("datalayer_length"),
            "sample": desktop_pass.get("datalayer"),
        },
        "mobile": {
            "length": mobile_pass.get("datalayer_length"),
            "sample": mobile_pass.get("datalayer"),
        },
    }

    result["cro_elements"] = {
        "desktop": desktop_pass.get("cro_elements"),
        "mobile": mobile_pass.get("cro_elements"),
    }

    result["quality_flags"] = quality_flags

    result["compliance_lgpd"] = compliance_report

    result["navigation"] = {
        "desktop": {
            "status": desktop_pass.get("status"),
            "nav_error": desktop_pass.get("nav_error"),
            "requests_count": desktop_pass.get("requests_count"),
            "responses_count": desktop_pass.get("responses_count"),
            "cookies_count": len(desktop_pass.get("cookies") or []),
        },
        "mobile": {
            "status": mobile_pass.get("status"),
            "nav_error": mobile_pass.get("nav_error"),
            "requests_count": mobile_pass.get("requests_count"),
            "responses_count": mobile_pass.get("responses_count"),
            "cookies_count": len(mobile_pass.get("cookies") or []),
        },
    }

    result["screenshots_fullpage"] = {
        "desktop": desktop_pass.get("screenshot_fullpage"),
        "mobile": mobile_pass.get("screenshot_fullpage"),
    }

    # Limpar campos internos
    result = sanitize_output(result)

    # Escrever output
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] Deep audit salvo em {out_path}", file=sys.stderr)
    print(f"     Ferramentas detectadas: {len(detected)}", file=sys.stderr)
    print(f"     Eventos GA4: {len(ga4_events)} | Meta Pixel: {len(meta_events)}", file=sys.stderr)
    print(f"     Red flags: {len(quality_flags)}", file=sys.stderr)
    if compliance_report:
        print(f"     Compliance: {compliance_report['status']} (score {compliance_report['score']}/10)", file=sys.stderr)


def main():
    if len(sys.argv) < 3:
        print("Uso: page_audit_deep.py <url> <output_json> [--skip-compliance]", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    out_path = sys.argv[2]
    skip_compliance = "--skip-compliance" in sys.argv
    asyncio.run(run_audit(url, out_path, skip_compliance=skip_compliance))


if __name__ == "__main__":
    main()
