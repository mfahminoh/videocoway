"""Batch video Coway Villaem 3 (skrip diluluskan 30/9 dalam skrip/villaem3.md): V3-02, 03, 04, 05, 07, 08, 09, 10.

    python videos/v3_batch.py                       # tulis videos/V3xx/{lines.json, spec.json}
    python videos/build_video.py V302 --tts --render

Harga (disahkan pengguna 30/9): harga asal RM120, promosi RM74/bulan, + rebat ulang tahun Coway RM20 x 7 bulan.
Klip: assets/clips/clip1..clip5 (milik sendiri). Elak clip1 >3s (teks "RM20" lama) dan clip3 >7s (teks rosak).
"""
import json
import pathlib

from neon_batch import L, title, chips, pill, NAVY, CORAL, SKY, FEM, MALE

HERE = pathlib.Path(__file__).parent
IMG = "../../assets/img/"
FINE = "*Harga asal RM120/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway."
TICKS = ["PROMOSI RM74 SEBULAN*", "+ REBAT RM20 × 7 BULAN*", "PEMASANGAN PERCUMA"]

PRES = {"clip": "clip1", "c0": 0.0, "c1": 2.9}          # presenter tunjuk produk (bercakap)
PRESS = {"clip": "clip2", "c0": 0.0, "c1": 3.0}         # tangan tekan panel 40 -> 50 -> 60
UV = {"clip": "clip2", "c0": 3.3, "c1": 6.2}            # tangki + cahaya UV
ECO = {"clip": "clip3", "c0": 0.0, "c1": 1.4}           # label ECO MODE
DUAL = {"clip": "clip3", "c0": 3.9, "c1": 5.6}          # label DUAL LOCK MODE
ORBIT = {"clip": "clip4", "c0": 6.0, "c1": 10.0}        # produk berputar, tiada teks
CAP = {"clip": "clip5", "c0": 0.3, "c1": 4.2}           # TOTAL CAPACITY 11.4L
PROD = {"clip": "clip5", "c0": 4.5, "c1": 6.2}          # produk, tiada teks
AMT = {"clip": "clip5", "c0": 6.3, "c1": 9.5}           # jari tekan panel 120ml
TWO = {"image": "two-colors.jpg", "color": "dark", "top": 420, "h": 925, "fit": "cover"}


def product(at, out, top=180, size=520):
    return {"type": "photo", "in": at, "out": out, "top": top, "left": (1080 - size) // 2, "w": size, "h": size,
            "src": IMG + "villaem3-front.png", "fit": "contain", "shadow": False, "radius": 0}


def price(at, out, strike, to_at, badge_at=None, top=520):
    e = {"type": "price", "in": at, "out": out, "top": top, "label": "HARGA ASAL", "from": "RM120", "strikeAt": strike, "to": "RM74", "toAt": to_at}
    if badge_at:
        e.update(badge="+ REBAT ULANG TAHUN RM20 × 7 BULAN", badgeAt=badge_at)
    return e


def cta(at, ticks=TICKS, btn_at=None, top=760):
    e = {"type": "cta", "in": at, "top": top, "ticks": ticks, "button": "WhatsApp saya", "fine": FINE}
    if btn_at:
        e["btnAt"] = btn_at
    return e


PRICE_LINE = ("Harga asal seratus dua puluh ringgit, promosi tujuh puluh empat ringgit sebulan, tambah rebat dua puluh ringgit, tujuh bulan.",
              "Asal *RM120*, promosi *RM74*, + rebat *RM20 × 7 bulan*.")

V = {}

