---
name: coway-iklan
description: Lancarkan iklan Meta untuk projek video Coway — (A) servis iklan untuk ejen di akaun iklan ejen (video, WhatsApp ejen) atau (B) iklan jual pakej video di page user sendiri (poster/video pakej, komen/DM) — ikut struktur 1 kreatif = 1 kempen, cipta dalam keadaan paused, dan jadualkan audit. Guna bila user kata "run iklan", "publish iklan", "lancar kempen" untuk projek video Coway, ejen klien, atau pakej video.
---

# Iklan projek video Coway

Input: video `out/<kod>/*.mp4` atau poster `out/<kod>/poster/*.png` yang **diluluskan**, `projek/<kod>/brief.md`, papan status.
Alat: Meta Ads connector. Peraturan tetap: `CLAUDE.md` (1 kempen = 1 ad set = 1 iklan; bajet yang disebut = bajet setiap kempen).

## 1. Aliran mana?

| | **A · Servis iklan ejen** | **B · Jual pakej video** |
|---|---|---|
| Akaun iklan | Akaun ejen klien | Akaun user sendiri |
| Kreatif | Video jenis iklan (pelanggan akhir) | Poster jenis B / video sampel pakej |
| Destinasi | WhatsApp ejen | Mesej / komen ke user (atau WhatsApp user) |
| Audiens | Pelanggan akhir di kawasan ejen (persona dari brief) | Ejen Coway / jurujual (minat: Coway, direct sales, ejen) |
| Klien baru | Skill `coway-onboarding-klien` dulu | — |

Jika tak jelas, tanya user: aliran mana, akaun iklan/page mana, bajet setiap kempen, tempoh.

## 2. Sediakan

- Pilih kreatif: video "Lulus" dari review (A) atau poster/video pakej (B). Satu kreatif satu kempen.
- Copy iklan: primary text dari skrip/hook kreatif itu (A: bahasa persona, harga + "*Tertakluk", nama ejen jika ada; B: dari `threads.md`). Headline ≤ 40 aksara.
- Nama kempen: `<kod> | <ID kreatif> | <A/B> | <tarikh>`, supaya audit boleh padankan prestasi dengan sudut dan persona.

## 3. Cipta (sentiasa paused)

Cipta setiap kempen dengan status **PAUSED**. Tunjuk user ringkasan: akaun, bilangan kempen, bajet setiap kempen × hari = jumlah, audiens, kreatif. **Aktifkan hanya selepas user sahkan**, kerana ini membelanjakan wang.

## 4. Rekod & audit

- Kemas kini `projek/<kod>/README.md` langkah 7: akaun, ID kempen, kreatif, bajet, tarikh mula.
- Selepas 3–5 hari: skill `coway-ads-audit` (kos setiap perbualan ikut kreatif/sudut). Tulis keputusan dalam papan status: sudut & hook yang menang, yang dihentikan.
- Hantar keputusan ke langkah awal: hook/sudut menang → `coway-skrip` batch seterusnya; persona yang terbukti/gagal → `coway-riset` (kemas kini `research/persona.md`).
- Laporan untuk klien: skill `coway-ads-dashboard`.
