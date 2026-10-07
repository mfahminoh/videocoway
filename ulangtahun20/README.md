# Coway Neon — Promosi Ulangtahun ke-20 (video 20 saat, 9:16)

Arahan projek penuh: `CLAUDE.md`. Data: `data/videos.csv` (copy), `data/clips.csv` (tag asal), `data/brand.json`.

## Video siap
`out/S1-V01-v1.mp4` … (nama ikut lajur `file`). Contact sheet (1.5s, 5s, 9s, 14s, 18s): `out/sheets/V01.jpg`. QC: `out/qc.csv`.

## Aliran
| Langkah | Skrip | Hasil |
|---|---|---|
| Muat turun klip Drive | `scripts/fetch_sources.py` | `sources/` (tidak di-commit) |
| Imbas klip | `scripts/scan_sources.py`, `scan_sheets.py`, `scan_seconds.py` | `out/scan/semakan_klip.csv` |
| Tetingkap klip yang dibenarkan | (manual, dari jalur 1 saat) | `data/clip_segments.csv` (`neon=1` = boleh di shot RM20) |
| Voiceover | ElevenLabs "Aisyah – Patient Malay School Tutor" (`eleven_multilingual_v2`) → `audio/el/V01.mp3`; `scripts/el_get.py V01 <url>` potong ikut ayat | `audio/V01.wav` + `audio/V01.json` (masa ayat) |
| Rancang shot | `scripts/plan.py` | `out/_build/V01.json` |
| Render | `scripts/render.py V01-V15` | mp4 + contact sheet |
| QC | `scripts/qc.py V01-V15` | `out/qc.csv` |

Templat: `templates/overlay.html` + `overlay.css` + `overlay.js` (enjin, `window.__render(t)` deterministik) + `styles.js` (S1–S8).
Muzik & SFX disintesis dalam `scripts/audio_mix.py` (tiada lesen pihak ketiga), muzik direndahkan bila VO bercakap, loudnorm -14 LUFS.

## Keputusan yang diluluskan pengguna
- Tag klip ikut `out/scan/semakan_klip.csv` (bukan tag asal). Klip dengan kapsyen/harga tertanam tidak digunakan langsung.
- `[x]` = 25 Okt 2026 tolak tarikh render (render 7 Okt → **18 hari**). `[5]` = 5.
- Suara: ElevenLabs Aisyah.

## Peraturan dikuatkuasa automatik
1. Babak yang ada "RM20" (teks atau sarikata) tanpa "7 bulan pertama" → chip "7 bulan pertama" ditambah.
5. Shot yang bertindih teks RM20 hanya guna tetingkap klip `neon=1`.
2/3/4 disemak dalam `scripts/qc.py`.
