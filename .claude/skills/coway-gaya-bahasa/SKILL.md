---
name: coway-gaya-bahasa
description: Gaya bahasa Melayu untuk SEMUA copy iklan Coway kepada pelanggan (primary text, headline, tajuk poster, skrip video, variasi bank autopilot) — santai, pendek, macam ejen WhatsApp kawan, guna bahasa pelanggan sebenar, bukan terjemahan Inggeris. Guna setiap kali menulis atau menyemak copy Coway, bila user kata copy "kaku", "tak smooth", "macam translate", "tak mesra BM", atau minta tulis semula gaya bahasa. Skill lain (coway-skrip, coway-poster, coway-iklan, coway-autopilot) mesti ikut skill ini.
---

# Gaya bahasa Coway

Copy ditulis oleh **ejen Coway yang bercakap dengan kawan**, bukan oleh syarikat atau copywriter. Kalau ejen tak akan taip ayat itu dalam WhatsApp, ayat itu salah.

Fail dalam folder ini:
- `semak_gaya.py`: penyemak automatik (frasa kaku, ayat panjang, emoji, "anda", T&C). **Wajib lulus (tiada 🔴) sebelum copy ditunjuk kepada user atau masuk bank.**
- `bank-bahasa.md`: frasa sebenar pelanggan (dari riset) + copy iklan yang menang. Ambil hook dari sini dulu.
- `semakan-ejen.md`: soalan dan mesej untuk minta ejen/pelanggan baca copy.

## Bukti dari akaun sendiri (Coway Azzuddin, Okt–Nov 2026)

| Copy | Gaya | Kos/mesej |
|---|---|---|
| "Abang, bila lagi nak pasang Coway?" 😂 (poster G1) | dialog, kelakar, ayat pendek | **RM8.90** |
| "Bau ikan dalam peti? Dah tak ada." (peti ais) | 2 ayat pendek, soalan → jawapan | **RM8.93** |
| "Satu peti. Empat suhu." / "Simpan semua. Segar lama." | 2–3 perkataan setiap ayat | RM15 |
| "Jom kenali Coway NeoN, pilihan penapis air untuk kemudahan air minuman di rumah." (B1) | panjang, kaku, terjemahan | RM35 |
| "Sesuai dipertimbangkan untuk dapur yang mempunyai ruang terhad." (D1) | bahasa brosur | RM34 |
| "Coway Neon ni model paling laris tahun 2026 ni." | dakwaan kosong | 0 mesej / RM63 |

Sampel kecil (1–7 mesej setiap iklan). Ia petanda, bukan bukti muktamad. Tapi arahnya konsisten: **pendek dan bunyi macam orang bercakap menang.**

## 10 peraturan

1. **Tulis dalam BM dari awal.** Ambil *idea* iklan luar negara, bukan ayatnya. "Goodbye X / Hello Y" → "Dulu: X. Sekarang: Y." "This is your sign" → "Kalau dah lama survey, ni masanya."
2. **Hook = ayat yang pelanggan sendiri sebut.** Cari dalam `bank-bahasa.md` dulu ("mls nk pening masak air" → "Malas nak pening masak air?").
3. **Ayat pendek.** Satu idea satu ayat, ±12 perkataan. Hook ≤ 8 perkataan. Tajuk poster ≤ 6 perkataan.
4. **Bahasa lisan, ejaan penuh.** Guna: tak, nak, dah, je, lah, kan, tau, pun, kena, ke, ni, tu, macam, ngam, takpe. Jangan singkatan SMS (x, nk, dh, sbb) dalam iklan.
5. **Panggil orang, jangan "anda".** Ikut situasi: "Abang", "Mak-mak", "Puan", "awak", atau tiada kata ganti langsung. "Anda" hanya dalam T&C.
6. **Sebut benda sebenar, bukan kategori.** ✗ "Pelbagai pilihan suhu air" ✓ "Panas, sejuk, suhu bilik. Tekan je." ✗ "Rekaan kompak" ✓ "Kecik, sejengkal je."
7. **Harga terus dan ringan.** "RM20 sebulan je*" · "Siap hantar & pasang free*". Bukan "Pakej serendah RM20 sahaja!*"
8. **CTA bunyi macam ejen.** ✓ "WhatsApp saya, saya kira pakej yang ngam untuk rumah awak." ✓ "Tanya dulu pun takpe." ✗ "Klik WhatsApp untuk dapatkan maklumat lanjut sekarang!"
9. **Emoji maksimum 3.** Satu pada hook, satu-dua pada senarai. Bukan setiap baris.
10. **English yang orang Malaysia memang guna, boleh.** filter, promo, install, worth it, free, upgrade, servis. Elak istilah marketing (premium experience, lifestyle, elevate).

