# Skrip Voiceover — 3 Model Coway Paling Laris (±30 saat)

Gaya: lelaki/perempuan Melayu, santai macam content creator, tempo laju tapi jelas.
Sasaran: orang yang tengah plan nak pasang Coway.

| # | Masa | Visual | Skrip |
|---|------|--------|-------|
| 01 | 0.2 – 3.8 | "Tengah plan nak PASANG COWAY?" + 3 produk jatuh | Tengah plan nak pasang Coway? Ni tiga model paling laris tahun ni. |
| 02 | 4.1 – 9.5 | Video Neon: tekan butang, air ke botol susu. MAMPU MILIK, "Lengkap 3 SUHU" | Pertama, Coway Neon. Model mampu milik, tapi lengkap tiga suhu. |
| 03 | 9.9 – 16.1 | Video: tekan butang suhu (40→60) → tangki UV → presenter. MODEL PREMIUM, GENERASI 3, panel ✓ | Kedua, Villaem 3. Model premium, generasi ketiga. Banyak pilihan suhu, ada air suam. Tangki paling besar. Senang guna, memang pilihan ramai! |
| 04 | 16.4 – 22.0 | Video Ais: ais jatuh ke gelas → tuang kopi ais. PALING SPECIAL, panel Pagi/Petang/Malam | Ketiga, Coway Ais. Paling special, sebab dia keluar ais! Family suka minum ais pagi, petang, malam? Ni lah model dia. |
| 05 | 22.3 – 27.6 | PROMO SEMUA MODEL · RM20 JE · Rebate RM20 × 7 bulan · percuma | Sekarang semua model tengah promo! RM20 je dah boleh pasang. Rebate dua puluh ringgit, tujuh bulan. Hantar dan pasang percuma, seluruh Malaysia! |
| 06 | 27.9 – 29.9 | 3 produk + butang WhatsApp | Nak yang mana satu? WhatsApp saya sekarang! |

Sari kata: `best3.srt` (boleh muat naik terus ke Meta sebagai kapsyen).

## Cara masukkan suara

**Pilihan A — rakam suara sendiri:** rakam setiap baris sebagai
`voiceover/best3/clips/01.mp3` … `06.mp3` (atau `.wav`), mula bercakap terus (tanpa senyap panjang di depan),
kemudian jalankan `python mix.py --ad best3`.

**Pilihan B — suara AI (perlu internet):**
```
pip install edge-tts imageio-ffmpeg
python voiceover/generate_vo.py --ad best3
python mix.py --ad best3
```
