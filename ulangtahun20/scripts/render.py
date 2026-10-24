"""Render video: rancang -> latar klip (ffmpeg) -> overlay HTML deterministik (Playwright, window.__render(t)) -> audio -> mp4.

    python scripts/render.py V01            # satu video -> out/S1-V01-v1.mp4 + out/sheets/V01.jpg
    python scripts/render.py V01-V15        # julat
    python scripts/render.py V01 --jobs 4   # bilangan proses Playwright selari

Ikut corak ../VideoCoway/scripts/render.py: halaman HTML deterministik, frame dipaip terus ke ffmpeg.
"""
import argparse
import io
import json
import multiprocessing as mp
import pathlib
import subprocess

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

import audio_mix
import plan as planner
from common import BUILD, CHROMIUM, DUR, FPS, H, OUT, ROOT, SRC, W, load_videos, read_json

TPL = ROOT / "templates" / "overlay.html"
NF = int(round(DUR * FPS))          # 600 frame


def fr(t):
    return int(round(t * FPS))


# ---------------- latar klip ----------------
def base_video(p, path):
    """Setiap shot: potong klip, skala ke 1080x1920 + gerakan perlahan (zoom 1.08 + seret), sambung semua."""
    inputs, chains = [], []
    k = 0
    for i, s in enumerate(p["shots"]):
        n = fr(s["t1"]) - fr(s["t0"])
        d = n / FPS + 0.2
        if s.get("endcard"):
            chains.append(f"color=c=white:s={W}x{H}:r={FPS}:d={n / FPS:.4f},format=yuv420p,trim=end_frame={n}[v{i}]")
            continue
        def src(c):
            nonlocal k
            inputs.extend(["-ss", f"{c['ss']:.3f}", "-t", f"{d:.3f}", "-i", str(SRC / c["file"])])
            k += 1
            return k - 1
        drift = 1 if i % 2 else -1
        move = (f"scale={int(W * 1.08)}:{int(H * 1.08)},setsar=1,"
                f"crop={W}:{H}:x='(in_w-out_w)/2+{drift}*(in_w-out_w)/2*(t/{d:.3f}-0.5)':y='(in_h-out_h)/2'")
        if s.get("split"):
            a, b = src(s["left"]), src(s["right"])
            chains.append(f"[{a}:v]fps={FPS},scale={W}:{H},setsar=1,crop={W // 2}:{H}:{W // 4}:0,hue=s=0,eq=brightness=-0.07[l{i}];"
                          f"[{b}:v]fps={FPS},scale={W}:{H},setsar=1,crop={W // 2}:{H}:{W // 4}:0,eq=saturation=1.15[r{i}];"
                          f"[l{i}][r{i}]hstack,trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
        else:
            a = src(s)
            chains.append(f"[{a}:v]fps={FPS},{move},eq=saturation=1.06:contrast=1.03,trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
    cat = "".join(f"[v{i}]" for i in range(len(p["shots"]))) + f"concat=n={len(p['shots'])}:v=1:a=0[out]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(chains) + ";" + cat,
                    "-map", "[out]", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "14", "-pix_fmt", "yuv420p",
                    "-frames:v", str(NF), str(path)], check=True)


# ---------------- overlay ----------------
def open_page(pw, p):
    b = pw.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else pw.chromium.launch()
    page = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    page.goto(TPL.as_uri())
    page.evaluate("Promise.all(['400','500','700','800'].map(w => document.fonts.load(w + ' 100px \"Noto Sans\"')))")
    page.evaluate("d => window.setup(d)", p)
    page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
    page.evaluate("document.fonts.ready")
    return b, page


