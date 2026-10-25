# mg-styles-15: 15 gaya motion design (rujukan)

Sumber: [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15), commit `49052d8`, lesen MIT ([`LICENSE`](LICENSE)). Tonton semua 15 filem: https://vincentwei1021.github.io/mg-styles-15/

Lima belas filem 10 s, satu gaya setiap satu, semuanya ditulis sebagai kod (SVG / Canvas / WebGL / Three.js) oleh Claude. Repo ini menyimpan bahagian yang kita perlukan untuk menghasilkan video Coway dalam gaya-gaya itu:

| Fail | Isi |
|---|---|
| `prompts/<gaya>.md` | Prompt penuh setiap gaya: Style, Creative seed, **Signature features** (ciri yang wajib ada), cara kerja, senarai semak juri. Arahan dalam bahasa Cina; prompt dalam English |
| `rubric.md` | Prompt juri untuk menilai filem (7 dimensi, skor 1–10) dan pusingan pembaikan |
| `template.md` | Templat untuk menulis prompt gaya baru (4 seksyen) |

Tidak disalin (besar, rujuk terus di GitHub atau clone ke scratchpad): `demos/<gaya>/` (kod sumber setiap filem, 64 MB), `videos/` (420 MB), `lib/audio` (mgaudio + 103 sampel instrumen), `harness/render.mjs`. Pipeline kita guna `render.py` dan `videos/build_audio.py`.

Cara guna untuk iklan Coway (adaptasi 9:16, VO, jenama, fon): [`.claude/skills/coway-video/formats/mg-gaya.md`](../../.claude/skills/coway-video/formats/mg-gaya.md). Contoh: `videos/NL01FV/` (Flat Vector).

| # | Gaya | Fail |
|---|---|---|
| 01 | Flat Vector | `01-flat-vector.md` |
| 02 | Line Art | `02-line-art.md` |
| 03 | Isometric 2.5D | `03-isometric.md` |
| 04 | 3D Render (Blender) | `04-3d-render.md` |
| 05 | Frame-by-Frame / Line Boil | `05-cel-boil.md` |
| 06 | Collage / Cut-out | `06-collage.md` |
| 07 | Liquid Motion | `07-liquid.md` |
| 08 | Shape Morph | `08-morph.md` |
| 09 | Geometric Bauhaus | `09-bauhaus.md` |
| 10 | 80s Synthwave / VHS | `10-synthwave.md` |
| 12 | Aurora & Glassmorphism | `12-aurora-glass.md` |
| 18 | Variety Captions 9:16 (花字) | `18-hanazi.md` |
| 19 | Sticker Explainer (PaperClip) | `19-paperclip.md` |
| 20 | Pixel Art | `20-pixel.md` |
| 22 | Cyberpunk HUD / FUI | `22-hud.md` |
