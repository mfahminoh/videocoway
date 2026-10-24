"""Potong VO penuh kepada baris (snap ke jeda terdekat dari anggaran ASR), rapatkan sela, lajukan.

    python tilam/vo/split.py v16
In : tilam/vo/<v>_full.wav, tilam/vo/<v>_asr.json, tilam/vo/lines_<v>.json
Out: tilam/vo/<v>_vo.wav (44.1k mono) + tilam/vo/<v>_timing.json  {id, scene, start, end} dalam masa video
"""
import json, pathlib, subprocess, sys, wave
import imageio_ffmpeg, numpy as np

D = pathlib.Path(__file__).parent; FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, TEMPO, GAP, LEAD = 44100, 1.12, 0.32, 0.25


def main(V):
    raw = subprocess.run([FF, "-v", "error", "-i", str(D / f"{V}_full.wav"), "-af", f"atempo={TEMPO}",
                          "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, "<i2").astype(float) / 32768
    hop = SR // 100
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop])
    quiet = rms < .006
    # jeda >= 0.18s -> calon sempadan (tengah jeda)
    gaps, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if j - i >= 18: gaps.append(((i + j) / 2 / 100, i / 100, j / 100))
            i = j
        else: i += 1
    asr = json.loads((D / f"{V}_asr.json").read_text())["lines"]
    lines = json.loads((D / f"lines_{V}.json").read_text())
    cuts = []
    for a, b in zip(asr, asr[1:]):
        want = (a["end"] + b["start"]) / 2 / TEMPO
        cuts.append(min(gaps, key=lambda g: abs(g[0] - want) - .8 * (g[2] - g[1])))   # utamakan jeda panjang (bukan koma)
    speech = np.nonzero(~quiet)[0]
    first, last = speech[0] / 100, speech[-1] / 100 + .05
    bounds = [(first, None)] + [(g[2] - .03, g[1] + .03) for g in cuts] + [(None, last)]
    segs = [(bounds[k][0], bounds[k + 1][1]) for k in range(len(lines))]
    out, t, timing = [np.zeros(int(LEAD * SR))], LEAD, []
    for ln, (s, e) in zip(lines, segs):
        seg = x[int(s * SR):int(e * SR)].copy()
        f = int(.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        timing.append(dict(id=ln["id"], scene=ln["scene"], start=round(t, 3), end=round(t + len(seg) / SR, 3), text=ln["text"]))
        out += [seg, np.zeros(int(GAP * SR))]; t += len(seg) / SR + GAP
    y = np.concatenate(out); y *= .89 / np.abs(y).max()
    with wave.open(str(D / f"{V}_vo.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype("<i2").tobytes())
    (D / f"{V}_timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1))
    for tm in timing: print(f'{tm["id"]} {tm["start"]:6.2f}-{tm["end"]:6.2f} ({tm["end"]-tm["start"]:.2f}s) {tm["text"][:50]}')
    print("jumlah", round(t, 2))


if __name__ == "__main__":
    main(sys.argv[1])
