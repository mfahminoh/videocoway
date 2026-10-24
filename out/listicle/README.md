# 3 Video Listicle Coway Neon (Template A "3 Sebab")

Portrait 1080×1920, 26–28 saat. Suara Gemini TTS (3.8-flash-tts), dicepatkan 1.1× (atempo), muzik & SFX dijana sendiri.
Rujukan: dokumen "Framework Iklan Video Listicle — Coway Neon".

| Fail | Hook | Suara |
|---|---|---|
| `NL01_3-sebab-ramai-pilih-neon.mp4` | 3 sebab kenapa ramai pilih Coway Neon (5 warna · 3 suhu · harga) | Orus (L) |
| `NL02_ada-anak-kecil-3-sebab-neon.mp4` | Ada anak kecil kat rumah? (kunci keselamatan · bancuh susu · filter/technician) | Aoede (P) |
| `NL03_dapur-kecil-3-sebab-neon.mp4` | Dapur kecil / rumah sewa? (kompak · paip & dulang · bayar bulanan) | Puck (L) |

Harga: asal RM104 → promosi RM54/bulan + rebat ulang tahun RM20 × 7 bulan (disahkan 15/10).

Masa baris (`videos/NL0x/segments.json`) dipadankan pada jeda dalam suara berpandukan transkrip Gemini
(`transcript.json`), sebab `voiceover/align.py` tersilap untuk NL01/NL02. Bina semula visual + audio:
`python3 videos/build_video.py NL01 --no-align --render`.
