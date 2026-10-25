# Rujukan spec: pemain `scenes` dan `hype`

Diambil daripada spec sebenar dalam `videos/*/spec.json`. Kod pemain: `videos/lib/{engine,scenes,hype,story}.js`.
Jika perlukan elemen yang tiada di sini, baca kod pemain dulu. Jangan reka kunci baru.

## Masa

Semua `at` / `in` / `out` / `*At` ikut baris VO dalam `lines.json`:

| Ungkapan | Maksud |
|---|---|
| `"@07"` | mula baris 07 |
| `"@07e"` | hujung baris 07 |
| `"@07%40"` | 40 % ke dalam baris 07 |
| `"@07+0.3"`, `"@07e-0.2"` | anjakan saat |
| `0`, `3.5` | saat VO mentah (guna hanya untuk babak pertama `at: 0`) |

Kanvas 1080×1920. `top` dalam px dari atas. Logo jenama ada di atas kiri (±100 px), dan bar kapsyen VO pada 1520–1690 px, jadi elemen biasanya `top` 230–1300.

`out` boleh ditinggalkan untuk elemen yang kekal hingga tamat (contohnya `cta`). Kesan bunyi (whoosh, pop, impact, cha-ching) ditambah secara automatik ikut jenis elemen. `"hit": true` menambah hentakan.

## Kunci atas `spec.json`

```json
{
  "slug": "bajet-kecil-tak-boleh-cantik",
  "voice": "Aoede",
  "style": "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling",
  "theme": "coway", "brand": "COWAY", "tagline": "Own Your Aesthetics, Affordably.",
  "bpm": 100,
  "scenes": [ ... ], "els": [ ... ]
}
```

- `voice`: suara Gemini. Perempuan yang dah diguna: `Aoede` (mesra, paling kerap), `Kore`, `Sulafat` (emosi), `Laomedeia`, `Vindemiatrix`, `Zephyr`. Lelaki: `Orus` (yakin), `Puck`, `Fenrir` (hype), `Achird`, `Algieba`.
- `style`: gaya suara dalam English. Untuk `hype`, letak gaya suara dalam `style_tts`, kerana `style` ialah gaya visual (`kinetic`, `paper`, `comic`, `glow`, `ugc`).
- `theme: "coway"`: warna rasmi Coway (putih/biru `#04A4E4`). Tinggalkan hanya untuk gaya lama navy/kuning.
- `bpm`: muzik latar (100 lalai; 128 untuk hype). `"cap": false` (hype) mematikan kapsyen VO.

## Latar (`scenes`)

```json
{"at": 0, "bg": "pastel"}
{"at": "@02", "bg": {"image": "neon/podium5.jpg", "color": "pastel", "top": 420, "h": 1080, "mask": true}}
{"at": "@06", "bg": {"clip": "presenter", "c0": 6.4, "c1": 9.6}}
```

- `scenes`: warna `blue`, `navy`, `pastel`, `dark`, `night`, `pink`, `mint` (dengan `theme: "coway"`, ditukar kepada versi cerah Coway).
- `hype`: `k-blue|k-ink|k-white|k-sky|k-pink` (kinetic), `paper-blue|paper-cream|paper-pink|paper-sky`, `comic-blue|comic-pink|comic-sky|comic-white`, `glow-dark|glow-wall`, `ugc-blue|ugc-white`.
- `image`: di bawah `assets/img/`. `clip`: `assets/clips/neon/<nama>.mp4` atau `assets/clips/<nama>.mp4`. `c0`→`c1` ialah saat dalam klip, dan kelajuan mesti 0.55–1.9× (build_video beri amaran jika tidak).
- Klip sedia ada: Neon `presenter`, `press_pour`, `bottle_to_baby`, `bottles_busy`. Villaem 3 `clip1`–`clip5` (lihat `assets/clips/README.md`: jangan guna clip1 > 3 s kerana ada teks RM20 lama, dan clip3 > 7 s).
- Gambar rasmi produk lain ada dalam `brand-brain/coway/Other Brand Assets/<kategori>/<produk>/`. Salin yang perlu ke `assets/img/<produk>/` (laluan tanpa ruang kosong) sebelum guna.

## Elemen `scenes`

