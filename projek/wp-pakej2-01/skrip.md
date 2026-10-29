# Skrip: wp-pakej2-01 — 35 draf (Cinnamon, Glaze, Ombak, Dazzie, Core Slim)

Status: **DRAF** (menunggu kelulusan user) · Brief: [brief.md](brief.md) · Harga dari laman rasmi 13 Okt 2026, **sahkan semula sebelum render**

Setiap model: **5 video produk** (satu video, satu kelebihan) + **2 video psikografik** (P = persona/situasi hidup).
Format: motion graphic `mg` (`.claude/skills/coway-video/formats/mg-gaya.md`). Gaya diagihkan supaya setiap model ada 4–5 gaya berbeza.
Lajur VO = teks TTS (nombor dalam perkataan). Lajur Kapsyen = teks skrin. CTA umum (pakej dijual kepada ejen, tiada nama/nombor ejen).
Suara Gemini: P = Kore, Aoede · L = Orus, Puck, Charon.

## Ringkasan

| ID | Model | Jenis | Hook | Kelebihan / persona | Jenis hook | Suara | Gaya mg | ±s |
|---|---|---|---|---|---|---|---|---|
| CN01 | Cinnamon | Produk | "Air RO bersih kat rumah, RM32 sebulan. Serius." | Harga | Angka | Kore | 01-flat-vector | 32 |
| CN02 | Cinnamon | Produk | "Air paip rumah awak keluar perlahan macam ni?" | Booster pump | Seru situasi | Orus | 07-liquid | 34 |
| CN03 | Cinnamon | Produk | "Isi botol air sekolah anak, tak payah berdiri tunggu." | Isipadu 250/500/1000 ml | Seru situasi | Kore | 08-morph | 33 |
| CN04 | Cinnamon | Produk | "Murah macam ni, betul ke RO?" | 6 langkah penapisan | Soalan bantahan | Orus | 19-paperclip | 38 |
| CN05 | Cinnamon | Produk | "Dapur rumah sewa sempit, kaunter dah penuh?" | Slim, 5L, faucet tanggal | Seru situasi | Kore | 03-isometric | 32 |
| CN06 | Cinnamon | **P** | "Gaji pertama, bilik sewa pertama…" | Bujang / rumah sewa pertama | Cerita pertama | Puck | 06-collage | 38 |
| CN07 | Cinnamon | **P** | "Balik kampung, mak masih jerang air dalam periuk." | Anak belikan untuk mak ayah | Cerita pertama | Aoede | 02-line-art | 38 |
| GZ01 | Glaze | Produk | "Air sejuk gelas ketiga, dah jadi suam?" | Cold Water+ | Seru situasi | Orus | 07-liquid | 32 |
| GZ02 | Glaze | Produk | "Kenapa air sejuk Glaze lebih banyak?" | Tangki sejuk & bilik berasingan | Soalan | Kore | 19-paperclip | 32 |
| GZ03 | Glaze | Produk | "Satu gelas, satu botol, satu jag. Tekan sekali je." | Panel digital, 120/250/500 ml | Listicle | Puck | 08-morph | 30 |
| GZ04 | Glaze | Produk | "Risau penapis panas sejuk makan elektrik?" | Sensor gelap + child lock | Soalan bantahan | Aoede | 22-hud | 33 |
| GZ05 | Glaze | Produk | "Dapur moden, penapis air pun kena sepadan." | Matte white, faucet & tray tanggal | Seru situasi | Kore | 02-line-art | 30 |
| GZ06 | Glaze | **P** | "Kerja bawah panas dari pagi…" | Kaki air sejuk / kerja luar | Cerita pertama | Charon | 01-flat-vector | 36 |
| GZ07 | Glaze | **P** | "Rumah awak ke port family berkumpul?" | Hos tetamu / kenduri | Soalan | Aoede | 06-collage | 36 |
| OM01 | Ombak | Produk | "90, 80, 40. Tahu nombor ni untuk apa?" | 3 suhu panas pratetap | Angka / kuiz | Aoede | 01-flat-vector | 33 |
| OM02 | Ombak | Produk | "Pagi-pagi semua nak bancuh, air panas habis." | Tangki panas terbesar 3.4L | Seru situasi | Orus | 07-liquid | 33 |
| OM03 | Ombak | Produk | "Elektrik terputus. Kipas mati, lampu mati." | Air keluar masa blackout | Seru situasi | Kore | 03-isometric | 30 |
| OM04 | Ombak | Produk | "Air minum dah tapis, tapi masak masih guna air paip?" | Faucet masak + penapis mineral (pilihan) | Soalan | Aoede | 19-paperclip | 34 |
| OM05 | Ombak | Produk | "Tengah malam, dapur sunyi, penapis berbunyi." | Silent, mod malam, child lock, preset | Seru situasi | Puck | 12-aurora-glass | 33 |
| OM06 | Ombak | **P** | "Subuh, mak dah bancuh kopi untuk ayah." | Mak yang dapur tak pernah tutup | Cerita | Aoede | 06-collage | 40 |
| OM07 | Ombak | **P** | "Hujung minggu, rumah mak penuh." | Rumah tempat semua balik | Cerita | Charon | 03-isometric | 36 |
| DZ01 | Dazzie | Produk | "18 sentimeter. Itu je ruang yang Dazzie perlukan." | Lebar 180 mm | Angka | Kore | 08-morph | 32 |
| DZ02 | Dazzie | Produk | "Faucet, bahagian paling kerap terdedah." | UV automatik faucet | Fakta | Orus | 12-aurora-glass | 33 |
| DZ03 | Dazzie | Produk | "0.01 mikron. Sekecil itu Nanotrap tangkap." | Nanotrap | Angka | Aoede | 07-liquid | 33 |
| DZ04 | Dazzie | Produk | "Tuang air panas dalam mug, terpercik ke tangan?" | Faucet panjang, panel pintar, kunci | Seru situasi | Puck | 01-flat-vector | 30 |
| DZ05 | Dazzie | Produk | "Penapis hidup 24 jam, membazir tak?" | Sleep mode + HEART / Self-Service | Soalan bantahan | Kore | 03-isometric | 33 |
| DZ06 | Dazzie | **P** | "Studio 500 kaki persegi. Setiap inci ada fungsi." | Penghuni kondo / studio | Cerita | Aoede | 06-collage | 36 |
| DZ07 | Dazzie | **P** | "Mesyuarat pukul 9, kopi kena siap 8:55." | WFH, kaki kopi / teh | Cerita | Orus | 02-line-art | 34 |
| CS01 | Core Slim | Produk | "Penapis berdiri selalunya besar macam peti sejuk kecil." | Langsing 260 mm | Mitos vs fakta | Orus | 02-line-art | 30 |
| CS02 | Core Slim | Produk | "12 liter air sedia, setiap masa." | Tangki 12L | Angka | Kore | 08-morph | 28 |
| CS03 | Core Slim | Produk | "Penapis buang semua, termasuk mineral?" | 6 peringkat + Nanotrap | Soalan bantahan | Aoede | 19-paperclip | 38 |
| CS04 | Core Slim | Produk | "Tapis sahaja tak cukup?" | Dual UV | Soalan | Puck | 12-aurora-glass | 32 |
| CS05 | Core Slim | Produk | "Isi jag besar, tak muat, kena senget?" | Tray panjang, pemegang, mudah cuci | Seru situasi | Kore | 03-isometric | 30 |
| CS06 | Core Slim | **P** | "Bos, staf awak masih beli air botol setiap hari?" | Pemilik pejabat kecil / kedai / klinik | Seru peranan | Charon | 01-flat-vector | 34 |
| CS07 | Core Slim | **P** | "Rice cooker, air fryer, blender, kettle. Penuh." | Kaunter dapur dah penuh | Listicle | Aoede | 06-collage | 34 |

