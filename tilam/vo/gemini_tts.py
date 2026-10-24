"""Jana VO Bahasa Melayu (lelaki, santai) dengan Gemini TTS, satu fail WAV setiap baris.

    python tilam/vo/gemini_tts.py tilam/vo/lines_v16.json tilam/vo/v16_full.wav   # satu fail, satu permintaan (disyorkan)
    python tilam/vo/gemini_tts.py tilam/vo/lines_v16.json tilam/vo/v16            # satu fail setiap baris
Teks dihantar tanpa arahan gaya: model ni cenderung membaca arahan gaya dengan kuat.
Perlu GEMINI_API_KEY (atau proksi yang menyuntik kunci untuk generativelanguage.googleapis.com).
"""
import base64, json, os, pathlib, sys, time, urllib.request, wave

MODELS = ["gemini-3.1-flash-tts-preview", "gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts"]
VOICE = "Orus"
STYLE = ""


def tts(text, model):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {"contents": [{"parts": [{"text": STYLE + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}}
    hdr = {"Content-Type": "application/json"}
    if os.environ.get("GEMINI_API_KEY"):
        hdr["x-goog-api-key"] = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(url, json.dumps(body).encode(), hdr)
    d = json.load(urllib.request.urlopen(req, timeout=180))
    part = d["candidates"][0]["content"]["parts"][0]["inlineData"]
    return base64.b64decode(part["data"])          # PCM s16le 24 kHz mono


def main(lines, out):
    out = pathlib.Path(out); lines = json.loads(pathlib.Path(lines).read_text())
    if out.suffix == ".wav":
        lines = [{"id": out.stem, "text": "\n\n".join(l["text"] for l in lines)}]; out = out.parent
    out.mkdir(parents=True, exist_ok=True)
    for ln in lines:
        dest = out / f"{ln['id']}.wav"
        if dest.exists():
            continue
        for attempt in range(6):
            model = MODELS[min(attempt // 2, len(MODELS) - 1)]
            try:
                pcm = tts(ln["text"], model); break
            except Exception as e:
                print(ln["id"], model, "gagal:", e); time.sleep(15 * (attempt + 1))
        else:
            sys.exit(f"gagal jana {ln['id']}")
        with wave.open(str(dest), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
        print(ln["id"], model, f"{len(pcm) / 48000:.2f}s")
        time.sleep(8)


if __name__ == "__main__":
    main(*sys.argv[1:3])
