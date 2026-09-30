"""Build one Meta ad per presenter clip (assets/clips/clip1..5.mp4) -> out/clipads/villaem3_klip{N}.mp4

Each video: 0–10s the clip (presenter audio kept) with captions + cover panels over outdated/misspelt
baked-in text, then a shared promo + CTA end card voiced with segments of the Gemini voiceover.

    python build_clipads.py                 # all 5 videos
    python build_clipads.py --only 2        # one video
    python build_clipads.py --stills        # preview frames -> out/stills/clipads/
"""
import argparse
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
FOOT = 10.0
END = 31.6
CHROMIUM = next((str(x) for x in [pathlib.Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")] if x.exists()), None)
OUT = ROOT / "out" / "clipads"

# Petikan voiceover Gemini (saat dalam voiceover/source/gemini_tts_long.wav) -> masa dalam video.
# Sempadan ayat dikesan dari jeda (lihat voiceover/align.py): ayat promo baris 12 dan CTA baris 13.
VO = [
    (70.62, 73.04, FOOT + 0.30),   # "Harga asal seratus dua puluh ringgit sebulan."
    (73.25, 77.61, FOOT + 3.05),   # "Tapi sekarang ada promosi diskaun, serendah tujuh puluh empat ringgit je sebulan."
    (78.15, 83.24, FOOT + 7.75),   # "Dan ganda lagi dengan rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan!"
    (87.25, 88.83, FOOT + 13.20),  # "Ni last call untuk promo ni."
    (89.10, 94.39, FOOT + 15.15),  # "Kalau anda tengah cari penapis air high spec, ... WhatsApp saya sekarang."
]


def open_page(p, v):
    b = p.chromium.launch(executable_path=CHROMIUM) if CHROMIUM else p.chromium.launch()
    page = b.new_page(viewport={"width": W, "height": H})
    page.goto((ROOT / "src" / "clipads.html").as_uri() + f"?v={v}")
    page.evaluate("document.fonts.ready")
    page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
    return b, page


def decode(path, start=None, dur=None, ch=1):
    cmd = [FF, "-v", "error"] + (["-ss", str(start)] if start is not None else []) + ["-i", str(path)]
    cmd += (["-t", str(dur)] if dur else []) + ["-vn", "-f", "s16le", "-ac", str(ch), "-ar", str(SR), "-"]
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, "<i2").astype(float) / 32768
    return x.reshape(-1, ch) if ch > 1 else x


# ---------------- audio ----------------
rng = np.random.default_rng(3)


def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=.005, rel=None): t = tt(d); return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))
def hz(m): return 440 * 2 ** ((m - 69) / 12)


def lowpass(x, c):
    a = np.exp(-2 * np.pi * np.asarray(c, float) / SR) * np.ones_like(x); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc; y[i] = acc
    return y


