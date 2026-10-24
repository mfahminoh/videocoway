"""Montaj promo pakej "30 VIDEO WP COWAY" — 3 versi × 15 s (portrait 1080×1920).

    python pakej30/build.py            # bina v1, v2, v3
    python pakej30/build.py 2          # bina v2 sahaja

Shot diambil daripada video sedia ada mengikut pakej30/shots.json ({cut, shots: [{video, t}]}); setiap shot
= [t - cut/2, t + cut/2]. Teks "30 VIDEO / WP COWAY" kekal di tengah sepanjang video.
"""
import json
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "pakej30"
TMP = ROOT / "out" / "_pakej30"
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H = 30, 1080, 1920
FONT = str(ROOT / "assets/fonts/Poppins-ExtraBold.ttf")


def run(*args):
    subprocess.run([FF, "-y", "-v", "error", *map(str, args)], check=True)


def title_png(path):
    """Teks tengah: '30 VIDEO' (putih, garis navy tebal) atas pil kuning 'WP COWAY', dengan bayang lembut."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # kegelapan lembut di tengah supaya teks sentiasa jelas di atas apa-apa shot
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rounded_rectangle([60, 700, W - 60, 1260], 120, fill=175)
    shade = shade.filter(ImageFilter.GaussianBlur(70))
    img.paste(Image.new("RGBA", (W, H), (4, 18, 44, 255)), (0, 0), shade)

    d = ImageDraw.Draw(img)
    t1, t2 = "30 VIDEO", "WP COWAY"
    size = 250
    while ImageDraw.Draw(img).textlength(t1, font=ImageFont.truetype(FONT, size)) + 28 > 920:   # muat dalam skrin
        size -= 5
    f1, f2 = ImageFont.truetype(FONT, size), ImageFont.truetype(FONT, 120)
    w1 = d.textlength(t1, font=f1)
    y1 = 960 - size - 20
    d.text(((W - w1) / 2 + 8, y1 + 12), t1, font=f1, fill=(0, 0, 0, 110))                   # bayang
    d.text(((W - w1) / 2, y1), t1, font=f1, fill="white", stroke_width=14, stroke_fill=(11, 47, 107))
    w2 = d.textlength(t2, font=f2)
    px, py, ph = (W - w2) / 2 - 50, 1000, 175
    d.rounded_rectangle([px + 8, py + 12, px + w2 + 108, py + ph + 12], 60, fill=(0, 0, 0, 110))
    d.rounded_rectangle([px, py, px + w2 + 100, py + ph], 60, fill=(255, 210, 63), outline=(11, 47, 107), width=10)
    d.text(((W - w2) / 2, py + 12), t2, font=f2, fill=(11, 47, 107))
    img.save(path)


def build(var, cfg):
    cut, shots = cfg["cut"], cfg["shots"]
    frames = int(round(cut * FPS))
    subprocess.run([sys.executable, str(HERE / "audio.py"), str(var)], check=True)
    segs = []
    for i, s in enumerate(shots):
        seg = TMP / f"v{var}_{i:02d}.mp4"
        zoom = 0.06 if cut >= 1 else 0.035                     # zoom perlahan dalam setiap shot
        vf = (f"scale=w='{W}*(1+{zoom}*t/{cut})':h=-2:eval=frame,crop={W}:{H},setsar=1,fps={FPS},"
              + ("fade=in:st=0:d=0.1:color=white," if i and cut >= 1 else "")
              + "tpad=stop_mode=clone:stop=3,format=yuv420p")
        run("-ss", f"{max(0, s['t'] - cut / 2):.3f}", "-i", ROOT / s["video"], "-t", cut + 0.2, "-vf", vf,
            "-frames:v", frames, "-an", "-c:v", "libx264", "-crf", "16", seg)
        segs.append(seg)
    inputs = []
    for p in segs:
        inputs += ["-i", p]
    n = len(segs)
    fc = ("".join(f"[{i}:v]setpts=PTS-STARTPTS[s{i}];" for i in range(n))
          + "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[cat];"
          + f"[cat][{n}:v]overlay=0:0:format=auto,format=yuv420p[vid]")
    out = ROOT / "out" / f"pakej30_v{var}.mp4"
    run(*inputs, "-loop", "1", "-i", TMP / "title.png", "-i", ROOT / "out" / f"pakej30_music_v{var}.wav",
        "-filter_complex", fc, "-map", "[vid]", "-map", f"{n + 1}:a", "-t", 15,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    print("wrote", out)


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    title_png(TMP / "title.png")
    cfg = json.loads((HERE / "shots.json").read_text())
    for v in ([int(sys.argv[1])] if len(sys.argv) > 1 else [1, 2, 3]):
        build(v, cfg[f"v{v}"])


if __name__ == "__main__":
    main()
