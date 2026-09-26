"""Music bed + SFX for the long version (src/long.html, 112.5 s) -> out/music_sfx_long.wav

Story part is light, the problem scene (40–56 s) turns tense (minor, ticking clock),
then it lifts at the water-drop bridge and goes full beat from the product reveal.
"""
import json
import pathlib
import sys
import wave

import numpy as np

ROOT = pathlib.Path(__file__).parent
SR = 44100
ANIM_DUR = 112.5
# --warp out/warp_long.json : semua masa di bawah ditulis dalam masa animasi, dan dipetakan ke masa output
WARP = json.loads(pathlib.Path(sys.argv[sys.argv.index("--warp") + 1]).read_text()) if "--warp" in sys.argv else None
DUR = WARP["duration"] if WARP else ANIM_DUR


def W(t):       # masa animasi -> masa output
    return float(np.interp(t, WARP["anim"], WARP["out"])) if WARP else t


def Winv(t):    # masa output -> masa animasi
    return float(np.interp(t, WARP["out"], WARP["anim"])) if WARP else t


N = int(SR * DUR)
rng = np.random.default_rng(11)
L = np.zeros(N)
R = np.zeros(N)


SFX_MODE = False


def add(sig, t0, gain=1.0, pan=0.0):
    if SFX_MODE:
        t0 = W(t0)
    i = int(t0 * SR)
    if i >= N or i < 0:
        return
    sig = sig[: N - i] * gain
    L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(d, a=0.005, rel=None):
    t = tt(d)
    return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * np.asarray(cutoff, dtype=float) / SR) * np.ones_like(x)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------------- muzik ----------------
BPM = 108
BEAT = 60 / BPM
BAR = 4 * BEAT
MAJOR = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]
ARP_MAJ = [[72, 76, 79, 76], [71, 74, 79, 74], [72, 76, 81, 76], [69, 72, 77, 72]]
MINOR = [[45, 57, 60, 64], [41, 53, 57, 60], [38, 50, 53, 57], [40, 52, 56, 59]]   # Am F Dm E

PROB = (40.0, 56.0)
BRIDGE = (56.0, 63.35)
BEAT_ON = 63.35
FADE_START = DUR - 1.7


def section(t):
    if PROB[0] <= t < PROB[1]:
        return "prob"
    if BRIDGE[0] <= t < BRIDGE[1]:
        return "bridge"
    return "full" if t >= BEAT_ON else "story"


bar_i = 0
t0 = 0.0
while t0 < DUR:
    sec = section(Winv(t0) + 0.01)
    ch = (MINOR if sec == "prob" else MAJOR)[bar_i % 4]
    d = BAR + 0.4
    t = tt(d)
    pad = sum(np.sin(2 * np.pi * hz(m) * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) for m in ch[1:])
    pad += 0.5 * np.sin(2 * np.pi * hz(ch[0]) * t)
    add(pad * np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4), t0, 0.045 if sec in ("prob", "bridge") else 0.035)
    for b in range(4):
        tb = t0 + b * BEAT
        s = section(Winv(tb))
        bd = BEAT * 0.9
        if s != "bridge":
            add(np.sin(2 * np.pi * hz(ch[0] - 12) * tt(bd)) * env(bd, 0.01, bd * 1.6), tb,
                {"story": 0.08, "prob": 0.14, "full": 0.16}[s])
        if s == "full":
            kd = 0.35
            ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR
            add(np.sin(ph) * env(kd, 0.001, 0.3), tb, 0.45)
            add(rng.standard_normal(int(0.06 * SR)) * env(0.06, 0.001, 0.05), tb + BEAT / 2, 0.05, pan=0.2)
            if b in (1, 3):
                sd = 0.18
                sn = rng.standard_normal(int(sd * SR)) * env(sd, 0.001, 0.15)
                add(lowpass(sn, 5000) + 0.4 * np.sin(2 * np.pi * 190 * tt(sd)) * env(sd, 0.001, 0.08), tb, 0.12)
        elif s == "prob":
            # jam berdetik + denyut rendah
            add(lowpass(rng.standard_normal(int(0.03 * SR)), 6000) * env(0.03, 0.0005, 0.02), tb, 0.16, pan=-0.3)
            add(lowpass(rng.standard_normal(int(0.03 * SR)), 4000) * env(0.03, 0.0005, 0.02), tb + BEAT / 2, 0.10, pan=0.3)
            if b == 0:
                kd = 0.5
                add(np.sin(2 * np.pi * np.cumsum(45 + 40 * np.exp(-tt(kd) * 20)) / SR) * env(kd, 0.002, 0.45), tb, 0.35)
        elif s == "story" and b in (1, 3):
            add(lowpass(rng.standard_normal(int(0.05 * SR)), 3500) * env(0.05, 0.001, 0.03), tb, 0.12)
    if section(Winv(t0) + 0.01) in ("story", "full"):
        for k in range(8):
            tn = t0 + k * BEAT / 2
            if section(Winv(tn)) not in ("story", "full"):
                continue
            m = ARP_MAJ[bar_i % 4][k % 4] + (12 if k >= 4 and Winv(tn) >= BEAT_ON else 0)
            x = np.sin(2 * np.pi * hz(m) * tt(0.45)) + 0.3 * np.sin(2 * np.pi * 2 * hz(m) * tt(0.45))
            add(x * env(0.45, 0.003, 0.35), tn, 0.06, pan=0.35 if k % 2 else -0.35)
    bar_i += 1
    t0 += BAR