Penafian standard (nota halus setiap video): `*Harga sewa obligasi 7+0. Tertakluk terma & syarat.`

---

# COWAY CINNAMON (P-6320R) · dari RM32/bulan

Warna aksen: coklat kayu manis + krim. Gambar: `cinnamon/table-top-...jpg`, `coway-cinnamon-volume-control-*.png`, `coway-cinnamon-water-purifier-with-booster-pump.jpg`.

### CN01 · Air RO RM32 sebulan
Produk · Kelebihan: harga · Suara: Kore (P, ceria) · Gaya: 01-flat-vector

| # | VO | Kapsyen | Visual (motion graphic) |
|---|---|---|---|
| 01 | Air RO bersih kat rumah, tiga puluh dua ringgit sebulan. Serius. | Air RO bersih · *RM32*/bulan | Angka "32" jatuh dari atas, squash & bounce, titis air flat memercik |
| 02 | Kalau bahagi tiga puluh hari, lebih kurang seringgit sehari. | ≈ *RM1* sehari | Grid kalendar 30 kotak, syiling RM1 pop satu-satu |
| 03 | Lebih kurang harga sebotol air kat kedai. | ≈ sebotol air kedai | Botol air flat di sebelah syiling, neraca seimbang |
| 04 | Dapat Coway Cinnamon, penapis RO enam langkah. | Coway Cinnamon · RO *6 langkah* | Produk rasmi slide masuk, 6 jalur warna menyusun di belakang |
| 05 | Servis percuma lima tahun, technician datang tukar penapis. | Servis percuma *5 tahun* | Ikon technician berjalan masuk, kalendar flip |
| 06 | Air bersih tak semestinya mahal. WhatsApp saya sekarang. | WHATSAPP SAYA SEKARANG | Butang hijau WhatsApp, pulse |

### CN02 · Booster pump untuk air paip lemah
Produk · Kelebihan: booster pump dalaman · Suara: Orus (L, tenang) · Gaya: 07-liquid

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Air paip rumah awak keluar perlahan macam ni? | Air paip *lemah*? | Paip, titisan metaball menitis perlahan |
| 02 | Ramai ingat, tekanan air rendah, tak boleh pasang penapis air. | "Tak boleh pasang penapis?" | Aliran tersekat dalam tiub, tanda soal cair |
| 03 | Coway Cinnamon ada booster pump dalaman. | *Booster pump* dalaman | Pam liquid berdenyut, metaball membesar |
| 04 | Dia tolak air melalui penapis, jadi aliran tetap stabil walaupun tekanan paip lemah. | Aliran tetap *stabil* | Aliran tebal konsisten masuk ke gelas |
| 05 | Sesuai untuk flat tingkat atas, atau kawasan yang air selalu lemah. | Flat tingkat atas ✓ | Siluet flat, tingkat atas menyala biru |
| 06 | Dari tiga puluh dua ringgit sebulan. WhatsApp saya, saya check rumah awak dulu. | Dari *RM32*/bulan · WhatsApp saya | Produk + butang WhatsApp |

### CN03 · Tekan sekali, ikut isipadu
Produk · Kelebihan: kawalan isipadu 250/500/1000 ml · Suara: Kore · Gaya: 08-morph

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Isi botol air sekolah anak, tak payah berdiri tunggu. | Tak payah *tunggu* | Satu titis air (bentuk tunggal yang akan morph) |
| 02 | Coway Cinnamon ada tiga pilihan isipadu. | *3* pilihan isipadu | Titis morph → panel sentuh 3 butang |
| 03 | Dua ratus lima puluh ml, untuk segelas. | *250 ml* · segelas | Morph → gelas, terisi |
| 04 | Lima ratus ml, untuk botol. | *500 ml* · botol | Gelas memanjang → botol |
| 05 | Satu liter untuk jag. Tekan sekali, dia berhenti sendiri. | *1 liter* · berhenti sendiri | Botol mengembang → jag; ikon tick |
| 06 | Panel sentuh bercahaya lembut, malam pun nampak. | Panel bercahaya | Latar gelap, panel bersinar lembut |
| 07 | Dari tiga puluh dua ringgit sebulan. WhatsApp saya. | Dari *RM32*/bulan | Jag morph → produk Cinnamon → butang |

### CN04 · Murah, tapi betul ke RO?
Produk · Kelebihan: 6 langkah penapisan, WQA & Halal · Suara: Orus · Gaya: 19-paperclip (explainer kertas + klip)

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Murah macam ni, betul ke RO? | RM32… *betul ke RO?* | Nota kuning dikepil dengan tanda soal |
| 02 | Betul. Langkah satu dan dua, buang kelodak, klorin, dan bahan organik meruap. | 1–2 · kelodak, klorin, VOC | Kad 1–2 dikepil pada papan, zarah tertapis |
| 03 | Langkah tiga, membran RO. Buang logam berat, bahan kimia, dan mikrob. | 3 · *Membran RO* | Kad 3 besar, ikon logam/kimia/mikrob dipangkah |
| 04 | Langkah empat dan lima, kurangkan bau dan sedapkan rasa air. | 4–5 · bau ↓ rasa ↑ | Kad 4–5, ikon hidung & lidah |
| 05 | Langkah enam, halang mikroorganisma membiak dalam tangki. | 6 · tangki terjaga | Kad 6, perisai atas tangki |
| 06 | Semua penapis diperakui WQA dan Halal. | WQA · Halal | Cop lencana jatuh atas papan |
| 07 | Murah, tapi tak murah kualiti. WhatsApp saya. | WhatsApp saya | Produk + butang |

