"""Voiceover AI (Gemini TTS) dari lajur `voiceover` -> audio/V01.wav + audio/V01.json (masa setiap ayat).

    python scripts/vo.py synth all      # jana audio (5 video satu panggilan) -> audio/tts/V01/00.wav ...
    python scripts/vo.py place all      # susun ayat dalam 20s -> audio/V01.wav + audio/V01.json

Kuota percuma Gemini TTS = 10 panggilan sehari setiap model, jadi beberapa skrip dihantar dalam satu panggilan
dan audio dipotong semula ke ayat: jeda senyap dipadankan dengan panjang teks dijangka (pengaturcaraan dinamik).
Satu model + satu suara untuk semua video supaya bunyi konsisten. Kunci API disuntik oleh proxy.
"""
import base64
import json
import re
import subprocess
import sys
import time
import urllib.request
import wave

import numpy as np

from common import AUDIO, load_videos, speakable, write_json

MODEL = "elevenlabs:eleven_multilingual_v2"
VOICE = "Aisyah – Patient Malay School Tutor (JOCyls6Fdo4qfmTUnFrJ)"
STYLE = "Say in an upbeat, confident, fast-paced Malaysian Malay sales voice, with a short pause between sentences: "
SR = 44100
T0, GAP, LAST_END = 0.15, 0.12, 19.55      # VO mula 0.15s, jeda min antara ayat, mesti habis sebelum 19.55s
MAX_TEMPO = 1.35
CTA_AT, MAX_GAP = 16.25, 0.75              # ayat akhir mula ~16.25s (babak CTA); jeda maksimum antara ayat
BATCH = 4


def sentences(text):
    return [p for p in re.split(r"(?<=[.?!])\s+", text.strip()) if p]


