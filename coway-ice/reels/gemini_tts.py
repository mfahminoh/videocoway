"""Generate the Reels voiceover with the Gemini TTS API, one clip per script line.

    export GEMINI_API_KEY=...            # atau tambah dalam tetapan environment
    python reels/gemini_tts.py reel1     # -> reels/vo_reel1/01.wav ... 05.wav
    python reels/gemini_tts.py reel2

Optional env: GEMINI_TTS_MODEL (default gemini-2.5-flash-preview-tts), GEMINI_TTS_VOICE (default Kore).
A clip longer than its slot in <name>.lines.json is sped up (pitch kept, max 1.35x) so it fits the video.
Then mix:  python mix.py --video out/reel1_video_noaudio.mp4 --bed out/reel1_music_sfx.wav \
             --lines reels/reel1.lines.json --clips reels/vo_reel1 --out out/reel1_final.mp4
"""
import base64
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.request
import wave

import imageio_ffmpeg

HERE = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")
VOICE = os.environ.get("GEMINI_TTS_VOICE", "Kore")
STYLE = ("Baca dalam Bahasa Melayu Malaysia, nada mesra, ceria dan bersemangat macam iklan pendek "
         "di Instagram Reels, tempo agak laju tapi jelas: ")
SLACK = 0.25                   # boleh melimpah sedikit ke jeda seterusnya
MAX_TEMPO = 1.35


def tts(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {
        "contents": [{"parts": [{"text": STYLE + text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}},
        },
    }
    req = urllib.request.Request(url, json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            return base64.b64decode(part["data"]), part.get("mimeType", "")
        except Exception as e:  # rangkaian / had kadar — cuba lagi
            if attempt == 3:
                raise
            print("  retry:", e)
            time.sleep(2 ** (attempt + 1))


def rate_of(mime):
    for tok in mime.split(";"):
        if tok.strip().startswith("rate="):
            return int(tok.split("=")[1])
    return 24000


def duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def main(name):
    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY tiada — tambah dalam tetapan environment dan buka sesi baru.")
    lines = json.loads((HERE / f"{name}.lines.json").read_text())
    out = HERE / f"vo_{name}"
    out.mkdir(exist_ok=True)
    for ln in lines:
        pcm, mime = tts(ln["text"])
        raw = out / f"_{ln['id']}.pcm"
        raw.write_bytes(pcm)
        dst = out / f"{ln['id']}.wav"
        # PCM 16-bit mono -> wav; buang senyap di awal/hujung
        trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
        subprocess.run([FF, "-y", "-v", "error", "-f", "s16le", "-ar", str(rate_of(mime)), "-ac", "1", "-i", str(raw),
                        "-af", trim, "-ar", "44100", str(dst)], check=True)
        raw.unlink()
        d, slot = duration(dst), ln["end"] - ln["start"] + SLACK
        tempo = 1.0
        if d > slot:
            tempo = min(MAX_TEMPO, d / slot)
            tmp = dst.with_suffix(".tmp.wav")
            subprocess.run([FF, "-y", "-v", "error", "-i", str(dst), "-af", f"atempo={tempo:.3f}", str(tmp)], check=True)
            tmp.replace(dst)
        print(f"{ln['id']}: {d:.2f}s -> {duration(dst):.2f}s (slot {slot:.2f}s, tempo {tempo:.2f}x)  {ln['text']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "reel1")
