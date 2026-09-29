"""Build the soundtrack for one video folder: music bed + SFX + Gemini voiceover (ducked).

    python videos/build_audio.py videos/V05            -> out/V05_audio.wav
    python videos/build_audio.py videos/V05 --mux out/V05_noaudio.mp4 -> out/V05_final.mp4

Reads <folder>/timing.js (window.V = {off, dur, sfx: [[type, t, gain, freq?], ...]}) and <folder>/vo.wav.
SFX times are voiceover times; the voiceover is placed at `off` seconds into the video.
Everything is synthesised with numpy, so there are no music licensing issues for Meta/TikTok ads.
"""
import argparse
import json
import pathlib
import subprocess
import wave

import imageio_ffmpeg
import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100
rng = np.random.default_rng(11)


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(d, a=0.005, rel=None):
    t = tt(d)
    return np.minimum(1, t / a) * np.exp(-t / ((rel or d) / 5))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


class Track:
    def __init__(self, dur):
        self.n = int(dur * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, sig, t0, gain=1.0, pan=0.0):
        i = int(t0 * SR)
        if i >= self.n or i < 0:
            return
        sig = sig[: self.n - i] * gain
        self.L[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
        self.R[i:i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


# ---------- SFX ----------
def whoosh(d=0.5):
    t = tt(d)
    return lowpass(rng.standard_normal(len(t)), 2500) * np.sin(np.pi * t / d) ** 2


def pop(f=900, d=0.12):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 60))) / SR
    return np.sin(ph) * env(d, 0.001, 0.1)


def impact(d=1.1):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(40 + 90 * np.exp(-t * 12)) / SR
    return np.sin(ph) * env(d, 0.002, 1.0) + 0.3 * lowpass(rng.standard_normal(len(t)), 1500) * env(d, 0.001, 0.3)


def bell(f, d=0.6):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2.76 * f * t)) * env(d, 0.002, 0.5)


def shimmer(d=1.2):
    t = tt(d)
    y = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([2093, 2637, 3136, 4186]))
    return y * np.minimum(1, t / 0.02)


def tap():  # bip lembut butang sentuh panel
    d = 0.09
    return 0.7 * np.sin(2 * np.pi * 2200 * tt(d)) * env(d, 0.001, 0.07)


def tick():
    d = 0.05
    return np.sin(2 * np.pi * 1600 * tt(d)) * env(d, 0.001, 0.04)


def lock():
    d = 0.25
    thud = impact(0.25) * 0.6
    clk = np.zeros(int(d * SR))
    c = lowpass(rng.standard_normal(int(0.015 * SR)), 7000) * env(0.015, 0.0005, 0.01)
    clk[:len(c)] += c
    clk[int(0.06 * SR):int(0.06 * SR) + len(c)] += c
    return thud[:len(clk)] + clk * 1.5


def chaching():
    y = np.zeros(int(1.0 * SR))
    for i, f in enumerate([2637, 3136, 3951, 4699, 5274]):
        b = bell(f, 0.7)
        y[int(i * 0.07 * SR):int(i * 0.07 * SR) + len(b)] += b
    return y


def sfx_track(tr, events, off):
    for ev in events:
        kind, t, gain = ev[0], ev[1] + off, ev[2]
        f = ev[3] if len(ev) > 3 else 900
        sig = {"whoosh": whoosh, "impact": impact, "shimmer": shimmer, "tick": tick, "lock": lock,
               "chaching": chaching, "tap": tap, "pop": lambda: pop(f)}[kind]
        tr.add(sig(), t, gain)


