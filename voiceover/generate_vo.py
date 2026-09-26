"""Generate a Malay voiceover with a Microsoft Edge neural voice (edge-tts).

Run on your own computer (needs internet):
    pip install edge-tts imageio-ffmpeg
    python voiceover/generate_vo.py                       # Villaem 3, lelaki (Osman)
    python voiceover/generate_vo.py --lines neoplus/lines.json --clips neoplus/clips --voice ms-MY-YasminNeural

Each line in lines.json becomes voiceover/clips/<id>.mp3. If a line is longer than its
slot in the video, it is regenerated a little faster so it still fits.
You can also skip this script and record your own voice as clips/01.mp3 ... clips/08.mp3.
"""
import argparse
import asyncio
import json
import os
import pathlib
import subprocess

import certifi

# edge-tts hanya percaya CA certifi; hormati SSL_CERT_FILE jika ditetapkan (cth. di belakang proxy korporat)
if os.environ.get("SSL_CERT_FILE"):
    certifi.where = lambda: os.environ["SSL_CERT_FILE"]

import edge_tts  # noqa: E402
import imageio_ffmpeg  # noqa: E402

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
VOICE = "ms-MY-OsmanNeural"
BASE_RATE = 8      # % lebih laju — gaya content creator
PITCH = "+0Hz"


def duration(path):
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True).stderr
    h, m, s = out.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


async def make(line, dest, voice):
    slot = line["end"] - line["start"]
    rate = BASE_RATE
    for _ in range(4):
        await edge_tts.Communicate(line["text"], voice, rate=f"+{rate}%", pitch=PITCH).save(str(dest))
        d = duration(dest)
        if d <= slot:
            break
        rate = min(45, int(rate + (d / slot - 1) * 100) + 3)
    print(f"{line['id']}: {d:.2f}s / slot {slot:.2f}s  (rate +{rate}%)")


async def main(a):
    clips = ROOT / a.clips
    clips.mkdir(parents=True, exist_ok=True)
    for line in json.loads((ROOT / a.lines).read_text()):
        await make(line, clips / f"{line['id']}.mp3", a.voice)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", default="voiceover/lines.json")
    ap.add_argument("--clips", default="voiceover/clips")
    ap.add_argument("--voice", default=VOICE)
    asyncio.run(main(ap.parse_args()))
