# -*- coding: utf-8 -*-
"""
Automacao de postagem no Meta Business Suite (Planner) via Playwright + CDP.

Pre-requisito: Chrome aberto com --remote-debugging-port=9222 (ou a porta passada
em --cdp) no perfil de automacao do cliente certo, ja logado no Meta Business
Suite na pagina certa. Use abrir_chrome_automacao.bat / setup_perfil_automacao.bat
pra isso.

Uso:
    python postar_conteudo.py --plan <plano.json> --post <numero> --media-dir <pasta> [--confirm] [--cdp http://127.0.0.1:9222]

Sem --confirm: faz tudo (upload, legenda, data/hora) e para ANTES do clique final
de Programar, tirando um screenshot pra revisao em preview_post<N>.png.
Com --confirm: roda tudo de novo do zero (nao continua de um dry-run anterior) e
clica em Programar/Compartilhar de verdade, fechando os popups de upsell.

Rode duas vezes: primeiro sem --confirm pra revisar a previa, depois com --confirm
pra publicar.
"""
import argparse
import json
import os
import time
from playwright.sync_api import sync_playwright

SCRATCH = os.path.dirname(os.path.abspath(__file__))

MESES_PT = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def get_composer_frame(page, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        for f in page.frames:
            if "composer" in f.url:
                return f
        page.wait_for_timeout(300)
    raise RuntimeError("Frame do composer nao encontrado a tempo. O Chrome esta "
                        "na pagina do Planner do Meta Business Suite, na conta certa?")


def click_widest(locator_set, label=""):
    """Entre varios elementos com o mesmo texto/role, clica no de maior largura
    (evita setinhas de carrossel/paginacao que tem o mesmo texto acessivel)."""
    best, best_w = None, 0
    for i in range(locator_set.count()):
        box = locator_set.nth(i).bounding_box()
        if box and box["width"] > best_w:
            best_w, best = box["width"], i
    if best is None:
        raise RuntimeError(f"Nenhum elemento visivel encontrado para {label}")
    locator_set.nth(best).click()


def upload_media_raw_cdp(ctx, page, composer, button_text, media_path):
    """Upload via CDP puro (DOM.setFileInputFiles), sem limite de tamanho de
    arquivo -- necessario pois arquivos >50MB nao passam pelo set_files normal
    quando conectado via connect_over_cdp."""
    if not os.path.exists(media_path):
        raise FileNotFoundError(f"Arquivo de midia nao encontrado: {media_path}")

    cdp = ctx.new_cdp_session(page)
    captured = {}

    def handler(params):
        captured.update(params)
    cdp.on("Page.fileChooserOpened", handler)
    cdp.send("Page.enable")
    cdp.send("Page.setInterceptFileChooserDialog", {"enabled": True})

    composer.get_by_text(button_text).first.click()
    page.wait_for_timeout(1500)

    if "backendNodeId" not in captured:
        raise RuntimeError("Nao capturou o evento de selecao de arquivo.")

    cdp.send("DOM.setFileInputFiles", {
        "backendNodeId": captured["backendNodeId"],
        "files": [media_path],
    })


def wait_upload_complete(composer, page, max_wait=180):
    """Espera a barra de progresso do upload de video chegar a 100%."""
    start = time.time()
    while time.time() - start < max_wait:
        txt = composer.locator("body").inner_text()
        if "100%" in txt:
            return
        page.wait_for_timeout(2000)


def fill_caption(page, composer, text):
    target = composer.locator("[contenteditable='true']").first
    target.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.wait_for_timeout(200)
    page.keyboard.insert_text(text)
    page.wait_for_timeout(400)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)


def find_calendar_header(composer):
    """Acha o texto do cabecalho do calendario ('julho de 2026') procurando
    por qual nome de mes esta visivel no momento."""
    for idx, nome in enumerate(MESES_PT, start=1):
        loc = composer.get_by_text(f"{nome} de", exact=False)
        cnt = loc.count()
        for i in range(cnt):
            el = loc.nth(i)
            if el.is_visible():
                return idx, el
    return None, None


def navigate_calendar_to_month(composer, page, target_month_idx, target_year):
    """Depois de abrir o calendario, avanca de mes ate bater com o alvo."""
    for _ in range(14):
        current_idx, header_el = find_calendar_header(composer)
        if current_idx is None:
            return
        text = header_el.inner_text().strip()
        if str(target_year) in text and MESES_PT[target_month_idx - 1] in text:
            return
        # o botao "Proximo mes" e um texto de leitor de tela sem tamanho visual
        # (sem aria-label, sem role=button visivel) -- so funciona com force click
        next_btn = composer.get_by_text("Próximo mês", exact=True).first
        next_btn.click(force=True)
        page.wait_for_timeout(400)


def set_date_field(page, composer, input_locator, day, month_idx, year):
    input_locator.click()
    page.wait_for_timeout(500)
    navigate_calendar_to_month(composer, page, month_idx, year)
    composer.get_by_text(str(day), exact=True).first.click()
    page.wait_for_timeout(400)


def set_time_field(page, hora_input, min_input, hour, minute):
    hora_input.click()
    page.keyboard.press("Control+A")
    page.keyboard.type(f"{hour:02d}")
    min_input.click()
    page.keyboard.press("Control+A")
    page.keyboard.type(f"{minute:02d}")