### CN05 · Dapur sempit? Cinnamon muat
Produk · Kelebihan: reka bentuk slim, tangki 5L, faucet boleh tanggal · Suara: Kore · Gaya: 03-isometric

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Dapur rumah sewa sempit, kaunter dah penuh? | Kaunter *penuh*? | Dapur isometrik kecil, barang bertimbun |
| 02 | Coway Cinnamon reka bentuk slim, muat celah kaunter. | *Slim* · muat celah | Barang beralih, Cinnamon meluncur masuk ruang kecil |
| 03 | Tangki air suhu bilik lima liter, cukup untuk minum seharian. | Tangki *5L* | Keratan isometrik tangki terisi |
| 04 | Faucet boleh tanggal, senang cuci sendiri. | Faucet boleh tanggal | Faucet terangkat, gelembung sabun |
| 05 | Tukar penapis? Technician datang, percuma lima tahun. | Servis percuma *5 tahun* | Technician isometrik masuk dapur |
| 06 | Dari tiga puluh dua ringgit sebulan. WhatsApp saya. | Dari *RM32*/bulan | Kamera zoom out, butang WhatsApp |

### CN06 · [P] Gaji pertama, bilik sewa pertama
Psikografik: bujang / pasangan muda, barang besar pertama (P1) · Suara: Puck (L, muda) · Gaya: 06-collage

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Gaji pertama, bilik sewa pertama. Benda pertama aku beli… bukan TV. | Gaji pertama. Benda pertama aku beli… | Kolaj slip gaji, kunci rumah, tanda soal |
| 02 | Sebab tiap minggu angkut air botol naik tangga, penat. | Angkut air botol *naik tangga* | Potongan kertas: watak tarik pek botol naik tangga |
| 03 | Masak air guna cerek? Bau besi. | Cerek… *bau besi* | Cerek kertas, garis bau |
| 04 | Kawan aku cakap, Coway ada model tiga puluh dua ringgit sebulan. | Coway *RM32*/bulan? | Gelembung chat kertas |
| 05 | Cinnamon. Air RO. Tak ada panas sejuk, tapi aku minum air bilik je pun. | Cinnamon · air RO · suhu bilik | Gambar rasmi Cinnamon ditampal dengan pita |
| 06 | Sebulan, kurang dari harga dua kali makan tengah hari. | < 2× makan tengah hari | Dua pinggan nasi kertas vs tag RM32 |
| 07 | Hidup dewasa bermula dengan air bersih. WhatsApp saya. | WhatsApp saya | Butang hijau, kolaj bertaburan |

### CN07 · [P] Untuk mak ayah yang tak nak benda canggih
Psikografik: anak dewasa belikan untuk ibu bapa (H2) · Suara: Aoede (P, lembut) · Gaya: 02-line-art

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Balik kampung, tengok mak masih jerang air dalam periuk. | Mak masih *jerang air* | Satu garisan melukis dapur kampung, periuk berwap |
| 02 | Mak cakap, mesin canggih-canggih, mak tak reti. | "Mak tak reti." | Garisan melukis wajah mak tersenyum segan |
| 03 | Jadi saya pilih yang paling ringkas. Coway Cinnamon. | Paling *ringkas* | Garisan sama bertukar jadi siluet Cinnamon, gambar rasmi fade in |
| 04 | Satu sentuhan, keluar air. Nak segelas ke satu jag, tekan je. | Satu sentuhan | Jari line-art sentuh panel |
| 05 | Penapis, technician datang tukar. Mak tak payah fikir. | Mak tak payah fikir | Garisan melukis technician di pintu |
| 06 | Tiga puluh dua ringgit sebulan. Hadiah yang mak guna hari-hari. | *RM32*/bulan · guna hari-hari | Hati line-art di atas produk |
| 07 | Nak hadiahkan untuk mak ayah? WhatsApp saya. | WhatsApp saya | Butang |

---

# COWAY GLAZE (CHP-6310L) · dari RM75/bulan

Warna aksen: putih matte + biru ais. Gambar: `glaze/coway-glaze-water-purifier-cool-water-plus-function.jpg`, `coway-glaze-digital-touch-panel.jpg`, `coway-glaze-volume-control-*.png`, `coway-glaze-water-purifier-in-kitchen.jpg`.

### GZ01 · Air sejuk tak jadi suam
Produk · Kelebihan: Cold Water+ · Suara: Orus · Gaya: 07-liquid

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Pernah tak, tuang air sejuk gelas ketiga, dah jadi suam? | Gelas ke-3… *suam*? | Tiga gelas liquid, warna biru pudar ke oren |
| 02 | Sebab air sejuk dalam tangki dah habis, kena tunggu sejuk balik. | Tangki sejuk *habis* | Metaball biru mengecut dalam tangki |
| 03 | Coway Glaze ada fungsi Cold Water Plus. | *Cold Water+* | Gambar rasmi Glaze, kristal sejuk merebak |
| 04 | Air sejuk keluar berterusan. Glaze perintis fungsi ni dalam pasaran. | Air sejuk *berterusan* | Aliran biru tak putus, gelas demi gelas terisi |
| 05 | Buat jag sirap, teh o ais, air sejuk tak putus. | Sirap · teh o ais · tak putus | Liquid berubah warna merah sirap → coklat teh |
| 06 | Dari tujuh puluh lima ringgit sebulan. WhatsApp saya. | Dari *RM75*/bulan | Butang WhatsApp |

