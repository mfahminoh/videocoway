# NeoN × templat swipe Grüns — neon-swipe-01

Dua templat poster iklan (pelanggan akhir) yang di-swipe dari artifak **Grüns Swipe File** (https://claude.ai/artifact/QLScV8VD6BvirhdKm83ybT), dipilih user 11 Nov 2026:

| Templat | Sumber Grüns | Fail | Kenapa |
|---|---|---|---|
| A · "X? NAH, COWAY." | #6, #21 Nütrops "ADDERALL? NAH, MUSHROOMS" | `poster/templat-nah.html` | Iklan Grüns paling lama hidup (39–69 hari) = calon pemenang |
| B · "Selamat tinggal / Hello" | #212 "Goodbye, Messy Greens!" | `poster/templat-goodbye.html` | Lawan kebiasaan lama (angkut air, masak air), bukan jenama lain |

| Langkah | Status | Fail | Nota |
|---|---|---|---|
| 5 Poster HTML (4) | ✅ draf | `out/neon-swipe-01/poster/{nah-a1-air-botol,nah-a2-masak-air,goodbye-b1-angkut-air,goodbye-b2-masak-air}.png` | menunggu kelulusan user |
| Poster D1 baru | ✅ 12 Nov | `out/neon-swipe-01/poster/nah-d1-dapur-sempit.png` | "DAPUR SEMPIT? TETAP MUAT." + garis "sejengkal je"; hash 975abeffde553ec3c13a4d7688149c3d; gambar untuk 5 variasi NEON-D1-V* |
| Prompt Flow | ✅ draf | `poster/flow-prompts.md` | A1, A2, B1, B2 + idea varian |
| 7 Iklan | ✅ 12 Nov | `iklan/README.md` | A1, A2, B1 × 2 ad set promo RM18 (Coway Azzuddin), ganti PR06 & PR09; bank `SWIPE-A1/A2/B1` |

## Cara guna templat

- Tambah poster: tambah satu objek dalam `VARIAN` (dalam `<script>` setiap fail). Tajuk templat A mengecil sendiri supaya muat satu baris.
- Tukar warna unit: tukar `UNIT` (potongan tanpa latar, contoh `img/neon-ciel-34.png`).
- Latar/prop baru: jana dengan Seedream, tanpa teks, dengan tengah kosong (A) atau atas latar krim #F2EEE6 (B). Prompt asal dalam sejarah sesi 11 Nov 2026; corak ringkas dalam `poster/flow-prompts.md`.
- Render:
  ```bash
  /Users/Fahmi/Claude/VideoCoway/.venv/bin/python .claude/skills/coway-poster/scripts/render_poster.py projek/neon-swipe-01/poster/templat-*.html --out out/neon-swipe-01/poster
  ```

## Aset

- `poster/img/bg_a1.jpg`, `bg_a2.jpg`: latar prop templat A (Seedream 4.5, 1728×2160)
- `poster/img/bg_b1.jpg`, `bg_b2.jpg`: prop templat B (Seedream 4.5, 2048×2048). `bg_b1.jpg` ialah versi edit tanpa tulisan "19.5L" pada galon; `bg_b1_asal.jpg` asal.
- `poster/img/bg_d1.jpg`: latar dapur sempit templat A (Seedream 4.5, 12 Nov)
- `poster/img/neon-ciel-34.png`: unit NeoN Ciel Blue rasmi (dari neon-rm20-01)
- Kos Seedream: 5 gambar ≈ USD 0.20

## Keputusan
- 2026-11-12: user: tiada ukuran cm ("sejengkal" sahaja); setiap poster sorot panas, sejuk, suhu bilik + 5 pilihan warna. Copy ikut `coway-gaya-bahasa`.
- 2026-11-12: user: iklan melebihi had kos → tukar kepada 3 poster (A1, A2, B1).
- 2026-11-11: user pilih templat Grüns #6/#21 dan #212, bentuk HTML + prompt Flow.
- 2026-11-11: harga = pakej serendah RM20 sebulan + penghantaran & pemasangan percuma (disahkan 4 Nov 2026, sah hingga 30 Nov 2026 dalam bank autopilot).

## Terbuka
- [ ] User luluskan / ubah 4 poster
- [ ] Jana versi Flow (manual) jika mahu
- [ ] Selepas lulus: upload ke akaun Coway Azzuddin dan tambah ke bank autopilot (`fizah-wp`) sebagai `LULUS`
