"""Langkah 1: ffprobe setiap klip + contact sheet 4 frame (10/35/60/85%) ke out/scan/."""
import csv, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/scan"
OUT.mkdir(parents=True, exist_ok=True)

rows = []
for i, row in enumerate(csv.DictReader(open(ROOT / "data/clips.csv", encoding="utf-8")), 1):
    if row["tag"] == "jangan_guna":
        continue
    f = ROOT / "sources" / row["file"]
    p = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
         "-of", "json", str(f)], capture_output=True, text=True).stdout)
    v = next(s for s in p["streams"] if s["codec_type"] == "video")
    dur = float(p["format"]["duration"])
    has_audio = any(s["codec_type"] == "audio" for s in p["streams"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    cid = f"C{i:02d}"
    # 4 frame sampel, disusun mendatar, label masa
    sel = "+".join(f"eq(n\\,{int(dur * k * num / den)})" for k in (0.10, 0.35, 0.60, 0.85))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf",
                    f"select='{sel}',scale=-2:480,tile=4x1:padding=6", "-frames:v", "1", "-vsync", "0",
                    str(OUT / f"{cid}.jpg")], check=True)
    rows.append(dict(id=cid, tag=row["tag"], file=row["file"], w=v["width"], h=v["height"],
                     fps=round(num / den, 2), dur=round(dur, 2), audio=has_audio))

with open(OUT / "probe.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
for r in rows:
    print(r["id"], r["tag"], f'{r["w"]}x{r["h"]}', r["fps"], r["dur"], "A" if r["audio"] else "-", r["file"][:55])
