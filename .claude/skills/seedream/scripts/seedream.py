#!/usr/bin/env python3
"""Generate images with BytePlus Seedream (ModelArk API).

Usage:
  python3 seedream.py "a red coffee cup on a wooden table"
  python3 seedream.py "same cup, studio light" --ref product.png --size 1440x2560 -n 2 --out assets/generated

The API key comes from ARK_API_KEY, or from the `export ARK_API_KEY=...` line
that set-ark-key.sh writes to ~/.bash_profile. Prints one saved path per line.
"""
import argparse
import base64
import json
import mimetypes
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path

BASE_URL = os.environ.get("ARK_BASE_URL", "https://ark.ap-southeast.bytepluses.com/api/v3")
MODELS = {
    "4.5": "seedream-4-5-251128",
    "4.0": "seedream-4-0-250828",
}
DEFAULT_MODEL = os.environ.get("ARK_IMAGE_MODEL", "4.5")
PROFILES = ["~/.bash_profile", "~/.bashrc", "~/.zshrc", "~/.zprofile"]


def load_key() -> str:
    key = os.environ.get("ARK_API_KEY")
    if key:
        return key
    for profile in PROFILES:
        path = Path(profile).expanduser()
        if not path.exists():
            continue
        for line in path.read_text(errors="ignore").splitlines():
            if line.startswith("export ARK_API_KEY="):
                value = shlex.split(line[len("export ARK_API_KEY="):])
                if value:
                    return value[0]
    setup = Path(__file__).with_name("set-ark-key.sh")
    sys.exit(f"ARK_API_KEY not found. Run: bash {setup}")


def to_image_ref(ref: str) -> str:
    """URLs pass through; local files become data URLs."""
    if ref.startswith(("http://", "https://", "data:")):
        return ref
    path = Path(ref).expanduser()
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "image"


def generate(key, prompt, model, size, refs, count):
    body = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "b64_json",
        "watermark": False,
    }
    if refs:
        body["image"] = refs[0] if len(refs) == 1 else refs
    if count > 1:
        body["sequential_image_generation"] = "auto"
        body["sequential_image_generation_options"] = {"max_images": count}

    # curl uses the macOS Keychain for TLS, which python.org Python does not.
    # The auth header goes in on stdin so the key never shows up in `ps`.
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(body, f)
        body_path = f.name
    try:
        proc = subprocess.run(
            ["curl", "-sS", "--max-time", "300", "-w", "\n%{http_code}",
             "-H", "Content-Type: application/json", "-H", "@-",
             "--data-binary", f"@{body_path}", f"{BASE_URL}/images/generations"],
            input=f"Authorization: Bearer {key}\n",
            capture_output=True, text=True,
        )
    finally:
        os.unlink(body_path)
    if proc.returncode != 0:
        sys.exit(f"curl failed: {proc.stderr.strip()}")
    payload, _, status = proc.stdout.rpartition("\n")
    if status != "200":
        sys.exit(f"API error {status}: {payload}")
    return json.loads(payload)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("prompt")
    p.add_argument("--model", default=DEFAULT_MODEL, help="4.5 (default), 4.0, or a full model/endpoint id")
    p.add_argument("--size", default="2K", help="1K, 2K, 4K or WIDTHxHEIGHT, e.g. 1440x2560")
    p.add_argument("--ref", action="append", default=[], help="reference image (file or URL), repeatable")
    p.add_argument("-n", type=int, default=1, help="number of images (uses sequential generation)")
    p.add_argument("--out", default="generated", help="output folder (default: ./generated)")
    args = p.parse_args()

    key = load_key()
    model = MODELS.get(args.model, args.model)
    result = generate(key, args.prompt, model, args.size, [to_image_ref(r) for r in args.ref], args.n)

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for i, item in enumerate(result.get("data", []), 1):
        if "b64_json" not in item:
            print(f"skipped image {i}: {item.get('error', item)}", file=sys.stderr)
            continue
        out = out_dir / f"{stamp}-{slug(args.prompt)}-{i}.jpg"
        out.write_bytes(base64.b64decode(item["b64_json"]))
        print(out.resolve())

    usage = result.get("usage")
    if usage:
        print(f"model: {model}  usage: {json.dumps(usage)}", file=sys.stderr)


if __name__ == "__main__":
    main()
