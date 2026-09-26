"""Synthesize a royalty-free music bed + sound effects matched to the animation timeline.

Output: out/music_sfx.wav (Villaem 3 ad) or out/best3_music_sfx.wav (--ad best3), 44.1 kHz stereo.
Everything is generated with numpy, so there are no licensing concerns for Meta Ads.
"""
import argparse
import pathlib
import wave

import numpy as np

ROOT = pathlib.Path(__file__).parent
SR = 44100
ap = argparse.ArgumentParser()
ap.add_argument("--ad", choices=["villaem3", "best3"], default="villaem3")
AD = ap.parse_args().ad
# ad -> (duration, when kick & hats come in, music fade-out start, output file)
DUR, REVEAL, END_FADE, OUTFILE = {
    "villaem3": (29.5, 8.6, 28.3, "music_sfx.wav"),
    "best3": (30.0, 4.0, 29.0, "best3_music_sfx.wav"),
}[AD]
N = int(SR * DUR)
rng = np.random.default_rng(7)

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
    # one-pole low-pass; cutoff may be scalar or array
    a = np.exp(-2 * np.pi * np.asarray(cutoff, dtype=float) / SR) * np.ones_like(x)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def hz(midi):
    return 440 * 2 ** ((midi - 69) / 12)


# ---------------- Muzik: 108 BPM, C - G - Am - F ----------------
BPM = 108
BEAT = 60 / BPM
BAR = 4 * BEAT
CHORDS = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]
ARP = [[72, 76, 79, 76], [71, 74, 79, 74], [72, 76, 81, 76], [69, 72, 77, 72]]

bar_idx = 0
t0 = 0.0
while t0 < DUR:
    ch = CHORDS[bar_idx % 4]
    # pad lembut
    d = BAR + 0.4
    t = tt(d)
    pad = sum(np.sin(2 * np.pi * hz(m) * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) for m in ch[1:])
    pad += 0.5 * np.sin(2 * np.pi * hz(ch[0]) * t)
    penv = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    add(pad * penv, t0, 0.035)
    # bass
    for b in range(4):
        tb = t0 + b * BEAT
        bd = BEAT * 0.9
        x = np.sin(2 * np.pi * hz(ch[0] - 12) * tt(bd))
        add(x * env(bd, 0.01, bd * 1.6), tb, 0.16 if tb >= REVEAL else 0.08)
    # pluck arpeggio (1/8 nota)
    for k in range(8):
        tn = t0 + k * BEAT / 2
        m = ARP[bar_idx % 4][k % 4] + (12 if k >= 4 and tn >= REVEAL else 0)
        dd = 0.45
        x = np.sin(2 * np.pi * hz(m) * tt(dd)) + 0.3 * np.sin(2 * np.pi * 2 * hz(m) * tt(dd))
        add(x * env(dd, 0.003, 0.35), tn, 0.06, pan=0.35 if k % 2 else -0.35)
    # dram
    for b in range(4):
        tb = t0 + b * BEAT
        if tb >= REVEAL:
            kd = 0.35
            ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR
            add(np.sin(ph) * env(kd, 0.001, 0.3), tb, 0.45)
            hd = 0.06
            add(rng.standard_normal(int(hd * SR)) * env(hd, 0.001, 0.05), tb + BEAT / 2, 0.05, pan=0.2)
            if b in (1, 3):
                sd = 0.18
                sn = rng.standard_normal(int(sd * SR)) * env(sd, 0.001, 0.15)
                add(lowpass(sn, 5000) + 0.4 * np.sin(2 * np.pi * 190 * tt(sd)) * env(sd, 0.001, 0.08), tb, 0.12)
        else:
            if b in (1, 3):  # klik jari lembut di bahagian cerita
                cd = 0.05
                add(lowpass(rng.standard_normal(int(cd * SR)), 3500) * env(cd, 0.001, 0.03), tb, 0.12)
    bar_idx += 1
    t0 += BAR

music_L, music_R = L.copy(), R.copy()
L[:] = 0
R[:] = 0


# ---------------- SFX ----------------
def whoosh(d=0.55, up=True):
    t = tt(d)
    x = rng.standard_normal(len(t))
    f = (400 + 5000 * (t / d) ** 2) if up else (5500 - 5000 * (t / d) ** 0.5)
    y = lowpass(x, f)
    return y * np.sin(np.pi * t / d) ** 2


def pop(f=900, d=0.12):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR
    return np.sin(ph) * env(d, 0.001, 0.1)


def impact(d=1.2):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR
    boom = np.sin(ph) * env(d, 0.002, 1.0)
    return boom + 0.3 * lowpass(rng.standard_normal(len(t)), 1500) * env(d, 0.001, 0.3)


def bell(f, d=0.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, 0.002, 0.5)


def click():
    d = 0.02
    return lowpass(rng.standard_normal(int(d * SR)), 6000) * env(d, 0.0005, 0.015)


def shimmer(d=1.0):
    t = tt(d)
    y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([2093, 2637, 3136, 4186]))
    return y * np.minimum(1, t / 0.02)