# ---------------------------------------------------------------- V3-02 Chat: kenapa lagi mahal
V["V302"] = dict(slug="kenapa-villaem3-lagi-mahal", voice="Aoede", style=FEM, lines=L(
    ("Customer selalu tanya saya satu soalan ni.", "Customer selalu tanya *satu soalan* ni."),
    ("Kenapa Vila-em Tiga lagi mahal dari model lain?", "Kenapa *Villaem 3* lagi mahal?"),
    ("Jawapan saya, sebab ni jenis beli sekali, pakai lama.", "Sebab ni jenis *beli sekali, pakai lama*."),
    ("Tangki paling besar, sebelas perpuluhan empat liter.", "Tangki paling besar, *11.4 liter*."),
    ("Lapan pilihan suhu, dari empat puluh sampai sembilan puluh lima darjah.", "*8 suhu*, dari *40°* sampai *95°*."),
    ("Dan ada lampu UV dalam tangki, hapuskan sembilan puluh sembilan perpuluhan sembilan peratus bakteria.", "*UV* dalam tangki, hapuskan *99.9%* bakteria."),
    ("Okay, tapi sebulan berapa?", "Okay, tapi *sebulan berapa?*"),
    PRICE_LINE,
    ("Okay, boleh set tarikh pasang.", "Okay, boleh *set tarikh pasang*!"),
    ("Nak tanya soalan yang sama? WhatsApp saya.", "Nak tanya juga? *WhatsApp* saya.")),
  scenes=[(0, "pastel"), ("@04", CAP), ("@05", PRESS), ("@06", UV), ("@07", "pastel"), ("@10", "blue")],
  els=[pill("@01", "@04", "SOALAN PALING KERAP", top=210, bg=NAVY, color="#fff"),
       product("@01", "@02", top=520, size=560),
       {"type": "chat", "in": "@02", "out": "@04", "top": 380, "items": [
           {"side": "L", "text": "Kenapa Villaem 3 lagi mahal dari model lain? 🤔", "at": "@02"},
           {"side": "R", "text": "Sebab ni jenis beli sekali, pakai lama 🙂", "at": "@03"}]},
       chips("@04", "@05", [("TANGKI 11.4L", "@04")]),
       chips("@05", "@06", [("8 SUHU", "@05"), ("40° – 95°", "@05%40")]),
       pill("@06", "@07", "UV DALAM TANGKI · 99.9% BAKTERIA", top=270),
       {"type": "chat", "in": "@07", "out": "@10", "top": 330, "items": [
           {"side": "L", "text": "Okay, tapi sebulan berapa? 💸", "at": "@07"},
           {"side": "R", "text": "Harga asal RM120. Promosi RM74 sebulan ✅", "at": "@08"},
           {"side": "R", "text": "+ Rebat ulang tahun Coway RM20 × 7 bulan 🎉", "at": "@08%60"},
           {"side": "L", "text": "Okay, boleh set tarikh pasang 👍", "at": "@09"}]},
       product("@10", None, top=150, size=460),
       cta("@10")])

# ---------------------------------------------------------------- V3-03 Explainer: boleh tercemar?
V["V303"] = dict(slug="air-tangki-boleh-tercemar", voice="Kore", style=FEM, lines=L(
    ("Air dalam tangki penapis, boleh tercemar ke?", "Air dalam tangki, boleh *tercemar* ke?"),
    ("Air yang lama tersimpan dalam tangki boleh dicemari bakteria.", "Air lama tersimpan boleh dicemari *bakteria*."),
    ("Sebab itu, Vila-em Tiga dilengkapi sistem sterilisasi UV di dalam tangki.", "Sebab itu, *Villaem 3* ada *sterilisasi UV* dalam tangki."),
    ("Cahaya UV menghapuskan sembilan puluh sembilan perpuluhan sembilan peratus bakteria.", "UV hapuskan *99.9%* bakteria."),
    ("Jadi, air yang disimpan kekal bersih.", "Air yang disimpan *kekal bersih*."),
    ("Sebelum masuk ke tangki, air ditapis dahulu dengan sistem RO.", "Sebelum masuk tangki, ditapis *RO* dahulu."),
    ("Tangkinya besar, sebelas perpuluhan empat liter, tetapi kebersihannya tetap terjaga.", "Tangki *11.4L*, kebersihan *tetap terjaga*."),
    ("Promosi tujuh puluh empat ringgit sebulan, tambah rebat ulang tahun Coway, dua puluh ringgit selama tujuh bulan.", "Promosi *RM74*, + rebat *RM20 × 7 bulan*."),
    ("Mahu air yang bersih hingga titisan terakhir? WhatsApp saya.", "Air bersih hingga *titisan terakhir*? *WhatsApp* saya.")),
  scenes=[(0, "dark"), ("@03", UV), ("@03%55", {"clip": "clip4", "c0": 6.0, "c1": 8.3}), ("@04", "navy"), ("@05", PROD), ("@06", "navy"), ("@07", CAP), ("@08", "blue"), ("@09", "blue")],
  els=[{"type": "icon", "in": "@01", "out": "@03", "top": 380, "icon": "drop", "size": 280, "color": "#9aa6b8"},
       title("@01", "@03", f"BOLEH <span style='color:var(--yellow)'>TERCEMAR?</span>", top=760, size=120),
       {"type": "text", "in": "@02", "out": "@03", "top": 1110, "size": 50, "html": "Air lama tersimpan boleh dicemari <b style='color:var(--yellow)'>bakteria</b>"},
       pill("@03", "@04", "STERILISASI UV DALAM TANGKI", top=270),
       title("@04", "@05", "BAKTERIA DIHAPUSKAN", top=420, size=70),
       {"type": "counter", "in": "@04", "out": "@05", "top": 540, "from": 0, "to": 99.9, "suffix": "%", "decimals": 1, "dur": 1.2},
       pill("@05", "@06", "AIR KEKAL BERSIH ✓", top=270),
       {"type": "card", "in": "@06", "out": "@07", "top": 760, "icon": "filter", "title": "PENAPISAN RO", "sub": "Sebelum air masuk ke tangki"},
       chips("@07", "@08", [("TANGKI 11.4L", "@07"), ("TETAP BERSIH ✓", "@07%50")]),
       price("@08", "@09", strike="@08%10", to_at="@08%25", badge_at="@08%55"),
       product("@09", None, top=150, size=460),
       cta("@09")])