| type | Kunci | Contoh |
|---|---|---|
| `banner` | `top html` | `{"type":"banner","in":"@01","out":"@02","top":230,"html":"KENAPA RAMAI PASANG<br><em>COWAY NEON?</em>"}` |
| `title` | `top size html color shadow` | `{"type":"title","in":"@02","out":"@03","top":760,"size":200,"html":"3 SEBAB","color":"var(--yellow)"}` |
| `text` | `top html size weight color` | `{"type":"text","in":"@08%60","out":"@09","top":940,"html":"RM54 sebulan ÷ 30 hari"}` |
| `pill` | `top html bg color` | `{"type":"pill","in":"@01%50","out":"@03","top":900,"html":"RUMAH PERTAMA","bg":"var(--yellow)","color":"var(--navy)"}` |
| `stamp` | `top html color rot` | `{"type":"stamp","in":"@07%70","out":"@08","top":1080,"html":"BOLEH ✓","color":"#1faa59","rot":-8}` |
| `reason` | `top num title sub` | `{"type":"reason","in":"@03","out":"@04","top":250,"num":"1","title":"KOMPAK","sub":"tak makan ruang dapur"}` |
| `card` | `top icon title sub icbg iccolor` | `{"type":"card","in":"@07","out":"@08","top":760,"icon":"tech","title":"BESERTA SERVIS","sub":"Technician datang ke rumah"}` |
| `icon` | `top icon size color` | ikon: `tech box drop home clock shield lock filter money baby cup pipe phone palette check x ruler` |
| `chips` | `top items[{text color at}]` | `{"type":"chips","in":"@11","out":"@12","top":280,"items":[{"text":"PANAS","color":"#ff7a6b","at":"@11"},{"text":"SEJUK","color":"#6cc2ff","at":"@11%30"}]}` |
| `grid` | `top items[{big small color at}]` | `{"big":"1L","small":"AIR PANAS","color":"#ff7a6b","at":"@05"}` |
| `steps` | `top items[{text at}]` | langkah 1-2-3-4 |
| `led` | `top items[{num unit label at}]` | paparan suhu: `{"num":"95","label":"MI SEGERA","at":"@02"}` |
| `counter` | `top from to decimals dur prefix suffix size color` | `{"type":"counter","in":"@08%40","out":"@09","top":660,"from":0,"to":1.8,"prefix":"RM","decimals":2,"dur":0.8}` |
| `price` | `top label from strikeAt to toAt badge badgeAt amount per note noteAt` | `{"type":"price","in":"@12","out":"@14","top":520,"label":"HARGA ASAL","from":"RM104","strikeAt":"@12%45","to":"RM54","toAt":"@12%60","badge":"+ REBAT RM20 × 7 BULAN","badgeAt":"@13"}` |
| `photo` | `top left w h src shadow radius fit pos label float zx zy zs zin zout` | `src` relatif kepada `videos/<ID>/`: `"../../assets/img/neon/pink.jpg"` |
| `vs` | `top left{title color items at} right{...}` | perbandingan dua lajur (RO vs Nanotrap) |
| `quiz` | `top options[{text color at}] answer answerAt` | kuiz pilihan |
| `chat` | `top items[{side:"L"/"R" text at}]` | gelembung WhatsApp |
| `quote` | `top lines lineAt size dim hideCap` | petikan pelanggan |
| `bottles` | `top n fill dur w label` | `"label":"≈ {n} botol"` (kira botol air) |
| `delivery` | `top` | animasi penghantaran / pemasangan |
| `lineup` | `keys[{at unit zoom}]` | **Neon sahaja**: `unit` `pink mint ciel gray white all` |
| `cta` | `top button ticks fine btnAt tag dim` | lihat bawah |

CTA (wajib di hujung):

```json
{"type": "cta", "in": "@14", "top": 720,
 "ticks": ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"],
 "button": "WhatsApp saya", "btnAt": "@14%40",
 "fine": "*Harga asal RM104/bulan. Rebat RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway."}
```

## Elemen `hype`

| type | Kunci | Contoh |
|---|---|---|
| `words` | `top items[{txt at size color box bg hit}]` | `{"txt":"STOP!","at":"@01","hit":true,"size":330,"color":"#fff"}` |
| `tag` | `top pre big sub hit` | `{"type":"tag","in":"@02%35","out":"@04","top":760,"pre":"PROMO","big":"RM20","sub":"DAH BOLEH PASANG!","hit":true}` |
| `burst` | `html top size x color textColor fs rot hit` | letupan komik "ALAMAK!" |
| `ticker` | `top text rot bg color` | jalur teks bergerak |
| `img` | `src w top anim g float rot zoom hit` | `anim: "rise"`; `src` relatif kepada `videos/<ID>/` |
| `temps` | `top items[{k: hot/cold/room, at}]` | tiga suhu |
| `gift` | `openAt top size rays box ribbon` | kotak hadiah terbuka |
| `cta` | `top button fine btnAt fineColor` | seperti `scenes` |

## Pemain `story` (`videos/peti_ais.py`)

Spec guna `shots` (bukan `scenes`), `style_tts` dan `lift` (baris di mana muzik bertukar dari sedih ke gembira). Imej di bawah `assets/img/`, klip di `assets/clips/fridge/`. Lihat `videos/PA01/spec.json` dan docstring `videos/peti_ais.py`. Elemen: `big bubble cal cta feats kicker logo photo price prod quote stamp year`.
