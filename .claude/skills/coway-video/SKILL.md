---
name: coway-video
description: Jana video iklan Coway (portrait 1080×1920, Meta/TikTok/Reels, suara Gemini TTS) daripada skrip yang dah diluluskan dalam projek/<kod>/skrip.md — 10 video sebatch, VO dulu kemudian visual ikut masa VO, dalam format motion graphic (termasuk 15 gaya mg: flat vector, liquid, sticker explainer, isometric, HUD, dsb.), cerita emosi, atau dengan footage AI (Seedance, Veo, Google Flow) — kemudian semak, review grid dan gabung ke main. Guna bila user minta jana, generate, render atau hasilkan video Coway, "buat video dari skrip", batch video seterusnya, tukar format video, atau "gaya motion graphic baru". Untuk tulis skrip guna coway-skrip dulu.
---

# Jana video Coway

Input: `projek/<kod>/skrip.md` dengan status **DILULUSKAN** (dari `coway-skrip`) dan `brief.md`.
Output: `videos/<ID>/`, `out/<kod>/*.mp4`, halaman review, papan status dikemas kini.
Langkah seterusnya: `coway-poster`, kemudian iklan / `coway-threads`.

Skrip belum diluluskan atau tiada → berhenti dan guna `coway-skrip`. Jangan tulis atau ubah sudut di sini; ubah kecil (pendekkan baris, betulkan sebutan) dibenarkan dan dicatat dalam `skrip.md`.

**Satu batch = 10 video.** Batch seterusnya hanya selepas batch ini diluluskan dalam review.
**VO dulu, visual ikut masa VO.** Jangan bina animasi dulu kemudian "retime" ke suara.

## Format

| Format | Bina dengan | Sesuai untuk |
|---|---|---|
| `scenes` (lalai, `theme: "coway"`) | `videos/build_video.py` | Infografik, listicle, harga, kuiz, mitos vs fakta, presenter + klip |
| `hype` (`"player": "hype"`) | `videos/build_video.py` | Promo tenaga tinggi: kinetic, papercut, komik, neon glow, UGC |
| `story` (spec dengan `shots`) | `videos/peti_ais.py` | Cerita emosi dengan gambar Seedream + Ken Burns (contoh PA01–PA05) |
| **`mg`** (`"player": "mg"`, 15 gaya motion design) | `videos/<ID>/index.html` ditulis tangan + `videos/lib/mg.js` | Rupa yang lebih kuat dan berbeza: flat vector, liquid, sticker explainer, isometric, HUD, dsb. Panduan: [`formats/mg-gaya.md`](formats/mg-gaya.md), contoh NL01FV |
| **Footage AI** (Seedance / Veo / Google Flow) | klip AI sebagai latar `scenes` | Situasi hidup: orang, rumah, emosi. Panduan: [`formats/ai-klip.md`](formats/ai-klip.md) |

Ikut "Format cadangan" dalam `skrip.md`; variasikan dalam satu batch supaya iklan boleh diuji. Format baru (contohnya 3D) ditambah sebagai fail dalam `formats/`.
Format `mg`: langkah 1, 3 dan 4 di bawah diganti dengan langkah dalam [`formats/mg-gaya.md`](formats/mg-gaya.md) (cue sheet dalam `spec.json`, halaman `index.html`, stills dengan `render.py`). Langkah 2 (VO), 5 dan 6 kekal sama.
Rujukan elemen, latar dan contoh spec: [`reference.md`](reference.md).

## 1. lines.json + spec.json

ID dari `skrip.md` (kod produk 2 huruf + nombor). Kod sedia ada: `NE`/`NL`/`HN` Neon, `V3xx` Villaem 3, `PA` peti ais. Baru: `NP` Neo Plus, `CP` Core Plus, `AI` AIS, `DZ` Dazzie, `CN` Cinnamon, `AP` penapis udara, `AC` aircond, `TL` tilam, `KU` kerusi urut, `BD` bidet.

Tulis **`videos/<kod>_batch.py`** yang menjana `videos/<ID>/{lines.json, spec.json}` untuk semua 10 video (ikut corak `videos/neon_batch.py`): lajur VO → `text`, lajur Kapsyen → `cap`, lajur Visual → `scenes`/`els`. Jalankan, kemudian:

```bash
python3 .claude/skills/coway-video/scripts/semak.py <ID...>
```

Baiki semua **RALAT**. Semak setiap **amaran**, kerana ada yang sengaja.

`spec.json`: `slug`, `voice`, `style` (arahan suara dalam English), `theme: "coway"`, `brand: "COWAY"`, `scenes`, `els`. Elemen terakhir `cta` dengan `fine` (nota harga + "Tertakluk ..."). Masa elemen ikut baris VO (`"@07"`, `"@07e"`, `"@07%40"`), bukan saat mentah.

