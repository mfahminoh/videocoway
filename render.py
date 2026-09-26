"""Render src/index.html frame-by-frame into a 1080x1920 MP4.

Usage:
  python render.py                      # full video -> out/villaem3_video_noaudio.mp4 (no audio)
  python render.py --stills 1,5.5,10    # PNG previews -> out/stills/
  python render.py --page neoplus/index.html --out out/neoplus_video_noaudio.mp4
  python render.py --page neoplus_full/index.html --out out/neoplus_full_video_noaudio.mp4 --workers 4
"""
import argparse
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
W, H = 1080, 1920
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)


def open_page(p, page_path):
    browser = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto((ROOT / page_path).resolve().as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
    return browser, page


def stills(times, page_path, out):
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser, page = open_page(p, page_path)
        for t in times:
            page.evaluate(f"seek({t})")
            page.screenshot(path=str(out / f"t{t:05.2f}.png"))
        browser.close()


def video(path, page_path, frames=None):
    """Render frames [a, b) (default: whole video) to an H.264 file."""
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    with sync_playwright() as p:
        browser, page = open_page(p, page_path)
        n = int(round(page.evaluate("window.DURATION") * FPS))
        a, b = frames or (0, n)
        b = min(b, n)
        proc = subprocess.Popen(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
             "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)],
            stdin=subprocess.PIPE,
        )
        for i in range(a, b):
            page.evaluate(f"seek({i / FPS})")
            proc.stdin.write(page.screenshot(type="png"))
            if (i - a) % 90 == 0:
                print(f"frame {i}/{n}", flush=True)
        proc.stdin.close()
        proc.wait()
        browser.close()
    print("wrote", path)


def video_parallel(path, page_path, workers):
    """Split the video into `workers` chunks rendered by separate processes, then join them losslessly."""
    with sync_playwright() as p:
        browser, page = open_page(p, page_path)
        n = int(round(page.evaluate("window.DURATION") * FPS))
        browser.close()
    tmp = pathlib.Path(path).with_suffix(".parts")
    tmp.mkdir(exist_ok=True)
    step = -(-n // workers)
    parts, procs = [], []
    for k in range(workers):
        part = tmp / f"part{k:02d}.mp4"
        parts.append(part)
        procs.append(subprocess.Popen([sys.executable, __file__, "--page", page_path, "--out", str(part),
                                       "--frames", f"{k * step}:{(k + 1) * step}"]))
    if any(pr.wait() for pr in procs):
        raise SystemExit("a render worker failed")
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{x.resolve()}'\n" for x in parts))
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(path)], check=True)
    for x in [*parts, lst]:
        x.unlink()
    tmp.rmdir()
    print("wrote", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills")
    ap.add_argument("--page", default="src/index.html")
    ap.add_argument("--stills-dir", default=str(ROOT / "out" / "stills"))
    ap.add_argument("--out", default=str(ROOT / "out" / "villaem3_video_noaudio.mp4"))
    ap.add_argument("--workers", type=int, default=1, help="render in N parallel browser processes")
    ap.add_argument("--frames", help="a:b — render only frames a..b-1 (used by --workers)")
    a = ap.parse_args()
    if a.stills:
        stills([float(x) for x in a.stills.split(",")], a.page, pathlib.Path(a.stills_dir))
    elif a.workers > 1:
        video_parallel(a.out, a.page, a.workers)
    else:
        video(a.out, a.page, tuple(map(int, a.frames.split(":"))) if a.frames else None)
