---
name: coway-poster
description: Hasilkan poster Coway sebagai PNG — (A) poster iklan untuk pelanggan akhir (Meta feed 1080×1350/1080×1080, story 1080×1920) dan (B) poster pakej video untuk Threads/iklan yang menjual pakej kepada ejen — guna HTML yang dirender (teks & harga tepat) dengan gambar rasmi, bingkai video siap, atau latar Seedream. Guna bila user minta poster, static ad, iklan gambar, visual Threads, poster pakej, atau "buat poster dari video ni".
---

# Poster Coway

Input: `projek/<kod>/brief.md`, `skrip.md`, video siap dalam `out/<kod>/`.
Output: sumber dalam `projek/<kod>/poster/` (HTML, prompt Seedream), PNG dalam `out/<kod>/poster/`.
Langkah seterusnya: iklan (jenis A) atau `coway-threads` (jenis B).

## Jenis poster

| | **A · Iklan** | **B · Pakej video** |
|---|---|---|
| Audiens | Pelanggan akhir (keluarga) | **Ejen Coway** yang akan beli pakej |
| Mesej | Pain persona → produk → harga → WhatsApp | "Feed kosong?" → pakej N video siap → harga pakej → "Komen <KATA> / DM" |
| Saiz | Feed 1080×1350 (utama), 1080×1080; story 1080×1920 | Threads 1080×1350 |
| Contoh dalam repo | `static/fridge/poster*.html` (+ `base.css`) → `out/static/` | `promo/threads/posters.html` → `promo/threads/out/` (AP vs Jerebu) |
| Visual | Gambar produk rasmi, latar warna produk / Seedream | Mockup telefon dengan bingkai video siap, latar tema pakej |

Satu batch: jenis A = 5–7 poster (satu setiap sudut / layout brand-guide §8); jenis B = 1 poster utama + 1 untuk setiap hari kempen Threads (lihat `coway-threads`).

## 1. Kandungan

- **A:** hook & harga dari skrip yang menang / `skrip.md`; ikut layout `brand-brain/coway/brand-guide.md` §8 (hero produk, ciri, masalah→penyelesaian, banding model, testimoni/trade-in, promo urgency). Headline 4–8 perkataan, bahasa persona.
- **B:** nama pakej, bilangan video, 3–4 isi ("✅ Siap VO BM, 9:16, download terus post"), harga pakej, had ("TERHAD 25 ORANG"), kata kunci komen. Harga pakej mesti sama dengan `projek/<kod>/threads.md` / CLAUDE.md.
- Penafian (A): "*Tertakluk terma & syarat" untuk promo; TÜV untuk UV 99.9%; nota kaki angka peti ais. Label kecil "Ejen Sah Coway" jika logo Coway dipakai.

## 2. Visual

1. **Gambar rasmi:** `brand-brain/coway/Other Brand Assets/<kategori>/<produk>/` (hero `*-front-view`, `*-features*`, `*-control-panel*`), `assets/img/`.
2. **Bingkai video siap** (jenis B, dan A untuk kesinambungan dengan video iklan):
   ```bash
   python3 render.py --src videos/<ID>/index.html --stills 2.5,9   # atau ekstrak dari MP4 siap dengan ffmpeg -ss <t> -frames:v 1
   ```
   Pilih bingkai dengan hook terbaca (macam p01: 5 telefon, tengah paling besar).
3. **Latar Seedream** (suasana, orang, rumah Malaysia): guna skill `seedream`, simpan dalam `projek/<kod>/poster/img/`. Prompt **tanpa teks**; lampirkan gambar produk rasmi sebagai `--ref` jika unit muncul, dan semak bentuk/logo.

**Teks, harga, CTA dan logo sentiasa dari HTML**, tidak dijana oleh model gambar.

## 3. Bina & render

Salin gaya contoh terdekat (`static/fridge/base.css` untuk A, `<style>` dalam `promo/threads/posters.html` untuk B) ke `projek/<kod>/poster/`. Satu fail boleh ada banyak poster: `<div class="poster" id="p01">…</div>` (`.poster` = 1080×1350, `overflow:hidden`). Fon: `assets/fonts/` (Poppins, Anton). Laluan relatif dari `projek/<kod>/poster/` = `../../../`.

```bash
python3 .claude/skills/coway-poster/scripts/render_poster.py projek/<kod>/poster/*.html --out out/<kod>/poster
```

Tanpa `.poster`, halaman penuh dirender pada `--size` atau `<meta name="poster-size" content="1080x1080">`. Skrip memberi amaran jika gambar tak dimuat.

## 4. Semak (Read setiap PNG)

- [ ] Headline terbaca pada saiz telefon (≥ 60 px untuk headline, ≥ 26 px untuk isi)
- [ ] Teks ≤ ~20% kawasan (feed); zon selamat story 120 px atas & bawah
- [ ] Harga = brief / pakej; penafian ada (A)
- [ ] Produk betul (model, warna); tiada teks rosak dari Seedream
- [ ] Jenis B bercakap kepada ejen, jenis A kepada pelanggan, tidak bercampur

Tambah `!out/<kod>/` dalam `.gitignore` jika belum, commit, kemas kini papan status (langkah 5), dan tunjuk poster kepada user.
