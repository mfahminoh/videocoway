# Plan Produksi 40 Video — Penapis Air Coway (30–45 saat, portrait 1080×1920)

Rujukan gaya: video **Villaem 3** yang sedia ada dalam repo ini (`src/index.html`, `out/villaem3_final.mp4`) —
motion graphic bercerita, suara santai "content creator", tanpa footage stok, muzik + SFX dijana sendiri
(tiada isu lesen untuk Meta Ads). Semua 40 video dirancang supaya boleh **dijana terus oleh Claude (Opus)**
sebagai animasi HTML → dirender ke MP4 dengan `render.py`, tanpa kamera atau editor.

Tracker (boleh import ke Google Sheets): [`plan/senarai_video.csv`](plan/senarai_video.csv)
Video rujukan kreator lain (skrip, analisis, skrip adaptasi): [`reference/`](reference/README.md)
Sampel suara Gemini TTS untuk dipilih: [`voiceover/sampel_suara/`](voiceover/sampel_suara/)

---

## 1. Produk & pembahagian (ikut permintaan tinggi)

| Produk | Kod | Harga promo semasa* | Kekuatan utama untuk video | Bil. video |
|---|---|---|---|---|
| **Villaem 3** | V3 | RM74/bln | RO, tangki terbesar 11.4L (6.1L bilik / 2.6L sejuk / 2.7L panas), UV sterilisasi 99.9% bakteria, 8+ suhu, ECO & Dual Lock | 8 |
| **Neo Plus** | NP | RM59/bln | RO 4 peringkat, panas/sejuk/bilik (2.5L / 2.3L / 1.0L), "penapis air semua orang boleh miliki" | 7 |
| **Ais** | AIS | RM120/bln, servis percuma 7 tahun | Pembuat ais (0.7 kg), RO, Ice Lock + Hot Water Lock, sensor cahaya jimat tenaga | 6 |
| **Cinnamon** | CN | RM32/bln | Paling mampu milik, RO, air suhu bilik 5.0L, booster pump (tekanan air lemah), pilih ½ / 1 / 2 cawan | 5 |
| **Dazzie** | DZ | RM74/bln | Kompak, 4 suhu pratetap 45°C susu bayi / 70°C teh / 85°C kopi / 98°C mi segera, Nanotrap (99.999% Murine Norovirus), UV | 5 |
| **Neon** | NE | RM54/bln → RM27 (diskaun 50% × 6 bulan)† | 5 warna pastel, Nanotrap (merkuri, plumbum, besi, aluminium), Eco Mode, kunci kanak-kanak, pakej *self-service* (filter percuma setiap 8 bulan) | 5 |
| Coway umum | GEN | — | Edukasi penapis air, servis, kos, pilih model | 4 |
| | | | **Jumlah** | **40** |

† Daripada video rujukan R02–R05 (`reference/`).
\* Harga & promo berubah setiap bulan — **sahkan sebelum render**. Semua harga disimpan dalam satu fail config
(`plan/harga.json`, dicadang) supaya satu perubahan terus kemas kini semua video.

## 2. Tiga kategori kandungan

| Kategori | Bil. | Tujuan | Struktur (±40s) |
|---|---|---|---|
| **Cerita** (storytelling) | 13 | Emosi & relatable — penonton nampak diri sendiri | Hook watak 0–3s → masalah 3–12s → "jadi dia pilih…" 12–17s → 2–3 ciri 17–32s → promo 32–38s → CTA 38–42s |
| **Edukasi** | 12 | Bina kepercayaan, orang *save & share* | Soalan/fakta mengejut 0–3s → terangkan 3–25s → kaitkan dengan produk 25–35s → CTA lembut 35–40s |
| **Produk** (penerangan) | 15 | Dorong keputusan beli | Tawaran/manfaat 0–3s → demo ciri 3–28s → harga & promo 28–36s → CTA 36–40s |

