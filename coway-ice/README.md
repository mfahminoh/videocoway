# Coway Ice — Video Iklan Meta "Family Kaki Ais" (Portrait 1080×1920, ±38s)

Motion graphic ikut skrip: keluarga kaki ais → Pagi/Tengah hari/Petang/Malam → **Coway Ice** →
ais sentiasa ready (700g) → ais baru setiap 15 minit → promo RM20 × 7 bulan → CTA WhatsApp.

**Video siap:** `out/coway_ice_final.mp4` (H.264, 30fps, voiceover Gemini TTS + muzik + SFX ais asli).

Voiceover: `voiceover/gemini_tts_full.wav` (satu rakaman 48s) dipotong ikut baris oleh `voiceover/split_vo.py`,
jeda panjang dipendekkan dan dilajukan 1.18× → `voiceover/clips/01–10.wav`. Masa babak dalam
`src/timeline.js` diselaraskan dengan setiap baris (`voiceover/lines.json`).

## Pelan babak

| Masa | Babak | Visual | Teks atas skrin |
|------|-------|--------|-----------------|
| 0 – 3.8s | 1 · Hook | Animasi keluarga di meja makan; teh ais, kopi ais, air kosong berais berlaga *clink clink* | AIR SEJUK TAK CUKUP. / MESTI ADA AIS! 🧊 |
| 3.8 – 7.95s | 2 · Relatable | Kad Pagi 🍳 teh ais · Tengah hari 🍛 kopi ais · Petang 🍩 sirap ais · Malam 🌙 air kosong berais (ikut sebutan VO) | PAGI 🧊 → TENGAH HARI 🧊 → PETANG 🧊 |
| 7.95 – 13.4s | 3 · Transition | 4 gelas masuk satu frame → Coway Ice muncul | COWAY ICE ❄️ |
| 13.4 – 17.15s | 4a · Ice ready | Footage ais jatuh ke gelas (slow-mo) | AIS SENTIASA READY 🧊 |
| 17.15 – 20.6s | 4b · 700g | Ruang simpanan ais penuh, meter 0g → 700g | SEHINGGA 700g AIS |
| 20.6 – 24.9s | 5a · 15 minit | Pemasa 15:00 → 00:00 → ais baru jatuh | AIS BARU SETIAP 15 MINIT |
| 24.9 – 27.35s | 5b · Fresh | Footage ais keluar dari muncung | FRESH ICE, BILA-BILA MASA. 🧊 |
| 27.35 – 34.5s | 6a · Offer | Hero produk, LAST CALL, RM20 berdenyut, bar "promo dah nak habis" | 🔥 LAST CALL! · RM20 / BULAN · SELAMA 7 BULAN · HANTAR & PASANG PERCUMA 🇲🇾 |
| 34.5 – 38.4s | 6b · CTA | Produk + butang WhatsApp berdenyut, jari 👆 menekan | 🧊 COWAY ICE · tagline · KLIK WHATSAPP SEKARANG |

**Warna (ikut Coway):** navy `#0B2F6B`, biru Coway `#0B4DA2`, biru langit `#2EA7E0`, ais `#DFF3FF`;
kuning `#FFD23F` untuk harga, merah `#E5322D` untuk LAST CALL, hijau WhatsApp `#25D366`. Font: Poppins.

**Footage rujukan:** video AIS_2 & AIS_3 ada kapsyen terbakar di jalur ~20–33% tinggi frame, jadi
`prep.py` hanya ambil bahagian **bawah** jalur itu (crop 720×840 dari y=440) dan buang audio asal.
Semua teks & VO dalam video ini ikut skrip anda sahaja.

**Nota Meta Ads:** teks penting diletak dalam zon y 180–1450 supaya tak ditutup UI Reels/Stories di bawah.
Durasi ~38s kerana rakaman VO 48s; dilajukan 1.18× supaya suara masih jelas dan semula jadi.

## Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow
python prep.py            # ekstrak bingkai footage (assets/clips -> build/frames)
python render.py          # animasi (src/index.html) -> out/coway_ice_video_noaudio.mp4
python audio.py           # muzik + SFX -> out/music_sfx.wav
python voiceover/split_vo.py   # potong gemini_tts_full.wav -> voiceover/clips/*.wav
python mix.py             # gabung video + muzik/SFX + voiceover -> out/coway_ice_final.mp4
```
Pratonton bingkai: `python render.py --stills 1,5.5,12`. Edit teks/harga terus dalam `src/index.html`;
masa babak dalam `src/timeline.js` (animasi & audio.py baca fail yang sama). Potong semula klip dari video asal: `python prep.py --ais2 AIS_2.mp4 --ais3 AIS_3.mp4`.
