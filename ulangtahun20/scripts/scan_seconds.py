"""Jalur frame 1 saat untuk klip terpilih -> out/scan/sec_XX.jpg (3 klip sehelai, berlabel masa)."""
import csv, pathlib, subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out/scan"
ids = sys.argv[1].split(",")
rows = {r["id"]: r for r in csv.DictReader(open(OUT / "probe.csv", encoding="utf-8"))}
font = ImageFont.truetype(str(ROOT.parent / "assets/fonts/Poppins-Bold.ttf"), 18)
TH = 230
def frame(f, t, land):
    vf = "scale=-2:%d" % TH
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(f), "-frames:v", "1", "-vf", vf, "-f", "image2", "-c:v", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(raw))
strips = []
for cid in ids:
    r = rows[cid]; f = ROOT / "sources" / r["file"]; dur = float(r["dur"])
    ims = [(t, frame(f, t + 0.5, int(r["w"]) > int(r["h"]))) for t in range(int(dur))]
    w = sum(im.width + 3 for _, im in ims)
    s = Image.new("RGB", (w, TH + 28), "white"); d = ImageDraw.Draw(s); x = 0
    d.text((4, 2), f"{cid} [{r['tag']}] {r['file'][:50]}", fill="black", font=font)
    for t, im in ims:
        s.paste(im, (x, 28)); d.rectangle([x, 28, x + 30, 50], fill="black"); d.text((x + 3, 29), f"{t}", fill="yellow", font=font); x += im.width + 3
    strips.append(s)
for g in range(0, len(strips), 3):
    grp = strips[g:g + 3]; W = max(s.width for s in grp)
    sheet = Image.new("RGB", (W, sum(s.height + 8 for s in grp)), "white"); y = 0
    for s in grp: sheet.paste(s, (0, y)); y += s.height + 8
    if W > 2000: sheet = sheet.resize((2000, int(sheet.height * 2000 / W)))
    sheet.save(OUT / f"sec_{ids[g]}.jpg", quality=85); print(OUT / f"sec_{ids[g]}.jpg")