Peraturan hook: **ayat pertama ≤ 2.5 saat**, teks besar dalam 0.3s pertama, tiada logo di saat pertama.

## 3. Sepuluh gaya visual (4 video setiap gaya)

Setiap gaya jadi **satu template HTML** yang boleh diguna semula — tukar teks, warna aksen & gambar produk sahaja.

| Kod | Gaya | Rupa | Sesuai untuk |
|---|---|---|---|
| **A** | Cerita Motion Graphic | Gaya Villaem 3 sedia ada: latar krim + ikon watak → tirai bulat ke gelap → produk "reveal" bercahaya | Cerita emosi |
| **B** | Chat Story | Gelembung mesej bertaip satu-satu (UI chat generik, **bukan** logo/skrin WhatsApp sebenar), watak "Customer" & "Agent Coway" | Bantah keraguan harga/keperluan |
| **C** | Kinetic Typography | Teks besar bergerak ikut rentak VO, latar warna produk, hampir tiada ikon | Iklan pendek padat, 30–35s |
| **D** | Explainer Diagram | Keratan rentas penapis/tangki, titisan air melalui lapisan, label bergerak | Teknologi (RO, UV, Nanotrap, ais) |
| **E** | Versus / Split-screen | Skrin dibelah dua, kiri kelabu "tanpa" vs kanan biru "dengan", skor naik | Perbandingan, sebelum/selepas |
| **F** | Mitos vs Fakta | Kad "MITOS" merah dipangkah → kad "FAKTA" hijau terbalik (flip) | Edukasi, patahkan salah faham |
| **G** | Infografik Nombor | Angka count-up, bar/cawan terisi, kalkulator kos | Kapasiti, kos, nilai |
| **H** | Listicle "3 Sebab / 3 Tanda" | Kad bernombor besar 1-2-3 slide masuk, tick kuning | Senarai manfaat/tanda |
| **I** | "Sehari Bersama…" | Jam berdetik pagi → malam, babak dapur/rumah berubah warna langit | Gaya hidup, keluarga |
| **J** | Kuiz / Teka | Soalan + pilihan A/B/C + kiraan detik 3-2-1 → jawapan | Engagement (komen jawapan) |

Warna aksen ikut produk (latar tetap navy/biru Coway): V3 biru langit · NP biru · AIS putih ais/cyan · CN coklat kayu manis ·
DZ hijau pudar · NE pastel (pink/mint/biru ikut warna produk).

## 4. Senarai 40 video

Lajur: **Kat** = Cerita / Edukasi / Produk · **Gaya** = kod §3 · **Suara** = §5.

### Villaem 3 (8)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| V01 | Cerita | A | 42 | "Raya tahun ni, 20 orang datang rumah mertua…" | Air habis tiap jam, cerek tak menang tangan → tahun depan pasang Villaem 3 → tangki 11.4L, panas-sejuk-bilik serentak → "raya ni tak ada siapa tunggu air" | Orus |
| V02 | Cerita | B | 40 | "Kenapa Villaem 3 lagi mahal dari model lain?" | Chat customer ragu → agent: beli sekali pakai lama, tangki terbesar, jarang rosak → customer: "ok, nak slot pemasangan" | Aoede |
| V03 | Edukasi | D | 38 | "Air dalam tangki penapis boleh basi ke?" | Bakteria dalam tangki tertutup → lampu UV menyala → 99.9% bakteria dihapuskan → Villaem 3 buat ini automatik | Kore |
| V04 | Produk | G | 35 | "11.4 liter tu banyak mana sebenarnya?" | Botol 1.5L terisi satu-satu → ±7.6 botol → pecahan 6.1/2.6/2.7L → promo | Puck |
| V05 | Produk | C | 40 | "Satu mesin, lapan suhu" *(ref R01)* | Panel LED 95/80/70 → 60/50/40 → isipadu 120ml–∞ → child lock 3s → 11.4L → harga (potong klip sendiri clip2/clip5) | Puck |
| V06 | Cerita | I | 44 | "Sehari dalam rumah keluarga 6 orang" | 6:30 pagi air suam ubat · 1 petang air sejuk balik sekolah · 8 malam air panas maggi · tangki tak pernah kosong | Orus |
| V07 | Edukasi | F | 38 | "Penapis besar = bil elektrik mahal?" | MITOS dipangkah → FAKTA: ECO Mode; + Dual Lock keselamatan anak → Villaem 3 | Kore |
| V08 | Produk | E | 42 | "Villaem 3 atau Neo Plus — mana satu untuk rumah anda?" | Kiri NP 5.8L / kanan V3 11.4L; ahli keluarga ≤3 vs 4+; "pilih ikut rumah, bukan ikut harga" | Aoede |

