"""Transcribe reference videos (Malay TikTok/Reels) with Gemini, audio only.

    python reference/transcribe.py video1.mp4 video2.mp4 ...   -> reference/raw/<name>.json

Audio is extracted to a small mono MP3 first (inline video uploads hit 502s through the proxy).
Models are tried in order because the larger Gemini models are often overloaded (503) or out of quota (429).
Check the result against the on-screen captions: product names and "beg biru" are often misheard.
"""
import base64
import json
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

import imageio_ffmpeg

HERE = pathlib.Path(__file__).parent
MODELS = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-flash-lite-latest"]
PROMPT = """Ini audio video TikTok/Reels Bahasa Melayu tentang penapis air Coway. Pulangkan JSON sahaja:
{"ringkasan": "1-2 ayat", "penutur": "lelaki/perempuan, atas kamera/voiceover, gaya & nada",
 "segmen": [{"mula": 0.0, "tamat": 3.2, "skrip": "transkrip TEPAT, kekalkan slang/campur Inggeris", "nada": "..."}],
 "muzik_sfx": "...", "produk": ["..."], "harga_promo": "semua harga/promo yang disebut"}
Segmen ikut ayat, masa dalam saat. Jangan tokok tambah."""


def audio(video):
    mp3 = HERE / "raw" / (video.stem + ".mp3")
    mp3.parent.mkdir(exist_ok=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1",
                    "-ar", "16000", "-b:a", "48k", str(mp3)], check=True)
    return mp3


def transcribe(mp3):
    body = json.dumps({"contents": [{"parts": [
        {"inlineData": {"mimeType": "audio/mp3", "data": base64.b64encode(mp3.read_bytes()).decode()}},
        {"text": PROMPT}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}}).encode()
    for i in range(12):
        m = MODELS[i % len(MODELS)]
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                     data=body, headers={"Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=300))
            r = json.loads(d["candidates"][0]["content"]["parts"][0]["text"])
            r["_model"] = m
            return r
        except urllib.error.HTTPError as e:
            print(mp3.name, m, e.code, flush=True)
        except (json.JSONDecodeError, KeyError) as e:
            print(mp3.name, m, "respons rosak:", e, flush=True)
        time.sleep(5 + 5 * (i // len(MODELS)))
    raise SystemExit("gagal " + mp3.name)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        v = pathlib.Path(arg)
        out = HERE / "raw" / (v.stem + ".json")
        out.write_text(json.dumps(transcribe(audio(v)), ensure_ascii=False, indent=1))
        print("ok", out)
