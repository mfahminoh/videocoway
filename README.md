# Video Iklan Coway (Meta, Portrait 1080×1920)

| Projek | Fail | Video siap |
|---|---|---|
| Villaem 3 (±29s, suara lelaki) | `src/`, `voiceover/` | `out/villaem3_final.mp4` |
| Neo Plus — untuk mak ayah (60s, suara Gemini perempuan) | `neoplus/` — lihat [neoplus/README.md](neoplus/README.md) | `out/neoplus_final.mp4` |
| Neo Plus — versi penuh, semua poin skrip (±2:51, suara Gemini) | `neoplus_full/` — lihat [neoplus_full/README.md](neoplus_full/README.md) | `out/neoplus_full_final.mp4` |

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

## 5 video gaya (out/v5/)
| Fail | Gaya | Sudut | Panjang |
|---|---|---|---|
| `villaem3_v1_premium.mp4` | Edit footage sinematik, hitam & emas | Premium / high spec | 38.3s |
| `villaem3_v2_upgrade.mp4` | UGC / POV TikTok, putih & teal | Penapis lama dah habis bayar → upgrade | 36.8s |
| `villaem3_v3_family.mp4` | Slideshow Ken Burns, krim & oren | Keluarga besar / tangki paling besar | 34.8s |
| `villaem3_v4_kinetic.mp4` | Kinetic typography, hitam/kuning/merah | Beli tak alang-alang | 34.2s |
| `villaem3_v6_tradein.mp4` | Cerita testimoni, hijau & emas | Alah membeli, menang memakai (trade-in) | 44.0s |

Bina semula: `python build_v5.py [--only v1_premium]`. Skrip VO badan: `voiceover/skrip_v5.md`.

## Pakej Jerebu — penapis udara (out/jerebu/)
6 video bersuara tentang jerebu, PM2.5 dan penapis udara Coway (J1 jerebu masuk rumah · J2 kenapa lampu merah ·
J3 PM2.5 · J4 6 tips guna · J5 pilih model · J6 lepas jerebu masih berbaloi?). Fakta & sumber, posting media sosial,
jadual produk, jawapan bantahan dan copy iklan: lihat `JEREBU_PACKAGE.md`. Bina semula: `python build_jerebu.py`.

## 5 video peti ais Coway: emosi & desire (out/peti_ais/)
Skrip dan sudut ada dalam `skrip/peti_ais.md` (berdasarkan `research/peti-ais-coway-headline-research.md`). Setiap video bawah 90 saat, portrait 1080×1920.

| Fail | Sudut | Pencerita | Model / offer |
|---|---|---|---|
| `PA01_cium-dulu-baru-masak.mp4` | Lauk basi = duit dapur cair | Ibu muda | 551L, dari RM99/bln |
| `PA02_siapa-nak-datang.mp4` | Mimpi ngeri repair → Heart Service | Ayah | dari RM84/bln |
| `PA03_peti-ais-masa-kahwin.mp4` | Peti dari masa kahwin, keluarga dah membesar | Ibu | 551L, dari RM99/bln |
| `PA04_tv-dah-65-inci.mp4` | Semua dah upgrade kecuali dapur isteri | Suami | 715L, dari RM84/bln |
| `PA05_mak-kata-masih-okay.mp4` | Anak belikan peti ais untuk mak | Anak perempuan | 551L, dari RM99/bln |

- Babak cerita: Seedream 4.5 (skill `.claude/skills/seedream`), prompt dalam `assets/img/peti_ais/prompts.json`. Untuk jana semula: `python3 videos/peti_ais_images.py [pa03_c]`.
- Produk: gambar/klip rasmi coway.com.my dalam `assets/img/coway_fridge/` dan `assets/clips/fridge/`.
- VO: Gemini TTS (`voiceover/gemini_tts.py`). Penyelarasan baris guna `voiceover/align.py`, disemak dengan `voiceover/transcribe_chunks.py` dan `voiceover/align_chunks.py`.
- Bina: `python3 videos/peti_ais.py PA01 --render` (atau `all`). Edit babak/teks dalam `videos/PA0x/spec.json`, teks VO/kapsyen dalam `lines.json`.
