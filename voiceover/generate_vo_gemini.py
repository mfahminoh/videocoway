"""Jana voiceover Bahasa Melayu dengan Gemini text-to-speech (Google Gemini API).

Perlu API key Gemini (https://aistudio.google.com/apikey), sama ada dalam pembolehubah GEMINI_API_KEY, atau
(dalam sesi cloud Claude Code) sebagai "API credential" environment untuk hos generativelanguage.googleapis.com
dengan header x-goog-api-key.

    python voiceover/generate_vo_gemini.py --lines neoplus_full/lines.json --clips neoplus_full/clips
    python voiceover/generate_vo_gemini.py --lines neoplus/lines.json --clips neoplus/clips --fit
    python voiceover/generate_vo_gemini.py --list          # senarai model TTS yang ada untuk kunci anda

Setiap baris menjadi <clips>/<id>.wav (mono 24 kHz). --fit mempercepat sedikit (atempo, pic kekal) klip yang
lebih panjang daripada slotnya — guna untuk video dengan slot tetap (neoplus/). Untuk neoplus_full/, jangan guna
--fit; sebaliknya jalankan `python neoplus_full/timeline.py --clips neoplus_full/clips` supaya video ikut suara.
"""
import argparse
import base64
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import wave

import imageio_ffmpeg

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://generativelanguage.googleapis.com/v1beta"
SR = 24000
VOICE = "Sulafat"   # suara perempuan yang hangat; cuba juga Kore, Aoede, Leda, Callirrhoe, Achernar
STYLE = ("Baca dalam Bahasa Melayu Malaysia, loghat standard. Suara wanita muda yang mesra dan ikhlas, "
         "macam seorang anak bercerita pasal mak ayah dia di kampung kepada kawan. Santai, hangat, tidak "
         "seperti iklan TV, tempo sederhana laju. Baca teks ini sahaja")


def call(url, body=None):
    headers = {"Content-Type": "application/json"}
    if os.environ.get("GEMINI_API_KEY"):     # tanpa ini, kunci dipasang oleh "API credentials" environment Claude
        headers["x-goog-api-key"] = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=headers)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code in (429, 500, 503) and attempt < 4:
                time.sleep(2 ** attempt * 5)
                continue
            raise SystemExit(f"Gemini API {e.code}: {msg[:600]}")


def tts_models():
    names, token = [], ""
    while True:
        d = call(f"{API}/models?pageSize=200" + (f"&pageToken={token}" if token else ""))
        names += [m["name"].split("/", 1)[1] for m in d.get("models", []) if "tts" in m["name"].lower()]
        token = d.get("nextPageToken")
        if not token:
            return names


def pick_model():
    models = tts_models()
    if not models:
        raise SystemExit("Tiada model TTS untuk kunci ini. Guna --model <nama>.")

    def rank(m):   # utamakan versi tertinggi, 'flash' (bukan lite), bukan preview
        ver = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)", m)[:1]] or [0]
        return (ver[0], "flash" in m and "lite" not in m, "preview" not in m)
    return max(models, key=rank)


def synth(model, voice, text, style):
    body = {
        "contents": [{"parts": [{"text": f"{style}: {text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }
    d = call(f"{API}/models/{model}:generateContent", body)
    try:
        part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    except (KeyError, IndexError):
        raise SystemExit(f"Tiada audio dalam respons: {json.dumps(d)[:600]}")
    return base64.b64decode(part["data"]), part.get("mimeType", "")


def write_wav(path, pcm, sr=SR):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)


def trim_and_fit(path, slot, fit):
    """Buang senyap di hujung klip; jika --fit dan masih lebih panjang daripada slot, percepat (maks 1.35x)."""
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    tmp = path.with_suffix(".tmp.wav")
    trim = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run([ff, "-y", "-v", "error", "-i", str(path), "-af", trim, str(tmp)], check=True)
    tmp.replace(path)
    d = duration(path)
    if fit and d > slot:
        k = min(1.35, d / slot)
        subprocess.run([ff, "-y", "-v", "error", "-i", str(path), "-af", f"atempo={k:.3f}", str(tmp)], check=True)
        tmp.replace(path)
        d = duration(path)
    return d


def duration(path):
    with wave.open(str(path)) as w:
        return w.getnframes() / w.getframerate()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", default="neoplus_full/lines.json")
    ap.add_argument("--clips", default="neoplus_full/clips")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--model", help="nama model TTS (lalai: pilih automatik daripada --list)")
    ap.add_argument("--style", default=STYLE, help="arahan gaya bacaan yang diletak sebelum teks")
    ap.add_argument("--fit", action="store_true", help="percepat klip yang lebih panjang daripada slot")
    ap.add_argument("--only", help="jana baris tertentu sahaja, cth. 03,11")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY tiada — anggap kunci dipasang oleh API credentials environment (header x-goog-api-key).")
    if a.list:
        print("\n".join(tts_models()))
        return
    model = a.model or pick_model()
    print(f"model: {model}  suara: {a.voice}")
    clips = ROOT / a.clips
    clips.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    for ln in json.loads((ROOT / a.lines).read_text()):
        if only and ln["id"] not in only:
            continue
        pcm, mime = synth(model, a.voice, ln["text"], a.style)
        sr = int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else SR
        dest = clips / f"{ln['id']}.wav"
        write_wav(dest, pcm, sr)
        for old in (clips / f"{ln['id']}.mp3",):     # elak mix.py ambil klip lama edge-tts
            old.unlink(missing_ok=True)
        slot = ln["end"] - ln["start"]
        d = trim_and_fit(dest, slot, a.fit)
        flag = "" if d <= slot + .05 else "  <- lebih panjang daripada slot"
        print(f"{ln['id']}: {d:5.2f}s / slot {slot:5.2f}s{flag}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
