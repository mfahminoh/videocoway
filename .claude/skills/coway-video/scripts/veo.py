"""Jana satu klip Veo (model video Google Flow) melalui Gemini API -> MP4 1080x1920 30fps tanpa audio.

    python3 .claude/skills/coway-video/scripts/veo.py --check                 # model Veo mana ada untuk key ini
    python3 .claude/skills/coway-video/scripts/veo.py "<prompt>" --out assets/clips/tilam-p2-01_s01.mp4 [--image ...]

Kunci: GEMINI_API_KEY jika ditetapkan (projek Google AI Studio berbayar dengan akses Veo); jika tidak, proxy
persekitaran menyuntik key (pada 25 Okt 2026 key proxy TIADA model Veo, jadi --check akan gagal).
Tanpa akses API, guna laluan Google Flow manual (formats/google-flow.md). Belum diuji dengan jana sebenar.
"""
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta"
HEAD = {"Content-Type": "application/json", **({"x-goog-api-key": os.environ["GEMINI_API_KEY"]} if os.environ.get("GEMINI_API_KEY") else {})}


def call(method, url, body=None):
    req = urllib.request.Request(url if url.startswith("http") else f"{BASE}/{url}", method=method,
                                 data=json.dumps(body).encode() if body else None, headers=HEAD)
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='ignore')[:500]}")


def veo_models():
    d = call("GET", "models?pageSize=200")
    return [m["name"].split("/", 1)[1] for m in d.get("models", [])
            if "veo" in m["name"] and "predictLongRunning" in m.get("supportedGenerationMethods", [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--image", help="imej bingkai pertama (gambar produk rasmi)")
    ap.add_argument("--model", help="lalai: model Veo pertama yang ada")
    ap.add_argument("--duration", type=int, default=8)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    models = veo_models()
    if a.check or not models:
        print("\n".join(models) or "Tiada model Veo untuk key ini. Tetapkan GEMINI_API_KEY (AI Studio berbayar) atau guna Google Flow manual.")
        return
    if not a.prompt or not a.out:
        ap.error("prompt dan --out diperlukan")
    model = a.model or models[0]
    inst = {"prompt": a.prompt}
    if a.image:
        p = pathlib.Path(a.image)
        inst["image"] = {"bytesBase64Encoded": base64.b64encode(p.read_bytes()).decode(),
                         "mimeType": mimetypes.guess_type(p.name)[0] or "image/jpeg"}
    op = call("POST", f"models/{model}:predictLongRunning",
              {"instances": [inst], "parameters": {"aspectRatio": "9:16", "durationSeconds": a.duration}})["name"]
    print("operasi:", op, model, flush=True)
    t0 = time.time()
    while not (r := call("GET", op)).get("done"):
        if time.time() - t0 > 900:
            sys.exit(f"belum siap selepas 15 minit: {op}")
        time.sleep(10)
    if "error" in r:
        sys.exit(f"gagal: {json.dumps(r['error'])[:500]}")
    uri = r["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".raw.mp4")
    with urllib.request.urlopen(urllib.request.Request(uri, headers=HEAD), timeout=300) as f:
        raw.write_bytes(f.read())
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-y", "-i", str(raw), "-an",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)
    raw.unlink()
    print(out)


if __name__ == "__main__":
    main()
