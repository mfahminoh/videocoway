"""Ganti beberapa baris VO tanpa jana semula keseluruhan skrip.

    python tilam/vo/splice.py v16 tilam/vo/v16_patch.wav 06 07 09
Patch = satu fail TTS berisi baris-baris baharu ikut turutan (dipisah jeda). Ia dipecah pada jeda paling panjang,
dilajukan sama seperti split.py, dan menggantikan baris tersebut dalam <v>_vo.wav + <v>_timing.json.
"""
import json, pathlib, subprocess, sys, wave
import imageio_ffmpeg, numpy as np
from split import SR, TEMPO, GAP, LEAD

D = pathlib.Path(__file__).parent; FF = imageio_ffmpeg.get_ffmpeg_exe()
V, patch, ids = sys.argv[1], sys.argv[2], sys.argv[3:]


def load(path, tempo=None):
    af = ["-af", f"atempo={tempo}"] if tempo else []
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), *af, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def trim(seg):
    hop = SR // 100; r = np.sqrt(np.convolve(seg ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop])
    on = np.nonzero(r >= .006)[0]
    seg = seg[max(0, on[0] * hop - hop * 3):(on[-1] + 5) * hop].copy()
    f = int(.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    return seg


old = load(D / f"{V}_vo.wav"); timing = json.loads((D / f"{V}_timing.json").read_text())
lines = {l["id"]: l for l in json.loads((D / f"lines_{V}.json").read_text())}
p = load(patch, TEMPO); hop = SR // 100
q = np.sqrt(np.convolve(p ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop]) < .006
gaps, i = [], 0
while i < len(q):
    if q[i]:
        j = i
        while j < len(q) and q[j]: j += 1
        if 0 < i and j < len(q): gaps.append((j - i, i, j))
        i = j
    else: i += 1
cuts = sorted(sorted(gaps, reverse=True)[:len(ids) - 1], key=lambda g: g[1])
bounds = [0] + [((a + b) // 2) * hop for _, a, b in cuts] + [len(p)]
new = {k: trim(p[bounds[n]:bounds[n + 1]]) for n, k in enumerate(ids)}

out, t, tm = [np.zeros(int(LEAD * SR))], LEAD, []
for x in timing:
    seg = new.get(x["id"])
    if seg is None: seg = old[int(x["start"] * SR):int(x["end"] * SR)]
    ln = lines[x["id"]]
    tm.append(dict(id=x["id"], scene=ln["scene"], start=round(t, 3), end=round(t + len(seg) / SR, 3), text=ln["text"]))
    out += [seg, np.zeros(int(GAP * SR))]; t += len(seg) / SR + GAP
y = np.concatenate(out); y *= .89 / np.abs(y).max()
with wave.open(str(D / f"{V}_vo.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype("<i2").tobytes())
(D / f"{V}_timing.json").write_text(json.dumps(tm, ensure_ascii=False, indent=1))
for x in tm: print(f'{x["id"]} {x["scene"]:9s} {x["start"]:6.2f}-{x["end"]:6.2f} ({x["end"]-x["start"]:.2f}s) {x["text"][:55]}')
print("jumlah", round(t, 2))
