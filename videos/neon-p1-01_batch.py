"""Coway Neon "mampu milik": skrip video TikTok rujukan (kreator lain, 34 s, showroom) dibina semula dalam 3 gaya
-> videos/NE1x/{lines.json, spec.json}. NE11 motion graphic (scenes), NE12 kinetic (hype), NE13 komik (hype).

    python3 videos/neon-p1-01_batch.py
    python3 videos/build_video.py NE11 --tts --render --review out/neon-p1-01
    # NE12/NE13 guna semula vo.wav NE11 (skrip & suara sama): skrip ini salin vo.wav + segments.json
    python3 videos/build_video.py NE12 --render --review out/neon-p1-01

Harga (brand-brain/coway/products.md): RM59 dengan servis, RM54 self-service.
Promo "RM20 x 7 bulan pertama" disahkan user 25/10; ditulis sebagai rebat ikut brand-guide (bukan "RM20 sahaja").
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FEM = "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"
IMG = "../../assets/img/neon/"
NAVY, CORAL, SKY = "#0B2F6B", "#E86E5A", "#2EA7E0"
FINE = ("*Harga bulanan RM59 (dengan servis) atau RM54 (self-service). Rebat RM20 sebulan untuk 7 bulan pertama. "
        "Kuota terhad. Tertakluk pada terma &amp; promosi semasa Coway.")
BRAND = {"theme": "coway", "brand": "COWAY", "tagline": "Own Your Aesthetics, Affordably."}



def R(name, color="navy"):
    """Gambar realistik Seedream (assets/img/neon-p1-01/, lihat README.txt) sebagai latar penuh, tepi digelapkan."""
    return {"image": f"neon-p1-01/{name}.jpg", "color": color, "shade": True}


REAL = ["a_hook", "b_dapur", "c_panas", "d_5warna", "e_minimalist", "f_servis", "g_selfservice", "h_keluarga"]


def real_scenes(color, rest):
    """Baris 01-08 (separuh pertama) atas gambar realistik, kemudian latar grafik `rest`."""
    return [(0 if i == 0 else f"@{i + 1:02d}", R(n, color)) for i, n in enumerate(REAL)] + rest


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c} for i, (t, c) in enumerate(rows)]


def title(at, out, html, top=240, size=110, dark=False, **kw):
    return {"type": "title", "in": at, "out": out, "top": top, "size": size, "html": html,
            **({"color": NAVY, "shadow": False} if dark else {}), **kw}


def photo(at, out, src="pink.jpg", top=160, size=360, **kw):
    return {"type": "photo", "in": at, "out": out, "top": top, "left": (1080 - size) // 2, "w": size, "h": size, "src": IMG + src, **kw}


BLUE, PINK, INK, YEL = "#04A4E4", "#ff8fb1", "#2f3337", "#ffd23f"
BOX = {"box": True, "bg": "#111"}


def W(at, out, top, *items):
    """words: item = (txt, at, size, color, extra-dict)"""
    return {"type": "words", "in": at, "out": out, "top": top,
            "items": [{"txt": t, "at": a, "size": z, "color": c, **(x[0] if x else {})} for t, a, z, c, *x in items]}


V = {}

# ---------------------------------------------------------------- NE11 (TikTok showroom "mampu milik")
V["NE11"] = dict(slug="penapis-air-mampu-milik", voice="Aoede", style=FEM, lines=L(
    ("Nak cari penapis air yang mampu milik?", "Nak cari penapis air *mampu milik?*"),
    ("Untuk model Coway Neon ni, lengkap dengan tiga suhu.", "Coway *Neon*, lengkap *3 suhu*."),
    ("Panas, sejuk, dan suhu bilik.", "*Panas*, *sejuk*, *suhu bilik*."),
    ("Ada lima pilihan warna yang cantik.", "Ada *5 pilihan warna* yang cantik."),
    ("Dan design Coway Neon ni memang sangat minimalist untuk penapis air.", "Design *sangat minimalist*."),
    ("Coway Neon ni korang boleh dapat dengan harga bulanan lima puluh sembilan ringgit, dengan servis.",
     "Harga bulanan *RM59*, dengan servis."),
    ("Ataupun lima puluh empat ringgit, self-service.", "Atau *RM54*, self-service."),
    ("Siapa yang order sekarang lagi untung, sebab akan dapat harga special, rebat dua puluh ringgit sebulan, untuk tujuh bulan pertama.",
     "Order sekarang: *rebat RM20* sebulan, *7 bulan pertama*."),
    ("Tapi korang kena cepat, sebab kuota harga promo tak banyak tau.", "Kena *cepat*, kuota promo *tak banyak* tau."),
    ("Jadi siapa yang minat, terus tekan butang WhatsApp sekarang.", "Minat? Terus tekan *WhatsApp* sekarang.")),
  scenes=real_scenes("navy", [("@08%55", "navy"), ("@09", "navy"), ("@10", "blue")]),
  els=[{"type": "banner", "in": "@01", "out": "@02", "top": 200, "html": "NAK CARI PENAPIS AIR<br><em>MAMPU MILIK?</em>"},
       {"type": "banner", "in": "@02", "out": "@03", "top": 200, "html": "COWAY <em>NEON</em>"},
       {"type": "pill", "in": "@02%55", "out": "@03", "top": 330, "html": "✓ 3 SUHU", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "chips", "in": "@03", "out": "@04", "top": 220, "items": [
           {"text": "PANAS", "color": "#ff7a6b", "at": "@03"}, {"text": "SEJUK", "color": "#6cc2ff", "at": "@03%30"},
           {"text": "SUHU BILIK", "color": NAVY, "at": "@03%60"}]},
       {"type": "banner", "in": "@04", "out": "@05", "top": 200, "html": "<em>5</em> PILIHAN WARNA"},
       {"type": "banner", "in": "@05", "out": "@06", "top": 200, "html": "DESIGN<br><em>SANGAT MINIMALIST</em>"},
       {"type": "banner", "in": "@06", "out": "@08", "top": 200, "html": "HARGA <em>BULANAN</em>"},
       {"type": "card", "in": "@06%30", "out": "@07", "top": 1260, "icon": "tech", "title": "RM59 SEBULAN", "sub": "Dengan servis, technician datang ke rumah"},
       {"type": "card", "in": "@07", "out": "@08", "top": 1260, "icon": "box", "icbg": "#fff3cc", "iccolor": "#b07b00",
        "title": "RM54 SEBULAN", "sub": "Self-service, tukar filter sendiri"},
       {"type": "pill", "in": "@08", "out": "@08%55", "top": 260, "html": "ORDER SEKARANG LAGI UNTUNG", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "text", "in": "@08%55", "out": "@09", "top": 300, "size": 60, "weight": 800, "html": "HARGA SPECIAL"},
       title("@08%55", "@09", "REBAT<br><span style='color:var(--yellow)'>RM20</span>", top=420, size=170, hit=True),
       {"type": "pill", "in": "@08%75", "out": "@09", "top": 900, "html": "SEBULAN × 7 BULAN PERTAMA*", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "icon", "in": "@09", "out": "@10", "top": 300, "icon": "clock", "size": 260, "color": "#fff"},
       title("@09", "@10", f"KENA <span style='color:var(--yellow)'>CEPAT!</span>", top=640, size=130),
       {"type": "stamp", "in": "@09%55", "out": "@10", "top": 960, "html": "KUOTA TERHAD", "rot": -6},
       photo("@10", None, top=200, size=420),
       {"type": "cta", "in": "@10", "top": 720, "button": "WhatsApp saya", "btnAt": "@10%35",
        "ticks": ["RM59 DENGAN SERVIS*", "RM54 SELF-SERVICE*", "+ REBAT RM20 × 7 BULAN*"], "fine": FINE}])

LINES = V["NE11"]["lines"]
HYPE_SPEC = {"voice": "Aoede", "style_tts": FEM, "player": "hype", "bpm": 128, "brand": "coway", "cap": True}

# ---------------------------------------------------------------- NE12 kinetic (skrip & VO sama dengan NE11)
V["NE12"] = dict(slug="kinetic-penapis-air-mampu-milik", lines=LINES, spec={**HYPE_SPEC, "style": "kinetic"},
  scenes=real_scenes("k-ink", [("@08%50", "k-white"), ("@09", "k-pink"), ("@10", "k-blue")]),
  els=[W("@01", "@02", 220, ("NAK CARI", "@01", 120, "#fff", BOX), ("PENAPIS AIR", "@01%30", 120, "#fff", BOX),
         ("MAMPU MILIK?", "@01%60", 140, "#fff", {"box": True, "bg": BLUE, "hit": True})),
       W("@02", "@03", 200, ("COWAY NEON", "@02", 140, "#fff", BOX)),
       W("@02%50", "@03", 1180, ("3 SUHU!", "@02%60", 170, "#fff", {"box": True, "bg": BLUE, "hit": True})),
       W("@03", "@04", 200, ("LENGKAP!", "@03", 150, "#fff", BOX)),
       {"type": "temps", "in": "@03", "out": "@04", "top": 780, "items": [{"k": "hot", "at": "@03"}, {"k": "cold", "at": "@03%30"}, {"k": "room", "at": "@03%60"}]},
       W("@04", "@05", 200, ("5 PILIHAN WARNA", "@04", 110, "#fff", BOX), ("CANTIK!", "@04%45", 170, "#fff", {"box": True, "bg": BLUE, "hit": True})),
       W("@05", "@06", 200, ("DESIGN SANGAT", "@05", 110, "#fff", BOX), ("MINIMALIST!", "@05%55", 170, "#fff", {"box": True, "bg": BLUE, "hit": True})),
       W("@06", "@07", 200, ("HARGA BULANAN", "@06", 120, "#fff", BOX)),
       {"type": "tag", "in": "@06%35", "out": "@07", "top": 1080, "big": "RM59", "sub": "DENGAN SERVIS", "hit": True},
       W("@07", "@08", 200, ("ATAU", "@07", 120, "#fff", BOX)),
       {"type": "tag", "in": "@07", "out": "@08", "top": 1080, "big": "RM54", "sub": "SELF-SERVICE", "hit": True},
       W("@08", "@08%50", 220, ("ORDER SEKARANG", "@08", 110, "#fff", BOX), ("LAGI UNTUNG!", "@08%20", 160, "#fff", {"box": True, "bg": BLUE, "hit": True})),
       W("@08%50", "@09", 380, ("REBAT", "@08%50", 160, INK), ("RM20", "@08%58", 400, BLUE, {"hit": True}),
         ("SEBULAN × 7 BULAN PERTAMA*", "@08%75", 72, "#fff", {"box": True, "bg": BLUE})),
       {"type": "ticker", "in": "@08", "out": "@10", "top": 1300, "text": "REBAT RM20 × 7 BULAN PERTAMA*", "rot": -5, "bg": "#111", "color": "#fff"},
       W("@09", "@10", 380, ("KENA", "@09", 170, INK), ("CEPAT!", "@09%20", 330, BLUE, {"hit": True}),
         ("KUOTA TERHAD", "@09%55", 120, "#fff", BOX)),
       W("@10", None, 330, ("MINAT?", "@10", 170, "#fff"), ("WHATSAPP SEKARANG!", "@10%30", 110, "#fff", BOX)),
       {"type": "cta", "in": "@10", "top": 900, "button": "WhatsApp saya", "btnAt": "@10%40", "fine": FINE}])

# ---------------------------------------------------------------- NE13 komik (skrip & VO sama dengan NE11)
V["NE13"] = dict(slug="komik-penapis-air-mampu-milik", lines=LINES, spec={**HYPE_SPEC, "style": "comic"},
  scenes=real_scenes("comic-blue", [("@08%50", "comic-white"), ("@09", "comic-pink"), ("@10", "comic-blue")]),
  els=[W("@01", "@02", 200, ("NAK CARI", "@01", 140, "#fff"), ("PENAPIS AIR", "@01%25", 140, YEL)),
       {"type": "burst", "in": "@01%50", "out": "@02", "html": "MAMPU<br>MILIK?", "top": 1000, "size": 500, "x": 540, "color": "#fff",
        "textColor": PINK, "fs": 100, "rot": -6, "hit": True},
       W("@02", "@03", 170, ("COWAY NEON!", "@02", 150, BLUE)),
       {"type": "burst", "in": "@02%55", "out": "@03", "html": "3<br>SUHU!", "top": 1000, "size": 400, "x": 800, "color": YEL,
        "textColor": "#fff", "fs": 96, "rot": 12, "hit": True},
       {"type": "temps", "in": "@03", "out": "@04", "top": 780, "items": [{"k": "hot", "at": "@03"}, {"k": "cold", "at": "@03%30"}, {"k": "room", "at": "@03%60"}]},
       W("@04", "@05", 170, ("5 WARNA", "@04", 170, PINK), ("CANTIK!", "@04%40", 150, BLUE, {"hit": True})),
       W("@05", "@06", 170, ("DESIGN", "@05", 150, "#fff")),
       {"type": "burst", "in": "@05%35", "out": "@06", "html": "SANGAT<br>MINIMALIST!", "top": 1020, "size": 560, "x": 540, "color": "#fff",
        "textColor": BLUE, "fs": 84, "rot": -6, "hit": True},
       W("@06", "@07", 170, ("HARGA BULANAN", "@06", 120, YEL)),
       {"type": "tag", "in": "@06%35", "out": "@07", "top": 1080, "big": "RM59", "sub": "DENGAN SERVIS", "hit": True},
       W("@07", "@08", 170, ("ATAU...", "@07", 150, BLUE)),
       {"type": "tag", "in": "@07%20", "out": "@08", "top": 1080, "big": "RM54", "sub": "SELF-SERVICE", "hit": True},
       W("@08", "@09", 170, ("ORDER SEKARANG", "@08", 120, PINK), ("LAGI UNTUNG!", "@08%20", 150, BLUE)),
       {"type": "gift", "in": "@08%50", "out": "@09", "openAt": "@08%62", "top": 440, "size": 560, "rays": "rgba(4,164,228,.35)"},
       W("@08%62", "@09", 1060, ("REBAT RM20", "@08%65", 140, "#fff", {"box": True, "bg": BLUE, "hit": True}),
         ("× 7 BULAN PERTAMA*", "@08%78", 90, INK)),
       {"type": "burst", "in": "@09", "out": "@10", "html": "CEPAT!", "top": 300, "size": 660, "x": 540, "color": YEL,
        "textColor": "#fff", "fs": 190, "rot": -6, "hit": True},
       W("@09%50", "@10", 1050, ("KUOTA TERHAD!", "@09%55", 130, "#fff")),
       W("@10", None, 380, ("MINAT?", "@10", 170, "#fff")),
       {"type": "cta", "in": "@10%30", "top": 780, "button": "WhatsApp saya", "btnAt": "@10%50", "fine": FINE}])


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        head = v.get("spec") or {"voice": v["voice"], "style": v["style"]}
        spec = {"slug": v["slug"], **head, "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"],
                **({} if v.get("spec") else BRAND)}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        if v["lines"] is LINES and vid != "NE11":          # suara sama: guna semula VO NE11
            for f in ("vo.wav", "segments.json", "chunks.txt"):
                if (HERE / "NE11" / f).exists():
                    (d / f).write_bytes((HERE / "NE11" / f).read_bytes())
        words = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['slug']:32s} {head['voice']:6s} {len(v['lines']):2d} baris, {words} perkataan (~{words / 2.6:.0f}s)")
