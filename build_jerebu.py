"""Pakej video Jerebu (penapis udara Coway) -> out/jerebu/<nama>.mp4

    python voiceover/jerebu/generate_vo.py        # 1) VO Gemini -> voiceover/jerebu/<nama>/NN.wav
    python build_jerebu.py --timing               # 2) masa babak ikut panjang VO -> src/jerebu/timing/*.js
    python build_jerebu.py --stills               # 3) pratonton -> out/stills/jerebu/<nama>.png
    python build_jerebu.py [--only j2_kenapa_merah] [--jobs 2]   # 4) render + audio

Babak N dalam src/jerebu/<nama>.html = baris N dalam voiceover/jerebu/skrip.json.
Tukar skrip -> jana VO semula -> --timing -> render. Animasi ikut masa VO secara automatik.
"""
import argparse
import io
import json
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
SRC, VO, OUT = ROOT / "src" / "jerebu", ROOT / "voiceover" / "jerebu", ROOT / "out" / "jerebu"
LEAD, TAIL, END_HOLD = .35, .45, 3.2

# muzik latar setiap video: tempo, mod (minor -> major pada 'lift' = indeks babak), dram mula babak ke-
MUSIC = {
    "j1_masuk_rumah":  dict(bpm=78, lift=5, drums=1, gain=.9),
    "j2_kenapa_merah": dict(bpm=104, lift=4, drums=0, gain=1.0),
    "j3_pm25":         dict(bpm=70, lift=6, drums=2, gain=.85),
    "j4_tips":         dict(bpm=110, lift=0, drums=0, gain=.9),
    "j5_pilih_model":  dict(bpm=100, lift=0, drums=0, gain=.9),
    "j6_lepas_jerebu": dict(bpm=96, lift=1, drums=1, gain=1.0),
}
NAMES = list(MUSIC)


def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def timing(name):
    n = len(json.loads((VO / "skrip.json").read_text())[name]["scenes"])
    if not (VO / name / f"{n:02d}.wav").exists():      # klip babak tak disimpan dalam git: potong dari full.wav
        subprocess.run(["python3", str(VO / "generate_vo.py"), "--only", name, "--split-only"], check=True)
    durs = [wav_len(VO / name / f"{i + 1:02d}.wav") for i in range(n)]
    t, rows = 0.0, []
    for i, d in enumerate(durs):
        lead = .3 if i == 0 else LEAD
        e = t + lead + d + (END_HOLD if i == n - 1 else TAIL)
        rows.append([round(t, 3), round(e, 3), round(t + lead, 3), round(d, 3)])
        t = e
    T = {"scenes": rows, "duration": round(t, 3)}
    (SRC / "timing").mkdir(exist_ok=True)
    (SRC / "timing" / f"{name}.js").write_text("window.TIMING = " + json.dumps(T) + ";\n")
    return T


def load_T(name):
    return json.loads((SRC / "timing" / f"{name}.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))


def open_page(p, name):
    b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = b.new_page(viewport={"width": W, "height": H})
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto((SRC / f"{name}.html").as_uri())
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].every(i => i.complete)")
    if errs:
        raise RuntimeError(f"{name}: {errs}")
    return b, page


# ---------------- audio ----------------
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=.005, rel=None): t = tt(d); return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))
def hz(m): return 440 * 2 ** ((m - 69) / 12)


def onepole(x, c):
    """Penapis lulus rendah satu kutub (vektor, guna lfilter-gaya kumulatif blok)."""
    a = np.exp(-2 * np.pi * c / SR); y = np.empty_like(x); acc = 0.0
    for i in range(0, len(x), 4096):          # gelung blok kecil — cukup laju untuk SFX pendek
        blk = x[i:i + 4096]; out = np.empty_like(blk)
        for j, v in enumerate(blk):
            acc = (1 - a) * v + a * acc; out[j] = acc
        y[i:i + 4096] = out
    return y


MAJOR = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]
MINOR = [[45, 57, 60, 64], [41, 53, 57, 60], [48, 55, 60, 64], [43, 55, 59, 62]]


