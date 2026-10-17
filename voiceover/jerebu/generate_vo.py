"""Jana VO pakej Jerebu dengan Gemini TTS, kemudian potong ikut babak.

    python voiceover/jerebu/generate_vo.py                 # semua video
    python voiceover/jerebu/generate_vo.py --only j2_kenapa_merah
    python voiceover/jerebu/generate_vo.py --voice Puck    # tukar suara (default Charon)
    python voiceover/jerebu/generate_vo.py --check         # transkrip full.wav untuk semakan

Kuota percuma Gemini TTS kecil (±10 permintaan sehari setiap model), jadi SATU permintaan
setiap video: skrip penuh dibaca sekali (jeda panjang antara babak), kemudian dipotong pada
N-1 jeda paling panjang -> voiceover/jerebu/<video>/NN.wav + durations.json.
Video yang skripnya tak berubah tidak dijana semula.

Rakaman sendiri: simpan voiceover/jerebu/<video>/full.wav (baca semua babak, jeda ±1 saat
antara babak) dan jalankan dengan --split-only. Atau ganti terus NN.wav satu per satu.
"""
import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import time
import wave

import imageio_ffmpeg
import numpy as np

HERE = pathlib.Path(__file__).parent
MODEL = os.environ.get("JEREBU_TTS_MODEL", "gemini-3.8-flash-tts")
SR = 24000
SPEED = float(os.environ.get("JEREBU_VO_SPEED", "1.2"))   # klien minta VO 1.2x lebih laju


def tts(text, style, voice):
    from google import genai
    from google.genai import types
    client = genai.Client()
    for attempt in range(3):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=text if os.environ.get("JEREBU_PLAIN") else f"{style}\n\n#### TRANSKRIP\n{text}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=voice)))))
            return np.frombuffer(r.candidates[0].content.parts[0].inline_data.data, "<i2").astype(float)
        except Exception as e:
            print("  cuba semula:", str(e)[:200])
            if "PerDay" in str(e):
                raise
            time.sleep(15 * 2 ** attempt)
    raise RuntimeError("TTS gagal")


def transcribe(path):
    from google import genai
    from google.genai import types
    client = genai.Client()
    r = client.models.generate_content(model="gemini-3.8-flash", contents=[
        types.Part.from_bytes(data=path.read_bytes(), mime_type="audio/wav"),
        "Transkripsikan audio ini kata demi kata. Tandakan setiap jeda panjang dengan baris baru. Teks sahaja."])
    return r.text.strip()


def align(path, scenes):
    """Minta Gemini anggarkan masa mula babak 2..N (saat). Disimpan ke cuts.json supaya sekali sahaja."""
    from google import genai
    from google.genai import types
    client = genai.Client()
    listing = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(scenes))
    r = client.models.generate_content(model="gemini-3.8-flash", contents=[
        types.Part.from_bytes(data=path.read_bytes(), mime_type="audio/wav"),
        f"Audio ini membaca {len(scenes)} perenggan berikut mengikut turutan:\n{listing}\n\n"
        f"Berikan masa (saat, 2 titik perpuluhan) bermulanya perenggan 2 hingga {len(scenes)} dalam audio. "
        "Jawab dengan tatasusunan JSON nombor sahaja."],
        config=types.GenerateContentConfig(response_mime_type="application/json"))
    return [float(v) for v in json.loads(r.text)]


def load(path):
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float)


def faster(x, speed):
    """Percepat tanpa ubah pic (ffmpeg atempo)."""
    if abs(speed - 1) < 1e-3:
        return x
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-i", "-",
                          "-filter:a", f"atempo={speed}", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         input=np.clip(x, -32768, 32767).astype("<i2").tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float)


def save(path, x):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(x, -32768, 32767).astype("<i2").tobytes())


