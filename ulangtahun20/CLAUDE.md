# Coway Neon — Promosi Ulangtahun ke-20 (30 video, 20 saat)

Projek ini hasilkan 30 video iklan direct response, 9:16 (1080×1920), tepat 20 saat.
Semua copy dah siap dalam `data/videos.csv`. Kerja Claude Code ialah bina templat, padankan klip, dan render.

## Fail input
- `data/videos.csv` — 30 baris, satu video satu baris: style, teks skrin setiap babak (`text_0_3s` … `text_16_20s`), `voiceover`, dan tag klip (`clip_hook_tag`, `clip_body_tag`).
- `data/clips.csv` — klip sumber dengan tag: `talking_head`, `produk_guna`, `susu_bayi`, `komersial`, `model_lain`, `semak_dulu`, `jangan_guna`.
- `data/brand.json` — fon dan warna Coway Neon.
- `sources/` — fail video sebenar dari Google Drive (folder "Video Coway - Google Flow"). Nama fail sama dengan lajur `file` dalam clips.csv.

## Guna semula projek sedia ada: `../VideoCoway`
- `../VideoCoway/tools/ffmpeg` — ffmpeg.
- `../VideoCoway/.venv` — Python dengan Playwright.
- `../VideoCoway/scripts/render.py` — corak render: halaman HTML deterministik `window.__render(t)`, frame dipaip terus ke ffmpeg. Ikut corak yang sama.
- `../VideoCoway/assets/fonts/NotoSans-Variable.ttf`, `assets/logo/`, `assets/img/` (gambar produk Neon 5 warna, `coway-neon-wp-product-video.mp4`).
- Jangan ubah apa-apa dalam `../VideoCoway`. Salin apa yang perlu ke projek ini.

## Struktur setiap video (20 saat)
| Masa | Babak | Teks skrin dari CSV |
|---|---|---|
| 0–3s | Hook | `text_0_3s` — besar, tengah skrin, HURUF BESAR |
| 3–7s | Tawaran | `text_3_7s` |
| 7–12s | Tawaran tambahan (hadiah) | `text_7_12s` |
| 12–16s | Urgency | `text_12_16s` |
| 16–20s | CTA | `text_16_20s` = "WhatsApp sekarang" + butang/ikon WhatsApp berdenyut |

Tukar shot setiap 2–3 saat. Sarikata voiceover sepanjang video, di bawah teks babak.

## 8 style (lajur `style`)
- **S1 Hentak Harga** — teks harga gergasi dihentak ke skrin (scale-in laju + shake kecil).
- **S2 Countdown** — jam undur ke 25 Oktober di penjuru sepanjang video. `[x]` hari = 25 Okt 2026 tolak tarikh render.
- **S3 Kalkulator Harga** — kalkulator/angka animasi (RM20 ÷ 30 hari, 7 × RM20 = RM140).
- **S4 3 Sebab** — nombor 1-2-3 besar atas kad pastel, satu sebab satu babak.
- **S5 Kad Soalan Lazim** — kad soalan muncul satu-satu, jawapan pendek di bawah.
- **S6 Sekarang vs Tunggu** — skrin dibelah: kiri "tunggu / lepas 25 Okt", kanan "sekarang / RM20".
- **S7 Montaj ASMR** — potongan 1 saat, bunyi air dan klik, teks minimum, VO sangat pendek.
- **S8 Pengumuman Ulangtahun** — nombor "20" besar + confetti, latar pink/pastel.

## Gaya (ikut `data/brand.json`)
- Fon Noto Sans: 800 untuk hook dan harga, 500 untuk teks biasa.
- Teks atas klip: putih dengan bayang lembut. Lencana harga/tarikh: Coway Blue `#00A0E0`, teks putih.
- Jalur urgency: charcoal `#231F20`. Kad S4/S5: Ciel Blue / Mint, teks charcoal.
- Gaya dua berat ala video Coway: "Promo **RM20**" (perkataan nipis + perkataan tebal).
- Logo Coway kecil di penjuru atas sepanjang video. Kad akhir: latar putih, logo Coway Blue.

## Peraturan wajib (semak sebelum render setiap video)
1. Setiap kali "RM20" muncul di skrin, "7 bulan pertama" mesti ada dalam babak yang sama.
2. Tarikh tamat ialah **25 Oktober**. Jangan sebut harga biasa / harga lepas promo.
3. CTA hanya "WhatsApp sekarang". Jangan tambah kata kunci lain.
4. Jangan sebut Halal, JAKIM atau WQA.
5. Shot yang ada teks "RM20" mesti tunjuk **Coway Neon**. Klip `model_lain` (Villaem, model ais) hanya untuk b-roll di babak tanpa harga.
6. Jangan guna klip `jangan_guna` (aircond, washer-dryer). Klip `semak_dulu` — tonton dulu, guna hanya jika jelas penapis air Coway.
7. Jangan guna klip yang tunjuk harga atau promo lama.
8. Placeholder yang belum diisi (`[x]`, `[5]`) — tanya pengguna, jangan teka.

## Audio
- Jika `audio/V01.wav` dan seterusnya wujud, guna sebagai voiceover.
- Jika tiada, tanya pengguna dulu: rakam suara sendiri, atau render dengan muzik + sarikata sahaja.

## Aliran kerja
1. Imbas `sources/`: ffprobe tempoh/resolusi, ambil frame sampel setiap klip, sahkan tag dalam clips.csv betul. Laporkan klip yang tak sepadan (contoh: tag `produk_guna` tapi bukan Neon).
2. Bina templat S1 dahulu dan render **V01 sahaja** ke `out/`. Tunjuk contact sheet (frame 1.5s, 5s, 9s, 14s, 18s) kepada pengguna dan tunggu kelulusan.
3. Bina 7 templat lain, render satu video setiap style untuk semakan.
4. Lepas lulus, render semua 30 video. Nama fail ikut lajur `file` (contoh `S1-V01-v1.mp4`).
5. QC akhir: tempoh tepat 20.0s, 1080×1920, peraturan wajib 1–5 dipatuhi. Tulis `out/qc.csv`.
