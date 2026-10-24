"""Batch 10 video Coway Neon (NE01-NE10): skrip + storyboard -> videos/NExx/{lines.json, spec.json}.

    python videos/neon_batch.py            # tulis semua fail
    python videos/build_video.py NE03 --tts --render

Rujukan: R02-R05 (kreator TikTok, ditulis semula), R06 (thread RO vs mineral), aset klip & gambar Neon anda.
Harga (disahkan pengguna 29/9): asal RM104/bulan, promosi RM54/bulan (jangan sebut %), + rebat ulang tahun Coway RM20 x 7 bulan.
Fakta lain yang perlu disahkan: tangki 1L/1.5L + direct flow (R05),
filter self-service setiap 8 bulan (R02/R03), dakwaan Nanotrap (laman Coway Neon).
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FEM = "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"
MALE = "Say in Malaysian Malay, as a friendly and confident young man on TikTok, relaxed and fairly quick, smiling"
IMG = "../../assets/img/neon/"
NAVY, CORAL, SKY = "#0B2F6B", "#E86E5A", "#2EA7E0"
FINE = "*Harga asal RM104/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway."


def L(*rows):
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c} for i, (t, c) in enumerate(rows)]


def title(at, out, html, top=240, size=110, dark=False, **kw):
    return {"type": "title", "in": at, "out": out, "top": top, "size": size, "html": html,
            **({"color": NAVY, "shadow": False} if dark else {}), **kw}


def price(at, out, strike=None, to_at=None, badge_at=None, top=520, label="HARGA ASAL", frm="RM104", to="RM54"):
    """HARGA ASAL RM104 (dipangkah) -> RM54 -> lencana rebat ulang tahun."""
    e = {"type": "price", "in": at, "out": out, "top": top, "label": label, "from": frm}
    if badge_at:
        e.update(badge="+ REBAT ULANG TAHUN RM20 × 7 BULAN", badgeAt=badge_at)
    if strike:
        e.update(strikeAt=strike, to=to, toAt=to_at)
    return e


def photo(at, out, src="pink.jpg", top=160, size=360, **kw):
    return {"type": "photo", "in": at, "out": out, "top": top, "left": (1080 - size) // 2, "w": size, "h": size, "src": IMG + src, **kw}


def cta(at, ticks, btn="WhatsApp saya", fine=FINE, top=720, btn_at=None):
    e = {"type": "cta", "in": at, "top": top, "ticks": ticks, "button": btn, "fine": fine}
    if btn_at:
        e["btnAt"] = btn_at
    return e


def lineup(at, out, keys):
    return {"type": "lineup", "in": at, "out": out, "keys": [{"at": a, "unit": u, "zoom": 1 if u == "all" else 2.1} for a, u in keys]}


def chips(at, out, items, top=280):
    col = {"PANAS": "#ff7a6b", "SEJUK": "#6cc2ff", "SUHU BILIK": "#e9eef5"}
    return {"type": "chips", "in": at, "out": out, "top": top, "items": [{"text": t, "color": col.get(t, "#fff"), "at": a} for t, a in items]}


def pill(at, out, html, top=260, bg="var(--yellow)", color="var(--navy)"):
    return {"type": "pill", "in": at, "out": out, "top": top, "html": html, "bg": bg, "color": color}


PODIUM = {"image": "neon/podium5.jpg", "color": "pastel", "top": 420, "h": 1080, "mask": True}
PINKBG = {"image": "neon/pink.jpg", "color": "pink", "top": 380, "h": 1080}
MINTBG = {"image": "neon/mint.jpg", "color": "mint", "top": 380, "h": 1080}
PRES_C = {"clip": "presenter", "c0": 6.4, "c1": 9.6}          # tangan tunjuk produk (tiada muka)
PRES_W = {"clip": "presenter", "c0": 0.0, "c1": 3.0}          # presenter lelaki (bercakap)
POUR = {"clip": "press_pour", "c0": 3.0, "c1": 6.6}           # tekan butang, air mengalir ke botol
PREP = {"clip": "press_pour", "c0": 0.0, "c1": 3.0}           # tangan sediakan botol
BUSY = {"clip": "bottles_busy", "c0": 0.0, "c1": 3.0}         # ibu bapa sibuk dengan botol
COT = {"clip": "bottle_to_baby", "c0": 7.2, "c1": 10.0}       # bawa botol ke katil bayi

V = {}

# ---------------------------------------------------------------- NE01 (R04)
V["NE01"] = dict(slug="bajet-kecil-tak-boleh-cantik", voice="Aoede", style=FEM, lines=L(
    ("Siapa kata bajet kecil tak boleh dapat penapis air yang cantik?", "Siapa kata bajet kecil tak boleh *cantik?*"),
    ("Kenalkan, Coway Neon.", "Kenalkan, *Coway Neon*."),
    ("Ada lima warna.", "Ada *5 warna*."),
    ("Peach pink, mint green, ciel blue,", "*Peach Pink*, *Mint Green*, *Ciel Blue*,"),
    ("pebble gray, dan porcelain white.", "*Pebble Gray* & *Porcelain White*."),
    ("Saiz kompak, ngam untuk dapur kecil.", "Saiz *kompak*, ngam dapur kecil."),
    ("Panas, sejuk, suhu bilik, semua ada.", "*Panas*, *sejuk*, *suhu bilik*, semua ada."),
    ("Kos sehari? Tak sampai dua ringgit.", "Kos sehari? *Bawah RM2.*"),
    ("Harga asal seratus empat ringgit, promosi sekarang lima puluh empat ringgit je.", "Harga asal *RM104*, promosi *RM54* je."),
    ("Tambah lagi rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan.", "+ Rebat ulang tahun *RM20 × 7 bulan*."),
    ("Dapur cantik, air pun bersih.", "Dapur *cantik*, air pun *bersih*."),
    ("WhatsApp saya, saya uruskan sampai siap pasang.", "*WhatsApp* saya, saya uruskan sampai *siap pasang*.")),
  scenes=[(0, "pastel"), ("@02", PODIUM), ("@03", "pastel"), ("@06", PRES_C), ("@07", POUR), ("@08", "navy"),
          ("@09", "blue"), ("@11", PINKBG), ("@12", "blue")],
  els=[title("@01", "@02", "BAJET KECIL", top=560, size=130, dark=True),
       title("@01%45", "@02", "= TAK CANTIK?", top=720, size=120, dark=True, color=CORAL),
       {"type": "stamp", "in": "@01e-0.2", "out": "@02", "top": 960, "html": "SALAH!"},
       title("@02", "@03", f"COWAY <span style='color:{CORAL}'>NEON</span>", size=120, dark=True),
       title("@03", "@06", f"<span style='color:{CORAL}'>5</span> WARNA", size=120, dark=True),
       lineup("@03", "@06", [("@03", "all"), ("@04", "pink"), ("@04%36", "mint"), ("@04%70", "ciel"), ("@05", "gray"), ("@05%45", "white"), ("@05e", "all")]),
       {"type": "reason", "in": "@06", "out": "@07", "top": 250, "num": "✓", "title": "KOMPAK", "sub": "ngam untuk dapur kecil"},
       chips("@07", "@08", [("PANAS", "@07"), ("SEJUK", "@07%25"), ("SUHU BILIK", "@07%50")]),
       title("@08", "@09", "KOS SEHARI", top=520, size=80),
       {"type": "counter", "in": "@08%40", "out": "@09", "top": 660, "from": 0, "to": 1.8, "prefix": "RM", "decimals": 2, "dur": .8},
       {"type": "text", "in": "@08%60", "out": "@09", "top": 940, "html": "RM54 sebulan ÷ 30 hari"},
       photo("@09", "@11"),
       price("@09", "@11", strike="@09%45", to_at="@09%60", badge_at="@10"),
       title("@11", "@12", f"DAPUR <span style='color:{CORAL}'>CANTIK</span><br>AIR <span style='color:{SKY}'>BERSIH</span>", top=170, size=96, dark=True),
       photo("@12", None, top=200, size=420),
       cta("@12", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"], btn_at="@12%20")])

# ---------------------------------------------------------------- NE02 (R05)
V["NE02"] = dict(slug="baru-kahwin-rumah-pertama", voice="Aoede", style=FEM, lines=L(
    ("Baru kahwin, baru nak susun rumah pertama?", "*Baru kahwin?* Baru nak susun rumah pertama?"),
    ("Ini penapis air yang saya selalu cadangkan.", "Ini yang saya selalu *cadangkan*."),
    ("Namanya, Coway Neon.", "Namanya, *Coway Neon*."),
    ("Panas, sejuk, dan suhu bilik, dalam satu mesin.", "*Panas*, *sejuk* & *suhu bilik*, satu mesin."),
    ("Tangki air panas satu liter, air sejuk satu perpuluhan lima liter.", "Panas *1L*, sejuk *1.5L*."),
    ("Air suhu bilik terus mengalir, tak payah tunggu.", "Suhu bilik *terus mengalir*."),
    ("Cukup untuk berdua, sampai anak pertama.", "Cukup untuk *berdua*, sampai *anak pertama*."),
    ("Saiz kompak, cantik di dapur rumah sewa.", "Saiz *kompak*, cantik di dapur."),
    ("Pilih warna ikut tema rumah, ada lima.", "Pilih warna ikut tema, ada *5*."),
    ("Harga asal seratus empat ringgit, promosi lima puluh empat ringgit sebulan,", "Harga asal *RM104*, promosi *RM54*,"),
    ("Dan tambah lagi rebat ulang tahun, dua puluh ringgit, selama tujuh bulan.", "+ rebat ulang tahun Coway *RM20 × 7 bulan*."),
    ("WhatsApp saya, penghantaran dan pemasangan percuma.", "*WhatsApp* saya, pemasangan *percuma*.")),
  scenes=[(0, "pastel"), ("@03", PODIUM), ("@04", {"clip": "press_pour", "c0": 3.0, "c1": 5.3}), ("@05", "navy"), ("@07", COT), ("@08", PRES_C), ("@09", "pastel"),
          ("@10", "blue"), ("@12", "blue")],
  els=[{"type": "icon", "in": "@01", "out": "@03", "top": 420, "icon": "home", "color": CORAL, "size": 240},
       title("@01", "@03", "BARU KAHWIN?", top=720, size=118, dark=True),
       pill("@01%50", "@03", "RUMAH PERTAMA", top=900),
       title("@03", "@04", f"COWAY <span style='color:{CORAL}'>NEON</span>", size=120, dark=True),
       chips("@04", "@05", [("PANAS", "@04"), ("SEJUK", "@04%25"), ("SUHU BILIK", "@04%55")]),
       title("@05", "@07", "KAPASITI", top=250, size=90),
       {"type": "grid", "in": "@05", "out": "@07", "top": 440, "items": [
           {"big": "1L", "small": "AIR PANAS", "color": "#ff7a6b", "at": "@05"},
           {"big": "1.5L", "small": "AIR SEJUK", "color": "#6cc2ff", "at": "@05%50"},
           {"big": "∞", "small": "SUHU BILIK · TERUS", "color": "#e9eef5", "at": "@06"}]},
       pill("@07", "@08", "BERDUA → BERTIGA 👶", top=270),
       {"type": "reason", "in": "@08", "out": "@09", "top": 250, "num": "✓", "title": "KOMPAK", "sub": "cantik di dapur rumah sewa"},
       title("@09", "@10", f"<span style='color:{CORAL}'>5</span> WARNA", size=120, dark=True),
       lineup("@09", "@10", [("@09", "all"), ("@09%35", "pink"), ("@09%70", "mint"), ("@09e", "all")]),
       photo("@10", "@12", src="mint.jpg"),
       price("@10", "@12", strike="@10%45", to_at="@10%60", badge_at="@11"),
       photo("@12", None, src="mint.jpg", top=200, size=420),
       cta("@12", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"])])

# ---------------------------------------------------------------- NE03 (R03)
V["NE03"] = dict(slug="pakej-self-service", voice="Orus", style=MALE, lines=L(
    ("Satu benda best pasal Coway Neon, ada pakej self-service.", "Satu benda best: pakej *self-service*."),
    ("Maksudnya, you servis sendiri, bila-bila masa.", "Servis *sendiri*, bila-bila masa."),
    ("Sesuai untuk yang selalu sibuk, susah nak set appointment.", "Untuk yang selalu *sibuk*."),
    ("Caranya senang. Buka penutup.", "Senang. *Buka* penutup."),
    ("Cabut filter lama.", "*Cabut* filter lama."),
    ("Pasang filter baru.", "*Pasang* filter baru."),
    ("Alirkan air sekejap, dan siap.", "*Alirkan* air sekejap, *siap*."),
    ("Filter nak beli kat mana? Tak payah beli.", "Filter beli kat mana? *Tak payah.*"),
    ("Coway hantar filter original ke rumah, setiap lapan bulan, percuma.", "Coway hantar *setiap 8 bulan*, *percuma*."),
    ("Pakej self-service, dari lima puluh empat ringgit sebulan.", "Self-service dari *RM54* sebulan."),
    ("WhatsApp saya untuk pilih pakej yang sesuai.", "*WhatsApp* saya, pilih pakej sesuai.")),
  scenes=[(0, PRES_W), ("@02", PRES_C), ("@03", BUSY), ("@04", "navy"), ("@08", "navy"), ("@09", "navy"), ("@10", "blue"), ("@11", "blue")],
  els=[{"type": "banner", "in": "@01", "out": "@02", "top": 230, "html": "SATU BENDA BEST PASAL<br><em>COWAY NEON</em>"},
       pill("@01%55", "@02", "PAKEJ SELF-SERVICE", top=450),
       pill("@02", "@03", "SERVIS SENDIRI · BILA-BILA MASA", top=270),
       title("@03", "@04", f"SELALU <span style='color:var(--yellow)'>SIBUK?</span>", top=260, size=120),
       title("@04", "@08", f"<span style='color:var(--yellow)'>4</span> LANGKAH", top=250, size=110),
       {"type": "steps", "in": "@04", "out": "@08", "top": 480, "items": [
           {"text": "Buka penutup", "at": "@04%45"}, {"text": "Cabut filter lama", "at": "@05"},
           {"text": "Pasang filter baru", "at": "@06"}, {"text": "Alirkan air, siap ✓", "at": "@07"}]},
       title("@08", "@09", "FILTER BELI<br>KAT MANA?", top=420, size=110),
       {"type": "stamp", "in": "@08%60", "out": "@09", "top": 760, "html": "TAK PAYAH!", "color": "#1faa59"},
       title("@09", "@10", f"FILTER ORIGINAL<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>", top=250, size=84),
       {"type": "delivery", "in": "@09", "out": "@10", "top": 620},
       {"type": "stamp", "in": "@09%80", "out": "@10", "top": 1250, "html": "PERCUMA"},
       photo("@10", "@11", src="mint.jpg"),
       price("@10", "@11", label="SELF-SERVICE", frm="RM54"),
       photo("@11", None, src="mint.jpg", top=200, size=420),
       cta("@11", ["PAKEJ SERVIS / SELF-SERVICE", "PENGHANTARAN PERCUMA", "PEMASANGAN PERCUMA"], fine="*Tertakluk pada terma &amp; promosi semasa Coway.")])

# ---------------------------------------------------------------- NE04 (kos sehari)
V["NE04"] = dict(slug="kos-sehari-coway-neon", voice="Orus", style=MALE, lines=L(
    ("Berapa sebenarnya kos pasang Coway Neon, sehari?", "Berapa kos Coway Neon *sehari?*"),
    ("Harga asal, seratus empat ringgit sebulan.", "Harga asal *RM104* sebulan."),
    ("Tapi promosi sekarang, lima puluh empat ringgit je.", "Promosi sekarang *RM54* je."),
    ("Bahagi tiga puluh hari, satu ringgit lapan puluh sen sehari.", "÷ 30 hari = *RM1.80* sehari."),
    ("Tambah lagi rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan.", "+ Rebat ulang tahun *RM20 × 7 bulan*."),
    ("Tujuh bulan pertama, bersamaan satu ringgit tiga belas sen sehari.", "7 bulan pertama ≈ *RM1.13* sehari!"),
    ("Lebih murah dari secawan teh tarik.", "Lebih murah dari *teh tarik*."),
    ("Untuk tu, you dapat air panas, sejuk, dan suhu bilik.", "*Panas*, *sejuk*, *suhu bilik*."),
    ("Ditapis dengan Nanotrap, pemasangan pun percuma.", "*Nanotrap*, pemasangan *percuma*."),
    ("Nak saya kirakan pakej yang sesuai? WhatsApp saya.", "Nak saya kirakan? *WhatsApp* saya.")),
  scenes=[(0, "navy"), ("@02", "blue"), ("@04", "navy"), ("@07", "navy"), ("@08", POUR), ("@09", PRES_C), ("@10", "blue")],
  els=[title("@01", "@02", f"BERAPA<br><span style='color:var(--yellow)'>SEHARI?</span>", top=300, size=130),
       photo("@01%40", "@02", top=760, size=460),
       price("@02", "@04", strike="@03", to_at="@03%25", top=420),
       title("@04", "@07", "SEHARI", top=300, size=80),
       {"type": "text", "in": "@04", "out": "@05", "top": 400, "size": 50, "weight": 700, "html": "RM54 ÷ 30 hari"},
       {"type": "counter", "in": "@04%20", "out": "@07", "top": 480, "from": 54, "to": 1.8, "prefix": "RM", "decimals": 2, "dur": .8, "color": "#fff"},
       pill("@05", "@07", "+ REBAT ULANG TAHUN RM20 × 7 BULAN", top=790),
       {"type": "text", "in": "@06", "out": "@07", "top": 900, "size": 42, "weight": 700, "html": "7 bulan pertama: (RM54 − RM20) ÷ 30"},
       {"type": "counter", "in": "@06%20", "out": "@07", "top": 980, "from": 1.8, "to": 1.13, "prefix": "RM", "decimals": 2, "dur": .8},
       {"type": "icon", "in": "@07", "out": "@08", "top": 420, "icon": "cup", "size": 300, "color": "#fff"},
       title("@07", "@08", f"LEBIH MURAH DARI<br><span style='color:var(--yellow)'>SECAWAN TEH TARIK</span>", top=800, size=76),
       chips("@08", "@09", [("PANAS", "@08%30"), ("SEJUK", "@08%55"), ("SUHU BILIK", "@08%75")]),
       pill("@09", "@10", "NANOTRAP · PEMASANGAN PERCUMA", top=270),
       photo("@10", None, top=200, size=420),
       cta("@10", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"], btn_at="@10%60")])

# ---------------------------------------------------------------- NE05 (bayi, 3 pagi)
V["NE05"] = dict(slug="pukul-3-pagi-bancuh-susu", voice="Aoede", style=FEM, lines=L(
    ("Pukul tiga pagi. Baby menangis.", "*3 pagi.* Baby menangis."),
    ("Susu kena siap, sekarang.", "Susu kena siap *sekarang*."),
    ("Tangan pegang botol, mata separuh terbuka.", "Mata separuh terbuka..."),
    ("Masa macam ni, you nak semua benda dekat dan cepat.", "Nak semua *dekat* & *cepat*."),
    ("Sebab tu Coway Neon ngam untuk dapur keluarga muda.", "*Coway Neon*, ngam untuk keluarga muda."),
    ("Tekan je, air terus keluar.", "Tekan je, air *terus keluar*."),
    ("Panas, sejuk, atau suhu bilik.", "*Panas*, *sejuk*, *suhu bilik*."),
    ("Nak cepat, pilih dua ratus lima puluh mililiter, dia berhenti sendiri.", "Pilih *250ml*, berhenti *sendiri*."),
    ("Air ditapis dengan penapis Nanotrap.", "Ditapis *Nanotrap*."),
    ("Untuk suhu air susu, ikut nasihat doktor ya.", "Suhu air susu? *Ikut nasihat doktor.*"),
    ("Promosi lima puluh empat ringgit sebulan, tambah rebat dua puluh ringgit, tujuh bulan.", "Promosi *RM54*, + rebat *RM20 × 7 bulan*."),
    ("WhatsApp saya, saya uruskan sampai siap pasang.", "*WhatsApp* saya, saya uruskan sampai *siap pasang*.")),
  scenes=[(0, "night"), ("@02", {"clip": "bottles_busy", "c0": 0.0, "c1": 3.9}), ("@04", PREP), ("@05", PINKBG), ("@06", POUR), ("@08", PINKBG), ("@09", "navy"),
          ("@10", "pastel"), ("@11", {"clip": "bottle_to_baby", "c0": 4.5, "c1": 10.0}), ("@12", "blue")],
  els=[title("@01", "@02", "03:00", top=560, size=260),
       {"type": "text", "in": "@01%40", "out": "@02", "top": 880, "size": 56, "weight": 700, "html": "Baby menangis... 😢"},
       pill("@04", "@05", "DEKAT & CEPAT", top=270),
       title("@05", "@06", f"COWAY <span style='color:{CORAL}'>NEON</span>", top=190, size=110, dark=True),
       pill("@06", "@07", "TEKAN JE", top=270),
       chips("@07", "@08", [("PANAS", "@07"), ("SEJUK", "@07%30"), ("SUHU BILIK", "@07%60")]),
       {"type": "photo", "in": "@08", "out": "@09", "top": 380, "left": 0, "w": 1080, "h": 1080, "radius": 0, "shadow": False, "float": False,
        "src": IMG + "pink.jpg", "zx": 74, "zy": 29, "zs": 2.6, "zin": "@08", "zout": "@08%45"},
       pill("@08%40", "@09", "250ml · BERHENTI SENDIRI", top=250, bg="#fff"),
       {"type": "card", "in": "@09", "out": "@10", "top": 760, "icon": "filter", "title": "PENAPIS NANOTRAP", "sub": "Teknologi penapisan Coway"},
       {"type": "card", "in": "@10", "out": "@11", "top": 760, "icon": "baby", "icbg": "#fde8e4", "iccolor": CORAL, "title": "SUHU AIR SUSU?", "sub": "Ikut nasihat doktor / pakar kanak-kanak"},
       pill("@11", "@12", "RM54 + REBAT RM20 × 7 BULAN*", top=270),
       photo("@12", None, top=200, size=420),
       cta("@12", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"])])

# ---------------------------------------------------------------- NE06 (R06 RO vs Nanotrap)
V["NE06"] = dict(slug="coway-semua-ro-ke", voice="Aoede", style=FEM, lines=L(
    ("Ramai tanya, Coway semua RO ke?", "Ramai tanya, Coway *semua RO* ke?"),
    ("Sebenarnya, tak. Coway ada dua jenis.", "Tak. Coway ada *2 jenis*."),
    ("RO, macam Vila-em Tiga dan Neo Plus.", "*RO*: Villaem 3, Neo Plus."),
    ("Dan Nanotrap, bukan RO, macam Coway Neon.", "*Nanotrap*, bukan RO: *Coway Neon*."),
    ("Air rumah keruh, berkarat, atau berkeladak? Pilih RO.", "Air *keruh* atau *berkarat*? Pilih *RO*."),
    ("Air paip rumah dah jernih? Neon boleh jadi pilihan.", "Air *jernih*? *Neon* boleh jadi pilihan."),
    ("Nanotrap bantu tapis bakteria, virus, dan logam berat.", "Tapis *bakteria*, *virus*, *logam berat*."),
    ("Pilih ikut air rumah, bukan ikut siapa paling kuat jual.", "Pilih ikut *air rumah*."),
    ("Tak pasti? Hantar gambar air paip rumah ke WhatsApp saya.", "Tak pasti? Hantar *gambar air paip* ke WhatsApp.")),
  scenes=[(0, "pastel"), ("@05", "navy"), ("@06", PODIUM), ("@07", "navy"), ("@08", "pastel"), ("@09", "blue")],
  els=[title("@01", "@02", "COWAY<br>SEMUA RO?", top=520, size=140, dark=True),
       {"type": "stamp", "in": "@01e-0.1", "out": "@02", "top": 900, "html": "MITOS"},
       title("@02", "@05", f"COWAY ADA <span style='color:{CORAL}'>2 JENIS</span>", top=260, size=90, dark=True),
       {"type": "vs", "in": "@02%50", "out": "@05", "top": 480,
        "left": {"title": "RO", "color": "#0B4DA2", "items": ["Villaem 3", "Neo Plus", "Cinnamon", "Ais"], "at": "@03"},
        "right": {"title": "NANOTRAP", "color": CORAL, "items": ["Neon", "Dazzie", "(bukan RO)"], "at": "@04"}},
       title("@05", "@06", "AIR RUMAH ANDA", top=250, size=84),
       chips("@05", "@06", [("KERUH", "@05"), ("BERKARAT", "@05%20"), ("BERKELADAK", "@05%40")], top=460),
       pill("@05%70", "@06", "→ PILIH RO", top=880, bg=SKY, color="#fff"),
       title("@06", "@07", f"AIR JERNIH?<br><span style='color:{CORAL}'>NEON BOLEH</span>", top=200, size=100, dark=True),
       {"type": "icon", "in": "@07", "out": "@08", "top": 330, "icon": "shield", "size": 260, "color": "#fff"},
       chips("@07", "@08", [("BAKTERIA", "@07%20"), ("VIRUS", "@07%40"), ("LOGAM BERAT", "@07%65")], top=700),
       title("@08", "@09", f"PILIH IKUT<br><span style='color:{CORAL}'>AIR RUMAH</span>", top=520, size=120, dark=True),
       {"type": "text", "in": "@08%50", "out": "@09", "top": 820, "color": NAVY, "html": "bukan ikut siapa paling kuat jual 🙂"},
       {"type": "icon", "in": "@09", "out": None, "top": 300, "icon": "drop", "size": 260, "color": "#fff"},
       cta("@09", ["NASIHAT PERCUMA", "TAKDE PAKSAAN"], btn="Hantar gambar air paip", fine="Saya cadangkan model yang sesuai dengan air rumah anda.")])

# ---------------------------------------------------------------- NE07 (kuiz warna)
V["NE07"] = dict(slug="kuiz-warna-dapur", voice="Aoede", style=FEM, lines=L(
    ("Kuiz sepuluh saat! Dapur you warna apa?", "*Kuiz 10 saat!* Dapur you warna apa?"),
    ("A, pink lembut.", "*A*, pink lembut."),
    ("B, hijau mint.", "*B*, hijau mint."),
    ("C, biru langit.", "*C*, biru langit."),
    ("D, kelabu gelap.", "*D*, kelabu gelap."),
    ("E, putih bersih.", "*E*, putih bersih."),
    ("Apa pun jawapan you, Coway Neon ada warna tu.", "Apa pun jawapan, *Neon ada warna tu!*"),
    ("Peach pink, mint green, ciel blue, pebble gray, porcelain white.", "*5 warna* Coway Neon."),
    ("Kompak, dan ada tiga suhu. Panas, sejuk, suhu bilik.", "*Kompak*, *3 suhu*."),
    ("Komen huruf pilihan you kat bawah!", "*Komen* huruf pilihan you!"),
    ("Nak pasang warna tu? WhatsApp saya. Promosi lima puluh empat ringgit sebulan, tambah rebat ulang tahun.", "*WhatsApp* saya. Promosi *RM54* + *rebat*!")),
  scenes=[(0, "pastel"), ("@08", "pastel"), ("@09", PRES_C), ("@10", PODIUM), ("@11", "blue")],
  els=[title("@01", "@08", f"KUIZ <span style='color:{CORAL}'>10 SAAT</span>", top=200, size=110, dark=True),
       pill("@01%50", "@08", "DAPUR ANDA WARNA APA?", top=350, bg=NAVY, color="#fff"),
       {"type": "quiz", "in": "@01%60", "out": "@08", "top": 500, "answer": [0, 1, 2, 3, 4], "answerAt": "@07", "options": [
           {"text": "Pink lembut", "color": "#F3C9BD", "at": "@02"}, {"text": "Hijau mint", "color": "#C5DCCB", "at": "@03"},
           {"text": "Biru langit", "color": "#BFD5E8", "at": "@04"}, {"text": "Kelabu gelap", "color": "#3a3d42", "at": "@05"},
           {"text": "Putih bersih", "color": "#F4F3EF", "at": "@06"}]},
       {"type": "stamp", "in": "@07", "out": "@08", "top": 1250, "html": "SEMUA BETUL!", "color": "#1faa59"},
       title("@08", "@09", f"<span style='color:{CORAL}'>5</span> WARNA NEON", size=110, dark=True),
       lineup("@08", "@09", [("@08", "pink"), ("@08%20", "mint"), ("@08%40", "ciel"), ("@08%60", "gray"), ("@08%80", "white"), ("@08e", "all")]),
       chips("@09", "@10", [("KOMPAK", "@09"), ("3 SUHU", "@09%40")]),
       title("@10", "@11", f"KOMEN<br><span style='color:{CORAL}'>A · B · C · D · E</span>", top=180, size=100, dark=True),
       photo("@11", None, top=200, size=420),
       cta("@11", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "5 PILIHAN WARNA"])])

# ---------------------------------------------------------------- NE08 (logam berat)
V["NE08"] = dict(slug="logam-berat-paip-lama", voice="Orus", style=MALE, lines=L(
    ("Rumah lama, paip lama? Ramai tak tahu pasal ni.", "Rumah lama, *paip lama?*"),
    ("Air boleh bawa logam berat dari paip dan tangki.", "Air boleh bawa *logam berat*."),
    ("Contohnya, merkuri,", "*Merkuri*,"),
    ("plumbum,", "*plumbum*,"),
    ("besi,", "*besi*,"),
    ("dan aluminium.", "& *aluminium*."),
    ("Coway Neon guna penapis Nanotrap.", "Neon guna *Nanotrap*."),
    ("Ia bantu tapis logam berat ni, termasuk bakteria dan virus.", "Tapis *logam berat*, *bakteria* & *virus*."),
    ("Air bersih, terus dari dapur you.", "Air *bersih*, terus dari dapur."),
    ("Harga asal seratus empat, promosi lima puluh empat ringgit, tambah rebat dua puluh ringgit, tujuh bulan.", "Asal *RM104*, promosi *RM54*, + rebat *RM20 × 7 bulan*."),
    ("WhatsApp saya, pemasangan percuma.", "*WhatsApp* saya, pemasangan *percuma*."),
    ("Jom, pastikan air untuk keluarga you betul-betul bersih.", "Pastikan air keluarga *bersih*.")),
  scenes=[(0, "dark"), ("@03", "dark"), ("@07", PODIUM), ("@08", "navy"), ("@09", {"clip": "press_pour", "c0": 3.0, "c1": 5.2}), ("@10", "blue"), ("@11", "blue")],
  els=[{"type": "icon", "in": "@01", "out": "@03", "top": 360, "icon": "pipe", "size": 300, "color": "#9aa6b8"},
       title("@01", "@03", f"PAIP <span style='color:var(--yellow)'>LAMA?</span>", top=760, size=130),
       {"type": "text", "in": "@02", "out": "@03", "top": 960, "size": 50, "html": "Air boleh bawa <b style='color:var(--yellow)'>logam berat</b>"},
       title("@03", "@07", "LOGAM BERAT", top=250, size=100),
       {"type": "grid", "in": "@03", "out": "@07", "top": 470, "items": [
           {"big": "Hg", "small": "MERKURI", "at": "@03"}, {"big": "Pb", "small": "PLUMBUM", "at": "@04"},
           {"big": "Fe", "small": "BESI", "at": "@05"}, {"big": "Al", "small": "ALUMINIUM", "at": "@06"}]},
       title("@07", "@08", f"PENAPIS<br><span style='color:{CORAL}'>NANOTRAP</span>", top=180, size=100, dark=True),
       {"type": "icon", "in": "@08", "out": "@09", "top": 330, "icon": "shield", "size": 260, "color": "#fff"},
       chips("@08", "@09", [("LOGAM BERAT", "@08%25"), ("BAKTERIA", "@08%55"), ("VIRUS", "@08%75")], top=700),
       pill("@09", "@10", "AIR BERSIH DARI DAPUR", top=270),
       photo("@10", "@11"),
       price("@10", "@11", strike="@10%30", to_at="@10%45", badge_at="@10%72"),
       photo("@11", None, top=200, size=420),
       cta("@11", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"])])

# ---------------------------------------------------------------- NE09 (3 tanda)
V["NE09"] = dict(slug="3-tanda-neon-sesuai", voice="Orus", style=MALE, lines=L(
    ("Tiga tanda Coway Neon memang sesuai untuk rumah you.", "*3 tanda* Neon sesuai untuk rumah you."),
    ("Satu, dapur you kecil.", "*1.* Dapur *kecil*."),
    ("Neon kompak, tak makan ruang.", "Neon *kompak*, tak makan ruang."),
    ("Dua, you selalu sibuk.", "*2.* Selalu *sibuk*."),
    ("Ambil pakej self-service, filter dihantar setiap lapan bulan.", "*Self-service*, filter tiap *8 bulan*."),
    ("Tiga, ada budak kecil di rumah.", "*3.* Ada *budak kecil*."),
    ("Air panas ada kunci, tekan tiga saat.", "Air panas *berkunci*, tekan *3 saat*."),
    ("Bonus, lima warna, pilih yang ngam dengan dapur.", "*Bonus:* *5 warna*!"),
    ("Harga asal seratus empat, promosi lima puluh empat ringgit, tambah rebat dua puluh ringgit, tujuh bulan.", "Asal *RM104*, promosi *RM54*, + rebat *RM20 × 7 bulan*."),
    ("WhatsApp saya, penghantaran dan pemasangan percuma.", "*WhatsApp* saya, pasang *percuma*."),
    ("Jom, pilih warna you sekarang.", "Jom, pilih *warna* you!")),
  scenes=[(0, "navy"), ("@02", PRES_C), ("@04", BUSY), ("@05", "navy"), ("@06", PINKBG), ("@08", "pastel"), ("@09", "blue"), ("@10", "blue")],
  els=[title("@01", "@02", f"<span style='color:var(--yellow)'>3 TANDA</span>", top=520, size=180),
       {"type": "banner", "in": "@01%30", "out": "@02", "top": 780, "html": "COWAY NEON SESUAI<br><em>UNTUK RUMAH ANDA</em>"},
       {"type": "reason", "in": "@02", "out": "@04", "top": 250, "num": "1", "title": "DAPUR KECIL", "sub": "Neon kompak, tak makan ruang"},
       {"type": "reason", "in": "@04", "out": "@05", "top": 250, "num": "2", "title": "SELALU SIBUK", "sub": "ambil pakej self-service"},
       title("@05", "@06", f"FILTER BARU<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>", top=250, size=84),
       {"type": "delivery", "in": "@05", "out": "@06", "top": 620},
       {"type": "reason", "in": "@06", "out": "@07", "top": 220, "num": "3", "title": "<span style='color:#0B2F6B; text-shadow:none'>ADA BUDAK KECIL</span>"},
       {"type": "photo", "in": "@07", "out": "@08", "top": 380, "left": 0, "w": 1080, "h": 1080, "radius": 0, "shadow": False, "float": False,
        "src": IMG + "pink.jpg", "zx": 57, "zy": 33, "zs": 2.8, "zin": "@07", "zout": "@07%45"},
       pill("@07%35", "@08", "🔒 HOT LOCK · TEKAN 3 SAAT", top=250, bg=NAVY, color="#fff"),
       title("@08", "@09", f"BONUS: <span style='color:{CORAL}'>5 WARNA</span>", size=100, dark=True),
       lineup("@08", "@09", [("@08", "all"), ("@08%35", "mint"), ("@08%65", "ciel"), ("@08e", "all")]),
       photo("@09", "@10"),
       price("@09", "@10", strike="@09%30", to_at="@09%45", badge_at="@09%72"),
       photo("@10", None, top=200, size=420),
       cta("@10", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"])])

# ---------------------------------------------------------------- NE10 (proses pasang)
V["NE10"] = dict(slug="proses-pasang-4-langkah", voice="Orus", style=MALE, lines=L(
    ("Nak pasang Coway Neon, tapi tak tahu prosesnya? Senang je.", "Tak tahu *proses* pasang? Senang je."),
    ("Langkah satu, WhatsApp saya.", "*1.* WhatsApp saya."),
    ("Langkah dua, pilih warna. Ada lima.", "*2.* Pilih *warna*, ada 5."),
    ("Langkah tiga, pilih pakej. Beserta servis, atau self-service.", "*3.* Pilih *pakej*."),
    ("Langkah empat, technician datang pasang, percuma.", "*4.* Technician pasang, *percuma*."),
    ("Lepas tu, terus guna. Panas, sejuk, suhu bilik.", "Terus guna: *panas*, *sejuk*, *suhu bilik*."),
    ("Kalau ambil self-service, filter baru dihantar setiap lapan bulan.", "Self-service: filter tiap *8 bulan*."),
    ("Harga asal seratus empat ringgit, tapi promosi sekarang lima puluh empat ringgit je,", "Harga asal *RM104*, promosi *RM54*,"),
    ("dan tambah rebat ulang tahun Coway, dua puluh ringgit, selama tujuh bulan.", "+ rebat ulang tahun *RM20 × 7 bulan*."),
    ("Jom, tekan WhatsApp sekarang.", "Jom, tekan *WhatsApp*!")),
  scenes=[(0, "navy"), ("@02", "navy"), ("@03", "pastel"), ("@04", "navy"), ("@05", PRES_C), ("@06", POUR), ("@07", "navy"),
          ("@08", "blue"), ("@10", "blue")],
  els=[title("@01", "@02", f"PROSES PASANG<br><span style='color:var(--yellow)'>COWAY NEON</span>", top=520, size=100),
       pill("@01%50", "@02", "4 LANGKAH", top=820),
       {"type": "reason", "in": "@02", "out": "@03", "top": 360, "num": "1", "title": "WHATSAPP SAYA"},
       {"type": "icon", "in": "@02%20", "out": "@03", "top": 700, "icon": "phone", "size": 300, "color": "#25D366"},
       pill("@03", "@04", "2 · PILIH WARNA", top=250, bg=NAVY, color="#fff"),
       lineup("@03", "@04", [("@03", "all"), ("@03%40", "pink"), ("@03%75", "ciel")]),
       {"type": "reason", "in": "@04", "out": "@05", "top": 250, "num": "3", "title": "PILIH PAKEJ"},
       {"type": "card", "in": "@04%30", "out": "@05", "top": 640, "icon": "tech", "title": "BESERTA SERVIS", "sub": "Technician datang servis"},
       {"type": "card", "in": "@04%60", "out": "@05", "top": 950, "icon": "box", "icbg": "#fff3cc", "iccolor": "#b07b00", "title": "SELF-SERVICE", "sub": "Tukar filter sendiri"},
       pill("@05", "@06", "4 · PEMASANGAN PERCUMA", top=270),
       chips("@06", "@07", [("PANAS", "@06%40"), ("SEJUK", "@06%60"), ("SUHU BILIK", "@06%80")]),
       title("@07", "@08", f"SELF-SERVICE:<br>FILTER TIAP <span style='color:var(--yellow)'>8 BULAN</span>", top=250, size=80),
       {"type": "delivery", "in": "@07", "out": "@08", "top": 620},
       photo("@08", "@10"),
       price("@08", "@10", strike="@08%45", to_at="@08%60", badge_at="@09"),
       photo("@10", None, top=200, size=420),
       cta("@10", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"], btn_at="@10%30")])

# ---------------------------------------------------------------- E04 (R02, versi template; ganti videos/E04 asal)
V["E04"] = dict(slug="3-sebab-ramai-pasang", voice="Orus", style=MALE, lines=L(
    ("Kenapa ramai sangat pasang Coway Neon sekarang?", "Kenapa ramai pasang *Coway Neon*?"),
    ("Tiga sebab.", "*3 sebab.*"),
    ("Satu, saiz dia kompak, tak makan ruang dapur.", "*1.* Saiz *kompak*, tak makan ruang dapur."),
    ("Dan ada lima warna.", "Ada *5 warna*."),
    ("Pink, mint, biru, kelabu, dan putih.", "*Pink*, *mint*, *biru*, *kelabu* & *putih*."),
    ("Dua, pakej ikut gaya hidup.", "*2.* Pakej ikut *gaya hidup*."),
    ("Nak technician datang servis? Boleh.", "Nak *technician* datang? *Boleh.*"),
    ("Selalu sibuk? Ambil pakej self-service.", "Selalu *sibuk?* Ambil *self-service*."),
    ("Filter baru dihantar setiap lapan bulan, percuma.", "Filter baru setiap *8 bulan*, *percuma*."),
    ("Tiga, harga.", "*3.* *Harga.*"),
    ("Panas, sejuk, suhu bilik, semua ada.", "*Panas*, *sejuk*, *suhu bilik*."),
    ("Harga asal seratus empat ringgit, promosi sekarang lima puluh empat ringgit je.", "Harga asal *RM104*, promosi *RM54* je."),
    ("Tambah rebat ulang tahun Coway, dua puluh ringgit, tujuh bulan.", "+ Rebat ulang tahun *RM20 × 7 bulan*."),
    ("Nak pasang? Tekan WhatsApp, penghantaran dan pemasangan percuma.", "*WhatsApp* saya, pasang *percuma*.")),
  scenes=[(0, PRES_W), ("@02", {"clip": "presenter", "c0": 6.4, "c1": 8.0}), ("@03", PREP), ("@04", PODIUM), ("@05", "pastel"),
          ("@06", "navy"), ("@08", BUSY), ("@09", "navy"), ("@10", "navy"), ("@11", POUR), ("@12", "blue"), ("@14", COT), ("@14e", "blue")],
  els=[{"type": "banner", "in": "@01", "out": "@02", "top": 230, "html": "KENAPA RAMAI PASANG<br><em>COWAY NEON?</em>"},
       title("@02", "@03", "3 SEBAB", top=760, size=200, color="var(--yellow)"),
       {"type": "reason", "in": "@03", "out": "@04", "top": 250, "num": "1", "title": "KOMPAK", "sub": "tak makan ruang dapur"},
       title("@04", "@06", f"<span style='color:{CORAL}'>5</span> WARNA", size=120, dark=True),
       lineup("@05", "@06", [("@05", "pink"), ("@05%20", "mint"), ("@05%40", "ciel"), ("@05%60", "gray"), ("@05%80", "white"), ("@05e", "all")]),
       {"type": "reason", "in": "@06", "out": "@08", "top": 330, "num": "2", "title": "PAKEJ IKUT<br>GAYA HIDUP"},
       {"type": "card", "in": "@07", "out": "@08", "top": 760, "icon": "tech", "title": "BESERTA SERVIS", "sub": "Technician datang ke rumah"},
       {"type": "stamp", "in": "@07%70", "out": "@08", "top": 1080, "html": "BOLEH ✓", "color": "#1faa59", "rot": -8},
       title("@08", "@09", f"SELALU <span style='color:var(--yellow)'>SIBUK?</span>", top=260, size=120),
       {"type": "card", "in": "@08%50", "out": "@09", "top": 1180, "icon": "box", "icbg": "#fff3cc", "iccolor": "#b07b00", "title": "SELF-SERVICE", "sub": "Tukar filter sendiri, bila-bila masa"},
       title("@09", "@10", f"FILTER BARU<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>", top=270, size=82),
       {"type": "delivery", "in": "@09", "out": "@10", "top": 620},
       {"type": "stamp", "in": "@09%80", "out": "@10", "top": 1250, "html": "PERCUMA"},
       {"type": "reason", "in": "@10", "out": "@11", "top": 760, "num": "3", "title": "HARGA"},
       chips("@11", "@12", [("PANAS", "@11"), ("SEJUK", "@11%30"), ("SUHU BILIK", "@11%55")]),
       photo("@12", "@14"),
       price("@12", "@14", strike="@12%45", to_at="@12%60", badge_at="@13"),
       title("@14", "@14e", "NAK PASANG?", top=260, size=120),
       photo("@14e", None, src="mint.jpg", top=200, size=420),
       cta("@14", ["PROMOSI RM54 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"], btn_at="@14%40")])


BRAND = {"theme": "coway", "brand": "COWAY", "tagline": "Own Your Aesthetics, Affordably."}

if __name__ == "__main__":
    import sys
    plain = "--plain" in sys.argv          # --plain: gaya asal tanpa tema brand Coway
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        spec = {"slug": v["slug"], "voice": v["voice"], "style": v["style"],
                "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"], **({} if plain else BRAND)}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['slug']:32s} {v['voice']:6s} {len(v['lines']):2d} baris, {words} perkataan (~{words / 2.6:.0f}s)")
