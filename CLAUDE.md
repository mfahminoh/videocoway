# Panduan untuk Claude

## Bisnes ini

User ialah pembuat kandungan untuk **ejen Coway** (bukan Coway Malaysia). Dua sumber jualan:

1. **Servis iklan untuk ejen:** ejen bayar user untuk jalankan iklan Meta di akaun iklan ejen, guna video dari repo ini (CTA ke WhatsApp ejen).
2. **Jual pakej video kepada ejen:** pakej video siap (contohnya WP RM68 / Tilam RM68 / Combo RM110 / AP vs Jerebu RM30), dijual melalui post Threads dan iklan poster di page user sendiri.

Jangan campur dua audiens ni: video & poster **iklan** bercakap kepada pelanggan akhir (keluarga). Post **Threads** dan poster pakej bercakap kepada **ejen Coway**.

## Aliran kerja projek video

Satu skill satu langkah. Fail serahan dan struktur folder: [`projek/README.md`](projek/README.md).

`coway-riset` → `coway-persona-produk` → `coway-skrip` → `coway-video` → `coway-poster` → `coway-threads` → `coway-iklan` (guna `coway-onboarding-klien`, `coway-ads-audit`, `coway-ads-dashboard`)

- Mula setiap sesi projek dengan membaca `projek/<kod>/README.md` (papan status), dan kemas kini papan tu sebelum tamat.
- Video dihasilkan 10 sebatch. Batch seterusnya hanya selepas batch semasa diluluskan.
- Semua kerja di-commit dan digabung ke `main`.

## Meta Ads

- **Struktur kempen 1-1-1:** setiap kempen ada 1 ad set dan 1 iklan sahaja. Kalau ada 3 video, buat 3 kempen berasingan (satu video satu kempen), bukan 3 iklan dalam satu ad set. Bajet yang user beri "untuk 1 kempen" ialah bajet setiap kempen.
