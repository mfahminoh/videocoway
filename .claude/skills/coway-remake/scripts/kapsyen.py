"""Sediakan bahan untuk baca skrip video rujukan: audio (untuk transkripsi) + jubin bingkai untuk dibaca (Read).

    python3 .claude/skills/coway-remake/scripts/kapsyen.py <video.mp4> <folder-keluar>

Keluar:  audio.wav (16 kHz mono)  ->  python3 voiceover/transcribe_chunks.py <folder>/audio.wav 0 99 0.3
         grid.jpg      satu bingkai setiap 2 s (visual, babak, teks besar)
         kap_NN.jpg    jalur kapsyen setiap 0.2 s dengan cap masa (sandaran bila Gemini 503 / tiada transkrip)
Jalur kapsyen ambil 70-80 % tinggi bingkai (kedudukan kapsyen TikTok biasa); ubah --y0/--y1 jika kapsyen di tempat lain.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess

import imageio_ffmpeg

FF = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()    # perlukan drawtext (cap masa): ffmpeg sistem


def probe(src):
    out = subprocess.run([FF, "-i", str(src)], capture_output=True, text=True).stderr
    dur = next(l for l in out.splitlines() if "Duration:" in l).split("Duration:")[1].split(",")[0].strip()
    h, m, s = dur.split(":")
    vline = next(l for l in out.splitlines() if "Video:" in l)
    w, hh = re.search(r"\b(\d{2,5})x(\d{2,5})\b", vline).groups()
    return float(h) * 3600 + float(m) * 60 + float(s), [int(w), int(hh)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--y0", type=float, default=.68)
    ap.add_argument("--y1", type=float, default=.80)
    ap.add_argument("--seg", type=float, default=17, help="saat setiap jubin kapsyen (5 fps, 6 lajur)")
    a = ap.parse_args()
    o = pathlib.Path(a.out)
    o.mkdir(parents=True, exist_ok=True)
    dur, (w, h) = probe(a.src)
    run = lambda *c: subprocess.run([FF, "-v", "error", "-y", *map(str, c)], check=True)
    run("-i", a.src, "-vn", "-ac", 1, "-ar", 16000, o / "audio.wav")
    rows = int(dur / 2 / 5) + 1
    run("-i", a.src, "-vf", f"fps=1/2,scale=288:-1,drawtext=text='%{{pts\\:hms}}':x=4:y=4:fontsize=14:fontcolor=red,tile=5x{rows}", "-frames:v", 1, o / "grid.jpg")
    cy, ch = int(h * a.y0), int(h * (a.y1 - a.y0))
    k, t = 0, 0.0
    while t < dur:
        rows = int(a.seg * 5 / 6) + 1
        run("-ss", t, "-i", a.src, "-t", a.seg, "-vf",
            f"fps=5,crop={w}:{ch}:0:{cy},scale=420:-1,drawtext=text='%{{pts\\:hms\\:{t}}}':x=2:y=2:fontsize=13:fontcolor=red,tile=6x{rows}",
            "-frames:v", 1, o / f"kap_{k:02d}.jpg")
        k, t = k + 1, t + a.seg
    print(json.dumps({"durasi": round(dur, 2), "saiz": [w, h], "fail": sorted(p.name for p in o.iterdir())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
