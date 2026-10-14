"""Map script lines to transcribed audio chunks (from chunks.py) -> segments.json.
    python3 align_chunks.py vo.wav lines.json chunks.txt out.json
Contiguous chunks per line, chosen by DP maximising text similarity; a/b = voiced edges."""
import json, re, sys, wave, difflib, numpy as np
wav, lines_p, chunks_p, out_p = sys.argv[1:5]
L = json.load(open(lines_p))
C = []
for ln in open(chunks_p):
    m = re.match(r"\s*([\d.]+)-\s*([\d.]+)\s+Clip \d+:\s*(.*)", ln)
    if m: C.append((float(m[1]), float(m[2]), m[3]))
def norm(s):
    s = s.lower().replace("*", "")
    s = re.sub(r"rm\s?(\d+)", r"\1 ringgit", s)
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()
K, M = len(L), len(C)
ref = [(norm(l["text"]), norm(l["cap"] or l["text"])) for l in L]
INF = -1e9
best = np.full((K + 1, M + 1), INF); back = np.zeros((K + 1, M + 1), int); best[0][0] = 0
for k in range(1, K + 1):
    for j in range(k, M + 1):
        for i in range(k - 1, j):
            if best[k - 1][i] <= INF: continue
            words = sum((norm(c[2]) for c in C[i:j]), [])
            v = best[k - 1][i] + max(sim(r, words) * max(len(r), 1) for r in ref[k - 1])
            if v > best[k][j]: best[k][j], back[k][j] = v, i
j = M; spans = []
for k in range(K, 0, -1):
    i = back[k][j]; spans.append((i, j)); j = i
spans.reverse()
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); voiced = db >= db.max() - 40
def edge(t0, t1, first):
    r = range(int(t0 * 100), min(n, int(t1 * 100)))
    idx = [q for q in r if voiced[q]]
    return (idx[0] if first else idx[-1] + 1) / 100 if idx else t0
segs = []
for (i, j), l in zip(spans, L):
    a, b = edge(C[i][0], C[j - 1][1], True), edge(C[i][0], C[j - 1][1], False)
    segs.append({"id": l["id"], "a": round(a, 2), "b": round(b, 2)})
    print(f"{l['id']} {a:6.2f}-{b:6.2f}  {' | '.join(c[2] for c in C[i:j])[:90]}")
json.dump(segs, open(out_p, "w"), indent=1)
