"""Generate one voiceover take for a whole script with Gemini TTS.

    python voiceover/gemini_tts.py videos/V05/lines.json videos/V05/vo.wav --voice Puck \
        --style "Bacakan dalam Bahasa Melayu Malaysia, gaya lelaki bertenaga ..."

All lines are read in a single request (more natural intonation); voiceover/align.py then
finds where each line starts and ends. Models are tried in order because they are often
overloaded (503) or rate-limited (429).
"""
import argparse
import base64
import json
import pathlib
import time
import urllib.error
import urllib.request
import wave

MODELS = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts", "gemini-3.8-flash-lite-tts"]


def tts(text, voice, style=None):
    req_body = {"contents": [{"parts": [{"text": text}]}],
                       "generationConfig": {"responseModalities": ["AUDIO"],
                                            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    if style:  # arahan gaya sebagai systemInstruction: jika diletak dalam teks, model 3.8 membacanya kuat-kuat
        req_body["systemInstruction"] = {"parts": [{"text": style}]}
    body = json.dumps(req_body).encode()
    for i in range(12):
        m = MODELS[i % len(MODELS)]
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                     data=body, headers={"Content-Type": "application/json"})
        try:
            d = json.load(urllib.request.urlopen(req, timeout=300))
            return base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]), m
        except urllib.error.HTTPError as e:
            print(m, e.code, flush=True)
        except (KeyError, IndexError) as e:
            print(m, "tiada audio:", e, flush=True)
        time.sleep(5 + 5 * (i // len(MODELS)))
    raise SystemExit("TTS gagal")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("lines")
    ap.add_argument("out")
    ap.add_argument("--voice", default="Puck")
    ap.add_argument("--style", default="Bacakan dalam Bahasa Melayu Malaysia, gaya santai macam content creator")
    a = ap.parse_args()
    script = " ".join(l["text"] for l in json.loads(pathlib.Path(a.lines).read_text()))
    data, model = tts(script, a.voice, a.style)
    out = pathlib.Path(a.out)
    if data[:4] == b"RIFF":            # model 3.x memulangkan WAV lengkap
        out.write_bytes(data)
    else:                              # model 2.5 memulangkan PCM 24 kHz mentah
        with wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(data)
    with wave.open(str(out)) as w:
        print(f"{out}: {w.getnframes() / w.getframerate():.2f}s ({model}, {a.voice})")
