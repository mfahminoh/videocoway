"""Generate the Malay male voiceover (Microsoft Edge neural voice ms-MY-OsmanNeural).

Run on your own computer (needs internet):
    pip install edge-tts imageio-ffmpeg
    python voiceover/generate_vo.py

Each line in lines.json becomes voiceover/clips/<id>.mp3. If a line is longer than its
slot in the video, it is regenerated a little faster so it still fits.
You can also skip this script and record your own voice as clips/01.mp3 ... clips/08.mp3.
"""
import asyncio
import json
import pathlib
import subprocess

import edge_tts
import imageio_ffmpeg

HERE = pathlib.Path(__file__).parent
VOICE = "ms-MY-OsmanNeural"
BASE_RATE = 8      # % lebih laju — gaya content creator
PITCH = "+0Hz"


def duration(path):
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True).stderr
    h, m, s = out.split("Duration: ")[1].split(",")[0].split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


async def make(line, dest):
    slot = line["end"] - line["start"]
    rate = BASE_RATE
    for _ in range(4):
        await edge_tts.Communicate(line["text"], VOICE, rate=f"+{rate}%", pitch=PITCH).save(str(dest))
        d = duration(dest)
        if d <= slot:
            break
        rate = min(45, int(rate + (d / slot - 1) * 100) + 3)
    print(f"{line['id']}: {d:.2f}s / slot {slot:.2f}s  (rate +{rate}%)")


async def main():
    clips = HERE / "clips"
    clips.mkdir(exist_ok=True)
    for line in json.loads((HERE / "lines.json").read_text()):
        await make(line, clips / f"{line['id']}.mp3")


if __name__ == "__main__":
    asyncio.run(main())