music = (L.copy(), R.copy())
L[:] = 0
R[:] = 0
SFX_MODE = True


# ---------------- SFX ----------------
def whoosh(d=0.55, up=True):
    t = tt(d)
    f = (400 + 5000 * (t / d) ** 2) if up else (5500 - 5000 * (t / d) ** 0.5)
    return lowpass(rng.standard_normal(len(t)), f) * np.sin(np.pi * t / d) ** 2


def pop(f=900, d=0.12):
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(d, 0.001, 0.1)


def impact(d=1.2):
    t = tt(d)
    boom = np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR) * env(d, 0.002, 1.0)
    return boom + 0.3 * lowpass(rng.standard_normal(len(t)), 1500) * env(d, 0.001, 0.3)


def bell(f, d=0.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, 0.002, 0.5)


def click(c=6000):
    return lowpass(rng.standard_normal(int(0.02 * SR)), c) * env(0.02, 0.0005, 0.015)


def shimmer(d=1.2):
    t = tt(d)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([2093, 2637, 3136, 4186])) * np.minimum(1, t / 0.02)


def buzz(d=0.28):          # bunyi "salah"
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * 110 * t)) * 0.6 + np.sin(2 * np.pi * 116 * t)
    return lowpass(x, 1800) * env(d, 0.005, 0.35)


def glass(d=0.9):
    t = tt(d)
    x = rng.standard_normal(len(t)) * np.exp(-t * 7)
    hi = x - lowpass(x, 2500)
    tinks = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 9) for f in [3200, 4100, 5300, 6100])
    return hi * 0.9 + 0.15 * tinks


def riser(d):
    t = tt(d)
    x = lowpass(rng.standard_normal(len(t)), 300 + 7000 * (t / d) ** 2)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 600 * (t / d) ** 2) / SR) * 0.3
    return (x + tone) * (t / d) ** 2


def bloop():
    d = 0.35
    t = tt(d)
    return np.sin(2 * np.pi * np.cumsum(300 + 900 * (t / d)) / SR) * env(d, 0.003, 0.3)


def engine(d=1.4):
    t = tt(d)
    f = 45 + 60 * np.minimum(1, t / 0.9)
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return lowpass(saw, 900) * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.4)


def swell(d):
    t = tt(d)
    return lowpass(rng.standard_normal(len(t)), 900 + 1500 * (t / d)) * np.sin(np.pi * t / d)


for w in [6.05, 19.85, 30.85, 39.85, 55.9, 61.85, 67.85, 72.85, 77.85, 84.85, 89.6, 104.35]:
    add(whoosh(), w, 0.22)
