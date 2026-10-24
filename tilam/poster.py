"""Poster Threads (1080x1350) dari frame penting video -> out/poster/<vid>_poster_threads.png

    python tilam/poster.py h01
    python tilam/poster.py p01
    python tilam/poster.py pakej    # mozek kulit semua video + teks pakej (src/poster/pakej.html)
Frame diambil terus dari video siap. Susun atur & teks: src/poster/<vid>.html (imej: out/poster/_frames/<vid>_<masa>.png).
"""
import json, pathlib, subprocess, sys

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
import render  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

VIDS = {
    # penat · hotel · fabrik penyejuk · topper nipis/tebal · ketebalan · bercuti
    "h01": ("out/tilam/h01_topper-fabrik-sejuk-gebu-macam-hotel.mp4", ["05", "19.5", "45", "63.5", "87", "96"]),
    # spring biasa · spring berpoket · bentuk badan · gelas air · zon · 5/7/9 zon
    "p01": ("out/tilam/p01_cara-spring-berpoket-berfungsi.mp4", ["17.8", "29.8", "40.3", "46.3", "55", "63.3"]),
}
OUT = R / "out/poster"


def covers(fr):
    """Kulit setiap video = frame hook pada 1.5s. Disusun bergilir ikut siri supaya mozek bercampur."""
    vids = sorted((R / "out/tilam").glob("*.mp4")) + [R / "out/tilam/gaya/e02_kinetic.mp4", R / "out/tilam/gaya/e05_berita.mp4"]
    names = []
    for v in vids:
        n = f"cover_{v.stem}.jpg"; names.append(n)
        if not (fr / n).exists():
            subprocess.run([render.FF, "-v", "error", "-y", "-ss", "1.5", "-i", str(v), "-frames:v", "1", "-vf", "scale=270:480", "-q:v", "3", str(fr / n)], check=True)
    groups = {}
    for n in names: groups.setdefault(n[6], []).append(n)       # huruf siri: b c d e h l p s v
    mixed = []
    while any(groups.values()):
        for k in sorted(groups):
            if groups[k]: mixed.append(groups[k].pop(0))
    (fr / "covers.js").write_text("window.COVERS = " + json.dumps(mixed) + ";\n")


def main(vid):
    fr = OUT / "_frames"; fr.mkdir(parents=True, exist_ok=True)
    if vid == "pakej":
        covers(fr)
    else:
        video, times = VIDS[vid]
        for t in times:
            subprocess.run([render.FF, "-v", "error", "-y", "-ss", t, "-i", str(R / video), "-frames:v", "1", str(fr / f"{vid}_{t}.png")], check=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=render.CHROMIUM) if render.CHROMIUM else p.chromium.launch()
        page = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        page.goto((R / "src/poster" / f"{vid}.html").as_uri())
        page.evaluate("document.fonts.ready")
        page.wait_for_function("[...document.images].every(i => i.complete)")
        out = OUT / f"{vid}_poster_threads.png"
        page.screenshot(path=str(out)); b.close()
    print("siap:", out)


if __name__ == "__main__":
    for v in sys.argv[1:] or [*VIDS, "pakej"]: main(v)
