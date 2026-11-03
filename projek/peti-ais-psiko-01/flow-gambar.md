# Gambar peti ais untuk PA38–PA42 — jana di Google Flow (manual)

API imej Google dari sesi Claude: kuota habis (HTTP 429, 2 Nov 2026). Seedream: akaun BytePlus tertunggak. Jadi gambar dijana manual di Flow.

## Cara
1. Buka **labs.google/flow** → projek baru → pilih **Image** (Nano Banana / Imagen), nisbah **3:4** (potret).
2. Muat naik **gambar rujukan** (kolum "Rujukan") sebagai *ingredient / reference*, supaya bentuk peti sama dengan produk sebenar.
3. Tampal prompt. Jana 2–4 variasi, pilih yang **bentuk peti, pintu, pemegang & panel sama** dengan rujukan, tiada logo/teks pelik.
4. Muat turun dan namakan ikut kolum "Nama fail". Muat naik 6 fail ke sesi Claude ini.
5. Claude akan letak dalam `assets/img/peti-ais-psiko-01/` dan render semula PA38–PA42 (pasangan berbeza setiap video).

Rujukan ada dalam repo: `brand-brain/coway/Other Brand Assets/refrigerator/`.

| Nama fail | Rujukan | Prompt |
|---|---|---|
| `g551_a.jpg` | `multidoor551l/fridge_551L_homebanner_fridge_mobile.png` | Place this exact refrigerator (same shape, black matte finish, four doors, handles and control panel; do not add or change any logo or text) with all doors closed, in a bright modern Malaysian terrace-house kitchen with white cabinets and a light wood counter, soft morning daylight. Photorealistic. The entire refrigerator visible top to bottom, centered, straight-on, eye level. No people, no text. |
| `g551_b.jpg` | sama | Same refrigerator, doors closed, built into a warm-toned Malaysian condo kitchen with beige cabinets and pendant lights, evening ambience. Photorealistic, entire fridge visible top to bottom, centered. No people, no text. |
| `g551_c.jpg` | sama | Same refrigerator, doors closed, in a clean Malaysian family kitchen with a basket of fresh vegetables and fruit on the counter beside it, natural daylight. Photorealistic, entire fridge visible top to bottom, centered. No people, no text. |
| `g715_a.jpg` | `sidebyside715l/Coway_SBS715-Refrigerator_Card1_V2.jpg` | Place this exact two-door side-by-side refrigerator (same shape, black finish, handles and control panel; do not add or change any logo or text) with doors closed, in a bright modern Malaysian kitchen with white cabinets and grey tiles, soft daylight. Photorealistic, entire fridge visible top to bottom, centered, eye level. No people, no text. |
| `g715_b.jpg` | sama | Same refrigerator, doors closed, in a spacious Malaysian family kitchen with wooden cabinets and a dining table in soft focus, warm afternoon light. Photorealistic, entire fridge visible top to bottom, centered. No people, no text. |
| `g715_c.jpg` | sama | Same refrigerator, doors closed, in a minimalist condo kitchen with dark grey cabinets and warm under-cabinet lighting, evening. Photorealistic, entire fridge visible top to bottom, centered. No people, no text. |

Pasangan (sedia dalam `videos/peti-ais-psiko-01_batch.py` selepas fail dimuat naik): PA38 a+a · PA39 b+b · PA40 c+c · PA41 a+b · PA42 b+c.
