# Video Tilam Coway

Plan 30 video: [`plan_30_video.md`](plan_30_video.md)

## Video 16 — Bedah tilam Coway Prime II (±51s, 1080×1920)
**Siap:** `out/tilam/v16_prime2_final.mp4`

Motion graphic 3D: tilam Prime II "dibedah" lapisan demi lapisan → cantum semula → harga sewa → CTA WhatsApp.
Kapsyen terbakar (sesuai tonton tanpa bunyi). VO: Gemini TTS (suara "Orus").

| Babak | Isi |
|---|---|
| Hook | "Apa ada DALAM tilam ni?" → tilam terburai |
| Lapisan 01 | Fabrik anti-statik & penyejuk (benang karbon + benang penyejuk) |
| Lapisan 02 | Topper boleh tukar (topper ditarik keluar & ganti baru) |
| Lapisan 03 | Latex asli 5 zon ketumpatan |
| Lapisan 04 | Foam berliang — aliran udara |
| Lapisan 05 | Pocket spring 7 zon — pasangan pusing tak terasa |
| Lapisan 06 | Sabut kelapa — sokongan padu, serap lembapan |
| Cantum | COWAY PRIME II · 33 cm · Queen & King |
| Harga | Sewa serendah RM139/bulan (Queen), King RM159 · servis tilam percuma 5 tahun · bawah RM5 semalam |
| CTA | Nak rasa sendiri? WhatsApp saya sekarang |

**Sahkan sebelum iklan:** harga sewa & promo semasa, dan susunan lapisan sebenar Prime II (susunan dalam video
ialah ilustrasi berdasarkan ciri yang diiklankan). Edit teks dalam `src/tilam/v16_prime2.html`
(objek `TEXT`, `BADGES`, blok `#pr` untuk harga).

### Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow
python tilam/vo/gemini_tts.py ...          # pilihan: jana VO baharu (lihat bawah)
python tilam/vo/split.py v16               # VO penuh -> baris + masa (tilam/vo/v16_timing.json)
python tilam/build_v16.py                  # render + muzik/SFX + gabung
python tilam/build_v16.py --stills 2,8,20  # pratonton PNG -> out/stills/
```
VO baharu: skrip dalam `tilam/vo/lines_v16.json`. Jana keseluruhan skrip dalam **satu** permintaan Gemini TTS
(kuota percuma ±10 permintaan/hari/model) ke `tilam/vo/v16_full.wav`, kemudian kemas kini anggaran masa setiap baris
dalam `tilam/vo/v16_asr.json` (transkrip Gemini) dan jalankan `split.py`.
Atau rakam suara sendiri sebagai `tilam/vo/v16_full.wav` (baca baris ikut turutan dengan jeda ±0.5s).
