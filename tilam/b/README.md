# Siri B — Badan & tahan lama (Coway Prime II)

Berdasarkan `tilam/plan_v2_draft.md` (Tiang B). Kategori A ditolak.

| Video | Fail | Sudut | Pain (#, `research/Pain_Tilam_Malaysia_v2.xlsx`) |
|---|---|---|---|
| B1 | `out/tilam/b1_sakit-pinggang-bangun-pagi.mp4` | 3 tanda tilam tak menyokong → spring 7 zon + latex 5 zon → Soft/Firm | #45 #49 #39 |
| B2 | `out/tilam/b2_tilam-tenggelam-topper.mp4` | Topper atas tilam mendap ikut tenggelam → struktur Prime II + topper boleh tukar (3 tahun) | #73 #63 #75 |
| B3 | `out/tilam/b3_tilam-murah-4-bulan-melendut.mp4` | Kinetic: komen sebenar "4 bulan dah melendut" → hybrid 4 lapisan | #74 #72 #79 |
| B4 | `out/tilam/b4_badan-besar-tilam-tahan.mp4` | Balas komen: badan besar → spring 7 zon, had ±160–200 kg gabungan, Firm >70 kg | #80 #64 #76 |
| B5 | `out/tilam/b5_tilam-untuk-mak-ayah.mp4` | Emosi: hadiah untuk mak ayah → Soft/Firm + servis berkala | #43 #46 #42 |
| B6 | `out/tilam/b6_topper-3-tahun-jawapan-jujur.mp4` | Balas komen jujur: topper ditukar 3 tahun sekali, kenapa, apa nak buat | #117 |
| B7 | `out/tilam/b7_kualiti-dari-dekat.mp4` | Close-up kualiti: fabrik, jahitan, latex, spring berpoket, sabut kelapa, rangka | #123–#126 |

**Fakta dari ejen (bukan laman rasmi) — sahkan sebelum iklan:** had berat ±160–200 kg gabungan (B4),
Firm untuk >70 kg (B4, B6), topper ditukar 3 tahun sekali untuk pelanggan sewa (B2, B4, B6).
Tiada harga dalam mana-mana video. Tiada dakwaan perubatan (B1 ada nota "rujuk doktor").
Footage & gambar: rasmi Coway (`assets/tilam/prime2/`).

## Bina semula
```
python tilam/build_b.py b1                 # satu video (VO Gemini dijana sekali, disimpan di tilam/b/vo/)
python tilam/build_b.py all
python tilam/build_b.py b1 --stills 2,8,16 # pratonton
python tilam/vo/check_asr.py b1            # semak potongan VO ikut baris (Gemini)
```
- Skrip & babak: `tilam/b/<vid>.json` — baris VO (`text`) + `scene` (bg, media, head, words, items, comment, chips, note, cta, diagram).
  `at` = saat dari mula baris, atau perkataan dalam baris (masa dianggar ikut kedudukan huruf).
- Enjin: `src/tilam/b/player.html`. VO & penjajaran: `tilam/lib_vo.py`. Muzik/SFX: `tilam/lib_audio.py`.
- Tukar skrip VO → padam `tilam/b/vo/<vid>_full.wav` supaya dijana semula (kuota Gemini TTS ±10/hari/model).
