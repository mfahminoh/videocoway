"""BOFU penapis air x kempen RM20 sebulan: skrip batch 1 projek/bofu-rm20-01/skrip.md (v2, copy user)
-> videos/BF01..BF05/{lines.json, spec.json}. Pemain `scenes`, latar klip showroom Google Flow (assets/clips/promo-rm18-01_sNN.mp4).

    python3 videos/bofu-rm20-01_batch.py                      # tulis lines.json + spec.json
    python3 videos/build_video.py BF01 --tts                  # VO dulu (segments.json)
    python3 videos/bofu-rm20-01_batch.py                      # jalankan semula: c0/c1 klip ikut masa VO sebenar
    python3 videos/build_video.py BF01 --render --review out/bofu-rm20-01

Teks di SATU tempat sahaja, hampir tengah (permintaan user 3 Nov): kapsyen VO pada capTop, tiada banner atas,
tiada bar kapsyen bawah, tiada brand tag. Semua teks dalam jalur y 560-1300, jadi kekal nampak bila Facebook Feed
memotong 9:16 kepada 4:5 (1080x1350 = y 285-1635).
Tawaran (brief.md): serendah RM20 sebulan, hantar & pasang PERCUMA seluruh Malaysia, free gift premium 5 terawal.
Jangan sebut jenis hadiah, model, tempoh atau negeri sehingga disahkan.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FEM = "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"
MALE = "Say in Malaysian Malay, as a friendly and confident young man on TikTok, relaxed and fairly quick, smiling"
VOICE = {"P": ("Aoede", FEM), "L": ("Orus", MALE)}
FINE = "*Serendah RM20/bulan. Free gift untuk 5 pelanggan terawal. Tertakluk terma &amp; syarat."
BRAND = {"theme": "coway", "capTop": 860}
CLIP_END = {"s01": 7.9, "s02": 7.9, "s03": 7.9, "s04": 7.9, "s05": 6.5}
NBSP = " "   # engine.js memecah kapsyen pada ruang biasa sahaja: frasa ini kekal dalam satu potongan

# baris tawaran (sama untuk semua video): VO + kapsyen, satu frasa satu potongan
OFFER_VO = "Serendah dua puluh ringgit sebulan. Hantar dan pasang percuma, seluruh Malaysia. Free gift premium untuk lima pelanggan terawal."
OFFER_CAP = " ".join("*" + p.replace(" ", NBSP) + "*" for p in ("Serendah RM20/bulan", "Hantar & pasang PERCUMA", "seluruh Malaysia", "Free gift premium", "5 pelanggan terawal"))


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c} for i, (t, c) in enumerate(rows)]


def icon(at, out, name, top=560, size=230):
    return {"type": "icon", "in": at, "out": out, "icon": name, "top": top, "size": size, "color": "#ffffff"}


def offer_icons(line="@03"):
    """Ikon tanpa teks di atas kapsyen semasa baris tawaran: harga, penghantaran, hadiah."""
    return [icon(line, f"{line}%33", "money"), icon(f"{line}%33", f"{line}%72", "truck"), icon(f"{line}%72", f"{line}e", "gift")]


def cta(at):
    return {"type": "cta", "in": at, "top": 660, "ticks": ["SERENDAH RM20 SEBULAN*", "HANTAR &amp; PASANG PERCUMA", "FREE GIFT 5 TERAWAL*"],
            "button": "WhatsApp saya", "btnAt": at, "fine": FINE}


V = {}

V["BF01"] = dict(slug="dah-lama-survey-ini-masanya", who="P", lines=L(
    ("Dah lama survey penapis air Coway, tapi asyik tangguh nak pasang?", "Dah lama *survey*? Asyik tangguh nak pasang?"),
    ("Haa, mungkin ini offer yang awak tunggu-tunggu!", "Ini offer yang awak *tunggu-tunggu*!"),
    (OFFER_VO, OFFER_CAP),
    ("Dah lama fikir, jangan terlepas peluang ni pula. WhatsApp saya sekarang!", "Jangan *terlepas*! WhatsApp saya sekarang")),
  scenes=[(0, "s01"), ("@02", "s03"), ("@03", "blue")],
  els=[*offer_icons(), cta("@04e+0.3")])

V["BF02"] = dict(slug="siapa-cepat-dia-dapat", who="L", lines=L(
    ("Eh! Ada hadiah untuk lima orang terawal sahaja!", "Eh! Hadiah untuk *5 orang* terawal je!"),
    ("Kalau tengah survey penapis air Coway, jangan scroll dulu.", "Tengah survey? Jangan *scroll* dulu!"),
    (OFFER_VO, OFFER_CAP),
    ("Bukan selalu ada peluang macam ni tau! WhatsApp saya sekarang.", "Bukan *selalu* ada! WhatsApp saya sekarang")),
  scenes=[(0, "blue"), ("@02", "s02"), ("@03", "blue")],
  els=[icon(0, "@02", "gift", size=260), *offer_icons(), cta("@04e+0.3")])

V["BF03"] = dict(slug="tak-perlu-pening-caj-pasang", who="P", lines=L(
    ("Nak pasang Coway, tapi takut kena macam-macam caj tambahan?", "Takut kena *caj tambahan*?"),
    ("Jangan risau, tengok tawaran ni.", "Jangan risau, tengok *tawaran* ni"),
    (OFFER_VO, OFFER_CAP),
    ("Duduk jauh pun jangan risau. WhatsApp saya, saya bantu explain sampai faham!", "Duduk *jauh* pun jangan risau. WhatsApp saya")),
  scenes=[(0, "s01"), ("@02", "s04"), ("@03", "blue")],
  els=[*offer_icons(), cta("@04e+0.3")])

V["BF04"] = dict(slug="asyik-tengok-bila-nak-pasang", who="L", lines=L(
    ("Jujur sikit, berapa lama dah simpan gambar penapis air Coway dalam phone?", "Berapa lama dah simpan gambar dalam *phone*?"),
    ("Tengok punya tengok, survey punya survey, tapi belum pasang lagi!", "Survey punya survey, tapi *belum pasang* lagi!"),
    ("Sekarang, " + OFFER_VO[0].lower() + OFFER_VO[1:], OFFER_CAP),
    ("Jom WhatsApp saya sekarang, kita borak dulu!", "Jom *WhatsApp* saya, kita borak dulu!")),
  scenes=[(0, "s02"), ("@02", "s01"), ("@03", "blue")],
  els=[*offer_icons(), cta("@04e+0.3")])

V["BF05"] = dict(slug="rm20-je-sebulan", who="P", lines=L(
    ("Dua puluh ringgit sebulan? Ya, awak tak salah baca!", "*RM20* sebulan?! Ya, awak tak salah baca!"),
    ("Kalau dah lama teringin nak pasang penapis air Coway, ini masanya.", "Dah lama teringin? Ini *masanya*"),
    (OFFER_VO, OFFER_CAP),
    ("Tiga tawaran dalam satu kempen! WhatsApp saya sekarang.", "*3 tawaran* dalam 1 kempen! WhatsApp saya")),
  scenes=[(0, "s05"), ("@02", "s03"), ("@03", "blue")],
  els=[*offer_icons(), cta("@04e+0.3")])


def at_time(at, seg):
    """`0`, `"@02"`, `"@02%40"`, `"@02e"` -> saat VO (hanya bentuk yang dipakai dalam fail ini)."""
    if not isinstance(at, str):
        return float(at)
    lid, _, pct = at[1:].partition("%")
    end = lid.endswith("e")
    s = seg[lid.rstrip("e")]
    if end:
        return s["b"]
    return s["a"] + (s["b"] - s["a"]) * (float(pct) / 100 if pct else 0)


def scenes(vid, rows):
    """Klip pada kelajuan 1x ikut masa VO sebenar (segments.json); sebelum --tts guna anggaran 3 s."""
    segf = HERE / vid / "segments.json"
    seg = {s["id"]: s for s in json.loads(segf.read_text())} if segf.exists() else None
    out = []
    for i, (at, bg) in enumerate(rows):
        if bg in CLIP_END:
            dur = 3.0
            if seg and i + 1 < len(rows):
                dur = at_time(rows[i + 1][0], seg) - at_time(at, seg)
            c1 = round(min(CLIP_END[bg], max(dur, 0.6)), 2)
            if dur > 0 and c1 / dur < 0.55:                 # babak terlalu panjang untuk klip: perlahankan setakat had
                c1 = round(min(CLIP_END[bg], dur * 0.55), 2)
            bg = {"clip": f"promo-rm18-01_{bg}", "c0": 0.0, "c1": c1}
        out.append({"at": at, "bg": bg})
    return out


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        voice, style = VOICE[v["who"]]
        spec = {"slug": v["slug"], "voice": voice, "style": style, "scenes": scenes(vid, v["scenes"]), "els": v["els"], **BRAND}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['slug']:28s} {voice:6s} {len(v['lines'])} baris, {words} perkataan (~{words / 2.6:.0f}s)")
