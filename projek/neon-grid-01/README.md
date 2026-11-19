# NeoN grid 4 panel (gaya iklan Threads) — neon-grid-01

Poster 1080×1080 untuk iklan Threads/Meta (pelanggan akhir), gaya rujukan iklan mop BOOMJOY di Threads: hook HURUF BESAR dalam caption + grid 2×2 dengan label kuning tulisan tangan. Setiap grid "memampatkan" satu video Neon dari pakej WP pertama (30 video) ke 4 panel.

| Grid | Video sumber | Fail | Status |
|---|---|---|---|
| G1 Pukul 3 pagi | NE05 | out/neon-grid-01/g1-pukul-3-pagi.png | ✅ lulus (19 Nov) |
| G2 3 tanda | NE09 | (dibuang) | ❌ ditolak (19 Nov) |
| G3 4 langkah | NE10 | (dibuang) | ❌ ditolak (19 Nov) |
| G4 Bajet kecil | NE01 | (dibuang) | ❌ ditolak (19 Nov) |
| G5 Baru kahwin | NE02 | out/neon-grid-01/g5-baru-kahwin.png | ✅ lulus (19 Nov) |
| G6 Penat masak air | bank bahasa | out/neon-grid-01/g6-masak-air.png | ✅ lulus (19 Nov) |
| G7 Angkut tong air | bank bahasa | out/neon-grid-01/g7-angkut-tong.png | ✅ lulus (19 Nov) |
| Copy Threads + headline + label panel (Codex) | — | copy.md | ✅ lulus (19 Nov) |
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

- 2026-11-19: copy (caption, headline, label panel) ditulis semula oleh Codex ikut AGENTS.md; label tanpa emoji, G4 panel 4 "air terus ada". Lulus semak_gaya. (user minta Codex)

- 2026-11-19: user luluskan G1 sahaja; G2–G4 ditolak terus ("tak nak langsung"). Draf baru ikut struktur G1 (masalah → produk → guna → hasil, cerita situasi), bukan listicle/langkah. (user)

- 2026-11-19: G5–G7: copy ditulis Codex (struktur G1), gambar panel 1 & 4 dijana Codex (`img/gen/`, tiada unit NeoN AI, pakaian sopan). Panel 3 guna semula bingkai klip (tuang/tekan).

## Terbuka
- [x] User luluskan G1, G5–G7 + copy (19 Nov 2026)
- [ ] Sahkan dengan ejen: RM20 sebulan masih sah untuk NeoN
