# Brand Brain — Iklan Static Coway

Satu tempat untuk semua bahan jenama Coway, supaya setiap iklan static (manual, Canva, atau jana dengan AI) guna gambar produk sebenar, harga betul dan nada yang sama.

```
brand-brain/
├── fetch_assets.py              # tarik semula aset dari coway.com.my
└── coway/
    ├── brand-guide.md           # logo, warna, fon, nada, CTA, peraturan & layout
    ├── products.md              # semua produk: model, tangki, warna, harga, sudut iklan
    └── Other Brand Assets/
        ├── _brand/              # logo Coway, HEART Service, Halal, NSF, WQA, anugerah, gambar penapis
        ├── water-purifier/<produk>/   # gambar produk + copy.md (teks laman rasmi)
        ├── air-purifier/<produk>/
        ├── handsfree-bidet/<produk>/
        ├── outdoor/<produk>/
        └── index.json           # senarai gambar setiap produk + URL sumber
```

## Cara guna untuk satu iklan static

1. Pilih produk & sudut dalam `coway/products.md`.
2. Ambil gambar dari `coway/Other Brand Assets/<kategori>/<produk>/`:
   - `*-CHP-*.jpg` / `*-front-view.jpg`: gambar hero produk
   - `*-side-view*`, `*-top-view*`, `*-control-panel*`: sudut & close-up
   - `*-features*.jpg`: gambar gaya hidup untuk ciri (UV, Eco Mode, Child Lock)
   - `*-product-spec.png`: kad spesifikasi rasmi
3. Ikut warna, fon, CTA dan peraturan dalam `coway/brand-guide.md`.
4. Sahkan harga/promo semasa sebelum publish.

Bila guna AI untuk jana gambar (Gemini/Higgsfield dll.), lampirkan gambar hero produk sebagai **rujukan**, supaya bentuk unit tak berubah, dan bagi `brand-guide.md` sebagai konteks.

Gambar tambahan dalam repo: `assets/img/` (Villaem 3, Neo), `assets/stills/` (still dari klip video).

## Kemas kini

```
python brand-brain/fetch_assets.py            # semua produk (gambar sedia ada dilangkau)
python brand-brain/fetch_assets.py villaem3   # satu produk sahaja
```
Tambah produk baru dalam `PRODUCTS` di `fetch_assets.py`.

Gambar & teks adalah hak cipta Coway Malaysia. Guna hanya untuk iklan anda sebagai ejen sah Coway.