### GZ02 · Kenapa air sejuk Glaze lebih banyak?
Produk · Kelebihan: tangki sejuk & bilik berasingan · Suara: Kore · Gaya: 19-paperclip

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Kenapa air sejuk Coway Glaze lebih banyak dari penapis biasa? | Kenapa air sejuk *lebih banyak*? | Nota dikepil, tanda soal |
| 02 | Sebab dalam badan dia, tangki sejuk dan tangki suhu bilik diasingkan. | Tangki sejuk ≠ tangki bilik | Lakaran keratan, dua tangki diasingkan dengan klip |
| 03 | Dua setengah liter sejuk, dua setengah liter bilik, satu liter panas. | 2.5L · 2.5L · 1.0L | Tiga bar kertas naik |
| 04 | Air sejuk tak bercampur, jadi bekalan sejuk lebih banyak. | Bekalan sejuk *lebih banyak* | Anak panah kertas, ikon salji |
| 05 | Cuaca Malaysia panas. Ini yang awak perlukan. WhatsApp saya. | Dari *RM75*/bulan · WhatsApp saya | Matahari kertas, produk, butang |

### GZ03 · Gelas, botol, jag, tekan sekali
Produk · Kelebihan: panel digital, isipadu 120/250/500 ml, tekan lama = aliran berterusan · Suara: Puck · Gaya: 08-morph

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Satu gelas, satu botol, satu jag. Tekan sekali je. | Tekan *sekali* | Satu bulatan biru (bentuk tunggal) |
| 02 | Panel sentuh digital Coway Glaze ada tiga isipadu. | Panel sentuh digital | Bulatan morph → panel |
| 03 | Seratus dua puluh ml, dua ratus lima puluh, lima ratus. | *120 · 250 · 500 ml* | Panel → cawan kecil → gelas → botol |
| 04 | Nak isi lebih? Tekan lama, air mengalir berterusan. | Tekan lama = *berterusan* | Botol → jag besar, aliran panjang |
| 05 | Pilih suhu, pilih isipadu, siap. | Suhu ✓ Isipadu ✓ | Ikon panas/sejuk/bilik rasmi |
| 06 | Dari tujuh puluh lima ringgit sebulan. WhatsApp saya. | Dari *RM75*/bulan | Morph → produk → butang |

### GZ04 · Jimat dalam gelap, selamat untuk anak
Produk · Kelebihan: kurang operasi motor & heater dalam gelap, child lock · Suara: Aoede · Gaya: 22-hud (imbasan sensor)

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Risau penapis air panas sejuk makan elektrik? | Makan *elektrik*? | HUD: meter tenaga berkelip merah |
| 02 | Coway Glaze ada sensor cahaya. | Sensor cahaya | Retikel HUD mengunci pada produk |
| 03 | Bila dapur gelap, waktu malam, dia kurangkan operasi motor dan pemanas secara automatik. | Gelap → motor & pemanas *↓* | Langit bertukar malam, graf tenaga turun |
| 04 | Siang guna, malam rehat. | Siang guna · malam rehat | Ikon matahari/bulan bertukar |
| 05 | Butang air panas pula ada kunci, anak kecil tak terbuka sendiri. | Kunci air panas | Ikon mangga, tangan kecil ditolak lembut |
| 06 | Dari tujuh puluh lima ringgit sebulan. WhatsApp saya. | Dari *RM75*/bulan | Butang |

### GZ05 · Cantik di luar, RO di dalam
Produk · Kelebihan: matte white minimalis, penutup faucet lutsinar & tray boleh tanggal · Suara: Kore · Gaya: 02-line-art

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Dapur moden, perabot putih. Penapis air pun kena sepadan. | Penapis pun kena *sepadan* | Garisan melukis dapur minimalis |
| 02 | Coway Glaze, kemasan matte white, reka bentuk minimalis. | *Matte white* | Garisan melukis siluet Glaze, gambar rasmi fade in |
| 03 | Penutup faucet lutsinar boleh tanggal dan cuci. | Penutup faucet boleh cuci | Close-up faucet, garisan melukis penutup terangkat |
| 04 | Tray bawah pun boleh tanggal, muat jag dan botol tinggi. | Tray tanggal · muat jag | Tray meluncur keluar, jag tinggi masuk |
| 05 | Cantik di luar, RO di dalam. WhatsApp saya. | Cantik di luar. *RO* di dalam. | Butang |

### GZ06 · [P] Kerja bawah panas, balik nak air sejuk
Psikografik: kaki air sejuk, kerja luar / cuaca panas (P4) · Suara: Charon (L, garau) · Gaya: 01-flat-vector

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Kerja bawah panas dari pagi. Balik rumah, satu je aku cari. | Satu je aku cari… | Matahari flat besar, watak berpeluh |
| 02 | Air sejuk. Bukan satu gelas. Tiga gelas. | *3 gelas* | Tiga gelas pop berturut |
| 03 | Dulu, gelas kedua dah tak sejuk. Peti ais pun penuh botol. | Peti ais *penuh botol* | Peti ais flat terbuka, botol jatuh |
| 04 | Sekarang rumah pasang Coway Glaze, dengan Cold Water Plus. | Coway Glaze · *Cold Water+* | Produk rasmi, kristal ais |
| 05 | Air sejuk keluar berterusan, tak payah sumbat botol dalam peti ais. | Sejuk *berterusan* | Aliran biru panjang, peti ais lega |
| 06 | Penat kerja, sekurang-kurangnya air sejuk tak kecewakan. | Air sejuk *tak kecewakan* | Watak minum, senyum |
| 07 | Dari tujuh puluh lima ringgit sebulan. WhatsApp saya. | Dari *RM75*/bulan | Butang |

### GZ07 · [P] Rumah port family berkumpul
Psikografik: hos tetamu, raya / kenduri / hari jadi · Suara: Aoede · Gaya: 06-collage

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Rumah awak ke yang selalu jadi port family berkumpul? | Rumah awak *port family*? | Kolaj rumah, banyak kasut di pintu |
| 02 | Raya, kenduri, hari jadi. Mesti ada jag air sirap. | Raya · kenduri · hari jadi | Ketupat, kek, jag sirap kertas |
| 03 | Masalahnya, ais habis, air sejuk habis, tetamu masih datang. | Ais *habis*. Tetamu *datang*. | Jag kosong, kereta kertas masuk |
| 04 | Coway Glaze, air sejuk keluar berterusan dengan Cold Water Plus. | *Cold Water+* | Gambar rasmi ditampal pita |
| 05 | Tekan lama, terus penuh jag. Tray pun boleh tanggal untuk jag tinggi. | Tekan lama · penuh jag | Jag terisi, tray dikeluarkan |
| 06 | Tuan rumah relaks, tetamu puas. | Tuan rumah *relaks* | Watak duduk, tetamu senyum |
| 07 | Dari tujuh puluh lima ringgit sebulan. WhatsApp saya. | Dari *RM75*/bulan | Butang |

