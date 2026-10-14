"""Generate the story stills for the peti ais videos (PA01-PA05) with the seedream skill.

    python3 videos/peti_ais_images.py              # only images that don't exist yet
    python3 videos/peti_ais_images.py pa03_c       # (re)generate given ones

Prompts: assets/img/peti_ais/prompts.json. Images with "ref" are generated from that image
(same people / kitchen), so the base image of each video is made first.
"""
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).parent.parent
DIR = ROOT / "assets" / "img" / "peti_ais"
SKILL = ROOT / ".claude" / "skills" / "seedream" / "scripts" / "seedream.py"


def gen(im, style):
    tmp = DIR / "_tmp" / im["file"].split(".")[0]
    cmd = [sys.executable, str(SKILL), f"{style} {im['prompt']}", "--size", "1440x2560", "--out", str(tmp)]
    if im.get("ref"):
        cmd += ["--ref", str(DIR / im["ref"])]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = [l for l in r.stdout.splitlines() if l.endswith(".jpg")]
    if not out:
        print(im["file"], "GAGAL:", r.stderr.strip()[:300], flush=True)
        return
    pathlib.Path(out[0]).replace(DIR / im["file"])
    for f in tmp.glob("*"):
        f.unlink()
    tmp.rmdir()
    print("ok", im["file"], flush=True)


def main():
    d = json.loads((DIR / "prompts.json").read_text())
    want = set(sys.argv[1:])
    todo = [im for im in d["images"] if (im["file"].split(".")[0] in want) or (not want and not (DIR / im["file"]).exists())]
    for base in (False, True):          # imej asas dahulu, kemudian yang guna rujukan
        batch = [im for im in todo if bool(im.get("ref")) == base]
        with ThreadPoolExecutor(6) as ex:
            list(ex.map(lambda im: gen(im, d["style"]), batch))
    (DIR / "_tmp").exists() and not any((DIR / "_tmp").iterdir()) and (DIR / "_tmp").rmdir()


if __name__ == "__main__":
    main()
