# Skrip Voiceover — Coway Villaem 3 (±29 saat)

Gaya: lelaki Melayu, santai macam content creator, bercerita — bukan nada "iklan TV".
Tempo agak laju tapi jelas. Senyum sikit bila bercakap (dengar dalam suara).

| # | Masa | Visual | Skrip |
|---|------|--------|-------|
| 01 | 0.2 – 3.9 | "3 TAHUN jual Coway" + customer muncul | Tiga tahun saya jual Coway, saya perasan ada satu jenis customer ni. |
| 02 | 4.1 – 8.3 | "beli banyak kali" dipotong → TAHAN LAMA & PUAS HATI | Diorang tak suka beli banyak kali. Sekali beli, nak yang *tahan lama*, dan *puas hati*. |
| 03 | 8.6 – 11.2 | Produk muncul, "Villaem 3" | Dan kebanyakan diorang… pilih **Coway Villaem 3**. |
| 04 | 11.4 – 13.7 | HIGH SPEC, tangki penuh | Spec tinggi, tangki paling besar. |
| 05 | 13.8 – 17.5 | 8+ pilihan suhu, chip Panas/Suam/Bilik/Sejuk | Lebih lapan pilihan suhu. Panas nak masak, suam, suhu bilik, sejuk — semua ada. |
| 06 | 17.6 – 19.7 | Perisai "TAHAN LASAK" | Paling tahan lasak. Technician pun jarang dapat repair! |
| 07 | 19.8 – 25.9 | Promo RM20 × 7 bulan, RM84/bulan | Sekarang ada promo! Rebate dua puluh ringgit, tujuh bulan. Serendah lapan puluh empat ringgit sebulan. Pemasangan percuma, servis setiap dua atau empat bulan. |
| 08 | 26.0 – 29.4 | "Sekali beli. Puas hati." + butang WhatsApp | Kalau you jenis nak sekali beli, puas hati — Villaem 3 untuk you. WhatsApp saya sekarang! |

## Cara masukkan suara

**Pilihan A — rakam suara sendiri (paling "real" untuk iklan Meta):**
Rakam setiap baris sebagai `voiceover/clips/01.mp3` … `08.mp3` (atau `.wav`), kemudian `python mix.py`.

**Pilihan B — suara AI lelaki Melayu (Microsoft "Osman", percuma):**
```
pip install edge-tts imageio-ffmpeg numpy
python voiceover/generate_vo.py
python mix.py
```

**Pilihan C — CapCut:** import `out/villaem3_final.mp4`, guna Text-to-Speech Bahasa Melayu
(suara lelaki), dan letak setiap baris ikut masa dalam jadual di atas. Fail `villaem3.srt`
boleh diimport terus sebagai kapsyen/rujukan masa.
