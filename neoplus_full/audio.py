"""Muzik latar + SFX untuk versi penuh iklan Neo Plus, dijana dengan numpy — tiada isu lesen Meta.

    python neoplus_full/audio.py   ->  out/neoplus_full_music_sfx.wav

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
S = dict(s1=0, s2=st(1) - .15, s3=st(3) - .25, s4=st(4) - .15, s4b=st(6) - .15, s5=st(7) - .25, s5b=st(8) - .15,
         s6=st(10) - .15, s7=st(12) - .15, s7b=st(13) - .25, s8=st(14) - .15, s9a=st(15) - .25, s9=st(16) - .15,
         s10=st(19) - .35, s10b=st(22) - .15, s10c=st(23) - .15, s11=st(24) - .25, s12=st(28) - .3)

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
LIFT = S["s10"]          # dram penuh masuk bila produk didedahkan
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
for k in ["s2", "s3", "s4", "s4b", "s5", "s5b", "s6", "s7", "s7b", "s8", "s9a", "s9", "s10b", "s10c", "s11", "s12"]:
    add(whoosh(), S[k] - .2, 0.16)
add(whoosh(0.7), S["s10"] - .4, 0.28)

# S1-S2
add(pop(700, 0.18), at(0, "penapis") - .15, 0.3)
for i in range(6):
    add(typing_blip(), S["s2"] + .7 + i * .12, 0.08)
add(pop(1250, 0.14), st(2), 0.32)
add(pop(1500, 0.12), en(2) - .1, 0.26)
# S3
add(pop(600), S["s3"] + .3, 0.26)
add(pop(750), at(3, "rasa") - .5, 0.26)
add(pop(1100, 0.15), at(3, "rasa"), 0.26)
# S4
add(whoosh(0.4), S["s4"], 0.14)
add(pop(900), at(4, "air panas"), 0.26)
add(pop(1050), at(4, "air sejuk"), 0.26)
add(whoosh(0.4), st(5) - .1, 0.14)
add(pop(1300, 0.15), st(5) + .2, 0.3)
for w, f in [("masak", 700), ("tunggu", 820), ("isi", 940)]:
    add(pop(f, 0.15), at(5, w) - .1, 0.26)
for i in range(6):
    add(click(0.02, 5000), at(5, "tunggu") + .1 + i * .18, 0.18)
add(pour(1.2), at(5, "isi") + .1, 0.12)
# S4b hadiah
add(pop(600, 0.2), S["s4b"] + .2, 0.25)
add(pop(1200, 0.14), at(6, "nak bantu") - .1, 0.25)
add(whoosh(0.35), at(6, "Nak") - .1, 0.14)
add(shimmer(1.2), at(6, "Nak") + .1, 0.12)
# S5
for i in range(4):
    add(pop(800 + 120 * i, 0.1), at(7, "paling") + .2 + i * .12, 0.2, pan=-0.4 + 0.27 * i)
add(whoosh(0.35, up=False), at(7, "Tapi") - .35, 0.18)
add(whoosh(0.6, up=False), at(7, "Tapi"), 0.12)
add(impact(1.0), at(7, "paling", 2), 0.45)
add(shimmer(1.0), at(7, "paling", 2) + .05, 0.08)
# S5b moden vs manual
add(whoosh(0.4), S["s5b"] + .1, 0.14)
for i in range(5):
    add(pop(1600 + 150 * (i % 3), 0.05), S["s5b"] + .6 + i * .33, 0.1)
add(pop(1300, 0.12), at(8, "moden") - .1, 0.22)
add(whoosh(0.4), st(9) - .1, 0.14)
for i in range(3):
    add(click(0.03, 4000), st(9) + .5 + i * .25, 0.3)
# S6 pulas, tekan, air
k1, k2, k3 = at(10, "Pulas"), at(10, "tekan"), at(10, "terus")
for i in range(4):
    add(click(0.03, 4500), k1 + .1 + i * .15, 0.35)
add(pop(500, 0.15), k2 - .05, 0.28)
add(click(0.05, 2000), k2, 0.45)
add(pour(1.6), k3 - .1, 0.22)
add(pop(1100, 0.12), at(10, "Itu"), 0.26)
add(pop(900), st(11), 0.25)
add(buzz(), at(11, "pening"), 0.18)
# S7
add(pop(1000, 0.15), S["s7"] + .1, 0.28)
add(pop(1400, 0.08), S["s7"] + .9, 0.15)
# S7b 3 suhu
for i, w in enumerate(["panas", "sejuk", "biasa"]):
    add(pop(700 + 200 * i, 0.15), at(13, w) - .15, 0.28, pan=-0.35 + 0.35 * i)
add(impact(0.9), at(13, "tersedia") - .1, 0.35)
add(shimmer(1.0), at(13, "tersedia"), 0.08)
# S8 kopi, teh, susu
add(whoosh(0.3), st(14) - .05, 0.12)
add(stamp(), at(14, "Tekan"), 0.35)
add(whoosh(0.3), at(14, "Nak buat teh") - .05, 0.12)
add(stamp(), at(14, "Tekan", 2), 0.35)
add(whoosh(0.3), at(14, "Nak bancuh") - .05, 0.12)
for i, f in enumerate([1568, 1976, 2349]):
    add(bell(f, 0.6), at(14, "Air") + i * .08, 0.08)
# S9a tabung
add(pop(600, 0.2), S["s9a"] + .3, 0.25)
for i in range(3):
    add(bell(2637 + 150 * i, 0.4), S["s9a"] + 1.1 + i * .7 + .5, 0.09)
add(impact(0.9), at(15, "Bajet") - .05, 0.4)
# S9 kongsi bayar
for w in ["Tahun ni", "Tahun depan", "Tahun seterusnya"]:
    add(bell(2637, 0.5), at(17, w) + .25, 0.1)
    add(bell(3520, 0.4), at(17, w) + .3, 0.06)
add(impact(0.9), st(18), 0.4)
# S10 pendedahan
cw = at(19, "Coway")
add(impact(1.6), cw + .1, 0.55)
add(shimmer(1.4), cw + .15, 0.12)
for i, w in enumerate(["Panas", "sejuk", "suhu bilik"]):
    add(pop(800 + 150 * i), at(20, w) - .1, 0.26, pan=-0.3 + 0.3 * i)
add(pop(1000, 0.12), st(21), 0.2)
# S10b keluarga
add(pop(700), at(22, "dua orang") - .1, 0.24)
add(pop(850), at(22, "dua orang") + .05, 0.24)
add(pop(1000), at(22, "adik") - .1, 0.24)
add(buzz(0.25), at(22, "terlalu"), 0.14)
add(bell(2093, 0.5), at(22, "besar"), 0.12)
# S10c
for i, w in enumerate(["cukup", "mudah", "praktikal"]):
    add(impact(0.5), at(23, w) - .05, 0.3)
    add(pop(1200 + 150 * i, 0.1), at(23, w) - .05, 0.2)
# S11 promo
add(pop(1200), at(24, "harga") - .15, 0.3)
add(impact(0.8), at(25, "lima") - .1, 0.35)
for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(f, 0.7), at(25, "sebulan") + i * 0.07, 0.07)
add(pop(1500, 0.1), at(25, "Jimat") - .05, 0.22)
add(whoosh(0.35, up=False), at(25, "seratus"), 0.16)
add(pop(1300, 0.12), at(26, "double") - .1, 0.26)
add(impact(1.0), at(26, "Tujuh") - .2, 0.45)
add(shimmer(1.2), at(26, "dua puluh"), 0.1)
add(pop(1000), st(27) - .05, 0.25)
add(pop(1150), at(27, "pemasangan") - .05, 0.25)
# S12 CTA
add(pop(700, 0.2), S["s12"] + .1, 0.25)
add(shimmer(1.4), at(29, "sedikit"), 0.08)
add(pop(900, 0.2), st(30) - .15, 0.3)
add(click(0.03, 3000), en(30) + .4, 0.5)
add(pop(1300, 0.1), en(30) + .45, 0.2)

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
with wave.open(str(out / "neoplus_full_music_sfx.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / "neoplus_full_music_sfx.wav")
