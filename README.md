# Video Iklan Coway (Meta, Portrait 1080×1920)

| Projek | Fail | Video siap |
|---|---|---|
| Villaem 3 (±29s, suara lelaki) | `src/`, `voiceover/` | `out/villaem3_final.mp4` |
| Neo Plus — untuk mak ayah (60s, suara perempuan) | `neoplus/` — lihat [neoplus/README.md](neoplus/README.md) | `out/neoplus_final.mp4` |
| Neo Plus — versi penuh, semua poin skrip (±2:35) | `neoplus_full/` — lihat [neoplus_full/README.md](neoplus_full/README.md) | `out/neoplus_full_final.mp4` |

---

## Coway Villaem 3 (±29s)

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
