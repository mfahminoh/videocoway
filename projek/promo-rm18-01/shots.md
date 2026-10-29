# Shot Google Flow — promo-rm18-01 (showroom panning, penapis air)

Video promo 10–15 s, potret 9:16. Setiap video = 1–2 klip Flow (8 s) + VO + teks promo "Serendah RM18" + CTA WhatsApp (ditambah oleh `videos/build_video.py`, bukan oleh Flow).

## Kaedah: gambar rasmi → still 9:16 → video (wajib untuk setiap shot)

Ujian 30 Okt 2026: Text to Video tanpa rujukan melukis "penapis air" generik (bentuk salah, logo rosak). Gambar rasmi pula tak boleh terus jadi frame pertama, kerana kebanyakannya 1:1 atau banner lebar (contoh `coway-neon-5-colours-1-perfect-fit.jpg` 1920×403) dan latarnya studio. Jadi setiap shot ada dua langkah:

1. **Still (Image, Nano Banana 2.1, 9:16, x2, 0 kredit):** lampirkan 2–3 gambar rasmi produk (butang **+** → Upload media → Add to prompt) dan tampal prompt still. Prompt menyebut bentuk produk secara terperinci (bahagian "Bentuk" di bawah). Semak still dengan gambar rasmi: siluet, panel kawalan, paip, dulang, warna. Jana semula sehingga tepat. Pilih still yang tiada teks rosak di latar.
2. **Video (Video → Frames, Veo 3.1 Fast untuk cuba / Quality untuk take akhir, 9:16, x2):** Start = still yang lulus, tampal prompt video. Prompt hanya gerakan kamera kecil + "keep exactly as shown in the first frame" + bentuk ringkas.

Ingredients to Video (rujukan tanpa frame pertama) tidak dipakai: model melukis semula produk dalam babak baru, jadi bentuk boleh lari.

Peraturan prompt: jangan tulis ukuran mm/cm (model melukis label), tiada orang, tiada papan tanda/teks. Pergerakan kamera perlahan sahaja; produk adalah objek tegar.

**Nama fail muat turun:** `promo-rm18-01_sNN.mp4` (ikut lajur Fail).

| Shot | Produk | Gambar rujukan (`brand-brain/coway/Other Brand Assets/water-purifier/…`) | Fail |
|---|---|---|---|
| s01 | NeoN ×5 warna, sebaris di kaunter | `neon/coway-neon-water-purifier-peach-pink-colour.jpg`, `neon/coway-neon-water-purifier-porcelain-white-colour.jpg`, `neon/coway-neon-water-purifier-mint-green-colour.jpg` | assets/clips/promo-rm18-01_s01.mp4 |
| s02 | NeoN ×3 (putih, mint, pink) di meja oak | sama seperti s01 | assets/clips/promo-rm18-01_s02.mp4 |
| s03 | NeoN ×5 di atas pedestal bertingkat | `neon/coway-neon-water-purifier-ciel-blue-colour.jpg`, `neon/coway-neon-water-purifier-pebble-gray-colour.jpg`, `neon/coway-neon-water-purifier-peach-pink-colour.jpg` | assets/clips/promo-rm18-01_s03.mp4 |
| s04 | Villaem 3, pebble gray + porcelain white | `villaem3/coway-Villaem3-in-pebble-gray-porcelain-white.jpg`, `villaem3/coway-villaem3-with-eco-mode-features.jpg`, `villaem3/coway-villaem-3-side-view2.jpg` | assets/clips/promo-rm18-01_s04.mp4 |
| s05 | Neo Plus, hero | `neoplus/coway-neo-plus-front-view.jpg`, `neoplus/coway-neo-plus-right-side-view.jpg`, `neoplus/coway-neo-plus-button-and-faucet.jpg` | assets/clips/promo-rm18-01_s05.mp4 |

## Bentuk produk (tampal dalam prompt)

- **NeoN (CHP-6210N):** a compact upright box with an inverted-L side profile, a wide rectangular top head that cantilevers forward over a narrower, recessed lower body, a flat front face on the head with a thin printed control panel row of small icons and one teardrop button, a hidden faucet tucked under the overhang, vertical vent slits on the side, flat base with no drip tray, smooth matte single-colour finish, softly rounded edges.
- **Villaem 3 (CHP-7320L):** a slim, tall, upright rectangular tower with crisp straight edges; a raised square control slab on the upper front with a small digital temperature readout and touch icons; two small square clear faucet heads directly under the slab; two flat vertical rectangular push paddles on the lower front; a thin flat base plate; side profile with a shallow overhang at the top front and vertical vent slits at the rear. Colours: pebble gray (dark charcoal, brushed) and porcelain white.
- **Neo Plus (CHP-264L):** a compact white countertop box with a softly rounded top and corners; a recessed rectangular brushed-silver front panel on the upper middle with small indicator icons and a row of round buttons; a chrome push-button faucet on the left and a round chrome dial faucet on the right, each with a small clear guard; a white slotted drip tray protruding at the front base; horizontal vent slats high on the side.

