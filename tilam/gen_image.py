"""Jana gambar babak masalah/hook (sebelum produk diperkenalkan) dengan Gemini image.

    python tilam/gen_image.py nama "prompt ..." [--ar 9:16] [--model gemini-3.1-flash-image]
-> assets/tilam/jana/<nama>.png
"""
import argparse, base64, json, pathlib, sys, urllib.request

R = pathlib.Path(__file__).resolve().parent.parent
OUT = R / "assets/tilam/jana"
STYLE = ("Photorealistic, natural light, shot on a phone camera, candid lifestyle photo of a Malaysian home. "
         "No text, no logos, no brand names, no watermark. ")


def gen(name, prompt, ar="9:16", model="gemini-3.1-flash-image"):
    body = {"contents": [{"parts": [{"text": STYLE + prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": ar}}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    for p in d["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            OUT.mkdir(parents=True, exist_ok=True)
            f = OUT / f"{name}.png"; f.write_bytes(base64.b64decode(p["inlineData"]["data"]))
            (OUT / f"{name}.txt").write_text(f"{model} | {ar}\n{prompt}\n")
            print("siap:", f); return f
    sys.exit("tiada gambar: " + json.dumps(d)[:500])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("name"); ap.add_argument("prompt")
    ap.add_argument("--ar", default="9:16"); ap.add_argument("--model", default="gemini-3.1-flash-image")
    a = ap.parse_args(); gen(a.name, a.prompt, a.ar, a.model)
