# Projek video Coway

Satu folder satu projek: `projek/<kod>/`. `<kod>` = produk + persona + nombor, huruf kecil-sengkang, contohnya `neon-p1-01`, `tilam-p2-01`, `aircond-p2-01`.

Setiap skill membaca fail dari langkah sebelumnya dan menulis failnya sendiri. Sesi baru mula dengan membaca `projek/<kod>/README.md`.

```
projek/<kod>/
├── README.md      # papan status: langkah, fail, keputusan, perkara terbuka (setiap skill kemas kini)
├── brief.md       # coway-persona-produk: persona → produk → sudut, harga disahkan, format video
├── skrip.md       # coway-skrip: batch skrip (10 setiap batch), status kelulusan
├── threads.md     # coway-threads: post Threads jual pakej + pelan posting
└── poster/        # coway-poster: sumber HTML / prompt Seedream (PNG siap dalam out/<kod>/poster/)
videos/<ID>/       # coway-video: lines.json, spec.json, vo.wav (satu folder satu video)
out/<kod>/         # video siap (*.mp4) dan poster/ (*.png). Tambah `!out/<kod>/` dalam .gitignore
research/          # coway-riset: persona.md (induk) + satu fail satu topik
```

## Aliran

| # | Skill | Baca | Tulis |
|---|---|---|---|
| 1 | `coway-riset` | soalan riset, data (chat, komen, iklan) | `research/<topik>.md`, `research/persona.md` |
| 2 | `coway-persona-produk` | `research/persona.md`, `brand-brain/coway/products.md` | `projek/<kod>/brief.md`, `README.md` |
| 3 | `coway-skrip` | `brief.md`, `research/*` | `projek/<kod>/skrip.md` |
| 4 | `coway-video` | `skrip.md` (diluluskan) | `videos/<ID>/`, `out/<kod>/*.mp4`, halaman review |
| 5 | `coway-poster` | `brief.md`, `skrip.md`, video siap | `projek/<kod>/poster/`, `out/<kod>/poster/*.png` |
| 6 | `coway-threads` | video + poster siap, pakej | `projek/<kod>/threads.md`, `promo/<kod>/pelan.html` |
| 7 | `coway-iklan` (+ `coway-onboarding-klien`, `coway-ads-audit`, `coway-ads-dashboard`) | video / poster diluluskan | kempen Meta (paused → aktif selepas user sahkan), keputusan audit |

## Templat `projek/<kod>/README.md`

```markdown
# <Produk> × <Persona> — <kod>

| Langkah | Status | Fail | Nota |
|---|---|---|---|
| 2 Brief | ✅ / ⏳ / — | brief.md | |
| 3 Skrip batch 1 (01–10) | | skrip.md | diluluskan <tarikh> |
| 4 Video batch 1 | | out/<kod>/ | review: <url> |
| 5 Poster | | out/<kod>/poster/ | |
| 6 Threads | | threads.md | |
| 7 Iklan | | | akaun, kempen |

## Keputusan
- <tarikh>: <apa diputuskan, oleh siapa>

## Terbuka
- [ ] <perkara yang menunggu user / data>
```
