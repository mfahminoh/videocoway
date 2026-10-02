"""Muzik ceria + SFX kertas + voiceover Gemini (voiceover/source/neo15_tts.wav, dilajukan 1.2x) -> out/neo_papercut_final.mp4"""
import sys, subprocess, wave, numpy as np, imageio_ffmpeg, pathlib
R = pathlib.Path(__file__).parent; FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 44100; D = 15.0; N = int(D * SR)
rng = np.random.default_rng(5); t = lambda d: np.arange(int(d * SR)) / SR
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(b, s, at, g):
    i = int(at * SR)
    if 0 <= i < N: s = s[:N - i] * g; b[i:i + len(s)] += s
env = lambda d, rel: np.minimum(1, t(d) / .004) * np.exp(-t(d) / rel)
mus = np.zeros(N); sfx = np.zeros(N); beat = 60 / 108
chords = [[60, 64, 67], [57, 60, 64], [65, 69, 72], [67, 71, 74]]
for bar in range(int(D / (4 * beat)) + 1):
    ch = chords[bar % 4]
    for b in range(8):                                   # marimba-ish plucks
        n = ch[b % 3] + (12 if b % 2 else 0)
        add(mus, np.sin(2 * np.pi * hz(n) * t(.4)) * env(.4, .08), bar * 4 * beat + b * beat / 2, .09)
    for b in range(4):
        tb = bar * 4 * beat + b * beat
        add(mus, np.sin(2 * np.pi * hz(ch[0] - 24) * t(beat)) * env(beat, .25), tb, .22)
        add(mus, np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-t(.25) * 35)) / SR) * env(.25, .08), tb, .28)
        add(mus, rng.standard_normal(int(.04 * SR)) * env(.04, .015), tb + beat / 2, .05)
for s in (3.2, 6.2, 9.2, 12.2):                          # kertas luncur
    d = .45; n = rng.standard_normal(int(d * SR)); k = int(SR * .0006)
    n = np.convolve(n, np.ones(8) / 8, "same") * np.sin(np.pi * t(d) / d) ** 2
    add(sfx, n, s - .4, .35)
for p in (.25, .4, .55, .7, 1.5, 3.9, 4.3, 4.7, 7.2, 9.9, 10.3, 10.7, 13.2):   # pop
    add(sfx, np.sin(2 * np.pi * np.cumsum(700 * (1 + 1.2 * np.exp(-t(.1) * 60))) / SR) * env(.1, .03), p, .2)
for x in (9.5, 9.7): add(sfx, (np.sin(2 * np.pi * 2637 * t(.5)) + .5 * np.sin(2 * np.pi * 7280 * t(.5))) * env(.5, .15), x, .08)
raw = subprocess.run([FF, "-v", "error", "-i", str(R / "voiceover/source/neo15_tts.wav"), "-af", "atempo=1.2", "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
vo = np.zeros(N); x = np.frombuffer(raw, "<i2").astype(float) / 32768; x = x[:N]; vo[:len(x)] = x * .9 / np.abs(x).max()
c = np.cumsum(np.concatenate([np.zeros(SR // 8), (np.abs(vo) > .02).astype(float), np.zeros(SR // 4)]))
act = (c[SR // 4 + SR // 8:][:N] - c[:N]) / (SR // 4 + SR // 8) if False else np.convolve((np.abs(vo) > .02).astype(float), np.ones(SR // 4) / (SR // 4), "same")
fade = np.clip((D - t(D)[:N]) / 1.0, 0, 1)
m = (mus * .8 * (1 - .6 * np.clip(act * 3, 0, 1)) + sfx) * fade + vo
m /= max(1, np.abs(m).max() / .95)
tmp = R / "out/_neo.wav"
with wave.open(str(tmp), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype("<i2").tobytes())
subprocess.run([FF, "-y", "-v", "error", "-i", str(R / f"out/{sys.argv[1]}_noaudio.mp4"), "-i", str(tmp), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(R / f"out/{sys.argv[1]}_final.mp4")], check=True)
tmp.unlink(); print("ok")
