"""Synthesize a royalty-free music bed + ice sound effects matched to the Coway Ice timeline.

Output: out/music_sfx.wav (44.1 kHz stereo, panjang ikut src/timeline.js). Everything is generated with numpy,
so there are no licensing concerns for Meta Ads.
"""
import json
import pathlib
import re
import wave

import numpy as np

ROOT = pathlib.Path(__file__).parent
SR = 44100
# garis masa dikongsi dengan animasi (src/timeline.js)
_tl = (ROOT / "src" / "timeline.js").read_text()
_tl = re.sub(r"/\*.*?\*/", "", _tl, flags=re.S).split("=", 1)[1].rsplit(";", 1)[0]
T = json.loads(re.sub(r"(\w+):", r'"\1":', _tl))
DUR = T["end"]
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


# ---------------- Muzik: 116 BPM, F - C - Dm - Bb (ceria) ----------------
BPM = 116
BEAT = 60 / BPM
BAR = 4 * BEAT
CHORDS = [[41, 53, 57, 60, 65], [36, 52, 55, 60, 64], [38, 50, 57, 62, 65], [34, 50, 53, 58, 62]]
ARP = [[77, 81, 84, 81], [76, 79, 84, 79], [74, 77, 81, 77], [74, 77, 82, 77]]

REVEAL = T["s3"] + .45        # dram penuh masuk bila Coway Ice muncul
END_FADE = DUR - 0.8

bar_idx = 0
t0 = 0.0
while t0 < DUR:
    ch = CHORDS[bar_idx % 4]
    d = BAR + 0.4
    t = tt(d)
    pad = sum(np.sin(2 * np.pi * hz(m) * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) for m in ch[1:])
    pad += 0.5 * np.sin(2 * np.pi * hz(ch[0]) * t)
    penv = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    add(pad * penv, t0, 0.03)
    for b in range(4):
        tb = t0 + b * BEAT
        bd = BEAT * 0.9
        x = np.sin(2 * np.pi * hz(ch[0] - 12) * tt(bd))
        add(x * env(bd, 0.01, bd * 1.6), tb, 0.16 if tb >= REVEAL else 0.10)
    # pluck "kristal" (1/8 nota) — bunyi sejuk
    for k in range(8):
        tn = t0 + k * BEAT / 2
        m = ARP[bar_idx % 4][k % 4] + (12 if k >= 4 and tn >= REVEAL else 0)
        dd = 0.45
        x = np.sin(2 * np.pi * hz(m) * tt(dd)) + 0.25 * np.sin(2 * np.pi * 3 * hz(m) * tt(dd))
        add(x * env(dd, 0.002, 0.3), tn, 0.055, pan=0.35 if k % 2 else -0.35)
    for b in range(4):
        tb = t0 + b * BEAT
        full = tb >= REVEAL
        kd = 0.35
        ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR
        if full or b in (0, 2):
            add(np.sin(ph) * env(kd, 0.001, 0.3), tb, 0.45 if full else 0.3)
        hd = 0.06
        add(rng.standard_normal(int(hd * SR)) * env(hd, 0.001, 0.05), tb + BEAT / 2, 0.05 if full else 0.03, pan=0.2)
        if b in (1, 3):
            if full:
                sd = 0.18
                sn = rng.standard_normal(int(sd * SR)) * env(sd, 0.001, 0.15)
                add(lowpass(sn, 5000) + 0.4 * np.sin(2 * np.pi * 190 * tt(sd)) * env(sd, 0.001, 0.08), tb, 0.12)
            else:
                cd = 0.05
                add(lowpass(rng.standard_normal(int(cd * SR)), 3500) * env(cd, 0.001, 0.03), tb, 0.14)
    bar_idx += 1
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


def clink(f=2200, d=0.9):
    """gelas berlaga — separa harmonik tak selaras, pudar cepat"""
    t = tt(d)
    y = sum(a * np.sin(2 * np.pi * f * m * t) * np.exp(-t * dcy) for m, a, dcy in
            [(1, 1, 5), (1.52, .6, 7), (2.34, .45, 9), (3.1, .3, 12), (4.2, .2, 16)])
    return y * np.minimum(1, t / 0.001)


def clack(f=None, d=0.09):
    """kiub ais kena gelas/ais — ketuk pendek + nada kaca"""
    f = f or rng.uniform(2600, 4200)
    t = tt(d)
    n = lowpass(rng.standard_normal(len(t)), 7000) * np.exp(-t * 90)
    return n + 0.35 * np.sin(2 * np.pi * f * t) * np.exp(-t * 45)


def tick():
    d = 0.03
    return lowpass(rng.standard_normal(int(d * SR)), 8000) * env(d, 0.0005, 0.012) + 0.4 * pop(2400, 0.03)


