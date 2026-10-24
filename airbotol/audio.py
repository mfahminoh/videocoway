"""Muzik latar + SFX untuk iklan "Menyampah tengok air botol", dijana dengan numpy — tiada isu lesen Meta.

    python airbotol/audio.py   ->  out/airbotol_music_sfx.wav

Masa diambil daripada skrip dalam timeline.py: at(i, 'perkataan') = bila perkataan itu disebut,
sama seperti index.html, jadi SFX sentiasa selari dengan animasi.
"""
import json
import pathlib
import sys
import wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import timeline  # noqa: E402

ROWS = json.loads((HERE / "lines.json").read_text())   # ditulis oleh timeline.py (anggaran atau klip sebenar)
DUR = round(ROWS[-1]["end"] + timeline.HOLD, 2)
SR = 44100
N = int(SR * DUR)
rng = np.random.default_rng(11)


def st(i):
    return ROWS[i]["start"]


def en(i):
    return ROWS[i]["end"]


def at(i, word=None, occ=1):
    return timeline.at(ROWS, i, word, occ)


# sama seperti objek S dalam index.html
S = dict(s1=0, s2=st(1) - .15, s3=st(2) - .2, s4=st(3) - .15, s5=st(4) - .15, s6=st(5) - .15, s8=st(7) - .15, s9=st(8) - .15,
         s10=st(9) - .15, s11=st(10) - .15, s12=st(11) - .3, s13=st(12) - .15, s14=st(13) - .15, s15=st(14) - .2, s16=st(15) - .15,
         s17=st(16) - .3, s19=st(18) - .15, s20=st(19) - .25, s21=st(20) - .15)

L = np.zeros(N)
R = np.zeros(N)


def add(sig, t0, gain=1.0, pan=0.0):
    i = int(t0 * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(d, a=0.005, rel=None):
    t = tt(d)
    e = np.minimum(1, t / a) if a > 0 else np.ones_like(t)
    rel = rel or d
    return e * np.exp(-t / (rel / 5))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * np.asarray(cutoff, dtype=float) / SR) * np.ones_like(x)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


def keys(m, d):
    """Bunyi 'piano' lembut: beberapa harmonik dengan reput."""
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3) + 0.12 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 5)
    return x * np.minimum(1, t / 0.004) * np.exp(-t * 2.2)


# ---------------- Muzik: 92 BPM, F - C - Dm - Bb (hangat, kekeluargaan) ----------------
BPM = 92
BEAT = 60 / BPM
BAR = 4 * BEAT
CHORDS = [[41, 57, 60, 65, 69], [36, 55, 60, 64, 67], [38, 57, 62, 65, 69], [34, 53, 58, 62, 65]]
ARP = [[65, 69, 72, 69, 77, 72, 69, 72], [64, 67, 72, 67, 76, 72, 67, 72],
       [62, 65, 69, 65, 74, 69, 65, 69], [62, 65, 70, 65, 74, 70, 65, 70]]
LIFT = S["s17"]          # dram penuh masuk bila produk didedahkan
END_FADE = DUR - 1.6

bar = 0
t0 = 0.0
while t0 < DUR:
    ch = CHORDS[bar % 4]
    d = BAR + 0.5
    t = tt(d)
    pad = sum(np.sin(2 * np.pi * hz(m) * t + 0.25 * np.sin(2 * np.pi * 0.25 * t + m)) for m in ch[1:])
    penv = np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.5)
    add(pad * penv, t0, 0.028)
    # bas
    for b in (0, 2, 3) if t0 >= LIFT else (0, 2):
        bd = BEAT * (1.8 if b == 0 else 0.9)
        x = np.sin(2 * np.pi * hz(ch[0]) * tt(bd)) + 0.3 * np.sin(2 * np.pi * 2 * hz(ch[0]) * tt(bd))
        add(x * env(bd, 0.01, bd * 1.5), t0 + b * BEAT, 0.14 if t0 >= LIFT else 0.09)
    # arpeggio piano (1/8)
    for k in range(8):
        tn = t0 + k * BEAT / 2
        m = ARP[bar % 4][k] + (12 if t0 >= LIFT and k % 4 == 3 else 0)
        add(keys(m, 0.9), tn, 0.075 if k % 2 == 0 else 0.055, pan=0.3 if k % 2 else -0.3)
    # perkusi
    for b in range(4):
        tb = t0 + b * BEAT
        if tb >= LIFT:
            kd = 0.35
            ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR
            add(np.sin(ph) * env(kd, 0.001, 0.3), tb, 0.38)
            if b in (1, 3):
                sd = 0.18
                sn = rng.standard_normal(int(sd * SR)) * env(sd, 0.001, 0.15)
                add(lowpass(sn, 5000) + 0.4 * np.sin(2 * np.pi * 190 * tt(sd)) * env(sd, 0.001, 0.08), tb, 0.10)
        # shaker 1/8 sepanjang lagu (lebih kuat selepas LIFT)
        for h in (0, 0.5):
            hd = 0.07
            add(rng.standard_normal(int(hd * SR)) * env(hd, 0.004, 0.05) * np.linspace(0.4, 1, int(hd * SR)),
                tb + h * BEAT, 0.035 if tb < LIFT else 0.05, pan=0.25)
    bar += 1
    t0 += BAR

