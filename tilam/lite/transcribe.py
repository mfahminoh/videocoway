"""Transkrip video rujukan (pertuturan + teks atas skrin) dengan Gemini.  python tilam/lite/transcribe.py r1 r2 ..."""
import base64, json, pathlib, sys, time, urllib.request
D = pathlib.Path(__file__).parent
MODELS = ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash", "gemini-flash-latest", "gemini-3.5-flash",
          "gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.1-flash-lite"]
PROMPT = """This is a Malaysian TikTok sales video about Coway mattresses (Malay/English mix). Output in Malay, as Markdown:
## Transkrip
Verbatim speech with timestamps, one line per sentence: `[mm:ss] text`. Keep the speaker's exact words (Malay slang, English words). Do not translate.
## Teks atas skrin
Every on-screen caption/sticker/graphic text with timestamp `[mm:ss] text`.
## Visual
Short timeline of what is shown (shots, demos, props, B-roll) with timestamps.
## Fakta & dakwaan
Bullet list of every product fact, spec, number, price, promo, gift, service or claim mentioned (spoken or on screen), noting the timestamp and which product (Prime Lite / Prime II / other).
Be exact; write [tak jelas] where unclear. Do not invent."""


def ask(path):
    data = base64.b64encode(path.read_bytes()).decode()
    body = json.dumps({"contents": [{"parts": [{"inlineData": {"mimeType": "video/mp4", "data": data}}, {"text": PROMPT}]}]}).encode()
    for a in range(4):
        for m in MODELS:
            try:
                r = urllib.request.urlopen(urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", body, {"Content-Type": "application/json"}), timeout=600)
                return m, json.load(r)["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e: print(path.name, m, e, file=sys.stderr)
        time.sleep(30)
    raise SystemExit("gagal: " + path.name)


for v in sys.argv[1:]:
    m, t = ask(D / "rujukan" / f"{v}.mp4")
    (D / "transkrip" / f"{v}.md").write_text(f"# {v} — transkrip (Gemini `{m}`)\n\n" + t + "\n")
    print(v, "ok", m)
