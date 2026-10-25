---
name: coway-video
description: Hasilkan siri video iklan Coway (portrait 1080×1920, Meta/TikTok/Reels, suara Gemini TTS) ikut aliran tetap repo videocoway — brief → skrip (satu kelulusan) → VO dulu → visual ikut masa VO → semak → review grid → gabung ke main → serah ke iklan. Guna bila user minta buat, jana, hasilkan atau render video Coway, siri/pakej video untuk mana-mana produk Coway (penapis air, penapis udara, peti ais, aircond, tilam, bidet), "produksi video", "video iklan baru", atau tambah video ke siri sedia ada.
---

# Produksi video Coway

Satu siri = **5 video** untuk satu produk (lalai). Lancar dulu, tunggu data iklan, kemudian buat lebih banyak versi video yang menang. Jangan hasilkan 30–70 video sebelum ada data.

Aliran ni wujud supaya kerja tak berulang: **suara (VO) dulu, visual ikut masa VO**. Jangan bina animasi dulu kemudian "retime" ke suara.

Enjin yang dah ada (jangan bina pemain baru melainkan user minta):

| Pemain | Bina dengan | Sesuai untuk |
|---|---|---|
| `scenes` (lalai, `theme: "coway"`) | `videos/build_video.py` | Infografik, listicle "3 sebab", harga, kuiz, mitos vs fakta, presenter + klip |
| `hype` (`"player": "hype"`) | `videos/build_video.py` | Promo tenaga tinggi: kinetic, papercut, komik, neon glow, UGC |
| `story` (spec dengan `shots`) | `videos/peti_ais.py` | Cerita emosi dengan gambar Seedream + Ken Burns (contoh: PA01–PA05) |

Rujukan elemen, latar dan contoh spec: [`reference.md`](reference.md).

## 1. Brief

Baca dulu, jangan teka:
- `CLAUDE.md` (peraturan iklan), `brand-brain/coway/brand-guide.md` (nada, warna, CTA, penafian wajib), `brand-brain/coway/products.md` (fakta & harga produk).
- Jadual "Peta repo" dalam `README.md` dan `skrip/` untuk video sedia ada produk yang sama — elak ulang sudut yang dah dibuat, dan guna semula aset (`assets/clips/`, `assets/img/`, `brand-brain/coway/Other Brand Assets/`).

Tentukan untuk siri: produk, 5 sudut (satu persona/situasi pembeli setiap video), pemain, suara, panjang sasaran (30–45 s; `story` boleh hingga 60 s).

Tanya user **sekali sahaja**, dalam satu soalan, hanya perkara yang tak ada dalam repo: harga/promo semasa (jika `products.md`/skrip lepas lebih 2 minggu atau promo berubah), dan apa-apa yang brief perlukan tapi tak boleh dicari. Selebihnya pilih sendiri dan nyatakan pilihan dalam brief.

Tulis brief + skrip dalam **`skrip/<siri>.md`** (satu fail satu siri).

## 2. Skrip → satu kelulusan

Setiap video dalam `skrip/<siri>.md`: ID · tajuk/hook · sudut & persona · pemain/gaya · suara · jadual baris VO (+ cadangan visual) · CTA.

Peraturan skrip:
- **Hook dalam baris pertama (≤ 3 s)**: soalan, situasi, atau angka. Bukan "Assalamualaikum" / pengenalan diri.
- 70–100 perkataan, ayat pendek, BM santai (brand-guide §5). Kita **ejen sah Coway** ("saya", "customer saya"), bukan Coway Malaysia.
- Fakta & harga hanya dari `products.md` / harga yang user sahkan. Harga dalam RM, **jangan sebut peratus diskaun**.
- Dakwaan wajib penafian: UV 99.9% → "Berdasarkan ujian TÜV SÜD Korea dalam persekitaran terkawal."; angka Silver Ion/deodoriser peti ais → nota kaki. Promo → "*Tertakluk terma & syarat".
- Tutup dengan CTA "WhatsApp saya". Jangan guna Careline 1800-888-111 atau nama page "Coway Malaysia".
- Isu kesihatan (susu bayi, penyakit): "ikut nasihat doktor", jangan dakwa perubatan.

Tunjuk user senarai 5 hook + sudut (ringkas dalam chat, skrip penuh dalam fail) dan minta **satu** kelulusan. Ubah ikut komen, kemudian teruskan sampai siap tanpa tanya lagi. Jika user dah kata "terus buat", langkau kelulusan.

## 3. lines.json + spec.json

ID: kod produk 2 huruf + nombor, sambung nombor yang belum diguna (`ls videos/`). Sedia ada: `NE`/`NL`/`HN` Neon, `V3xx` Villaem 3, `PA` peti ais. Baru: `NP` Neo Plus, `CP` Core Plus, `AI` AIS, `DZ` Dazzie, `CN` Cinnamon, `AP` penapis udara, `AC` aircond, `TL` tilam, `BD` bidet.

Untuk ≥ 3 video, tulis **`videos/<siri>_batch.py`** yang menjana `videos/<ID>/{lines.json, spec.json}` (ikut corak `videos/neon_batch.py`: fungsi kecil untuk harga, CTA, produk; semua skrip dalam satu fail senang diubah). Jalankan, kemudian:

```bash
python3 .claude/skills/coway-video/scripts/semak.py <ID...>
```

