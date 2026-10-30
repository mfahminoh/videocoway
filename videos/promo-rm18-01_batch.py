"""Promo "Serendah RM18" x penapis air (showroom): skrip batch 1 projek/promo-rm18-01/skrip.md
-> videos/PR01..PR10/{lines.json, spec.json}. Pemain `scenes`, latar klip Google Flow (assets/clips/promo-rm18-01_sNN.mp4).

    python3 videos/promo-rm18-01_batch.py                     # tulis lines.json + spec.json
    python3 videos/build_video.py PR01 --tts                  # VO dulu (segments.json)
    python3 videos/promo-rm18-01_batch.py                     # jalankan semula: c0/c1 klip ikut masa VO sebenar
    python3 videos/build_video.py PR01 --render --review out/promo-rm18-01

Tawaran (brief.md, disahkan user 29/10): Promosi Ulang Tahun Coway, serendah RM18 sebulan selama 7 bulan, semua model.
Jangan tulis harga penuh, tarikh tamat, peratus diskaun atau nombor telefon.
Klip: s05 hanya 0-6.5 s (hujungnya bucu atas unit), s01 lebih baik < 4 s (papan tanda di latar selepas itu).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FEM = "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"
MALE = "Say in Malaysian Malay, as a friendly and confident young man on TikTok, relaxed and fairly quick, smiling"
VOICE = {"P": ("Aoede", FEM), "L": ("Orus", MALE)}
FINE = "*Serendah RM18/bulan selama 7 bulan. Tertakluk terma &amp; syarat."
BRAND = {"theme": "coway", "brand": "COWAY"}
CORAL = "#E86E5A"
CLIP_END = {"s01": 7.9, "s02": 7.9, "s03": 7.9, "s04": 7.9, "s05": 6.5}


NBSP = "\u00a0"   # engine.js memecah kapsyen pada ruang biasa sahaja: frasa ini kekal dalam satu potongan


def capfix(c):
    """Kapsyen skrip -> kapsyen skrin: "·" jadi koma (bukan perkataan sendiri), sorotan RM18 ditutup selepas /bulan."""
    c = c.replace(" · ", ", ").replace("*RM18*/bulan", "*RM18/bulan*")
    for w in ("penapis air", "tong air"):
        c = c.replace(w, w.replace(" ", NBSP))
    return c


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": capfix(c)} for i, (t, c) in enumerate(rows)]


def banner(at, out, html, top=210):
    return {"type": "banner", "in": at, "out": out, "top": top, "html": html}


def pill(at, out, html, top=360):
    return {"type": "pill", "in": at, "out": out, "top": top, "html": html, "bg": "var(--yellow)", "color": "var(--navy)"}


def price(at, out, badge_at):
    return {"type": "price", "in": at, "out": out, "top": 470, "label": "SERENDAH", "from": "RM18", "sub": "sebulan",
            "badge": "SELAMA 7 BULAN*", "badgeAt": badge_at}


def cta(at, btn_at, top=720):
    return {"type": "cta", "in": at, "top": top, "ticks": ["SEMUA MODEL PENAPIS AIR", "SERENDAH RM18 SEBULAN*", "SELAMA 7 BULAN*"],
            "button": "WhatsApp saya", "btnAt": btn_at, "fine": FINE}


V = {}

V["PR01"] = dict(slug="tunggu-harga-turun", who="P", lines=L(
    ("Lama survey penapis air, tunggu harga turun?", "Lama *survey*?"),
    ("Sempena ulang tahun Coway, semua model penapis air serendah lapan belas ringgit sebulan.", "Promosi Ulang Tahun *Coway*"),
    ("Selama tujuh bulan.", "Serendah *RM18*/bulan · 7 bulan"),
    ("WhatsApp saya sekarang.", "WhatsApp saya sekarang")),
  scenes=[(0, "s01"), ("@02", "s03"), ("@03", "blue")],
  els=[banner("@01", "@02", "LAMA SURVEY,<br><em>TUNGGU HARGA TURUN?</em>"),
       banner("@02", "@03", "PROMOSI<br><em>ULANG TAHUN COWAY</em>"),
       pill("@02%45", "@03", "SEMUA MODEL PENAPIS AIR", top=420),
       price("@03", "@04", "@03%40"),
       cta("@04", "@04%30")])

V["PR02"] = dict(slug="rm18-itu-je", who="L", lines=L(
    ("Lapan belas ringgit sebulan. Itu je.", "*RM18* sebulan. Itu je."),
    ("Untuk penapis air Coway, semua model. Promosi ulang tahun, selama tujuh bulan.", "Semua model · 7 bulan"),
    ("Nak pilih model, WhatsApp saya.", "WhatsApp saya sekarang")),
  scenes=[(0, "s02"), ("@02", "s04"), ("@02%70", "blue")],
  els=[{"type": "title", "in": "@01", "out": "@02", "top": 300, "size": 230, "html": "RM18"},
       {"type": "text", "in": "@01%35", "out": "@02", "top": 560, "html": "sebulan. <b>Itu je.</b>", "size": 80, "weight": 800},
       banner("@02", "@02%70", "PENAPIS AIR COWAY<br><em>SEMUA MODEL</em>"),
       pill("@02%30", "@02%70", "PROMOSI ULANG TAHUN · 7 BULAN*", top=420),
       price("@02%70", "@03", "@02%80"),
       cta("@03", "@03%40")])

V["PR03"] = dict(slug="coway-mahal-bulan-ni-tak", who="P", lines=L(
    ("Coway mahal? Bulan ni, tak.", "*Coway* mahal?"),
    ("Promosi ulang tahun Coway, semua model penapis air serendah lapan belas ringgit sebulan.", "Semua model penapis air"),
    ("Selama tujuh bulan. WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s01"), ("@02", "s05"), ("@02%65", "blue")],
  els=[{"type": "title", "in": "@01", "out": "@02", "top": 420, "size": 150, "html": "COWAY<br>MAHAL?"},
       {"type": "stamp", "in": "@01%55", "out": "@02", "top": 900, "html": "BULAN NI, TAK!", "color": "#1faa59", "rot": -8},
       banner("@02", "@02%65", "PROMOSI<br><em>ULANG TAHUN COWAY</em>"),
       price("@02%65", "@03%45", "@03"),
       cta("@03%45", "@03%65")])

V["PR04"] = dict(slug="tur-showroom", who="L", lines=L(
    ("Jom tengok penapis air Coway dalam showroom.", "Jom ke *showroom*"),
    ("Yang kompak, yang tangki besar, semua ada.", "Pilih ikut dapur awak"),
    ("Promosi ulang tahun, semua model serendah lapan belas ringgit sebulan, selama tujuh bulan.", "Serendah *RM18*/bulan · 7 bulan"),
    ("Pilih yang awak suka, WhatsApp saya.", "WhatsApp saya sekarang")),
  scenes=[(0, "s01"), ("@02", "s03"), ("@02%50", "s04"), ("@03", "blue")],
  els=[banner("@01", "@02", "JOM KE<br><em>SHOWROOM COWAY</em>"),
       pill("@02", "@02%50", "YANG KOMPAK", top=300),
       pill("@02%50", "@03", "YANG TANGKI BESAR", top=300),
       banner("@03", "@03%40", "PROMOSI<br><em>ULANG TAHUN</em>"),
       price("@03%40", "@04", "@03%80"),
       cta("@04", "@04%35")])

V["PR05"] = dict(slug="bukan-selalu-ada", who="P", lines=L(
    ("Promosi macam ni bukan selalu ada.", "Bukan *selalu* ada"),
    ("Sempena ulang tahun Coway, semua model penapis air serendah lapan belas ringgit sebulan.", "Promosi Ulang Tahun *Coway*"),
    ("Selama tujuh bulan. Jangan tunggu, WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s02"), ("@02", "s04"), ("@02%65", "blue")],
  els=[banner("@01", "@02", "PROMOSI MACAM NI<br><em>BUKAN SELALU ADA</em>"),
       banner("@02", "@02%65", "PROMOSI<br><em>ULANG TAHUN COWAY</em>"),
       price("@02%65", "@03%40", "@03"),
       cta("@03%40", "@03%65")])

V["PR06"] = dict(slug="enam-puluh-sen-sehari", who="L", lines=L(
    ("Enam puluh sen sehari, untuk air bersih di rumah.", "*60 sen* sehari"),
    ("Itulah promosi ulang tahun Coway. Semua model penapis air serendah lapan belas ringgit sebulan.", "RM18 ÷ 30 hari"),
    ("Selama tujuh bulan. WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s01"), ("@02", "s05"), ("@02%60", "navy"), ("@03%40", "blue")],
  els=[{"type": "title", "in": "@01", "out": "@02", "top": 300, "size": 90, "html": "AIR BERSIH DI RUMAH"},
       {"type": "counter", "in": "@01%15", "out": "@02", "top": 460, "from": 0, "to": 60, "suffix": " SEN", "dur": 0.9, "size": 200},
       {"type": "text", "in": "@01%55", "out": "@02", "top": 720, "html": "sehari", "size": 80, "weight": 800},
       banner("@02", "@02%60", "PROMOSI<br><em>ULANG TAHUN COWAY</em>"),
       {"type": "text", "in": "@02%60", "out": "@03%40", "top": 330, "html": "SERENDAH", "size": 60, "weight": 800},
       {"type": "title", "in": "@02%60", "out": "@03%40", "top": 420, "size": 200, "html": "RM18"},
       {"type": "text", "in": "@02%75", "out": "@03%40", "top": 680, "html": "÷ 30 hari = <b>60 sen sehari</b>", "size": 70, "weight": 700},
       pill("@03", "@03%40", "SELAMA 7 BULAN*", top=860),
       cta("@03%40", "@03%65")])

V["PR07"] = dict(slug="customer-terkejut", who="P", lines=L(
    ("Customer saya semalam terkejut tengok harga ni.", "Customer saya *terkejut*"),
    ("Penapis air Coway, semua model, serendah lapan belas ringgit sebulan.", "Semua model"),
    ("Promosi ulang tahun, selama tujuh bulan. WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s02"), ("@02", "s03"), ("@02%60", "blue")],
  els=[{"type": "chat", "in": "@01", "out": "@02", "top": 330, "items": [
           {"side": "L", "text": "Betul ke RM18 je sebulan?? 😳", "at": "@01%20"},
           {"side": "R", "text": "Betul, promosi ulang tahun Coway 😊", "at": "@01%65"}]},
       banner("@02", "@02%60", "PENAPIS AIR COWAY<br><em>SEMUA MODEL</em>"),
       price("@02%60", "@03%50", "@03%10"),
       cta("@03%50", "@03%70")])

V["PR08"] = dict(slug="dapur-kecil-keluarga-besar", who="L", lines=L(
    ("Dapur kecil, atau keluarga besar?", "Dapur kecil? Keluarga besar?"),
    ("Ada model Coway untuk setiap rumah.", "Ada untuk *setiap* rumah"),
    ("Promosi ulang tahun, semua model serendah lapan belas ringgit sebulan, selama tujuh bulan.", "Serendah *RM18*/bulan · 7 bulan"),
    ("WhatsApp saya sekarang.", "WhatsApp saya sekarang")),
  scenes=[(0, "s01"), ("@02", "s03"), ("@02%55", "s05"), ("@03", "blue")],
  els=[{"type": "chips", "in": "@01", "out": "@02", "top": 330, "items": [
           {"text": "DAPUR KECIL?", "color": "#6cc2ff", "at": "@01"},
           {"text": "KELUARGA BESAR?", "color": "#ffd23f", "at": "@01%50"}]},
       banner("@02", "@03", "ADA MODEL UNTUK<br><em>SETIAP RUMAH</em>"),
       banner("@03", "@03%35", "PROMOSI<br><em>ULANG TAHUN</em>"),
       price("@03%35", "@04", "@03%80"),
       cta("@04", "@04%30")])

V["PR09"] = dict(slug="orang-berduit-je", who="P", lines=L(
    ("Ingat Coway untuk orang berduit je?", "Untuk orang *berduit* je?"),
    ("Sekarang, semua model penapis air serendah lapan belas ringgit sebulan.", "Semua model penapis air"),
    ("Promosi ulang tahun Coway, selama tujuh bulan. WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s02"), ("@02", "s05"), ("@02%55", "blue")],
  els=[{"type": "title", "in": "@01", "out": "@02", "top": 380, "size": 120, "html": "COWAY UNTUK<br>ORANG BERDUIT JE?"},
       {"type": "stamp", "in": "@01e-0.3", "out": "@02", "top": 900, "html": "MITOS!", "color": CORAL, "rot": -8},
       banner("@02", "@02%55", "SEMUA MODEL<br><em>PENAPIS AIR</em>"),
       price("@02%55", "@03%50", "@03%15"),
       cta("@03%50", "@03%70")])

V["PR10"] = dict(slug="tong-air-botol", who="L", lines=L(
    ("Masih angkut tong air botol tiap minggu?", "Masih angkut *tong air*?"),
    ("Promosi ulang tahun Coway, semua model penapis air serendah lapan belas ringgit sebulan.", "Promosi Ulang Tahun *Coway*"),
    ("Selama tujuh bulan. WhatsApp saya sekarang.", "Serendah *RM18*/bulan · 7 bulan")),
  scenes=[(0, "s01"), ("@02", "s04"), ("@02%65", "blue")],
  els=[banner("@01", "@02", "MASIH ANGKUT<br><em>TONG AIR BOTOL?</em>"),
       {"type": "bottles", "in": "@01%30", "out": "@02", "top": 560, "n": 4, "dur": 1.2, "label": "tiap minggu"},
       banner("@02", "@02%65", "PROMOSI<br><em>ULANG TAHUN COWAY</em>"),
       price("@02%65", "@03%40", "@03"),
       cta("@03%40", "@03%65")])


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