# ---------------------------------------------------------------- V3-04 Infografik: 11.4 liter
V["V304"] = dict(slug="11-liter-banyak-mana", voice="Puck", style=MALE, lines=L(
    ("Sebelas perpuluhan empat liter. Banyak mana tu sebenarnya?", "*11.4 liter.* Banyak mana tu?"),
    ("Kalau botol air satu setengah liter, lebih kurang tujuh botol setengah.", "Botol 1.5L? Lebih kurang *7.6 botol*."),
    ("Enam perpuluhan satu liter, suhu bilik.", "*6.1L* suhu bilik."),
    ("Dua perpuluhan enam liter, air sejuk.", "*2.6L* air sejuk."),
    ("Dua perpuluhan tujuh liter, air panas.", "*2.7L* air panas."),
    ("Maksudnya, anda ada hampir lapan botol besar air standby setiap hari.", "Hampir *8 botol besar* air *standby* setiap hari!"),
    ("Ini antara tangki paling besar dalam barisan Coway.", "Antara tangki *paling besar* Coway."),
    PRICE_LINE,
    ("WhatsApp saya untuk slot pemasangan percuma.", "*WhatsApp* saya, pemasangan *percuma*.")),
  scenes=[(0, "navy"), ("@02", "navy"), ("@03", CAP), ("@05", PROD), ("@06", "navy"), ("@07", ORBIT), ("@08", "blue"), ("@09", "blue")],
  els=[{"type": "counter", "in": "@01", "out": "@02", "top": 600, "from": 0, "to": 11.4, "suffix": "L", "decimals": 1, "dur": 1.0, "size": 260},
       title("@01%45", "@02", "BANYAK MANA TU?", top=940, size=80),
       title("@02", "@03", "BOTOL 1.5L", top=300, size=80),
       {"type": "bottles", "in": "@02", "out": "@03", "top": 470, "n": 8, "fill": 7.6, "dur": 2.2, "w": 100, "label": "≈ {n} botol"},
       chips("@03", "@06", [("6.1L BILIK", "@03"), ("2.6L SEJUK", "@04"), ("2.7L PANAS", "@05")], top=1250),
       title("@06", "@07", f"HAMPIR <span style='color:var(--yellow)'>8 BOTOL BESAR</span><br>STANDBY SETIAP HARI", top=260, size=70),
       {"type": "bottles", "in": "@06", "out": "@07", "top": 520, "n": 8, "fill": 7.6, "dur": 1.2, "delay": .1, "w": 100},
       pill("@07", "@08", "ANTARA TANGKI PALING BESAR COWAY", top=270),
       price("@08", "@09", strike="@08%25", to_at="@08%40", badge_at="@08%65"),
       product("@09", None, top=150, size=460),
       cta("@09")])

