# Coway Neo Plus — Versi Penuh (Portrait 1080×1920, ±2:51)

Konsep sama dengan `neoplus/` (60s), tetapi **setiap poin dalam skrip asal** ada suara dan babak sendiri:
hook → rasa serba salah → rumah sendiri vs kampung (masak air, tunggu panas, isi bekas) → nak bantu →
tak perlu canggih → moden vs manual → pulas tombol, tekan tuil → tak perlu LED / spek membaca → 3 suhu tersedia →
kopi, teh, susu → bajet mampu milik → kongsi bayar gilir-gilir → Coway Neo Plus → 3 suhu → keluarga kecil,
tangki tak perlu besar → cukup, mudah, praktikal → harga promosi → double promo → hantar & pasang percuma → CTA WhatsApp.

Suara: AI perempuan Bahasa Melayu.
> **Suara semasa:** Gemini TTS (`gemini-3.1-flash-tts-preview`, suara `Sulafat`), klip dalam `neoplus_full/clips/` (disimpan
> dalam repo supaya boleh bina semula tanpa guna kuota). Garis masa (`lines.json`, `lines.js`, SRT) dijana daripada tempoh klip sebenar, jadi video ±2:51.


## Skrip & babak
| Masa | Visual | VO |
|------|--------|----|
| 0:00.3 | Rumah kampung + PENAPIS AIR? | Mak ayah dah lama teringin nak ada penapis air dekat rumah? |
| 0:05.2 | Chat daripada Mak ♥ | Atau mungkin mak dekat kampung sendiri pernah cakap, |
| 0:09.7 | 〃 | Kalau ada penapis air dekat kampung, kan senang… |
| 0:15.0 | Peta bandar → kampung | Kita yang duduk jauh ni, kadang-kadang rasa serba salah. |
| 0:19.8 | Rumah sendiri: panas ✓ sejuk ✓ | Dekat rumah sendiri, air panas, air sejuk, semua dah ada. |
| 0:24.9 | Rumah mak ayah: masak air · tunggu panas · isi bekas | Tapi dekat rumah mak ayah di kampung, masih kena masak air, tunggu air panas, atau isi air dalam bekas macam biasa. |
| 0:34.1 | Kotak hadiah: nak bantu | Dah lama kita fikir nak bantu. Nak belikan penapis air untuk mak ayah. |
| 0:39.9 | ~~PALING CANGGIH~~ → PALING SENANG | Mak ayah tak perlukan produk paling canggih. Tapi apa yang paling senang untuk mak ayah guna. |
| 0:46.9 | Bagi kita: elektronik = MODEN | Sebab bagi kita, model yang banyak elektronik mungkin nampak lagi moden. |
| 0:52.0 | Bagi mak ayah: biasa MANUAL | Tapi bagi mak ayah, yang dah biasa dengan barang-barang manual… |
| 0:56.0 | Foto panel: ① pulas ② tekan ③ air keluar | Pulas tombol suhu, tekan tuil, terus keluar air. Itu yang lagi senang. |
| 1:01.7 | LED ⃠ | Tak perlu pening tengok nombor LED. |
| 1:04.8 | Mak cari spek membaca | Takkan nak ambil air pun, kena ambil spek membaca dulu? |
| 1:09.6 | Air panas · sejuk · biasa — TERSEDIA | Yang penting, air panas, air sejuk, dan air biasa, semuanya dah tersedia bila diperlukan. |
| 1:17.5 | Kopi? TEKAN. Teh? TEKAN. Susu? | Nak buat kopi? Tekan. Nak buat teh? Tekan. Nak bancuh susu? Air panas dah tersedia. |
| 1:25.5 | Tabung — BAJET MAMPU MILIK | Dan sebagai anak, kita pun kena fikir satu lagi benda. Bajet mampu milik. |
| 1:31.0 | Kongsi bayar: Kita → Abang → Adik | Sebab kalau adik-beradik nak kongsi bayar pun, boleh. |
| 1:34.3 | 〃 | Tahun ni kita bayar. Tahun depan, mungkin abang pula. Tahun seterusnya, adik pula. |
| 1:41.1 | GILIR-GILIR! | Gilir-gilir. Jadi tak terasa sangat membebankan seorang. |
| 1:47.0 | Pendedahan Coway Neo Plus | Kalau untuk mak ayah dekat kampung, salah satu model yang boleh dipertimbangkan ialah, Coway Neo Plus. |
| 1:54.5 | 3 cip suhu | Ada tiga suhu air. Panas, sejuk, dan suhu bilik. |
| 1:59.2 | Saiz keluarga kecil | Saiz pun sesuai untuk keluarga kecil. |
| 2:01.8 | Ayah + Mak (+ adik?) · tangki besar ✗ | Kalau dekat rumah mak ayah cuma dua orang, atau ada adik yang masih tinggal bersama, tak lah perlukan model dengan tangki yang terlalu besar. |
| 2:10.3 | Cukup. Mudah. Praktikal. | Yang penting, cukup, mudah, dan praktikal untuk kegunaan harian. |
| 2:15.5 | HARGA PROMOSI | Dan sekarang, Neo Plus ni ada harga promosi. |
| 2:18.8 | RM59/bulan · ~~RM104~~ · JIMAT RM45 | Serendah lima puluh sembilan ringgit sebulan. Jimat empat puluh lima ringgit, dari harga asal seratus empat ringgit. |
| 2:26.3 | DOUBLE PROMO: 7 bulan pertama RM20/bulan | Dan ada double promo. Tujuh bulan pertama, cuma dua puluh ringgit sebulan! |
| 2:32.3 | Penghantaran & pemasangan PERCUMA | Penghantaran dan pemasangan pun percuma. |
| 2:35.9 | Foto pemasangan sebenar | Jadi kalau memang dah lama terfikir nak belikan penapis air untuk mak ayah… |
| 2:41.7 | Hidup lebih mudah | mungkin sekarang, masa yang sesuai untuk buatkan hidup mereka sedikit lebih mudah. |
| 2:46.4 | Butang WhatsApp | Klik WhatsApp sekarang, untuk tanya detail. |

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
python voiceover/generate_vo_gemini.py --lines neoplus_full/lines.json --clips neoplus_full/clips --batch 7   # 7 baris/permintaan
python neoplus_full/timeline.py --clips neoplus_full/clips      # slot = tempoh klip sebenar
python render.py --page neoplus_full/index.html --out out/neoplus_full_video_noaudio.mp4 --workers 4
python neoplus_full/audio.py
python mix.py --project neoplus_full
```
`--voice Kore` / `Aoede` / `Leda` untuk tukar suara, `--style "..."` untuk tukar gaya bacaan,
`--only 03,11` untuk jana semula baris tertentu, `--list` untuk lihat model TTS yang ada.
Kuota percuma: 10 permintaan sehari bagi setiap model, jadi guna `--batch` (beberapa baris dalam satu permintaan,
dipotong pada jeda) dan `--missing` untuk isi baris yang belum ada sahaja.

