---
name: coway-riset
description: Riset sahaja untuk iklan Coway — fakta produk, pasaran & pesaing, atau voice of customer (VoC) dan persona pembeli — dan simpan hasilnya dalam research/ (termasuk kemas kini research/persona.md). Guna bila user minta riset, research, kaji, cari pain point, frustrasi pelanggan, apa orang cakap pasal <produk>, pesaing, persona, VoC, atau analisis chat WhatsApp / komen. Skill ini tidak menulis skrip, video atau poster.
---

# Riset Coway

Kerja skill ini **berhenti pada fakta dan bukti**. Ia tidak menulis skrip, tidak memilih produk untuk projek, dan tidak menjana video.
Langkah seterusnya: `coway-persona-produk`.

## 0. Mula

1. Baca [`research/README.md`](../../../research/README.md) dan [`research/persona.md`](../../../research/persona.md). Jangan ulang riset yang dah ada. Sambung atau kemas kini fail sedia ada.
2. Kenal pasti mod daripada permintaan user (boleh lebih dari satu):

| Mod | Soalan | Output |
|---|---|---|
| **Produk** | Apa fakta, ciri, harga, terma sebenar <produk>? | `research/<produk>-produk.md` dan kemas kini `brand-brain/coway/products.md` jika harga/fakta berubah |
| **Pasaran** | Siapa pesaing, apa sudut mereka, apa yang tepu, apa yang kosong? | `research/<produk>-pasaran.md` |
| **VoC / persona** | Apa pelanggan *sendiri* kata: frustrasi, keinginan, bantahan, pencetus beli? | `research/<produk>-voc.md` dan kemas kini `research/persona.md` |

Jika skop tak jelas (produk mana, untuk siapa), tanya **sekali** dan teruskan.

## 1. Sumber

Guna sumber yang ada dalam sesi. Catat setiap sumber yang dicuba, termasuk yang kosong.

| Sumber | Cara | Guna untuk |
|---|---|---|
| Laman rasmi coway.com.my | WebFetch, `brand-brain/fetch_assets.py <produk>`, `brand-brain/coway/Other Brand Assets/<kategori>/<produk>/copy.md` | Produk (satu-satunya sumber fakta & dakwaan) |
| Forum & media sosial awam: Facebook group, Threads, Lemon8, Lowyat, Carigold, TikTok, Reddit | WebSearch (`extended` untuk niche), WebFetch | VoC, pasaran |
| Meta Ad Library | Meta Ads connector `ads_library_search` | Pasaran: sudut & tawaran pesaing / ejen lain |
| Prestasi iklan ejen (akaun yang user urus) | Meta Ads connector: perbualan & kos setiap perbualan ikut sudut kreatif | Persona (hipotesis): sudut mana yang tarik mesej |
| Chat WhatsApp, komen, ulasan, nota jualan yang user beri | Fail yang dimuat naik / Drive | VoC (satu-satunya sumber yang boleh **sahkan** persona) |
| Riset lama | `research/`, `tilam/research/*.xlsx`, `JEREBU_PACKAGE.md`, `reference/` | Semua |

Untuk riset besar merentas banyak sumber, guna skill `deep-research` dan simpan laporannya di sini.

## 2. Peraturan bukti

- **Petikan verbatim** dengan sumber + tarikh untuk setiap dakwaan VoC. Ringkasan sendiri bukan bukti.
- Copy iklan ejen ialah bukti **sudut yang berfungsi**, bukan suara pelanggan.
- Fakta produk hanya dari laman rasmi Coway. Dakwaan (99.9%, Halal, NSF) disalin tepat berserta syaratnya.
- Nyatakan **bias** setiap sumber (contohnya Lowyat = lelaki urban berbahasa Inggeris; responden iklan = cenderung pada harga dan impulsif).
- Angka prestasi iklan: laporkan **kos setiap perbualan** di sebelah jumlah, kerana jumlah ikut bajet, bukan permintaan.

## 3. Persona (`research/persona.md`)

Persona = **situasi membeli** (pencetus + halangan + penyelesaian sebelum ini), bukan demografi, saluran, manfaat atau jenis transaksi.
Contoh yang dibuang: "suri rumah" (demografi), "pemburu promo" (transaksi), "lead marketplace" (saluran).

Bila kemas kini:
- Tambah bukti baru di bawah persona sedia ada; jangan cipta persona baru jika ia cuma variasi.
- Tukar status hanya ikut pintu ini: `HIPOTESIS` → `DISAHKAN` bila ada **≥ 2 petikan verbatim pelanggan** dari sumber berbeza. `DIBUANG` bila data menolak; tulis sebabnya.
- Kekalkan ID (P1, P2, H1 …) supaya `brief.md` projek lama masih merujuk dengan betul.
- Setiap persona ada baris **Produk lazim** (dibaca oleh `coway-persona-produk`).

## 4. Format fail riset

```markdown
# <Produk/topik> — <Produk | Pasaran | VoC>

Tarikh: <hari ini> · Sumber: <senarai> · Sumber kosong: <senarai>
Had & bias: <ayat pendek>

## Ringkasan (5 baris)
## Penemuan  (setiap satu: dakwaan → petikan/angka → sumber, tarikh)
## Sudut yang tepu / sudut yang kosong   (mod pasaran)
## Bank bahasa pelanggan                 (mod VoC: frasa sebenar untuk hook & copy)
## Perlu disahkan dengan user / HQ
```

Selepas tulis, tambah baris dalam jadual `research/README.md`, commit, dan beritahu user 3–5 penemuan paling penting + apa yang masih perlu disahkan.
