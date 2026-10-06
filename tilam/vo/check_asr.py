"""Semak potongan VO: transkrip setiap baris (Gemini) dan banding dengan skrip.  python tilam/vo/check_asr.py b1"""
import base64, json, pathlib, subprocess, sys, time, urllib.request
import imageio_ffmpeg
V = sys.argv[1]; D = pathlib.Path(__file__).resolve().parent.parent / "b/vo"; FF = imageio_ffmpeg.get_ffmpeg_exe()
tm = json.loads((D / f"{V}_timing.json").read_text())
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else [x["id"] for x in tm]


def ask(parts):
    body = json.dumps({"contents": [{"parts": parts}]}).encode()
    for a in range(6):
        for m in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-flash-latest", "gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite"]:
            try:
                r = urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", body, {"Content-Type": "application/json"}), timeout=200)
                return json.load(r)["candidates"][0]["content"]["parts"][0]["text"].strip()
            except Exception as e: print(m, e, file=sys.stderr)
        time.sleep(10)
    return "?"


for x in tm:
    if x["id"] not in ONLY: continue
    mp3 = subprocess.run([FF, "-v", "error", "-ss", str(x["start"]), "-to", str(x["end"]), "-i", str(D / f"{V}_vo.wav"), "-f", "mp3", "-b:a", "48k", "-"], capture_output=True, check=True).stdout
    got = ask([{"inlineData": {"mimeType": "audio/mp3", "data": base64.b64encode(mp3).decode()}}, {"text": "Transcribe this Malay audio verbatim. Output only the transcript."}])
    ok = "OK " if got.lower()[:12].replace(",", "") == x["text"].lower()[:12].replace(",", "") else "?? "
    print(ok + x["id"], "SKRIP:", x["text"], "\n      DENGAR:", got)
sys.exit(0)
parts = []
parts.append({"text": "Transcribe each clip verbatim in Malay. Reply JSON list of {id, text}."})
body = json.dumps({"contents": [{"parts": parts}], "generationConfig": {"responseMimeType": "application/json"}}).encode()
for a in range(8):
    for m in ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash"]:
        try:
            r = urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", body, {"Content-Type": "application/json"}), timeout=200)
            got = json.loads(json.load(r)["candidates"][0]["content"]["parts"][0]["text"])
            for x, g in zip(tm, got): print(x["id"], "SKRIP:", x["text"], "\n   DENGAR:", g.get("text"))
            sys.exit(0)
        except Exception as e: print(m, e, file=sys.stderr)
    time.sleep(15)
sys.exit("ASR tidak tersedia")
