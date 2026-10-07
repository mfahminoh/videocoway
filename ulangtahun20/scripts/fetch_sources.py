"""Muat turun klip dari Google Drive ke sources/ ikut data/clips.csv (langkau jangan_guna)."""
import csv, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
SRC.mkdir(exist_ok=True)
URL = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"

fail = []
for row in csv.DictReader(open(ROOT / "data/clips.csv", encoding="utf-8")):
    if row["tag"] == "jangan_guna":
        continue
    dst = SRC / row["file"]
    if dst.exists() and dst.stat().st_size > 100_000:
        continue
    r = subprocess.run(["curl", "-sL", "--retry", "3", "-o", str(dst), URL.format(row["drive_id"])])
    head = dst.read_bytes()[:12] if dst.exists() else b""
    ok = r.returncode == 0 and b"ftyp" in head
    print(("OK  " if ok else "GAGAL ") + row["file"], flush=True)
    if not ok:
        fail.append(row["file"])
        dst.unlink(missing_ok=True)
sys.exit(1 if fail else 0)
