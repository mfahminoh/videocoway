"""Mux the rendered video with music/SFX and (if present) the voiceover clips.

    python mix.py            -> out/villaem3_final.mp4       (30s; clips in voiceover/clips/)
    python mix.py --long     -> out/villaem3_long_final.mp4  (1:52; clips in voiceover/clips_long/)

Voiceover clips are placed at the start times in voiceover/lines.json, and the music bed
is ducked (~-9 dB) underneath the voice.
"""
import argparse
import json
import pathlib
import subprocess
import wave

import imageio_ffmpeg
import numpy as np

ROOT = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100


def read_wav(path):
    with wave.open(str(path)) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
        return x.reshape(-1, w.getnchannels())


def decode(path):
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def smooth(x, sec):
    n = max(1, int(sec * SR))
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


def main(long=False):
    sfx = "_long" if long else ""
    bed = read_wav(ROOT / "out" / f"music_sfx{sfx}.wav")
    N = len(bed)
    vo = np.zeros(N)
    lines = json.loads((ROOT / "voiceover" / f"lines{sfx}.json").read_text())
    used = 0
    placed = ROOT / "out" / "vo_long.wav"
    if long and placed.exists():            # voiceover sebenar, sudah diletak oleh retime_long.py
        x = decode(placed)[:N]
        vo[:len(x)] = x
        used = len(lines)
        lines = []
    for ln in lines:
        clip = ROOT / "voiceover" / f"clips{sfx}" / f"{ln['id']}.mp3"
        if not clip.exists():
            clip = clip.with_suffix(".wav")
        if not clip.exists():
            continue
        x = decode(clip)
        i = int(ln["start"] * SR)
        x = x[: N - i]
        vo[i:i + len(x)] += x
        used += 1

    if used:
        vo = vo / (np.abs(vo).max() + 1e-9) * 0.9
        active = smooth((np.abs(vo) > 0.02).astype(float), 0.25)
        duck = 1 - 0.65 * np.clip(active * 3, 0, 1)             # ~ -9 dB bila ada suara
        mix = bed * 0.75 * duck[:, None] + vo[:, None]
    else:
        mix = bed
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)

    tmp = ROOT / "out" / "_mix.wav"
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())

    out = ROOT / "out" / f"villaem3{sfx}_final.mp4"
    subprocess.run([FF, "-y", "-v", "error", "-i", str(ROOT / "out" / f"villaem3{sfx}_video_noaudio.mp4"), "-i", str(tmp),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
                   check=True)
    tmp.unlink()
    print(f"wrote {out}  (voiceover lines: {used})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--long", action="store_true")
    main(ap.parse_args().long)
