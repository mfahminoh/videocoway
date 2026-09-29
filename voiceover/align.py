"""Align a single voiceover recording to the lines in lines_long.json (no ASR needed).

Finds pauses in the recording, then picks one pause per line boundary with dynamic
programming so that each segment's speech length matches the line's text length and
its internal pause count matches the line's punctuation.
Output: voiceover/vo_segments_long.json  [{id, a, b}]  (seconds in the recording)

    python voiceover/align.py [recording.wav] [lines.json] [out.json]
"""
import json, pathlib, re, sys, wave
import numpy as np

HERE = pathlib.Path(__file__).parent
src = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "source" / "gemini_tts_long.wav")
L = json.loads(pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else HERE / "lines_long.json").read_text())
OUT = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else HERE / "vo_segments_long.json")

w = wave.open(src); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
hop = int(sr * 0.01); n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
sil = db < db.max() - 40
voiced = np.where(~sil)[0]; T0, T1 = voiced[0] * .01, (voiced[-1] + 1) * .01
P = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        if (j - i) * .01 >= .18 and T0 < i * .01 and j * .01 < T1: P.append((i * .01, j * .01))
        i = j
    else: i += 1

def units(s): return len(re.sub(r"[^a-z0-9]", "", s.lower()))
def puncts(s): return len(re.findall(r"[,.!?]", s.strip()[:-1]))
U = np.array([units(l["text"]) for l in L], float)
K = len(L)
bounds = [T0] + [None] * 0
# speech time between two real times
def speech(a, b): return (b - a) - sum(max(0, min(b, q) - max(a, p)) for p, q in P)
total = speech(T0, T1); rate = total / U.sum()
# DP over pause indices: state (k boundaries used, last pause idx)
M = len(P); INF = 1e18
cost = np.full((K, M + 1), INF); back = np.zeros((K, M + 1), int)
def seg_cost(k, a, b, inner):
    exp = U[k] * rate; d = speech(a, b)
    return ((d - exp) / max(exp, 1.5)) ** 2 * 4 + 0.35 * abs(inner - puncts(L[k]["text"]))
starts = [T0] + [q for p, q in P]; ends = [p for p, q in P] + [T1]
# segment k spans from start s (index into starts) to end e (index into ends), e >= s
for e in range(M + 1):
    inner = e
    cost[0][e] = seg_cost(0, T0, ends[e], inner) - (0.6 * (P[e][1] - P[e][0]) if e < M else 0)
for k in range(1, K):
    for e in range(k, M + 1):
        best = INF; arg = -1
        for s in range(k - 1, e):
            if cost[k - 1][s] >= INF: continue
            c = cost[k - 1][s] + seg_cost(k, starts[s + 1], ends[e], e - s - 1) - (0.6 * (P[e][1] - P[e][0]) if e < M else 0)
            if c < best: best, arg = c, s
        cost[k][e] = best; back[k][e] = arg
e = M; segs = []
for k in range(K - 1, -1, -1):
    s = back[k][e] if k > 0 else -1
    a = T0 if k == 0 else starts[s + 1]
    segs.append({"id": L[k]["id"], "a": round(a, 2), "b": round(ends[e], 2)})
    e = s
segs.reverse()
OUT.write_text(json.dumps(segs, indent=1))
for sgm, l in zip(segs, L):
    slot = f", slot {l['end']-l['start']:5.2f}s" if "end" in l else ""
    print(f"{sgm['id']} {sgm['a']:6.2f}-{sgm['b']:6.2f} ({sgm['b']-sgm['a']:5.2f}s{slot})  {l['text'][:60]}")
