"""Transcribe a voiceover chunk by chunk (split at pauses) with Gemini, to check/fix line alignment.
    python3 voiceover/transcribe_chunks.py videos/PA05/vo.wav 0 99 0.35 > videos/PA05/chunks.txt
Then: python3 voiceover/align_chunks.py videos/PA05/vo.wav videos/PA05/lines.json videos/PA05/chunks.txt videos/PA05/segments.json
"""
import base64, json, sys, urllib.request, subprocess, wave, time, numpy as np, imageio_ffmpeg
f, lo, hi = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); minp = float(sys.argv[4]) if len(sys.argv) > 4 else .4
w = wave.open(f); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), "<i2")
hop = sr // 100; n = len(x) // hop
db = 20 * np.log10(np.sqrt(((x[:n*hop].astype(float) / 32768).reshape(n, hop) ** 2).mean(1)) + 1e-9)
sil = db < db.max() - 40
pauses = []; i = 0
while i < n:
    if sil[i]:
        j = i
        while j < n and sil[j]: j += 1
        if (j - i) / 100 >= minp: pauses.append((i / 100, j / 100))
        i = j
    else: i += 1
voiced = np.where(~sil)[0]; end = voiced[-1] / 100 + .05
cuts = [lo] + [(a + b) / 2 for a, b in pauses if lo < (a + b) / 2 < min(hi, end)] + [min(hi, end)]
parts = []
for k in range(len(cuts) - 1):
    seg = x[int(cuts[k] * sr): int(cuts[k + 1] * sr)]
    mp3 = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1", "-i", "-", "-b:a", "48k", "-f", "mp3", "-"], input=seg.tobytes(), capture_output=True).stdout
    parts += [{"text": f"Clip {k + 1}:"}, {"inlineData": {"mimeType": "audio/mp3", "data": base64.b64encode(mp3).decode()}}]
parts.append({"text": f"Transcribe each of the {len(cuts) - 1} Malay audio clips above verbatim. Output one line per clip as 'Clip N: <text>'."})
body = json.dumps({"contents": [{"parts": parts}]}).encode()
for i in range(25):
    m = ["gemini-3.6-flash", "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash"][i % 4]
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", data=body, headers={"Content-Type": "application/json"}), timeout=180))
        txt = d["candidates"][0]["content"]["parts"][0]["text"]; break
    except Exception as e:
        print(m, e, file=sys.stderr); time.sleep(6 + i)
for k, line in enumerate([l for l in txt.splitlines() if l.strip().startswith("Clip")]):
    print(f"{cuts[k]:6.2f}-{cuts[k+1]:6.2f}  {line}")