# ---------------------------------------------------------------- V3-05 Listicle: setiap suhu untuk apa
V["V305"] = dict(slug="8-suhu-untuk-apa", voice="Aoede", style=FEM, lines=L(
    ("Vila-em Tiga ada lapan suhu. Tapi setiap satu untuk apa?", "*8 suhu*. Setiap satu untuk apa?"),
    ("Sembilan puluh lima darjah, untuk mi segera dan masakan cepat.", "*95°*: mi segera & masakan cepat."),
    ("Lapan puluh, untuk kopi.", "*80°*: kopi."),
    ("Tujuh puluh, untuk teh.", "*70°*: teh."),
    ("Air suam pun ada tiga. Empat puluh untuk susu baby, lima puluh untuk air minum, enam puluh untuk rendam bihun.",
     "Suam: *40°* susu baby, *50°* air minum, *60°* rendam bihun."),
    ("Suhu bilik untuk minum banyak, dan air sejuk bila cuaca panas.", "*Suhu bilik* & *air sejuk*."),
    ("Isipadu pun boleh set, dari seratus dua puluh mililiter sampai tanpa had.", "Isipadu *120ml* sampai *tanpa had*."),
    ("Semua ni dalam satu mesin, tangki sebelas perpuluhan empat liter.", "Satu mesin, tangki *11.4L*."),
    ("Promosi tujuh puluh empat ringgit sebulan, tambah rebat dua puluh ringgit selama tujuh bulan. WhatsApp saya.",
     "Promosi *RM74* + rebat *RM20 × 7 bulan*. *WhatsApp* saya!")),
  scenes=[(0, "dark"), ("@06", ORBIT), ("@07", AMT), ("@08", CAP), ("@09", "blue")],
  els=[title("@01", "@02", f"<span style='color:var(--yellow)'>8 SUHU</span><br>UNTUK APA?", top=240, size=110),
       {"type": "led", "in": "@01%40", "out": "@06", "top": 560, "items": [
           {"num": "8", "unit": "", "label": "PILIHAN SUHU", "at": "@01%40"},
           {"num": "95", "label": "MI SEGERA", "at": "@02"}, {"num": "80", "label": "KOPI", "at": "@03"},
           {"num": "70", "label": "TEH", "at": "@04"}, {"num": "40", "label": "SUSU BABY", "at": "@05%20"},
           {"num": "50", "label": "AIR MINUM", "at": "@05%52"}, {"num": "60", "label": "RENDAM BIHUN", "at": "@05%78"}]},
       chips("@06", "@07", [("SUHU BILIK", "@06"), ("SEJUK", "@06%50")]),
       pill("@07", "@08", "120ml → TANPA HAD", top=270),
       pill("@08", "@09", "SATU MESIN · 11.4L", top=1250, bg=NAVY, color="#fff"),
       price("@09", None, strike="@09%10", to_at="@09%22", badge_at="@09%45", top=380),
       {"type": "cta", "in": "@09%75", "top": 1300, "ticks": [], "button": "WhatsApp saya", "fine": FINE}])

