"""Transkrip audio dengan Gemini (semakan sebutan VO).  python scripts/stt.py fail.wav [fail2.wav ...]"""
import base64, json, sys, urllib.request

MODEL = "gemini-3.1-flash-lite"


def transcribe(path):
    data = base64.b64encode(open(path, "rb").read()).decode()
    body = {"contents": [{"parts": [
        {"inlineData": {"mimeType": "audio/mpeg" if path.endswith(".mp3") else "audio/wav", "data": data}},
        {"text": "Transkrip audio Bahasa Melayu ini perkataan demi perkataan. Tulis nombor sebagai perkataan seperti yang disebut. "
                 "Pulangkan teks transkrip sahaja, kemudian satu baris 'DURASI_ANGGARAN: <saat>'."}]}]}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent",
                                 json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["candidates"][0]["content"]["parts"][0]["text"].strip()


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, "->", transcribe(p))
