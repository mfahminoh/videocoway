"""VO untuk video tutorial Profile / Page / Ads Manager (tutorial-fb-ads-01, TF01).

Visual siap (kapsyen terbakar, tanpa audio) dalam videos/TF01/visual_tanpa_vo.mp4; masa setiap
kapsyen dalam projek/tutorial-fb-ads-01/kapsyen.srt. Satu baris SRT = satu panggilan Gemini TTS,
diletak pada masa mula kapsyen tu (dipercepat sedikit jika tak muat), kemudian di-mux.

    python3 videos/tutorial-fb-ads-01_vo.py            # jana baris yang belum ada + mix + mux
    python3 videos/tutorial-fb-ads-01_vo.py --redo 3,28  # jana semula baris tertentu
"""
import argparse, concurrent.futures as cf, json, pathlib, re, subprocess, sys, wave
import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "voiceover"))
import gemini_tts  # noqa: E402
from gemini_tts import tts  # noqa: E402
gemini_tts.MODELS[:] = ["gemini-3.1-flash-tts-preview"]  # 3.8/2.5 kerap baca arahan gaya

D = ROOT / "videos" / "TF01"
SRT = ROOT / "projek" / "tutorial-fb-ads-01" / "kapsyen.srt"
OUT = ROOT / "out" / "tutorial-fb-ads-01" / "TF01_profile_page_adsmanager.mp4"
VOICE = "Kore"
STYLE = "Bacakan dalam Bahasa Melayu Malaysia, nada mesra, tenang dan jelas macam cikgu terangkan kepada kawan"
SR = 24000
# sebutan untuk TTS sahaja (kapsyen kekal)
SAY = [("business.facebook.com", "business titik facebook titik com"),
       ("adsmanager.facebook.com", "ads manager titik facebook titik com"),
       ("Page & Ads Manager", "Page dan Ads Manager")]


def srt():
    out = []
    for blk in SRT.read_text().strip().split("\n\n"):
        ls = blk.strip().splitlines()
        a, b = [sum(float(x) * m for x, m in zip(t.replace(",", ".").split(":"), (3600, 60, 1))) for t in ls[1].split(" --> ")]
        out.append({"i": int(ls[0]), "a": a, "b": b, "text": " ".join(ls[2:])})
    return out


def read(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768, w.getframerate()


def trim(x, sr):
    """Buang senyap di awal dan hujung sahaja."""
    hop = sr // 100
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop)) ** 2).mean(1) + 1e-9)
    idx = np.where(db > db.max() - 40)[0]
    return x[max(0, idx[0] - 5) * hop: min(n, idx[-1] + 9) * hop]


CPS = 14.5  # kadar bacaan Kore (aksara/saat) dari baris yang betul


def gen(seg):
    """Jana satu baris; ulang jika panjangnya tak munasabah (arahan gaya dibaca / ayat terpotong)."""
    p = D / f"line_{seg['i']:02d}.wav"
    text = seg["text"]
    for k, v in SAY:
        text = text.replace(k, v)
    exp = len(text) / CPS
    best = None
    for attempt in range(4):
        prompt = f"{STYLE}: {text}" if attempt < 3 else text   # cubaan terakhir tanpa arahan gaya
        data, model = tts(prompt, VOICE)
        if data[:4] == b"RIFF":
            raw = D / "_raw.wav"; raw.write_bytes(data); x, sr = read(raw); raw.unlink()
        else:
            x, sr = np.frombuffer(data, "<i2").astype(float) / 32768, 24000
        y = trim(x, sr)
        r = len(y) / sr / exp
        if best is None or abs(np.log(r)) < abs(np.log(best[2])):
            best = (y, sr, r, model)
        if 0.75 < r < 1.3:
            break
        print(f"  baris {seg['i']:02d} cubaan {attempt + 1}: {len(y) / sr:.1f}s vs jangka {exp:.1f}s, ulang", flush=True)
    y, sr, r, model = best
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((y * 32767).astype("<i2").tobytes())
    return seg["i"], len(y) / sr, f"{model}, x{r:.2f} jangka"


def tempo(x, sr, f):
    if f <= 1.001:
        return x
    tmp_in, tmp_out = D / "_t_in.wav", D / "_t_out.wav"
    with wave.open(str(tmp_in), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((x * 32767).astype("<i2").tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp_in, "-filter:a", f"atempo={f:.4f}", tmp_out], check=True)
    y, _ = read(tmp_out)
    tmp_in.unlink(); tmp_out.unlink()
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--redo", default="")
    a = ap.parse_args()
    segs = srt()
    redo = {int(i) for i in a.redo.split(",") if i}
    todo = [s for s in segs if s["i"] in redo or not (D / f"line_{s['i']:02d}.wav").exists()]
    with cf.ThreadPoolExecutor(2) as ex:
        for i, dur, model in ex.map(gen, todo):
            print(f"baris {i:02d}: {dur:.2f}s ({model})", flush=True)

    total = 214.8
    track = np.zeros(int(total * SR) + SR)
    log, prev_end = [], 0.0
    for k, s in enumerate(segs):
        x, sr = read(D / f"line_{s['i']:02d}.wav")
        assert sr == SR, sr
        nxt = segs[k + 1]["a"] if k + 1 < len(segs) else total
        start = max(s["a"] + 0.08, prev_end + 0.12)
        room = nxt - 0.12 - start
        f = min(1.25, max(1.0, (len(x) / sr) / room))
        y = tempo(x, sr, f)
        i0 = int(start * SR)
        y = y[: max(0, len(track) - i0)]
        track[i0:i0 + len(y)] += y
        prev_end = start + len(y) / SR
        log.append({"i": s["i"], "kapsyen": [round(s["a"], 2), round(s["b"], 2)], "vo": [round(start, 2), round(prev_end, 2)],
                    "tempo": round(f, 3), "lewat": round(max(0, prev_end - nxt), 2)})
    track = track[: int(total * SR)]
    track *= 0.89 / np.abs(track).max()
    vo = D / "vo.wav"
    with wave.open(str(vo), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((track * 32767).astype("<i2").tobytes())
    (D / "timing.json").write_text(json.dumps(log, indent=1))
    for r in log:
        flag = "  <-- melimpah" if r["lewat"] > 0 else ""
        print(f"{r['i']:02d} kapsyen {r['kapsyen'][0]:6.2f}-{r['kapsyen'][1]:6.2f}  vo {r['vo'][0]:6.2f}-{r['vo'][1]:6.2f}  x{r['tempo']}{flag}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", D / "visual_tanpa_vo.mp4", "-i", vo,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                    "-shortest", "-movflags", "+faststart", OUT], check=True)
    print(OUT)


if __name__ == "__main__":
    main()
