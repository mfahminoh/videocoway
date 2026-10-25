"""Jajarkan baris VO kepada jeda dalam vo.wav tanpa transkripsi (bila Gemini 429/503 untuk audio).

    python3 .claude/skills/coway-remake/scripts/jajar_jeda.py videos/<ID>              # cetak, tak tulis
    python3 .claude/skills/coway-remake/scripts/jajar_jeda.py videos/<ID> --tulis      # tulis segments.json

Anggaran hujung setiap baris = kadar suku kata (vokal) sepanjang suara; sempadan dipilih (DP) daripada jeda >= --min s
yang paling hampir dengan anggaran, dengan keutamaan pada jeda yang lebih panjang. Selepas ini guna --no-align.
Semak hasil: setiap baris mesti ada tempoh munasabah (±2.5 perkataan/saat); senaraikan baris ragu untuk user dengar.
"""
import argparse
import json
import pathlib
import wave

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--min", type=float, default=.08, help="jeda minimum (s)")
    ap.add_argument("--db", type=float, default=36, help="senyap = bawah puncak - db")
    ap.add_argument("--tulis", action="store_true")
    a = ap.parse_args()
    d = pathlib.Path(a.folder)
    w = wave.open(str(d / "vo.wav"))
    sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float) / 32768
    hop = sr // 100
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    sil = db < db.max() - a.db
    P, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]:
                j += 1
            if (j - i) / 100 >= a.min:
                P.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    voiced = np.where(~sil)[0]
    t0, t1 = voiced[0] / 100, voiced[-1] / 100
    P = [(p, q) for p, q in P if t0 < p and q < t1]
    L = json.loads((d / "lines.json").read_text())
    syl = [sum(c in "aeiouAEIOU" for c in l["text"]) for l in L]
    cum = np.cumsum(syl) / sum(syl)
    exp = [t0 + (t1 - t0) * c for c in cum[:-1]]
    K, M = len(exp), len(P)
    assert M >= K, f"jeda tak cukup ({M} < {K}); kurangkan --min atau --db"
    mids = [((p + q) / 2, q - p) for p, q in P]
    cost = lambda k, m: (mids[m][0] - exp[k]) ** 2 - 2.0 * mids[m][1]
    INF = 1e18
    dp = np.full((K, M), INF)
    bk = np.zeros((K, M), int)
    for m in range(M):
        dp[0][m] = cost(0, m)
    for k in range(1, K):
        best, arg = INF, -1
        for m in range(M):
            if m > 0 and dp[k - 1][m - 1] < best:
                best, arg = dp[k - 1][m - 1], m - 1
            if arg >= 0:
                dp[k][m], bk[k][m] = best + cost(k, m), arg
    m = int(np.argmin(dp[K - 1]))
    cuts = [m]
    for k in range(K - 1, 0, -1):
        m = bk[k][m]
        cuts.append(m)
    cuts = cuts[::-1]
    segs, start = [], t0
    for k, l in enumerate(L):
        end = P[cuts[k]][0] if k < K else t1 + .05
        segs.append({"id": l["id"], "a": round(start, 2), "b": round(end, 2)})
        if k < K:
            start = P[cuts[k]][1]
    for s, l in zip(segs, L):
        wps = len(l["text"].split()) / max(.1, s["b"] - s["a"])
        flag = "  <- ragu" if not 1.6 <= wps <= 4.2 else ""
        print(f"{s['id']} {s['a']:6.2f}-{s['b']:6.2f} ({s['b'] - s['a']:4.2f}s, {wps:3.1f} p/s) {l['text'][:55]}{flag}")
    if a.tulis:
        (d / "segments.json").write_text(json.dumps(segs, indent=1))
        print("ditulis:", d / "segments.json", "(guna --no-align selepas ini)")


if __name__ == "__main__":
    main()
