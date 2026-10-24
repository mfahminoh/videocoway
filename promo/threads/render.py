"""Render poster Threads (1080x1350) daripada posters.html -> promo/threads/out/<id>.png

    python promo/threads/render.py
"""
import pathlib

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto((HERE / "posters.html").as_uri())
    pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready")
    OUT.mkdir(exist_ok=True)
    for el in pg.query_selector_all(".poster"):
        pid = el.get_attribute("id")
        el.screenshot(path=str(OUT / f"{pid}.png"))
        print(pid)
    b.close()
