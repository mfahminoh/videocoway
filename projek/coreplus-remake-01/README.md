# Coway Core Plus × remake TikTok "tangki paling besar" — coreplus-remake-01

Asal: video TikTok kreator lain (penyampai + footage Core Plus, 66 s), diberi user 25/10/2026. Skrip sama, suara baru, 3 gaya rawak (`coway-remake`).

| Langkah | Status | Fail | Nota |
|---|---|---|---|
| Skrip | ✅ | skrip.md | diluluskan 25/10 |
| Storyboard + gambar | ✅ | storyboard.json, assets/img/coreplus-remake-01/ | 9 gambar Seedream (14 dijana, 5 ditolak) |
| Video CP01 glow | ⏳ review v2 | out/coreplus-remake-01/CP01_tangki-paling-besar-glow.mp4 | 57.4 s |
| Video CP02 papercut | ⏳ review v2 | out/coreplus-remake-01/CP02_tangki-paling-besar-paper.mp4 | 57.4 s |
| Video CP03 mg 08-morph | ⏳ review v2 | out/coreplus-remake-01/CP03_tangki-paling-besar-morph.mp4 | 57.4 s, `videos/CP03/index.html` ditulis tangan |
| Review | ⏳ v2 | https://claude.ai/artifact/Wnp8sPfHCpuQFUQ3Lyasjb | v1 "perlu ubah" (26/10), v2 menunggu |
| Iklan | — | | CTA WhatsApp ejen |

## Keputusan
- 25/10: tiada harga, ±60 s, UV versi lembut, suara perempuan (Aoede), CTA WhatsApp. (user)
- 25/10: gaya rawak `pilih_gaya.py`: glow, paper, mg:08-morph (kinetic/comic/coway dielak, dipakai neon-p1-01). (Claude)

- 25/10: Gemini habis kuota harian audio (tier percuma) → skrip dari kapsyen; VO dijajar ikut jeda (`coway-remake/scripts/jajar_jeda.py`), semua build guna `--no-align`. (Claude)

- 25/10: CP01–CP03 diluluskan dalam chat, kemudian ditanda "perlu ubah" dalam halaman review (26/10): "gambar produk terlalu tinggi, faucet semua salah, ikut spec dan bentuk yang sama". (user)
- 26/10: v2: 8 gambar produk dijana semula ikut spec 320 × 488 × 1260 mm (paras dada) dan faucet sebenar (muncung bulat rata + pemetik leper); lukisan Core Plus dalam CP03 dilukis semula ikut lukisan spec; ketiga-tiga video dirender semula. (Claude)

## Terbuka
- [ ] User dengar VO: sebutan "Coway" / "Core Plus", dan masa kapsyen baris 01 (hook) & 07 (touch panel) yang ditanda ragu oleh penjajaran.
- [ ] "Waranti sepanjang tempoh kontrak": dakwaan dari video asal, sahkan dengan HQ sebelum iklan.
- [ ] `brand-brain/coway/products.md` tulis Core Plus "RO" tanpa UV; laman Coway kata ada UV-Sterilisation (langkah 6). Kemas kini fail fakta.
