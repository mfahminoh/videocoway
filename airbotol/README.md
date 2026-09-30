# Coway Neo Plus — "Menyampah Tengok Air Botol" (Portrait 1080×1920, ±1:42)

Motion graphic bercerita dari sudut **ejen Coway (suara perempuan)** tentang customer terbaru:
3 tahun hidup "berkisar dekat air botol" (48 → 72 botol seminggu, stock hunting, kotak makan space,
masih jerang air) → balik kampung, mak dah pasang Coway ("Sonang kojo!") → tak tahan, pasang Neo Plus
→ RM59/bulan, 7 bulan pertama RM20 → CTA WhatsApp.

Skrip & cadangan visual: [`skrip.md`](skrip.md). Output: `out/airbotol_final.mp4`.

## Bina semula
```
python airbotol/timeline.py                    # anggaran daripada teks (sebelum ada suara)
python voiceover/generate_vo_gemini.py --lines airbotol/lines.json --clips airbotol/clips --batch 7
python airbotol/timeline.py --clips airbotol/clips   # slot = tempoh klip sebenar
python render.py --page airbotol/index.html --out out/airbotol_video_noaudio.mp4 --workers 4
python airbotol/audio.py                       # muzik + SFX (ikut lines.json)
python mix.py --project airbotol               # -> out/airbotol_final.mp4
```

## Nota suara
- Suara: Gemini TTS `Sulafat` (perempuan). Klip disimpan dalam `clips/` supaya boleh bina semula tanpa kuota.
- Dalam teks suara, "Coway" di baris 13 & 17 ditulis **"Kowei"** (ejaan sebutan) kerana suara AI tersilap sebut
  jenama ("CCTV", "Coenzyme"). Sarikata (`airbotol.srt`) tetap tulis "Coway".
- "Sonang kojo!" = loghat Negeri Sembilan untuk "senang kerja"; dipaparkan dengan sarikata *(senang kerja)*.
