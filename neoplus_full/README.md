# Coway Neo Plus — Versi Penuh (Portrait 1080×1920, ±2:34)

Konsep sama dengan `neoplus/` (60s), tetapi **setiap poin dalam skrip asal** ada suara dan babak sendiri:
hook → rasa serba salah → rumah sendiri vs kampung (masak air, tunggu panas, isi bekas) → nak bantu →
tak perlu canggih → moden vs manual → pulas tombol, tekan tuil → tak perlu LED / spek membaca → 3 suhu tersedia →
kopi, teh, susu → bajet mampu milik → kongsi bayar gilir-gilir → Coway Neo Plus → 3 suhu → keluarga kecil,
tangki tak perlu besar → cukup, mudah, praktikal → harga promosi → double promo → hantar & pasang percuma → CTA WhatsApp.

Suara: AI perempuan Bahasa Melayu (`ms-MY-YasminNeural`).

## Skrip & babak
| Masa | Visual | VO |
|------|--------|----|
| 0:00.3 | Rumah kampung + PENAPIS AIR? | Mak ayah dah lama teringin nak ada penapis air dekat rumah? |
| 0:04.2 | Chat daripada Mak ♥ | Atau mungkin mak dekat kampung sendiri pernah cakap, |
| 0:07.8 | 〃 | Kalau ada penapis air dekat kampung, kan senang… |
| 0:11.6 | Peta bandar → kampung | Kita yang duduk jauh ni, kadang-kadang rasa serba salah. |
| 0:15.4 | Rumah sendiri: panas ✓ sejuk ✓ | Dekat rumah sendiri, air panas, air sejuk, semua dah ada. |
| 0:19.6 | Rumah mak ayah: masak air · tunggu panas · isi bekas | Tapi dekat rumah mak ayah di kampung, masih kena masak air, tunggu air panas, atau isi air dalam bekas macam biasa. |
| 0:27.2 | Kotak hadiah: nak bantu | Dah lama kita fikir nak bantu. Nak belikan penapis air untuk mak ayah. |
| 0:32.4 | ~~PALING CANGGIH~~ → PALING SENANG | Mak ayah tak perlukan produk paling canggih. Tapi apa yang paling senang untuk mak ayah guna. |
| 0:38.8 | Bagi kita: elektronik = MODEN | Sebab bagi kita, model yang banyak elektronik mungkin nampak lagi moden. |
| 0:43.6 | Bagi mak ayah: biasa MANUAL | Tapi bagi mak ayah, yang dah biasa dengan barang-barang manual… |
| 0:47.9 | Foto panel: ① pulas ② tekan ③ air keluar | Pulas tombol suhu, tekan tuil, terus keluar air. Itu yang lagi senang. |
| 0:53.1 | LED ⃠ | Tak perlu pening tengok nombor LED. |
| 0:55.5 | Mak cari spek membaca | Takkan nak ambil air pun, kena ambil spek membaca dulu? |
| 0:59.5 | Air panas · sejuk · biasa — TERSEDIA | Yang penting, air panas, air sejuk, dan air biasa, semuanya dah tersedia bila diperlukan. |
| 1:05.8 | Kopi? TEKAN. Teh? TEKAN. Susu? | Nak buat kopi? Tekan. Nak buat teh? Tekan. Nak bancuh susu? Air panas dah tersedia. |
| 1:13.1 | Tabung — BAJET MAMPU MILIK | Dan sebagai anak, kita pun kena fikir satu lagi benda. Bajet mampu milik. |
| 1:18.3 | Kongsi bayar: Kita → Abang → Adik | Sebab kalau adik-beradik nak kongsi bayar pun, boleh. |
| 1:22.0 | 〃 | Tahun ni kita bayar. Tahun depan, mungkin abang pula. Tahun seterusnya, adik pula. |
| 1:28.3 | GILIR-GILIR! | Gilir-gilir. Jadi tak terasa sangat membebankan seorang. |
| 1:32.8 | Pendedahan Coway Neo Plus | Kalau untuk mak ayah dekat kampung, salah satu model yang boleh dipertimbangkan ialah, Coway Neo Plus. |
| 1:39.5 | 3 cip suhu | Ada tiga suhu air. Panas, sejuk, dan suhu bilik. |
| 1:43.4 | Saiz keluarga kecil | Saiz pun sesuai untuk keluarga kecil. |
| 1:46.0 | Ayah + Mak (+ adik?) · tangki besar ✗ | Kalau dekat rumah mak ayah cuma dua orang, atau ada adik yang masih tinggal bersama, tak lah perlukan model dengan tangki yang terlalu besar. |
| 1:55.2 | Cukup. Mudah. Praktikal. | Yang penting, cukup, mudah, dan praktikal untuk kegunaan harian. |
| 2:00.0 | HARGA PROMOSI | Dan sekarang, Neo Plus ni ada harga promosi. |
| 2:03.2 | RM59/bulan · ~~RM104~~ · JIMAT RM45 | Serendah lima puluh sembilan ringgit sebulan. Jimat empat puluh lima ringgit, dari harga asal seratus empat ringgit. |
| 2:11.1 | DOUBLE PROMO: 7 bulan pertama RM20/bulan | Dan ada double promo. Tujuh bulan pertama, cuma dua puluh ringgit sebulan! |
| 2:16.3 | Penghantaran & pemasangan PERCUMA | Penghantaran dan pemasangan pun percuma. |
| 2:19.4 | Foto pemasangan sebenar | Jadi kalau memang dah lama terfikir nak belikan penapis air untuk mak ayah… |
| 2:24.3 | Hidup lebih mudah | mungkin sekarang, masa yang sesuai untuk buatkan hidup mereka sedikit lebih mudah. |
| 2:29.8 | Butang WhatsApp | Klik WhatsApp sekarang, untuk tanya detail. |

## Cara ia disegerakkan
Skrip hanya ada di satu tempat: `timeline.py`. Ia menganggar tempoh setiap baris dan menulis `lines.json`
(untuk suara & campuran), `lines.js` (untuk animasi) dan `neoplus_full.srt`. Animasi dan SFX guna
`at(baris, 'perkataan')` untuk muncul tepat bila perkataan itu disebut. Jadi jika skrip diubah:
jalankan semula `timeline.py`, dan semua masa akan ikut.

## Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow edge-tts
python neoplus_full/timeline.py                                  # jika skrip diubah
python render.py --page neoplus_full/index.html --out out/neoplus_full_video_noaudio.mp4 --workers 4
python neoplus_full/audio.py                                     # muzik + SFX
python voiceover/generate_vo.py --lines neoplus_full/lines.json --clips neoplus_full/clips --voice ms-MY-YasminNeural
python mix.py --project neoplus_full                             # -> out/neoplus_full_final.mp4
```

## Suara dengan Gemini TTS (alternatif kepada edge-tts)
Perlu `GEMINI_API_KEY` (Google AI Studio). Video versi penuh akan **ikut tempoh suara sebenar**:
```
python voiceover/generate_vo_gemini.py --lines neoplus_full/lines.json --clips neoplus_full/clips   # suara lalai: Sulafat
python neoplus_full/timeline.py --clips neoplus_full/clips      # slot = tempoh klip sebenar
python render.py --page neoplus_full/index.html --out out/neoplus_full_video_noaudio.mp4 --workers 4
python neoplus_full/audio.py
python mix.py --project neoplus_full
```
`--voice Kore` / `Aoede` / `Leda` untuk tukar suara, `--style "..."` untuk tukar gaya bacaan,
`--only 03,11` untuk jana semula baris tertentu, `--list` untuk lihat model TTS yang ada.

