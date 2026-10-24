"""Muzik latar + SFX untuk iklan Neo Plus (60 s), dijana dengan numpy — tiada isu lesen Meta.

    python neoplus/audio.py   ->  out/neoplus_music_sfx.wav

Masa SFX ikut garis masa dalam neoplus/index.html (V = mula setiap baris VO, T = mula babak).
"""
import pathlib
import wave

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
SR = 44100
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(11)

V = [0.3, 3.35, 7.8, 10.55, 15.65, 20.55, 25.4, 28.4, 33.95, 39.9, 45.45, 54.0]
T = dict(s1=0, s2=3.2, s3=7.65, s4=10.4, s5=15.5, s6=20.4, s7=25.25, s8=28.25, s9=33.8, s10=39.75, s11=45.3, s12=53.85)

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
LIFT = T["s10"]          # dram penuh masuk bila produk didedahkan
END_FADE = 58.6

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
for tw in [T["s2"] - .15, T["s3"] - .15, T["s4"] - .15, T["s5"] - .2, T["s6"] - .2, T["s7"] - .15,
           T["s8"] - .15, T["s9"] - .15, T["s11"] - .2, T["s12"] - .3]:
    add(whoosh(), tw, 0.18)
add(whoosh(0.7), T["s10"] - .4, 0.28)

# S1
add(pop(700, 0.18), 0.45, 0.3)
add(whoosh(0.3), 1.1, 0.08)
# S2 chat
for i in range(6):
    add(typing_blip(), V[1] + .3 + i * .12, 0.08)
add(pop(1250, 0.14), V[1] + 1.0, 0.32)
add(pop(1500, 0.12), V[1] + 3.3, 0.26)
# S3 peta
add(pop(600), T["s3"] + .3, 0.26)
add(pop(750), T["s3"] + 1.6, 0.26)
add(pop(1100, 0.15), V[2] + 1.2, 0.26)
# S4
add(whoosh(0.4), T["s4"], 0.14)
add(pop(900), V[3] + .5, 0.26)
add(pop(1050), V[3] + .9, 0.26)
add(whoosh(0.4), V[3] + 2.1, 0.14)
add(pop(1300, 0.15), V[3] + 2.4, 0.3)
add(pop(650, 0.2), V[3] + 3.3, 0.26)
# S5
for i in range(4):
    add(pop(800 + 120 * i, 0.1), T["s5"] + .6 + i * .12, 0.2, pan=-0.4 + 0.27 * i)
add(whoosh(0.35, up=False), V[4] + 1.6, 0.18)
add(whoosh(0.6, up=False), V[4] + 1.9, 0.12)
add(impact(1.0), V[4] + 2.8, 0.45)
add(shimmer(1.0), V[4] + 2.85, 0.08)
# S6 pulas, tekan, air
for i in range(4):
    add(click(0.03, 4500), V[5] + .15 + i * .2, 0.35)
add(pop(500, 0.15), V[5] + .9, 0.28)
add(click(0.05, 2000), V[5] + 1.0, 0.45)
add(pour(1.6), V[5] + 1.5, 0.22)
add(pop(900), V[5] + 2.95, 0.25)
add(buzz(), V[5] + 3.45, 0.18)
# S7
add(pop(1000, 0.15), T["s7"] + .1, 0.28)
add(pop(1400, 0.08), T["s7"] + .9, 0.15)
# S8 kopi, teh, susu
add(whoosh(0.3), V[7] - .05, 0.12)
add(stamp(), V[7] + 1.05, 0.35)
add(whoosh(0.3), V[7] + 1.65, 0.12)
add(stamp(), V[7] + 2.45, 0.35)
add(whoosh(0.3), V[7] + 3.0, 0.12)
for i, f in enumerate([1568, 1976, 2349]):
    add(bell(f, 0.6), V[7] + 3.8 + i * .08, 0.08)
# S9 duit syiling
add(pop(1100), T["s9"] + .05, 0.25)
for i, tw in enumerate([V[8] + 1.6, V[8] + 2.6, V[8] + 3.6]):
    add(bell(2637 + 200 * i, 0.5), tw + .25, 0.1)
    add(bell(3520 + 200 * i, 0.4), tw + .3, 0.06)
add(impact(0.9), V[8] + 4.8, 0.4)
# S10 pendedahan
add(impact(1.6), V[9] + 1.2, 0.55)
add(shimmer(1.4), V[9] + 1.25, 0.12)
for i in range(3):
    add(pop(800 + 150 * i), V[9] + 2.6 + i * .25, 0.26, pan=-0.3 + 0.3 * i)
# S11 promo
add(pop(1200), T["s11"] + .1, 0.3)
add(whoosh(0.35, up=False), V[10] + 2.4, 0.16)
add(impact(0.8), V[10] + 2.7, 0.35)
for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(f, 0.7), V[10] + 3.8 + i * 0.07, 0.07)
add(pop(1500, 0.1), V[10] + 4.3, 0.22)
add(impact(1.0), V[10] + 5.2, 0.45)
add(shimmer(1.2), V[10] + 5.3, 0.1)
add(pop(1000), V[10] + 6.9, 0.25)
add(pop(1150), V[10] + 7.3, 0.25)
# S12 CTA
add(pop(700, 0.2), T["s12"] + .1, 0.25)
add(shimmer(1.4), V[11] + 1.2, 0.08)
add(pop(900, 0.2), V[11] + 2.5, 0.3)
add(click(0.03, 3000), V[11] + 4.0, 0.5)
add(pop(1300, 0.1), V[11] + 4.05, 0.2)

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
with wave.open(str(out / "neoplus_music_sfx.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / "neoplus_music_sfx.wav")
