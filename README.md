# Coway Villaem 3 — Video Iklan Meta (Portrait 1080×1920, ±29s)

Motion graphic bercerita: *"3 tahun jual Coway… ada satu jenis customer yang nak beli sekali, puas hati"* → Villaem 3 → ciri → promo → CTA WhatsApp.

**Video siap:** `out/villaem3_final.mp4` (H.264, 30fps, muzik + SFX asli, tanpa lesen pihak ketiga).

## Babak
| Masa | Babak |
|------|-------|
| 0 – 4s | Hook: "3 TAHUN jual Coway" + ikon customer |
| 4 – 8.6s | Jenis customer: ~~beli banyak kali~~ → **TAHAN LAMA & PUAS HATI** |
| 8.6 – 11.4s | Pendedahan produk Coway Villaem 3 |
| 11.4 – 19.8s | HIGH SPEC + tangki paling besar · 8+ pilihan suhu · paling tahan lasak |
| 19.8 – 26s | Promo: Rebate RM20 × 7 bulan · serendah RM84/bulan · pemasangan percuma · servis 2/4 bulan |
| 26 – 29.5s | "Sekali beli. Puas hati." + butang WhatsApp |

## Voiceover
Lihat `voiceover/skrip_voiceover.md` (skrip + masa, juga `villaem3.srt`).

## Bina semula
```
pip install playwright imageio-ffmpeg numpy pillow
python render.py          # animasi (src/index.html) -> out/villaem3_video_noaudio.mp4
python audio.py           # muzik + SFX -> out/music_sfx.wav
python mix.py             # gabung (+ voiceover jika ada voiceover/clips/*.mp3)
```
Edit teks/harga terus dalam `src/index.html`; masa babak dalam objek `T`.
Warna: navy/biru Coway, aksen biru langit; merah/biru panas-sejuk ikut garis pada produk. Font: Poppins.

---

# Iklan 2 — 3 Model Coway Paling Laris (Portrait 1080×1920, 30s)

Sasaran: orang yang tengah plan nak pasang Coway. **Video siap:** `out/best3_final.mp4`.

| Masa | Babak |
|------|-------|
| 0 – 4s | Hook: "Tengah plan nak PASANG COWAY?" → "Ni 3 model paling laris tahun ni" + 3 produk |
| 4 – 9.8s | #1 **Neon**: mampu milik · lengkap 3 suhu |
| 9.8 – 16.3s | #2 **Villaem 3**: premium · generasi 3 · pilihan ramai, senang guna · banyak pilihan suhu, ada air suam · tangki paling besar |
| 16.3 – 22.2s | #3 **Coway Ais**: paling special, keluar ais · pagi / petang / malam |
| 22.2 – 27.8s | Promo semua model: RM20 je dah boleh pasang · rebate RM20 × 7 bulan · hantar & pasang percuma seluruh Malaysia |
| 27.8 – 30s | "Nak yang mana satu?" + butang WhatsApp |

**Neon:** babak video penuh skrin dari `assets/video/neon3.mp4` + `neon2.mp4` (potongan ditetapkan dalam
`src/best3.clips.json`; `render.py` pecahkan jadi frame JPG dalam `out/clips/`). Thumbnail: `assets/img/neon-thumb.jpg`.

**Ais:** `assets/img/ais.png` masih **gambar sementara** — ganti dengan gambar sebenar (PNG latar lutsinar/putih,
nama fail sama) atau tambah klip video seperti Neon, kemudian render semula.

Voiceover: `voiceover/best3/skrip_voiceover.md` (+ `best3.srt`).

```
python render.py --ad best3   # src/best3.html -> out/best3_video_noaudio.mp4
python audio.py --ad best3    # -> out/best3_music_sfx.wav
python mix.py --ad best3      # -> out/best3_final.mp4 (+ VO jika ada voiceover/best3/clips/*.mp3)
```