### Neo Plus (7)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| N01 | Cerita | A | 38 | "Baru kahwin? Ini penapis air yang saya cadangkan" *(ref R05)* | Rumah pertama → Neo Plus → 1.0/2.3/2.5L ngam berdua sampai anak pertama → RO 4 peringkat → RM59 | Aoede |
| N02 | Edukasi | D | 40 | "4 lapisan dalam Neo Plus — apa kerja setiap satu?" | Neo-Sense (sedimen + pra-karbon) → membran RO → Inno-Sense (pasca-karbon + halus) → antibakteria | Kore |
| N03 | Produk | G | 35 | "5.8 liter cukup untuk berapa orang?" | Gelas terisi mengikut isi rumah → 2.5 / 2.3 / 1.0L → sesuai 2–4 orang → promo | Puck |
| N04 | Cerita | B | 40 | "Duduk sorang, perlu ke penapis air?" | Chat pekerja bujang → agent kira: air botol + gas masak air vs RM59 → "ok la, pasang" | Orus |
| N05 | Edukasi | H | 38 | "3 tanda air paip rumah anda perlukan penapis" | 1. bau klorin 2. keladak dalam cerek 3. kerak putih → penyelesaian: Neo Plus | Kore |
| N06 | Produk | C | 30 | "Panas. Sejuk. Suhu bilik. RM59." | Kinetic laju, 3 suhu, 4 penapis, pemasangan percuma, CTA | Puck |
| N07 | Edukasi | J | 35 | "Teka: berapa lapisan penapis dalam Neo Plus?" | A) 2 B) 3 C) 4 → 3-2-1 → C → terangkan ringkas → "komen jawapan anda" | Aoede |

### Ais (6)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| A01 | Cerita | E | 42 | "Setiap minggu beli ais plastik untuk tetamu…" | Kiri: angkut ais, cair, peti penuh / kanan: tekan butang, ais keluar → AIS 0.7 kg | Orus |
| A02 | Produk | D | 40 | "Macam mana ais dibuat dalam mesin sebesar ni?" | Air RO → sistem ais keluli tahan karat → tangki ais 0.7 kg → berhenti sendiri bila penuh | Kore |
| A03 | Edukasi | F | 38 | "Ais pun dari air — tapi air apa?" | MITOS: "ais semua sama" → FAKTA: ais bersih bermula dari air ditapis RO | Kore |
| A04 | Produk | G | 38 | "RM120 sebulan — apa yang anda dapat sebenarnya?" | Air 3 suhu + ais + servis percuma 7 tahun, count-up nilai → Ice Lock & Hot Water Lock | Puck |
| A05 | Cerita | I | 44 | "Sehari di pejabat kecil 10 orang" | 9 pagi kopi panas · 12 tengahari air sejuk · 3 petang ais untuk teh o ais · malam sensor cahaya jimat tenaga | Aoede |
| A06 | Edukasi | J | 35 | "Lampu padam, mesin berhenti buat ais — kenapa?" | Pilihan A/B/C → sensor cahaya kesan malam, kurangkan tenaga → "bijak kan?" | Orus |

