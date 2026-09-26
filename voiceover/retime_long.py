"""Fit the long animation to a real voiceover recording.

Input : voiceover/source/gemini_tts_long.wav + voiceover/vo_segments_long.json (from align.py)
Output: out/warp_long.json  – piecewise-linear map output-time -> animation-time
        out/vo_long.wav     – the voiceover, each line placed at its new start (44.1 kHz mono)

Each line's animation window [start, end] (lines_long.json) is stretched/compressed to
fit its spoken length (never shorter than 60% of the original window so reveals still
breathe). Gaps between lines keep a natural pause.
"""
import json
import pathlib
import subprocess
import wave

import imageio_ffmpeg
import numpy as np

ROOT = pathlib.Path(__file__).parent.parent
V = ROOT / "voiceover"
SR = 44100
ANIM_END = 112.5
TAIL = 2.2          # CTA dibiar sedikit selepas ayat terakhir

lines = json.loads((V / "lines_long.json").read_text())
segs = {s["id"]: s for s in json.loads((V / "vo_segments_long.json").read_text())}

raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", str(V / "source" / "gemini_tts_long.wav"),
                      "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
src = np.frombuffer(raw, "<i2").astype(float) / 32768

out_pts, anim_pts = [0.0], [0.0]
o = lines[0]["start"]                      # masa output semasa
out_pts.append(o); anim_pts.append(lines[0]["start"])
place = []
for k, ln in enumerate(lines):
    sg = segs[ln["id"]]
    vo_len = sg["b"] - sg["a"]
    slot = ln["end"] - ln["start"]
    win = max(vo_len + 0.2, slot * 0.6)
    place.append((o, sg["a"], sg["b"]))
    o += win
    out_pts.append(o); anim_pts.append(ln["end"])
    if k + 1 < len(lines):
        gap_anim = lines[k + 1]["start"] - ln["end"]
        o += max(gap_anim, 0.3)
        out_pts.append(o); anim_pts.append(lines[k + 1]["start"])
out_pts.append(o + TAIL); anim_pts.append(ANIM_END)
duration = round(o + TAIL, 2)

out = ROOT / "out"
out.mkdir(exist_ok=True)
(out / "warp_long.json").write_text(json.dumps({"duration": duration, "out": out_pts, "anim": anim_pts}))

vo = np.zeros(int(duration * SR))
for t_out, a, b in place:
    clip = src[max(0, int((a - 0.04) * SR)): int((b + 0.12) * SR)].copy()
    f = int(0.01 * SR); clip[:f] *= np.linspace(0, 1, f); clip[-f:] *= np.linspace(1, 0, f)
    i = int(max(0, t_out - 0.04) * SR)
    clip = clip[: len(vo) - i]
    vo[i:i + len(clip)] += clip
with wave.open(str(out / "vo_long.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(vo, -1, 1) * 32767).astype("<i2").tobytes())

print(f"duration {duration}s")
for (t_out, a, b), ln in zip(place, lines):
    print(f"{ln['id']}: out {t_out:6.2f}  vo {b - a:5.2f}s  anim {ln['start']:6.2f}-{ln['end']:6.2f}")
