"""Montaj promo 15s: 10 shot × 1s daripada video sedia ada + kad promo 5s + muzik 120 BPM.

    python montaj/audio.py     # muzik + SFX  -> out/montaj_music.wav
    python montaj/build.py     # video akhir  -> out/montaj_15s.mp4

Shot diambil daripada versi bisu (out/<projek>_video_noaudio.mp4), mengikut montaj/shots.json
({src, t = saat paling menarik, label}); setiap shot = [t - 0.5, t + 0.5], zoom perlahan + kilat putih.
"""
import json
import pathlib
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
HERE = ROOT / "montaj"
TMP = ROOT / "out" / "_montaj"
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, CUT = 30, 1.0


def run(*args):
    subprocess.run([FF, "-y", "-v", "error", *map(str, args)], check=True)


def badge(path):
    """Lencana promo di bahagian atas sepanjang montaj."""
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(ROOT / "assets/fonts/Poppins-ExtraBold.ttf"), 40)
    text = "PROMO NEO PLUS · 7 BULAN PERTAMA RM20*"
    w = d.textlength(text, font=f)
    x0, y0, h = (1080 - w) / 2 - 34, 96, 78
    d.rounded_rectangle([x0 + 4, y0 + 6, x0 + w + 72, y0 + h + 6], 40, fill=(0, 0, 0, 70))
    d.rounded_rectangle([x0, y0, x0 + w + 68, y0 + h], 40, fill=(255, 210, 63, 255))
    d.text((x0 + 34, y0 + 12), text, font=f, fill=(11, 47, 107, 255))
    img.save(path)


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    shots = json.loads((HERE / "shots.json").read_text())

    # 1. kad promo (HTML beranimasi -> mp4)
    end = TMP / "endcard.mp4"
    subprocess.run([sys.executable, str(ROOT / "render.py"), "--page", "montaj/endcard.html", "--out", str(end)], check=True)

    # 2. potong setiap shot: zoom 1.00 -> 1.07, kilat putih 0.12s di permulaan
    segs = []
    for i, s in enumerate(shots):
        seg = TMP / f"seg{i:02d}.mp4"
        vf = (f"scale=w='1080*(1+0.07*t/{CUT})':h=-2:eval=frame,crop=1080:1920,setsar=1,fps={FPS},"
              + ("fade=in:st=0:d=0.12:color=white," if i else "")
              + "tpad=stop_mode=clone:stop=3,format=yuv420p")          # pastikan tepat 30 bingkai
        run("-ss", f"{max(0, s['t'] - CUT / 2):.3f}", "-i", ROOT / "out" / f"{s['src']}_video_noaudio.mp4",
            "-t", CUT + 0.2, "-vf", vf, "-frames:v", int(CUT * FPS), "-an", "-c:v", "libx264", "-crf", "16", seg)
        segs.append(seg)

    # 3. sambung + lencana (0-10s) + muzik
    badge(TMP / "badge.png")
    inputs = []
    for p in [*segs, end]:
        inputs += ["-i", p]
    n = len(segs) + 1
    montage_end = len(segs) * CUT
    fc = ("".join(f"[{i}:v]setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v{i}];" for i in range(n))
          + "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[cat];"
          + f"[cat][{n}:v]overlay=0:0:enable='lt(t,{montage_end})'[vid]")
    run(*inputs, "-loop", "1", "-i", TMP / "badge.png", "-i", ROOT / "out" / "montaj_music.wav",
        "-filter_complex", fc, "-map", "[vid]", "-map", f"{n + 1}:a", "-t", montage_end + 5.0,
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", ROOT / "out" / "montaj_15s.mp4")
    print("wrote", ROOT / "out" / "montaj_15s.mp4")


if __name__ == "__main__":
    main()