def sfx_villaem3():
    for tw in [3.85, 8.3, 11.25, 13.65, 17.45, 19.55, 25.85]:
        add(whoosh(), tw, 0.22, pan=0)
    add(impact(), 0.3, 0.55)                          # "3" hentak
    for i, tk in enumerate([1.25, 1.47, 1.69]):         # customer muncul
        add(pop(500 + 120 * i), tk, 0.35, pan=-0.4 + 0.4 * i)
    for i in range(int(1.3 * 18)):                     # taip kapsyen
        add(click(), 2.0 + i / 18 + rng.uniform(0, .02), 0.18)
    for i in range(3):                                 # beg
        add(pop(700 + 100 * i), 4.6 + i * .15, 0.28)
    add(whoosh(0.35, up=False), 5.35, 0.18)            # garis potong
    add(pop(1300, 0.15), 6.85, 0.3)                    # TAHAN LAMA
    add(pop(1500, 0.15), 7.5, 0.3)                     # PUAS HATI
    add(impact(1.6), 10.05, 0.6)                       # pendedahan Villaem 3
    add(shimmer(1.4), 10.1, 0.12)
    add(pop(1100), 11.45, 0.25)                        # HIGH SPEC
    for i in range(4):                                 # chip suhu
        add(pop(800 + 150 * i), 14.9 + i * .55, 0.3, pan=-0.3 if i % 2 == 0 else 0.3)
    add(pop(600, 0.2), 17.65, 0.3)
    add(bell(1568, 0.5), 18.2, 0.12)                   # tick perisai
    add(pop(1200), 19.95, 0.3)                         # PROMO
    add(impact(0.8), 20.3, 0.35)                       # RM20
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):   # cha-ching RM84
        add(bell(f, 0.7), 22.3 + i * 0.07, 0.07)
    add(impact(0.8), 22.35, 0.3)
    add(pop(1000), 23.7, 0.28)
    add(pop(1150), 24.4, 0.28)
    add(shimmer(1.6), 26.4, 0.12)
    add(pop(900, 0.2), 27.4, 0.3)                      # butang


def sfx_best3():
    for tw in [3.7, 9.55, 16.05, 21.9, 27.55]:        # peralihan babak
        add(whoosh(), tw, 0.22)
    add(impact(), 0.3, 0.5)                           # PASANG
    add(impact(0.8), 0.55, 0.3)                       # COWAY
    add(pop(1400, 0.15), 1.0, 0.3)                    # "?"
    for i in range(3):                                # 3 produk jatuh
        add(pop(500 + 150 * i), 2.3 + i * .2, 0.35, pan=-0.4 + 0.4 * i)
    # --- Neon ---
    add(pop(1100), 4.3, 0.28)
    add(shimmer(1.2), 4.6, 0.1)
    add(pop(700, 0.2), 5.65, 0.35)                    # pelekat MAMPU MILIK
    add(pop(1300, 0.15), 7.25, 0.3)                   # 3 SUHU
    for i in range(3):                                # titisan
        add(pop(900 + 200 * i, 0.1), 7.85 + i * .18, 0.25, pan=-0.3 + 0.3 * i)
    # --- Villaem 3 ---
    add(pop(1100), 10.1, 0.28)
    add(shimmer(1.4), 10.75, 0.12)                    # PREMIUM
    add(pop(700, 0.2), 11.35, 0.35)                   # GENERASI 3
    for i, tk in enumerate([12.15, 13.1, 13.95, 14.75]):
        add(pop(800 + 120 * i), tk, 0.28, pan=-0.2)
    # --- Ais ---
    add(pop(1100), 16.6, 0.28)
    add(shimmer(1.4), 16.8, 0.12)
    add(pop(700, 0.2), 17.55, 0.35)                   # PALING SPECIAL
    add(pop(1300, 0.15), 17.85, 0.28)
    for c in range(3):                                # pagi / petang / malam
        t0 = 19.0 + c * .55
        add(pop(600 + 150 * c, 0.15), t0 + .05, 0.25, pan=-0.4 + 0.4 * c)
        for j in range(3):                            # ketulan ais "ting"
            add(bell(2600 + 350 * j + 150 * c, 0.3), t0 + .45 + j * .12, 0.05, pan=-0.4 + 0.4 * c)
    # --- Promo ---
    add(pop(1200), 22.35, 0.3)
    add(impact(0.8), 22.65, 0.35)                     # RM20
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
        add(bell(f, 0.7), 23.15 + i * 0.07, 0.07)
    add(pop(900, 0.2), 24.2, 0.3)                     # kad rebate
    add(pop(1000), 25.55, 0.28)
    add(pop(1150), 26.15, 0.28)
    # --- CTA ---
    add(shimmer(1.6), 28.0, 0.12)
    add(pop(900, 0.2), 28.75, 0.3)                    # butang


{"villaem3": sfx_villaem3, "best3": sfx_best3}[AD]()
sfx_L, sfx_R = L, R

# ---------------- Campur ----------------
t = np.arange(N) / SR
fade = np.minimum(1, t / 0.3) * np.clip((DUR - t) / (DUR - END_FADE), 0, 1)
mL = (music_L + sfx_L) * fade
mR = (music_R + sfx_R) * fade
peak = max(np.abs(mL).max(), np.abs(mR).max())
mL, mR = mL / peak * 0.89, mR / peak * 0.89          # ~ -1 dBFS

out = ROOT / "out"
out.mkdir(exist_ok=True)
data = (np.stack([mL, mR], 1) * 32767).astype("<i2")
with wave.open(str(out / OUTFILE), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / OUTFILE)