**Saiz & sorotan NeoN (keputusan user 12 Nov 2026):** jangan sebut ukuran dalam cm; kalau perlu, "sejengkal je". Setiap poster NeoN mesti sorot **panas, sejuk, suhu bilik** dan **5 pilihan warna**.

Peraturan fakta tetap terpakai (brand-guide, brief, `projek/*/brief.md`): harga yang disahkan sahaja, tiada dakwaan kesihatan/terlaris/bukti sosial palsu, `*Tertakluk terma & syarat.` di hujung.

## Frasa kaku → ganti

Senarai penuh (sumber tunggal): `python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py --senarai`. Yang paling kerap muncul dalam copy lama:

| Kaku | Ganti |
|---|---|
| Jom kenali Coway NeoN | Ni Coway NeoN. / Coway NeoN ni... |
| pilihan penapis air untuk kemudahan air minuman | senang nak minum air |
| sesuai dipertimbangkan untuk dapur yang mempunyai ruang terhad | ngam untuk dapur sempit |
| bagaimana pula dengan keperluan air minuman? | habis tu, air minum macam mana? |
| Klik WhatsApp untuk dapatkan maklumat lanjut | WhatsApp saya, tanya je dulu |
| Tak perlu terus buat keputusan | Tanya dulu pun takpe. |
| sedia bila-bila masa | nak bila-bila pun ada |
| Selamat tinggal X / Hello Y | Dulu: X. Sekarang: Y. |
| X? Nah, Y. | X? Tak payah dah. / X? Dah tak zaman. |
| sahaja / tidak / hendak / sudah / apabila / sekiranya | je / tak / nak / dah / bila / kalau |

## 4 bentuk copy yang menang

**A. Pendek (peti ais, RM8.93):** hook 2 bahagian → 1 ayat produk → harga → CTA.
```
Bau ikan dalam peti? Dah tak ada. 🐟
Coway Peti Ais Dual Hygiene ada Silver Ion dan penapis bau.
RM79 sebulan, rebat RM20 x 7 bulan*.
WhatsApp saya, saya semak pakej untuk awak.
*Tertakluk terma & syarat.
```

**B. Dialog (G1, RM8.90):** petikan dialog → 2–3 ayat situasi lucu → produk 1 baris → harga → CTA.
```
"Abang, bila lagi nak pasang Coway?" 😂
Dah tiga kali tanya. Abang buat-buat tak dengar.
Coway NeoN: panas, sejuk, suhu bilik. 5 pilihan warna.
RM20 sebulan je, siap hantar & pasang free*.
WhatsApp saya sebelum hint keempat sampai.
*Tertakluk terma & syarat.
```

**C. Dulu / Sekarang:** dua baris kontras → produk → harga.
```
Dulu: angkut air botol tiap minggu.
Sekarang: tekan je, air terus keluar.
Coway NeoN, RM20 sebulan je*.
*Tertakluk terma & syarat.
```

**D. Cerita ejen:** "Customer saya semalam..." → masalah dia → apa jadi lepas pasang → tawaran. (Hanya cerita yang betul berlaku; jika lakonan, jangan guna nama.)

## Cara kerja setiap kali menulis copy

1. Baca brief/tawaran yang disahkan.
2. Pilih 1–2 frasa pelanggan dari `bank-bahasa.md` untuk hook.
3. Tulis ikut salah satu bentuk A–D. Pendek dulu; tambah hanya jika perlu.
4. Baca kuat (dalam kepala): ada ayat yang tersekat? Tulis semula.
5. Jalankan `semak_gaya.py`. Baiki semua 🔴; 🟡 boleh kekal jika ada sebab.
6. Tunjuk kepada user. Jika ejen boleh dihubungi, guna `semakan-ejen.md`.

## Tambah bahasa dari chat WhatsApp (sumber paling kuat)

Bila user beri export chat WhatsApp lead (.txt / .zip):
1. Simpan dalam `research/whatsapp/` (folder ini **diabaikan git**: repo awam, chat ada nama & nombor).
2. Ambil mesej pertama & kedua pelanggan sahaja. Buang nama, nombor, alamat.
3. Tag setiap mesej: soalan harga / bantahan / pencetus (pindah rumah, baby, rosak) / cara lama (masak air, botol, filter murah).
4. Masukkan frasa yang berulang (≥ 2 orang) ke `bank-bahasa.md` bahagian "WhatsApp", **tanpa maklumat peribadi**, dengan tarikh dan bilangan.