# ---------------------------------------------------------------- V3-07 Mitos vs fakta
V["V307"] = dict(slug="mitos-bil-elektrik-tinggi", voice="Kore", style=FEM, lines=L(
    ("Ramai takut ambil penapis air besar. Katanya bil elektrik naik.", "Penapis besar, *bil elektrik naik?*"),
    ("Mitos: tangki besar, mesti makan elektrik banyak.", "*Mitos:* tangki besar, makan elektrik."),
    ("Fakta: Vila-em Tiga ada Eco Mode, jimatkan penggunaan tenaga.", "*Fakta:* ada *Eco Mode*, jimat tenaga."),
    ("Satu lagi mitos: air panas bahaya untuk budak.", "*Mitos:* air panas bahaya untuk budak."),
    ("Fakta: ada Dual Lock, dan kunci air panas, tekan tiga saat.", "*Fakta:* *Dual Lock*, kunci *3 saat*."),
    ("Jadi, besar, tapi bijak dan selamat.", "Besar, tapi *bijak* & *selamat*."),
    ("Promosi tujuh puluh empat ringgit sebulan, tambah rebat dua puluh ringgit selama tujuh bulan.", "Promosi *RM74*, + rebat *RM20 × 7 bulan*."),
    ("Ada soalan lain? WhatsApp saya, saya jawab jujur.", "Ada soalan? *WhatsApp* saya.")),
  scenes=[(0, "dark"), ("@03", ECO), ("@03%45", {"clip": "clip4", "c0": 6.0, "c1": 8.0}), ("@04", "dark"), ("@05", DUAL),
          ("@05%45", {"clip": "clip4", "c0": 8.0, "c1": 10.0}), ("@06", PROD), ("@07", "blue"), ("@08", "blue")],
  els=[{"type": "icon", "in": "@01", "out": "@02", "top": 420, "icon": "money", "size": 260, "color": "#ffd23f"},
       title("@01", "@02", f"BIL ELEKTRIK<br><span style='color:var(--yellow)'>NAIK?</span>", top=760, size=120),
       title("@02", "@03", "TANGKI BESAR =<br>MAKAN ELEKTRIK?", top=560, size=96),
       {"type": "stamp", "in": "@02%40", "out": "@03", "top": 900, "html": "MITOS ✕"},
       {"type": "stamp", "in": "@03", "out": "@04", "top": 1180, "html": "FAKTA: ECO MODE", "color": "#1faa59"},
       title("@04", "@05", "AIR PANAS<br>BAHAYA UNTUK BUDAK?", top=560, size=96),
       {"type": "stamp", "in": "@04%40", "out": "@05", "top": 900, "html": "MITOS ✕"},
       {"type": "stamp", "in": "@05", "out": "@06", "top": 1180, "html": "FAKTA: KUNCI 3 SAAT", "color": "#1faa59"},
       pill("@06", "@07", "BESAR · BIJAK · SELAMAT", top=270),
       price("@07", "@08", strike="@07%10", to_at="@07%25", badge_at="@07%55"),
       product("@08", None, top=150, size=460),
       cta("@08")])

# ---------------------------------------------------------------- V3-08 Versus: Villaem 3 atau Neon
V["V308"] = dict(slug="villaem3-atau-neon", voice="Aoede", style=FEM, lines=L(
    ("Vila-em Tiga atau Neon? Ni soalan yang ramai tanya.", "*Villaem 3* atau *Neon*?"),
    ("Vila-em Tiga, sistem RO, tangki sebelas perpuluhan empat liter, lapan suhu.", "*Villaem 3*: RO, *11.4L*, *8 suhu*."),
    ("Neon, sistem Nanotrap, kompak, tiga suhu, lima warna.", "*Neon*: Nanotrap, kompak, *3 suhu*, *5 warna*."),
    ("Keluarga besar, masak banyak, air rumah kurang jernih? Pilih Vila-em Tiga.", "Keluarga besar, air kurang jernih? *Villaem 3*."),
    ("Rumah kecil, bajet ketat, air paip dah jernih? Neon memang ngam.", "Rumah kecil, air jernih? *Neon* ngam."),
    ("Vila-em Tiga, promosi tujuh puluh empat ringgit, tambah rebat dua puluh ringgit selama tujuh bulan.", "Villaem 3: promosi *RM74* + rebat *RM20 × 7 bulan*."),
    ("Neon, promosi lima puluh empat ringgit, tambah rebat yang sama.", "Neon: promosi *RM54* + rebat sama."),
    ("Masih tak pasti? WhatsApp saya, saya bantu pilih.", "Tak pasti? *WhatsApp* saya, saya bantu pilih.")),
  scenes=[(0, "pastel"), ("@02", "pastel"), ("@04", ORBIT), ("@05", {"image": "neon/podium5.jpg", "color": "pastel", "top": 420, "h": 1080, "mask": True}),
          ("@06", "blue"), ("@08", "blue")],
  els=[title("@01", "@02", f"VILLAEM 3<br><span style='color:{CORAL}'>ATAU NEON?</span>", top=240, size=110, dark=True),
       {"type": "photo", "in": "@01", "out": "@02", "top": 620, "left": 40, "w": 500, "h": 500, "src": IMG + "villaem3-front.png", "fit": "contain", "shadow": False, "radius": 0},
       {"type": "photo", "in": "@01%30", "out": "@02", "top": 650, "left": 580, "w": 440, "h": 440, "src": IMG + "neon/pink.jpg"},
       {"type": "vs", "in": "@02", "out": "@04", "top": 420,
        "left": {"title": "VILLAEM 3", "color": "#0B4DA2", "items": ["Sistem RO", "Tangki 11.4L", "8 suhu", "UV dalam tangki"], "at": "@02"},
        "right": {"title": "NEON", "color": CORAL, "items": ["Nanotrap", "Kompak", "3 suhu", "5 warna"], "at": "@03"}},
       pill("@04", "@05", "KELUARGA BESAR → VILLAEM 3", top=270),
       pill("@05", "@06", "RUMAH KECIL → NEON", top=250, bg=CORAL, color="#fff"),
       title("@06", "@08", "VILLAEM 3", top=330, size=80),
       title("@06%20", "@08", "<span style='color:var(--yellow)'>RM74</span><small style='font-size:50px'> /bulan*</small>", top=430, size=180),
       title("@07", "@08", "NEON", top=730, size=80),
       title("@07%20", "@08", "<span style='color:var(--yellow)'>RM54</span><small style='font-size:50px'> /bulan*</small>", top=830, size=180),
       pill("@06%60", "@08", "+ REBAT ULANG TAHUN RM20 × 7 BULAN", top=1110),
       cta("@08", ticks=["NASIHAT PERCUMA", "PEMASANGAN PERCUMA"], top=620)])

