"""Poster Threads (1080x1350) dari frame penting video H01 -> out/poster/h01_poster_threads.png

    python tilam/poster_h01.py
Frame diambil terus dari video siap (out/tilam/h01_*.mp4). Susun atur & teks: src/poster/h01.html.
"""
import pathlib, subprocess, sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
import render  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

VIDEO = R / "out/tilam/h01_topper-fabrik-sejuk-gebu-macam-hotel.mp4"
TIMES = ["05", "19.5", "45", "63.5", "87", "96"]   # penat · hotel · fabrik penyejuk · topper nipis/tebal · ketebalan · bercuti
OUT = R / "out/poster"


def main():
    fr = OUT / "_frames"; fr.mkdir(parents=True, exist_ok=True)
    for t in TIMES:
        subprocess.run([render.FF, "-v", "error", "-y", "-ss", t, "-i", str(VIDEO), "-frames:v", "1", str(fr / f"h01_{t}.png")], check=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=render.CHROMIUM) if render.CHROMIUM else p.chromium.launch()
        page = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.goto((R / "src/poster/h01.html").as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_function("[...document.images].every(i => i.complete)")
        out = OUT / "h01_poster_threads.png"
        page.screenshot(path=str(out)); b.close()
    print("siap:", out)


if __name__ == "__main__":
    main()
