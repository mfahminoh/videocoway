---
name: coway-threads
description: Tulis kempen Threads untuk menjual pakej video Coway kepada ejen (post 2 bahagian isu → jualan, ≤ 500 aksara) dan bina content planner — jadual posting Threads user dengan copy, poster/video dan butang salin (pelan.html). Guna bila user minta post Threads, copywriting Threads, kempen jual pakej video, pelancaran pakej, content planner / jadual posting Threads, atau "nak post apa hari ni".
---

# Threads: jual pakej video + content planner

Audiens: **ejen Coway** (bukan pelanggan akhir). Tujuan: ejen komen/DM untuk beli pakej video.
Input: video siap `out/<kod>/`, poster jenis B dari `coway-poster`, maklumat pakej.
Output: `projek/<kod>/threads.md` (copy), `promo/<kod>/` (posts.json → `pelan.html` + poster), papan status langkah 6.

## 1. Pakej

Sahkan dengan user (sekali): nama pakej, kandungan (bilangan video, model), harga, had slot, kata kunci komen, tempoh kempen.
Pakej sedia ada (rujukan harga & gaya): WP (Neon, Neo Plus, Villaem 3) 30 video RM68 · Tilam (Prime, Prime Lite) 30 video RM68 · Combo 60 video RM110 · AP vs Jerebu 15 video RM30 (terhad 25 orang).
Contoh kempen: `threads/posting_10hari_afifuddeen.md` (10 hari, post 2 bahagian), `promo/threads/posts.json` (AP vs Jerebu, 10 post).

## 2. Pelan posting (content planner)

Lalai: **10 hari, 1–2 post sehari** (pagi ±8.30 pg, malam ±8.30 mlm). Campuran sepanjang kempen:

| Jenis | Contoh sudut | Media |
|---|---|---|
| Pelancaran | "Pakej X dah siap: N video, RMxx" | Poster utama |
| Pain ejen | Story kosong 3 hari, tak tahu nak post apa, prospek lupa | Bingkai video / tiada |
| Isu semasa | Jerebu, musim panas, promo bulan ni: kenapa pelanggan cari sekarang | Video sampel |
| Bukti | Sampel video penuh, "ni contoh video no 7", hasil ejen yang guna | Video sampel |
| Bantahan | "Boleh buat sendiri guna Canva", "video sama dengan ejen lain?" | Poster/teks |
| Kandungan pakej | Senarai video, persona, sudut yang dicover | Grid poster |
| Desakan | Tinggal N slot, harga naik esok, last call | Poster slot (10/5/3) |

Peraturan copy:
- **≤ 500 aksara setiap post** (had Threads). Kira dan papar.
- Post 2 bahagian: **1/2** angkat isu/cerita (tiada jualan); **2/2** balasan pada post sendiri: pakej + harga + CTA. Post yang memang menjual boleh satu bahagian.
- Nada Threads santai ("aku/kau" atau "saya/korang", ikut kempen lepas), ayat pendek, senarai `+` atau `✅`, 1–2 emoji.
- CTA konsisten: "Komen "<KATA>" atau DM saya".
- Jangan janji hasil jualan; boleh cerita pengalaman sebenar user.
- Gaya penulis tertentu (contohnya "thread-afifuddeen-1-style") hanya jika user minta dengan nama.

## 3. Fail

`projek/<kod>/threads.md`: jadual pelan (hari, masa, jenis, media) + copy penuh setiap post (1/2 dan 2/2).

Halaman pelan dengan butang salin, guna semula pembina sedia ada:

```bash
mkdir -p promo/<kod>/out && cp promo/threads/build_page.py promo/<kod>/
# tulis promo/<kod>/posts.json: [{"n", "day", "type", "tag", "media": ["p01.png" | "sampel.mp4"], "text", "reply"?}]
# letak media dalam promo/<kod>/out/ (poster dari coway-poster, video sampel dari out/<kod>/)
python3 promo/<kod>/build_page.py        # -> promo/<kod>/pelan.html
```

Terbitkan `pelan.html` sebagai artifact peribadi (dengan `promo/<kod>/out/*` sebagai fail sokongan), supaya user boleh buka di telefon dan salin setiap post. Video sampel dalam artifact: guna salinan 720p yang kecil.

## 4. Semak

- [ ] Setiap post ≤ 500 aksara; balasan 2/2 juga ≤ 500
- [ ] Harga, kandungan pakej dan had slot sama dalam semua post & poster
- [ ] Bercakap kepada ejen (bukan pelanggan akhir); tiada copy iklan pelanggan dicampur
- [ ] Setiap hari ada media; video sampel dari pakej sebenar
- [ ] CTA dan kata kunci komen konsisten

Commit, kemas kini papan status (langkah 6), dan beri user pautan pelan + post hari pertama.
Untuk iklan berbayar yang menjual pakej (page user sendiri), guna poster jenis B dan aliran iklan dalam `CLAUDE.md` (1 kreatif = 1 kempen).
