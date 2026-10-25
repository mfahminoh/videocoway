---
name: coway-remake
description: Remake video TikTok yang dah terbukti (view tinggi) menjadi 3 video iklan Coway baru — skrip sama (diambil dari audio atau kapsyen video), suara Gemini dijana semula, dan 3 gaya motion graphic berbeza yang dipilih secara rawak (6 gaya templat + 15 gaya mg-styles-15) dengan gambar realistik Seedream — dalam projek/<kod>/storyboard.json, kemudian render dengan coway-video. Guna bila user upload video TikTok / Reels dan kata "recreate", "remake", "tiru video ni", "guna skrip sama", "buat semula guna gambar sendiri", atau nak beberapa versi gaya dari satu video rujukan.
---

# Remake video TikTok → 3 gaya

Input: satu video rujukan (MP4 yang user upload) + produk Coway yang dijual.
Output: `projek/<kod>/{README.md, skrip.md, storyboard.json}`, gambar `assets/img/<kod>/`, 3 video dalam `out/<kod>/`, halaman review.
Langkah: ambil skrip (1–2) → storyboard + gambar (3–4) → suara sekali (5) → 3 gaya (6) → semak & review (7).

Skill ini menggantikan `coway-riset` → `coway-skrip` untuk satu video rujukan: skrip datang dari video, bukan ditulis baru.
Render guna pemain dan arahan `coway-video` (jangan salin logiknya ke sini).

**Satu batch remake = 1 video rujukan × 3 gaya berbeza.** Batch seterusnya hanya selepas review batch ini.

## 1. Ambil skrip dari video

```bash
K=<scratchpad>/remake-<kod>; mkdir -p $K && cp "<video>" $K/src.mp4
python3 .claude/skills/coway-remake/scripts/kapsyen.py $K/src.mp4 $K          # audio.wav, grid.jpg, kap_NN.jpg
python3 voiceover/transcribe_chunks.py $K/audio.wav 0 99 0.3                   # transkrip Gemini ikut jeda
```

- Read `grid.jpg` (babak, teks besar, produk dalam video) dan setiap `kap_NN.jpg` (kapsyen setiap 0.2 s, cap masa merah).
- Gemini 503 / 429 berterusan → jangan tunggu: kapsyen TikTok biasanya ikut suara perkataan demi perkataan, jadi bina skrip dari `kap_NN.jpg`. Bahagian tanpa kapsyen (hook dengan teks besar, babak harga): baca teks besar dalam `grid.jpg` atau jubin penuh bingkai bahagian itu.
- Kapsyen bukan di 68–80 % tinggi bingkai → `--y0 .1 --y1 .25` (contoh), ulang.
- Video ada muzik berhak cipta / suara orang lain: **jangan guna audio asal**. Hanya skrip diambil; suara dijana semula.

## 2. Sesuaikan & dapatkan satu kelulusan

Tulis `projek/<kod>/skrip.md` (kod: `<produk>-<persona>-<nn>`, lihat `projek/README.md`): transkrip asal, kemudian jadual baris (VO, kapsyen), kemudian senarai **Ubah daripada skrip asal**. Ubah hanya yang perlu:

- **Harga & dakwaan** ikut `brand-brain/coway/products.md` dan `brand-guide.md`. Promo bulanan (contohnya rebat RM20 × 7 bulan) mesti disahkan user. Tulis sebagai rebat, bukan "RM20 sahaja", dan letak "*Tertakluk ..." dalam `fine`.
- **CTA**: "link di bio / beg kuning / beg biru" → "tekan butang WhatsApp" untuk iklan Meta ejen. Audiens iklan ialah pelanggan akhir (lihat `CLAUDE.md`).
- **Sebutan TTS**: nombor dieja ("lima puluh sembilan ringgit"), "tahu" → "tau", English yang pelik dibetulkan ("with service" → "dengan servis").
- **Panjang**: kekal ±panjang asal. Jangan tambah baris baru atau tukar sudut.

Tanya user sekali dengan AskUserQuestion. Soalan biasa: promo masih sah, CTA, dan "skrip 100% sama atau rapikan sikit". Kemudian tandakan `**Status: DILULUSKAN** (<tarikh>)`.

## 3. Storyboard

Tulis `projek/<kod>/storyboard.json` (contoh penuh: `projek/neon-p1-01/storyboard.json`). Setiap baris skrip ada `id`, `text` (untuk TTS), `cap` (kapsyen, `*sorot*`) dan `jenis` dengan medannya:

| jenis | medan | contoh |
|---|---|---|
| `hook` | `tajuk`, `sorot` | `"NAK CARI\|PENAPIS AIR"`, `"MAMPU MILIK?"` |
| `produk` | `tajuk`, `sorot` | `"COWAY NEON"`, `"3 SUHU"` |
| `suhu` | `tajuk`? | panas / sejuk / suhu bilik |
| `warna`, `poin` | `tajuk`, `sorot` | `"DESIGN"`, `"SANGAT MINIMALIST"` |
| `harga` | `label`?, `harga`, `sub`, `per`?, `ikon`? | `"HARGA BULANAN"`, `"RM59"`, `"DENGAN SERVIS"` |
| `promo` | `tajuk`, `pre`, `harga`, `sub`, `atas`? | separuh pertama atas gambar, separuh kedua harga besar |
| `desak` | `tajuk`, `sorot` | `"KENA\|CEPAT!"`, `"KUOTA TERHAD"` |
| `cta` | `tajuk` | `"MINAT?"` (sentiasa baris terakhir) |

