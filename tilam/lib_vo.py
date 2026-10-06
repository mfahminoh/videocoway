"""VO untuk siri video tilam: satu permintaan Gemini TTS -> potong ikut baris -> masa setiap baris.

Penjajaran: calon sempadan = jeda dalam audio; pilih N-1 jeda dengan DP. Setiap baris dijangka panjangnya
seimbang dengan bilangan hurufnya, dan jeda panjang (antara perenggan) lebih diutamakan daripada jeda koma.
"""
import json, pathlib, subprocess, sys, wave
import imageio_ffmpeg, numpy as np

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE / "vo"))
import gemini_tts  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, TEMPO, GAP, LEAD = 44100, 1.12, 0.32, 0.25


def tts_full(lines, path):
    text = "\n\n".join(l["text"] for l in lines)
    for m in gemini_tts.MODELS:
        try:
            pcm = gemini_tts.tts(text, m); break
        except Exception as e:
            print("TTS", m, "gagal:", e)
    else:
        raise SystemExit("TTS gagal untuk semua model")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
    print("TTS ok", m, f"{len(pcm) / 48000:.1f}s")


def load(path, tempo=None):
    af = ["-af", f"atempo={tempo}"] if tempo else []
    raw = subprocess.run([FF, "-v", "error", "-i", str(path), *af, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, "<i2").astype(float) / 32768


def align(x, lines):
    hop = SR // 100
    rms = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), "same")[::hop])
    quiet = rms < .006
    sp = np.nonzero(~quiet)[0]; s0, s1 = sp[0] / 100, sp[-1] / 100 + .05
    gaps, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]: j += 1
            if j - i >= 12 and s0 < i / 100 and j / 100 < s1: gaps.append((i / 100, j / 100))
            i = j
        else: i += 1
    ch = [len(l["text"]) for l in lines]; N = len(lines)
    rate = (s1 - s0) / sum(ch)
    INF = 1e18
    # dp[k][g]: kos terbaik jika sempadan ke-k (antara baris k dan k+1) ialah jeda g
    dp = [[INF] * len(gaps) for _ in range(N - 1)]; bk = [[-1] * len(gaps) for _ in range(N - 1)]

    def cost(prev_end, g, k):
        exp = ch[k] * rate; got = gaps[g][0] - prev_end
        return abs(got - exp) / exp * 2 - (gaps[g][1] - gaps[g][0]) * 3

    for g in range(len(gaps)):
        dp[0][g] = cost(s0, g, 0)
    for k in range(1, N - 1):
        for g in range(len(gaps)):
            for h in range(g):
                if dp[k - 1][h] == INF: continue
                c = dp[k - 1][h] + cost(gaps[h][1], g, k)
                if c < dp[k][g]: dp[k][g], bk[k][g] = c, h
    best, bg = INF, -1
    for g in range(len(gaps)):
        if dp[N - 2][g] == INF: continue
        exp = ch[N - 1] * rate
        c = dp[N - 2][g] + abs((s1 - gaps[g][1]) - exp) / exp * 2
        if c < best: best, bg = c, g
    sel = [bg]
    for k in range(N - 2, 0, -1): sel.append(bk[k][sel[-1]])
    sel = sel[::-1]
    segs, st = [], s0
    for g in sel:
        segs.append((st, gaps[g][0] + .03)); st = gaps[g][1] - .03
    segs.append((st, s1))
    for l, (a, b), c in zip(lines, segs, ch):
        r = (b - a) / (c * rate)
        flag = "  <-- semak" if r < .7 or r > 1.4 else ""
        print(f'  {l["id"]} {b - a:5.2f}s (x{r:.2f}){flag} {l["text"][:48]}')
    return segs


def build_vo(vid, lines, vodir):
    vodir.mkdir(parents=True, exist_ok=True)
    full = vodir / f"{vid}_full.wav"
    if not full.exists():
        tts_full(lines, full)
    x = load(full, TEMPO)
    segs = align(x, lines)
    out, t, tm = [np.zeros(int(LEAD * SR))], LEAD, []
    for l, (a, b) in zip(lines, segs):
        seg = x[int(a * SR):int(b * SR)].copy()
        f = int(.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        tm.append(dict(id=l["id"], start=round(t, 3), end=round(t + len(seg) / SR, 3), text=l["text"]))
        out += [seg, np.zeros(int(GAP * SR))]; t += len(seg) / SR + GAP
    y = np.concatenate(out); y *= .89 / np.abs(y).max()
    with wave.open(str(vodir / f"{vid}_vo.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((y * 32767).astype("<i2").tobytes())
    (vodir / f"{vid}_timing.json").write_text(json.dumps(tm, ensure_ascii=False, indent=1))
    return tm
