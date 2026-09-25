"""Prepare footage from the reference videos (AIS_2 / AIS_3) for the Coway Ice ad.

The reference videos already have burned-in captions in a band at ~20-33% of the frame height,
so every clip is cropped to the area BELOW that band (y >= 440 of 1280) and muted.
Our own on-screen text (from the script) is drawn by src/index.html instead.

    python prep.py --ais2 path/to/AIS_2.mp4 --ais3 path/to/AIS_3.mp4   # cut clips -> assets/clips/*.mp4
    python prep.py                                                      # only extract frames -> build/frames/

render.py needs build/frames/<clip>/0001.jpg ... (30 fps), which this script extracts from assets/clips.
"""
import argparse
import pathlib
import shutil
import subprocess

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
CROP = "crop=720:840:0:440"          # buang jalur teks asal (atas) — tinggal bahagian bawah sahaja

# nama -> (video sumber, mula, tamat) dalam saat
CLIPS = {
    "drop":     ("ais3", 5.9, 8.3),     # ais jatuh masuk gelas (close-up)
    "dispense": ("ais2", 15.0, 17.9),   # ais keluar dari muncung, gelas penuh
}


def cut(sources):
    out = ROOT / "assets" / "clips"
    out.mkdir(parents=True, exist_ok=True)
    for name, (src, a, b) in CLIPS.items():
        subprocess.run([FF, "-y", "-v", "error", "-ss", str(a), "-to", str(b), "-i", str(sources[src]), "-an",
                        "-vf", f"{CROP},fps=30", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                        str(out / f"{name}.mp4")], check=True)
        print("cut", name)


def frames():
    for name in CLIPS:
        d = ROOT / "build" / "frames" / name
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        subprocess.run([FF, "-y", "-v", "error", "-i", str(ROOT / "assets" / "clips" / f"{name}.mp4"),
                        "-q:v", "2", str(d / "%04d.jpg")], check=True)
        print(name, len(list(d.glob("*.jpg"))), "frames")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ais2")
    ap.add_argument("--ais3")
    a = ap.parse_args()
    if a.ais2 and a.ais3:
        cut({"ais2": a.ais2, "ais3": a.ais3})
    frames()
