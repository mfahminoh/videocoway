"""Render poster HTML -> PNG.

    python3 .claude/skills/coway-poster/scripts/render_poster.py projek/<kod>/poster/*.html --out out/<kod>/poster
    python3 .claude/skills/coway-poster/scripts/render_poster.py promo/threads/posters.html --out promo/threads/out

Satu fail HTML boleh ada beberapa poster: setiap elemen `.poster` dengan `id` jadi <id>.png (corak promo/threads).
Tanpa `.poster`, seluruh halaman jadi <nama-fail>.png pada saiz `--size` atau <meta name="poster-size" content="1080x1350">.
Saiz: feed 1080x1350 (lalai) atau 1080x1080, story 1080x1920.
"""
import argparse
import pathlib
import re

from playwright.sync_api import sync_playwright

CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome"),
                                  pathlib.Path("/opt/pw-browsers/chromium")] if x.exists()), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", help="WxH, contohnya 1080x1350")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
        for f in map(pathlib.Path, a.files):
            html = f.read_text(errors="ignore")
            m = re.search(r'name="poster-size"\s+content="(\d+)x(\d+)"', html)
            w, h = map(int, (a.size or (f"{m.group(1)}x{m.group(2)}" if m else "1080x1350")).split("x"))
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto(f.resolve().as_uri())
            pg.wait_for_load_state("networkidle")
            pg.evaluate("document.fonts.ready")
            broken = pg.evaluate("[...document.images].filter(i => !(i.complete && i.naturalWidth)).map(i => i.getAttribute('src'))")
            if broken:
                print(f"  ! {f.name}: gambar tak dapat dimuat: {broken[:5]}")
            posters = pg.query_selector_all(".poster[id]")
            if posters:
                for el in posters:
                    dst = out / f"{el.get_attribute('id')}.png"
                    el.screenshot(path=str(dst))
                    print(dst)
            else:
                dst = out / f"{f.stem}.png"
                pg.screenshot(path=str(dst))
                print(dst)
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
