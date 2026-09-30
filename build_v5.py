"""Build the 5 style videos (src/v5/*.html) -> out/v5/<name>.mp4

    python build_v5.py                      # all
    python build_v5.py --only v3_family     # one
    python build_v5.py --stills             # preview contact sheets -> out/stills/v5/

v1/v2 are overlays on an edit of the presenter clips (EDL below); v3–v5 are fully animated.
All share the promo/CTA end card (engine.js) voiced with Gemini VO excerpts.
"""
import argparse
import io
import multiprocessing as mp
import pathlib
import subprocess
import wave

import imageio_ffmpeg
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H, SR = 30, 1080, 1920, 44100
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)
OUT = ROOT / "out" / "v5"
ENDLEN = 17.8

# Petikan VO Gemini (saat dalam voiceover/source/gemini_tts_long.wav) -> masa relatif kad promo
ENDCARD_VO = [
    (73.25, 77.61, 0.30),    # "Tapi sekarang ada promosi diskaun, serendah tujuh puluh empat ringgit je sebulan."
    (78.15, 83.24, 5.00),    # "Dan ganda lagi dengan rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan!"
    (87.25, 88.83, 10.20),   # "Ni last call untuk promo ni."
    (89.10, 94.39, 11.95),   # "Kalau anda tengah cari penapis air high spec, ... WhatsApp saya sekarang."
]

V = {
    "v1_premium": dict(S=20.5, zoom=True,
        edl=[(4, 6.0, 3.0), (5, 6.0, 2.5), (2, 0.0, 2.5), (2, 3.6, 2.5), (3, 0.0, 2.5), (5, 0.2, 2.5), (3, 3.0, 2.5), (4, 0.5, 2.5)],
        presenter=[(3, 3.0, 2.5, 15.5), (4, 0.5, 2.5, 18.0)],
        music=dict(bpm=84, mood="lush", drums_from=0.0),
        cuts=[3.0, 5.5, 8.0, 10.5, 13.0, 15.5, 18.0], pops=[0.3, 5.6], impacts=[5.6]),
    "v2_upgrade": dict(S=19.0, zoom=False,
        edl=[(1, 7.05, 2.95), (4, 0.0, 3.0), (2, 6.0, 2.5), (2, 0.0, 2.5), (5, 0.3, 2.5), (4, 6.0, 2.5), (3, 3.0, 3.0)],
        presenter=[], music=dict(bpm=112, mood="bright", drums_from=0.0),
        cuts=[3.0, 6.0, 8.5, 11.0, 13.5, 16.0], pops=[0.1, 0.35, 3.05, 4.0, 6.05, 8.55, 9.1, 11.05, 13.55, 16.05, 16.6], impacts=[]),
    "v3_family": dict(S=17.0, edl=None, presenter=[], music=dict(bpm=96, mood="warm", drums_from=6.5),
        cuts=[3.5, 6.5, 9.5, 12.0, 14.5], pops=[0.1, 0.4, 1.4, 3.6, 3.9, 6.9, 9.8, 12.3, 14.8], impacts=[]),
    "v4_kinetic": dict(S=16.4, edl=None, presenter=[], music=dict(bpm=128, mood="hard", drums_from=0.0),
        cuts=[], pops=[11.1, 11.8, 12.5, 13.2],
        impacts=[0.0, 0.6, 1.2, 1.55, 2.5, 2.9, 3.9, 5.0, 5.7, 6.4, 7.2, 7.75, 8.4, 8.85, 9.8, 10.2, 14.6, 14.95]),
    "v5_compare": dict(S=22.0, edl=None, presenter=[], music=dict(bpm=104, mood="tension_then_lift", drums_from=2.8, lift=17.0),
        cuts=[2.8, 17.0], pops=[0.2, 0.4, 3.4, 5.9, 8.4, 10.9, 13.4, 17.6], impacts=[1.6, 19.0]),
}


def open_page(p, name):
    b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto((ROOT / "src" / "v5" / f"{name}.html").as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
    return b, page


def decode(path, start=None, dur=None):
    cmd = [FF, "-v", "error"] + (["-ss", str(start)] if start is not None else []) + ["-i", str(path)]
    cmd += (["-t", str(dur)] if dur else []) + ["-vn", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, "<i2").astype(float) / 32768


# ---------------- audio ----------------
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=.005, rel=None): t = tt(d); return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))
def hz(m): return 440 * 2 ** ((m - 69) / 12)


def lowpass(x, c):
    a = np.exp(-2 * np.pi * np.asarray(c, float) / SR) * np.ones_like(x); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y


MAJOR = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]
MINOR = [[45, 57, 60, 64], [41, 53, 57, 60], [48, 55, 60, 64], [43, 55, 59, 62]]


