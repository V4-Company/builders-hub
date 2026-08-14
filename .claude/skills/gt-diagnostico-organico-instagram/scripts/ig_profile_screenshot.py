"""
ig_profile_screenshot.py — Captura print do header do perfil Instagram para embed no portal.

Uso:
    python3 ig_profile_screenshot.py <client_dir> --usernames user1,user2,user3
    python3 ig_profile_screenshot.py <client_dir>   # le de outputs/gt-diagnostico-organico-instagram.json

Saida:
    <client_dir>/assets/instagram/<username>.png
    Atualiza outputs/gt-diagnostico-organico-instagram.json com profile_screenshot_data_uri nos accounts.
"""
import asyncio
import argparse
import base64
import json
import sys
from pathlib import Path

from playwright.async_api import async_playwright


async def snap(page, username, out_path):
    url = f"https://www.instagram.com/{username}/"
    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    await asyncio.sleep(4)
    for sel in [
        'div[role="dialog"] button[aria-label="Close"]',
        'svg[aria-label="Close"]',
        'button[aria-label="Close"]',
    ]:
        try:
            el = await page.query_selector(sel)
            if el:
                await el.click()
                break
        except Exception:
            pass
    await asyncio.sleep(1)
    header = await page.query_selector("header")
    if not header:
        return False
    await header.screenshot(path=str(out_path))
    return True


async def run(client_dir: Path, usernames: list[str]):
    assets_dir = client_dir / "assets" / "instagram"
    assets_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
        )
        page = await ctx.new_page()
        for username in usernames:
            username = username.strip().lstrip("@")
            if not username:
                continue
            out = assets_dir / f"{username}.png"
            try:
                ok = await snap(page, username, out)
                if ok and out.exists():
                    data = out.read_bytes()
                    uri = f"data:image/png;base64,{base64.b64encode(data).decode('ascii')}"
                    results[username] = {"path": str(out.relative_to(client_dir)), "data_uri": uri, "bytes": len(data)}
                    print(f"OK  @{username}: {len(data)} bytes -> {out}")
                else:
                    print(f"FAIL @{username}: header nao encontrado", file=sys.stderr)
            except Exception as e:
                print(f"FAIL @{username}: {e}", file=sys.stderr)
        await browser.close()
    return results


def update_output(client_dir: Path, results: dict):
    out_path = client_dir / "outputs" / "gt-diagnostico-organico-instagram.json"
    if not out_path.exists():
        return
    with out_path.open() as f:
        d = json.load(f)
    accounts = [d.get("client_account") or {}] + list(d.get("competitor_accounts") or [])
    for a in accounts:
        if not a:
            continue
        u = (a.get("username") or "").lstrip("@")
        if u in results:
            a["profile_screenshot_data_uri"] = results[u]["data_uri"]
            a["profile_screenshot_path"] = results[u]["path"]
    with out_path.open("w") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"Atualizado {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("client_dir", type=Path)
    ap.add_argument("--usernames", type=str, default="")
    args = ap.parse_args()

    if args.usernames:
        usernames = [u.strip() for u in args.usernames.split(",") if u.strip()]
    else:
        out = args.client_dir / "outputs" / "gt-diagnostico-organico-instagram.json"
        if not out.exists():
            print("ERROR: --usernames nao fornecido e nao ha gt-diagnostico-organico-instagram.json", file=sys.stderr)
            sys.exit(1)
        with out.open() as f:
            d = json.load(f)
        usernames = []
        c = d.get("client_account")
        if c and c.get("username"):
            usernames.append(c["username"])
        for comp in d.get("competitor_accounts") or []:
            if comp.get("username"):
                usernames.append(comp["username"])

    if not usernames:
        print("ERROR: nenhum username para capturar", file=sys.stderr)
        sys.exit(1)

    print(f"Capturando {len(usernames)} perfis: {', '.join('@'+u for u in usernames)}")
    results = asyncio.run(run(args.client_dir, usernames))
    if results:
        update_output(args.client_dir, results)


if __name__ == "__main__":
    main()
