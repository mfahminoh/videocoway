# Coway Ice — 2 Video Reels 15s (Portrait 1080×1920)

| Fail | Sudut | Aliran |
|------|-------|--------|
| `out/reel1_final.mp4` | **Family kaki ais?**: padat & laju | Hook (hujan ais + produk hentak masuk) → ais baru setiap 15 minit → 700g → RM20/bulan × 7 bulan → hantar & pasang percuma + WhatsApp |
| `out/reel2_final.mp4` | **Hari-hari beli ais bungkus?**: pain point | Beg ais bungkus jatuh → bekas ais kosong ❌ → "Ais dah ready" (footage) → 15 min + 700g → RM20/bulan × 7 bulan → pasang percuma + WhatsApp |

## Skrip voiceover (TTS)

Masa setiap baris ada dalam `reel1.lines.json` / `reel2.lines.json`. Nombor ditulis dalam perkataan supaya TTS sebut dengan betul.

**Reel 1: Family kaki ais**
| # | Masa | Skrip | Teks atas skrin |
|---|------|-------|-----------------|
| 01 | 0.15 – 2.5 | Family kaki ais? Ni dia, Coway Ice! | FAMILY KAKI AIS? 🧊 · COWAY ICE ❄️ |
| 02 | 2.7 – 5.5 | Ais baru keluar setiap lima belas minit. | AIS BARU SETIAP 15 MINIT |
| 03 | 5.7 – 8.2 | Simpan sehingga tujuh ratus gram ais. | SEHINGGA 700g AIS |
| 04 | 8.4 – 11.5 | Promosi dua puluh ringgit sebulan, untuk tujuh bulan. | 🔥 PROMOSI · RM20 / BULAN · SELAMA 7 BULAN |
| 05 | 11.7 – 14.8 | Hantar dan pasang percuma. Klik WhatsApp sekarang! | HANTAR & PASANG PERCUMA 🇲🇾 · KLIK WHATSAPP SEKARANG |

**Reel 2: Ais bungkus**
| # | Masa | Skrip | Teks atas skrin |
|---|------|-------|-----------------|
| 01 | 0.15 – 2.9 | Hari-hari beli ais bungkus? Bekas ais pula selalu kosong? | HARI-HARI BELI AIS BUNGKUS? 😩 · BEKAS AIS KOSONG LAGI? 🙄 |
| 02 | 3.1 – 6.1 | Dengan Coway Ice, ais dah ready dalam mesin. | DENGAN COWAY ICE, AIS DAH READY ✅ |
| 03 | 6.3 – 9.1 | Ais baru setiap lima belas minit, simpan sampai tujuh ratus gram. | SENTIASA ADA AIS 🧊 · 15 min · 700g |
| 04 | 9.3 – 12.1 | Sekarang dua puluh ringgit sebulan, selama tujuh bulan. | 🔥 PROMOSI · RM20 / BULAN · SELAMA 7 BULAN |
| 05 | 12.3 – 14.8 | Pasang percuma. WhatsApp sekarang! | PASANG PERCUMA 🇲🇾 · WHATSAPP SEKARANG |

## Bina semula
```
python render.py --page reels/reel1.html --out out/reel1_video_noaudio.mp4
python reels/audio_reels.py reel1                      # muzik + SFX -> out/reel1_music_sfx.wav
python reels/gemini_tts.py reel1                       # perlu GEMINI_API_KEY -> reels/vo_reel1/*.wav
python mix.py --video out/reel1_video_noaudio.mp4 --bed out/reel1_music_sfx.wav \
              --lines reels/reel1.lines.json --clips reels/vo_reel1 --out out/reel1_final.mp4
```
(sama untuk `reel2`). Tanpa folder `vo_reelN`, `mix.py` hasilkan video dengan muzik + SFX sahaja.
Pratonton: `python render.py --page reels/reel1.html --stills 1,5 --stills-dir out/stills_r1`.
Komponen dikongsi (enjin animasi, bekas ais, footage) dalam `lib.js` / `lib.css`; footage dari `../build/frames` (`python prep.py`).