def post_estatico(ctx, page, post, media_path, confirm):
    page.get_by_role("button", name="Criar post").first.click()
    composer = get_composer_frame(page)
    page.wait_for_timeout(1500)

    upload_media_raw_cdp(ctx, page, composer, "Adicionar foto/vídeo", media_path)
    page.wait_for_timeout(4000)

    fill_caption(page, composer, post["legenda"] + "\n\n" + post["hashtags"])
    composer.get_by_text("Detalhes do post", exact=True).click()

    switch = composer.locator("input[aria-label='Definir data e hora']")
    switch.click()
    page.wait_for_timeout(1000)

    year, month, day = post["data"].split("-")
    hour, minute = post["hora"].split(":")
    date_inputs = composer.locator("input")

    set_date_field(page, composer, date_inputs.nth(2), int(day), int(month), int(year))
    set_date_field(page, composer, date_inputs.nth(5), int(day), int(month), int(year))

    horas = composer.locator("input[aria-label='horas']")
    minutos = composer.locator("input[aria-label='minutos']")
    set_time_field(page, horas.nth(0), minutos.nth(0), int(hour), int(minute))
    set_time_field(page, horas.nth(1), minutos.nth(1), int(hour), int(minute))

    page.wait_for_timeout(1000)
    shot = os.path.join(SCRATCH, f"preview_post{post['post']}.png")
    page.screenshot(path=shot)
    print("Preview salvo em:", shot)

    if not confirm:
        print("Rode de novo com --confirm para publicar de fato.")
        return

    click_widest(composer.get_by_role("button", name="Programar"), "Programar")
    page.wait_for_timeout(4000)
    try:
        page.get_by_text("Talvez mais tarde", exact=True).click(timeout=5000)
    except Exception:
        pass
    print(f"POST {post['post']} programado.")


def post_video(ctx, page, post, media_path, confirm):
    caret = page.get_by_role("button").nth(2)
    caret.click()
    page.wait_for_timeout(800)
    page.get_by_text("Criar reel", exact=True).click()
    composer = get_composer_frame(page)
    page.wait_for_timeout(2000)

    upload_media_raw_cdp(ctx, page, composer, "Adicionar vídeo", media_path)
    wait_upload_complete(composer, page)
    page.wait_for_timeout(2000)

    fill_caption(page, composer, post["legenda"] + "\n\n" + post["hashtags"])
    composer.get_by_text("Detalhes do reel", exact=True).click()
    page.wait_for_timeout(500)

    # Criar -> Editar
    click_widest(composer.get_by_role("button", name="Avançar"), "Avancar1")
    page.wait_for_timeout(3000)
    # Editar -> Compartilhar
    click_widest(composer.get_by_role("button", name="Avançar"), "Avancar2")
    page.wait_for_timeout(3000)

    composer.get_by_text("Programar", exact=True).click()
    page.wait_for_timeout(1500)

    year, month, day = post["data"].split("-")
    hour, minute = post["hora"].split(":")
    inputs = composer.locator("input")

    set_date_field(page, composer, inputs.nth(0), int(day), int(month), int(year))
    set_date_field(page, composer, inputs.nth(3), int(day), int(month), int(year))
    set_time_field(page, inputs.nth(1), inputs.nth(2), int(hour), int(minute))
    set_time_field(page, inputs.nth(4), inputs.nth(5), int(hour), int(minute))

    page.wait_for_timeout(1000)
    shot = os.path.join(SCRATCH, f"preview_post{post['post']}.png")
    page.screenshot(path=shot)
    print("Preview salvo em:", shot)

    if not confirm:
        print("Rode de novo com --confirm para publicar de fato.")
        return

    click_widest(composer.get_by_role("button", name="Programar"), "ProgramarFinal")
    page.wait_for_timeout(4000)
    try:
        page.get_by_text("Concluir", exact=True).click(timeout=5000)
    except Exception:
        pass
    print(f"POST {post['post']} (reel) programado.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True, help="Caminho pro plano.json do lote")
    ap.add_argument("--post", required=True, type=int, help="Numero do post dentro do plano")
    ap.add_argument("--media-dir", required=True, help="Pasta onde estao os arquivos de midia")
    ap.add_argument("--confirm", action="store_true", help="Clica em Programar de verdade (sem isso, so gera preview)")
    ap.add_argument("--cdp", default="http://127.0.0.1:9222", help="Endereco do endpoint CDP do Chrome")
    args = ap.parse_args()

    with open(args.plan, encoding="utf-8") as f:
        plan = json.load(f)
    try:
        post = next(p for p in plan["posts"] if p["post"] == args.post)
    except StopIteration:
        nums = [p["post"] for p in plan["posts"]]
        raise SystemExit(f"Post {args.post} nao existe no plano. Numeros disponiveis: {nums}")
    media_path = os.path.join(args.media_dir, post["arquivo"])

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(args.cdp)
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        page.bring_to_front()

        if "content_calendar" not in page.url:
            page.goto("https://business.facebook.com/latest/content_calendar",
                      wait_until="domcontentloaded")
            page.wait_for_timeout(2500)

        if post["tipo"] == "VIDEO":
            post_video(ctx, page, post, media_path, args.confirm)
        else:
            post_estatico(ctx, page, post, media_path, args.confirm)

        browser.close()


if __name__ == "__main__":
    main()