---

# COWAY OMBAK (CHP-7310R) · dari RM90/bulan

Warna aksen: biru laut + oren hangat. Gambar: `ombak/coway-ombak-variety-water-temperature.jpg`, `suitable-temperature-for-milk-preparation-coway-ombak.jpg`, `largest-hot-water-tank-coway-ombak-water-purifier.jpg`, `additional-water-backup-dispenser-coway-ombak.jpg`, `multipurpose-faucet-for-cooking-coway-ombak-water-purifier.jpg`.

### OM01 · 90, 80, 40
Produk · Kelebihan: suhu panas pratetap · Suara: Aoede · Gaya: 01-flat-vector

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Sembilan puluh, lapan puluh, empat puluh. Tahu tak nombor ni untuk apa? | *90° · 80° · 40°* untuk apa? | Tiga angka besar pop, tanda soal |
| 02 | Sembilan puluh darjah, untuk telur. | *90°C* · telur | Angka 90 berubah jadi telur flat dalam mangkuk |
| 03 | Lapan puluh darjah, kopi lebih wangi. | *80°C* · kopi | Cawan kopi, garis aroma |
| 04 | Empat puluh darjah, bancuh susu anak. Ikut nasihat doktor ya. | *40°C* · susu anak | Botol susu flat |
| 05 | Semua dari satu penapis. Coway Ombak. | Coway Ombak | Tiga ikon terbang masuk ke produk rasmi |
| 06 | Dari sembilan puluh ringgit sebulan. WhatsApp saya. | Dari *RM90*/bulan | Butang |

Nota: 40°C susu → penafian "ikut nasihat doktor" pada skrin.

### OM02 · Air panas tak cukup waktu pagi
Produk · Kelebihan: tangki panas 3.4L, terbesar dalam rangkaian kaunter Coway · Suara: Orus · Gaya: 07-liquid

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Pagi-pagi, semua orang nak bancuh. Air panas habis. | Air panas *habis* | Liquid oren dikongsi ke 4 cawan, kering |
| 02 | Kena tunggu panas balik, dah lambat nak keluar kerja. | Tunggu… *lambat* | Jam liquid menitis |
| 03 | Coway Ombak ada tangki air panas tiga perpuluhan empat liter. | Tangki panas *3.4L* | Metaball oren besar memenuhi tangki |
| 04 | Paling besar dalam rangkaian penapis atas kaunter Coway. | *Terbesar* dalam rangkaian kaunter Coway | Bar perbandingan liquid, Ombak tertinggi (tanpa nama model lain) |
| 05 | Tambah tujuh perpuluhan lapan liter suhu bilik, dan dua perpuluhan tiga liter sejuk. | 7.8L bilik · 2.3L sejuk | Tiga tangki liquid berwarna |
| 06 | Dari sembilan puluh ringgit sebulan. WhatsApp saya. | Dari *RM90*/bulan | Butang |

### OM03 · Elektrik terputus, air tetap ada
Produk · Kelebihan: boleh keluar air masa blackout · Suara: Kore · Gaya: 03-isometric (rumah malam)

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Elektrik terputus. Kipas mati, lampu mati. | *Blackout* | Rumah isometrik, lampu padam satu-satu |
| 02 | Tapi anak dahaga, dan penapis air pun ikut mati. | Penapis pun *mati*? | Watak kecil pegang gelas kosong |
| 03 | Coway Ombak masih boleh keluarkan air walaupun blackout. | Air tetap keluar | Satu cahaya biru: Ombak, gelas terisi |
| 04 | Air bersih tetap ada, masa paling perlu. | Masa *paling perlu* | Kamera dekat, keluarga lega |
| 05 | Sesuai untuk kawasan yang selalu gangguan bekalan elektrik. WhatsApp saya. | Dari *RM90*/bulan · WhatsApp saya | Lampu kembali menyala, butang |

**[SAHKAN]** suhu air yang keluar masa blackout (laman hanya kata "Dispense water even during a blackout"). Jangan janji air panas.

### OM04 · Masak pun guna air bersih
Produk · Kelebihan: faucet tambahan untuk masak + penapis mineral (kedua-dua pilihan, caj tambahan) · Suara: Aoede · Gaya: 19-paperclip

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Air minum dah tapis, tapi masak nasi, masak sup, masih guna air paip? | Masak masih guna *air paip*? | Nota dikepil: periuk + paip |
| 02 | Coway Ombak boleh tambah faucet kedua, khas untuk masak. | Faucet kedua · *untuk masak* | Lakaran faucet ke singki, dikepil |
| 03 | Terus ke singki, isi periuk tak payah angkat. | Terus ke singki | Anak panah kertas ke periuk |
| 04 | Nak air ada mineral? Ada pilihan penapis mineral. | Penapis *mineral* | Kad mineral ditambah |
| 05 | Dua-dua ni pilihan tambahan, ada caj berasingan. | *Pilihan, caj tambahan | Nota halus jelas di skrin |
| 06 | Dari sembilan puluh ringgit sebulan. WhatsApp saya. | Dari *RM90*/bulan | Butang |

### OM05 · Senyap waktu malam
Produk · Kelebihan: silent mode, mod malam, child lock, preset · Suara: Puck · Gaya: 12-aurora-glass

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Tengah malam, dapur sunyi. Tiba-tiba penapis air berbunyi. | *Bzzz…* tengah malam | Aurora gelap, gelombang bunyi berkelip |
| 02 | Coway Ombak ada silent mode. | *Silent mode* | Kad kaca, gelombang mendatar |
| 03 | Waktu malam, motor dan pemanas berkurang secara automatik. | Malam → *jimat* | Ikon bulan, meter turun |
| 04 | Air panas ada kunci keselamatan kanak-kanak. | Kunci air panas | Mangga kaca bersinar |
| 05 | Suhu dan isipadu kegemaran boleh set awal. Tekan sekali je. | Preset · tekan sekali | Panel kaca, satu butang menyala |
| 06 | Dari sembilan puluh ringgit sebulan. WhatsApp saya. | Dari *RM90*/bulan | Butang |

