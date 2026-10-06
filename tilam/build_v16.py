"""Video 16 — Bedah tilam Coway Prime II -> out/tilam/v16_prime2_final.mp4

    python tilam/vo/gemini_tts.py ...   # (sekali) VO penuh -> tilam/vo/v16_full.wav, lihat README tilam
    python tilam/vo/split.py v16        # potong VO -> tilam/vo/v16_vo.wav + v16_timing.json
    python tilam/build_v16.py           # timing.js + render animasi + muzik/SFX + gabung
    python tilam/build_v16.py --stills 1,6,20   # pratonton PNG -> out/stills/
"""
import argparse, json, pathlib, subprocess, sys, wave
import imageio_ffmpeg, numpy as np

R = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R))
import render  # noqa: E402

FF, SR = imageio_ffmpeg.get_ffmpeg_exe(), 44100
SRC, OUT = "tilam/v16_prime2.html", R / "out" / "tilam"
HOLD = 2.6


def timing():
    tm = json.loads((R / "tilam/vo/v16_timing.json").read_text())
    (R / "src/tilam/v16_timing.js").write_text("window.TIMING = " + json.dumps(tm, ensure_ascii=False) + ";\n")
    return {x["scene"]: x for x in tm}


def audio(T, path):
    D = T["cta"]["end"] + HOLD; N = int(D * SR); rng = np.random.default_rng(16)
    t = lambda d: np.arange(int(d * SR)) / SR
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    env = lambda d, a, rel: np.minimum(1, t(d) / a) * np.exp(-t(d) / rel)
    mus, sfx = np.zeros(N), np.zeros(N)

    def add(b, s, at, g):
        i = int(at * SR)
        if 0 <= i < N: s = s[:N - i] * g; b[i:i + len(s)] += s

    def smooth(x, n): return np.convolve(x, np.ones(n) / n, "same")
    whoosh = lambda d=.7: smooth(rng.standard_normal(int(d * SR)), 14) * np.sin(np.pi * t(d) / d) ** 2
    pop = lambda f=900: np.sin(2 * np.pi * np.cumsum(f * (1 + 1.1 * np.exp(-t(.12) * 55))) / SR) * env(.12, .002, .03)
    thud = lambda: np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t(.6) * 18)) / SR) * env(.6, .003, .16)
    bell = lambda f, d=1.2: (np.sin(2 * np.pi * f * t(d)) + .4 * np.sin(2 * np.pi * f * 2.76 * t(d))) * env(d, .003, d / 4)

    # muzik: pad lembut + piano arpeggio (premium, tenang), kick perlahan selepas tilam terburai
    bpm = 88; beat = 60 / bpm
    prog = [[50, 57, 62, 66, 69], [47, 54, 59, 62, 66], [43, 50, 55, 59, 62], [45, 52, 57, 61, 64]]   # D Bm G A
    e1 = T["hook"]["start"] + (T["hook"]["end"] - T["hook"]["start"]) * .62
    bar = 0; t0 = 0.0
    while t0 < D:
        ch = prog[bar % 4]; d = 4 * beat + .6; tt = t(d)
        pad = sum(np.sin(2 * np.pi * hz(n) * tt + .25 * np.sin(2 * np.pi * .25 * tt)) for n in ch[1:])
        add(mus, pad * np.minimum(1, tt / .8) * np.minimum(1, (d - tt) / .6), t0, .026)
        add(mus, np.sin(2 * np.pi * hz(ch[0] - 12) * tt) * np.minimum(1, tt / .05) * np.exp(-tt / 2.2), t0, .14)
        for k in range(8):                                   # arpeggio
            n = ch[[1, 2, 3, 4, 3, 2, 3, 4][k]] + 12
            tone = (np.sin(2 * np.pi * hz(n) * t(1.2)) + .3 * np.sin(4 * np.pi * hz(n) * t(1.2))) * env(1.2, .004, .3)
            add(mus, tone, t0 + k * beat / 2, .045 if t0 + k * beat / 2 > e1 else .03)
        if t0 >= e1 - .1:
            for k in range(4):
                tb = t0 + k * beat
                add(mus, np.sin(2 * np.pi * np.cumsum(50 + 80 * np.exp(-t(.3) * 30)) / SR) * env(.3, .002, .09), tb, .22)
                if k % 2: add(mus, smooth(rng.standard_normal(int(.06 * SR)), 2) * env(.06, .001, .02), tb, .05)
        bar += 1; t0 += 4 * beat

    # SFX ikut animasi (src/tilam/v16_prime2.html)
    add(sfx, whoosh(1.1), e1 - .2, .32)
    for i in range(6): add(sfx, pop(700 + i * 90), e1 + .15 + (5 - i) * .06 + .5, .1)
    for k in ["fabric", "topper", "latex", "foam", "spring", "coconut", "assemble", "promo", "cta"]:
        add(sfx, whoosh(.55), T[k]["start"] - .45, .16)
    s = T["fabric"]["start"]
    for x in (1.2, 1.9): add(sfx, pop(1000), s + x, .18)
    for j in range(5): add(sfx, bell(1760 + j * 220, .5), s + .6 + j * .12, .025)
    s = T["topper"]["start"]; add(sfx, whoosh(.6), s + 1.3, .3); add(sfx, whoosh(.6), s + 2.0, .3); add(sfx, pop(800), s + 2.6, .2)
    add(sfx, pop(1000), s + 1.5, .18)
    for j in range(5): add(sfx, pop(800 + j * 70), T["latex"]["start"] + 1.0 + j * .32, .17)
    add(sfx, whoosh(1.6), T["foam"]["start"] + .3, .12); add(sfx, pop(1000), T["foam"]["start"] + 1.0, .18)
    for j in range(7): add(sfx, pop(760 + j * 60), T["spring"]["start"] + 1.0 + j * .3, .16)
    add(sfx, pop(1000), T["spring"]["start"] + 3.4, .18)
    for x in (1.2, 2.0): add(sfx, pop(1000), T["coconut"]["start"] + x, .18)
    add(sfx, thud(), T["assemble"]["start"] + .75, .5)
    for j, f in enumerate([1568, 2093, 2637]): add(sfx, bell(f), T["assemble"]["start"] + 1.0 + j * .1, .05)
    s = T["promo"]["start"]
    for x in (.05, .35, .75, 1.6): add(sfx, pop(900 + x * 200), s + x, .2)
    add(sfx, thud(), s + 3.2, .45)
    for j, f in enumerate([2637, 3136, 3951]): add(sfx, bell(f, .7), s + 3.3 + j * .07, .05)
    add(sfx, pop(950), T["cta"]["start"] + .5, .25)

    # VO + ducking
    raw = subprocess.run([FF, "-v", "error", "-i", str(R / "tilam/vo/v16_vo.wav"), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    vo = np.zeros(N); x = np.frombuffer(raw, "<i2").astype(float) / 32768; vo[:min(N, len(x))] = x[:N]
    act = np.clip(smooth((np.abs(vo) > .02).astype(float), SR // 3) * 3, 0, 1)
    fade = np.clip((D - t(D)[:N]) / 1.2, 0, 1) * np.clip(t(D)[:N] / .3, 0, 1)
    m = (mus * (1 - .5 * act) + sfx) * fade + vo * 1.0
    m /= max(1, np.abs(m).max() / .95)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype("<i2").tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--stills"); ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    T = timing()
    if a.stills:
        render.stills(SRC, [float(x) for x in a.stills.split(",")], prefix="v16_"); sys.exit()
    OUT.mkdir(parents=True, exist_ok=True)
    silent, wav, final = OUT / "_v16_noaudio.mp4", OUT / "_v16.wav", OUT / "v16_prime2_final.mp4"
    render.video(SRC, silent, a.jobs)
    audio(T, wav)
    subprocess.run([FF, "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    silent.unlink(); wav.unlink(); print("siap:", final)