def build_audio(name, cfg, dur, path):
    rng = np.random.default_rng(abs(hash(name)) % 2 ** 32)
    N = int(dur * SR); S = cfg["S"]; m = cfg["music"]
    mus = np.zeros(N); sfx = np.zeros(N)

    def add(buf, sig, t0, g):
        i = int(t0 * SR)
        if 0 <= i < N:
            s = sig[: N - i] * g; buf[i:i + len(s)] += s

    beat = 60 / m["bpm"]; t0 = 0.0; bi = 0
    while t0 < dur:
        minor = m["mood"] == "lush" or (m["mood"] == "tension_then_lift" and t0 < m.get("lift", 0) and t0 < S)
        ch = (MINOR if minor else MAJOR)[bi % 4]; d = 4 * beat + .4; t = tt(d)
        wave_ = (lambda f, t: 2 * np.abs(2 * ((f * t) % 1) - 1) - 1) if m["mood"] == "warm" else (lambda f, t: np.sin(2 * np.pi * f * t))
        pad = sum(np.sin(2 * np.pi * hz(n) * t + .3 * np.sin(2 * np.pi * .3 * t)) for n in ch[1:]) + .5 * np.sin(2 * np.pi * hz(ch[0]) * t)
        add(mus, pad * np.minimum(1, t / .4) * np.minimum(1, (d - t) / .4), t0, .05 if m["mood"] == "lush" else .035)
        for b in range(4):
            tb = t0 + b * beat
            add(mus, np.sin(2 * np.pi * hz(ch[0] - 12) * tt(beat * .9)) * env(beat * .9, .01, beat * 1.4), tb, .15)
            if tb >= m["drums_from"]:
                kd = .35
                add(mus, np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR) * env(kd, .001, .3), tb,
                    {"hard": .6, "lush": .3}.get(m["mood"], .42))
                add(mus, rng.standard_normal(int(.06 * SR)) * env(.06, .001, .05), tb + beat / 2, .05)
                if b in (1, 3) and m["mood"] in ("bright", "hard", "tension_then_lift"):
                    sn = lowpass(rng.standard_normal(int(.18 * SR)), 5000) * env(.18, .001, .15)
                    add(mus, sn, tb, .14)
        for k in range(8 if m["mood"] != "lush" else 4):
            step = beat / 2 if m["mood"] != "lush" else beat
            n = ch[1 + k % (len(ch) - 1)] + 12 + (12 if k % 2 else 0)
            add(mus, wave_(hz(n), tt(.5)) * env(.5, .003, .4), t0 + k * step, .05)
        bi += 1; t0 += 4 * beat

    def pop(f=900, d=.12): t = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(d, .001, .1)
    def whoosh(d=.45): t = tt(d); return lowpass(rng.standard_normal(len(t)), 400 + 5000 * (t / d) ** 2) * np.sin(np.pi * t / d) ** 2
    def impact(d=.8): t = tt(d); return np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR) * env(d, .002, .7) + .25 * lowpass(rng.standard_normal(len(t)), 1500) * env(d, .001, .2)
    def bell(f, d=.6): t = tt(d); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, .002, .5)

    for c in cfg["cuts"]:
        add(sfx, whoosh(), c - .2, .22)
    for i, x in enumerate(cfg["pops"]):
        add(sfx, pop(850 + 60 * (i % 5)), x, .25)
    for x in cfg["impacts"]:
        add(sfx, impact(), x, .45 if m["mood"] == "hard" else .35)
    e = S  # kad promo
    add(sfx, whoosh(.6), e - .35, .3)
    add(sfx, pop(1200), e + .15, .3)
    add(sfx, lowpass(rng.standard_normal(int(.35 * SR)), 3000) * np.sin(np.pi * tt(.35) / .35), e + 1.1, .15)
    add(sfx, impact(), e + 2.3, .45)
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
        add(sfx, bell(f, .7), e + 3.9 + i * .07, .07)
    add(sfx, impact(), e + 5.0, .4); add(sfx, pop(1100), e + 5.6, .3)
    add(sfx, pop(1000), e + 8.9, .25); add(sfx, pop(1150), e + 9.4, .25)
    for x in (e + 10.1, e + 10.35):
        add(sfx, bell(1760, .2), x, .12)
    add(sfx, whoosh(), e + 11.0, .25)
    add(sfx, impact(.6), e + 11.7, .3); add(sfx, impact(.6), e + 12.2, .3); add(sfx, pop(900, .2), e + 13.2, .3)

    src = decode(ROOT / "voiceover" / "source" / "gemini_tts_long.wav")
    vo = np.zeros(N)
    for a, b, at in ENDCARD_VO:
        c = src[int((a - .04) * SR): int((b + .12) * SR)].copy()
        f = int(.01 * SR); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
        i = int((e + at - .04) * SR); c = c[: N - i]; vo[i:i + len(c)] += c
    vo *= .9 / (np.abs(vo).max() + 1e-9)
    pres = np.zeros(N)
    for clip, a, d, at in cfg.get("presenter", []):
        x = decode(ROOT / "assets" / "clips" / f"clip{clip}.mp4", a, d)
        f = int(.08 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
        i = int(at * SR); x = x[: N - i]; pres[i:i + len(x)] += x
    if np.abs(pres).max() > 0:
        pres *= .5 / np.abs(pres).max()

    t = np.arange(N) / SR
    voice = np.abs(vo) + np.abs(pres)
    speech = np.convolve((voice > .02).astype(float), np.ones(int(.25 * SR)) / int(.25 * SR), "same")
    body_gain = 1.0 if m["mood"] == "hard" else .85
    g = np.where(t < e, body_gain, .9) * (1 - .6 * np.clip(speech * 3, 0, 1)) * np.clip((dur - t) / 1.5, 0, 1)
    mix = mus * g + sfx * .8 + vo + pres
    mix = mix / max(1.0, np.abs(mix).max() / .95)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())


