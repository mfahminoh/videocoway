# Panduan untuk Codex (copywriting iklan Coway)

Codex ialah penulis copy utama untuk iklan dalam repo ini (keputusan user, 19 Nov 2026). Claude Code menguruskan poster, video, render dan pelancaran iklan, dan memanggil Codex untuk copy. Fail ini ialah arahan projek untuk Codex. Arahan Claude ada dalam `CLAUDE.md`.

## Bisnes ini

User ialah pembuat kandungan untuk **ejen Coway** (bukan Coway Malaysia). Dua sumber jualan:

1. **Servis iklan untuk ejen:** iklan Meta di akaun iklan ejen, CTA ke WhatsApp ejen.
2. **Jual pakej video kepada ejen:** pakej video siap, dijual melalui post Threads dan poster di page user sendiri.

**Jangan campur dua audiens ni:**
- Iklan, poster, skrip video, caption iklan Threads/Meta → **pelanggan akhir** (keluarga).
- Post Threads jual pakej, poster pakej → **ejen Coway**.

Dalam iklan, kita **ejen sah Coway**, bukan syarikat. Bercakap sebagai orang ("saya", "customer saya"). Jangan guna nama "Coway Malaysia", Careline atau WhatsApp rasmi Coway.

## Gaya bahasa (wajib untuk semua copy kepada pelanggan)

Sumber penuh: `.claude/skills/coway-gaya-bahasa/SKILL.md`. **Baca fail tu dan `bank-bahasa.md` sebelum menulis.**

Ringkasnya: copy ditulis macam **ejen Coway WhatsApp kawan**. Kalau ejen tak akan taip ayat tu dalam WhatsApp, ayat tu salah.

1. Tulis terus dalam BM. Ambil idea iklan luar, bukan ayatnya. Jangan terjemah.
2. Hook = ayat yang pelanggan sendiri sebut. Cari dalam `.claude/skills/coway-gaya-bahasa/bank-bahasa.md` dulu.
3. Ayat pendek: ±12 perkataan satu ayat. Hook ≤ 8 perkataan. Tajuk poster ≤ 6 perkataan.
4. Bahasa lisan, ejaan penuh: tak, nak, dah, je, lah, ni, tu, macam, ngam, takpe. **Jangan** singkatan SMS (x, nk, dh, sbb).
5. Jangan guna "anda" (kecuali T&C). Panggil "awak", "Abang", "Mak-mak", "Puan", atau tiada kata ganti.
6. Sebut benda sebenar, bukan kategori. ✗ "Pelbagai pilihan suhu air" ✓ "Panas, sejuk, suhu bilik. Tekan je."
7. Harga terus dan ringan: "RM20 sebulan je*", "Siap hantar & pasang free*". Bukan "Pakej serendah RM20 sahaja!"
8. CTA bunyi macam ejen: "WhatsApp saya, tanya dulu pun takpe." Bukan "Klik WhatsApp untuk maklumat lanjut!"
9. Emoji maksimum 3: satu pada hook, satu-dua pada senarai.
10. English yang orang Malaysia memang guna boleh (filter, promo, install, worth it, free, servis). Elak istilah marketing (premium experience, lifestyle, elevate).

Frasa kaku yang mesti ditukar: `python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py --senarai`.

**4 bentuk copy yang menang** (contoh penuh dalam SKILL.md): A. Pendek (hook 2 bahagian → produk 1 ayat → harga → CTA), B. Dialog ("Abang, bila lagi nak pasang Coway?" 😂), C. Dulu / Sekarang, D. Cerita ejen (hanya cerita benar).

## Fakta & harga

- Fakta produk: `brand-brain/coway/products.md`, `brand-brain/coway/brand-guide.md`, dan `projek/<kod>/brief.md`. Jangan reka spek.
- **Tiada** dakwaan kesihatan, "paling laris", testimoni atau bukti sosial palsu.
- Harga hanya yang disahkan dalam brief/README projek. Kalau tak pasti, tulis `[HARGA?]` dan beritahu.
- Setiap copy yang ada harga atau tawaran mesti berakhir dengan: `*Tertakluk terma & syarat.`
- Dakwaan UV 99.9% mesti disertai: "Berdasarkan ujian TÜV SÜD Korea dalam persekitaran terkawal."

### Coway NeoN (keputusan user)
- Jangan sebut ukuran dalam cm. Kalau perlu: "kecik, sejengkal je".
- Setiap copy/poster NeoN mesti sorot **panas, sejuk, suhu bilik** dan **5 pilihan warna**.
- Tawaran semasa (disahkan 4 Nov 2026): **RM20 sebulan + hantar & pasang free**. Sahkan dalam README projek sebelum guna.

## Format serahan copy iklan

Simpan dalam `projek/<kod>/copy.md` (atau fail yang diminta). Untuk setiap iklan:

```
## <ID> · <sudut ringkas>
**Primary text:**
<HOOK>
<2–4 baris badan>
<harga>
<CTA>
*Tertakluk terma & syarat.

**Headline:** <≤ 6 perkataan>
**Teks poster (jika ada):** <tajuk ≤ 6 perkataan / label panel>
```

Untuk iklan Threads gaya hook huruf besar: baris hook ditulis HURUF BESAR, badan dalam huruf biasa.

## Sebelum serah (wajib)

1. Jalankan penyemak: `python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py projek/<kod>/copy.md`
2. Baiki semua 🔴. 🟡 boleh kekal jika ada sebab (contohnya baris nota dalaman).
3. Baca kuat dalam kepala: ada ayat yang tersekat? Tulis semula.

## Peraturan repo

- Jangan ubah fail di luar fail copy yang diminta, kecuali user minta.
- Jangan commit atau push melainkan user minta. Claude Code menyemak dan commit.
- Data klien dan chat WhatsApp (`ads/autopilot/data/`, `research/whatsapp/`) kekal lokal. Jangan salin nama atau nombor pelanggan ke dalam copy.
