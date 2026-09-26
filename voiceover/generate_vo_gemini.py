"""Generate the voiceover with Gemini TTS (one clip per line in lines.json).

    export GEMINI_API_KEY=...                       # from Google AI Studio
    python voiceover/generate_vo_gemini.py --ad best3
    python voiceover/generate_vo_gemini.py --ad best3 --voice Puck --only 03   # redo one line
    python mix.py --ad best3

Each line becomes voiceover/<ad>/clips/<id>.wav. A clip longer than its slot in the video
is sped up (pitch kept) so it still fits. Needs only the standard library + imageio-ffmpeg.
"""
import argparse
import base64
import json
import os
import pathlib
import subprocess
import urllib.request
import wave

import imageio_ffmpeg

HERE = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
STYLE = ("Baca dalam Bahasa Melayu Malaysia yang santai, macam content creator TikTok yang mesra dan bersemangat, "
         "tempo agak laju tapi jelas, senyum bila bercakap. Baca teks ini sahaja:")


def tts(text, voice, model, key):
    body = {
        "contents": [{"parts": [{"text": f"{STYLE}\n{text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=120) as r:
        res = json.load(r)
    return base64.b64decode(res["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])  # 24 kHz 16-bit mono PCM


def trim_and_fit(raw, dest, slot):
    tmp = dest.with_suffix(".raw.wav")
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(24000)
        w.writeframes(raw)
    trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run([FF, "-v", "error", "-y", "-i", str(tmp), "-af", trim, str(dest)], check=True)
    with wave.open(str(dest)) as w:
        d = w.getnframes() / w.getframerate()
    if d > slot:
        speed = min(1.6, d / slot)
        subprocess.run([FF, "-v", "error", "-y", "-i", str(dest), "-af", f"{trim},atempo={speed:.3f}", str(tmp)], check=True)
        tmp.replace(dest)
        print(f"   sped up x{speed:.2f} to fit")
        d /= speed
    tmp.unlink(missing_ok=True)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ad", choices=["villaem3", "best3"], default="best3")
    ap.add_argument("--voice", default="Puck", help="Gemini prebuilt voice, e.g. Puck, Kore, Charon, Fenrir, Aoede")
    ap.add_argument("--model", default=os.environ.get("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts"))
    ap.add_argument("--only", help="comma-separated line ids to regenerate")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise SystemExit("Set GEMINI_API_KEY first.")
    base = HERE if a.ad == "villaem3" else HERE / a.ad
    clips = base / "clips"
    clips.mkdir(exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    for line in json.loads((base / "lines.json").read_text()):
        if only and line["id"] not in only:
            continue
        slot = line["end"] - line["start"]
        d = trim_and_fit(tts(line["text"], a.voice, a.model, key), clips / f"{line['id']}.wav", slot)
        print(f"{line['id']}: {d:.2f}s / slot {slot:.2f}s")


if __name__ == "__main__":
    main()
