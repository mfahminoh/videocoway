"""Batch 5 video Coway Neon "high energy" (HN01-HN05), setiap satu gaya visual berbeza, flow sama:
   Promo RM20 dah boleh pasang > Neon model mampu milik > lengkap panas/sejuk/suhu bilik > free gift premium > WhatsApp sekarang.

    python videos/hype_batch.py                       # tulis videos/HNxx/{lines.json, spec.json}
    python voiceover/gemini_tts.py videos/HN01/lines.json videos/HN01/vo.wav --voice Fenrir --style "..."
    python videos/build_video.py HN01 --render --review out/hype

Pemain: videos/lib/hype.js + hype.css ("player": "hype"). Gaya: kinetic, paper, comic, glow, ugc.
Harga/promo ikut ayat pengguna (7/10): "Promo RM20 dah boleh pasang" + "free gift premium" (hadiah tidak dinamakan).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
IMG = "../../assets/img/hype/"
PINK, LINEUP = IMG + "neon_pink.png", IMG + "lineup_cut.png"
CW, INK, PK, YL, WHITE = "#04A4E4", "#2f3337", "#ff8fb1", "#ffd23f", "#fff"
FINE = "*Tertakluk pada terma &amp; syarat promosi semasa Coway."
PRES_C = {"clip": "presenter", "c0": 6.4, "c1": 8.6}
PRES_W = {"clip": "presenter", "c0": 0.0, "c1": 3.0}
POUR = {"clip": "press_pour", "c0": 3.0, "c1": 6.6}
PREP = {"clip": "press_pour", "c0": 0.0, "c1": 3.0}


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c} for i, (t, c) in enumerate(rows)]


def w(txt, at, size=None, color=None, **kw):
    d = {"txt": txt, "at": at, **kw}
    if size:
        d["size"] = size
    if color:
        d["color"] = color
    return d


def words(at, out, top, *items, **kw):
    return {"type": "words", "in": at, "out": out, "top": top, "items": list(items), **kw}


def img(at, out, src, width, top, anim="pop", **kw):
    return {"type": "img", "in": at, "out": out, "src": src, "w": width, "top": top, "anim": anim, **kw}


def temps(at, out, top, hot, cold, room):
    return {"type": "temps", "in": at, "out": out, "top": top, "items": [{"k": "hot", "at": hot}, {"k": "cold", "at": cold}, {"k": "room", "at": room}]}


def gift(at, out, open_at, top, size=620, **kw):
    return {"type": "gift", "in": at, "out": out, "openAt": open_at, "top": top, "size": size, **kw}


def burst(at, out, html, top, size=420, x=540, color=YL, text=WHITE, fs=90, rot=-6, **kw):
    return {"type": "burst", "in": at, "out": out, "html": html, "top": top, "size": size, "x": x, "color": color, "textColor": text, "fs": fs, "rot": rot, **kw}


def cta(at, top=760, btn_at=None, **kw):
    e = {"type": "cta", "in": at, "top": top, "button": "WhatsApp saya", "fine": FINE, **kw}
    if btn_at:
        e["btnAt"] = btn_at
    return e


V = {}

# ---------------------------------------------------------------- HN01 kinetic typography
V["HN01"] = dict(
    slug="kinetic-stop-scroll-rm20", style="kinetic", voice="Fenrir", cap=False,
    tts="Say in Malaysian Malay, as a hyped, high-energy young man in a fast TikTok ad, punchy, excited and very quick",
    lines=L(
        ("Stop! Jangan scroll dulu!", "STOP! Jangan *scroll* dulu!"),
        ("Promo Coway kali ni memang padu!", "Promo Coway kali ni memang *padu!*"),
        ("Dua puluh ringgit je, dah boleh pasang!", "*RM20* je, dah boleh *pasang!*"),
        ("Ya, betul. Dua puluh ringgit. Tak tipu!", "Ya, betul. *RM20.* Tak tipu!"),
        ("Ni dia, Coway Neon. Model mampu milik!", "Ni dia, *Coway Neon.* Model *mampu milik!*"),
        ("Harga mesra poket, tapi lengkap!", "Harga mesra poket, tapi *lengkap!*"),
        ("Nak bancuh minuman? Air panas.", "Nak bancuh minuman? Air *panas.*"),
        ("Nak hilang dahaga? Air sejuk.", "Nak hilang dahaga? Air *sejuk.*"),
        ("Nak minum biasa? Suhu bilik.", "Nak minum biasa? *Suhu bilik.*"),
        ("Satu mesin, semua ada!", "Satu mesin, *semua ada!*"),
        ("Bonus! Ada free gift premium lagi!", "BONUS! Ada *free gift premium* lagi!"),
        ("Hadiah premium, percuma untuk anda!", "Hadiah premium, *percuma* untuk anda!"),
        ("Nak tahu details? WhatsApp saya sekarang!", "Nak details? *WhatsApp* saya sekarang!"),
    ),
    scenes=[(0, "k-blue"), ("@02", "k-ink"), ("@03", "k-white"), ("@04", "k-blue"), ("@05", "k-sky"), ("@06", "k-ink"),
            ("@07", "k-white"), ("@10", "k-blue"), ("@11", "k-pink"), ("@13", "k-blue")],
    els=[words("@01", "@02", 560, w("STOP!", "@01", 330, WHITE, hit=True), w("JANGAN SCROLL", "@01%45", 100, WHITE, box=True, bg="#111")),
         words("@02", "@03", 500, w("PROMO", "@02", 200, WHITE), w("COWAY", "@02%30", 200, CW), w("PADU!", "@02%65", 280, PK, hit=True)),
         words("@03", "@04", 460, w("RM20", "@03%10", 430, CW, hit=True), w("DAH BOLEH PASANG!", "@03%55", 100, WHITE, box=True, bg=CW)),
         {"type": "ticker", "in": "@03", "out": "@05", "top": 1330, "text": "PROMO RM20 DAH BOLEH PASANG", "rot": -5, "bg": "#111", "color": WHITE},
         words("@04", "@05", 520, w("YA, BETUL.", "@04", 140, WHITE), w("RM20", "@04%35", 380, WHITE, hit=True), w("TAK TIPU!", "@04%70", 120, WHITE, box=True, bg="#111")),
         img("@05", "@07", PINK, 430, 330, anim="rise", zoom=1.05),
         words("@05", "@06", 140, w("COWAY NEON", "@05", 150, INK)),
         words("@05%50", "@06", 1260, w("MAMPU MILIK!", "@05%55", 150, WHITE, box=True, bg=CW, hit=True)),
         words("@06", "@07", 1260, w("HARGA MESRA,", "@06", 110, WHITE), w("TAPI LENGKAP!", "@06%45", 150, CW, hit=True)),
         words("@07", "@08", 170, w("BANCUH MINUMAN?", "@07", 130, INK)),
         words("@08", "@09", 170, w("HILANG DAHAGA?", "@08", 130, INK)),
         words("@09", "@10", 170, w("MINUM BIASA?", "@09", 130, INK)),
         temps("@07", "@10", 420, "@07%45", "@08%45", "@09%45"),
         words("@10", "@11", 560, w("SATU MESIN,", "@10", 160, WHITE), w("SEMUA ADA!", "@10%40", 230, WHITE, hit=True)),
         words("@11", "@13", 170, w("BONUS!", "@11", 220, INK, hit=True)),
         gift("@11", "@13", "@11%50", 470, rays="rgba(255,255,255,.85)"),
         words("@12", "@13", 1150, w("FREE GIFT PREMIUM", "@12", 110, WHITE, box=True, bg=CW), w("PERCUMA!", "@12%55", 170, INK)),
         words("@13", None, 330, w("NAK DETAILS?", "@13", 150, WHITE), w("SEKARANG!", "@13%55", 220, WHITE, hit=True)),
         cta("@13", top=900, btn_at="@13%40")],
)

# ---------------------------------------------------------------- HN02 papercut
V["HN02"] = dict(
    slug="papercut-modal-kecil-rm20", style="paper", voice="Laomedeia",
    tts="Say in Malaysian Malay, as a bubbly, excited young woman in a fast, playful TikTok ad, bright and quick",
    lines=L(
        ("Siapa kata nak pasang Coway kena modal besar?", "Siapa kata pasang Coway kena *modal besar?*"),
        ("Salah! Sekarang ada promo dua puluh ringgit, dah boleh pasang!", "SALAH! Sekarang promo *RM20* dah boleh *pasang!*"),
        ("Dua puluh ringgit je tau!", "*RM20* je tau!"),
        ("Kenalkan, Coway Neon.", "Kenalkan, *Coway Neon.*"),
        ("Model mampu milik, rupa pun cantik, sesuai untuk rumah pertama.", "Model *mampu milik*, rupa pun *cantik!*"),
        ("Fungsi? Lengkap!", "Fungsi? *Lengkap!*"),
        ("Air panas untuk bancuh susu, air sejuk masa panas terik, suhu bilik untuk minum harian.",
         "*Panas* untuk susu, *sejuk* masa terik, *suhu bilik* untuk harian."),
        ("Lagi best, ada free gift premium menanti!", "Lagi best, ada *free gift premium!*"),
        ("Jangan tunggu lama-lama.", "Jangan tunggu *lama-lama.*"),
        ("WhatsApp saya sekarang untuk details lanjut!", "*WhatsApp* saya sekarang untuk *details!*"),
    ),
    scenes=[(0, "paper-cream"), ("@02", "paper-blue"), ("@04", "paper-sky"), ("@05", "paper-pink"), ("@06", "paper-cream"),
            ("@07", "paper-sky"), ("@08", "paper-pink"), ("@09", "paper-cream"), ("@10", "paper-blue")],
    els=[words("@01", "@02", 360, w("Pasang Coway", "@01", 120), w("kena modal", "@01%35", 120), w("BESAR?", "@01%65", 170, WHITE, bg=CW, hit=True)),
         words("@02", "@04", 220, w("SALAH!", "@02", 150, WHITE, bg="#ff5a3c", rot=-6, hit=True)),
         {"type": "tag", "in": "@02%35", "out": "@04", "top": 760, "pre": "PROMO", "big": "RM20", "sub": "DAH BOLEH PASANG!", "hit": True},
         words("@03", "@04", 1260, w("JE TAU!", "@03", 110, rot=4)),
         words("@04", "@05", 200, w("Kenalkan,", "@04", 100), w("Coway Neon!", "@04%30", 130, WHITE, bg=CW)),
         img("@04%30", "@05", PINK, 400, 580, anim="drop", rot=-3, float=True),
         words("@05", "@06", 200, w("MAMPU MILIK", "@05", 130, WHITE, bg=CW, hit=True), w("rupa pun cantik!", "@05%40", 100)),
         img("@05%40", "@06", LINEUP, 1000, 760, anim="rise"),
         words("@06", "@07", 640, w("Fungsi?", "@06", 130), w("LENGKAP!", "@06%45", 200, WHITE, bg=CW, hit=True)),
         words("@07", "@08", 200, w("3 SUHU", "@07", 130, WHITE, bg=CW)),
         temps("@07", "@08", 470, "@07%5", "@07%35", "@07%65"),
         gift("@08", "@09", "@08%40", 330, rays="rgba(255,255,255,.85)"),
         words("@08%40", "@09", 1080, w("FREE GIFT", "@08%45", 120, WHITE, bg=CW), w("PREMIUM", "@08%60", 120, rot=3)),
         words("@09", "@10", 620, w("Jangan tunggu", "@09", 110), w("LAMA-LAMA!", "@09%50", 150, WHITE, bg=PK, hit=True)),
         words("@10", None, 360, w("Details lanjut?", "@10", 110)),
         cta("@10", btn_at="@10%30")],
)

# ---------------------------------------------------------------- HN03 komik / pop-art
V["HN03"] = dict(
    slug="komik-3-kuasa-neon", style="comic", voice="Puck",
    tts="Say in Malaysian Malay, like an energetic cartoon superhero announcer, dramatic, excited and fast",
    lines=L(
        ("Alamak! Nak air bersih, tapi bajet ketat?", "ALAMAK! Nak air bersih, *bajet ketat?*"),
        ("Poket makin nipis, tapi famili tetap nak yang terbaik!", "Poket *nipis*, famili nak yang *terbaik!*"),
        ("Jangan risau! Coway datang selamatkan keadaan!", "Jangan risau! *Coway* datang!"),
        ("Kuasa pertama: promo dua puluh ringgit, terus boleh pasang!", "Kuasa #1: promo *RM20*, terus boleh *pasang!*"),
        ("Kuasa kedua: Coway Neon, model mampu milik!", "Kuasa #2: *Coway Neon*, model *mampu milik!*"),
        ("Kuasa ketiga: tiga suhu dalam satu mesin!", "Kuasa #3: *3 suhu* dalam satu!"),
        ("Panas! Sejuk! Suhu bilik! Semua satu tekan!", "*Panas!* *Sejuk!* *Suhu bilik!* Satu tekan!"),
        ("Dan kuasa rahsia, free gift premium!", "Kuasa rahsia: *free gift premium!*"),
        ("Nak sertai misi ni?", "Nak sertai *misi* ni?"),
        ("WhatsApp saya sekarang untuk details lanjut!", "*WhatsApp* saya sekarang!"),
    ),
    scenes=[(0, "comic-pink"), ("@02", "comic-sky"), ("@03", "comic-blue"), ("@04", "comic-white"), ("@05", "comic-blue"),
            ("@06", "comic-pink"), ("@07", "comic-sky"), ("@08", "comic-blue"), ("@09", "comic-white")],
    els=[burst("@01", "@02", "ALAMAK!", 280, size=660, color=WHITE, text=PK, fs=150, hit=True),
         words("@01%50", "@02", 1000, w("BAJET", "@01%55", 150, WHITE), w("KETAT?!", "@01%75", 200, YL, hit=True)),
         words("@02", "@03", 480, w("POKET", "@02", 170, CW), w("NIPIS!", "@02%30", 220, PK, hit=True), w("FAMILI NAK", "@02%60", 120, WHITE), w("TERBAIK!", "@02%80", 170, CW)),
         words("@03", "@04", 380, w("JANGAN RISAU!", "@03", 130, WHITE), w("COWAY", "@03%40", 300, WHITE, hit=True), w("DATANG!", "@03%65", 170, "#CEF3FF")),
         words("@04", "@05", 170, w("KUASA #1", "@04", 130, PK)),
         burst("@04%30", "@05", "RM20", 400, size=660, color=CW, fs=220, hit=True),
         words("@04%60", "@05", 1110, w("TERUS PASANG!", "@04%65", 130, CW)),
         words("@05", "@06", 150, w("KUASA #2", "@05", 130, YL)),
         img("@05%15", "@06", PINK, 430, 400, anim="spin", float=True),
         burst("@05%55", "@06", "MAMPU<br>MILIK!", 1080, size=400, x=800, fs=76, rot=12, hit=True),
         words("@06", "@07", 160, w("KUASA #3", "@06", 130, WHITE)),
         burst("@06%30", "@07", "3 SUHU<br>1 MESIN", 520, size=640, color=WHITE, text=CW, fs=104, hit=True),
         temps("@07", "@08", 330, "@07", "@07%22", "@07%44"),
         words("@07%70", "@08", 1080, w("SATU TEKAN!", "@07%75", 150, CW, hit=True)),
         words("@08", "@09", 170, w("KUASA RAHSIA!", "@08", 130, YL)),
         gift("@08", "@09", "@08%40", 420, size=600, rays="rgba(255,255,255,.6)"),
         words("@08%50", "@09", 1080, w("FREE GIFT PREMIUM!", "@08%55", 110, WHITE, hit=True)),
         words("@09", None, 380, w("SERTAI MISI?", "@09", 150, CW)),
         cta("@09%60", top=780, btn_at="@10", fineColor="#333")],
)

# ---------------------------------------------------------------- HN04 neon glow
V["HN04"] = dict(
    slug="neon-glow-bukan-lampu", style="glow", voice="Zephyr",
    tts="Say in Malaysian Malay, as a confident, trendy young woman hyping a product on TikTok, energetic, playful and quick",
    lines=L(
        ("Neon ni bukan lampu, okay!", "*Neon* ni bukan lampu, okay!"),
        ("Ni Coway Neon, penapis air yang tengah hot sekarang!", "Ni *Coway Neon*, penapis air yang tengah *hot!*"),
        ("Promo dua puluh ringgit, dah boleh pasang!", "Promo *RM20*, dah boleh *pasang!*"),
        ("Dua puluh ringgit je, dah menyala dapur awak!", "*RM20* je, dah *menyala* dapur awak!"),
        ("Model mampu milik, tapi gaya tetap premium!", "Model *mampu milik*, gaya tetap *premium!*"),
        ("Air panas, air sejuk, suhu bilik. Semua lengkap!", "Air *panas*, *sejuk*, *suhu bilik*. Semua *lengkap!*"),
        ("Siap ada free gift premium lagi!", "Siap ada *free gift premium* lagi!"),
        ("Lampu dah on, promo pun on!", "Lampu dah *on*, promo pun *on!*"),
        ("Jom, jangan tunggu lagi!", "Jom, *jangan tunggu* lagi!"),
        ("WhatsApp saya sekarang untuk details lanjut!", "*WhatsApp* saya sekarang untuk *details!*"),
    ),
    scenes=[(0, "glow-wall"), ("@02", "glow-dark"), ("@03", "glow-wall"), ("@04", "glow-dark"), ("@05", "glow-wall"),
            ("@06", "glow-dark"), ("@07", "glow-wall"), ("@08", "glow-dark"), ("@09", "glow-wall"), ("@10", "glow-dark")],
    els=[words("@01", "@02", 520, w("Neon", "@01", 280, g="#ff4f8f", hit=True), w("bukan lampu!", "@01%45", 120, g=CW)),
         words("@02", "@03", 150, w("Coway Neon", "@02", 140, g=CW)),
         img("@02%25", "@03", PINK, 400, 470, g=CW),
         words("@02%65", "@03", 1300, w("tengah hot!", "@02%70", 110, g="#ff4f8f")),
         words("@03", "@04", 400, w("PROMO", "@03", 110, g=CW, sans=True), w("RM20", "@03%20", 330, g="#ff4f8f", sans=True, hit=True), w("dah boleh pasang!", "@03%60", 110, g=CW)),
         words("@04", "@05", 560, w("RM20 je,", "@04", 130, g=CW), w("dah menyala", "@04%45", 150, g=YL, hit=True), w("dapur awak!", "@04%70", 110, g=CW)),
         words("@05", "@06", 360, w("Mampu Milik", "@05", 170, g=CW), w("gaya premium!", "@05%50", 130, g="#ff4f8f", hit=True)),
         img("@05%30", "@06", LINEUP, 1000, 900, anim="rise", g=CW),
         temps("@06", "@07", 380, "@06", "@06%22", "@06%44"),
         words("@06%70", "@07", 1150, w("Lengkap!", "@06%75", 150, g="#20b58f", hit=True)),
         gift("@07", "@08", "@07%35", 360, size=600, rays="rgba(4,164,228,.35)"),
         words("@07%40", "@08", 1060, w("Free Gift", "@07%45", 130, g="#ff4f8f"), w("PREMIUM", "@07%60", 90, g=CW, sans=True)),
         words("@08", "@09", 560, w("Lampu ON,", "@08", 150, g=YL), w("Promo ON!", "@08%50", 180, g="#ff4f8f", hit=True)),
         words("@09", "@10", 640, w("Jom!", "@09", 220, g=CW, hit=True)),
         words("@10", None, 380, w("WhatsApp", "@10", 150, g="#25D366")),
         cta("@10", btn_at="@10%30")],
)

# ---------------------------------------------------------------- HN05 UGC / POV TikTok
V["HN05"] = dict(
    slug="pov-kawan-tanya-harga", style="ugc", voice="Aoede",
    tts="Say in Malaysian Malay, as a young woman telling a funny story to friends on TikTok, lively, expressive and quick",
    lines=L(
        ("POV: Kawan tanya, pasang Coway berapa?", "POV: Kawan tanya, *pasang Coway berapa?*"),
        ("Aku jawab, promo dua puluh ringgit je, dah boleh pasang!", "Aku jawab: promo *RM20* je, dah boleh *pasang!*"),
        ("Dia terus terkejut. Serius lah?", "Dia terkejut. *Serius lah?*"),
        ("Serius! Ni Coway Neon, model mampu milik.", "Serius! *Coway Neon*, model *mampu milik.*"),
        ("Tekan je, air panas. Tekan lagi, air sejuk. Suhu bilik pun ada.", "Tekan je: *panas*. Tekan lagi: *sejuk*. *Suhu bilik* pun ada."),
        ("Semua lengkap dalam satu mesin.", "Semua *lengkap* dalam satu."),
        ("Lepas tu aku cakap, siap dapat free gift premium lagi!", "Siap dapat *free gift premium* lagi!"),
        ("Terus dia minta nombor aku.", "Terus dia minta *nombor* aku. 😂"),
        ("Nak juga? WhatsApp saya sekarang untuk details!", "Nak juga? *WhatsApp* saya sekarang!"),
    ),
    scenes=[(0, PRES_W), ("@02", PREP), ("@03", "ugc-white"), ("@04", "ugc-blue"), ("@05", POUR), ("@06", PRES_C),
            ("@07", "ugc-blue"), ("@08", "ugc-white"), ("@09", "ugc-blue")],
    els=[words("@01", "@02", 220, w("POV:", "@01", 90, box=True), w("Kawan tanya harga Coway 🤔", "@01%30", 62, box=True)),
         burst("@02%15", "@03", "RM20<br>JE!", 360, size=560, color=CW, fs=150, rot=-8, hit=True),
         words("@02%55", "@03", 1000, w("DAH BOLEH PASANG!", "@02%55", 90, WHITE)),
         words("@03", "@04", 520, w("😱", "@03", 300, hit=True), w("SERIUS LAH?", "@03%40", 130, CW)),
         words("@04", "@05", 150, w("SERIUS!", "@04", 130, WHITE)),
         img("@04%20", "@05", PINK, 430, 400, anim="slam", hit=True),
         burst("@04%55", "@05", "MAMPU<br>MILIK", 1100, size=380, x=800, color=YL, text="#111", fs=70, rot=10),
         words("@05", "@06", 200, w("TEKAN JE 👆", "@05", 80, box=True)),
         temps("@05", "@06", 420, "@05%20", "@05%45", "@05%70"),
         words("@06", "@07", 250, w("SEMUA LENGKAP ✅", "@06", 90, box=True)),
         words("@07", "@08", 170, w("SIAP ADA…", "@07", 90, WHITE)),
         gift("@07", "@08", "@07%45", 420, size=600),
         words("@07%55", "@08", 1110, w("FREE GIFT PREMIUM 🎁", "@07%60", 80, box=True)),
         words("@08", "@09", 560, w("📱", "@08", 260), w("TERUS MINTA NOMBOR 😂", "@08%40", 76, CW)),
         words("@09", None, 400, w("NAK JUGA? 👇", "@09", 110, WHITE)),
         cta("@09", btn_at="@09%35")],
)

if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        spec = {"slug": v["slug"], "voice": v["voice"], "style_tts": v["tts"], "style": v["style"], "player": "hype", "bpm": 128,
                "brand": "coway", "cap": v.get("cap", True),
                "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"]}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        n = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['style']:8s} {v['slug']:28s} {v['voice']:9s} {len(v['lines']):2d} baris, {n} perkataan (~{n / 2.9:.0f}s laju)")
