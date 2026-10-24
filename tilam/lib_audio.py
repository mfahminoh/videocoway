"""Muzik latar + SFX (dari senarai acara animasi) + VO dengan ducking -> WAV mono 44.1k."""
import subprocess, wave
import imageio_ffmpeg, numpy as np

FF, SR = imageio_ffmpeg.get_ffmpeg_exe(), 44100
MOODS = {   # bpm, progression (MIDI), pad gain, arpeggio gain, kick
    "calm":  (88, [[50, 57, 62, 66, 69], [47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [45, 52, 57, 61, 64]], .026, .04, True),
    "warm":  (72, [[48, 55, 60, 64, 67], [45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [43, 50, 55, 59, 62]], .03, .05, False),
    "drive": (110, [[45, 52, 57, 60, 64], [41, 48, 53, 57, 60], [48, 55, 60, 64, 67], [43, 50, 55, 59, 62]], .022, .035, True),
}


def build(duration, events, vo_path, out_path, mood="calm", seed=7):
    D = duration; N = int(D * SR); rng = np.random.default_rng(seed)
    t = lambda d: np.arange(int(d * SR)) / SR
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    env = lambda d, a, rel: np.minimum(1, t(d) / a) * np.exp(-t(d) / rel)
    smooth = lambda x, n: np.convolve(x, np.ones(n) / n, "same")
    mus, sfx = np.zeros(N), np.zeros(N)

    def add(b, s, at, g):
        i = int(at * SR)
        if 0 <= i < N: s = s[:N - i] * g; b[i:i + len(s)] += s

    whoosh = lambda d=.6: smooth(rng.standard_normal(int(d * SR)), 14) * np.sin(np.pi * t(d) / d) ** 2
    pop = lambda f=900: np.sin(2 * np.pi * np.cumsum(f * (1 + 1.1 * np.exp(-t(.12) * 55))) / SR) * env(.12, .002, .03)
    thud = lambda: np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t(.6) * 18)) / SR) * env(.6, .003, .16)
    bell = lambda f, d=1.0: (np.sin(2 * np.pi * f * t(d)) + .4 * np.sin(2 * np.pi * f * 2.76 * t(d))) * env(d, .003, d / 4)

    bpm, prog, gp, ga, kick = MOODS[mood]; beat = 60 / bpm
    bar, t0 = 0, 0.0
    while t0 < D:
        ch = prog[bar % 4]; d = 4 * beat + .6; tt = t(d)
        pad = sum(np.sin(2 * np.pi * hz(n) * tt + .25 * np.sin(2 * np.pi * .25 * tt)) for n in ch[1:])
        add(mus, pad * np.minimum(1, tt / .8) * np.minimum(1, (d - tt) / .6), t0, gp)
        add(mus, np.sin(2 * np.pi * hz(ch[0] - 12) * tt) * np.minimum(1, tt / .05) * np.exp(-tt / 2.2), t0, .14)
        for k in range(8):
            n = ch[[1, 2, 3, 4, 3, 2, 3, 4][k]] + 12
            add(mus, (np.sin(2 * np.pi * hz(n) * t(1.2)) + .3 * np.sin(4 * np.pi * hz(n) * t(1.2))) * env(1.2, .004, .3), t0 + k * beat / 2, ga)
        if kick and t0 > 1.5:
            for k in range(4):
                tb = t0 + k * beat
                add(mus, np.sin(2 * np.pi * np.cumsum(50 + 80 * np.exp(-t(.3) * 30)) / SR) * env(.3, .002, .09), tb, .2)
                if k % 2: add(mus, smooth(rng.standard_normal(int(.06 * SR)), 2) * env(.06, .001, .02), tb, .05)
        bar += 1; t0 += 4 * beat

    last = {}
    for e in sorted(events, key=lambda e: e["t"]):
        k, at = e["k"], e["t"]
        if at - last.get(k, -9) < .12: continue        # elak bertindih
        last[k] = at
        if k == "whoosh": add(sfx, whoosh(.55), at - .35, .16)
        elif k == "pop": add(sfx, pop(850 + rng.integers(0, 300)), at, .16)
        elif k == "slam": add(sfx, thud(), at, .32); add(sfx, pop(700), at, .1)
        elif k == "swipe": add(sfx, whoosh(.3), at - .05, .22)
        elif k == "ding":
            for j, f in enumerate([1568, 2093, 2637]): add(sfx, bell(f), at + j * .08, .05)

    raw = subprocess.run([FF, "-v", "error", "-i", str(vo_path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    vo = np.zeros(N); x = np.frombuffer(raw, "<i2").astype(float) / 32768; vo[:min(N, len(x))] = x[:N]
    act = np.clip(smooth((np.abs(vo) > .02).astype(float), SR // 3) * 3, 0, 1)
    tt = t(D)[:N]; fade = np.clip((D - tt) / 1.2, 0, 1) * np.clip(tt / .3, 0, 1)
    m = (mus * (1 - .5 * act) + sfx) * fade + vo
    m /= max(1, np.abs(m).max() / .95)
    with wave.open(str(out_path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype("<i2").tobytes())
