# 10 Video Coway Neon (NE01–NE10) + bonus E04

Fail video ada dalam folder ni (`out/`), sama seperti video Villaem 3 (`villaem3_final.mp4`, `V05_final.mp4`).

Semua video portrait 1080×1920, 30 fps, 31–40 saat. Suara dijana dengan Gemini TTS, muzik & SFX dijana sendiri (tiada lesen pihak ketiga).
Aset yang digunakan: klip Neon anda (`assets/clips/neon/`), gambar rasmi Neon (`assets/img/neon/`).
Skrip & storyboard ada dalam [`videos/neon_batch.py`](../../videos/neon_batch.py). Untuk ubah teks atau harga: edit fail tu, kemudian
`python videos/neon_batch.py && python videos/build_video.py NE0X --tts --render`.

| Fail | Tajuk / hook | Gaya | Suara | Saat | Rujukan |
|---|---|---|---|---|---|
| `NE01_bajet-kecil-tak-boleh-cantik.mp4` | "Siapa kata bajet kecil tak boleh cantik?" | Cerita + 5 warna + harga | Aoede (P) | 36.3 | R04 |
| `NE02_baru-kahwin-rumah-pertama.mp4` | "Baru kahwin? Ini yang saya selalu cadangkan" | Cerita + kapasiti | Aoede (P) | 38.6 | R05 |
| `NE03_pakej-self-service.mp4` | "Satu benda best: pakej self-service" | Presenter + 4 langkah + penghantaran filter | Orus (L) | 33.0 | R03 |
| `NE04_kos-sehari-coway-neon.mp4` | "Berapa kos Coway Neon sehari?" | Infografik (RM104 → RM54 → RM1.80 → ≈RM1.13 sehari) | Orus (L) | 35.8 | R04 |
| `NE05_pukul-3-pagi-bancuh-susu.mp4` | "Pukul 3 pagi. Baby menangis." | Cerita klip bayi | Aoede (P) | 40.0 | klip anda |
| `NE06_coway-semua-ro-ke.mp4` | "Coway semua RO ke?" | Mitos vs fakta (RO vs Nanotrap) | Aoede (P) | 34.6 | R06 (Threads) |
| `NE07_kuiz-warna-dapur.mp4` | "Kuiz 10 saat! Dapur you warna apa?" | Kuiz A–E + 5 warna | Aoede (P) | 33.6 | Plan E02 |
| `NE08_logam-berat-paip-lama.mp4` | "Rumah lama, paip lama?" | Edukasi (Hg, Pb, Fe, Al) | Orus (L) | 31.1 | Plan E03 |
| `NE09_3-tanda-neon-sesuai.mp4` | "3 tanda Coway Neon sesuai untuk rumah you" | Listicle + zoom Hot Lock | Orus (L) | 34.4 | R02 |
| `NE10_proses-pasang-4-langkah.mp4` | "Tak tahu proses pasang? Senang je." | 4 langkah | Orus (L) | 35.8 | — |
| `E04_3-sebab-ramai-pasang.mp4` *(bonus)* | "Kenapa ramai pasang Coway Neon? 3 sebab" | Listicle + klip + gambar | Orus (L) | 40.1 | R02 |

## Semak sebelum guna untuk iklan

1. **Harga (dikemas kini 29/9):** harga asal **RM104**/bulan → promosi **RM54**/bulan (tanpa sebut %), ditambah **rebat ulang tahun Coway RM20 × 7 bulan**. NE04 mengira ≈RM1.13 sehari untuk 7 bulan pertama, iaitu (RM54 − RM20) ÷ 30. Kiraan ni menganggap rebat ditolak terus dari bil bulanan, jadi sahkan dulu.
2. **Kapasiti NE02:** tangki panas 1L, sejuk 1.5L, suhu bilik *direct flow*. Diambil dari R05.
3. **Self-service:** filter dihantar percuma setiap 8 bulan (dari R02/R03). Dipakai dalam NE03, NE09 dan NE10.
4. **Nanotrap:** dakwaan "tapis logam berat (merkuri, plumbum, besi, aluminium), bakteria & virus" diambil dari laman Coway Neon. Dipakai dalam NE06 dan NE08.
5. **Sebutan:** "Coway" kadang-kadang disebut "Ko-wei"/"Kawi", dan "Villaem" disebut "Vila-em". Tolong dengar NE02 dan NE06.
6. **NE05 (susu bayi):** video ni sengaja tak nyatakan suhu untuk susu. Ia cuma sebut "ikut nasihat doktor".
7. **NE08 & NE06:** masa kapsyen NE08 dibetulkan secara manual, dan NE06 sedikit. Tolong semak kapsyen selari dengan suara.
