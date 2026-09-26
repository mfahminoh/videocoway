"""Render src/index.html frame-by-frame into a 1080x1920 MP4.

Usage:
  python render.py                      # Villaem 3 ad -> out/villaem3_video_noaudio.mp4 (no audio)
  python render.py --ad best3           # 3-model ad (src/best3.html) -> out/best3_video_noaudio.mp4
  python render.py --stills 1,5.5,10    # PNG previews -> out/stills/
"""
import argparse
import json
import pathlib
import subprocess

import imageio_ffmpeg
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FPS = 30
W, H = 1080, 1920
# ad name -> (animation source, silent video output)
ADS = {
    "villaem3": ("index.html", "villaem3_video_noaudio.mp4"),
    "best3": ("best3.html", "best3_video_noaudio.mp4"),
}
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)


def prepare_clips(src):
    """Explode the video clips an animation uses (src/<name>.clips.json) into JPG frames at FPS,
    so every rendered frame shows the exact matching video frame. Writes out/clips/<ad>_clips.js."""
    cfg = ROOT / "src" / src.replace(".html", ".clips.json")
    if not cfg.exists():
        return
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    counts = {}
    for name, c in json.loads(cfg.read_text()).items():
        if name.startswith("_"):
            continue
        d = ROOT / "out" / "clips" / name
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob("*.jpg"):
            old.unlink()
        subprocess.run([ffmpeg, "-v", "error", "-y", "-ss", str(c["start"]), "-t", str(c["dur"]), "-i", str(ROOT / c["src"]),
                        "-vf", f"setpts=PTS/{c.get('speed', 1)},fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                        "-q:v", "3", str(d / "f%04d.jpg")], check=True)
        counts[name] = len(list(d.glob("*.jpg")))
    (ROOT / "out" / "clips" / (src.replace(".html", "_clips.js"))).write_text(f"window.CLIPS = {json.dumps(counts)};\n")


def open_page(p, src):
    browser = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto((ROOT / "src" / src).as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].filter(i => !i.dataset.clip).every(i => i.complete && i.naturalWidth > 0)")
    return browser, page


def stills(src, times, prefix=""):
    out = ROOT / "out" / "stills"
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser, page = open_page(p, src)
        for t in times:
            page.evaluate(f"seek({t})")
            page.screenshot(path=str(out / f"{prefix}t{t:05.2f}.png"))
        browser.close()


def video(src, path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    with sync_playwright() as p:
        browser, page = open_page(p, src)
        duration = page.evaluate("window.DURATION")
        n = int(round(duration * FPS))
        proc = subprocess.Popen(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS),
             "-c:v", "png", "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)],
            stdin=subprocess.PIPE,
        )
        for i in range(n):
            page.evaluate(f"seek({i / FPS})")
            proc.stdin.write(page.screenshot(type="png"))
            if i % 90 == 0:
                print(f"frame {i}/{n}", flush=True)
        proc.stdin.close()
        proc.wait()
        browser.close()
    print("wrote", path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ad", choices=ADS, default="villaem3")
    ap.add_argument("--stills")
    ap.add_argument("--out")
    a = ap.parse_args()
    src, out = ADS[a.ad]
    prepare_clips(src)
    if a.stills:
        stills(src, [float(x) for x in a.stills.split(",")], prefix=f"{a.ad}_")
    else:
        (ROOT / "out").mkdir(exist_ok=True)
        video(src, a.out or str(ROOT / "out" / out))
