---
name: coway-persona-produk
description: Padankan persona pembeli dengan produk Coway yang sesuai (penapis air, penapis udara, tilam, peti ais, aircond, kerusi urut, bidet) dan tentukan sudut iklan, lalu tulis brief projek video dalam projek/<kod>/brief.md. Guna bila user kata "persona ni sesuai produk apa", "bawa persona ke produk", "buat brief", "mula projek video baru", atau pilih produk/sudut untuk siri video atau pakej seterusnya.
---

# Persona → produk → brief

Input: [`research/persona.md`](../../../research/persona.md) dan [`brand-brain/coway/products.md`](../../../brand-brain/coway/products.md).
Output: `projek/<kod>/brief.md` + papan status `projek/<kod>/README.md` (templat dalam [`projek/README.md`](../../../projek/README.md)).
Langkah seterusnya: `coway-skrip`.

## 1. Tujuan projek

Tanya jika tak jelas. Tujuan mengubah bilangan video dan sudut:

| Tujuan | Audiens video | Saiz | Nota |
|---|---|---|---|
| **Iklan servis ejen** | Pelanggan akhir | 10 video sebatch | Nama ejen, akaun iklan, produk yang ejen jual, promo ejen |
| **Pakej video untuk dijual** | Pelanggan akhir (ejen yang post) | 30 video (3 batch × 10) | Mesti boleh dipakai mana-mana ejen: tiada nama ejen; CTA umum "WhatsApp saya" |

## 2. Pilih persona

Guna persona yang user sebut. Jika tidak, cadangkan 1–2 dari `persona.md` ikut saiz × kos setiap perbualan × status bukti, dan nyatakan statusnya (`HIPOTESIS` = projek ini juga ujian persona).

## 3. Padankan dengan produk

Untuk persona terpilih, nilai setiap produk berkaitan (skala 1–3) dan tulis jadual dalam brief:

| Kriteria | Soalan |
|---|---|
| **Pencetus** | Adakah pencetus persona berlaku secara semula jadi untuk produk ini? (P2 "barang lama rosak" → tilam, peti ais, penapis lama) |
| **Halangan** | Adakah harga/terma produk menjawab halangan persona? (P1 "ingat tak layak" → bulanan rendah: Cinnamon RM32, Studio RM49, Neon RM54, promo RM20) |
| **Bukti visual** | Ada klip/gambar sebenar? Semak `assets/`, `brand-brain/coway/Other Brand Assets/`, `README.md` (Peta repo) |
| **Ruang kosong** | Video sedia ada untuk produk ini guna sudut apa? Elak ulang (Peta repo, `skrip/`, `projek/`) |
| **Nilai bisnes** | Produk ini dijual oleh ejen klien / ada dalam pakej (WP, Tilam, AP)? |

Produk tiada dalam `products.md` (contohnya aircond, kerusi urut): jalankan `coway-riset` mod produk dulu, atau tandakan fakta "PERLU DISAHKAN" dalam brief. Jangan reka spesifikasi.

## 4. Sudut

Pilih **1 produk utama** (2 jika pakej Combo). Tulis 3–5 **sudut** untuk batch pertama. Setiap sudut:
- **Situasi** persona dalam satu ayat (contoh: "Tilam 8 tahun, bangun pagi sakit pinggang, ingat tilam bagus mesti RM3,000 tunai").
- **Tahap kesedaran:** tak sedar masalah → sedar masalah → sedar penyelesaian → sedar produk → paling sedar. Ini menentukan hook.
- **Janji / mekanisme** produk yang menjawab situasi (fakta dari `products.md` sahaja).
- **Bantahan** yang perlu dijawab.
- **Bukti** yang boleh ditunjuk (klip, gambar, servis HEART, lencana).

Format video dicadangkan ikut sudut (keputusan akhir di `coway-video`): motion graphic (`scenes`/`hype`), cerita emosi (`story` + Seedream), Seedance, Veo/Google Flow, presenter/UGC.

## 5. Harga & promo

Harga dari `products.md`. Promo berubah setiap bulan: tanya user **sekali** untuk promo semasa (dan nama ejen untuk iklan servis), kemudian rekod dalam brief dengan tarikh disahkan.

## 6. Tulis brief

`<kod>` = `<produk>-<persona>-<nn>`, contohnya `tilam-p2-01`. Semak `projek/` untuk nombor seterusnya.

```markdown
# Brief: <Produk> × <Persona ID nama> — <kod>

Tarikh: · Tujuan: iklan servis <ejen> / pakej <nama> · Saiz: 10 (batch 1)
Persona: <ID, situasi, status bukti> · Produk: <model, harga, promo disahkan <tarikh>>

## Padanan persona × produk   (jadual skor bahagian 3, dan kenapa produk ini dipilih)
## Sudut batch 1              (3–5 sudut, format bahagian 4)
## Fakta & dakwaan dibenarkan (dengan penafian wajib)
## Jangan                     (sudut tepu, dakwaan tak boleh, aset tak boleh guna)
## Aset tersedia              (laluan klip / gambar)
## Perlu disahkan
```

Cipta `projek/<kod>/README.md` dari templat, tandakan langkah 2 ✅, commit, dan beritahu user: persona, produk dipilih (dan kenapa), sudut, serta apa yang menunggu pengesahan.
