# Video Tilam Coway

- **Draf plan v2 (berasaskan data pain 169 ayat):** [`plan_v2_draft.md`](plan_v2_draft.md)
- **Siri B, C, D (19 video Prime II) + Siri L (15 video Prime Lite):** [`b/README.md`](b/README.md)
- **Prime Lite: analisa 5 video rujukan + draf 15 video:** [`lite/analisis_dan_plan.md`](lite/analisis_dan_plan.md)
- Plan asal 30 video: [`plan_30_video.md`](plan_30_video.md)
- Padanan pain × produk (data Lowyat): [`padanan_pain_coway.md`](padanan_pain_coway.md)
- Data research: `research/`

## Video 16 — Bedah tilam Coway Prime II (±52s, 1080×1920)
**Siap:** `out/tilam/v16_prime2_final.mp4`

Motion graphic 3D: tilam Prime II "dibedah" lapisan demi lapisan → cantum semula → pilihan Soft/Firm + promo bulan ini → CTA WhatsApp.
Kapsyen terbakar (sesuai tonton tanpa bunyi). VO: Gemini TTS (suara "Orus").

| Babak | Isi |
|---|---|
| Hook | "Apa ada DALAM tilam ni?" → tilam terburai |
| Lapisan 01 | Fabrik anti-statik & penyejuk (benang karbon + benang penyejuk) |
| Lapisan 02 | Topper boleh tukar (topper ditarik keluar & ganti baru) |
| Lapisan 03 | Latex asli 5 zon ketumpatan |
| Lapisan 04 | Foam berliang — aliran udara |
| Lapisan 05 | Pocket spring 7 zon — pasangan pusing tak terasa |
| Lapisan 06 | Sabut kelapa (paling bawah) — sokongan padu, serap lembapan |
| Cantum | COWAY PRIME II · 33 cm · Soft & Firm · Queen & King |
| Promo | SOFT (tidur mengiring) / FIRM (tidur terlentang) · Queen & King · "PROMO BULAN INI — tanya saya harga terkini" (tiada angka harga) |
| CTA | Nak rasa sendiri? WhatsApp saya sekarang |

**Tiada harga dalam video** — promo Coway bertukar setiap bulan, jadi video ni boleh guna tanpa render semula.
Susunan lapisan disahkan dengan animasi lapisan rasmi Coway (`assets/tilam/prime2/video/prime2-panel5.mp4`). Edit teks dalam `src/tilam/v16_prime2.html`
(objek `TEXT`, `BADGES`, blok `#pr` untuk kad Soft/Firm + promo).

### Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow
python tilam/vo/gemini_tts.py ...          # pilihan: jana VO baharu (lihat bawah)
python tilam/vo/split.py v16               # VO penuh -> baris + masa (tilam/vo/v16_timing.json)
python tilam/vo/splice.py v16 tilam/vo/v16_patch09.wav 09     # ganti baris 09 (promo, tanpa harga)
python tilam/build_v16.py                  # render + muzik/SFX + gabung
python tilam/build_v16.py --stills 2,8,20  # pratonton PNG -> out/stills/
```
VO baharu: skrip dalam `tilam/vo/lines_v16.json`. Jana keseluruhan skrip dalam **satu** permintaan Gemini TTS
(kuota percuma ±10 permintaan/hari/model) ke `tilam/vo/v16_full.wav`, kemudian kemas kini anggaran masa setiap baris
dalam `tilam/vo/v16_asr.json` (transkrip Gemini) dan jalankan `split.py`.
Atau rakam suara sendiri sebagai `tilam/vo/v16_full.wav` (baca baris ikut turutan dengan jeda ±0.5s).

Nota: `v16_vo.wav` = `v16_full.wav` (baris 01–08, 10) + `v16_patch09.wav` (baris 09 baharu). Jalankan `split.py` dan kemudian `splice.py` seperti di atas.

## Aset rasmi Prime II
`assets/tilam/prime2/` — gambar & video dari laman rasmi coway.com.my (produk, close-up lapisan, Soft/Firm, servis 7 langkah, video lapisan). Banner promo tidak diambil.