# ---------- Muzik: 100 BPM, pop cerah I-V-vi-IV ----------
def music(tr, dur, drop):
    bpm = 100
    beat = 60 / bpm
    bar = 4 * beat
    chords = [[50, 57, 62, 66, 69], [45, 57, 61, 64, 69], [47, 59, 62, 66, 71], [43, 55, 59, 62, 67]]  # D A Bm G
    arp = [[74, 78, 81, 78], [73, 76, 81, 76], [74, 78, 83, 78], [71, 74, 79, 74]]
    t0, k = 0.0, 0
    while t0 < dur:
        ch = chords[k % 4]
        d = bar + 0.4
        t = tt(d)
        pad = sum(np.sin(2 * np.pi * hz(m) * t + 0.3 * np.sin(2 * np.pi * 0.3 * t)) for m in ch[1:])
        tr.add(pad * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.4), t0, 0.03)
        for b in range(4):
            tb = t0 + b * beat
            bd = beat * 0.9
            tr.add(np.sin(2 * np.pi * hz(ch[0] - 12) * tt(bd)) * env(bd, 0.01, bd * 1.6), tb, 0.15 if tb >= drop else 0.07)
            if tb >= drop:
                kd = 0.3
                ph = 2 * np.pi * np.cumsum(50 + 110 * np.exp(-tt(kd) * 30)) / SR
                tr.add(np.sin(ph) * env(kd, 0.001, 0.3), tb, 0.42)
                tr.add(rng.standard_normal(int(0.05 * SR)) * env(0.05, 0.001, 0.04), tb + beat / 2, 0.05, 0.2)
                if b in (1, 3):
                    sd = 0.16
                    tr.add(lowpass(rng.standard_normal(int(sd * SR)), 5000) * env(sd, 0.001, 0.14), tb, 0.13)
            elif b in (1, 3):
                cd = 0.04
                tr.add(lowpass(rng.standard_normal(int(cd * SR)), 3500) * env(cd, 0.001, 0.03), tb, 0.1)
        for j in range(8):
            tn = t0 + j * beat / 2
            m = arp[k % 4][j % 4] + (12 if j >= 4 and tn >= drop else 0)
            x = np.sin(2 * np.pi * hz(m) * tt(0.4)) + 0.3 * np.sin(2 * np.pi * 2 * hz(m) * tt(0.4))
            tr.add(x * env(0.4, 0.003, 0.3), tn, 0.05, 0.35 if j % 2 else -0.35)
        k += 1
        t0 += bar


def decode(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def main(folder, mux=None):
    folder = pathlib.Path(folder)
    V = json.loads((folder / "timing.js").read_text().split("=", 1)[1].strip().rstrip(";"))
    dur, off = V["dur"], V["off"]
    drop = next((e[1] for e in V["sfx"] if e[0] == "impact"), 3.0) + off

    mus = Track(dur)
    music(mus, dur, drop)
    fx = Track(dur)
    sfx_track(fx, V["sfx"], off)
    t = np.arange(mus.n) / SR
    fade = np.minimum(1, t / 0.3) * np.clip((dur - t) / 1.2, 0, 1)

    vo = np.zeros(mus.n)
    x = decode(folder / "vo.wav")
    i = int(off * SR)
    x = x[: mus.n - i]
    vo[i:i + len(x)] = x / (np.abs(x).max() + 1e-9) * 0.92
    k = int(0.25 * SR)
    active = np.convolve((np.abs(vo) > 0.02).astype(float), np.ones(k) / k, mode="same")
    duck = 1 - 0.6 * np.clip(active * 3, 0, 1)                   # muzik turun ~8 dB bila ada suara

    Lm = (mus.L * duck + fx.L * 0.8) * fade + vo * np.sqrt(0.5)
    Rm = (mus.R * duck + fx.R * 0.8) * fade + vo * np.sqrt(0.5)
    peak = max(np.abs(Lm).max(), np.abs(Rm).max())
    Lm, Rm = Lm / peak * 0.93, Rm / peak * 0.93
    name = folder.name
    out = ROOT / "out" / f"{name}_audio.wav"
    out.parent.mkdir(exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.stack([Lm, Rm], 1) * 32767).astype("<i2").tobytes())
    print("wrote", out)
    if mux:
        final = ROOT / "out" / f"{name}_final.mp4"
        subprocess.run([FF, "-y", "-v", "error", "-i", str(mux), "-i", str(out), "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)], check=True)
        print("wrote", final)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--mux")
    a = ap.parse_args()
    main(a.folder, a.mux)
