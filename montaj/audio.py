"""Muzik + SFX untuk montaj promo 15s (120 BPM: satu potongan = 2 ketukan). numpy sahaja, tiada lesen.

    python montaj/audio.py  ->  out/montaj_music.wav
"""
import pathlib
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
SR = 44100
DUR = 15.0
N = int(SR * DUR)
rng = np.random.default_rng(3)
CUT = 1.0          # panjang setiap shot
SHOTS = 10         # 0-10s montaj, 10-15s kad promo
END = SHOTS * CUT

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


def keys(m, d):
    t = tt(d)
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 3)
    return x * np.minimum(1, t / 0.004) * np.exp(-t * 3.5)


# ---------------- Muzik: 120 BPM, C - Am - F - G, rancak ----------------
BEAT = 0.5
CHORDS = [[48, 60, 64, 67], [45, 57, 60, 64], [41, 57, 60, 65], [43, 55, 59, 62]]
ARP = [[72, 76, 79, 84], [69, 72, 76, 81], [65, 69, 72, 77], [67, 71, 74, 79]]
bar = 0
t0 = 0.0
while t0 < DUR:
    ch = CHORDS[bar % 4]
    d = 4 * BEAT + 0.2
    t = tt(d)
    pad = sum(np.sin(2 * np.pi * hz(m) * t) for m in ch[1:]) * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.2)
    add(pad, t0, 0.02)
    for b in range(4):
        tb = t0 + b * BEAT
        # kick setiap ketukan, snare/clap pada 2 & 4, hi-hat 1/8
        kd = 0.3
        ph = 2 * np.pi * np.cumsum(50 + 120 * np.exp(-tt(kd) * 32)) / SR
        add(np.sin(ph) * env(kd, 0.001, 0.25), tb, 0.42)
        for h in (0, .5):
            hd = 0.05
            add(rng.standard_normal(int(hd * SR)) * env(hd, 0.001, 0.035), tb + h * BEAT, 0.05 if h else 0.03, pan=0.3)
        if b in (1, 3):
            sd = 0.16
            add(lowpass(rng.standard_normal(int(sd * SR)), 6000) * env(sd, 0.001, 0.12), tb, 0.14)
        bd = BEAT * 0.45
        for k in (0, .5):
            x = np.sin(2 * np.pi * hz(ch[0] - 12) * tt(bd)) + 0.3 * np.sin(2 * np.pi * hz(ch[0]) * tt(bd))
            add(x * env(bd, 0.005, bd * 1.2), tb + k * BEAT, 0.13)
        for k in range(2):
            add(keys(ARP[bar % 4][(b * 2 + k) % 4], 0.4), tb + k * BEAT / 2, 0.05, pan=-0.3 if k else 0.3)
    bar += 1
    t0 += 4 * BEAT

music_L, music_R = L.copy(), R.copy()
L[:] = 0
R[:] = 0


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


def riser(d):
    t = tt(d)
    return lowpass(rng.standard_normal(len(t)), 300 + 6000 * (t / d) ** 2) * (t / d) ** 2


# whoosh + klik pada setiap potongan
for i in range(1, SHOTS):
    add(whoosh(0.3), i * CUT - 0.18, 0.12, pan=-0.4 if i % 2 else 0.4)
add(impact(1.0), 0.02, 0.4)                 # buka dengan hentakan
add(riser(1.4), END - 1.4, 0.12)
add(impact(1.6), END, 0.6)                  # masuk kad promo
add(shimmer(1.4), END + .05, 0.12)
add(pop(1200), END + .1, 0.3)               # DOUBLE PROMO
add(pop(900), END + .6, 0.28)               # RM59
add(impact(0.8), END + 1.0, 0.4)            # kad RM20
for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(f, 0.7), END + 1.05 + i * 0.07, 0.07)
add(pop(1000), END + 1.8, 0.25)             # percuma
add(pop(900, 0.2), END + 2.4, 0.3)          # butang
add(click(), END + 3.45, 0.5)               # tekan

sfx_L, sfx_R = L, R
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.05) * np.clip((DUR - t) / 0.8, 0, 1)
mL = (music_L + sfx_L) * fade
mR = (music_R + sfx_R) * fade
peak = max(np.abs(mL).max(), np.abs(mR).max())
mL, mR = mL / peak * 0.89, mR / peak * 0.89
data = (np.stack([mL, mR], 1) * 32767).astype("<i2")
(ROOT / "out").mkdir(exist_ok=True)
with wave.open(str(ROOT / "out" / "montaj_music.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", ROOT / "out" / "montaj_music.wav")
