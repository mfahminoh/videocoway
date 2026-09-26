# Coway Neo Plus — "Untuk Mak Ayah di Kampung" (Portrait 1080×1920, 60s)

Motion graphic bercerita dari sudut anak yang duduk jauh: mak teringin penapis air → rumah kita vs kampung
→ tak perlu canggih, cukup senang guna (pulas tombol, tekan tuil) → kongsi bayar adik-beradik → **Coway Neo Plus**
→ double promo → CTA butang WhatsApp.

Suara: AI perempuan Bahasa Melayu (`ms-MY-YasminNeural`, Microsoft Edge TTS, percuma).

## Babak
| Masa | Babak | VO |
|------|-------|----|
| 0 – 3.2s | Rumah kampung + "PENAPIS AIR?" | Mak ayah dah lama teringin nak ada penapis air? |
| 3.2 – 7.6s | Chat daripada Mak ♥ | Atau mak pernah cakap, kalau ada penapis air dekat kampung, kan senang… |
| 7.6 – 10.4s | Peta bandar → kampung | Kita yang duduk jauh ni, rasa serba salah. |
| 10.4 – 15.5s | Rumah kita VS rumah mak ayah (cerek, jam) | Rumah kita, air panas sejuk semua ada. Tapi di kampung, mak masih masak air. |
| 15.5 – 20.4s | ~~PALING CANGGIH~~ → PALING SENANG guna | Mak ayah tak perlukan yang paling canggih. Cukup yang paling senang guna. |
| 20.4 – 25.2s | Foto panel: ① pulas tombol ② tekan tuil ③ air keluar · LED ⃠ | Pulas tombol, tekan tuil, terus keluar air. Tak payah tengok nombor LED. |
| 25.2 – 28.2s | Mak pegang spek | Takkan nak ambil air pun, kena cari spek dulu? |
| 28.2 – 33.8s | Kopi? TEKAN. Teh? TEKAN. Susu? | Nak buat kopi? Tekan. Teh? Tekan. Susu? Air panas dah sedia. |
| 33.8 – 39.7s | Bajet mampu milik: Kita → Abang → Adik, GILIR-GILIR | Kongsi bayar pun boleh. Tahun ni kita, tahun depan abang, lepas tu adik. Gilir-gilir. |
| 39.7 – 45.3s | Pendedahan Coway Neo Plus + 3 suhu | Pilihan yang sesuai, Coway Neo Plus. Tiga suhu air, saiz padat untuk keluarga kecil. |
| 45.3 – 53.8s | DOUBLE PROMO: ~~RM104~~ → RM59/bulan · 7 bulan pertama RM20/bulan · hantar & pasang percuma | Sekarang double promo! … |
| 53.8 – 60s | Foto pemasangan sebenar + butang WhatsApp | Masa yang sesuai untuk mudahkan hidup mak ayah. Klik WhatsApp sekarang! |

Harga & teks promo boleh diubah terus dalam `index.html` (cari `RM104`, `RM59`, `RM20`, `JIMAT RM45`).
Sarikata untuk dimuat naik ke Meta: `neoplus.srt`.

## Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow edge-tts
python render.py --page neoplus/index.html --out out/neoplus_video_noaudio.mp4   # animasi
python neoplus/audio.py                                                          # muzik + SFX
python voiceover/generate_vo.py --lines neoplus/lines.json --clips neoplus/clips --voice ms-MY-YasminNeural
python mix.py --project neoplus                                                  # -> out/neoplus_final.mp4
```
`generate_vo.py` perlukan internet (speech.platform.bing.com). Jika satu baris terlalu panjang untuk slotnya,
ia dijana semula sedikit laju supaya muat. Boleh juga rakam suara sendiri sebagai `neoplus/clips/01.mp3` … `12.mp3`.
