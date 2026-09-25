# Skrip Voiceover — Coway Ice (±31 saat)

Gaya: mesra, santai, macam kawan bagi tips — tempo agak laju, senyum dalam suara.
Masa ikut video (`lines.json` / `coway_ice.srt`).

| # | Masa | Visual | Skrip |
|---|------|--------|-------|
| 01 | 0.2 – 3.8 | Keluarga di meja makan, gelas berlaga *clink* | Family anda jenis… air mesti ada ais baru puas? |
| 02 | 4.0 – 7.9 | Montaj Pagi → Tengah hari → Petang → Malam | Pagi sarapan nak teh ais. Tengah hari kopi ais. Petang pun nak air ais. |
| 03 | 8.0 – 11.0 | Semua gelas masuk satu frame → COWAY ICE | Kalau family memang kaki ais, dan anda nak pasang penapis air… model Ice memang patut masuk dalam pilihan. |
| 04 | 11.1 – 13.3 | Footage ais jatuh dalam gelas | Sebab Coway Ice bukan sekadar bagi air sejuk. Ais pun memang dah ready. |
| 05 | 13.4 – 16.9 | Grafik ruang simpanan penuh, 0g → 700g | Ruang simpanan ais boleh menyimpan sehingga 700 gram ais. |
| 06 | 17.0 – 20.3 | Pemasa 15:00 → 00:00, ais baru jatuh | Dan paling best, mesin ni akan terus hasilkan ais baru setiap 15 minit. |
| 07 | 20.4 – 22.9 | Footage ais keluar dari mesin | Jadi anda sentiasa ada bekalan ais yang fresh. |
| 08 | 23.0 – 25.2 | LAST CALL, RM20/BULAN, 7 bulan | Dan sekarang, Coway Ice ada promosi RM20 untuk 7 bulan. |
| 09 | 25.3 – 27.5 | Hantar & pasang percuma 🇲🇾, bar masa menyusut | Promo ni dah nak habis. Penghantaran dan pemasangan percuma seluruh Malaysia. |
| 10 | 27.7 – 30.8 | Skrin akhir + butang WhatsApp | Kalau family anda memang kaki ais, klik WhatsApp sekarang. |

> Baris 03 agak panjang untuk slot 3 saat — bila rakam, laju sedikit atau biar ia melimpah ~0.5s ke babak 4 (tiada teks bertindih).

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
