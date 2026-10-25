---
name: coway-skrip
description: Tulis skrip video iklan Coway (10 setiap batch) daripada brief projek — pain point, hook, copywriting, bantahan, CTA — dalam projek/<kod>/skrip.md, dan dapatkan satu kelulusan user. Guna bila user minta tulis skrip, copywriting video, hook, "develop script", "batch skrip seterusnya", atau ubah skrip sebelum video dijana. Skill ini tidak menjana suara atau video.
---

# Skrip video Coway

Input: `projek/<kod>/brief.md` (dari `coway-persona-produk`), `research/persona.md` dan fail VoC produk dalam `research/` jika ada.
Output: `projek/<kod>/skrip.md` (batch 10 skrip) + kemas kini `projek/<kod>/README.md`.
Langkah seterusnya: `coway-video` (hanya selepas batch **DILULUSKAN**).

Tiada brief? Jalankan `coway-persona-produk` dulu, atau jika user dah beri produk + sudut dengan jelas, tulis brief ringkas sendiri.

## 1. Bahan

- Sudut, fakta, penafian dan "Jangan" dari `brief.md`. **Hanya** fakta dalam brief / `brand-brain/coway/products.md`.
- Bahasa pelanggan sebenar dari fail VoC (`research/<produk>-voc.md`, `research/peti-ais-coway-headline-research.md`, `tilam/padanan_pain_coway.md`). Guna frasa mereka dalam hook dan pain.
- Nada & ayat terbukti: `brand-brain/coway/brand-guide.md` §5. Formula hook dari video rujukan: `reference/README.md`.
- Skrip lama produk yang sama (`skrip/`, `projek/*/skrip.md`): elak hook berulang.

## 2. Pecahan batch 10

Agihkan 10 skrip ke sudut brief (2–3 skrip setiap sudut) dan variasikan **jenis hook**:

| Jenis hook | Contoh |
|---|---|
| Seru situasi | "Tilam dah 8 tahun, bangun pagi pinggang sakit?" |
| Soalan bantahan | "Coway mahal ke sebenarnya?" |
| Angka / kira | "Berapa kos air botol sebulan untuk family 5 orang?" |
| Cerita pertama | "Customer saya semalam cerita…" |
| Mitos vs fakta | "Coway semua RO ke? Tak." |
| Listicle | "3 tanda peti ais awak dah nak rosak" |
| Tarikh akhir (P3) | "Kalau dah lama survey, promo ni habis 31 hb." |

Setiap batch: sekurang-kurangnya 4 jenis hook berbeza dan 2 suara (lelaki/perempuan), supaya iklan boleh diuji.

## 3. Struktur satu skrip (30–45 s, 70–100 perkataan)

1. **Hook (≤ 3 s, baris 1):** situasi/soalan/angka dalam bahasa persona. Bukan salam, bukan nama sendiri, bukan nama produk dulu.
2. **Pain / agitate (2–3 baris):** akibat yang persona rasa (duit, masa, malu, risau), guna frasa VoC.
3. **Penyelesaian + mekanisme (2–3 baris):** produk + *kenapa* ia berfungsi (fakta brief).
4. **Bukti / bantahan (1–2 baris):** servis HEART, lencana, angka, atau jawapan bantahan utama.
5. **Tawaran:** harga RM yang disahkan (tiada peratus diskaun).
6. **CTA:** "WhatsApp saya" (+ desakan masa jika promo bertarikh).

Peraturan wajib:
- Kita **ejen sah Coway** ("saya", "customer saya"). Bukan Coway Malaysia; tiada Careline 1800-888-111.
- Penafian: UV 99.9% → "Berdasarkan ujian TÜV SÜD Korea dalam persekitaran terkawal."; promo → "*Tertakluk terma & syarat"; angka Silver Ion/deodoriser peti ais → nota kaki.
- Kesihatan (susu bayi, asma, resdung): "ikut nasihat doktor"; tiada dakwaan perubatan.
- Pakej untuk dijual: tiada nama/no ejen; CTA umum.

## 4. Format `skrip.md`

```markdown
# Skrip: <kod> — Batch 1 (01–10)

Status: DRAF | DILULUSKAN <tarikh> · Brief: brief.md · Harga disahkan: <tarikh>

| ID | Hook | Sudut | Jenis hook | Suara | Format cadangan | ±saat |
|---|---|---|---|---|---|---|

---
### <ID> · <tajuk pendek>
Sudut: <#> · Persona: <ID> · Kesedaran: <tahap> · Suara: <L/P, gaya>

| # | VO (apa disebut) | Kapsyen skrin | Visual |
|---|---|---|---|
| 01 | Tilam dah lapan tahun, bangun pagi pinggang sakit? | Tilam dah *8 tahun*? | close-up orang pegang pinggang |
| … |

CTA: … · Penafian: …
```

- Lajur **VO** = teks TTS: nombor dalam perkataan ("lima puluh empat ringgit"), "Kowei" jika sebutan Coway bermasalah.
- Lajur **Kapsyen** = teks skrin: angka, `*sorotan*`, "Coway".
- ID video ikut konvensyen `coway-video` (kod produk 2 huruf + nombor, sambung dari `ls videos/`).

## 5. Kelulusan (sekali sebatch)

Tunjuk user jadual ringkasan (10 hook) dalam chat, dengan skrip penuh dalam fail. Minta **satu** kelulusan. Ubah ikut komen, tukar status kepada `DILULUSKAN <tarikh>`, kemas kini papan status, commit.
Jika user dah kata "terus buat video", luluskan sendiri dan teruskan ke `coway-video`.

Batch 2 (11–20) ditulis hanya selepas batch 1 siap video dan diluluskan. Gunakan keputusan review / data iklan batch 1: lebih banyak variasi untuk hook dan sudut yang menang.