### OM06 · [P] Dapur mak tak pernah tutup
Psikografik: ibu yang memasak untuk keluarga sepanjang hari · Suara: Aoede · Gaya: 06-collage

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Subuh, mak dah bancuh kopi untuk ayah. | 5:45 · kopi ayah | Kolaj jam + cawan kopi |
| 02 | Pukul tujuh, telur untuk anak sekolah. | 7:00 · telur | Telur, beg sekolah kertas |
| 03 | Tengah hari masak sup. Malam, bancuh susu adik. | 12:30 · sup · 21:00 · susu | Periuk, botol susu |
| 04 | Dapur mak tak pernah tutup. Jadi penapis air mak pun kena faham dapur. | Dapur mak *tak pernah tutup* | Semua potongan berkumpul dalam bingkai dapur |
| 05 | Coway Ombak. Suhu untuk kopi, telur, susu. Faucet tambahan untuk masak. | 80° · 90° · 40° · faucet masak* | Gambar rasmi Ombak, label ditampal |
| 06 | Buatan Korea, tapi jiwa Malaysia. | Korea asalnya. *Malaysia jiwanya.* | Bendera warna pastel, dapur Malaysia |
| 07 | Untuk mak. WhatsApp saya. | Dari *RM90*/bulan · WhatsApp saya | Butang |

Penafian: *faucet tambahan pilihan, caj tambahan · susu: ikut nasihat doktor.

### OM07 · [P] Rumah mak tempat semua balik
Psikografik: rumah keluarga besar, anak cucu balik hujung minggu · Suara: Charon · Gaya: 03-isometric

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Hujung minggu, rumah mak penuh. Anak, menantu, cucu. | Rumah mak *penuh* | Rumah isometrik, kereta berderet di luar |
| 02 | Cerek berbunyi tak berhenti, air panas tak cukup. | Air panas *tak cukup* | Cerek berwap, barisan cawan |
| 03 | Penapis kecil pun tak menang tangan. | Tak menang tangan | Penapis kecil dikerumun |
| 04 | Coway Ombak simpan tujuh perpuluhan lapan liter air bilik, dan tiga perpuluhan empat liter air panas. | 7.8L bilik · *3.4L panas* | Keratan isometrik tangki besar |
| 05 | Semua bancuh air sendiri, mak duduk berbual je. | Mak *duduk berbual* | Mak di sofa, cucu bancuh air |
| 06 | Rumah ramai orang, penapis kena kuat. WhatsApp saya. | Dari *RM90*/bulan · WhatsApp saya | Butang |

---

# COWAY DAZZIE (CHP-1201N) · dari RM74 (Self-Service) / RM79 (HEART)

Warna aksen: Porcelain White / Pebble Gray + cerulean. Gambar: `dazzie/coway-dazzie-water-purifier-minimum-size-maximum-style2.jpg`, `coway-dazzie-with-automatically-uv-sterilises-features.png`, `coway-nanotrap-filter-8.png`, `coway-dazzie-with-smart-panel.jpg`, `coway-dazzie-water-purifier-with-additional-faucet.jpg`.
Nota: skrip lama D-01–D-10 (`skrip/dazzie.md`) belum jadi video; hook di bawah sengaja berbeza.

### DZ01 · 18 sentimeter
Produk · Kelebihan: lebar 180 mm, direct flow · Suara: Kore · Gaya: 08-morph

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Lapan belas sentimeter. Itu je ruang yang Coway Dazzie perlukan. | *18 cm* | Garisan ukur memanjang lalu berhenti |
| 02 | Lebih kecil dari sebatang pembaris sekolah. | < pembaris 30 cm | Garisan morph → pembaris, Dazzie di sebelah |
| 03 | Kaunter kondo, pantri pejabat, tepi singki, muat. | Kondo · pantri · tepi singki | Pembaris morph → 3 ruang kecil berturut |
| 04 | Kecil, tapi air tak terhad, sebab dia direct flow, tiada tangki simpanan. | *Direct flow* · tiada tangki | Aliran terus dari paip ke cawan |
| 05 | Dua warna, Porcelain White dan Pebble Gray. | Porcelain White · Pebble Gray | Produk bertukar warna |
| 06 | Dari tujuh puluh empat ringgit sebulan. WhatsApp saya. | Dari *RM74*/bulan (Self-Service) | Butang |

### DZ02 · Faucet yang jaga diri sendiri
Produk · Kelebihan: UV automatik faucet · Suara: Orus · Gaya: 12-aurora-glass

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Faucet. Bahagian penapis air yang paling kerap terdedah. | Faucet = paling *terdedah* | Close-up faucet, zarah halus terapung |
| 02 | Coway Dazzie jaga sendiri. | Dazzie jaga sendiri | Gambar rasmi, cahaya kaca |
| 03 | Bila tak guna enam jam, dia sterilkan faucet dengan UV selama dua puluh lima minit. | *6 jam* rehat → *25 minit* UV | Jam kaca 6:00, cincin UV ungu berputar |
| 04 | Hapuskan sehingga sembilan puluh sembilan perpuluhan sembilan peratus bakteria seperti E. coli. | Sehingga *99.9%* bakteria** | Zarah pecah jadi cahaya |
| 05 | Automatik. Awak tak perlu ingat. WhatsApp saya. | Automatik · WhatsApp saya | Butang |

Penafian: **Berdasarkan ujian TÜV SÜD Korea dalam persekitaran terkawal.

### DZ03 · Nanotrap, sekecil 0.01 mikron
Produk · Kelebihan: penapis Nanotrap · Suara: Aoede · Gaya: 07-liquid

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Kosong perpuluhan kosong satu mikron. Sekecil itu penapis Nanotrap boleh tangkap. | *0.01 µ* | Titis air besar, zoom masuk ke dalam |
| 02 | Penapis ni ada salutan gentian nano yang bercas positif. | Gentian nano *bercas +* | Gentian liquid berkilau, tanda + |
| 03 | Virus dan bakteria bercas negatif, jadi ia tertarik dan melekat pada penapis. | Virus & bakteria *melekat* | Zarah merah (−) ditarik, melekat |
| 04 | Lepas tu, penapis karbon kurangkan bau dan perbaiki rasa. | Bau ↓ rasa ↑ | Liquid jernih mengalir keluar |
| 05 | Diperakui WQA dan Halal. | WQA · Halal | Lencana |
| 06 | Coway Dazzie, dari tujuh puluh empat ringgit sebulan. WhatsApp saya. | Dari *RM74*/bulan | Butang |