music_L, music_R = L.copy(), R.copy()
L[:] = 0
R[:] = 0


# ---------------- SFX ----------------
def whoosh(d=0.5, up=True):
    t = tt(d)
    x = rng.standard_normal(len(t))
    f = (400 + 5000 * (t / d) ** 2) if up else (5500 - 5000 * (t / d) ** 0.5)
    return lowpass(x, f) * np.sin(np.pi * t / d) ** 2


def pop(f=900, d=0.12):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR
    return np.sin(ph) * env(d, 0.001, 0.1)


def impact(d=1.2):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR
    return np.sin(ph) * env(d, 0.002, 1.0) + 0.3 * lowpass(rng.standard_normal(len(t)), 1500) * env(d, 0.001, 0.3)


def bell(f, d=0.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, 0.002, 0.5)


def click(d=0.025, cut=6000):
    return lowpass(rng.standard_normal(int(d * SR)), cut) * env(d, 0.0005, 0.015)


def shimmer(d=1.0):
    t = tt(d)
    y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([2093, 2637, 3136, 4186]))
    return y * np.minimum(1, t / 0.02)


def pour(d=1.4):
    t = tt(d)
    x = rng.standard_normal(len(t))
    y = lowpass(x, 1800 + 900 * np.sin(2 * np.pi * 7 * t) ** 2) - lowpass(x, 300)
    return y * np.minimum(1, t / 0.08) * np.minimum(1, (d - t) / 0.3)


def stamp():
    x = impact(0.5) * 0.8
    c = click(0.04, 2500) * 2
    x[:len(c)] += c
    return x


def buzz(d=0.35):
    t = tt(d)
    return np.sign(np.sin(2 * np.pi * 110 * t)) * 0.3 * env(d, 0.005, 0.3)


def typing_blip():
    return pop(1800, 0.05)


# peralihan babak
for k in ["s2", "s3", "s4", "s5", "s6", "s8", "s9", "s10", "s11", "s13", "s14", "s15", "s16", "s19", "s20", "s21"]:
    add(whoosh(), S[k] - .2, 0.16)
add(whoosh(0.7), S["s12"] - .4, 0.24)
add(whoosh(0.7), S["s17"] - .4, 0.28)

# S1 hook
add(impact(1.2), at(0, "menyampah") - .1, 0.55)
add(buzz(0.4), at(0, "menyampah") + .1, 0.12)
# S2 nota
add(pop(700, 0.18), S["s2"] + .05, 0.28)
# S3
add(pop(900), at(2, "kahwin") - .2, 0.26)
add(pop(1100), at(2, "kahwin") + .5, 0.26)
add(whoosh(0.5), at(2, "Awal") - .1, 0.14)
add(bell(1976, 0.5), at(2, "senang") - .1, 0.12)
# S4 orbit
add(shimmer(1.0), S["s4"] + .2, 0.06)
# S5 angkut
for i in range(3):
    add(impact(0.4), at(4, "angkut") - .3 + i * .45, 0.18)
# S6-7 kiraan
for i in range(16):
    add(click(0.02, 5000), at(5, "Empat") - .3 + i * .07, 0.18)
for i, t0 in enumerate([at(5, "dua kotak") - .2, at(5, "dua kotak") + .05, at(6, "tiga") - .1]):
    add(stamp(), t0 + .35, 0.3)
