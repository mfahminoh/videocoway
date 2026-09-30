# Montaj Promo Neo Plus — 15 saat (Portrait 1080×1920)

0–10s: 10 shot × 1s daripada video sedia ada (Menyampah air botol, Neo Plus versi penuh), dipotong ikut rentak
muzik 120 BPM, zoom perlahan + kilat putih, lencana "PROMO NEO PLUS · 7 BULAN PERTAMA RM20*" di atas.
10–15s: kad promo beranimasi (`endcard.html`): RM59/bulan · 7 bulan pertama RM20/bulan · penghantaran &
pemasangan percuma · butang WhatsApp · T&C.

Tiada voiceover (sesuai ditonton tanpa bunyi). Output: `out/montaj_15s.mp4`.

## Bina semula
```
python montaj/audio.py    # muzik + SFX
python montaj/build.py    # perlu out/airbotol_video_noaudio.mp4 & out/neoplus_full_video_noaudio.mp4
```
Tukar shot: edit `shots.json` (`src` = projek, `t` = saat paling menarik dalam video bisu projek itu).
