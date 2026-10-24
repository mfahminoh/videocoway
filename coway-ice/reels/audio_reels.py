"""Music bed + ice SFX for the 15s Reels (reels/reel1.html, reels/reel2.html).

    python reels/audio_reels.py reel1     -> out/reel1_music_sfx.wav

Timing is read from reels/<name>.timeline.js (same file the animation uses). Everything is generated with numpy,
so there are no licensing concerns for Meta Ads.
"""
import json
import pathlib
import re
import sys
import wave

import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
NAME = sys.argv[1] if len(sys.argv) > 1 else "reel1"
SR = 44100
# garis masa dikongsi dengan animasi (reels/<name>.timeline.js)
_tl = (ROOT / "reels" / f"{NAME}.timeline.js").read_text()
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


# ---------------- Muzik: 124 BPM, F - C - Dm - Bb (ceria) ----------------
BPM = 124
BEAT = 60 / BPM
BAR = 4 * BEAT
CHORDS = [[41, 53, 57, 60, 65], [36, 52, 55, 60, 64], [38, 50, 57, 62, 65], [34, 50, 53, 58, 62]]
ARP = [[77, 81, 84, 81], [76, 79, 84, 79], [74, 77, 81, 77], [74, 77, 82, 77]]

REVEAL = 1.35 if NAME == "reel1" else T["ready"]   # dram penuh masuk bila produk/penyelesaian muncul
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



def cta_sfx(e, btn, hand):
    add(whoosh(), e - .15, 0.22)
    add(shimmer(1.4), e + .15, 0.12)
    add(pop(1000), e + .25, 0.25)
    add(pop(900, 0.2), btn, 0.3)                     # butang WhatsApp
    tap = hand + (np.pi / 2) / 6                     # puncak "tekan" jari (ikut html)
    while tap < DUR - .1:
        add(pop(1500, 0.08), tap, 0.28)
        tap += 2 * np.pi / 6


def offer_sfx(o):
    add(whoosh(), o - .15, 0.22)
    add(pop(1300, 0.15), o + .1, 0.3)                # PROMOSI
    add(impact(0.9), o + .3, 0.45)                   # RM20
    for i, fq in enumerate([2637, 3136, 3951, 4699, 5274]):
        add(bell(fq, 0.7), o + .35 + i * 0.07, 0.07)
    add(pop(900), o + .55, 0.22)
    add(pop(1100), o + 1.35, 0.28)                   # SELAMA 7 BULAN


if NAME == "reel1":
    # hook: hujan kiub ais + produk hentak masuk
    for i in range(18):
        t0 = (np.sin(i * 127.1 + 311.7) * 43758.5453) % 1 * 1.6
        add(clack(d=0.07), t0 + .5, 0.12, pan=rng.uniform(-.6, .6))
    add(pop(1100), .1, 0.28)
    add(pop(1250), .4, 0.28)
    add(whoosh(0.35), 1.05, 0.2)
    add(impact(1.4), 1.4, 0.6)
    add(shimmer(1.2), 1.45, 0.14)
    add(pop(1200, 0.15), 1.6, 0.28)
    # ais baru 15 minit (footage + jam)
    f = T["fresh"]
    add(whoosh(), f - .15, 0.2)
    add(pop(1000), f + .3, 0.26)
    tk = f + .7
    while tk < f + 2.15:
        add(tick(), tk, 0.22)
        tk += max(0.05, 0.2 * (1 - (tk - f - .7) / 1.5) ** 1.3)
    for i, fq in enumerate([1568, 2093, 2637]):
        add(bell(fq, 0.8), f + 2.2 + i * 0.08, 0.1)
    for k in [.4, .8, 1.2, 1.6, 2.0, 2.4]:
        rattle(f + k, 2, .06, .26)
    # 700g
    c = T["cap"]
    add(whoosh(), c - .15, 0.2)
    add(impact(0.8), c + .15, 0.35)
    for i in range(48):
        add(clack(d=0.07), c + .3 + i * .036 + .18, 0.13, pan=rng.uniform(-.5, .5))
    add(shimmer(1.2), c + 2.2, 0.14)
    offer_sfx(T["offer"])
    cta_sfx(T["cta"], T["cta"] + 1.25, T["cta"] + 2.05)
else:
    # beg ais bungkus jatuh
    for i in range(5):
        add(clack(900 + 120 * i, 0.12), .3 + i * .16 + .3, 0.3)
        rattle(.3 + i * .16 + .3, 2, .05, .18)
    add(pop(1100), .25, 0.25)
    # bekas ais kosong + pangkah merah
    e0 = T["empty"]
    add(whoosh(0.3), e0 - .1, 0.18)
    add(pop(700, 0.2), e0 + .1, 0.25)
    add(impact(0.5), e0 + .6, 0.3)
    for i, fq in enumerate([392, 330]):              # "tet-tot" salah
        add(bell(fq, 0.35), e0 + .6 + i * .18, 0.12)
    # ais dah ready (footage)
    r = T["ready"]
    add(whoosh(), r - .15, 0.22)
    add(impact(1.2), r, 0.45)
    add(shimmer(1.2), r + .05, 0.12)
    slow = max(1, (T["stats"] - r) / (73 / 30))
    for k in [.35, .65, .95, 1.25, 1.55, 1.85, 2.15]:
        rattle(r + k * slow, 2, .06, .28)
    # statistik
    s = T["stats"]
    add(whoosh(), s - .15, 0.2)
    add(whoosh(0.3), s + .1, 0.15, pan=-.5)
    tk = s + .4
    while tk < s + 1.55:
        add(tick(), tk, 0.2)
        tk += max(0.05, 0.18 * (1 - (tk - s - .4) / 1.2) ** 1.3)
    add(bell(2093, 0.7), s + 1.6, 0.1)
    add(whoosh(0.3), s + .85, 0.15, pan=.5)
    for i in range(48):
        add(clack(d=0.06), s + 1.0 + i * .03 + .18, 0.1, pan=rng.uniform(-.5, .5))
    offer_sfx(T["offer"])
    cta_sfx(T["cta"], T["cta"] + .85, T["cta"] + 1.5)

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
with wave.open(str(out / f"{NAME}_music_sfx.wav"), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out / f"{NAME}_music_sfx.wav")