add(pop(1300, 0.12), at(6, "anak") - .1, 0.26)
for i in range(10):
    add(click(0.02, 5000), at(6, "tiga") + i * .06, 0.18)
# S8 stock hunting
add(impact(0.6), at(7, "stock") - .1, 0.3)
for i in range(3):
    add(pop(800 + 200 * i), at(7, "Cari") - .2 + i * .6, 0.24)
add(buzz(0.3), at(7, "harga") - .1, 0.14)
# S9 brand
for i in range(2):
    add(stamp(), at(8, "brand lain") + i * .2, 0.28)
# S10 dapur
for i in range(12):
    add(impact(0.25), S["s10"] + .5 + i * (at(9, "Makan") - S["s10"] - .5) / 12 + .3, 0.12)
add(impact(0.6), at(9, "Makan") - .05, 0.3)
add(pop(900), at(9, "tak cantik") - .1, 0.22)
add(pop(1000), at(9, "sorok") - .2, 0.22)
# S11 air panas
add(pour(1.0) * 0.4, at(10, "jerang") - .4, 0.1)
for i in range(6):
    add(click(0.02, 5000), at(10, "jerang") + i * .25, 0.14)
add(bell(1568, 0.4), at(10, "boiler") - .2, 0.1)
# S12 kampung
add(shimmer(1.2), at(11, "Coway") - .3, 0.1)
add(pop(700, 0.2), at(11, "Coway") - .5, 0.25)
# S13 dialog
add(pop(1200, 0.12), S["s13"] + .1, 0.25)
add(pop(900, 0.2), at(12, "sonang") - .25, 0.32)
add(bell(2349, 0.4), at(12, "sonang") + .1, 0.08)
# S14 sejuk
add(pop(1500, 0.08), at(13, "sedap") - .15, 0.2)
for i in range(3):
    add(bell(3000 + 400 * i, 0.3), at(13, "Air sejuk") + i * .07, 0.05)
add(stamp(), at(13, "peti ais"), 0.28)
# S15 mendung
add(pour(1.8) * 0.5, at(14, "kotak"), 0.08)
add(buzz(0.5), at(14, "makin") - .1, 0.1)
# S16 tak tahan
for i in range(3):
    add(click(0.03, 3000), at(15, "Dua") + i * .4, 0.3)
add(impact(1.2), at(15, "Aku") - .2, 0.55)
add(whoosh(0.6), at(15, "Aku") - .2, 0.2)
# S17-18 Neo Plus
add(impact(1.6), at(16, "Kowei") + .15, 0.5)
add(shimmer(1.4), at(16, "Kowei") + .2, 0.12)
for i, w in enumerate(["Air panas", "air sejuk", "suhu bilik"]):
    add(pop(800 + 150 * i), at(17, w) - .1, 0.26, pan=-0.3 + 0.3 * i)
add(pop(1000, 0.12), at(17, "keluarga") - .2, 0.2)
# S19 harga
add(pop(1100), S["s19"] + .1, 0.28)
add(impact(1.0), at(18, "Tapi") - .1, 0.45)
for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(f, 0.7), at(18, "dua puluh") + i * 0.07, 0.07)
# S20 berbaloi
add(stamp(), at(19, "berbaloi") - .1, 0.45)
add(shimmer(1.0), at(19, "berbaloi"), 0.08)
# S21 CTA
add(whoosh(0.5, up=False), at(20, "WhatsApp") - .6, 0.16)
add(pop(900, 0.2), at(20, "WhatsApp") - .2, 0.3)
add(click(0.03, 3000), en(20) + .5, 0.5)
add(pop(1300, 0.1), en(20) + .55, 0.2)

sfx_L, sfx_R = L, R

# ---------------- Campur ----------------
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.3) * np.clip((DUR - t) / (DUR - END_FADE), 0, 1)
mL = (music_L + sfx_L) * fade
mR = (music_R + sfx_R) * fade
peak = max(np.abs(mL).max(), np.abs(mR).max())
mL, mR = mL / peak * 0.89, mR / peak * 0.89

out = ROOT / "out"
out.mkdir(exist_ok=True)
data = (np.stack([mL, mR], 1) * 32767).astype("<i2")
with wave.open(str(out / "airbotol_music_sfx.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / "airbotol_music_sfx.wav")