def build_audio(name, T, path):
    m = MUSIC[name]; dur = T["duration"]; N = int(dur * SR); rng = np.random.default_rng(7)
    mus, sfx, vo = np.zeros(N), np.zeros(N), np.zeros(N)
    sc = T["scenes"]; lift_t = sc[m["lift"]][0]; drums_t = sc[m["drums"]][0]

    def add(buf, sig, t0, g):
        i = int(t0 * SR)
        if 0 <= i < N:
            s = sig[:N - i] * g; buf[i:i + len(s)] += s

    beat = 60 / m["bpm"]; t0 = 0.0; bi = 0
    while t0 < dur:
        minor = t0 < lift_t
        ch = (MINOR if minor else MAJOR)[bi % 4]; d = 4 * beat + .4; t = tt(d)
        pad = sum(np.sin(2 * np.pi * hz(n) * t + .3 * np.sin(2 * np.pi * .3 * t)) for n in ch[1:]) + .5 * np.sin(2 * np.pi * hz(ch[0]) * t)
        add(mus, pad * np.minimum(1, t / .5) * np.minimum(1, (d - t) / .5), t0, .04)
        for b in range(4):
            tb = t0 + b * beat
            add(mus, np.sin(2 * np.pi * hz(ch[0] - 12) * tt(beat * .9)) * env(beat * .9, .01, beat * 1.4), tb, .13)
            if tb >= drums_t:
                kd = .35
                add(mus, np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR) * env(kd, .001, .3), tb, .38)
                add(mus, rng.standard_normal(int(.05 * SR)) * env(.05, .001, .04), tb + beat / 2, .04)
                if b in (1, 3) and not minor:
                    add(mus, rng.standard_normal(int(.15 * SR)) * env(.15, .001, .12), tb, .07)
        for k in range(8):
            n = ch[1 + k % (len(ch) - 1)] + 12 + (12 if k % 2 else 0)
            add(mus, np.sin(2 * np.pi * hz(n) * tt(.5)) * env(.5, .003, .4), t0 + k * beat / 2, .035)
        bi += 1; t0 += 4 * beat

    def whoosh(d=.45):
        t = tt(d); return onepole(rng.standard_normal(len(t)), 2500) * np.sin(np.pi * t / d) ** 2
    def pop(f=900, d=.12):
        t = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(d, .001, .1)
    w = whoosh()
    for i, (s, e, vs, vd) in enumerate(sc):
        if i:
            add(sfx, w, s - .25, .3)
        add(sfx, pop(850 + 70 * (i % 4)), s + .1, .18)
        clip = VO / name / f"{i + 1:02d}.wav"
        raw = subprocess.run([FF, "-v", "error", "-i", str(clip), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, "<i2").astype(float) / 32768
        add(vo, x / max(.05, np.abs(x).max()) * .82, vs, 1.0)
    # duck muzik bawah suara
    a = np.abs(vo); k = int(.25 * SR); c = np.cumsum(np.concatenate([np.zeros(k), a]))
    speech = np.clip((c[k:] - c[:-k]) / k * 8, 0, 1)
    tail = np.clip((dur - np.arange(N) / SR) / 1.5, 0, 1)
    mix = (mus * m["gain"] * (1 - .55 * speech) + sfx * .7) * tail + vo
    mix = mix / max(1.0, np.abs(mix).max() / .97)
    with wave.open(str(path), "wb") as wv:
        wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR)
        wv.writeframes((mix * 32767).astype("<i2").tobytes())


# ---------------- video ----------------
def render_part(args):
    name, i0, i1, path = args
    cmd = [FF, "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(path)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, page = open_page(p, name)
        for i in range(i0, i1):
            page.evaluate(f"seek({i / FPS})")
            proc.stdin.write(page.screenshot(type="png"))
            if (i - i0) % 300 == 0:
                print(f"[{name}] {i}/{i1}", flush=True)
        b.close()
    proc.stdin.close(); proc.wait()


def build(name, jobs):
    OUT.mkdir(parents=True, exist_ok=True)
    T = load_T(name); n = int(round(T["duration"] * FPS))
    cuts = np.linspace(0, n, jobs + 1).astype(int)
    parts = [(name, int(a), int(b), OUT / f"_{name}_{k}.mp4") for k, (a, b) in enumerate(zip(cuts[:-1], cuts[1:]))]
    with mp.Pool(jobs) as pool:
        pool.map(render_part, parts)
    lst = OUT / f"_{name}.txt"; lst.write_text("".join(f"file '{x[3].name}'\n" for x in parts))
    silent = OUT / f"_{name}.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(silent)], check=True)
    wav = OUT / f"_{name}.wav"; build_audio(name, T, wav)
    final = OUT / f"coway_jerebu_{name}.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    for x in parts:
        x[3].unlink()
    for x in (lst, silent, wav):
        x.unlink()
    print("siap:", final, f"({T['duration']:.1f}s)", flush=True)


def stills(names, per=3):
    d = ROOT / "out" / "stills" / "jerebu"; d.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        for name in names:
            T = load_T(name); times = []
            for s, e, vs, vd in T["scenes"]:
                times += [round(vs + vd * f, 2) for f in np.linspace(.15, 1.0, per)]
            b, page = open_page(p, name); row = []
            for t in times:
                page.evaluate(f"seek({t})")
                row.append(Image.open(io.BytesIO(page.screenshot(type="png"))).convert("RGB").resize((216, 384)))
            b.close()
            cols = per * 4; rows = -(-len(row) // cols)
            sheet = Image.new("RGB", (216 * cols, 384 * rows), "black")
            for i, im in enumerate(row):
                sheet.paste(im, ((i % cols) * 216, (i // cols) * 384))
            sheet.save(d / f"{name}.jpg", quality=85)
            print("stills:", d / f"{name}.jpg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timing", action="store_true"); ap.add_argument("--stills", action="store_true")
    a = ap.parse_args()
    names = [a.only] if a.only else NAMES
    if a.timing:
        for nm in names:
            T = timing(nm); print(nm, f"{T['duration']:.1f}s")
    elif a.stills:
        stills(names)
    else:
        for nm in names:
            build(nm, a.jobs)
