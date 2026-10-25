# Format `mg`: 15 gaya motion graphic (mg-styles-15)

Satu video = satu halaman `videos/<ID>/index.html` yang ditulis tangan dan melukis setiap bingkai daripada masa `t`, dalam satu gaya motion design yang dikenali.
Gaya, prompt asal dan rubrik datang dari [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) (MIT), disalin ke [`reference/mg-styles-15/`](../../../../reference/mg-styles-15/README.md).
Contoh siap: **`videos/NL01FV/`** (Flat Vector, VO NL01 "3 sebab ramai pilih Neon") → `out/mg/NL01FV_3-sebab-neon-flat-vector.mp4`.

Berbanding `scenes`/`hype` (templat elemen JSON), `mg` lebih lambat dibina (±400–600 baris setiap video), tapi rupa visualnya jauh lebih kuat dan berbeza.
Untuk satu batch, bina video pertama dalam gaya itu, dapatkan kelulusan, kemudian salin `index.html` itu ke video lain dalam batch dan tukar teks, cue dan babak.

## Pilih gaya

| Gaya (`"mg"`) | Sesuai untuk Coway | Contoh sudut |
|---|---|---|
| `01-flat-vector` ✅ | Listicle, "3 sebab", ciri, harga | **NL01FV** |
| `07-liquid` ✅ | Penapis air: titisan, aliran, penapisan, "air bersih" | Neon/Villaem: titis → gelas → penapis |
| `19-paperclip` ✅ | Explainer fakta: apa dalam air paip, perbandingan, carta | RO vs Nanotrap, kos sehari |
| `08-morph` ✅ | Satu bentuk berubah sepanjang video | titis → gelas → produk → harga |
| `03-isometric` ✅ | Rumah/dapur isometrik: pemasangan, servis, aliran udara | "Technician datang ke rumah" |
| `06-collage` ✅ | Gaya kertas potong + gambar produk rasmi, mesra ibu | Ganti `hype` paper |
| `12-aurora-glass` ✅ | Premium/teknologi: UV, sensor, penapis udara | AIS, penapis udara |
| `22-hud` ✅ | "Imbasan" kualiti air/udara, sensor PM2.5 | Jerebu, penapis udara |
| `18-hanazi` ✅ | Kapsyen meriah 9:16 atas klip presenter (asal variety show Cina) | Presenter / UGC dengan klip AI |
| `02-line-art` ✅ | Minimal, satu garisan melukis produk | Villaem 3, Glaze (premium) |
| `09-bauhaus` ⚠️ | Jenama, premium; kurang mesra keluarga | |
| `10-synthwave` ⚠️ | Promo malam / 11.11 sahaja | |
| `20-pixel` ⚠️ | Gen Z, permainan | |
| `05-cel-boil` ⚠️ | Cerita lucu lukisan tangan; kerja paling berat | |
| `04-3d-render` ❌ | Perlukan Blender (tiada dalam persekitaran ini) | |

## Peraturan adaptasi (Coway mengatasi prompt asal)

Prompt asal ditulis untuk filem 10 s 16:9 tanpa jenama. Untuk iklan Coway:

- **Output:** 1080×1920, 30 fps, panjang ikut VO (`OFF + VO + 2.4 s`). Render dengan `render.py`, audio dengan `videos/build_audio.py` (muzik + SFX + VO di-duck). Jangan guna `harness/render.mjs` atau `mgaudio` dari repo asal.
- **VO dulu:** setiap beat dikunci kepada baris VO melalui `cues` dalam `spec.json`. Gambar dan bunyi baca cue sheet yang sama (seperti `cues.json` dalam repo asal).
- **Zon selamat:** kandungan 230–1440 px, logo `coway` di atas kiri (±100 px), bar kapsyen VO 1520–1690 px, nota halus 1720–1800 px. Teks penting ≥ 120 px dari atas & bawah.
- **Jenama & fakta:** abaikan "invent brand names". Guna Coway (kita ejen, jangan tulis "Coway Malaysia"). Produk mesti tepat: guna gambar rasmi (`assets/img/`, `brand-brain/coway/Other Brand Assets/`), atau ilustrasi yang setia kepada bentuk sebenar. Harga = harga dalam brief, dan penafian "Tertakluk ..." mesti ada.
- **Fon:** hanya `assets/fonts/` (Lilita One, Nunito Sans, Poppins, Anton, Bebas Neue, Bangers, Pacifico, Playfair). Fon dalam prompt asal (Fredoka, Resource Han, dsb.) tiada, jadi pilih yang paling dekat.
- **Warna:** palet gaya, dengan Coway cerulean `#04A4E4` sebagai warna utama bila gaya membenarkan.
- **Signature features wajib:** baca seksyen *Signature features and key techniques* dalam `reference/mg-styles-15/prompts/<gaya>.md` dan petakan setiap ciri kepada satu beat. Itulah yang menjadikan gaya dikenali.
- **CTA:** butang WhatsApp di hujung, dengan ≥ 1.5 s hold dan gerak mikro.

## Langkah

