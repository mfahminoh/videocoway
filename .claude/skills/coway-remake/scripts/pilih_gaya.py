"""Pilih N gaya berbeza secara rawak untuk satu remake, elak gaya yang baru dipakai dalam remake lain.

    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py                 # 3 gaya
    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py --n 3 --seed 7  # boleh diulang
    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py --kecuali kinetic,comic

Pool = 6 gaya templat (videos/remake.py jana spec terus dari storyboard) + 15 gaya mg (mg-styles-15, halaman ditulis
tangan dengan pemain mg). Gaya mg hanya masuk pool bila videos/lib/mg.js wujud. Sejarah dibaca daripada
projek/*/storyboard.json ("video": [{"gaya": ...}]): gaya dalam --elak remake terakhir dielakkan selagi pool cukup.
"""
import argparse
import json
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[4]
TEMPLAT = {
    "coway": "motion graphic Coway (pemain scenes): putih/biru, kad harga, banner",
    "kinetic": "teks besar menghentak, latar warna solid, ticker",
    "comic": "latar komik halftone, letupan 'WOW', kotak hadiah",
    "glow": "latar gelap, tulisan neon bercahaya",
    "paper": "kertas koyak, label bertampal, mesra",
    "ugc": "gaya post TikTok biasa, teks bergaris tebal, emoji",
}
MG = {
    "mg:01-flat-vector": "flat vector: blok warna, bentuk geometri, lantun elastik",
    "mg:02-line-art": "line art: satu garisan halus melukis semua",
    "mg:03-isometric": "isometrik 2.5D: dunia mini, bangunan tumbuh",
    "mg:04-3d-render": "3D render: bahan lembut/kaca, cahaya studio",
    "mg:05-cel-boil": "lukisan tangan bergetar (line boil), tekstur kertas",
    "mg:06-collage": "kolaj potongan foto, halftone, retro",
    "mg:07-liquid": "cecair mengalir, titisan, peralihan percikan",
    "mg:08-morph": "bentuk bertukar ke bentuk lain dengan licin",
    "mg:09-bauhaus": "geometri Bauhaus: merah/kuning/biru, grid, ikut beat",
    "mg:10-synthwave": "retro 80an / VHS / Y2K: grid neon, chrome",
    "mg:12-aurora-glass": "aurora kabur + kad kaca (glassmorphism), perlahan & mewah",
    "mg:18-hanazi": "hanazi (lihat prompts/18-hanazi.md)",
    "mg:19-paperclip": "pelekat bergaris tebal gaya sains popular (PaperClip)",
    "mg:20-pixel": "pixel art",
    "mg:22-hud": "HUD / antara muka fiksyen sains",
}


def history():
    rows = []
    for f in sorted((ROOT / "projek").glob("*/storyboard.json"), key=lambda p: p.stat().st_mtime):
        try:
            rows.append([v["gaya"] for v in json.loads(f.read_text()).get("video", [])])
        except (ValueError, KeyError):
            pass
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--elak", type=int, default=2, help="elak gaya dalam N remake terakhir")
    ap.add_argument("--kecuali", default="", help="gaya yang tak mahu, dipisah koma")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    pool = dict(TEMPLAT)
    mg_ok = (ROOT / "videos/lib/mg.js").exists()
    if mg_ok:
        pool.update(MG)
    for k in filter(None, a.kecuali.split(",")):
        pool.pop(k.strip(), None)
    recent = {g for row in history()[-a.elak:] for g in row} if a.elak else set()
    fresh = [g for g in pool if g not in recent]
    rng = random.Random(a.seed)
    pick = rng.sample(fresh, min(a.n, len(fresh)))
    if len(pick) < a.n:                                   # pool segar tak cukup: tambah dari yang lain
        pick += rng.sample([g for g in pool if g not in pick], a.n - len(pick))
    print(json.dumps(pick))
    for g in pick:
        print(f"  {g:22s} {pool[g]}")
    print(f"pool: {len(pool)} gaya ({'termasuk' if mg_ok else 'tanpa'} 15 gaya mg"
          f"{'' if mg_ok else ': videos/lib/mg.js belum ada'}), dielak: {', '.join(sorted(recent)) or '-'}")


if __name__ == "__main__":
    main()
