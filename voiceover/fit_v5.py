"""Fit a style video (src/v5/<name>.html) to a real voiceover recording.

    python voiceover/fit_v5.py v1_premium            # uses voiceover/source/v1_premium.wav

1. Finds pauses in the recording and assigns one speech segment per script line (dynamic
   programming on text length + punctuation, same idea as align.py).
2. Tightens the pacing: each line gets an output window = max(speech + 0.4s, 60% of its
   original animation window); VO is placed 0.1s after each cut.
3. Writes out/v5/fit_<name>.json  {duration, out[], anim[], segs[]}  (output-time -> animation-time)
   and out/v5/vo_<name>.wav (placed VO, 44.1 kHz). build_v5.py picks both up automatically.
"""
import json
import pathlib
import re
import subprocess
import sys

import imageio_ffmpeg
import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
SR = 44100
FF = imageio_ffmpeg.get_ffmpeg_exe()

# Baris skrip dan tetingkap animasi asal (saat) bagi setiap video.
E = lambda S: [  # kad promo dikongsi (engine.js addEndcard), relatif S
    ("Sekarang ada promosi diskaun, serendah tujuh puluh empat ringgit je sebulan.", S, S + 5.0),
    ("Ganda lagi dengan rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan!", S + 5.0, S + 10.1),
    ("Last call untuk promo ni.", S + 10.1, S + 11.2),
]
SCRIPTS = {
    "v1_premium": dict(S=20.5, end=38.3, lines=[
        ("Rumah dah cantik.", 0.0, 3.0),
        ("Penapis air pun kena setaraf.", 3.0, 5.5),
        ("Coway Villaem 3. Model premium, high spec.", 5.5, 8.0),
        ("Tangki paling besar.", 8.0, 10.5),
        ("Lebih lapan pilihan suhu.", 10.5, 13.0),
        ("Cukup untuk seisi keluarga.", 13.0, 15.5),
        ("Dan paling tahan lasak.", 15.5, 18.0),
        ("Beli sekali, tak perlu dua kali.", 18.0, 20.5),
        *E(20.5),
        ("Rumah premium, penapis air pun premium. WhatsApp saya sekarang.", 31.7, 36.8),
    ]),
    "v2_upgrade": dict(S=19.0, end=36.8, lines=[
        ("Penapis air kat rumah dah habis bayar?", 0.0, 3.0),
        ("Tapi dah bertahun pakai, tangki kecil, suhu pun terhad.", 3.0, 6.0),
        ("Ni masa untuk upgrade ke model lebih power.", 6.0, 8.5),
        ("Lebih lapan pilihan suhu.", 8.5, 11.0),
        ("Tangki paling besar.", 11.0, 13.5),
        ("Model premium, high spec.", 13.5, 16.0),
        ("Coway Villaem 3. Upgrade yang memang berbaloi.", 16.0, 19.0),
        *E(19.0),
        ("Dah habis bayar? Jom upgrade. WhatsApp saya sekarang.", 30.2, 35.3),
    ]),
    "v3_family": dict(S=17.0, end=34.8, lines=[
        ("Keluarga besar? Air panas selalu tak cukup?", 0.0, 3.5),
        ("Asyik kena tunggu, nak masak pun kena bergilir.", 3.5, 6.5),
        ("Villaem 3 ada tangki paling besar, sebelas perpuluhan empat liter.", 6.5, 9.5),
        ("Air panas, suhu bilik, sejuk, semua cukup.", 9.5, 12.0),
        ("Lebih lapan pilihan suhu, untuk semua orang dalam rumah.", 12.0, 14.5),
        ("Coway Villaem 3. Model premium untuk keluarga.", 14.5, 17.0),
        *E(17.0),
        ("Satu mesin, cukup satu keluarga. WhatsApp saya sekarang.", 28.2, 33.3),
    ]),
    "v4_kinetic": dict(S=16.4, end=34.2, lines=[   # dipecah ikut perkataan di skrin (kinetic)
        ("Kalau beli,", 0.0, 1.2),
        ("biar puas hati.", 1.2, 2.5),
        ("Jangan alang-alang.", 2.5, 3.9),
        ("Beli murah?", 3.9, 5.0),
        ("Rosak.", 5.0, 5.7),
        ("Repair.", 5.7, 6.4),
        ("Rosak lagi.", 6.4, 7.2),
        ("Beli baru. Rugi.", 7.2, 8.4),
        ("Sekali beli, pakai lama.", 8.4, 9.8),
        ("Penapis air pun sama.", 9.8, 11.0),
        ("High spec.", 11.0, 11.8),
        ("Tangki paling besar.", 11.8, 12.5),
        ("Lebih lapan pilihan suhu.", 12.5, 13.2),
        ("Paling tahan lasak.", 13.2, 14.6),
        ("Coway Villaem 3.", 14.6, 16.4),
        *E(16.4),
        ("Kalau beli, biar puas hati. WhatsApp saya sekarang.", 27.6, 32.7),
    ]),
    "v6_tradein": dict(S=35.0, end=44.0, lines=[
        ("Orang tua-tua kata, alah membeli, menang memakai.", 0.0, 4.2),
        ("Ada seorang customer saya, beli Coway Villaem tahun dua ribu enam belas.", 4.2, 9.2),
        ("Sepuluh tahun pakai, sampai sekarang masih okay, masih steady.", 9.2, 15.2),
        ("Tahun ni dia pindah rumah. Alang-alang pindah, dia nak tukar model baru.", 15.2, 20.4),
        ("Dan dia pilih model yang sama, versi terbaru. Villaem 3.", 20.4, 26.4),
        ("Dia trade-in unit lama, dapat harga diskaun.", 26.4, 31.4),
        ("Sepuluh tahun pakai, masih puas hati. Betul lah, alah membeli, menang memakai.", 31.4, 35.0),
        ("Kalau anda pun nak tukar atau upgrade penapis air, trade-in unit lama, dapat harga diskaun. WhatsApp saya sekarang.", 35.0, 42.0),
    ]),
}


