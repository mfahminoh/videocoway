# Siri B, C, D — Video tilam Coway Prime II

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

## Siri C — Pilih betul (C1 = video 16, `out/tilam/v16_prime2_final.mp4`)  ·  Siri D — Realiti rumah Malaysia

| Video | Fail | Sudut | Pain (#) |
|---|---|---|---|
| C2 | `out/tilam/c2_prime2-lembut-ke-keras.mp4` | Prime II lembut ke keras? | #24 #23 #26 |
| C3 | `out/tilam/c3_malam-pertama-sakit-badan.mp4` | Malam pertama sakit badan? Mungkin salah kekerasan | #26 #29 #22 |
| C4 | `out/tilam/c4_jenis-spring-beza-30-saat.mp4` | Pocket spring vs spring biasa vs foam: beza 30 saat | #62 #66 #61 |
| C5 | `out/tilam/c5_topper-atas-tilam-lama.mp4` | Topper atas tilam lama: berbaloi? | #58 #63 #73 |
| C6 | `out/tilam/c6_cara-test-tilam-5-minit.mp4` | Cara test tilam dalam 5 minit | #59 #38 |
| C7 | `out/tilam/c7_dah-cuba-3-tilam.mp4` | Dah cuba 3 tilam, baru faham | #156 #158 |
| D1 | `out/tilam/d1_anak-terkencing-atas-tilam.mp4` | Anak terkencing atas tilam | #85 #87 #91 #92 |
| D2 | `out/tilam/d2_tilam-gatal-servis-7-langkah.mp4` | Tilam baru, kaki gatal tiap malam | #93 #89 #94 |
| D3 | `out/tilam/d3_segan-technician-masuk-bilik.mp4` | Segan technician masuk bilik? | #114 |
| D4 | `out/tilam/d4_bilik-panas-tanpa-aircond.mp4` | Bilik panas tanpa aircond | #160 #161 #162 |
| D5 | `out/tilam/d5_toddler-tidur-sekali-katil-goyang.mp4` | Toddler tidur sekali, katil bergoyang | #164 #165 #166 |

D6 (penghantaran / pasang / Sabah-Sarawak / buang tilam lama) **belum dibuat**, menunggu pengesahan fakta.
Siri D guna tema teal; C5 guna tema hitam/kuning (kinetic). Tiada dakwaan servis selain yang tertulis di laman rasmi
(7 langkah + fogging); D1 tidak mendakwa servis menghilangkan kesan air kencing — tips pembersihan am sahaja.
VO: model Gemini TTS bercampur kerana kuota harian (suara "Orus" sama) — lihat nota di bawah.

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

## Nota suara (VO)
Semua guna suara Gemini "Orus". Model berbeza kerana had kuota harian:
- `gemini-3.1-flash-tts-preview`: B1–B7, C2, C3, C5, D3
- `gemini-3.8-flash-tts`: C4
- `gemini-2.5-flash-preview-tts`: C6, C7, D1, D2, D4, D5

Untuk suara seragam: padam `tilam/b/vo/<vid>_full.wav` bagi video tersebut dan jalankan semula `python tilam/build_b.py <vid>`
selepas kuota model 3.1 reset (±10 permintaan/hari).
