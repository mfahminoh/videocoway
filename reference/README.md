# Video Rujukan — Batch 1 (R01–R05)

Lima video TikTok yang anda beri (29 Sep 2026). Skrip ditranskrip dengan Gemini (`gemini-3.5-flash-lite`) dan disemak dengan kapsyen
di skrin. Frame 1 saat/sekeping ada dalam [`frames/`](frames/). Fail MP4 asal **tidak** dimasukkan ke repo.

| ID | Kreator | Produk | Tempoh | Formula hook | Guna untuk (plan) |
|---|---|---|---|---|---|
| R01 | @farracowayhq (Farah) | Villaem 3 | 45s | Seru sasaran: *"Ha korang family yang ramai, nak tangki yang besar…"* | **V05** (demo panel suhu) |
| R02 | @_syaifulaiman | Neon | 61s | Senarai: *"3 sebab kenapa ramai pasang…"* | **E04** (listicle) |
| R03 | @_syaifulaiman | Neon (pakej self-service) | 48s | *"Satu benda yang best pasal…"* | **E05** (versus: self-service vs servis) |
| R04 | @_syaifulaiman | Neon | 36s | Bantah mitos: *"Siapa cakap harga murah tak boleh dapat penapis air cantik?"* | **E01** (cerita dapur pastel) |
| R05 | @_syaifulaiman | Neon | 44s | Label golongan: *"Ini penapis air pilihan golongan baru berkahwin"* | **N01** (formula sama, produk Neo Plus) |

Skrip asal penuh: [`skrip_rujukan.md`](skrip_rujukan.md) · Skrip baharu kita (ditulis semula, sedia untuk Gemini TTS):
[`skrip_adaptasi.md`](skrip_adaptasi.md)

---

## Apa yang menjadikan video ni berkesan (untuk ditiru dari segi *struktur*)

1. **Hook satu ayat, ≤ 3 saat**, terus sebut siapa sasaran atau janji nombor ("3 sebab", "satu benda best").
2. **Nombor spesifik** di setiap babak: 95 / 80 / 70°C, 120 ml → 1,000 ml, tangki 1L / 1.5L, filter setiap 8 bulan.
3. **Soalan yang dijawab sendiri** untuk patahkan bantahan: *"Tapi filter ni nak beli kat mana?" → "Coway hantar percuma."*
4. **Tangga harga**: "tak sampai RM2 sehari" → "bawah RM60 sebulan" → "diskaun 50% 6 bulan" → **RM27**.
5. **CTA berganda**: isi beg biru + link di bio + "saya bantu uruskan sampai siap pasang" + penghantaran & pemasangan percuma seluruh Malaysia.
6. **Kapsyen**: 2–4 perkataan satu masa, tengah-bawah, huruf tebal condensed, satu kata kunci diwarnakan (kuning/hijau/merah).
7. **Rentak visual**: tukar syot setiap 1.5–3 saat (muka presenter ↔ produk ↔ tangan tekan panel ↔ grafik).

## Kenapa visual **tidak** dipotong (cut) dari video ini — semua dibina semula (recreate)

| Sebab | Butiran |
|---|---|
| Watermark TikTok bergerak | Logo TikTok + `@farracowayhq` / `@_syaifulaiman` tertanam dan berpindah kedudukan — tak boleh dibuang dengan bersih. |
| Hak cipta & wajah orang lain | Footage dan muka Farah / Syaiful milik mereka. Guna dalam iklan kita = risiko *takedown* & iklan ditolak Meta/TikTok. |
| Resolusi rendah | Fail 576×1024; bila dibesarkan ke 1080×1920 nampak kabur. |

**Yang boleh dipotong (cut):** klip milik kita sendiri dalam `assets/clips/` (Villaem 3 — tangan tekan panel 40°→50°→60°,
tangki dengan cahaya UV, jumlah kapasiti 11.4L). Tiada watermark, 1080×1920. Digunakan dalam V05.

## Pelan recreate setiap jenis syot

| Syot dalam rujukan | Cara kita bina semula |
|---|---|
| Presenter bercakap ke kamera | VO Gemini TTS + kapsyen besar bergerak (tiada muka), **atau** anda rakam muka sendiri 3–4 syot pendek dan saya sambung |
| Tangan tekan panel, bacaan LED 95°→40° | Replika panel dalam HTML/SVG: digit LED bertukar, riak "tap", jari animasi — lebih tajam daripada footage |
| Deretan Neon 5 warna di showroom | Gambar produk rasmi (PNG) diwarnakan 5 warna, disusun di atas "rak" animasi |
| Buka penutup, tukar filter, flushing | Ilustrasi keratan rentas: penutup terbuka → kartrij keluar/masuk → titisan air mengalir |
| Harga "RM54 → RM27" | Kad harga: angka lama dipangkah merah, angka baru *count-down* dengan pop kuning |
| End card TikTok (@handle) | Butang CTA WhatsApp + "penghantaran & pemasangan percuma" (tiada logo TikTok) |

## Fakta baharu daripada rujukan (masuk ke plan — **perlu disahkan**)

- **Neon**: RM54/bulan; **diskaun 50% selama 6 bulan → serendah RM27**; "tak sampai RM2 sehari"; tangki panas 1L, sejuk 1.5L,
  suhu bilik *direct flow*; 2 pakej: **beserta servis** atau **self-service** (Coway hantar filter percuma setiap 8 bulan, pelanggan tukar sendiri).
- **Villaem 3**: suhu panas 95 / 80 / 70°C, suam 60 / 50 / 40°C, + suhu bilik + sejuk; isipadu 120 / 250 / 500 / 1,000 ml / tanpa had;
  *child lock* tekan 3 saat; 2 warna Pebble Grey & White. R01 papar "RM18 sebulan" — bercanggah dengan RM74 dalam plan, jangan guna sebelum disahkan.
- Penghantaran & pemasangan percuma ke seluruh Malaysia (disebut dalam R03–R05).
