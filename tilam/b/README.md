# Siri B, C, D (Prime II) & L (Prime Lite) — Video tilam Coway

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

| D6 | `out/tilam/d6_hantar-pasang-percuma-sabah-sarawak.mp4` | Hantar & pasang percuma, Sabah & Sarawak termasuk (fakta dari ejen) | #133 #130 #136 #135 |

D6 sengaja tidak sebut naik tangga atau tilam lama.
Siri D guna tema teal; C5 guna tema hitam/kuning (kinetic). Tiada dakwaan servis selain yang tertulis di laman rasmi
(7 langkah + fogging); D1 tidak mendakwa servis menghilangkan kesan air kencing — tips am + topper boleh dibuka & mudah diangkat untuk dicuci sendiri.
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
- `gemini-3.8-flash-tts`: C4, D1 (versi baharu), D6
- `gemini-2.5-flash-preview-tts`: C6, C7, D2, D4, D5 (model ini kini tidak digunakan lagi oleh `lib_vo.py`)

Untuk suara seragam: padam `tilam/b/vo/<vid>_full.wav` bagi video tersebut dan jalankan semula `python tilam/build_b.py <vid>`
selepas kuota model 3.1 reset (±10 permintaan/hari).

Nota semakan: `check_asr.py` jatuh ke model Gemini "lite" bila kuota habis. Model lite sering salah dengar "Coway"
(cth. "Koei", "Kuari") walaupun pada VO yang betul — jadi semakan sebutan jenama perlu didengar sendiri.

## Siri L — Coway Prime Lite (15 video)
Spesifikasi dijana oleh `tilam/lite/gen_specs.py` (tema biru muda, footage & gambar rasmi `assets/tilam/primelite/`).
Analisa & sumber: `tilam/lite/analisis_dan_plan.md`.

| Video | Fail | Sudut | Rujukan |
|---|---|---|---|
| L01 | `out/tilam/l01_3-sebab-ramai-pilih-prime-lite.mp4` | 3 sebab ramai pilih Prime Lite | r1 r6 |
| L02 | `out/tilam/l02_patutlah-ramai-order.mp4` | Patutlah ramai order | r3 |
| L03 | `out/tilam/l03_anak-terkencing-buka-zip.mp4` | Anak terkencing? Buka zip je | #87 r5 |
| L04 | `out/tilam/l04_lite-vs-prime2-30-saat.mp4` | Prime Lite vs Prime II: beza 30 saat | r4 |
| L05 | `out/tilam/l05_lite-atau-prime2-pilih.mp4` | Lite atau Prime II? Pilih dalam 10 saat | #57 #70 |
| L06 | `out/tilam/l06_5-zon-vs-7-zon.mp4` | 5 zon vs 7 zon | #62 #66 |
| L07 | `out/tilam/l07_suami-mengiring-isteri-terlentang.mp4` | Suami mengiring, isteri terlentang | #23 #164 |
| L08 | `out/tilam/l08_12-inci-rasa-hotel.mp4` | 12 inci: tidur rasa hotel | r1 r5 |
| L09 | `out/tilam/l09_robot-vakum-bawah-katil.mp4` | Robot vakum masuk bawah katil | #93 #89 |
| L10 | `out/tilam/l10_anak-lasak-bucu-lembut.mp4` | Anak lasak? Bucu lembut | #164 #165 |
| L11 | `out/tilam/l11_pasangan-pusing-terjaga.mp4` | Pasangan pusing, you terjaga? | #164 #166 |
| L12 | `out/tilam/l12_bilik-panas-cooling.mp4` | Bilik panas, kipas satu je | #160 #161 #162 |
| L13 | `out/tilam/l13_topper-tukar-percuma.mp4` | Topper tukar percuma, tilam kekal segar | #73 #117 |
| L14 | `out/tilam/l14_rumah-pertama-set-biru.mp4` | Rumah pertama, set biru lembut | #2 #57 |
| L15 | `out/tilam/l15_lite-servis-tetap-penuh.mp4` | Tilam Lite, servis tetap penuh | #93 #114 |

Fakta disahkan ejen (6 Okt): Medium Firm sahaja (all-rounder), topper cuci di rumah (bukan dobi), tukar topper 3 tahun sekali
(pelanggan sewa), servis setiap 4 bulan (pakej termasuk servis), hantar & pasang percuma termasuk Sabah & Sarawak.
VO: `gemini-3.1-flash-tts-preview` untuk L01–L08, `gemini-3.8-flash-tts` untuk L09–L15.

## Variasi gaya editing (1 video = 1 gaya, digilir)
Spesifikasi yang sama (`tilam/b/<vid>.json`, VO & masa sama) boleh dirender dalam 8 gaya. Gaya 1–7 dalam
`src/tilam/b/styled.html`; gaya `coway` = `player.html` asal.

| # | Gaya | Rupa |
|---|---|---|
| 1 | `kinetic` | Teks besar 1–3 perkataan ikut suara, kata kunci kuning, footage gelap |
| 2 | `berita` | Bar "BERITA TILAM", LANGSUNG, lower-third, ticker fakta |
| 3 | `whiteboard` | Kertas grid, tulisan marker, garis bawah merah, checklist, video dalam bulatan |
| 4 | `sinematik` | Hitam, warna filem, "BAB n", sari kata serif emas, grain |
| 5 | `majalah` | Krim, serif, nombor Roman, gambar berbingkai, petikan |
| 6 | `chat` | Perbualan WhatsApp: soalan pelanggan → jawapan ejen |
| 7 | `clean` | Footage penuh + kapsyen kecil (minimal) |
| 8 | `coway` | Gaya asal siri B/C/D/L |

```
python tilam/build_b.py l01 l02 l03 l04 l05 l06 l07 l08 l09 l10 --rotate   # video 1 kinetic, 2 berita, 3 whiteboard, ...
python tilam/build_b.py l01 l02 --rotate --offset 3                         # mula dari gaya ke-4 (sinematik)
python tilam/build_b.py c4 --style chat                                     # satu gaya tertentu
python tilam/build_b.py l07 --style berita --stills 2,8,20                  # pratonton
```
Output: `out/tilam/gaya/<vid>_<gaya>.mp4`. Muzik ikut gaya (kinetic/berita = laju, sinematik/majalah = hangat).
VO tidak dijana semula jika `tilam/b/vo/<vid>_full.wav` sudah ada (tiada kuota TTS digunakan).