## s01 — Pan sepanjang kaunter NeoN (pembuka)

Still:
```
Vertical 9:16 photo. Use the three reference images as the exact product: the Coway NeoN countertop water purifier. Reproduce its shape exactly: a compact upright box with an inverted-L side profile, a wide rectangular top head that cantilevers forward over a narrower, recessed lower body, a flat front face on the head with a thin printed control panel row of small icons and one teardrop button, a hidden faucet tucked under the overhang, vertical vent slits on the side, flat base with no drip tray, smooth matte single-colour finish, softly rounded edges. Scene: a bright, modern home-appliance showroom in a Malaysian shopping mall. Five NeoN units in a neat row on a long white display counter with a light oak edge, colours left to right: porcelain white, mint green, peach pink, ciel blue, pebble gray. Three-quarter view from chest height, the nearest unit sharp, the others falling gently out of focus. Bright daylight-balanced lighting, soft reflections on the glossy counter. Background: blurred showroom with plain white walls, soft arches and warm downlights, no signage, no text, no people. Realistic commercial product photography.
```
Video (Frames, Start = still):
```
Vertical 9:16 video. Keep every water purifier exactly as shown in the first frame: same inverted-L box shape with the top head overhanging the narrower lower body, same flat control panel, same colours, proportions and details. The products are rigid objects and never change shape. Very slow, smooth camera truck from left to right along the display counter at chest height, with a subtle push-in toward the row. Soft daylight sweeps gently across the matte surfaces, gentle reflections on the glossy white counter. Calm, premium showroom atmosphere. No people, no new objects, no text, no subtitles.
```

## s02 — Dolly masuk ke meja NeoN (pembuka alternatif)