`|` dalam `tajuk` memecah baris. Teks storyboard pendek (≤ 3 perkataan setiap kepingan): ia dipaparkan besar, bukan kapsyen.
Kunci atas: `kod`, `slug`, `produk`, `voice`, `style_tts`, `produk_img` / `produk_cut` / `produk_lineup` (di bawah `assets/img/`), `ticks` (3 baris CTA), `button`, `fine`, `video`.

## 4. Gambar realistik (Seedream)

Guna skill `seedream`. Satu gambar 9:16 (`--size 1440x2560`) untuk setiap baris dari hook hingga separuh pertama `promo`. Baris `desak` dan `cta` kekal grafik supaya harga dan butang jelas.

- **Produk**: rujukan gambar rasmi dari `brand-brain/coway/Other Brand Assets/<kategori>/<produk>/` (`--ref`). Tulis dalam prompt: "Keep the product exactly as in the reference ... small grey 'coway' wordmark only, no other text, flags or logos. Full-bleed photorealistic photo, no phone frame".
- **Hook / masalah**: rumah Malaysia, tanpa produk Coway.
- **Pakaian sopan** (peraturan user): wanita bertudung sarung dan berlengan panjang, lelaki berbaju dan berseluar panjang. Sebut dalam prompt.
- **Jana serentak**, kemudian Read setiap gambar. Tolak dan jana semula jika ada: tiada tudung, warna/bentuk produk salah, bingkai telefon, bendera/logo lain, atau fizik pelik (air paip jatuh atas mesin). Jangka ±1 daripada 2 gambar perlu dijana semula.
- Simpan dalam `assets/img/<kod>/<huruf>_<babak>.jpg` + `README.txt` (model, kos, senarai babak) dan isi `gambar` dalam storyboard.
- **Menunggu**: `until ! pgrep -f "python3 .claude/skills/[s]eedream" ...`. Tanpa `[s]`, `pgrep` turut jumpa arahan tunggu itu sendiri dan tak pernah berhenti.

## 5. Pilih 3 gaya rawak

```bash
python3 .claude/skills/coway-remake/scripts/pilih_gaya.py          # cetak 3 gaya + sebab dielak
```

Pool = 6 gaya templat (`coway`, `kinetic`, `comic`, `glow`, `paper`, `ugc`) + 15 gaya `mg:*` (bila `videos/lib/mg.js` wujud). Gaya dalam 2 remake terakhir dielakkan. Jika user minta gaya tertentu, ikut user. Tulis pilihan dalam `storyboard.json` → `"video": [{"id": "NE14", "gaya": "glow"}, ...]` (ID: kod produk 2 huruf + nombor seterusnya, lihat `coway-video`).

## 6. Suara sekali, 3 video

```bash
python3 videos/remake.py projek/<kod>/storyboard.json                 # lines.json + spec.json bagi gaya templat
python3 videos/build_video.py <ID1> --tts                             # suara SEKALI, pada video pertama
python3 voiceover/transcribe_chunks.py videos/<ID1>/vo.wav 0 99 0.35 > videos/<ID1>/chunks.txt
python3 videos/remake.py projek/<kod>/storyboard.json                 # sekali lagi: salin vo.wav/segments ke video lain
python3 .claude/skills/coway-video/scripts/semak.py <ID1> <ID2> <ID3>
```

- Gaya templat: spec dijana terus. Jangan edit `spec.json` dengan tangan, kerana ia ditulis semula setiap kali `remake.py` dijalankan. Baiki storyboard atau `videos/remake.py`.
- Gaya `mg:*`: `remake.py` hanya sediakan `lines.json` + VO. Tulis `videos/<ID>/index.html` dan `spec.json` ikut `.claude/skills/coway-video/formats/mg.md` dan prompt gaya itu. Guna teks dari storyboard (tajuk/harga/sub) supaya kandungan sama dengan 2 video lain.
- Stills: `python3 videos/build_video.py <ID> --stills 1.6,4.6,7.2,9.2,12,16.8,20.5,23,26,30.5,35` (ubah ikut masa baris dalam `segments.json`). Jubin dengan ffmpeg dan Read. Bingkai kabur atau bertindih tepat pada mula elemen biasanya hanya animasi masuk: semak semula dengan masa +0.4 s sebelum baiki.
- Semak khusus remake: teks putih atas gambar cerah (tukar ke kotak/`banner`), blok `temps` atau kad yang kena bar kapsyen (bawah ±1450 px), teks besar yang terpotong di tepi (pendekkan atau `|`).
- Render: `python3 videos/build_video.py <ID> --render --review out/<kod>`, satu demi satu (±4–5 minit setiap satu), dalam background.

## 7. Review & simpan

- Guna skill **video-review** untuk 3 video (Lulus / Perlu ubah). Baiki hanya yang "Perlu ubah".
- Tambah `!out/<kod>/` dalam `.gitignore`. Commit `projek/<kod>/`, `assets/img/<kod>/`, `videos/<ID>/`, `out/<kod>/`. Kemas kini papan status `projek/<kod>/README.md` dan satu baris "Peta repo" dalam `README.md`.

## Senarai semak akhir

- [ ] Skrip diluluskan; harga = brand-brain / disahkan user; tiada "link di bio"; `fine` ada "Tertakluk"
- [ ] Transkrip VO disemak (setiap baris disebut, Coway / nama model betul)
- [ ] 3 gaya berbeza, dari `pilih_gaya.py` atau pilihan user
- [ ] Setiap gambar Seedream disemak: pakaian sopan, produk betul, tiada teks/logo/bendera lain
- [ ] Stills setiap video disemak; tiada teks terpotong, bertindih kapsyen, atau putih atas putih
- [ ] Render siap, `semak.py` OK, review diterbitkan, papan status & README dikemas kini, di-commit
