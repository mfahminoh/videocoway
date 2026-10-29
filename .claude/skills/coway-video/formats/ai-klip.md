# Format klip AI: Seedance · Veo · Google Flow (manual)

Klip AI ialah **footage latar** untuk pemain `scenes`/`hype`. Enjin sedia ada menambah VO, kapsyen, harga, produk sebenar dan CTA di atasnya.
Dengan cara ini teks dan produk dalam video sentiasa tepat, kerana model AI merosakkan teks dan bentuk produk.

```
skrip.md (lajur Visual) → senarai shot → jana klip 5–8 s → assets/clips/<kod>_sNN.mp4 → spec.json bg {"clip": "<kod>_sNN", "c0": 0, "c1": 4.5}
```

`videos/build_video.py` mencari klip dalam `assets/clips/<nama>.mp4`, jadi simpan semua klip AI di situ dengan awalan kod projek.

## Pilih enjin

| Enjin | Cara | Status (25 Okt 2026) | Sesuai untuk |
|---|---|---|---|
| **Seedance** | `scripts/seedance.py` (BytePlus ModelArk, `ARK_API_KEY`) | Key ada; **model belum diaktifkan** di Ark Console | Banyak klip sekali gus, imej → video dari gambar produk rasmi |
| **Veo (API)** | `scripts/veo.py` (Gemini API) | Key proxy **tiada akses Veo**; perlu `GEMINI_API_KEY` AI Studio berbayar | Realisme orang & suasana rumah |
| **Google Flow (manual)** | Claude tulis prompt; user jana di labs.google/flow; user muat naik klip | Sentiasa boleh | Bila API tiada, atau user nak pilih take sendiri |

Sebelum jana dengan API: jalankan `--check`, beritahu user **anggaran bilangan klip** (contoh 10 video × 3 shot = 30 klip) kerana setiap klip berbayar. Jana 1 klip ujian dulu, semak, kemudian baki.

## Senarai shot

Dari lajur **Visual** dalam `skrip.md`, pilih hanya babak yang perlukan footage hidup (2–4 setiap video). Babak harga, CTA, listicle dan infografik kekal motion graphic.
Tulis senarai dalam `projek/<kod>/shots.md`:

| Shot | Video / baris | Prompt | Imej rujukan | Enjin | Fail |
|---|---|---|---|---|---|
| s01 | TL01 / 01–02 | (prompt penuh) | — | Seedance | assets/clips/tilam-p2-01_s01.mp4 |

## Menulis prompt (sama untuk semua enjin)

Struktur: **subjek + aksi + tempat + kamera + cahaya + gaya**, satu shot, 5–8 s, potret 9:16.

```
Vertical 9:16 video. A Malaysian Malay mother in her 30s wearing a light tudung, in a modest terrace-house kitchen,
opens an old white fridge and sniffs a container of chicken curry, frowning slightly. Medium close-up, handheld,
slow push-in. Warm late-afternoon light from the window. Realistic, natural skin tones, documentary style.
No text, no logos, no subtitles.
```

Peraturan:
- **Konteks Malaysia:** orang Melayu/Malaysia, rumah teres/flat/rumah kampung, dapur dan barang tempatan. Sebut secara jelas, kerana model cenderung ke latar Barat/Korea.
- **Tiada teks dalam prompt atau klip** ("No text, no logos, no subtitles"). Semua teks datang dari enjin kapsyen.
- **Produk Coway:** jangan minta model melukis unit Coway dari teks. Sama ada (a) shot tanpa produk (masalah, emosi, suasana), atau (b) imej → video dengan gambar rasmi sebagai bingkai pertama (`--image brand-brain/coway/Other Brand Assets/.../*-front-view.jpg`), gerakan kamera kecil sahaja. Semak bentuk & logo unit setiap klip.
- Gerakan perlahan dan satu aksi sahaja. Aksi kompleks (tangan menuang, kanak-kanak berlari) kerap rosak.
- Elak muka kanak-kanak close-up dan situasi perubatan.
- Simpan `seed` take yang elok dalam `shots.md` untuk variasi.