def split(x, weights, hints=None):
    """Potong kepada len(weights) klip pada jeda senyap. Titik potong dipilih (DP) supaya panjang
    setiap klip paling hampir dengan bahagian yang dijangka (ikut panjang teks), dengan bonus jeda panjang."""
    n = len(weights); hop = int(.01 * SR)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop])
    loud = rms > max(250, .04 * np.percentile(rms, 95))
    on = np.flatnonzero(loud); first, last = int(on[0]), int(on[-1])
    gaps, i = [], first
    while i < last:
        if not loud[i]:
            j = i
            while not loud[j]:
                j += 1
            if j - i >= 18:
                gaps.append((i, j))
            i = j
        else:
            i += 1
    if hints:   # snap setiap anggaran ke jeda terdekat (ikut turutan)
        cuts, lo = [], 0
        for h in hints:
            k = min(range(lo, len(gaps)), key=lambda g: abs(gaps[g][1] / 100 - h) - .6 * (gaps[g][1] - gaps[g][0]) / 100)
            cuts.append(gaps[k]); lo = k + 1
        bounds = [first] + [b for g in cuts for b in g] + [last]
        clips = [x[max(0, a * hop - int(.04 * SR)):min(len(x), b * hop + int(.15 * SR))] for a, b in zip(bounds[::2], bounds[1::2])]
        return clips, [(b - a) / 100 for a, b in cuts]
    w = np.asarray(weights, float); tot = last - first
    exp_end = first + np.cumsum(w / w.sum()) * tot          # hujung dijangka setiap babak (hop)
    m = len(gaps); INF = 1e18
    # cost[k][g] = kos terbaik bila potongan ke-k (selepas babak k) di jeda g
    cost = np.full((n - 1, m), INF); back = np.zeros((n - 1, m), int)
    def c(k, g):
        mid = (gaps[g][0] + gaps[g][1]) / 2
        return ((mid - exp_end[k]) / (tot / n)) ** 2 - .8 * min(1.0, (gaps[g][1] - gaps[g][0]) / 80)
    for g in range(m):
        cost[0][g] = c(0, g)
    for k in range(1, n - 1):
        for g in range(m):
            prev = cost[k - 1][:g]
            if len(prev) and prev.min() < INF:
                back[k][g] = int(prev.argmin()); cost[k][g] = prev.min() + c(k, g)
    g = int(cost[n - 2].argmin()); cuts = [g]
    for k in range(n - 2, 0, -1):
        g = back[k][g]; cuts.append(g)
    cuts = [gaps[g] for g in reversed(cuts)]
    bounds = [first] + [b for g in cuts for b in g] + [last]
    clips = [x[max(0, a * hop - int(.04 * SR)):min(len(x), b * hop + int(.15 * SR))] for a, b in zip(bounds[::2], bounds[1::2])]
    return clips, [(b - a) / 100 for a, b in cuts]


def build(name, spec, voice, split_only=False, check=False, do_align=False):
    d = HERE / name; d.mkdir(exist_ok=True)
    scenes = spec["scenes"]; full = d / "full.wav"; tag = d / "full.hash"
    style = ("# PROFIL AUDIO\nPelakon suara iklan lelaki Malaysia.\n\n### NOTA PENGARAH\n"
             f"Gaya: {spec['style']}\nSebutan: Bahasa Melayu Malaysia (bukan Indonesia).\n"
             "Rentak: setiap perenggan transkrip ialah babak berasingan; diam kira-kira satu saat antara perenggan.\n"
             "Baca HANYA bahagian TRANSKRIP, kata demi kata.")
    script = "\n\n".join(scenes)
    h = hashlib.sha1(f"{MODEL}|{voice}|{style}|{script}".encode()).hexdigest()
    if not split_only and not (full.exists() and tag.exists() and tag.read_text() == h):
        print(f"[{name}] jana TTS ({len(scenes)} babak)…", flush=True)
        save(full, tts(script, style, voice)); tag.write_text(h)
    x = load(full)
    cj = d / "cuts.json"
    if do_align and not (cj.exists() and json.loads(cj.read_text()).get("hash") == h):
        cj.write_text(json.dumps({"hash": h, "starts": align(full, scenes)}))
    hints = json.loads(cj.read_text())["starts"] if cj.exists() else None
    clips, gaps = split(x, [len(t) for t in scenes], hints)
    durs = []
    for i, c in enumerate(clips):
        c = faster(c, SPEED)
        save(d / f"{i + 1:02d}.wav", c); durs.append(round(len(c) / SR, 3))
    (d / "durations.json").write_text(json.dumps(durs))
    rate = [dd / len(t) for dd, t in zip(durs, scenes)]     # saat per aksara patut lebih kurang sama
    med = float(np.median(rate))
    print(f"== {name}: {len(x) / SR:.1f}s, jeda potong {min(gaps):.2f}–{max(gaps):.2f}s")
    for i, (dd, t, r) in enumerate(zip(durs, scenes, rate)):
        print(f"  {i + 1:02d} {dd:5.2f}s  {t[:60]}{'  <-- SEMAK' if not .7 < r / med < 1.4 else ''}")
    if check:
        print(transcribe(full))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--voice", default="Charon")
    ap.add_argument("--split-only", action="store_true", help="guna full.wav sedia ada (cth. rakaman sendiri)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--align", action="store_true", help="guna Gemini untuk anggar sempadan babak (lebih tepat)")
    a = ap.parse_args()
    S = json.loads((HERE / "skrip.json").read_text())
    for n in ([a.only] if a.only else [k for k in S if not k.startswith("_")]):
        build(n, S[n], a.voice, a.split_only, a.check, a.align)


if __name__ == "__main__":
    main()
