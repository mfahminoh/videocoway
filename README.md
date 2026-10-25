# Video Iklan Coway (Meta, Portrait 1080×1920)

Semua kerja ada dalam satu branch ini (digabung daripada 17 branch pada 24 Okt 2026).
Kerja baru: mula dari branch ini, dan gabung balik ke sini bila siap.

## Peta repo

| Produk / projek | Fail kerja | Video / bahan siap |
|---|---|---|
| **Villaem 3** — 30s, versi panjang, 5 gaya, V3xx | `src/`, `voiceover/`, `build_v5.py`, `build_clipads.py`, `videos/V3xx` | `out/villaem3_*.mp4`, `out/v5/`, `out/siap_dengan_vo/`, `out/V3*.mp4`, `out/V05_final.mp4` |
| **3 model paling laris** (Neon, Villaem 3, Ais) | `src/best3.html`, `voiceover/best3/` | `out/best3_final.mp4` |
| **Neon** — NE01–NE10, E04, hype HN01–HN05, listicle, versi warna Coway | `videos/`, `skrip/` | `out/NE*.mp4`, `out/E04_*.mp4`, `out/hype/`, `out/listicle/`, `out/coway/` |
| **Neo Plus / papercut** | `neoplus/`, `neoplus_full/`, `src/papercut/` | `out/neoplus_*.mp4`, `out/neo_papercut_*.mp4` |
| **Penapis air lain** — Air Botol, pakej 30 video | `airbotol/`, `pakej30/`, `PLAN_40_VIDEO.md` | `out/airbotol_final.mp4`, `out/pakej30_v*.mp4` |
| **Coway Ice** | `coway-ice/` | `coway-ice/out/` |
| **Ulangtahun 20** — V01–V15 | `ulangtahun20/` | `ulangtahun20/out/` |
| **Tilam** — BEREX Elite, copy gradualization, poster | `tilam/`, `copy/` | `out/tilam/`, `out/poster/`, `posters/P3*` |
| **Penapis udara (jerebu)** | `build_jerebu.py`, `build_short.py`, `JEREBU_PACKAGE.md` | `out/jerebu/`, `out/pendek/`, `out/model/`, `out/kesedaran/` |
| **Peti ais** — 5 video emosi, poster static | `videos/PA0x`, `campaigns/coway-peti-ais/`, `research/`, `static/` | `out/peti_ais/`, `out/static/` |
| **Neon × P1 "mampu milik"** — NE11–NE13, skrip TikTok rujukan → motion graphic / kinetic / komik | `projek/neon-p1-01/`, `videos/neon-p1-01_batch.py`, `videos/NE11`–`NE13` | `out/neon-p1-01/` |
| **Peti ais & aircond** — plan content | `plan/` | — |
| **Brand brain** (suara, warna, font, aset rasmi) | `brand-brain/` | — |
| **Threads / posting** | `threads/`, `promo/threads/` | — |
| **Poster iklan Meta** | `posters/` | `posters/*.jpg` |
| **Gaya motion graphic `mg`** (15 gaya mg-styles-15) — contoh NL01FV Flat Vector | `videos/lib/mg.js`, `videos/NL01FV/`, `reference/mg-styles-15/`, `reference/opus-video-prompts.md` | `out/mg/` |
| Rujukan & iklan | `reference/`, `ads/`, `iklan_meta_whatsapp.md` | — |

**Projek baru:** ikut aliran skill dalam [`projek/README.md`](projek/README.md): `coway-riset` → `coway-persona-produk` → `coway-skrip` → `coway-video` → `coway-poster` → `coway-threads` → `coway-iklan`. Persona induk: [`research/persona.md`](research/persona.md).

Skrip kongsi: `render.py`, `audio.py`, `mix.py`, `voiceover/`. Projek lama yang perlukan versi skrip
berbeza guna salinannya sendiri: `render_neoplus.py` / `mix_neoplus.py` / `voiceover/generate_vo_neoplus.py`
(Neo Plus, Air Botol) dan `render_best3.py` / `mix_best3.py` / `voiceover/generate_vo*_best3.py` (3 model).

---

## Coway Villaem 3 (±29s)

Motion graphic bercerita: *"3 tahun jual Coway… ada satu jenis customer yang nak beli sekali, puas hati"* → Villaem 3 → ciri → promo → CTA WhatsApp.

**Video siap:** `out/villaem3_final.mp4` (H.264, 30fps, muzik + SFX asli, tanpa lesen pihak ketiga).

## Babak
| Masa | Babak |
|------|-------|
| 0 – 3.6s | Hook: "3 TAHUN jual Coway" + ikon customer |
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

---

# Iklan 2 — 3 Model Coway Paling Laris (Portrait 1080×1920, 35s)

Sasaran: orang yang tengah plan nak pasang Coway. **Video siap:** `out/best3_final.mp4`.

| Masa | Babak |
|------|-------|
| 0 – 3.6s | Hook: "Tengah plan nak PASANG COWAY?" → "Ni 3 model paling laris tahun ni" + 3 produk |
| 3.9 – 8.2s | #1 **Neon** (video): mampu milik · lengkap 3 suhu (panas, suhu bilik, sejuk) |
| 8.2 – 17.1s | #2 **Villaem 3** (video): premium · generasi 3 · banyak pilihan suhu, ada air suam · tangki paling besar · senang guna, pilihan ramai |
| 17.1 – 24.3s | #3 **Coway Ais** (video): siap keluar ais · paling special · pagi / petang / malam |
| 24.3 – 32.3s | Promo semua model: RM20 je dah boleh pasang · rebate RM20 × 7 bulan · hantar & pasang percuma seluruh Malaysia |
| 32.3 – 35s | "Nak yang mana satu?" + butang WhatsApp |

**Neon:** babak video penuh skrin dari `assets/video/neon3.mp4` + `neon2.mp4` (potongan ditetapkan dalam
`src/best3.clips.json`; `render_best3.py` pecahkan jadi frame JPG dalam `out/clips/`). Thumbnail: `assets/img/neon-thumb.jpg`.

**Ais:** babak video penuh skrin dari `assets/video/ais3.mp4` (ais jatuh ke gelas) + `ais1.mov` (tuang kopi ais).
Sari kata asal dalam `ais1.mov` ditutup oleh panel Pagi/Petang/Malam. Thumbnail: `assets/img/ais.png`.

**Villaem 3:** babak video dari `assets/video/vil2.mp4` sahaja (tekan butang suhu → tangki UV → presenter) —
klip lain ada teks tertanam (ECO MODE, DUAL LOCK MODE, SERENDAH RM20). Thumbnail: `assets/img/villaem3-front.png`.

Voiceover: Gemini TTS, `voiceover/best3/source/gemini-tts_3.wav`, dipecah jadi klip per baris dengan
`python voiceover/split_vo.py voiceover/best3/source/gemini-tts_3.wav --ad best3 --cuts 4.1,9.2,19.8,28.2,37.4 --tempo 1.1`
(jeda dipendekkan, dilajukan 1.1×). Garis masa animasi (`T` dalam `src/best3.html`) diselaraskan dengan suara.
Skrip + sari kata: `voiceover/best3/skrip_voiceover.md`, `best3.srt`.

```
python render_best3.py --ad best3   # src/best3.html -> out/best3_video_noaudio.mp4
python audio.py --ad best3    # -> out/best3_music_sfx.wav
python mix_best3.py --ad best3      # -> out/best3_final.mp4 (+ VO jika ada voiceover/best3/clips/*.mp3)
```