Still:
```
Vertical 9:16 photo. Use the three reference images as the exact product: the Coway NeoN countertop water purifier. Reproduce its shape exactly: a compact upright box with an inverted-L side profile, a wide rectangular top head that cantilevers forward over a narrower, recessed lower body, a flat front face on the head with a thin printed control panel row of small icons and one teardrop button, a hidden faucet tucked under the overhang, vertical vent slits on the side, flat base with no drip tray, smooth matte single-colour finish, softly rounded edges. Scene: inside a clean, minimalist appliance showroom in Kuala Lumpur, white walls, warm accent lighting. Three NeoN units side by side on a light oak display table, porcelain white, mint green and peach pink, seen from the front at a slight angle, centred in frame with space above. Gentle bokeh highlights in the background. Calm, inviting, high-end commercial look. No signage, no text, no people.
```
Video:
```
Vertical 9:16 video. Keep the three water purifiers exactly as shown in the first frame: same inverted-L box shape, same control panel, same colours and proportions. The products are rigid objects and never change shape. Smooth, slow forward dolly toward the display table, the camera itself is never visible. Gentle parallax as the background softly drifts out of focus. Calm, inviting mood, steady natural light. Plain walls, no store signage. No people, no hands, no camera equipment, no lens flares, no new objects, no text, no subtitles.
```
Versi pertama menyebut "on a gimbal" dan "bokeh drifting": Veo melukis tangan memegang gimbal dan bulatan bokeh besar dalam bingkai.
```

## s03 — NeoN 5 warna di pedestal

Still:
```
Vertical 9:16 photo. Use the three reference images as the exact product: the Coway NeoN countertop water purifier. Reproduce its shape exactly: a compact upright box with an inverted-L side profile, a wide rectangular top head that cantilevers forward over a narrower, recessed lower body, a flat front face on the head with a thin printed control panel row of small icons and one teardrop button, a hidden faucet tucked under the overhang, vertical vent slits on the side, flat base with no drip tray, smooth matte single-colour finish, softly rounded edges. Scene: five NeoN units in porcelain white, mint green, peach pink, ciel blue and pebble gray, each standing on its own matte white display pedestal of a different height, arranged in a staggered cluster in a bright showroom corner. Soft studio light, pale grey background, gentle shadows. No signage, no text, no people. Realistic commercial product photography.
```
Video:
```
Vertical 9:16 video. Keep all five water purifiers exactly as shown in the first frame: same inverted-L box shape, same control panel, same colours and proportions. The products are rigid objects and never change shape. Very slow, smooth camera truck from left to right across the pedestals with a subtle push-in. Soft studio light sweeps gently across the matte surfaces. Clean showroom atmosphere. No new objects, no text, no subtitles.
```

## s04 — Villaem 3 dua warna

Still:
```
Vertical 9:16 photo. Use the three reference images as the exact product: the Coway Villaem 3 water purifier. Reproduce its shape exactly: a slim, tall, upright rectangular tower with crisp straight edges; a raised square control slab on the upper front with a small digital temperature readout and touch icons; two small square clear faucet heads directly under the slab; two flat vertical rectangular push paddles on the lower front; a thin flat base plate; side profile with a shallow overhang at the top front and vertical vent slits at the rear. Scene: two Villaem 3 units side by side on a white showroom display counter, left one pebble gray (dark charcoal, brushed), right one porcelain white, angled slightly toward each other, seen from a low three-quarter angle. Premium showroom with soft warm downlights and a softly blurred background. No signage, no captions, no text labels, no people. Realistic commercial product photography.
```
Video:
```
Vertical 9:16 video. Keep both water purifiers exactly as shown in the first frame: same slim tower shape, same control slab, faucets, paddles, colours and proportions. The products are rigid objects and never change shape. Slow cinematic orbit of about 15 degrees around the units with a gentle push-in. A soft highlight glides across the front panels. Premium, calm mood. No people, no new objects, no text, no subtitles.
```

## s05 — Neo Plus hero

Still:
```
Vertical 9:16 photo. Use the three reference images as the exact product: the Coway Neo Plus water purifier. Reproduce its shape exactly: a compact white countertop box with a softly rounded top and corners; a recessed rectangular brushed-silver front panel on the upper middle with small indicator icons and a row of round buttons; a chrome push-button faucet on the left and a round chrome dial faucet on the right, each with a small clear guard; a white slotted drip tray protruding at the front base; horizontal vent slats high on the side. Scene: one Neo Plus unit alone on a white showroom display counter with a light oak edge, three-quarter front view, the unit filling the middle of the frame with space above. Soft showroom lighting, subtle reflection on the counter, blurred bright background. No signage, no text, no people. Realistic commercial product photography.
```
Video:
```
Vertical 9:16 video. Keep the water purifier exactly as shown in the first frame: same rounded white body, silver front panel, chrome faucets, drip tray, colour and proportions. The product is a rigid object and never changes shape. Slow vertical crane move from the base up to the top of the unit with a slight push-in, soft showroom lighting, subtle reflections on the counter. Clean, premium product-commercial look. No people, no new objects, no text, no subtitles.
```

## Take terpilih

Dijana 30 Okt 2026, Flow projek "Oct 30 - 00:46" (akaun PRO), Veo 3.1 Fast, 720p dinaikkan ke 1080×1920 30fps tanpa audio. Semua klip 8 s.

| Shot | Still | Take / model | Nota semakan (bentuk, logo, teks rosak) |
|---|---|---|---|
| s01 | Still A: 5 NeoN sebaris, kaunter putih tepi oak, lengkung kayu | Take 1 / Veo 3.1 Fast (take 2 gagal audio, dipulangkan) | Bentuk L terbalik, panel & warna kekal 8 s. Dari ±4 s papan tanda "COWAY" muncul di dinding latar (tulisan jelas, bukan rosak); tutup dengan overlay atau potong sebelum 4 s jika perlu. Diluluskan user. |
| s02 | Still A: 3 NeoN (putih, mint, pink) di meja oak, pokok di latar | Take 4 (prompt v2) / Veo 3.1 Fast | Dolly masuk ke unit putih, berakhir pada close-up panel kawalan NeoN (ikon & titisan tepat). Prompt v1 (take 1–2) ditolak: tangan memegang gimbal masuk bingkai, bulatan bokeh besar. |
| s03 | Still A: 5 NeoN di pedestal putih bertingkat | Take 1 / Veo 3.1 Fast | Truck perlahan, kelima-lima unit kekal bentuk & warna. Take 2 push-in terlalu kuat. |
| s04 | Still A: Villaem 3 pebble gray + porcelain white di kaunter putih | Take 2 / Veo 3.1 Fast | Menara nipis, panel paparan "95°", paip segi empat & pedal kekal. Saat ±1–2 cahaya menyapu menjadikan unit kelabu nampak perak seketika. Take 1 sama, tapi unit putih terlalu terang di ±4 s. |
| s05 | Still A: Neo Plus di kaunter putih tepi oak | Take 2 / Veo 3.1 Fast | Crane naik dengan push-in: panel perak, dua paip krom, dulang, logo "coway" kekal. 1.5 s terakhir hanya bucu atas unit; guna 0–6.5 s. Take 1 kehilangan paip kiri di ±6 s. |