### DZ04 · Tak terpercik, tak tersalah tekan
Produk · Kelebihan: faucet panjang percuma, panel suhu & isipadu, kunci air panas · Suara: Puck · Gaya: 01-flat-vector

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Tuang air panas dalam mug, terpercik ke tangan? | *Terpercik*? | Mug flat, percikan, ikon "aduh" |
| 02 | Coway Dazzie datang dengan faucet panjang, percuma. Air jatuh terus dalam cawan. | Faucet panjang *percuma* | Faucet memanjang, aliran tepat |
| 03 | Panel pintar, pilih suhu dan isipadu ikut cawan awak. | Pilih suhu · pilih isipadu | Panel flat, dua dail |
| 04 | Butang air panas berkunci. Tekan tiga saat untuk buka. | Kunci · tekan *3 saat* | Kiraan 3-2-1, mangga terbuka |
| 05 | Kecil, tapi fikir semua benda. WhatsApp saya. | Dari *RM74*/bulan · WhatsApp saya | Butang |

**[SAHKAN]** suhu pratetap Dazzie sebelum sebut angka (lihat brief §5).

### DZ05 · Rehat bila tak guna
Produk · Kelebihan: sleep mode 1 jam + pilihan servis · Suara: Kore · Gaya: 03-isometric

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Penapis air hidup dua puluh empat jam. Membazir tak? | Hidup *24 jam*? | Dapur isometrik, jam berputar |
| 02 | Coway Dazzie masuk sleep mode kalau tak guna satu jam. | *Sleep mode* selepas 1 jam | Dazzie redup, "Zzz" |
| 03 | Jimat tenaga, tanpa awak tekan apa-apa. | Jimat · automatik | Meter tenaga turun |
| 04 | Pilih servis. HEART, technician datang. Atau Self-Service, penapis dihantar ke rumah. | HEART · Self-Service | Dua laluan isometrik: technician / kotak pos |
| 05 | Tujuh puluh sembilan ringgit HEART, tujuh puluh empat Self-Service, tujuh tahun. | *RM79* HEART · *RM74* Self-Service · 7 tahun | Dua tag harga |
| 06 | WhatsApp saya, saya bantu pilih. | WhatsApp saya | Butang |

### DZ06 · [P] Studio 500 kaki persegi
Psikografik: penghuni kondo / studio, ruang terhad (P5) · Suara: Aoede · Gaya: 06-collage

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Studio lima ratus kaki persegi. Setiap inci ada fungsi. | *500 kps* · setiap inci ada fungsi | Pelan lantai kertas dipotong |
| 02 | Kaunter dapur aku muat satu kettle, satu rice cooker. Itu je. | Muat *2 barang* je | Kettle & rice cooker kertas berhimpit |
| 03 | Aku nak air bersih, tapi tak nak mesin besar curi ruang. | Tak nak mesin *besar* | Penapis besar kertas dipangkah |
| 04 | Jumpa Coway Dazzie. Lebar lapan belas sentimeter. | Coway Dazzie · *18 cm* | Gambar rasmi ditampal, pembaris kertas |
| 05 | Air panas, air suhu bilik, kettle pun boleh simpan. | Kettle boleh *simpan* | Kettle dimasukkan ke kotak |
| 06 | Rumah kecil, hidup tetap kemas. | Rumah kecil, hidup *kemas* | Kaunter lapang |
| 07 | Dari tujuh puluh empat ringgit sebulan. WhatsApp saya. | Dari *RM74*/bulan | Butang |

### DZ07 · [P] WFH, kopi kena siap 8:55
Psikografik: kerja dari rumah, kaki kopi / teh · Suara: Orus · Gaya: 02-line-art

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | WFH. Mesyuarat pukul sembilan, kopi kena siap pukul lapan lima puluh lima. | Meeting 9:00 · kopi *8:55* | Garisan melukis laptop + jam |
| 02 | Tunggu kettle mendidih, tunggu sejuk sikit. Dah lambat. | Tunggu… tunggu… | Wap line-art, jam melompat |
| 03 | Dapur aku sekarang ada Coway Dazzie. | Coway Dazzie | Garisan bertukar jadi Dazzie, gambar rasmi |
| 04 | Pilih suhu, pilih isipadu, terus ke mug. | Suhu · isipadu · *terus ke mug* | Aliran line-art ke mug |
| 05 | Air ditapis Nanotrap. Kopi siap, aku siap. | Kopi siap. *Aku siap.* | Watak line-art join meeting |
| 06 | Dari tujuh puluh empat ringgit sebulan. WhatsApp saya. | Dari *RM74*/bulan | Butang |

---

# COWAY CORE SLIM (CHP-5731N) · dari RM89/bulan (HEART, servis 7 tahun)

Warna aksen: Porcelain White / Pebble Gray + cerulean. Gambar: `coreslim/Main_KV_mobile.png`, `USP_Slim_1-3.png`, `USP_water_tank_1-3.png`, `UV.png`, `extendable-tray.png`, `handle.png`, `talent.jpg`.
**[SAHKAN]** harga & ketersediaan: `products.md` (13 Okt) kata "tiada di laman", tapi `copy.md` ada RM89 / RM5,000.

### CS01 · Berdiri tapi langsing
Produk · Kelebihan: lebar 260 mm · Suara: Orus · Gaya: 02-line-art

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Penapis air berdiri, selalunya besar macam peti sejuk kecil. | Berdiri = *besar*? | Garisan melukis kotak tebal |
| 02 | Coway Core Slim lain. Berdiri, tapi langsing. | Berdiri, tapi *langsing* | Kotak dipicit jadi siluet Core Slim, gambar rasmi |
| 03 | Lebar dua puluh enam sentimeter je. Muat sudut dapur atau pantri. | Lebar *26 cm* | Garisan ukur, sudut bilik |
| 04 | Tak ambil ruang kaunter langsung. | Kaunter kekal *lapang* | Kaunter kosong line-art |
| 05 | Dua warna, Porcelain White dan Pebble Gray. WhatsApp saya. | Dari *RM89*/bulan · WhatsApp saya | Dua warna, butang |

