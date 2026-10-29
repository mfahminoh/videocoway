"""Pilih N gaya berbeza secara rawak untuk satu remake, elak gaya yang baru dipakai dalam remake lain.

    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py                 # 3 gaya
    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py --n 3 --seed 7  # boleh diulang
    python3 .claude/skills/coway-remake/scripts/pilih_gaya.py --kecuali kinetic,comic

Pool = 6 gaya templat (videos/remake.py jana spec terus dari storyboard) + 10 gaya mg ✅ (mg-styles-15, halaman ditulis
tangan dengan pemain mg, lihat coway-video/formats/mg-gaya.md); --semua tambah 4 gaya ⚠️. Gaya mg hanya masuk pool bila
videos/lib/mg.js wujud. Sejarah dibaca daripada
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
MG = {   # status dari coway-video/formats/mg-gaya.md: lalai = ✅; --semua tambah ⚠️; 04-3d-render (perlu Blender) tiada
    "mg:01-flat-vector": "flat vector: blok warna, bentuk geometri, lantun elastik (contoh NL01FV)",
    "mg:07-liquid": "cecair mengalir: titisan, aliran, penapisan, air bersih",
    "mg:19-paperclip": "explainer pelekat bergaris tebal: fakta, perbandingan, carta",
    "mg:08-morph": "satu bentuk berubah sepanjang video: titis -> gelas -> produk -> harga",
    "mg:03-isometric": "rumah/dapur isometrik: pemasangan, servis",
    "mg:06-collage": "kolaj kertas potong + gambar produk, mesra ibu",
    "mg:12-aurora-glass": "aurora kabur + kad kaca, premium/teknologi",
    "mg:22-hud": "HUD imbasan kualiti air/udara, sensor",
    "mg:18-hanazi": "kapsyen meriah variety show atas gambar/klip",
    "mg:02-line-art": "minimal: satu garisan melukis produk",
}
MG_LAIN = {
    "mg:09-bauhaus": "geometri Bauhaus, premium; kurang mesra keluarga",
    "mg:10-synthwave": "retro 80an / VHS / Y2K; promo malam / 11.11",
    "mg:20-pixel": "pixel art; Gen Z",
    "mg:05-cel-boil": "lukisan tangan bergetar; kerja paling berat",
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
    ap.add_argument("--semua", action="store_true", help="masukkan juga gaya mg bertanda ⚠️ dalam mg-gaya.md")
    ap.add_argument("--maks-mg", type=int, default=3, help="had gaya mg (ditulis tangan, lebih lambat) dalam satu remake")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    pool = dict(TEMPLAT)
    mg_ok = (ROOT / "videos/lib/mg.js").exists()
    if mg_ok:
        pool.update(MG)
        if a.semua:
            pool.update(MG_LAIN)
    for k in filter(None, a.kecuali.split(",")):
        pool.pop(k.strip(), None)
    recent = {g for row in history()[-a.elak:] for g in row} if a.elak else set()
    fresh = [g for g in pool if g not in recent]
    rng = random.Random(a.seed)
    pick = []
    for cand in (rng.sample(fresh, len(fresh)), rng.sample(list(pool), len(pool))):   # segar dulu, kemudian selebihnya
        for g in cand:
            if len(pick) < a.n and g not in pick and (not g.startswith("mg:") or sum(x.startswith("mg:") for x in pick) < a.maks_mg):
                pick.append(g)
    print(json.dumps(pick))
    for g in pick:
        print(f"  {g:22s} {pool[g]}")
    n_mg = sum(g.startswith("mg:") for g in pool)
    print(f"pool: {len(pool)} gaya ({len(pool) - n_mg} templat + {n_mg} mg"
          f"{'' if mg_ok else '; videos/lib/mg.js belum ada'}), dielak: {', '.join(sorted(recent)) or '-'}")


if __name__ == "__main__":
    main()
