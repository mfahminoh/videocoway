"""Render src/index.html frame-by-frame into a 1080x1920 MP4.

Usage:
  python render.py                      # full video -> out/coway_ice_video_noaudio.mp4 (no audio)
  python render.py --stills 1,5.5,10    # PNG previews -> out/stills/
"""
import argparse
import pathlib
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
W, H = 1080, 1920
CHROMIUM = next((str(x) for x in sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome"))), None)


def open_page(p, page_path):
    browser = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto(pathlib.Path(page_path).resolve().as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].filter(i => i.getAttribute('src')).every(i => i.complete && i.naturalWidth > 0)")
    return browser, page


def stills(times, page_path, out):
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser, page = open_page(p, page_path)
        for t in times:
            page.evaluate(f"render({t})")
            page.screenshot(path=str(out / f"t{t:05.2f}.png"))
        browser.close()


def video(path, page_path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    with sync_playwright() as p:
        browser, page = open_page(p, page_path)
        duration = page.evaluate("window.DURATION")
        n = int(round(duration * FPS))
        proc = subprocess.Popen(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
             "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)],
            stdin=subprocess.PIPE,
        )
        for i in range(n):
            page.evaluate(f"render({i / FPS})")
            proc.stdin.write(page.screenshot(type="png"))
            if i % 90 == 0:
                print(f"frame {i}/{n}", flush=True)
        proc.stdin.close()
        proc.wait()
        browser.close()
    print("wrote", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills")
    ap.add_argument("--page", default=str(ROOT / "src" / "index.html"), help="halaman animasi (cth. reels/reel1.html)")
    ap.add_argument("--stills-dir", default=str(ROOT / "out" / "stills"))
    ap.add_argument("--out", default=str(ROOT / "out" / "coway_ice_video_noaudio.mp4"))
    a = ap.parse_args()
    if a.stills:
        stills([float(x) for x in a.stills.split(",")], a.page, pathlib.Path(a.stills_dir))
    else:
        video(a.out, a.page)