### Cinnamon (5)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| C01 | Cerita | I | 42 | "Duduk flat tingkat 15, air paip lemah…" | Pagi air menitis perlahan → penapis biasa lambat → Cinnamon ada booster pump → aliran stabil | Orus |
| C02 | Produk | C | 30 | "RM32 sebulan. Air bersih. Itu je." | Kinetic minimalis, RO, 5L, ½/1/2 cawan, CTA | Puck |
| C03 | Edukasi | F | 38 | "Penapis murah mesti kualiti rendah?" | MITOS dipangkah → FAKTA: Cinnamon guna penapisan RO juga, cuma air suhu bilik sahaja | Kore |
| C04 | Cerita | B | 40 | "Mak tanya: mesin kecik ni boleh tahan ke?" | Chat anak-mak → servis berkala, penapis ditukar technician → mak setuju | Aoede |
| C05 | Produk | H | 36 | "3 sebab Cinnamon sesuai untuk dapur kecil" | 1. saiz kompak 2. booster pump 3. tekan ½/1/2 cawan terus | Aoede |

### Dazzie (5)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| D01 | Cerita | A | 42 | "Pukul 3 pagi. Baby menangis. Susu kena bancuh sekarang." | Masak air, tunggu sejuk, uji di tangan → Dazzie: tekan 45°C terus → ibu tidur semula | Aoede |
| D02 | Produk | C | 30 | "45° susu. 70° teh. 85° kopi. 98° maggi." | Kinetic 4 suhu pratetap + kawalan isipadu → CTA | Puck |
| D03 | Edukasi | D | 40 | "Apa itu Nanotrap?" | Virus/bakteria dalam air paip → membran Nanotrap perangkap → 99.999% Murine Norovirus + UV | Kore |
| D04 | Produk | E | 38 | "Cerek + termos vs Dazzie" | Kiri: masak, tunggu, tuang, tunggu sejuk (jam berjalan) / kanan: 1 tekan → masa dijimat | Orus |
| D05 | Cerita | B | 40 | "Isteri: nak buat susu anak kena tunggu air sejuk dulu…" | Chat suami-isteri → suami tanya agent → Dazzie 45°C → "order hari ni" | Aoede |

### Neon (5)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| E01 | Cerita | A | 38 | "Siapa kata bajet kecil tak boleh cantik?" *(ref R04)* | Dapur pastel, penapis lama kelabu → Neon 5 warna → 3 suhu, < RM2 sehari → RM54 → RM27 | Aoede |
| E02 | Produk | J | 35 | "Warna dapur anda yang mana?" | Pilih: Peach Pink / Mint Green / Ciel Blue / Pebble Gray / Porcelain White → "komen warna pilihan" | Puck |
| E03 | Edukasi | H | 40 | "4 logam berat yang boleh ada dalam paip lama" | Merkuri · plumbum · besi · aluminium → Nanotrap Neon tapis → promo | Kore |
| E04 | Produk | H | 40 | "3 sebab ramai pasang Coway Neon" *(ref R02)* | 1. kompak + 5 warna 2. pakej servis / self-service 3. harga RM54 → RM27 | Aoede |
| E05 | Produk | E | 40 | "Servis sendiri atau technician datang?" *(ref R03)* | Kiri: pakej beserta servis / kanan: self-service → 4 langkah tukar filter → filter percuma tiap 8 bulan → RM54 | Orus |

