# Coway Ice — Video Iklan Meta "Family Kaki Ais" (Portrait 1080×1920, ±31s)

Motion graphic ikut skrip: keluarga kaki ais → Pagi/Tengah hari/Petang/Malam → **Coway Ice** →
ais sentiasa ready (700g) → ais baru setiap 15 minit → promo RM20 × 7 bulan → CTA WhatsApp.

**Video siap:** `out/coway_ice_final.mp4` (H.264, 30fps, muzik + SFX ais asli, tanpa lesen pihak ketiga).
Voiceover belum dimasukkan — lihat `voiceover/skrip_voiceover.md`.

## Pelan babak

| Masa | Babak | Visual | Teks atas skrin |
|------|-------|--------|-----------------|
| 0 – 4s | 1 · Hook | Animasi keluarga (ayah, ibu bertudung, 2 anak) di meja makan; teh ais, kopi ais, air kosong berais jatuh atas meja & berlaga *clink clink* | AIR SEJUK TAK CUKUP. / MESTI ADA AIS! 🧊 |
| 4 – 8s | 2 · Relatable | Montaj pantas 4 kad (whip-pan): Pagi 🍳 teh ais · Tengah hari 🍛 kopi ais · Petang 🍩 sirap ais · Malam 🌙 air kosong berais | PAGI 🧊 → TENGAH HARI 🧊 → PETANG 🧊 (muncul satu-satu) |
| 8 – 11s | 3 · Transition | 4 gelas terbang masuk satu frame → kilat → Coway Ice naik di tengah, gelas berkumpul di kaki produk | COWAY ICE ❄️ |
| 11 – 13.4s | 4a · Ice ready | Footage sebenar ais jatuh ke gelas (dari video rujukan, teks lama dipotong) | AIS SENTIASA READY 🧊 |
| 13.4 – 17s | 4b · 700g | Grafik ruang simpanan ais: 48 kiub jatuh & bertimbun, meter 0g → 700g, kilauan bila penuh | SEHINGGA 700g AIS |
| 17 – 20.4s | 5a · 15 minit | Pemasa 15:00 → 14:59 → laju ke 00:00 → *ding* → ais baru jatuh ke storan | AIS BARU SETIAP 15 MINIT |
| 20.4 – 23s | 5b · Fresh | Footage sebenar ais keluar dari muncung ke gelas | FRESH ICE, BILA-BILA MASA. 🧊 |
| 23 – 27.6s | 6a · Offer | Hero shot produk, lencana LAST CALL bergoyang, RM20 berdenyut, bar "promo dah nak habis" menyusut | 🔥 LAST CALL! · RM20 / BULAN · SELAMA 7 BULAN · HANTAR & PASANG PERCUMA 🇲🇾 |
| 27.6 – 31s | 6b · CTA | Produk + butang WhatsApp berdenyut, jari 👆 menekan | 🧊 COWAY ICE · Untuk family yang memang tak boleh hidup tanpa ais. · KLIK WHATSAPP SEKARANG |

**Warna (ikut Coway):** navy `#0B2F6B`, biru Coway `#0B4DA2`, biru langit `#2EA7E0`, ais `#DFF3FF`;
kuning `#FFD23F` untuk harga, merah `#E5322D` untuk LAST CALL, hijau WhatsApp `#25D366`. Font: Poppins.

**Footage rujukan:** video AIS_2 & AIS_3 ada kapsyen terbakar di jalur ~20–33% tinggi frame, jadi
`prep.py` hanya ambil bahagian **bawah** jalur itu (crop 720×840 dari y=440) dan buang audio asal.
Semua teks & VO dalam video ini ikut skrip anda sahaja.

**Nota Meta Ads:** teks penting diletak dalam zon y 180–1450 supaya tak ditutup UI Reels/Stories di bawah.
Durasi ~31s (lebih 1s dari anggaran) supaya baris VO babak 6 sempat dibaca dengan jelas.

## Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow
python prep.py            # ekstrak bingkai footage (assets/clips -> build/frames)
python render.py          # animasi (src/index.html) -> out/coway_ice_video_noaudio.mp4
python audio.py           # muzik + SFX -> out/music_sfx.wav
python mix.py             # gabung (+ voiceover jika ada voiceover/clips/*.mp3) -> out/coway_ice_final.mp4
```
Pratonton bingkai: `python render.py --stills 1,5.5,12`. Edit teks/harga terus dalam `src/index.html`;
masa babak dalam objek `T`. Potong semula klip dari video asal: `python prep.py --ais2 AIS_2.mp4 --ais3 AIS_3.mp4`.
