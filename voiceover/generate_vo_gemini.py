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
# Tag gaya di depan teks. Model TTS baharu (gemini-3.x) MEMBACA arahan ayat penuh ("Baca dengan nada ...: teks")
# dengan kuat, tetapi memahami tag dalam kurungan tanpa menyebutnya.
STYLE = "[warm] [sincere] [conversational]"


def call(url, body=None):
    headers = {"Content-Type": "application/json"}
    if os.environ.get("GEMINI_API_KEY"):     # tanpa ini, kunci dipasang oleh "API credentials" environment Claude
        headers["x-goog-api-key"] = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=headers)
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code in (429, 500, 502, 503, 504) and attempt < 5:
                m = re.search(r"retry in ([\d.]+)s", msg)   # had kuota seminit: tunggu seperti yang diminta
                time.sleep(float(m.group(1)) + 2 if m else 2 ** attempt * 5)
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
        "contents": [{"parts": [{"text": f"{style} {text}".strip()}]}],
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


def to_wav(audio, mime, dest):
    if audio[:4] == b"RIFF":              # model baharu pulangkan fail WAV lengkap
        dest.write_bytes(audio)
    else:                                 # model lama: PCM 16-bit mentah (audio/L16;rate=24000)
        write_wav(dest, audio, int(mime.split("rate=")[1].split(";")[0]) if "rate=" in mime else SR)


def speak_time(text):
    return len(text) / 14.5 + 0.3


def split_on_pauses(path, texts):
    """Potong satu rakaman berbilang baris kepada len(texts) bahagian pada jeda senyap.

    Pilih len(texts)-1 jeda (mengikut urutan) yang paling panjang dan paling hampir dengan kedudukan
    jangkaan (berkadar dengan panjang teks). Pulangkan senarai (mula, tamat) dalam saat, atau None jika
    hasilnya tak munasabah."""
    import numpy as np
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
    hop = int(sr * 0.01)
    db = 20 * np.log10(np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop]) + 1e-9)
    loud = db > db.max() - 38
    idx = np.flatnonzero(loud)
    t0, t1 = idx[0] * .01, idx[-1] * .01
    runs, i = [], idx[0]
    while i < idx[-1]:                      # senarai jeda senyap (mula, panjang) dalam saat
        if not loud[i]:
            j = i
            while j < len(loud) and not loud[j]:
                j += 1
            if (j - i) * .01 >= .15:
                runs.append(((i + j) / 2 * .01, (j - i) * .01))
            i = j
        else:
            i += 1
    n = len(texts)
    if n == 1:
        return [(t0, t1)]
    w_ = np.cumsum([speak_time(t) for t in texts])
    expect = t0 + (t1 - t0) * (w_[:-1] / w_[-1])
    m = len(runs)
    if m < n - 1:
        return None
    NEG = -1e9
    best = np.full((n - 1, m), NEG)
    back = np.zeros((n - 1, m), int)
    for k in range(n - 1):
        for c in range(m):
            gain = runs[c][1] * 4 - abs(runs[c][0] - expect[k]) * 1.0
            if k == 0:
                best[k, c] = gain
            else:
                prev = best[k - 1, :c]
                if len(prev) and prev.max() > NEG:
                    back[k, c] = int(prev.argmax())
                    best[k, c] = prev.max() + gain
    c = int(best[n - 2].argmax())
    if best[n - 2, c] <= NEG:
        return None
    cuts = [c]
    for k in range(n - 2, 0, -1):
        c = back[k, c]
        cuts.append(c)
    cuts = [runs[c][0] for c in reversed(cuts)]
    bounds = list(zip([t0] + cuts, cuts + [t1]))
    for (a_, b_), t in zip(bounds, texts):   # semak munasabah: tempoh berbanding panjang teks
        if not (.4 * speak_time(t) <= b_ - a_ <= 2.3 * speak_time(t)):
            return None
    return bounds


def cut(src, a_, b_, dest):
    with wave.open(str(src)) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        w.setpos(max(0, int((a_ - .05) * sr)))
        data = w.readframes(int((b_ - a_ + .1) * sr))
    with wave.open(str(dest), "wb") as o:
        o.setnchannels(ch)
        o.setsampwidth(sw)
        o.setframerate(sr)
        o.writeframes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lines", default="neoplus_full/lines.json")
    ap.add_argument("--clips", default="neoplus_full/clips")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--model", help="nama model TTS (lalai: pilih automatik daripada --list)")
    ap.add_argument("--style", default=STYLE, help='tag gaya sebelum teks, cth. "[warm] [cheerful]" ("" = tiada)')
    ap.add_argument("--fit", action="store_true", help="percepat klip yang lebih panjang daripada slot")
    ap.add_argument("--only", help="jana baris tertentu sahaja, cth. 03,11")
    ap.add_argument("--missing", action="store_true", help="jana hanya baris yang belum ada klip .wav")
    ap.add_argument("--batch", type=int, default=1,
                    help="bilangan baris setiap permintaan; audio dipotong pada jeda (jimat kuota: percuma = 10 permintaan/hari/model)")
    ap.add_argument("--pause", type=float, default=6.5, help="saat antara permintaan (had seminit)")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY tiada — anggap kunci dipasang oleh API credentials environment (header x-goog-api-key).")
    if a.list:
        print("\n".join(tts_models()))
        return
    model = a.model or pick_model()
    print(f"model: {model}  suara: {a.voice}  baris/permintaan: {a.batch}")
    clips = ROOT / a.clips
    clips.mkdir(parents=True, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    todo = [ln for ln in json.loads((ROOT / a.lines).read_text())
            if (not only or ln["id"] in only) and not (a.missing and (clips / f"{ln['id']}.wav").exists())]
    groups = [todo[i:i + a.batch] for i in range(0, len(todo), a.batch)]
    for g in groups:
        texts = [ln["text"] for ln in g]
        est = sum(speak_time(t) for t in texts) + .6 * (len(g) - 1)
        raw = clips / f"_batch_{g[0]['id']}.wav"
        for attempt in range(3):
            # baris dipisah dengan baris kosong + tag jeda supaya ada senyap yang jelas untuk dipotong
            audio, mime = synth(model, a.voice, "\n\n[long pause]\n\n".join(texts), a.style)
            time.sleep(a.pause)
            to_wav(audio, mime, raw)
            bounds = split_on_pauses(raw, texts) if duration(raw) <= est * 1.7 else None
            if bounds:
                break
            print(f"{g[0]['id']}..{g[-1]['id']}: {duration(raw):.1f}s — tak dapat dipotong dengan yakin, jana semula", flush=True)
        else:
            raise SystemExit(f"Gagal untuk baris {g[0]['id']}..{g[-1]['id']}; cuba --batch lebih kecil.")
        for ln, (b0, b1) in zip(g, bounds):
            dest = clips / f"{ln['id']}.wav"
            cut(raw, b0, b1, dest)
            (clips / f"{ln['id']}.mp3").unlink(missing_ok=True)   # elak mix.py ambil klip lama edge-tts
            slot = ln["end"] - ln["start"]
            d = trim_and_fit(dest, slot, a.fit)
            flag = "" if d <= slot + .05 else "  <- lebih panjang daripada slot"
            print(f"{ln['id']}: {d:5.2f}s / slot {slot:5.2f}s{flag}", flush=True)
        raw.unlink()


if __name__ == "__main__":
    sys.exit(main())
