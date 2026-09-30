"""Mux the rendered video with music/SFX and (if present) the voiceover clips.

    python mix.py                     # video utama
    python mix.py --video V --bed B --lines L --clips C --out O   # cth. Reels
      -> out/coway_ice_final.mp4   (music + SFX, + VO when voiceover/clips/*.mp3 exist)

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
    k = np.ones(n) / n
    return np.convolve(x, k, mode="same")


def main(a):
    bed = read_wav(a.bed)
    N = len(bed)
    vo = np.zeros(N)
    lines = json.loads(pathlib.Path(a.lines).read_text())
    used = 0
    for ln in lines:
        clip = pathlib.Path(a.clips) / f"{ln['id']}.mp3"
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

    tmp = pathlib.Path(a.out).with_suffix(".mix.wav")
    with wave.open(str(tmp), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((mix * 32767).astype("<i2").tobytes())

    out = pathlib.Path(a.out)
    subprocess.run([FF, "-y", "-v", "error", "-i", str(a.video), "-i", str(tmp),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
                   check=True)
    tmp.unlink()
    print(f"wrote {out}  (voiceover clips used: {used}/{len(lines)})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=str(ROOT / "out" / "coway_ice_video_noaudio.mp4"))
    ap.add_argument("--bed", default=str(ROOT / "out" / "music_sfx.wav"))
    ap.add_argument("--lines", default=str(ROOT / "voiceover" / "lines.json"))
    ap.add_argument("--clips", default=str(ROOT / "voiceover" / "clips"))
    ap.add_argument("--out", default=str(ROOT / "out" / "coway_ice_final.mp4"))
    main(ap.parse_args())
