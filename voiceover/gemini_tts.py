"""Generate one voiceover take for a whole script with Gemini TTS.

    python voiceover/gemini_tts.py videos/V05/lines.json videos/V05/vo.wav --voice Puck \
        --style "Bacakan dalam Bahasa Melayu Malaysia, gaya lelaki bertenaga ..."

All lines are read in a single request (more natural intonation); voiceover/align.py then
finds where each line starts and ends.

The TTS models reject systemInstruction ("Developer instruction is not enabled"), and when the
style is put in front of the text they read it aloud. So the style goes in the text, and the
spoken instruction is cut off afterwards at the longest pause near where it should end
(the untrimmed take is kept as <out>_raw.wav). Check the result with a transcript. Models are tried in order because they are often
overloaded (503) or rate-limited (429).
"""
import argparse
import base64
import json
import os
import pathlib
import time
import urllib.error
import urllib.request
import wave

import numpy as np

# Key sendiri (cth. projek Google AI Studio berbayar) jika ditetapkan; jika tidak, proxy persekitaran menyuntik key.
HEADERS = {"Content-Type": "application/json", **({"x-goog-api-key": os.environ["GEMINI_API_KEY"]} if os.environ.get("GEMINI_API_KEY") else {})}

MODELS = ["gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts", "gemini-3.8-flash-lite-tts"]


def tts(text, voice):
    req_body = {"contents": [{"parts": [{"text": text}]}],
                       "generationConfig": {"responseModalities": ["AUDIO"],
                                            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    body = json.dumps(req_body).encode()
    for i in range(12):
        m = MODELS[i % len(MODELS)]
        req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent",
                                     data=body, headers=HEADERS)
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
    ap.add_argument("--models", help="senarai model dipisah koma (cth. gemini-3.8-flash-tts); lalai: MODELS")
    a = ap.parse_args()
    if a.models:
        MODELS[:] = a.models.split(",")
    script = " ".join(l["text"] for l in json.loads(pathlib.Path(a.lines).read_text()))
    data, model = tts(f"{a.style}: {script}" if a.style else script, a.voice)
    out = pathlib.Path(a.out)
    raw = out.with_name(out.stem + "_raw.wav")
    if data[:4] == b"RIFF":            # model 3.x memulangkan WAV lengkap
        raw.write_bytes(data)
    else:                              # model 2.5 memulangkan PCM 24 kHz mentah
        with wave.open(str(raw), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(data)
    with wave.open(str(raw)) as w:
        sr, x = w.getframerate(), np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float)
    cut = 0.0
    if a.style:                        # potong arahan yang turut dibaca
        hop = sr // 100
        n = len(x) // hop
        db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) / 32768) ** 2).mean(1) + 1e-9)
        sil = db < db.max() - 38
        guess = len(a.style) * 0.055
        best, i = (0, 0), 0
        while i < n:
            if sil[i]:
                j = i
                while j < n and sil[j]:
                    j += 1
                if guess * 0.5 < i / 100 < guess * 1.8 + 1.5 and j - i > best[1] - best[0]:
                    best = (i, j)
                i = j
            else:
                i += 1
        if best[1] - best[0] >= 80:     # jeda >= 0.8s: tanda arahan dibaca (3.1-preview biasanya tak baca)
            cut = max(0, best[1] / 100 - 0.1)
    y = x[int(cut * sr):].copy()
    f = int(0.01 * sr)
    y[:f] *= np.linspace(0, 1, f)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.astype("<i2").tobytes())
    print(f"{out}: {len(y) / sr:.2f}s, dipotong {cut:.2f}s di depan ({model}, {a.voice})")
