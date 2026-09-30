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

## 5 video gaya (out/v5/)
| Fail | Gaya | Sudut | Panjang |
|---|---|---|---|
| `villaem3_v1_premium.mp4` | Edit footage sinematik, hitam & emas | Premium / high spec | 38.3s |
| `villaem3_v2_upgrade.mp4` | UGC / POV TikTok, putih & teal | Penapis lama dah habis bayar → upgrade | 36.8s |
| `villaem3_v3_family.mp4` | Slideshow Ken Burns, krim & oren | Keluarga besar / tangki paling besar | 34.8s |
| `villaem3_v4_kinetic.mp4` | Kinetic typography, hitam/kuning/merah | Beli tak alang-alang | 34.2s |
| `villaem3_v6_tradein.mp4` | Cerita testimoni, hijau & emas | Alah membeli, menang memakai (trade-in) | 44.0s |

Bina semula: `python build_v5.py [--only v1_premium]`. Skrip VO badan: `voiceover/skrip_v5.md`.