def build_audio(v, path):
    N = int(END * SR)
    mus = np.zeros(N); sfx = np.zeros(N)

    def add(buf, sig, t0, g):
        i = int(t0 * SR)
        if i < N:
            s = sig[: N - i] * g; buf[i:i + len(s)] += s

    beat = 60 / 108
    chords = [[48, 55, 60, 64, 67], [43, 55, 59, 62, 67], [45, 57, 60, 64, 69], [41, 53, 57, 60, 65]]
    arp = [[72, 76, 79, 76], [71, 74, 79, 74], [72, 76, 81, 76], [69, 72, 77, 72]]
    t0, bi = 0.0, 0
    while t0 < END:
        ch = chords[bi % 4]; d = 4 * beat + .4; t = tt(d)
        pad = sum(np.sin(2 * np.pi * hz(m) * t) for m in ch[1:]) + .5 * np.sin(2 * np.pi * hz(ch[0]) * t)
        add(mus, pad * np.minimum(1, t / .35) * np.minimum(1, (d - t) / .4), t0, .035)
        for b in range(4):
            tb = t0 + b * beat
            add(mus, np.sin(2 * np.pi * hz(ch[0] - 12) * tt(beat * .9)) * env(beat * .9, .01, beat * 1.4), tb, .14)
            if tb >= FOOT:
                ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(.35) * 30)) / SR
                add(mus, np.sin(ph) * env(.35, .001, .3), tb, .4)
                add(mus, rng.standard_normal(int(.06 * SR)) * env(.06, .001, .05), tb + beat / 2, .05)
        for k in range(8):
            m = arp[bi % 4][k % 4] + (12 if k >= 4 else 0)
            add(mus, np.sin(2 * np.pi * hz(m) * tt(.45)) * env(.45, .003, .35), t0 + k * beat / 2, .05)
        bi += 1; t0 += 4 * beat

    def pop(f=900, d=.12): t = tt(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR) * env(d, .001, .1)
    def whoosh(d=.55): t = tt(d); return lowpass(rng.standard_normal(len(t)), 400 + 5000 * (t / d) ** 2) * np.sin(np.pi * t / d) ** 2
    def impact(d=.9): t = tt(d); return np.sin(2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR) * env(d, .002, .8)
    def bell(f, d=.6): t = tt(d); return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, .002, .5)

    bands = {1: [.2, 3.1, 7.1], 2: [.2, 3.1, 6.1], 3: [.2, 3.1, 6.4], 4: [.2, 3.1, 6.1], 5: [.2, 3.6, 6.1]}[v]
    for i, b in enumerate(bands):
        add(sfx, pop(900 + 150 * i), b, .22)
    add(sfx, whoosh(), FOOT - .15, .3)
    te = FOOT
    add(sfx, pop(1200), te + .2, .3)
    add(sfx, lowpass(rng.standard_normal(int(.35 * SR)), 3000) * np.sin(np.pi * tt(.35) / .35), te + 2.0, .15)
    add(sfx, impact(), te + 4.6, .45)
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
        add(sfx, bell(f, .7), te + 6.2 + i * .07, .07)
    add(sfx, impact(), te + 7.8, .4)
    add(sfx, pop(1100), te + 8.5, .3)
    add(sfx, pop(1000), te + 11.8, .25); add(sfx, pop(1150), te + 12.3, .25)
    for x in (te + 13.2, te + 13.45):
        add(sfx, bell(1760, .2), x, .12)
    add(sfx, whoosh(), te + 14.85, .25)
    add(sfx, impact(.6), te + 15.5, .3); add(sfx, impact(.6), te + 16.0, .3)
    add(sfx, pop(900, .2), te + 17.0, .3)

    # suara presenter (kekal sebahagian: 0–10s), fade keluar hujung footage
    pres = decode(ROOT / "assets" / "clips" / f"clip{v}.mp4", 0, FOOT)
    fade = np.clip((FOOT - np.arange(len(pres)) / SR) / .4, 0, 1)
    pres = pres * fade
    # voiceover Gemini untuk kad promo
    src = decode(ROOT / "voiceover" / "source" / "gemini_tts_long.wav")
    vo = np.zeros(N)
    for a, b, at in VO:
        c = src[int((a - .04) * SR): int((b + .12) * SR)].copy()
        f = int(.01 * SR); c[:f] *= np.linspace(0, 1, f); c[-f:] *= np.linspace(1, 0, f)
        i = int((at - .04) * SR); c = c[: N - i]; vo[i:i + len(c)] += c
    vo *= .9 / (np.abs(vo).max() + 1e-9)

    t = np.arange(N) / SR
    speech = np.convolve((np.abs(vo) > .02).astype(float), np.ones(int(.25 * SR)) / int(.25 * SR), "same")
    music_gain = np.where(t < FOOT, .35, 1.0) * (1 - .6 * np.clip(speech * 3, 0, 1))
    music_gain *= np.clip((END - t) / 1.5, 0, 1)
    mix = mus * music_gain + sfx * .8 + vo
    mix[:len(pres)] += pres * (.85 / (np.abs(pres).max() + 1e-9))
    mix = mix / max(1.0, np.abs(mix).max() / .95)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())


# ---------------- video ----------------
def build(v):
    OUT.mkdir(parents=True, exist_ok=True)
    silent = OUT / f"_v{v}.mp4"
    clip = ROOT / "assets" / "clips" / f"clip{v}.mp4"
    n = int(round(END * FPS))
    proc = subprocess.Popen(
        [FF, "-y", "-loglevel", "error",
         "-i", str(clip),
         "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
         "-filter_complex",
         f"[0:v]trim=0:{FOOT},setpts=PTS-STARTPTS,fps={FPS},scale={W}:{H},tpad=stop_mode=clone:stop_duration={END - FOOT + 1}[bg];"
         f"[bg][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
         "-map", "[v]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS), str(silent)],
        stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, page = open_page(p, v)
        for i in range(n):
            page.evaluate(f"seek({i / FPS})")
            proc.stdin.write(page.screenshot(type="png", omit_background=True))
            if i % 150 == 0:
                print(f"[klip{v}] frame {i}/{n}", flush=True)
        b.close()
    proc.stdin.close(); proc.wait()
    wav = OUT / f"_v{v}.wav"
    build_audio(v, wav)
    final = OUT / f"villaem3_klip{v}.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(final)], check=True)
    silent.unlink(); wav.unlink()
    print("wrote", final, flush=True)
    return final


def stills(times):
    d = ROOT / "out" / "stills" / "clipads"; d.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        for v in range(1, 6):
            b, page = open_page(p, v)
            row = []
            for t in times:
                page.evaluate(f"seek({t})")
                ov = Image.open(__import__("io").BytesIO(page.screenshot(type="png", omit_background=True))).convert("RGBA")
                if t < FOOT:
                    raw = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", str(ROOT / "assets" / "clips" / f"clip{v}.mp4"),
                                          "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-"], capture_output=True).stdout
                    base = Image.open(__import__("io").BytesIO(raw)).convert("RGBA").resize((W, H))
                else:
                    base = Image.new("RGBA", (W, H), "black")
                row.append(Image.alpha_composite(base, ov).convert("RGB").resize((216, 384)))
            b.close()
            sheet = Image.new("RGB", (216 * len(row), 384))
            for i, im in enumerate(row): sheet.paste(im, (i * 216, 0))
            sheet.save(d / f"klip{v}.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int)
    ap.add_argument("--stills", action="store_true")
    a = ap.parse_args()
    if a.stills:
        stills([1.5, 4.5, 8.0, 12.5, 16.5, 19.0, 23.8, 28.0])
    else:
        vids = [a.only] if a.only else [1, 2, 3, 4, 5]
        with mp.Pool(min(5, len(vids))) as pool:
            pool.map(build, vids)