## Seedance

```bash
python3 .claude/skills/coway-video/scripts/seedance.py --check
python3 .claude/skills/coway-video/scripts/seedance.py "<prompt>" --out assets/clips/<kod>_s01.mp4 --duration 5
python3 .claude/skills/coway-video/scripts/seedance.py "<prompt gerakan kamera>" --image "<gambar produk rasmi>" --out assets/clips/<kod>_s02.mp4
```
Model: `--model pro-fast` (lalai, paling murah), `pro`, `2.0-fast`, `2.0`, `2.5`. Ralat `ModelNotOpen` → minta user aktifkan model itu di Ark Console, kemudian ulang.

## Veo (API)

```bash
python3 .claude/skills/coway-video/scripts/veo.py --check
python3 .claude/skills/coway-video/scripts/veo.py "<prompt>" --out assets/clips/<kod>_s01.mp4
```
Jika `--check` kata tiada model, guna Google Flow manual.

## Google Flow (manual)

1. Tulis `projek/<kod>/shots.md` dengan prompt penuh, satu shot satu prompt, dan nama fail sasaran.
2. Beritahu user langkahnya: buka labs.google/flow → projek baru → **9:16** → model Veo → tampal prompt (untuk imej → video, muat naik gambar produk rasmi sebagai frame) → jana 2–4 take → muat turun take terbaik dengan nama `<kod>_sNN.mp4`.
3. User muat naik klip ke sesi (atau ke Drive). Simpan dalam `assets/clips/`, kemudian normalkan:
   ```bash
   python3 -c "import imageio_ffmpeg,subprocess,sys; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',sys.argv[1],'-an','-vf','scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',sys.argv[2]],check=True)" muat-naik.mp4 assets/clips/<kod>_s01.mp4
   ```
4. Tonton klip (stills dengan `render.py` atau ekstrak bingkai) sebelum guna. Klip 16:9 akan dipotong tengah, jadi pastikan subjek berada di tengah.

**Shot yang ada unit Coway (ujian 30 Okt 2026, promo-rm18-01):** Text to Video melukis penapis generik dengan logo rosak, dan gambar rasmi jarang sesuai terus sebagai frame 9:16 (kebanyakan 1:1 atau banner lebar, latar studio). Kaedah yang menjadi:
1. **Image → Nano Banana 2.1, 9:16** (0 kredit): lampirkan 2–3 gambar rasmi produk (butang **+** → Upload media → Add to prompt) dan tulis prompt yang menerangkan **bentuk** produk dengan perkataan (siluet, panel kawalan, paip, dulang, lubang udara, warna; tanpa ukuran mm). Semak still dengan gambar rasmi, pilih yang tiada teks rosak di latar.
2. **Video → Frames**, Start = still itu, prompt gerakan kamera perlahan + "keep exactly as shown in the first frame… rigid objects". Bentuk kekal sepanjang 8 s.
Contoh penuh dan teks bentuk setiap model: `projek/promo-rm18-01/shots.md`. Veo kadang-kadang menambah papan tanda di latar semasa push-in; jika jadi, kurangkan push-in atau tulis "plain walls, no store signage". Jangan sebut peralatan kamera ("on a gimbal") atau "bokeh": Veo melukisnya dalam bingkai. "A highlight glides across" boleh menukar warna unit gelap seketika.

## Guna dalam spec

```json
{"at": "@01", "bg": {"clip": "tilam-p2-01_s01", "c0": 0.0, "c1": 4.5}}
```
`c1 − c0` mesti sepadan dengan tempoh babak (kelajuan 0.55–1.9×). Letak tajuk/kapsyen di atas footage dengan `theme: "coway"`, dan tambah `"shade": true` pada bg jika teks sukar dibaca.
