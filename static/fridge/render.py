"""Render poster static (HTML 1080x1080) -> out/static/*.png.   python static/fridge/render.py [nama.html ...]"""
import pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent.parent / "out" / "static"
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)

files = [HERE / f for f in sys.argv[1:]] or sorted(HERE.glob("poster*.html"))
OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = b.new_page(viewport={"width": 1080, "height": 1080})
    for f in files:
        page.goto(f.as_uri())
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        out = OUT / (f.stem + ".png")
        page.screenshot(path=str(out))
        print(out)
    b.close()