def tts(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body = {"contents": [{"parts": [{"text": STYLE + text}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}}
    req = urllib.request.Request(url, json.dumps(body).encode(), method="POST", headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                part = json.load(r)["candidates"][0]["content"]["parts"][0]["inlineData"]
            data, mime = base64.b64decode(part["data"]), part.get("mimeType", "")
            if data[:4] == b"RIFF":                       # sesetengah model pulangkan wav penuh
                with wave.open(__import__("io").BytesIO(data)) as w:
                    return w.readframes(w.getnframes()), w.getframerate()
            rate = next((int(t.split("=")[1]) for t in mime.split(";") if t.strip().startswith("rate=")), 24000)
            return data, rate
        except urllib.error.HTTPError as e:
            if e.code == 429 or attempt == 3:
                raise SystemExit(f"TTS gagal ({e.code}): {e.read()[:300]}")
            print("  cuba lagi:", e, flush=True); time.sleep(5 * 2 ** attempt)


def pcm_to_float(pcm, rate):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "-",
                          "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"], input=pcm, capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(np.float32) / 32768


def pauses(x, hop=0.01, thr_db=-38, min_len=0.12):
    """Selang senyap [(mula, tamat)] dalam saat."""
    n = int(hop * SR)
    rms = np.sqrt(np.mean(x[: len(x) // n * n].reshape(-1, n) ** 2, axis=1) + 1e-12)
    quiet = 20 * np.log10(rms / (rms.max() + 1e-9)) < thr_db
    out, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if (j - i) * hop >= min_len:
                out.append((i * hop, j * hop))
            i = j
        else:
            i += 1
    return out


def split_by_text(x, texts, thr_db=-32, min_len=0.08, pause_w=0.6):
    """Potong audio x kepada len(texts) bahagian. Calon potongan = tengah setiap jeda; pilih N-1 potongan
    yang meminimumkan beza tempoh dengan jangkaan (nisbah aksara) dan utamakan jeda panjang."""
    total = len(x) / SR
    ps = pauses(x, thr_db=thr_db, min_len=min_len)
    lead = ps[0][1] if ps and ps[0][0] == 0 else 0.0
    tail = ps[-1][0] if ps and ps[-1][1] >= total - 0.02 else total
    inner = [p for p in ps if p[0] > lead + 0.05 and p[1] < tail - 0.05]
    cuts, plen = [(a + b) / 2 for a, b in inner], [b - a for a, b in inner]
    chars = np.array([len(t) for t in texts], float)
    exp = chars / chars.sum() * (tail - lead)
    N, K = len(texts), len(cuts)
    if K < N - 1:                                  # jeda tak cukup: bahagi ikut nisbah aksara
        edges = lead + np.concatenate([[0], np.cumsum(exp)])
        return [(edges[i], edges[i + 1]) for i in range(N)], exp
    pts = [lead] + cuts + [tail]
    INF = 1e18
    dp = np.full((N + 1, K + 2), INF); bk = np.zeros((N + 1, K + 2), int); dp[0][0] = 0
    for i in range(1, N + 1):
        ks = [K + 1] if i == N else range(i, K + 1)
        for k in ks:
            bonus = -pause_w * plen[k - 1] if k <= K else 0
            for j in range(i - 1, k):
                if dp[i - 1][j] >= INF:
                    continue
                c = dp[i - 1][j] + (pts[k] - pts[j] - exp[i - 1]) ** 2 / max(exp[i - 1], .3) + bonus
                if c < dp[i][k]:
                    dp[i][k], bk[i][k] = c, j
    idx, k = [K + 1], K + 1
    for i in range(N, 0, -1):
        k = bk[i][k]; idx.append(k)
    idx = idx[::-1]
    return [(pts[idx[i]], pts[idx[i + 1]]) for i in range(N)], exp


def trim(c, thr_db=-40):
    n = int(0.005 * SR)
    if len(c) < n * 4:
        return c
    rms = np.sqrt(np.mean(c[: len(c) // n * n].reshape(-1, n) ** 2, axis=1) + 1e-12)
    loud = np.where(20 * np.log10(rms / (rms.max() + 1e-9)) > thr_db)[0]
    a, b = max(0, loud[0] * n - n), min(len(c), (loud[-1] + 2) * n)
    c = c[a:b].copy(); f = int(0.008 * SR)
    c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
    return c


def save_wav(path, x):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def load_wav(path):
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768


def batch_text(grp):
    return "\n\n".join("\n".join(speakable(s) for s in sentences(v["voiceover"])) for v in grp)


def synth(vids):
    vids = [v for v in vids if not (AUDIO / "tts" / v["id"] / "00.wav").exists()]
    for g in range(0, len(vids), BATCH):
        grp = vids[g:g + BATCH]
        text = batch_text(grp)
        print(f"TTS {[v['id'] for v in grp]} ({len(text)} aksara)", flush=True)
        process(grp, *tts(text))


def process(grp, pcm, rate):
    """Audio satu panggilan (beberapa video) -> audio/tts/<id>/NN.wav untuk setiap ayat.
    Peringkat 1: potong ikut video (jeda panjang). Peringkat 2: potong ikut ayat dalam setiap video."""
    x = pcm_to_float(pcm, rate)
    vtexts = [" ".join(speakable(s) for s in sentences(v["voiceover"])) for v in grp]
    vb, _ = split_by_text(x, vtexts, thr_db=-38, min_len=0.35, pause_w=8.0)
    for v, (va, vb_) in zip(grp, vb):
        seg = x[int(va * SR):int(vb_ * SR)]
        ss = sentences(v["voiceover"])
        bounds, exp = split_by_text(seg, [speakable(s) for s in ss])
        d = AUDIO / "tts" / v["id"]; d.mkdir(parents=True, exist_ok=True)
        print(f"  {v['id']}: {va:6.2f}-{vb_:6.2f}s", flush=True)
        for i, (s, (a, b), e) in enumerate(zip(ss, bounds, exp)):
            c = trim(seg[int(a * SR):int(b * SR)])
            save_wav(d / f"{i:02d}.wav", c)
            flag = "" if 0.6 < (len(c) / SR) / e < 1.6 else "  <-- SEMAK"
            print(f"    [{i}] {len(c) / SR:5.2f}s (jangka {e:4.1f}s) {s}{flag}", flush=True)


def place(durs):
    """Masa mula setiap ayat. Ayat akhir (CTA) cuba mula pada CTA_AT supaya jatuh dalam babak CTA;
    ayat lain diregang sama rata (jeda GAP..MAX_GAP) dari T0."""
    n = len(durs)
    starts, t = [], T0
    tight = T0 + sum(durs) + GAP * (n - 1)
    if n < 2 or tight >= LAST_END - 0.05:
        for d in durs:
            starts.append(t); t += d + GAP
        return starts
    last = min(CTA_AT, LAST_END - durs[-1])
    gap = (last - 0.2 - T0 - sum(durs[:-1])) / max(1, n - 2) if n > 2 else 0
    gap = min(MAX_GAP, max(GAP, gap))
    for d in durs[:-1]:
        starts.append(t); t += d + gap
    starts.append(max(t - gap + GAP, last))     # t - gap = hujung ayat sebelum
    return starts


def tempo_fx(x, tempo):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                          "-af", f"atempo={tempo:.4f}", "-f", "f32le", "-"], input=x.astype("<f4").tobytes(),
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<f4")


def assemble(v):
    sents = sentences(v["voiceover"])
    clips = [load_wav(AUDIO / "tts" / v["id"] / f"{i:02d}.wav") for i in range(len(sents))]
    need = sum(len(c) for c in clips) / SR + GAP * (len(clips) - 1)
    tempo = 1.0
    if need > LAST_END - T0:
        tempo = need / (LAST_END - T0) * 1.01
        if tempo > MAX_TEMPO:
            raise SystemExit(f"{v['id']}: VO {need:.1f}s terlalu panjang (tempo {tempo:.2f}x)")
        clips = [tempo_fx(c, tempo) for c in clips]
    out = np.zeros(int(20.0 * SR), np.float32)
    cues = []
    for s, c, t in zip(sents, clips, place([len(c) / SR for c in clips])):
        i = int(t * SR)
        out[i:i + len(c)] += c[: len(out) - i]
        cues.append({"text": s, "start": round(t, 3), "end": round(t + len(c) / SR, 3)})
    out *= 0.89 / (np.abs(out).max() + 1e-9)
    save_wav(AUDIO / f"{v['id']}.wav", out)
    write_json(AUDIO / f"{v['id']}.json", {"id": v["id"], "model": MODEL, "voice": VOICE, "tempo": round(tempo, 3), "cues": cues})
    print(f"{v['id']}: {len(sents)} ayat {need:.2f}s -> habis {cues[-1]['end']:.2f}s (tempo {tempo:.2f}x)", flush=True)


if __name__ == "__main__":
    cmd, want = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "V01")
    vids = [v for v in load_videos() if want == "all" or v["id"] in want.split(",")]
    if cmd == "synth":
        synth(vids)
    for v in vids if cmd in ("place", "synth") else []:
        assemble(v)


def resplit(v):
    """Bina semula audio video dari potongan ayat sedia ada, kemudian potong semula dengan ambang terbaik."""
    ss = sentences(v["voiceover"])
    d = AUDIO / "tts" / v["id"]
    gap = np.zeros(int(0.25 * SR), np.float32)
    x = np.concatenate([np.concatenate([load_wav(d / f"{i:02d}.wav"), gap]) for i in range(len(ss))])
    best = None
    for thr in (-40, -36, -32, -28, -24):
        for ml in (0.06, 0.1, 0.15):
            b, exp = split_by_text(x, [speakable(s) for s in ss], thr_db=thr, min_len=ml)
            err = sum(abs(np.log(max(bb - aa, .05) / e)) for (aa, bb), e in zip(b, exp))
            if best is None or err < best[0]:
                best = (err, b, exp, thr, ml)
    err, b, exp, thr, ml = best
    print(f"{v['id']}: ralat {err:.2f} (thr {thr}, min {ml})")
    for i, (s, (aa, bb), e) in enumerate(zip(ss, b, exp)):
        c = trim(x[int(aa * SR):int(bb * SR)])
        save_wav(d / f"{i:02d}.wav", c)
        flag = "" if 0.6 < (len(c) / SR) / e < 1.6 else "  <-- SEMAK"
        print(f"    [{i}] {len(c) / SR:5.2f}s (jangka {e:4.1f}s) {s}{flag}")


PAUSE_W = 3.0      # ElevenLabs berhenti jelas antara ayat: utamakan jeda panjang sebagai sempadan


def gap_at(x, bounds):
    """Jumlah senyap (saat) di sekitar setiap sempadan ayat — lebih besar = potongan jatuh dalam jeda sebenar."""
    tot = 0.0
    for (a, b) in bounds[:-1]:
        i = int(b * SR); w = x[max(0, i - int(.15 * SR)): i + int(.15 * SR)]
        tot += float(np.mean(np.abs(w) < 0.01)) * 0.3
    return tot


def from_file(v, path):
    """Satu fail VO penuh (cth. ElevenLabs mp3) -> potong ikut ayat -> audio/tts/<id>/NN.wav"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-ar", str(SR), "-ac", "1", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, "<i2").astype(np.float32) / 32768
    ss = sentences(v["voiceover"])
    d = AUDIO / "tts" / v["id"]
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("*.wav"):
        f.unlink()
    best = None
    for thr in (-40, -36, -32, -28):
        for ml in (0.06, 0.1, 0.15):
            b, exp = split_by_text(x, [speakable(s) for s in ss], thr_db=thr, min_len=ml, pause_w=PAUSE_W)
            err = sum(abs(np.log(max(bb - aa, .05) / e)) for (aa, bb), e in zip(b, exp)) - PAUSE_W * gap_at(x, b)
            if best is None or err < best[0]:
                best = (err, b, exp)
    err, b, exp = best
    print(f"{v['id']}: {len(x) / SR:.2f}s, ralat potong {err:.2f}")
    for i, (s, (aa, bb), e) in enumerate(zip(ss, b, exp)):
        c = trim(x[int(aa * SR):int(bb * SR)])
        save_wav(d / f"{i:02d}.wav", c)
        flag = "" if 0.6 < (len(c) / SR) / e < 1.6 else "  <-- SEMAK"
        print(f"    [{i}] {len(c) / SR:5.2f}s (jangka {e:4.1f}s) {s}{flag}")
