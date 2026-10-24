"""Split one continuous TTS take (voiceover/gemini_tts_full.wav) into the 10 script lines.

Each line is cut at the pauses found by silence detection, long internal pauses are shortened,
and the result is sped up by TEMPO (pitch kept) -> voiceover/clips/01.wav ... 10.wav.
Prints each clip's length so timeline.js can be matched to it.
"""
import pathlib
import subprocess
import wave

import imageio_ffmpeg
import numpy as np

HERE = pathlib.Path(__file__).parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 24000
TEMPO = 1.18
MAX_PAUSE = 0.18          # jeda dalam ayat dipendekkan ke ini (saat)
# (mula, tamat) setiap baris dalam fail asal — dari silencedetect (-35 dB, 0.25 s)
LINES = [(0.0, 4.21), (4.80, 9.73), (10.22, 16.50), (17.10, 21.55), (22.27, 25.99),
         (26.49, 31.37), (31.92, 34.47), (35.18, 39.11), (39.75, 43.93), (44.62, 48.21)]


def load():
    raw = subprocess.run([FF, "-v", "error", "-i", str(HERE / "gemini_tts_full.wav"), "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def squeeze(x):
    """pendekkan jeda senyap > MAX_PAUSE di dalam satu baris"""
    win = int(0.02 * SR)
    loud = np.array([np.abs(x[i:i + win]).max() > 10 ** (-35 / 20) for i in range(0, len(x), win)])
    out, run = [], 0
    for k, l in enumerate(loud):
        seg = x[k * win:(k + 1) * win]
        run = 0 if l else run + len(seg)
        if l or run <= MAX_PAUSE * SR:
            out.append(seg)
    y = np.concatenate(out)
    nz = np.nonzero(np.abs(y) > 10 ** (-40 / 20))[0]            # potong senyap hujung
    return y[max(0, nz[0] - int(.03 * SR)): nz[-1] + int(.08 * SR)]


def main():
    x = load()
    out = HERE / "clips"
    out.mkdir(exist_ok=True)
    for i, (a, b) in enumerate(LINES, 1):
        y = squeeze(x[int(a * SR):int(b * SR)])
        tmp = out / "_tmp.wav"
        with wave.open(str(tmp), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((y * 32767).astype("<i2").tobytes())
        dst = out / f"{i:02d}.wav"
        subprocess.run([FF, "-y", "-v", "error", "-i", str(tmp), "-af", f"atempo={TEMPO}", "-ar", "44100", str(dst)], check=True)
        tmp.unlink()
        with wave.open(str(dst)) as w:
            print(f"{i:02d}: {w.getnframes() / w.getframerate():.2f}s")


if __name__ == "__main__":
    main()