def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def pauses(x):
    hop = int(SR * .01); n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    sil = db < db.max() - 40
    v = np.where(~sil)[0]; T0, T1 = v[0] * .01, (v[-1] + 1) * .01
    P, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if (j - i) * .01 >= .15 and T0 < i * .01 and j * .01 < T1: P.append((i * .01, j * .01))
            i = j
        else: i += 1
    return T0, T1, P


def align(texts, T0, T1, P):
    units = np.array([len(re.sub(r"[^a-z0-9]", "", t.lower())) for t in texts], float)
    puncts = [len(re.findall(r"[,.!?]", t.strip()[:-1])) for t in texts]
    speech = lambda a, b: (b - a) - sum(max(0, min(b, q) - max(a, p)) for p, q in P)
    rate = speech(T0, T1) / units.sum()
    starts = [T0] + [q for p, q in P]; ends = [p for p, q in P] + [T1]
    K, M = len(texts), len(P)
    def cost(k, a, b, inner, e):
        exp = units[k] * rate; d = speech(a, b)
        bonus = 1.2 * (P[e][1] - P[e][0]) if e < M else 0      # sempadan ayat biasanya jeda panjang
        return ((d - exp) / max(exp, 1.0)) ** 2 * 4 + .3 * abs(inner - puncts[k]) - bonus
    INF = 1e18; C = np.full((K, M + 1), INF); B = np.zeros((K, M + 1), int)
    for e in range(M + 1):
        C[0][e] = cost(0, T0, ends[e], e, e)
    for k in range(1, K):
        for e in range(k, M + 1):
            for s in range(k - 1, e):
                if C[k - 1][s] < INF:
                    c = C[k - 1][s] + cost(k, starts[s + 1], ends[e], e - s - 1, e)
                    if c < C[k][e]: C[k][e], B[k][e] = c, s
    segs, e = [], M
    for k in range(K - 1, -1, -1):
        s = B[k][e] if k > 0 else -1
        segs.append((T0 if k == 0 else starts[s + 1], ends[e])); e = s
    return segs[::-1]


def main(name):
    spec = SCRIPTS[name]
    src = ROOT / "voiceover" / "source" / f"{name}.wav"
    x = load(src)
    T0, T1, P = pauses(x)
    texts = [l[0] for l in spec["lines"]]
    segs = align(texts, T0, T1, P)

    out_pts, anim_pts, placed = [0.0], [0.0], []
    o = 0.0
    for (text, a0, a1), (s, e) in zip(spec["lines"], segs):
        win = max((e - s) + 0.4, (a1 - a0) * 0.6)
        if out_pts[-1] != o or anim_pts[-1] != a0:
            out_pts.append(o); anim_pts.append(a0)
        placed.append((o + 0.1, s, e))
        o += win
        out_pts.append(o); anim_pts.append(a1)
    tail = 1.5
    out_pts.append(o + tail); anim_pts.append(spec["end"])
    dur = round(o + tail, 2)

    vo = np.zeros(int(dur * SR))
    for at, s, e in placed:
        c = x[max(0, int((s - .04) * SR)): int((e + .12) * SR)].copy()
        f = int(.01 * SR); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
        i = int(at * SR); c = c[: len(vo) - i]; vo[i:i + len(c)] += c
    vo *= .9 / (np.abs(vo).max() + 1e-9)
    outdir = ROOT / "out" / "v5"; outdir.mkdir(parents=True, exist_ok=True)
    import wave
    with wave.open(str(outdir / f"vo_{name}.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((vo * 32767).astype("<i2").tobytes())
    (outdir / f"fit_{name}.json").write_text(json.dumps({"duration": dur, "out": out_pts, "anim": anim_pts,
                                                          "segs": [[round(s, 2), round(e, 2)] for s, e in segs]}))
    print(f"{name}: recording {len(x) / SR:.1f}s -> video {dur}s")
    for (text, a0, a1), (at, s, e) in zip(spec["lines"], placed):
        print(f"  out {at:6.2f}  vo {s:6.2f}-{e:6.2f} ({e - s:4.2f}s)  anim {a0:5.1f}-{a1:5.1f}  {text[:55]}")


if __name__ == "__main__":
    main(sys.argv[1])
