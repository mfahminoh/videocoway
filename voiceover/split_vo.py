"""Split one long voiceover recording into per-line clips for mix.py.

    python voiceover/split_vo.py --ad best3 voiceover/best3/source/gemini-tts_3.wav \
        --cuts 4.1,9.2,19.8,28.2,37.4 --tempo 1.1

--cuts are the times (s) in the source where one paragraph ends and the next begins (pick the middle of
the pause). Each paragraph gets leading/trailing silence trimmed, pauses inside it shortened to --gap
seconds, and is sped up by --tempo (pitch kept). Writes voiceover/<ad>/clips/01.wav, 02.wav, ... and
prints each clip's length plus where its sentences start, for lining up the animation.
"""
import argparse
import pathlib
import wave

import imageio_ffmpeg
import numpy as np
import subprocess

HERE = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100


def load(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def speech_runs(x, thresh_db=-40, min_gap=0.2):
    """[(start, end)] sample ranges of speech, split on pauses longer than min_gap."""
    win = int(0.01 * SR)
    n = len(x) // win
    rms = np.sqrt((x[: n * win].reshape(n, win) ** 2).mean(1) + 1e-12)
    loud = 20 * np.log10(rms) > thresh_db
    runs, start, quiet = [], None, 0
    for i, v in enumerate(loud):
        if v:
            if start is None:
                start = i
            quiet = 0
        elif start is not None:
            quiet += 1
            if quiet * 0.01 >= min_gap:
                runs.append((start * win, (i - quiet + 1) * win))
                start, quiet = None, 0
    if start is not None:
        runs.append((start * win, (n - quiet) * win))
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--ad", default="best3")
    ap.add_argument("--cuts", required=True)
    ap.add_argument("--tempo", type=float, default=1.0)
    ap.add_argument("--gap", type=float, default=0.15)
    a = ap.parse_args()
    x = load(a.src)
    cuts = [0] + [int(float(c) * SR) for c in a.cuts.split(",")] + [len(x)]
    out = HERE / a.ad / "clips"
    out.mkdir(parents=True, exist_ok=True)
    pad = int(0.03 * SR)
    for k in range(len(cuts) - 1):
        seg = x[cuts[k]:cuts[k + 1]]
        runs = speech_runs(seg)
        gap = np.zeros(int(a.gap * SR))
        parts, starts, t = [], [], 0
        for i, (s, e) in enumerate(runs):
            piece = seg[max(0, s - pad):min(len(seg), e + pad)]
            if i:
                parts.append(gap)
                t += len(gap)
            starts.append(t / SR / a.tempo)
            parts.append(piece)
            t += len(piece)
        y = np.concatenate(parts)
        tmp = out / f"_{k + 1:02d}.wav"
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())
        dest = out / f"{k + 1:02d}.wav"
        subprocess.run([FF, "-v", "error", "-y", "-i", str(tmp), "-af", f"atempo={a.tempo}", str(dest)], check=True)
        tmp.unlink()
        print(f"{k + 1:02d}: {len(y) / SR / a.tempo:5.2f}s  sentences at " + ", ".join(f"{s:.2f}" for s in starts))


if __name__ == "__main__":
    main()