Format footage AI: jana klip ikut [`formats/ai-klip.md`](formats/ai-klip.md) **selepas** VO (langkah 2), supaya panjang setiap shot diketahui.

## 2. VO dulu

```bash
python3 videos/build_video.py <ID> --tts          # Gemini TTS satu take + penjajaran + timing (tiada render)
python3 .claude/skills/coway-video/scripts/semak.py <ID>
python3 voiceover/transcribe_chunks.py videos/<ID>/vo.wav 0 99 0.35 > videos/<ID>/chunks.txt
```

- Baca `chunks.txt`: pastikan setiap baris disebut, "Coway"/"Villaem" betul, dan tiada arahan gaya terbaca. Jika salah sebut, betulkan `text` dan ulang `--tts` untuk video itu sahaja. Transkrip potongan sangat pendek (< 1.5 s) selalu salah dengar. Jika hanya potongan pendek yang pelik dan selebihnya betul, jangan jana semula; senaraikan baris itu untuk user dengar semasa review.
- Kapsyen lari dari suara (amaran segmen pendek): jalankan `python3 voiceover/align_chunks.py videos/<ID>/vo.wav videos/<ID>/lines.json videos/<ID>/chunks.txt videos/<ID>/segments.json`, kemudian guna `--no-align` selepas ini.
- Terlalu panjang → pendekkan skrip (catat dalam `skrip.md`), bukan lajukan suara.
- TTS 429 = had per minit (tunggu ±1 minit). "PerDay" = kuota harian habis: berhenti dan beritahu user. **Jangan jana semula VO yang dah elok**, kerana ubah visual tak perlukan `--tts`.

## 3. Gambar contoh dulu, render kemudian

```bash
python3 videos/build_video.py <ID> --stills 1,8,20,30     # masa: hook, isi, harga, CTA (dari segments.json)
```

Buka setiap PNG dalam `out/stills/` (Read) dan semak:
- teks tak terpotong atau bertindih;
- teks penting ≥ 120 px dari atas & bawah (UI Meta);
- produk dan harga betul;
- bar kapsyen VO duduk pada 1520–1690 px, jadi letak elemen dengan `top` ≤ ~1300.

Untuk ubah, edit `spec.json`, kemudian jalankan `python3 videos/build_video.py <ID> --stills ...` (tanpa `--tts`; tambah `--no-align` jika segments dibaiki manual).

## 4. Render

```bash
python3 videos/build_video.py <ID> --render --review out/<kod>     # guna vo.wav sedia ada (+ --no-align jika segments dibaiki manual)
python3 .claude/skills/coway-video/scripts/semak.py <ID...>         # panjang & fail siap
```

- `out/*` diabaikan oleh git: tambah `!out/<kod>/` dalam `.gitignore` (bahagian produk berkenaan) supaya video siap di-commit.
- Render semula hanya video yang berubah.
- Pemain `story`: `python3 videos/peti_ais.py <ID> --tts --render` (ikut corak `videos/peti_ais.py`; gambar babak dijana dengan skill `seedream`).

## 5. Review

Guna skill **video-review** untuk `out/<kod>/*.mp4` (grid, butang Lulus / Perlu ubah, komen). Baca keputusan, baiki **hanya** video "Perlu ubah", render semula, kemas kini halaman yang sama.

## 6. Simpan

- Commit `videos/<kod>_batch.py`, `videos/<ID>/`, `out/<kod>/`, klip AI dalam `assets/clips/`, `projek/<kod>/shots.md`, `.gitignore`.
- Kemas kini `projek/<kod>/README.md` (langkah 4 ✅, URL review) dan tambah satu baris dalam "Peta repo" `README.md`.
- Gabung ke `main` (merge ke `main` dan push jika sesi dibenarkan; jika tidak, beritahu user untuk merge).

## Senarai semak akhir (sebelum kata "siap")

- [ ] `semak.py` tiada RALAT untuk semua 10 ID
- [ ] Transkrip VO disemak; sebutan Coway/model betul
- [ ] Stills disemak; tiada teks terpotong; harga = harga dalam brief
- [ ] Penafian wajib ada (TÜV untuk UV 99.9%, "Tertakluk" untuk promo, nota kaki angka peti ais)
- [ ] Klip AI: tiada teks rosak, bentuk & logo produk betul, konteks Malaysia
- [ ] Setiap video ≤ panjang sasaran, CTA WhatsApp di hujung
- [ ] Format `mg`: Signature features gaya ada, semua beat dikunci pada cue VO, tiada `Math.random`/`Date`
- [ ] Halaman review diterbitkan; video "Perlu ubah" dibaiki
- [ ] Di-commit, papan status & README dikemas kini, digabung ke `main`