def shimmer(d=1.0):
    t = tt(d)
    y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([2093, 2637, 3136, 4186]))
    return y * np.minimum(1, t / 0.02)


def rattle(t0, n=4, spread=.18, gain=.25):
    for _ in range(n):
        add(clack(), t0 + rng.uniform(0, spread), gain * rng.uniform(.6, 1), pan=rng.uniform(-.4, .4))


# S1 hook — keluarga, gelas berlaga
add(whoosh(0.4), 0.0, 0.12)
for i, tg in enumerate([.45, .6, .75]):             # gelas mendarat atas meja
    add(clack(1800 + 300 * i, 0.12), tg, 0.3)
add(clink(2200), 1.08, 0.3, pan=-.2)
rattle(1.08, 3)
add(clink(2500), 2.48, 0.3, pan=.2)
rattle(2.48, 3)
add(pop(1100), 1.55, 0.3)                           # MESTI ADA AIS!
# S2 montaj
for k, tc in enumerate(T["cards"]):
    add(whoosh(0.3), tc - .15, 0.2)
    rattle(tc + .15, 3, gain=.22)
    add(pop(900 + 120 * k), tc + .15, 0.2)
# S3 gelas masuk -> COWAY ICE
s3 = T["s3"]
for i in range(4):
    add(whoosh(0.35), s3 - .05 + i * .06, 0.12, pan=[-.6, .6, -.4, .4][i])
add(impact(1.6), s3 + .45, 0.6)
add(shimmer(1.4), s3 + .5, 0.14)
add(pop(1200, 0.15), s3 + .95, 0.3)
# S4a footage ais jatuh (slow-mo ikut panjang babak)
r = T["rdy"]
add(whoosh(), r - .15, 0.2)
slow = max(1, (T["cap"] - r - .1) / (73 / 30))
for k in [.35, .65, .95, 1.25, 1.55, 1.85, 2.15]:
    rattle(r + k * slow, 2, .06, .3)
# S4b bekas 700g
c = T["cap"]
add(whoosh(), c - .15, 0.2)
add(impact(0.8), c + .2, 0.35)                      # 700g
for i in range(48):
    add(clack(d=0.07), c + .45 + i * .055 + .18, 0.14, pan=rng.uniform(-.5, .5))
add(bell(1568, 0.6), c + 3.0, 0.12)
add(shimmer(1.4), c + 3.15, 0.14)
# S5a pemasa 15 minit
m = T["tmr"]
add(whoosh(), m - .15, 0.2)
add(pop(1000), m + .3, 0.28)
for tk in [m + .05, m + .6, m + 1.0]:
    add(tick(), tk, 0.35)
tk = m + 1.0
while tk < m + 2.15:                                # tik semakin laju
    add(tick(), tk, 0.25)
    tk += max(0.035, 0.22 * (1 - (tk - m - 1.0) / 1.15) ** 1.5)
for i, f in enumerate([1568, 2093, 2637]):          # ding 00:00
    add(bell(f, 0.9), m + 2.2 + i * 0.08, 0.1)
for i in range(8):
    add(clack(d=0.08), m + 2.3 + i * .09 + .2, 0.22, pan=rng.uniform(-.4, .4))
# S5b footage fresh ice
f0 = T["fresh"]
add(whoosh(), f0 - .15, 0.2)
for k in [.15, .55, .95, 1.3, 1.65, 2.0, 2.3]:
    rattle(f0 + k, 2, .06, .28)
# S6a tawaran
o = T["offer"]
add(whoosh(), o - .15, 0.22)
add(pop(1300, 0.15), o + .15, 0.3)                  # LAST CALL
add(impact(0.9), o + .4, 0.45)                      # RM20
for i, fq in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(fq, 0.7), o + .45 + i * 0.07, 0.07)
add(pop(900), o + .75, 0.22)
add(pop(1100), o + 1.35, 0.28)                      # SELAMA 7 BULAN
h = T["hantar"]
add(pop(1250), h + .05, 0.28)                       # HANTAR & PASANG
for i in range(int((T["cta"] - .2 - (h + .4)) / 0.25)):   # jam berdetik (urgent)
    add(tick(), h + .4 + i * 0.25, 0.16)
# S6b CTA
e = T["cta"]
add(whoosh(), e - .15, 0.22)
add(shimmer(1.6), e + .2, 0.12)
add(pop(1000), e + .2, 0.25)
add(pop(900, 0.2), e + 1.05, 0.3)                   # butang WhatsApp
tap = e + 2.0 + (np.pi / 2) / 6                     # puncak "tekan" jari (ikut index.html)
while tap < DUR - .1:
    add(pop(1500, 0.08), tap, 0.28)
    tap += 2 * np.pi / 6

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
with wave.open(str(out / "music_sfx.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / "music_sfx.wav")
