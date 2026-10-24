"""Gabung out/scan/Cxx.jpg jadi helaian 6 klip berlabel (untuk semakan visual)."""
import csv, pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCAN = ROOT / "out/scan"
rows = list(csv.DictReader(open(SCAN / "probe.csv", encoding="utf-8")))
font = ImageFont.truetype(str(ROOT.parent / "assets/fonts/Poppins-Bold.ttf"), 22)
RH, W = 330, 1400
for g in range(0, len(rows), 6):
    grp = rows[g:g + 6]
    sheet = Image.new("RGB", (W, RH * len(grp)), "white")
    d = ImageDraw.Draw(sheet)
    for i, r in enumerate(grp):
        im = Image.open(SCAN / f"{r['id']}.jpg")
        im.thumbnail((W, RH - 34))
        sheet.paste(im, (0, i * RH + 34))
        d.text((6, i * RH + 4), f"{r['id']}  [{r['tag']}]  {r['w']}x{r['h']}  {r['dur']}s  {r['file'][:60]}", fill="black", font=font)
    sheet.save(SCAN / f"sheet_{g // 6 + 1:02d}.jpg", quality=85)
print("ok")
