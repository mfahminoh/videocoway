"""Jana satu klip video Seedance (BytePlus ModelArk) -> MP4 1080x1920 30fps tanpa audio, sedia untuk latar `scenes`.

    python3 .claude/skills/coway-video/scripts/seedance.py "<prompt>" --out assets/clips/tilam-p2-01_s01.mp4
    python3 .claude/skills/coway-video/scripts/seedance.py "<prompt>" --image assets/img/neon/pink.jpg --out ...   # imej -> video
    python3 .claude/skills/coway-video/scripts/seedance.py --check                                               # model mana aktif

Kunci: ARK_API_KEY (sama seperti skill seedream). Model mesti diaktifkan dalam Ark Console
(ralat "ModelNotOpen" = belum aktif). Kos dikenakan bagi setiap klip yang berjaya, jadi jangan ulang tanpa sebab.
Parameter Seedance 1.x dihantar sebagai bendera dalam teks prompt (--ratio, --duration, --resolution);
untuk model dreamina-seedance-2.x skrip menghantarnya sebagai medan badan. Belum diuji dengan jana sebenar
(model belum aktif pada 25 Okt 2026); semak hasil pertama dengan teliti.
"""
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("ARK_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api/v3")
MODELS = {"pro-fast": "seedance-1-0-pro-fast-251015", "pro": "seedance-1-0-pro-250528",
          "2.0-fast": "dreamina-seedance-2-0-fast-260128", "2.0": "dreamina-seedance-2-0-260128",
          "2.5": "dreamina-seedance-2-5-260628"}


def key():
    k = os.environ.get("ARK_API_KEY")
    if not k:
        prof = pathlib.Path.home() / ".bash_profile"
        for line in prof.read_text().splitlines() if prof.exists() else []:
            if line.startswith("export ARK_API_KEY="):
                k = shlex.split(line[len("export ARK_API_KEY="):])[0]
    if not k:
        sys.exit("ARK_API_KEY tiada. Jalankan: bash .claude/skills/seedream/scripts/set-ark-key.sh")
    return k


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        err = e.read().decode(errors="ignore")
        if "ModelNotOpen" in err:
            sys.exit(f"Model belum diaktifkan. Aktifkan di Ark Console (console.byteplus.com/ark → Model activation).\n{err[:300]}")
        sys.exit(f"HTTP {e.code}: {err[:500]}")


def image_ref(src):
    if src.startswith(("http://", "https://", "data:")):
        return src
    p = pathlib.Path(src)
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def check():
    d = call("GET", "/models")
    for m in d.get("data", []):
        if "seedance" in m.get("id", ""):
            print(m["id"], m.get("status", ""), m.get("task_type", ""))
    print("Nota: senarai ini tunjuk model yang wujud; 'ModelNotOpen' semasa jana bermakna belum diaktifkan untuk akaun.")


def normalize(src, dst):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-y", "-i", str(src), "-an",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--image", help="imej bingkai pertama (fail atau URL) — guna gambar produk rasmi supaya bentuk unit tepat")
    ap.add_argument("--model", default="pro-fast", help=f"{', '.join(MODELS)} atau id penuh")
    ap.add_argument("--duration", type=int, default=5)
    ap.add_argument("--resolution", default="1080p")
    ap.add_argument("--ratio", default="9:16")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.check:
        return check()
    if not a.prompt or not a.out:
        ap.error("prompt dan --out diperlukan")
    model = MODELS.get(a.model, a.model)
    params = {"ratio": a.ratio, "duration": a.duration, "resolution": a.resolution, "watermark": False}
    if a.seed is not None:
        params["seed"] = a.seed
    text = a.prompt
    body = {"model": model, "content": []}
    if model.startswith("dreamina-"):
        body.update(params)
    else:
        text += " " + " ".join(f"--{k} {str(v).lower()}" for k, v in params.items())
    body["content"].append({"type": "text", "text": text})
    if a.image:
        body["content"].append({"type": "image_url", "image_url": {"url": image_ref(a.image)}, "role": "first_frame"})

    task = call("POST", "/contents/generations/tasks", body)["id"]
    print("tugas:", task, model, flush=True)
    t0 = time.time()
    while True:
        r = call("GET", f"/contents/generations/tasks/{task}")
        st = r.get("status")
        if st == "succeeded":
            break
        if st in ("failed", "cancelled", "expired"):
            sys.exit(f"gagal: {json.dumps(r.get('error', r))[:500]}")
        if time.time() - t0 > 900:
            sys.exit(f"masih {st} selepas 15 minit; semak tugas {task} kemudian")
        time.sleep(10)
    url = r["content"]["video_url"]
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".raw.mp4")
    urllib.request.urlretrieve(url, raw)
    normalize(raw, out)
    raw.unlink()
    print(out, "usage:", json.dumps(r.get("usage", {})))


if __name__ == "__main__":
    main()
