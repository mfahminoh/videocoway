# Panduan untuk Claude

## Bisnes ini

User ialah pembuat kandungan untuk **ejen Coway** (bukan Coway Malaysia). Dua sumber jualan:

1. **Servis iklan untuk ejen:** ejen bayar user untuk jalankan iklan Meta di akaun iklan ejen, guna video dari repo ini (CTA ke WhatsApp ejen).
2. **Jual pakej video kepada ejen:** pakej video siap (contohnya WP RM68 / Tilam RM68 / Combo RM110 / AP vs Jerebu RM30), dijual melalui post Threads dan iklan poster di page user sendiri.

Jangan campur dua audiens ni: video & poster **iklan** bercakap kepada pelanggan akhir (keluarga). Post **Threads** dan poster pakej bercakap kepada **ejen Coway**.

## Gaya bahasa

Semua copy kepada pelanggan (iklan, poster, skrip, bank autopilot) ikut skill `coway-gaya-bahasa`: macam ejen WhatsApp kawan, ayat pendek, bahasa pelanggan sebenar, bukan terjemahan. Penyemak: `.claude/skills/coway-gaya-bahasa/semak_gaya.py`.

**Copywriting iklan ditulis oleh Codex** (pilihan user, 19 Nov 2026). Arahan Codex: `AGENTS.md`. Panggil dari Bash, contohnya:
`codex exec --sandbox workspace-write "Tulis copy iklan untuk projek/<kod> ... simpan dalam projek/<kod>/copy.md" < /dev/null`
Claude semak hasilnya dengan `semak_gaya.py` dan fakta/harga, kemudian guna dalam poster atau iklan dan commit. Kalau `AGENTS.md` dan skill gaya bahasa berubah, pastikan kedua-duanya selari.

## Aliran kerja projek video

Satu skill satu langkah. Fail serahan dan struktur folder: [`projek/README.md`](projek/README.md).

`coway-riset` → `coway-persona-produk` → `coway-skrip` → `coway-video` → `coway-poster` → `coway-threads` → `coway-iklan` (guna `coway-onboarding-klien`, `coway-ads-audit`, `coway-ads-dashboard`)

- Mula setiap sesi projek dengan membaca `projek/<kod>/README.md` (papan status), dan kemas kini papan tu sebelum tamat.
- Video dihasilkan 10 sebatch. Batch seterusnya hanya selepas batch semasa diluluskan.
- Remake video TikTok (skrip sama, suara baru): `coway-remake` → `coway-video`. Satu batch remake = 1 video rujukan × 3 gaya berbeza (rawak).
- Semua kerja di-commit dan digabung ke `main`.

## Meta Ads

- **Autopilot harian:** skill `coway-autopilot` (fail `ads/autopilot/`). Ia pause iklan kalah dan ganti dengan kreatif `LULUS` dari `ads/autopilot/bank.json` dalam ad set yang sama, tanpa naikkan bajet. Peraturan dan akaun dalam `ads/autopilot/daftar.json`. `ads/neon_autopilot.json` ialah rekod lama (Okt 2026).
- **Struktur kempen 1-1-1:** setiap kempen ada 1 ad set dan 1 iklan sahaja. Kalau ada 3 video, buat 3 kempen berasingan (satu video satu kempen), bukan 3 iklan dalam satu ad set. Bajet yang user beri "untuk 1 kempen" ialah bajet setiap kempen.