### Coway umum (4)
| ID | Kat | Gaya | Saat | Tajuk / Hook | Jalan cerita ringkas | Suara |
|---|---|---|---|---|---|---|
| G01 | Edukasi | F | 38 | "Air paip dah dirawat, tak perlu tapis lagi?" | MITOS → FAKTA: air dirawat di loji, tapi melalui paip & tangki rumah → penapis di hujung | Kore |
| G02 | Edukasi | G | 40 | "Berapa keluarga anda habis beli air botol setahun?" | Kalkulator: 4 orang × 2L/hari → botol & RM setahun → banding sewa Coway (andaian ditulis jelas di skrin) | Puck |
| G03 | Cerita | I | 44 | "Ikut technician Coway sehari" | Ketuk pintu → tukar penapis → cuci tangki → uji air → rumah seterusnya; "servis setiap 2/4 bulan" | Orus |
| G04 | Produk | J | 40 | "10 saat: model Coway mana untuk anda?" | Soalan pokok keputusan: ada bayi? → Dazzie · nak ais? → AIS · keluarga besar? → V3 · bajet? → CN/NP | Aoede |

**Semakan agihan:** Cerita 13 · Edukasi 12 · Produk 15 · setiap gaya A–J = 4 video · semua 30–44 saat.

## 5. Audio — Gemini TTS

Sudah diuji dari persekitaran ini (29 Sep 2026): model **`gemini-3.8-flash-tts`** berfungsi untuk Bahasa Melayu.
Model lain tersedia: `gemini-2.5-pro-preview-tts`, `gemini-3.1-flash-tts-preview`, `gemini-3.8-flash-lite-tts` (lebih murah untuk draf).

| Suara | Watak | Guna untuk | Sampel |
|---|---|---|---|
| **Orus** | Lelaki, bercerita santai (paling dekat dengan video Villaem 3) | Cerita A/E/I | `voiceover/sampel_suara/Orus.wav` |
| **Puck** | Lelaki, bertenaga & laju | Kinetic C, Infografik G, Kuiz | `…/Puck.wav` |
| **Kore** | Perempuan, yakin & jelas | Edukasi D/F/H | `…/Kore.wav` |
| **Aoede** | Perempuan, mesra "kakak bercerita" | Chat B, ibu/keluarga | `…/Aoede.wav` |

Cara jana (ikut aliran video panjang sedia ada — **suara dulu, animasi ikut suara**):
1. Satu panggilan TTS untuk **seluruh skrip** (bukan baris demi baris) → intonasi lebih semula jadi.
   Arahan gaya diletak di depan teks, cth: *"Bacakan dalam Bahasa Melayu Malaysia, gaya lelaki bercerita santai macam content creator:"*
2. Nombor ditulis dalam perkataan ("tujuh puluh empat ringgit") supaya sebutan betul.
3. `voiceover/align.py` → cari masa setiap baris → animasi diletak ikut masa sebenar (atau `retime` seperti versi panjang).
4. Nota teknikal: model 3.8 memulangkan **fail WAV lengkap** (24 kHz mono), bukan PCM mentah — jangan tambah header lagi.
5. Had kadar: kena **429 Too Many Requests** selepas 3 panggilan berturut-turut semasa ujian → skrip batch mesti ada
   jeda + cuba semula (backoff 20s, 40s, 60s…). 40 video ≈ 40–60 panggilan, masih kecil.

Muzik & SFX: kekal dijana dengan numpy (`audio.py`) — ubah tempo/kunci ikut gaya (cth. C & G 120 BPM, A & I 96 BPM,
F/D 104 BPM) supaya 40 video tak berbunyi sama. VO di-*duck* muzik ~-9 dB seperti `mix.py`.

## 6. Simpan di Google Drive

| Pilihan | Status | Catatan |
|---|---|---|
| **A. rclone terus dari container (dicadang)** | Boleh — `www.googleapis.com` boleh dicapai dari sini (diuji) | Perlu token OAuth Google Drive disimpan sebagai *environment secret* (`RCLONE_CONFIG_GDRIVE_TOKEN`). Selepas render: `rclone copy out/final/ gdrive:Coway-Video/Batch-1/`. Automatik untuk semua 40 video. |
| B. Connector Google Drive (dalam Claude) | Boleh untuk fail kecil sahaja | Sesuai untuk cipta folder, Google Sheet tracker, skrip & SRT. **Tidak praktikal untuk MP4** (5–15 MB setiap satu perlu dihantar sebagai base64). |
| C. GitHub → muat turun → Drive | Cara sekarang | Repo akan membesar ±400 MB untuk 40 video; kalau pilih cara ini guna Git LFS atau GitHub Releases. |