### CS02 · 12 liter sedia
Produk · Kelebihan: tangki 12L (3.0 panas / 3.5 sejuk / 5.5 bilik) · Suara: Kore · Gaya: 08-morph

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Dua belas liter air sedia, setiap masa. | *12 liter* | Angka 12 morph → bentuk tangki |
| 02 | Tiga liter panas, tiga setengah sejuk, lima setengah suhu bilik. | 3.0L · 3.5L · 5.5L | Tangki pecah jadi 3 ruang warna |
| 03 | Cukup untuk satu pejabat kecil, atau satu keluarga ramai. | Pejabat kecil · keluarga ramai | Ruang morph → ikon pejabat → ikon keluarga |
| 04 | Semua dalam badan yang langsing. | Badan *langsing* | Morph → Core Slim |
| 05 | Dari lapan puluh sembilan ringgit sebulan. WhatsApp saya. | Dari *RM89*/bulan | Butang |

### CS03 · Tapis yang jahat, kekal yang baik
Produk · Kelebihan: 6 peringkat + Nanotrap, kekalkan mineral berguna · Suara: Aoede · Gaya: 19-paperclip

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Penapis air buang semua, termasuk mineral? Untuk Core Slim, tak. | Buang *mineral*? | Nota dikepil, tanda pangkah |
| 02 | Peringkat satu dan dua, buang pasir, karat dan klorin. | 1–2 · pasir, karat, klorin | Kad 1–2 |
| 03 | Peringkat tiga, tapis bahan berbahaya, tapi kekalkan mineral berguna. | 3 · *mineral kekal* | Kad 3, ikon mineral tick |
| 04 | Peringkat empat dan lima, buang bau, kerak, dan habuk halus. | 4–5 · bau, kerak, habuk | Kad 4–5 |
| 05 | Peringkat enam, Nanotrap tangkap virus dan bakteria sekecil kosong perpuluhan kosong satu mikron. | 6 · *Nanotrap 0.01 µ* | Kad 6 besar, zarah melekat |
| 06 | Dari lapan puluh sembilan ringgit sebulan. WhatsApp saya. | Dari *RM89*/bulan | Butang |

### CS04 · Satu lapisan lagi: Dual UV
Produk · Kelebihan: dual UV + servis HEART 7 tahun · Suara: Puck · Gaya: 12-aurora-glass

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Tapis sahaja tak cukup? Core Slim tambah satu lapisan lagi. | Tambah *satu lapisan* | Lapisan kaca bertindih |
| 02 | Dual UV sterilisation. | *Dual UV* | Dua cincin UV ungu |
| 03 | Hapuskan sehingga sembilan puluh sembilan perpuluhan sembilan peratus bakteria berbahaya seperti E. coli. | Sehingga *99.9%* bakteria* | Zarah pecah jadi cahaya |
| 04 | Untuk rumah dan pejabat yang ramai orang guna, kebersihan penting. | Ramai guna = *kebersihan penting* | Ikon ramai tangan |
| 05 | Servis HEART, technician cuci dan tukar penapis, percuma tujuh tahun. | Servis percuma *7 tahun* | Technician kaca |
| 06 | Dari lapan puluh sembilan ringgit sebulan. WhatsApp saya. | Dari *RM89*/bulan | Butang |

Penafian: *Keputusan ujian dalam persekitaran terkawal. **[SAHKAN]** badan penguji untuk Core Slim (laman tak nyatakan).

### CS05 · Jag besar pun muat
Produk · Kelebihan: tray boleh dipanjangkan, pemegang ergonomik, mudah tanggal untuk cuci · Suara: Kore · Gaya: 03-isometric

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Isi jag besar dari penapis biasa? Tak muat, kena senget. | Tak muat, kena *senget* | Jag isometrik condong, air tumpah |
| 02 | Coway Core Slim ada tray yang boleh dipanjangkan. | Tray *boleh panjang* | Tray meluncur keluar |
| 03 | Jag, botol, bekas kecil, tegak dan stabil. | Tegak · stabil | Tiga bekas berturut |
| 04 | Pemegang ergonomik, senang alih bila nak sapu lantai. | Pemegang ergonomik | Unit dialih sedikit, penyapu lalu |
| 05 | Bahagian mudah tanggal, cuci pun senang. WhatsApp saya. | Dari *RM89*/bulan · WhatsApp saya | Butang |

### CS06 · [P] Bos, staf masih beli air botol?
Psikografik: pemilik pejabat kecil / kedai / klinik / salun · Suara: Charon · Gaya: 01-flat-vector

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Bos, staf awak masih beli air botol setiap hari? | Staf beli *air botol* hari-hari? | Meja pejabat flat, botol bertimbun |
| 02 | Atau pantri penuh galon air yang kena tukar setiap minggu? | Galon *setiap minggu* | Galon bergolek, kalendar |
| 03 | Coway Core Slim. Penapis berdiri, dua belas liter, panas, sejuk, bilik. | Core Slim · *12L* · panas/sejuk/bilik | Produk rasmi masuk pantri |
| 04 | Langsing, muat sudut pantri. Dual UV, servis percuma tujuh tahun. | Langsing · Dual UV · servis *7 tahun* | Tiga ikon tick |
| 05 | Staf terjaga, pelanggan pun selesa. | Staf terjaga. Pelanggan *selesa*. | Watak staf & pelanggan minum |
| 06 | Untuk pejabat, kedai, klinik. WhatsApp saya. | Dari *RM89*/bulan · WhatsApp saya | Butang |

### CS07 · [P] Kaunter dapur dah penuh
Psikografik: keluarga yang kaunter dapur penuh perkakas · Suara: Aoede · Gaya: 06-collage

| # | VO | Kapsyen | Visual |
|---|---|---|---|
| 01 | Rice cooker, air fryer, blender, kettle. Kaunter penuh. | Kaunter *penuh* | Perkakas kertas jatuh satu-satu |
| 02 | Nak pasang penapis air, nak letak mana? | Nak letak *mana*? | Tanda soal kertas |
| 03 | Jawapannya, jangan letak atas kaunter. | *Jangan* atas kaunter | Kaunter dipangkah |
| 04 | Coway Core Slim berdiri sendiri di sudut. Lebar dua puluh enam sentimeter. | Berdiri di sudut · *26 cm* | Gambar rasmi ditampal di sudut |
| 05 | Dua belas liter air panas, sejuk dan bilik. Kaunter kekal macam sekarang. | *12L* · kaunter tak terganggu | Kaunter kekal, produk di sebelah |
| 06 | Dari lapan puluh sembilan ringgit sebulan. WhatsApp saya. | Dari *RM89*/bulan | Butang |
