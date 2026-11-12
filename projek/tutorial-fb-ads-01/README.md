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
- 2026-11-12: suara Kore (perempuan, mesra/tenang), tiada muzik latar. Model dikunci ke `gemini-3.1-flash-tts-preview` kerana 3.8 / 2.5 kerap membaca arahan gaya.

## Terbuka
- [ ] User dengar sebutan istilah Inggeris (Profile, Ads Manager, Business Portfolio, Ad Set) dan URL.
- [ ] Muzik latar lembut? (belum ditambah)