Struktur folder Drive dicadang:
```
Coway-Video/
  00-Tracker (Google Sheet dari plan/senarai_video.csv)
  Batch-1/  V01_raya-mertua.mp4  V01_raya-mertua.srt  V01_skrip.txt …
  Batch-2/ …
  _Thumbnail/   (still frame 1080×1920 setiap video)
```

## 7. Aliran kerja & jadual

**Struktur repo selepas ini:**
```
engine/        timeline.js (seek, tween, easing) — diekstrak dari src/index.html
templates/     A_cerita.html … J_kuiz.html  (10 template)
videos/V01/    config.json (teks, harga, warna, suara) · skrip.md · vo.wav · index.html
out/final/     V01_raya-mertua.mp4 …
```

**Satu video, hujung ke hujung:** skrip (Claude) → TTS (Gemini) → align → isi template → `render.py` → `audio.py` → `mix.py`
→ QC → upload Drive.

**Senarai semak QC setiap video:** 30–45s · hook ≤2.5s · teks dalam *safe zone* (elak 250px bawah & 150px atas — UI Reels/TikTok) ·
harga betul ikut `harga.json` · sebutan nama produk betul · tiada teks bertindih · CTA WhatsApp jelas 3s terakhir.

| Batch | Video | Fokus |
|---|---|---|
| **1** | V01, V02, V05, N02, N05, A04, C01, D04, E02, G01 | **Satu video bagi setiap gaya A–J** → 10 template siap & diluluskan |
| 2 | V03, V04, V06, N01, N03, N06, A01, C02, D01, E01 | Guna semula template, fokus produk permintaan tinggi |
| 3 | V07, V08, N04, N07, A02, A03, C03, D03, E03, G02 | Edukasi & perbandingan |
| 4 | A05, A06, C04, C05, D02, D05, E04, E05, G03, G04 | Lengkapkan baki |

Batch 1 paling lama (bina template); batch 2–4 jauh lebih cepat kerana hanya tukar config + skrip.

## 8. Yang saya perlukan daripada anda sebelum mula

1. **Gambar produk** (PNG latar lutsinar, pandangan depan) untuk Neo Plus, Ais, Cinnamon, Dazzie, Neon — sekarang repo hanya ada Villaem 3.
2. **Harga & promo semasa** setiap model (dan tarikh tamat promo) + nombor/pautan WhatsApp untuk CTA.
3. Pilih **suara** daripada 4 sampel (atau campur seperti cadangan §5).
4. Pilih cara **Google Drive** (§6) — jika A, sediakan token rclone sebagai secret persekitaran.
5. Perkara **no. 6** dalam mesej anda kosong — ada syarat lain (cth. platform: Meta/TikTok, kapsyen terbakar, logo agen)?

## 9. Nota pematuhan (Meta/TikTok Ads)

- Guna hanya dakwaan rasmi Coway (angka kapasiti, 99.9% UV, 99.999% Nanotrap dll.) — jangan tambah dakwaan kesihatan sendiri.
- Video cerita & chat ialah **lakonan senario**, bukan testimoni pelanggan sebenar — jangan letak nama/muka orang sebenar
  atau tulis "review sebenar". Letak teks kecil "Senario lakonan" jika perlu.
- UI chat generik — tiada logo WhatsApp/Meta dalam animasi (butang CTA "WhatsApp saya" dibenarkan).
- Kalkulator kos (G02) mesti papar andaian di skrin.

Sumber spesifikasi & harga: laman produk Coway Malaysia (Villaem 3, Neo Plus, Ais, Dazzie, Neon, Cinnamon) melalui carian web 29 Sep 2026.
