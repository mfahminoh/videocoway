"""Coway Neon "mampu milik" (NE11): skrip video TikTok rujukan (kreator lain, 34 s, showroom) ditulis semula
sebagai motion graphic dengan gambar rasmi Neon -> videos/NE11/{lines.json, spec.json}.

    python3 videos/neon-p1-01_batch.py
    python3 videos/build_video.py NE11 --tts --render --review out/neon-p1-01

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

PODIUM = {"image": "neon/podium5.jpg", "color": "pastel", "top": 420, "h": 1080, "mask": True}
PINKBG = {"image": "neon/pink.jpg", "color": "pink", "top": 380, "h": 1080}
POUR = {"clip": "press_pour", "c0": 3.0, "c1": 6.6}           # tekan butang, air mengalir


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c} for i, (t, c) in enumerate(rows)]


def title(at, out, html, top=240, size=110, dark=False, **kw):
    return {"type": "title", "in": at, "out": out, "top": top, "size": size, "html": html,
            **({"color": NAVY, "shadow": False} if dark else {}), **kw}


def photo(at, out, src="pink.jpg", top=160, size=360, **kw):
    return {"type": "photo", "in": at, "out": out, "top": top, "left": (1080 - size) // 2, "w": size, "h": size, "src": IMG + src, **kw}


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
  scenes=[(0, PODIUM), ("@02", "pastel"), ("@04", "pastel"), ("@05", PINKBG), ("@06", "blue"), ("@08", POUR),
          ("@08%55", "navy"), ("@09", "navy"), ("@10", "blue")],
  els=[title("@01", "@02", "NAK CARI<br>PENAPIS AIR", top=170, size=96, dark=True),
       {"type": "pill", "in": "@01%45", "out": "@02", "top": 410, "html": "MAMPU MILIK?", "bg": "var(--yellow)", "color": "var(--navy)"},
       title("@02", "@04", f"COWAY <span style='color:{CORAL}'>NEON</span>", top=200, size=120, dark=True),
       photo("@02", "@04", top=380, size=500),
       {"type": "pill", "in": "@02%55", "out": "@03", "top": 950, "html": "✓ 3 SUHU", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "chips", "in": "@03", "out": "@04", "top": 950, "items": [
           {"text": "PANAS", "color": "#ff7a6b", "at": "@03"}, {"text": "SEJUK", "color": "#6cc2ff", "at": "@03%30"},
           {"text": "SUHU BILIK", "color": NAVY, "at": "@03%60"}]},
       title("@04", "@05", f"<span style='color:{CORAL}'>5</span> PILIHAN WARNA", top=220, size=100, dark=True),
       {"type": "lineup", "in": "@04", "out": "@05", "keys": [
           {"at": "@04", "unit": "all", "zoom": 1}, {"at": "@04%25", "unit": "pink", "zoom": 2.1},
           {"at": "@04%40", "unit": "mint", "zoom": 2.1}, {"at": "@04%55", "unit": "ciel", "zoom": 2.1},
           {"at": "@04%70", "unit": "gray", "zoom": 2.1}, {"at": "@04%85", "unit": "white", "zoom": 2.1},
           {"at": "@04e", "unit": "all", "zoom": 1}]},
       title("@05", "@06", "MINIMALIST", top=220, size=120, dark=True),
       {"type": "text", "in": "@05%30", "out": "@06", "top": 380, "html": "cantik di mana-mana dapur", "color": NAVY},
       title("@06", "@08", "HARGA BULANAN", top=230, size=90),
       photo("@06", "@08", src="mint.jpg", top=400, size=380),
       {"type": "card", "in": "@06%30", "out": "@08", "top": 840, "icon": "tech", "title": "RM59 SEBULAN", "sub": "Dengan servis, technician datang ke rumah"},
       {"type": "card", "in": "@07", "out": "@08", "top": 1080, "icon": "box", "icbg": "#fff3cc", "iccolor": "#b07b00",
        "title": "RM54 SEBULAN", "sub": "Self-service, tukar filter sendiri"},
       {"type": "pill", "in": "@08", "out": "@08%55", "top": 300, "html": "ORDER SEKARANG LAGI UNTUNG", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "text", "in": "@08%55", "out": "@09", "top": 300, "size": 60, "weight": 800, "html": "HARGA SPECIAL"},
       title("@08%55", "@09", "REBAT<br><span style='color:var(--yellow)'>RM20</span>", top=420, size=170, hit=True),
       {"type": "pill", "in": "@08%75", "out": "@09", "top": 900, "html": "SEBULAN × 7 BULAN PERTAMA*", "bg": "var(--yellow)", "color": "var(--navy)"},
       {"type": "icon", "in": "@09", "out": "@10", "top": 300, "icon": "clock", "size": 260, "color": "#fff"},
       title("@09", "@10", f"KENA <span style='color:var(--yellow)'>CEPAT!</span>", top=640, size=130),
       {"type": "stamp", "in": "@09%55", "out": "@10", "top": 960, "html": "KUOTA TERHAD", "rot": -6},
       photo("@10", None, top=200, size=420),
       {"type": "cta", "in": "@10", "top": 720, "button": "WhatsApp saya", "btnAt": "@10%35",
        "ticks": ["RM59 DENGAN SERVIS*", "RM54 SELF-SERVICE*", "+ REBAT RM20 × 7 BULAN*"], "fine": FINE}])


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        spec = {"slug": v["slug"], "voice": v["voice"], "style": v["style"],
                "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"], **BRAND}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['slug']:32s} {v['voice']:6s} {len(v['lines']):2d} baris, {words} perkataan (~{words / 2.6:.0f}s)")
