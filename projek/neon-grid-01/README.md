# NeoN grid 4 panel (gaya iklan Threads) — neon-grid-01

Poster 1080×1080 untuk iklan Threads/Meta (pelanggan akhir), gaya rujukan iklan mop BOOMJOY di Threads: hook HURUF BESAR dalam caption + grid 2×2 dengan label kuning tulisan tangan. Setiap grid "memampatkan" satu video Neon dari pakej WP pertama (30 video) ke 4 panel.

| Grid | Video sumber | Fail | Status |
|---|---|---|---|
| G1 Pukul 3 pagi | NE05 | out/neon-grid-01/g1-pukul-3-pagi.png | ⏳ draf |
| G2 3 tanda | NE09 | out/neon-grid-01/g2-3-tanda.png | ⏳ draf |
| G3 4 langkah | NE10 | out/neon-grid-01/g3-4-langkah.png | ⏳ draf |
| G4 Bajet kecil | NE01 | out/neon-grid-01/g4-bajet-kecil.png | ⏳ draf |
| Copy Threads | — | copy.md | ⏳ draf |
| 7 Iklan | — | | — |

## Cara bina
- Teks panel & susunan: tatasusunan `GRIDS` dalam `grid.html`. Label `{r:..}` merah, `{b:..}` biru, `\n` baris baru.
- Gambar: bingkai klip asal `assets/clips/neon/*.mp4` (tanpa kapsyen) → `img/*.jpg`; cutout rasmi `img/neon-ciel-34.png`; gambar rasmi brand-brain (`self-service.jpg`, `heart-service.jpg`); `assets/img/neon/podium5.jpg`.
- Font label: Kalam 700 (Google Fonts, perlu internet semasa render).
- Render:
  ```bash
  /Users/Fahmi/Claude/VideoCoway/.venv/bin/python .claude/skills/coway-poster/scripts/render_poster.py projek/neon-grid-01/grid.html --out out/neon-grid-01
  ```

## Keputusan
- 2026-11-19: user minta guna skrip pakej 30 video penapis air dan mampatkan beberapa video Neon ke grid 4 panel macam iklan mop. Pilih NE05, NE09, NE10, NE01. (user + Claude)
- 2026-11-19: harga ikut tawaran semasa (RM20 sebulan + hantar & pasang free), bukan RM54 + rebat dalam video asal. Ukuran tulis "sejengkal je". (Claude, ikut coway-gaya-bahasa)
- 2026-11-19: close-up unit dari klip presenter/press_pour ada tulisan butang herot (klip AI) → panel pakej guna gambar rasmi self-service & heart service.

## Terbuka
- [ ] User luluskan 4 grid + copy
- [ ] Sahkan dengan ejen: RM20 sebulan masih sah untuk NeoN