# ---------------- video ----------------
def base_filter(cfg, dur):
    parts, labels = [], []
    for i, (clip, a, d) in enumerate(cfg["edl"]):
        f = f"[{clip - 1}:v]trim={a}:{a + d},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H}"
        if cfg.get("zoom"):
            n = int(d * FPS)
            f += f",scale={W * 2}:{H * 2},zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS}"
        parts.append(f + f",setsar=1[s{i}]"); labels.append(f"[s{i}]")
    body = sum(d for _, _, d in cfg["edl"])
    parts.append("".join(labels) + f"concat=n={len(labels)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={dur - body + 1}[bg]")
    return ";".join(parts)


def build(name):
    cfg = V[name]
    OUT.mkdir(parents=True, exist_ok=True)
    dur = cfg["S"] + ENDLEN
    n = int(round(dur * FPS))
    silent = OUT / f"_{name}.mp4"
    if cfg["edl"]:
        ins = sum((["-i", str(ROOT / "assets" / "clips" / f"clip{k}.mp4")] for k in range(1, 6)), [])
        cmd = [FF, "-y", "-loglevel", "error", *ins, "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
               "-filter_complex", base_filter(cfg, dur) + ";[bg][5:v]overlay=0:0:shortest=1,format=yuv420p[v]",
               "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), str(silent)]
    else:
        cmd = [FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
               "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(silent)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, page = open_page(p, name)
        for i in range(n):
            page.evaluate(f"seek({i / FPS})")
            proc.stdin.write(page.screenshot(type="png", omit_background=bool(cfg["edl"])))
            if i % 150 == 0:
                print(f"[{name}] frame {i}/{n}", flush=True)
        b.close()
    proc.stdin.close(); proc.wait()
    wav = OUT / f"_{name}.wav"
    build_audio(name, cfg, dur, wav)
    final = OUT / f"villaem3_{name}.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    silent.unlink(); wav.unlink()
    print("wrote", final, flush=True)


def edl_frame(cfg, t):
    acc = 0.0
    for clip, a, d in cfg["edl"]:
        if t < acc + d:
            return clip, a + (t - acc)
        acc += d
    clip, a, d = cfg["edl"][-1]
    return clip, a + d - .05


def stills():
    d = ROOT / "out" / "stills" / "v5"; d.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        for name, cfg in V.items():
            S = cfg["S"]
            times = [round(x, 2) for x in np.linspace(0.8, S - .6, 7)] + [S + 4.5, S + 10.8, S + 15.5]
            b, page = open_page(p, name)
            row = []
            for t in times:
                page.evaluate(f"seek({t})")
                ov = Image.open(io.BytesIO(page.screenshot(type="png", omit_background=bool(cfg["edl"])))).convert("RGBA")
                if cfg["edl"] and t < S:
                    clip, ct = edl_frame(cfg, t)
                    raw = subprocess.run([FF, "-v", "error", "-ss", str(ct), "-i", str(ROOT / "assets" / "clips" / f"clip{clip}.mp4"),
                                          "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-"], capture_output=True).stdout
                    base = Image.open(io.BytesIO(raw)).convert("RGBA").resize((W, H))
                else:
                    base = Image.new("RGBA", (W, H), "black")
                row.append(Image.alpha_composite(base, ov).convert("RGB").resize((180, 320)))
            b.close()
            sheet = Image.new("RGB", (180 * len(row), 320))
            for i, im in enumerate(row):
                sheet.paste(im, (i * 180, 0))
            sheet.save(d / f"{name}.png")
    ims = [Image.open(d / f"{n}.png") for n in V]
    allim = Image.new("RGB", (ims[0].width, 320 * len(ims)))
    for i, im in enumerate(ims):
        allim.paste(im, (0, i * 320))
    allim.save(d / "all.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--stills", action="store_true")
    a = ap.parse_args()
    if a.stills:
        stills()
    else:
        names = [a.only] if a.only else list(V)
        with mp.Pool(len(names)) as pool:
            pool.map(build, names)
