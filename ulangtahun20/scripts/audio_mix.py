"""Audio akhir 20s: muzik latar (disintesis, tiada lesen pihak ketiga) + SFX ikut babak/shot + voiceover (audio/V01.wav).
Muzik direndahkan automatik ketika VO bercakap."""
import wave

import numpy as np

from common import AUDIO, DUR

SR = 44100
N = int(DUR * SR)


def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=.005, rel=None): t = tt(d); return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))
def hz(m): return 440 * 2 ** ((m - 69) / 12)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


def lowpass(x, cut):
    """Penapis satu-kutub (vektor kecil sahaja: SFX pendek)."""
    a = np.exp(-2 * np.pi * np.asarray(cut, float) / SR) * np.ones_like(x)
    y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y


def add(buf, sig, t0, g):
    i = int(t0 * SR)
    if 0 <= i < len(buf):
        s = sig[: len(buf) - i] * g; buf[i:i + len(s)] += s


def music(style, rng):
    bpm = {"S7": 92, "S8": 124}.get(style, 116)
    beat = 60 / bpm
    out = np.zeros(N)
    chords = [[45, 57, 60, 64, 69], [41, 53, 57, 60, 65], [48, 55, 60, 64, 67], [43, 55, 59, 62, 67]]   # Am F C G
    arp = [[76, 81, 84, 81], [77, 81, 84, 81], [76, 79, 84, 79], [74, 79, 83, 79]]
    t0, bi = 0.0, 0
    while t0 < DUR:
        ch = chords[bi % 4]; d = 4 * beat + .3; t = tt(d)
        pad = sum(np.sin(2 * np.pi * hz(m) * t) + .3 * np.sin(4 * np.pi * hz(m) * t) for m in ch[1:])
        add(out, pad * np.minimum(1, t / .3) * np.minimum(1, (d - t) / .3), t0, .022)
        for b in range(4):
            tb = t0 + b * beat
            add(out, np.sin(2 * np.pi * hz(ch[0] - 12) * tt(beat * .9)) * env(beat * .9, .01, beat * 1.2), tb, .16)
            if style != "S7":
                ph = 2 * np.pi * np.cumsum(48 + 120 * np.exp(-tt(.3) * 32)) / SR
                add(out, np.sin(ph) * env(.3, .001, .25), tb, .42)                         # kick
                add(out, rng.standard_normal(int(.05 * SR)) * env(.05, .001, .04), tb + beat / 2, .045)   # hi-hat
            if b in (1, 3) and style != "S7":
                add(out, rng.standard_normal(int(.18 * SR)) * env(.18, .002, .12), tb, .09)  # clap
        for k in range(8):
            m = arp[bi % 4][k % 4]
            add(out, np.sin(2 * np.pi * hz(m) * tt(.35)) * env(.35, .003, .28), t0 + k * beat / 2, .045 if style != "S7" else .03)
        bi += 1; t0 += 4 * beat
    return out


def sfx(plan, rng):
    out = np.zeros(N)

    def pop(f=900, d=.12): t = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(d, .001, .1)
    def whoosh(d=.45): t = tt(d); return lowpass(rng.standard_normal(len(t)), 300 + 5200 * (t / d) ** 2) * np.sin(np.pi * t / d) ** 2
    def impact(d=.8): t = tt(d); return np.sin(2 * np.pi * np.cumsum(38 + 100 * np.exp(-t * 12)) / SR) * env(d, .002, .7) + .25 * rng.standard_normal(len(t)) * env(d, .001, .08)
    def bell(f, d=.6): t = tt(d); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, .002, .5)
    def tick(): return pop(2400, .03)
    def beep(f): t = tt(.08); return np.sin(2 * np.pi * f * t) * env(.08, .002, .07)

    st = plan["style"]
    wh = whoosh()
    for s in plan["shots"][1:]:
        add(out, wh, s["t0"] - .2, .10 if st != "S7" else .05)
    for sc in plan["scenes"]:
        if sc["key"] == "cta":
            continue
        if st in ("S1", "S6") and sc["key"] in ("hook", "offer"):
            add(out, impact(), sc["t0"] + .12, .55)
        else:
            add(out, pop(900 + 120 * len(sc["key"])), sc["t0"] + .1, .25)
    if st == "S2":
        for k in range(int(plan["end_card"])):
            add(out, tick(), k + .02, .12)
    if st == "S3":
        for i, f in enumerate([1320, 1480, 1175, 1568]):
            add(out, beep(f), 3.25 + i * .16, .18)
        add(out, bell(1760, .4), 3.95, .2)
    if st == "S4":
        for t0 in (3.0, 7.0, 12.0):
            add(out, impact(.5), t0 + .2, .3)
    for i, f in enumerate([1568, 1976, 2349, 3136]):                                  # kad akhir
        add(out, bell(f, .8), plan["end_card"] + .45 + i * .06, .08)
    return out


def build(plan, path):
    rng = np.random.default_rng(int(plan["id"][1:]))
    with wave.open(str(AUDIO / f"{plan['id']}.wav")) as w:
        vo = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
    vo = np.pad(vo, (0, max(0, N - len(vo))))[:N]
    mus = music(plan["style"], rng)
    t = np.arange(N) / SR
    speech = movavg((np.abs(vo) > .02).astype(float), int(.3 * SR))
    mus *= (1 - .55 * np.clip(speech * 3, 0, 1)) * np.clip((DUR - t) / 1.2, 0, 1) * np.clip(t / .15, 0, 1)
    mix = .9 * vo + mus + .7 * sfx(plan, rng)
    mix /= max(1.0, np.abs(mix).max() / .95)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())