1. **Gaya:** ikut "Format cadangan" dalam `skrip.md`, atau gaya yang user pilih. Baca prompt gaya (Style, Creative seed, Signature features). Untuk teknik kod, rujuk `demos/<gaya>/` dalam repo asal (clone ke scratchpad): `git clone --depth 1 https://github.com/Vincentwei1021/mg-styles-15`.
2. **VO:** `spec.json` minimum (`slug voice style player:"mg" mg`), kemudian `python3 videos/build_video.py <ID> --tts`, dan semak sebutan seperti langkah 2 dalam SKILL.md. Untuk ubah gaya video sedia ada, salin `lines.json`, `segments.json` dan `vo.wav` (tak perlu TTS).
3. **Cue sheet:** dalam `spec.json` tulis `cues` (nama → `"@03%40"`) untuk setiap beat, dan `sfx` yang merujuk nama cue (`["pop", "unit1", .26, 700]`, `["whoosh", "wipe1", .2]`, `"nama+0.1"`). Jenis SFX: `whoosh pop impact shimmer tick tap lock chaching chime boom thud`. Impact pertama memulakan dram; `bpm` 100–128.
4. **Halaman:** tulis `videos/<ID>/index.html`. Mulakan dengan menyalin `videos/NL01FV/index.html` (rangka: lapisan + wipe + satu fungsi `drawN(t)` setiap babak), kemudian ganti babak ikut gaya. Jalankan `python3 videos/build_video.py <ID> --no-align` untuk menulis `timing.js`.
5. **Stills:** `python3 render.py --src videos/<ID>/index.html --stills 0.5,3,8,...` (masa video) → `out/stills/<ID>_index_t*.png`. Buka semua (Read) dan betulkan susun atur, pertindihan, teks terpotong dan zon selamat. Ulang hingga setiap still layak jadi poster.
6. **Render:** `python3 videos/build_video.py <ID> --no-align --render --review out/<kod>`, kemudian `python3 .claude/skills/coway-video/scripts/semak.py <ID>`. Buat contact sheet (ffmpeg `fps=1/1.5,tile=6x3`) untuk semak gerak keseluruhan.
7. **Kritik:** nilai sendiri dengan [`reference/mg-styles-15/rubric.md`](../../../../reference/mg-styles-15/rubric.md) (gaya, idea, gerak, reka bentuk, bunyi). Baiki skor terendah dulu, kemudian teruskan ke review (langkah 5 SKILL.md).

## Kontrak `index.html`

```html
<script src="timing.js"></script>          <!-- window.V: off, dur, lines, seg, cues, sfx (dari build_video.py) -->
<script src="../lib/engine.js"></script>   <!-- clamp mix p E set inout buildChunks caption -->
<script src="../lib/mg.js"></script>       <!-- MG.at MG.cue MG.run + spring/squash/rng/svg/tf -->
<script>
window.READY = Promise.all([document.fonts.load('400 100px Lilita'), ...]).then(() => {
  const T = MG.at, Q = MG.cue;             // T('@03%40') / Q('unit1') -> saat VO
  ... bina SVG/DOM ...
  MG.run(t => { ... lukis bingkai pada masa VO t ... });   // menetapkan seek() dan DURATION untuk render.py
});
</script>
```

- **Deterministik:** setiap bingkai fungsi tulen bagi `t`. Jangan guna `Math.random` (guna `MG.rng(seed)`), `Date`, `requestAnimationFrame`, peralihan CSS atau animasi CSS yang tak disetkan oleh `t`.
- Bina semua teks yang diukur (`measureText`) **selepas** fon dimuat, iaitu dalam `READY`.
- `#cap > #capText` dalam halaman = kapsyen VO automatik (gayakan ikut gaya; `<b>` = sorotan). Tiada `#cap` = tiada kapsyen.
- Imej: laluan relatif dari `videos/<ID>/` (`../../assets/img/...`). Pastikan sudah dimuat sebelum `READY` selesai.
- Pembantu `mg.js`: `E.pop` (cubic-bezier .34,1.56,.64,1), `E.outQt`, `E.outX`, `E.inB`; `MG.squash(t, t0, {amt})` → `[skala, squash]` untuk pop spring dengan squash & stretch; `MG.spring`, `MG.inv`, `MG.hump`, `MG.svg`, `MG.tf`.
- Corak dalam NL01FV yang boleh diguna semula: **shape wipe** (bulatan warna + `clipPath` yang sama bagi babak seterusnya, jadi tiada crossfade), `letters()` (huruf pop berselang), `popAt()` (pop dengan paksi), lukisan Neon rata `neon()`.

## Kos

NL01FV (26 s): ±500 baris HTML/JS, 4 pusingan stills, render 48 s (`--jobs 4`). Untuk 10 video dalam satu gaya, kebanyakan kod boleh diguna semula; babak yang berubah ialah kandungan, bukan enjin.

Idea prompt lain (703 video Opus, termasuk iklan produk 9:16 dan explainer): [`reference/opus-video-prompts.md`](../../../../reference/opus-video-prompts.md).
