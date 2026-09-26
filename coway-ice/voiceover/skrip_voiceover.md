# Skrip Voiceover — Coway Ice (±38 saat)

> Versi dalam video: Gemini TTS (`gemini_tts_full.wav`), dipotong & dilajukan 1.18× oleh `split_vo.py`.
> Masa terkini: `lines.json` / `coway_ice.srt`.

Gaya: mesra, santai, macam kawan bagi tips — tempo agak laju, senyum dalam suara.
Masa ikut video (`lines.json` / `coway_ice.srt`).

| # | Masa | Visual | Skrip |
|---|------|--------|-------|
| 01 | 0.15 – 3.61 | Keluarga di meja makan, gelas berlaga *clink* | Family anda jenis… air mesti ada ais baru puas? |
| 02 | 3.9 – 7.74 | Montaj Pagi → Tengah hari → Petang → Malam | Pagi sarapan nak teh ais. Tengah hari kopi ais. Petang pun nak air ais. |
| 03 | 8.0 – 13.21 | Semua gelas masuk satu frame → COWAY ICE | Kalau family memang kaki ais, dan anda nak pasang penapis air… model Ice memang patut masuk dalam pilihan. |
| 04 | 13.5 – 16.97 | Footage ais jatuh dalam gelas | Sebab Coway Ice bukan sekadar bagi air sejuk. Ais pun memang dah ready. |
| 05 | 17.25 – 20.42 | Grafik ruang simpanan penuh, 0g → 700g | Ruang simpanan ais boleh menyimpan sehingga 700 gram ais. |
| 06 | 20.7 – 24.75 | Pemasa 15:00 → 00:00, ais baru jatuh | Dan paling best, mesin ni akan terus hasilkan ais baru setiap 15 minit. |
| 07 | 25.0 – 27.17 | Footage ais keluar dari mesin | Jadi anda sentiasa ada bekalan ais yang fresh. |
| 08 | 27.45 – 30.75 | LAST CALL, RM20/BULAN, 7 bulan | Dan sekarang, Coway Ice ada promosi RM20 untuk 7 bulan. |
| 09 | 31.0 – 34.38 | Hantar & pasang percuma 🇲🇾, bar masa menyusut | Promo ni dah nak habis. Penghantaran dan pemasangan percuma seluruh Malaysia. |
| 10 | 34.65 – 37.46 | Skrin akhir + butang WhatsApp | Kalau family anda memang kaki ais, klik WhatsApp sekarang. |


## Cara masukkan suara

**A — rakam suara sendiri (paling "real" untuk Meta Ads):** rakam setiap baris sebagai
`voiceover/clips/01.mp3` … `10.mp3` (atau `.wav`), kemudian `python mix.py`.

**B — suara AI Bahasa Melayu (Microsoft Edge, percuma, perlu internet):**
```
pip install edge-tts imageio-ffmpeg numpy
python voiceover/generate_vo.py
python mix.py
```

**C — CapCut:** import `out/coway_ice_final.mp4`, guna Text-to-Speech Bahasa Melayu dan letak setiap
baris ikut masa di atas. `coway_ice.srt` boleh diimport terus sebagai rujukan masa.
