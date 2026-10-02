"""Render an animation page (src/*.html) frame-by-frame into a 1080x1920 MP4.

Usage:
  python render.py                                  # 30s version -> out/villaem3_video_noaudio.mp4
  python render.py --src long.html --out out/villaem3_long_noaudio.mp4 --jobs 4
  python render.py --src long.html --stills 1,5.5,10  # PNG previews -> out/stills/
  python render.py --src long.html --warp out/warp_long.json --out out/villaem3_long_video_noaudio.mp4 --jobs 4
                                                    # retimed to a real voiceover
"""
import argparse
import json
import multiprocessing as mp
import pathlib
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
W, H = 1080, 1920
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)
FF = imageio_ffmpeg.get_ffmpeg_exe()


def open_page(p, src):
    browser = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto((ROOT / "src" / src).as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].every(i => i.complete)")
    return browser, page


def stills(src, times, prefix=""):
    out = ROOT / "out" / "stills"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser, page = open_page(p, src)
        for t in times:
            page.evaluate(f"seek({t})")
            page.screenshot(path=str(out / f"{prefix}t{t:06.2f}.png"))
        browser.close()


def duration(src):
    with sync_playwright() as p:
        browser, page = open_page(p, src)
        d = page.evaluate("window.DURATION")
        browser.close()
    return d


def anim_time(i, warp):
    t = i / FPS
    if not warp:
        return t
    import numpy as np
    return float(np.interp(t, warp["out"], warp["anim"]))


def render_range(args):
    src, start, end, path, warp = args
    proc = subprocess.Popen(
        [FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(path)],
        stdin=subprocess.PIPE,
    )
    with sync_playwright() as p:
        browser, page = open_page(p, src)
        for i in range(start, end):
            page.evaluate(f"seek({anim_time(i, warp)})")
            proc.stdin.write(page.screenshot(type="png"))
            if (i - start) % 150 == 0:
                print(f"[{start}-{end}] frame {i}", flush=True)
        browser.close()
    proc.stdin.close()
    proc.wait()
    return path


def video(src, path, jobs, warp=None):
    n = int(round((warp["duration"] if warp else duration(src)) * FPS))
    tmp = ROOT / "out" / "_parts"
    tmp.mkdir(parents=True, exist_ok=True)
    bounds = [round(n * k / jobs) for k in range(jobs + 1)]
    parts = [(src, bounds[k], bounds[k + 1], tmp / f"part{k}.mp4", warp) for k in range(jobs)]
    with mp.Pool(jobs) as pool:
        files = pool.map(render_range, parts)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-movflags", "+faststart", str(path)], check=True)
    for f in files:
        f.unlink()
    lst.unlink()
    print("wrote", path, f"({n} frames)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="index.html")
    ap.add_argument("--stills")
    ap.add_argument("--out", default=str(ROOT / "out" / "villaem3_video_noaudio.mp4"))
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--warp", help="JSON time map from voiceover/retime_long.py")
    a = ap.parse_args()
    if a.stills:
        stills(a.src, [float(x) for x in a.stills.split(",")], prefix=pathlib.Path(a.src).stem + "_")
    else:
        video(a.src, a.out, a.jobs, json.loads(pathlib.Path(a.warp).read_text()) if a.warp else None)
