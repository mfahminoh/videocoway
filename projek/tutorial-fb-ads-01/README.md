# Tutorial Profile, Page & Ads Manager — tutorial-fb-ads-01

Video tutorial untuk pemula (ejen): beza Facebook Profile, Page dan Ads Manager, susunan Business Portfolio → Page / Akaun Iklan → Campaign / Ad Set / Ad, dan cara create Page, Portfolio dan akaun iklan. Visual (kapsyen terbakar, tanpa audio) disediakan user; repo ini tambah suara latar.

| Langkah | Status | Fail | Nota |
|---|---|---|---|
| Skrip | ✅ | skrip_suara_latar.txt, kapsyen.srt | dari user, 12 babak / 40 kapsyen |
| Visual | ✅ | videos/TF01/visual_tanpa_vo.mp4 | dari user, 1080×1920, 214.8 s, tiada audio |
| VO + video | ✅ | out/tutorial-fb-ads-01/TF01_profile_page_adsmanager.mp4 | Gemini TTS (Kore), satu baris satu kapsyen |

## Cara jana semula

```bash
python3 videos/tutorial-fb-ads-01_vo.py              # jana baris yang tiada + mix + mux
python3 videos/tutorial-fb-ads-01_vo.py --redo 3,28  # jana semula baris tertentu
```

Setiap baris SRT dijana berasingan (`videos/TF01/line_NN.wav`), diletak pada masa mula kapsyennya dan dipercepat sehingga ×1.25 jika tak muat. Masa sebenar dalam `videos/TF01/timing.json`. URL disebut "business titik facebook titik com" / "ads manager titik facebook titik com" (kapsyen kekal).

## Keputusan
- 2026-11-12: suara Kore (perempuan, mesra/tenang), tiada muzik latar. 3.1-preview diutamakan kerana 3.8 / 2.5 kerap membaca arahan gaya; setiap baris disemak panjangnya (aksara ÷ 14.5/s) dan dijana semula jika tak munasabah.
- 2026-11-12: kuota percuma harian Gemini TTS (10 permintaan/model/hari) habis; baris 25, 31, 33–35, 38–40 dijana dengan `gemini-3.8-flash-lite-tts` tanpa arahan gaya (`TTS_MODELS=... TTS_FIRST_ATTEMPT=3`). Transkrip semakan penuh sepadan dengan skrip.
- Masa: VO paling lewat ~1.6 s di belakang kapsyen (baris 21–26, langkah Create Page) dan ~1 s di baris 39–40; baris lain dalam slot kapsyen. Banyak baris dipercepat ×1.1–1.25 kerana slot SRT ketat.

## Terbuka
- [ ] User dengar sebutan istilah Inggeris (Profile, Ads Manager, Business Portfolio, Ad Set) dan URL.
- [ ] Muzik latar lembut? (belum ditambah)
- [ ] Baris 25, 31, 33–35, 38–40 dari model lite: semak warna suara sama dengan baris lain; jana semula dengan 3.1-preview bila kuota pulih jika perlu (`--redo`).