def render_part(args):
    vid, a, b, base, out = args
    p = read_json(BUILD / f"{vid}.json")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-ss", f"{a / FPS:.4f}", "-i", str(base),
                           "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                           "-filter_complex", f"[0:v]trim=end_frame={b - a},setpts=PTS-STARTPTS[bg];[bg][1:v]overlay=0:0:eof_action=repeat,format=yuv420p[v]",
                           "-map", "[v]", "-frames:v", str(b - a), "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(out)],
                          stdin=subprocess.PIPE)
    with sync_playwright() as pw:
        br, page = open_page(pw, p)
        for i in range(a, b):
            page.evaluate(f"window.__render({i / FPS})")
            ff.stdin.write(page.screenshot(type="png", omit_background=True))
        br.close()
    ff.stdin.close(); ff.wait()
    return out


def stills(p, times):
    """Frame overlay sahaja (untuk semakan pantas)."""
    with sync_playwright() as pw:
        br, page = open_page(pw, p)
        res = []
        for t in times:
            page.evaluate(f"window.__render({t})")
            res.append(Image.open(io.BytesIO(page.screenshot(type="png", omit_background=True))))
        br.close()
    return res


# ---------------- contact sheet ----------------
def sheet(mp4, vid, times=(1.5, 5, 9, 14, 18)):
    d = OUT / "sheets"; d.mkdir(parents=True, exist_ok=True)
    ims = []
    for t in times:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "-vf", "scale=360:-2",
                              "-f", "image2", "-c:v", "png", "-"], capture_output=True, check=True).stdout
        ims.append(Image.open(io.BytesIO(raw)))
    w, h = ims[0].size
    s = Image.new("RGB", (5 * w + 6 * 10, h + 50), "white")
    dr = ImageDraw.Draw(s)
    font = ImageFont.truetype(str(ROOT.parent / "assets/fonts/Poppins-Bold.ttf"), 24)
    for i, (t, im) in enumerate(zip(times, ims)):
        s.paste(im, (10 + i * (w + 10), 44)); dr.text((10 + i * (w + 10), 8), f"{vid}  {t}s", fill="black", font=font)
    path = d / f"{vid}.jpg"; s.save(path, quality=88)
    return path


def render(v, jobs):
    p = planner.plan(v)
    BUILD.mkdir(parents=True, exist_ok=True)
    base = BUILD / f"{v['id']}_base.mp4"
    base_video(p, base)
    bounds = [round(NF * k / jobs) for k in range(jobs + 1)]
    parts = [(v["id"], bounds[k], bounds[k + 1], base, BUILD / f"{v['id']}_p{k}.mp4") for k in range(jobs)]
    with mp.Pool(jobs) as pool:
        files = pool.map(render_part, parts)
    lst = BUILD / f"{v['id']}_list.txt"
    lst.write_text("".join(f"file '{f.resolve()}'\n" for f in files))
    wav = BUILD / f"{v['id']}_mix.wav"
    audio_mix.build(p, wav)
    final = OUT / v["file"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "44100",
                    "-t", f"{DUR:.3f}", "-movflags", "+faststart", str(final)], check=True)
    for f in files + [lst, base, wav]:
        f.unlink()
    sh = sheet(final, v["id"])
    print(f"{v['id']}: {final.name}  sheet {sh.name}", flush=True)
    return final


def pick(spec):
    vids = load_videos()
    ids = [v["id"] for v in vids]
    want = set()
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); want |= set(ids[ids.index(a):ids.index(b) + 1])
        else:
            want.add(part)
    return [v for v in vids if v["id"] in want]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ids")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--stills", help="cth 1.5,5,9 -> out/stills/V01_*.png (overlay sahaja)")
    a = ap.parse_args()
    for v in pick(a.ids):
        if a.stills:
            p = planner.plan(v)
            d = OUT / "stills"; d.mkdir(parents=True, exist_ok=True)
            for t, im in zip(a.stills.split(","), stills(p, [float(x) for x in a.stills.split(",")])):
                bg = Image.new("RGBA", im.size, (90, 110, 120, 255)); bg.alpha_composite(im.convert("RGBA"))
                bg.convert("RGB").save(d / f"{v['id']}_{t}.png")
            print("stills", v["id"])
        else:
            render(v, a.jobs)
