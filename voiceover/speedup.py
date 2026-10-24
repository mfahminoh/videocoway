"""Make a voiceover faster: cap long pauses, then time-stretch (pitch kept). Segments are remapped.
    python3 voiceover/speedup.py videos/PA01 [--tempo 1.15 --maxpause 0.3]
Keeps the original as vo_slow.wav / segments_slow.json (re-running starts from those)."""
import argparse, json, pathlib, shutil, subprocess, wave
import numpy as np, imageio_ffmpeg
ap = argparse.ArgumentParser(); ap.add_argument("folder"); ap.add_argument("--tempo", type=float, default=1.15); ap.add_argument("--maxpause", type=float, default=0.3)
a = ap.parse_args(); d = pathlib.Path(a.folder)
for s, t in (("vo.wav", "vo_slow.wav"), ("segments.json", "segments_slow.json")):
    if not (d / t).exists(): shutil.copy(d / s, d / t)
w = wave.open(str(d / "vo_slow.wav")); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2")
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt(((x[:n * hop] / 32768.0).reshape(n, hop) ** 2).mean(1)) + 1e-9); sil = db < db.max() - 40
keep, src_t, dst_t, out_len, i = [], [0.0], [0.0], 0, 0
while i < n:
    j = i
    while j < n and sil[j] == sil[i]: j += 1
    seg = (i * hop, j * hop)
    if sil[i] and (j - i) / 100 > a.maxpause:
        k = int(a.maxpause * sr); keep.append((seg[0], seg[0] + k // 2)); keep.append((seg[1] - k // 2, seg[1]))
        src_t += [seg[0] / sr + a.maxpause / 2, seg[1] / sr - a.maxpause / 2]; dst_t += [(out_len + k // 2) / sr] * 2; out_len += k
    else:
        keep.append(seg); out_len += seg[1] - seg[0]
    i = j
src_t.append(len(x) / sr); dst_t.append(out_len / sr)
y = np.concatenate([x[s:e] for s, e in keep])
FF = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([FF, "-v", "error", "-y", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", f"atempo={a.tempo}", str(d / "vo.wav")], input=y.tobytes(), check=True)
f = lambda t: float(np.interp(t, src_t, dst_t)) / a.tempo
segs = [{**g, "a": round(f(g["a"]), 2), "b": round(f(g["b"]), 2)} for g in json.load(open(d / "segments_slow.json"))]
json.dump(segs, open(d / "segments.json", "w"), indent=1)
print(d, f"{len(x)/sr:.1f}s -> {segs[-1]['b']:.1f}s")