# ---------------------------------------------------------------- V3-09 Cerita: beli sekali pakai lama
V["V309"] = dict(slug="beli-sekali-pakai-lama", voice="Orus", style=MALE, lines=L(
    ("Tiga tahun saya jual Coway, ada satu jenis customer yang saya paling suka.", "*3 tahun* jual Coway, ada satu jenis customer..."),
    ("Diorang tak beli barang murah berulang kali.", "Diorang tak beli barang murah *berulang kali*."),
    ("Diorang beli sekali, yang terbaik, dan pakai lama.", "Beli sekali, *yang terbaik*, pakai *lama*."),
    ("Bila pilih penapis air, kebanyakan diorang pilih Vila-em Tiga.", "Kebanyakan diorang pilih *Villaem 3*."),
    ("Spec tinggi, tangki paling besar, lapan suhu.", "*Spec tinggi*, tangki *paling besar*, *8 suhu*."),
    ("Dan tahan lasak. Technician kami pun jarang dapat repair.", "*Tahan lasak.* Technician pun *jarang repair*."),
    ("Harga asal seratus dua puluh ringgit, sekarang promosi tujuh puluh empat ringgit sebulan.", "Asal *RM120*, promosi *RM74* sebulan."),
    ("Tambah rebat ulang tahun Coway, dua puluh ringgit selama tujuh bulan.", "+ Rebat ulang tahun *RM20 × 7 bulan*."),
    ("Kalau you pun jenis beli sekali pakai lama, WhatsApp saya.", "Beli sekali, pakai lama? *WhatsApp* saya.")),
  scenes=[(0, PRES), ("@02", "pastel"), ("@04", ORBIT), ("@05", PROD), ("@06", "navy"), ("@07", "blue"), ("@09", "blue")],
  els=[{"type": "banner", "in": "@01", "out": "@02", "top": 230, "html": "<em>3 TAHUN</em> JUAL COWAY"},
       title("@02", "@03", "BELI BARANG MURAH<br>BERULANG KALI", top=560, size=90, dark=True),
       {"type": "stamp", "in": "@02%50", "out": "@03", "top": 860, "html": "✕"},
       title("@03", "@04", f"BELI SEKALI.<br><span style='color:{CORAL}'>PAKAI LAMA.</span>", top=560, size=120, dark=True),
       title("@04", "@05", "VILLAEM 3", top=250, size=120),
       chips("@05", "@06", [("SPEC TINGGI", "@05"), ("11.4L", "@05%35"), ("8 SUHU", "@05%70")]),
       {"type": "icon", "in": "@06", "out": "@07", "top": 420, "icon": "shield", "size": 280, "color": "#fff"},
       title("@06", "@07", f"<span style='color:var(--yellow)'>TAHAN LASAK</span>", top=800, size=120),
       {"type": "text", "in": "@06%50", "out": "@07", "top": 960, "size": 46, "html": "Technician pun jarang dapat repair"},
       price("@07", "@09", strike="@07%45", to_at="@07%60", badge_at="@08"),
       product("@09", None, top=150, size=460),
       cta("@09")])

