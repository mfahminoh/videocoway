"""Buat _contact-sheet.jpg dalam setiap folder produk (thumbnail + nama fail) untuk pilih gambar cepat."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent / "coway" / "Other Brand Assets"
FONT = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "Poppins-Regular.ttf"
TW, TH, COLS, LABEL = 300, 240, 6, 34


def sheet(folder):
    files = sorted(p for p in folder.iterdir()
                   if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and not p.name.startswith("_"))
    if not files:
        return
    rows = (len(files) + COLS - 1) // COLS
    img = Image.new("RGB", (COLS * TW, rows * (TH + LABEL)), "white")
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(FONT), 11)
    for i, p in enumerate(files):
        x, y = (i % COLS) * TW, (i // COLS) * (TH + LABEL)
        try:
            im = Image.open(p)
            im.thumbnail((TW - 10, TH - 10))
            bg = Image.new("RGB", im.size, (225, 228, 232))  # kelabu supaya PNG lutsinar putih nampak
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[3])
            img.paste(bg, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        except Exception:  # noqa: BLE001
            d.text((x + 10, y + 10), "rosak", fill="red", font=font)
        name = p.name if len(p.name) <= 46 else p.name[:43] + "..."
        d.text((x + 6, y + TH + 4), name, fill=(40, 40, 40), font=font)
    img.save(folder / "_contact-sheet.jpg", quality=70)


for f in sorted(ROOT.glob("*/*")):
    if f.is_dir():
        sheet(f)
sheet(ROOT / "_brand")
print("siap")