# hook
add(impact(), 0.3, 0.55)
for i, x in enumerate([1.25, 1.47, 1.69]):
    add(pop(500 + 120 * i), x, 0.35, pan=-0.4 + 0.4 * i)
add(pop(1300, 0.15), 4.4, 0.25)
for a, b in [(2.0, 3.3), (4.5, 5.6)]:
    for i in range(int((b - a) * 18)):
        add(click(), a + i / 18 + rng.uniform(0, .02), 0.16)
# telefon
add(pop(1100), 6.3, 0.28)
add(pop(700, 0.2), 6.7, 0.3)
add(whoosh(0.35, up=False), 8.8, 0.18)
add(pop(1300), 10.8, 0.3)
for i in range(8):
    add(bell(1400 + i * 90, 0.25), 13.8 + i * 4.6 / 7, 0.06)
add(pop(900, 0.18), 18.6, 0.28)
# kereta
add(pop(1100), 20.1, 0.28)
add(engine(), 20.4, 0.35)
add(whoosh(0.35, up=False), 22.9, 0.18)
add(pop(1300), 24.6, 0.3)
for i in range(60):
    add(click(4000), 26.4 + i * 4.0 / 60, 0.10)
# mindset
add(pop(1000), 31.1, 0.28)
add(impact(0.6), 32.4, 0.35)
add(impact(0.6), 33.3, 0.35)
add(pop(1200), 36.6, 0.28)
# masalah
add(impact(1.5), 40.2, 0.5)
for x in [43.8, 45.0, 46.4, 47.6]:
    add(buzz(), x, 0.22)
for i, x in enumerate([51.0, 51.8, 52.6]):
    add(riser(0.7), x, 0.12)
add(glass(), 54.1, 0.5)
add(impact(1.4), 54.12, 0.6)
# jambatan
add(bloop(), 57.0, 0.35)
add(pop(900), 57.8, 0.25)
add(riser(5.0), 58.35, 0.18)
# pendedahan
add(impact(1.6), 63.35, 0.65)
add(shimmer(1.4), 63.4, 0.12)
# ciri
add(pop(1100), 68.1, 0.25)
add(impact(0.6), 69.5, 0.3)
add(pop(1000), 73.3, 0.25)
add(swell(1.6), 73.6, 0.22)
add(impact(0.6), 78.05, 0.3)
for i, x in enumerate([79.9, 81.4, 82.1, 82.8]):
    add(pop(800 + 150 * i), x, 0.3, pan=-0.3 if i % 2 == 0 else 0.3)
add(pop(600, 0.2), 85.05, 0.3)
add(bell(1568, 0.5), 85.6, 0.12)
# promo
add(pop(1200), 90.1, 0.3)
add(whoosh(0.35, up=False), 92.4, 0.2)
for i in range(14):
    add(click(5000), 93.3 + i * 2.0 / 14, 0.12)
for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
    add(bell(f, 0.7), 95.3 + i * 0.07, 0.07)
add(impact(0.8), 95.35, 0.3)
add(impact(0.9), 96.4, 0.4)
add(pop(1100), 97.0, 0.3)
add(pop(1000), 100.3, 0.28)
add(pop(1150), 101.1, 0.28)
for x in [102.2, 102.45]:
    add(bell(1760, 0.2), x, 0.12)
# CTA
add(shimmer(1.6), 104.7, 0.12)
add(impact(0.6), 105.1, 0.3)
add(impact(0.6), 105.6, 0.3)
add(pop(900, 0.2), 106.7, 0.3)

t = np.arange(N) / SR
fade = np.minimum(1, t / 0.3) * np.clip((DUR - t) / (DUR - FADE_START), 0, 1)
mL = (music[0] + L) * fade
mR = (music[1] + R) * fade
pk = max(np.abs(mL).max(), np.abs(mR).max())
data = (np.stack([mL, mR], 1) / pk * 0.89 * 32767).astype("<i2")
out = ROOT / "out" / "music_sfx_long.wav"
out.parent.mkdir(exist_ok=True)
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("wrote", out)