# ---------------------------------------------------------------- V3-10 Kinetic: 3 sebab sekarang
V["V310"] = dict(slug="3-sebab-pasang-sekarang", voice="Puck", style=MALE, lines=L(
    ("Tiga sebab sekarang masa paling best pasang Vila-em Tiga.", "*3 sebab* sekarang masa paling best!"),
    ("Satu, harga asal seratus dua puluh ringgit, sekarang promosi tujuh puluh empat ringgit je.", "*1.* Asal *RM120*, promosi *RM74* je."),
    ("Dua, double promo, rebat ulang tahun Coway, dua puluh ringgit selama tujuh bulan.", "*2.* Double promo: rebat *RM20 × 7 bulan*."),
    ("Tiga, pemasangan percuma, servis berkala oleh technician.", "*3.* Pemasangan *percuma*, servis berkala."),
    ("Dapat tangki sebelas perpuluhan empat liter, lapan suhu, UV dalam tangki.", "*11.4L*, *8 suhu*, *UV* dalam tangki."),
    ("Semua ni untuk pastikan keluarga you dapat air bersih, panas dan sejuk, setiap hari.", "Air *bersih*, *panas* & *sejuk*, setiap hari."),
    ("Promo ulang tahun tak lama.", "Promo ulang tahun *tak lama*!"),
    ("Tekan WhatsApp sekarang, saya uruskan sampai siap pasang.", "Tekan *WhatsApp*, saya uruskan sampai *siap pasang*.")),
  scenes=[(0, "navy"), ("@02", "blue"), ("@03", "blue"), ("@04", "navy"), ("@05", CAP), ("@06", ORBIT), ("@07", "dark"), ("@08", "blue")],
  els=[title("@01", "@02", f"<span style='color:var(--yellow)'>3 SEBAB</span>", top=500, size=190),
       {"type": "banner", "in": "@01%35", "out": "@02", "top": 780, "html": "PASANG <em>VILLAEM 3</em><br>SEKARANG"},
       {"type": "reason", "in": "@02", "out": "@03", "top": 200, "num": "1", "title": "HARGA PROMOSI"},
       price("@02", "@03", strike="@02%45", to_at="@02%60", top=500),
       {"type": "reason", "in": "@03", "out": "@04", "top": 200, "num": "2", "title": "DOUBLE PROMO"},
       title("@03", "@04", f"REBAT<br><span style='color:var(--yellow)'>RM20 × 7 BULAN</span>", top=620, size=110),
       {"type": "reason", "in": "@04", "out": "@05", "top": 250, "num": "3", "title": "PEMASANGAN<br>PERCUMA"},
       {"type": "card", "in": "@04%30", "out": "@05", "top": 760, "icon": "tech", "title": "SERVIS BERKALA", "sub": "Oleh technician Coway"},
       chips("@05", "@06", [("11.4L", "@05"), ("8 SUHU", "@05%35"), ("UV", "@05%65")]),
       chips("@06", "@07", [("BERSIH", "@06%20"), ("PANAS", "@06%45"), ("SEJUK", "@06%65")]),
       {"type": "icon", "in": "@07", "out": "@08", "top": 440, "icon": "clock", "size": 260, "color": "#ffd23f"},
       title("@07", "@08", "PROMO<br>TAK LAMA!", top=800, size=130),
       product("@08", None, top=150, size=460),
       cta("@08", btn_at="@08%30")])


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        (d / "lines.json").write_text(json.dumps(v["lines"], ensure_ascii=False, indent=1))
        spec = {"slug": v["slug"], "voice": v["voice"], "style": v["style"],
                "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"]}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in v["lines"])
        print(f"{vid} {v['slug']:30s} {v['voice']:6s} {len(v['lines']):2d} baris, {words} perkataan (~{words / 2.4 + 2.7:.0f}s)")