Baiki semua **RALAT**. Semak setiap **amaran** (ada yang sengaja).

`lines.json`: `text` = apa TTS sebut (**nombor dalam perkataan**: "lima puluh empat ringgit"), `cap` = kapsyen skrin (angka, `*sorotan*`). Jika transkrip (langkah 4) tunjuk "Coway" disebut salah, tulis `Kowei` dalam `text` dan kekalkan `Coway` dalam `cap`.

`spec.json`: `slug`, `voice`, `style` (arahan suara dalam English, cth. "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"), `theme: "coway"`, `brand: "COWAY"`, `scenes`, `els`. Elemen terakhir `cta` dengan `fine` (nota harga + "Tertakluk ..."). Masa elemen ikut baris VO (`"@07"`, `"@07e"`, `"@07%40"`) — jangan tulis saat mentah, supaya visual ikut suara secara automatik.

## 4. VO dulu

```bash
python3 videos/build_video.py <ID> --tts          # Gemini TTS satu take + penjajaran + timing (tiada render)
python3 .claude/skills/coway-video/scripts/semak.py <ID>
python3 voiceover/transcribe_chunks.py videos/<ID>/vo.wav 0 99 0.35 > videos/<ID>/chunks.txt
```

- Baca `chunks.txt`: pastikan setiap baris disebut, "Coway"/"Villaem" betul, tiada arahan gaya terbaca. Jika salah sebut → betulkan `text`, ulang `--tts` untuk video itu sahaja. Transkrip bagi potongan yang sangat pendek (< 1.5 s) selalu salah dengar. Jika hanya potongan pendek yang pelik dan selebihnya betul, jangan jana semula; senaraikan baris itu untuk user dengar semasa review.
- Kapsyen lari dari suara (amaran segmen pendek) → `python3 voiceover/align_chunks.py videos/<ID>/vo.wav videos/<ID>/lines.json videos/<ID>/chunks.txt videos/<ID>/segments.json`, kemudian guna `--no-align` selepas ini.
- Terlalu panjang → pendekkan skrip, bukan lajukan suara.
- TTS 429 = had per minit (tunggu ~1 minit); "PerDay" = kuota harian habis, berhenti dan beritahu user. **Jangan jana semula VO yang dah elok** — ubah visual tak perlukan `--tts`.

## 5. Gambar contoh dulu, render kemudian

```bash
python3 videos/build_video.py <ID> --stills 1,8,20,30     # masa: hook, isi, harga, CTA (ambil dari segments.json)
```

Buka setiap PNG dalam `out/stills/` (Read) dan semak: teks tak terpotong/bertindih, teks penting ≥ 120 px dari atas & bawah (UI Meta), produk betul, harga betul. Bar kapsyen VO duduk pada 1520–1690 px, jadi letak elemen dengan `top` ≤ ~1300. Ubah `spec.json` → `python3 videos/build_video.py <ID> --stills ...` (tanpa `--tts`; tambah `--no-align` jika segments dibaiki manual).

## 6. Render

```bash
python3 videos/build_video.py <ID> --render --review out/<siri>     # guna vo.wav sedia ada (+ --no-align jika segments dibaiki manual)
python3 .claude/skills/coway-video/scripts/semak.py <ID...>         # panjang & fail siap
```

- `out/*` diabaikan oleh git: tambah `!out/<siri>/` dalam `.gitignore` (bahagian produk berkenaan) supaya video siap ikut di-commit.
- Render semula hanya video yang berubah.
- Pemain `story`: `python3 videos/peti_ais.py <ID> --tts --render` (ikut corak `videos/peti_ais.py`; gambar babak dijana dengan skill `seedream`).

## 7. Review

Guna skill **video-review** untuk `out/<siri>/*.mp4` (grid, butang Lulus / Perlu ubah, komen). Baca keputusan, baiki **hanya** video "Perlu ubah", render semula, kemas kini halaman yang sama.

## 8. Simpan

- Commit `skrip/<siri>.md`, `videos/<siri>_batch.py`, `videos/<ID>/`, `out/<siri>/`, `.gitignore`.
- Tambah satu baris dalam jadual "Peta repo" `README.md` (produk · fail kerja · video siap).
- Gabung ke `main` (merge ke `main` dan push jika sesi dibenarkan; jika tidak, beritahu user untuk merge). Kerja tak boleh tinggal di branch sesi.

## 9. Serah ke iklan

- Lancar ikut `CLAUDE.md`: **1 video = 1 kempen = 1 ad set = 1 iklan**. Untuk akaun klien/ejen baru guna skill `coway-onboarding-klien`.
- Selepas 3–5 hari, audit dengan skill `coway-ads-audit`. Siri seterusnya = lebih banyak variasi hook/sudut video yang menang, bukan produk baru.

## Senarai semak akhir (sebelum kata "siap")

- [ ] `semak.py` tiada RALAT untuk semua ID
- [ ] Transkrip VO disemak; sebutan Coway/model betul
- [ ] Stills disemak; tiada teks terpotong; harga = harga disahkan
- [ ] Penafian wajib ada (TÜV untuk UV 99.9%, "Tertakluk" untuk promo, nota kaki angka peti ais)
- [ ] Setiap video ≤ panjang sasaran, CTA WhatsApp di hujung
- [ ] Halaman review diterbitkan; video "Perlu ubah" dibaiki
- [ ] Di-commit, README dikemas kini, digabung ke `main`
