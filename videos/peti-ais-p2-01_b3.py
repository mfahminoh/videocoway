"""Peti ais Coway, pakej video untuk ejen (projek/peti-ais-p2-01), batch 3: PA26-PA35
-> videos/PA26..PA35/{lines.json, spec.json} dan bahagian Batch 3 dalam projek/peti-ais-p2-01/skrip.md.

    python3 videos/peti-ais-p2-01_b3.py
    python3 videos/build_video.py PA26 --tts
    python3 videos/peti-ais-p2-01_b3.py            # jalan semula selepas VO / klip Flow
    python3 videos/build_video.py PA26 --render --review out/peti-ais-p2-01

Brief: projek/peti-ais-p2-01/brief.md, batch 3 = video pelan 18, 19, 21, 22, 23, 24, 26, 28, 29, 30.
Promo (user, 30 Okt 2026): rebat, bayar RM20 sebulan untuk 7 bulan pertama, kemudian RM84 (715L) / RM99 (551L),
penghantaran & pemasangan percuma seluruh Malaysia, tiada tarikh tamat disebut ("promosi terhad").
Shot hidup s18-s20 dijana user di Google Flow (shots.md); sehingga itu latar = bingkai Seedream.
"""
import importlib.util
import json
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("b2", HERE / "peti-ais-p2-01_b2.py")
b2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b2)
b1 = b2.b1
globals().update({k: getattr(b1, k) for k in (
    "KOD", "F", "NAVY", "YEL", "BLUE", "RED", "INK", "BRAND", "FEM", "FEM_STORY", "MALE", "MALE_HYPE",
    "L", "R", "banner", "title", "pill", "photo", "reason", "rban", "card", "stamp", "lakonan", "W", "BOX", "BBOX")})
b2.SHOTS.update({"s18": "s18_balik_raya", "s19": "s19_dapur_raya", "s20": "s20_dapur_baru"})
S, resolve, times, at_sec = b2.S, b2.resolve, b2.times, b2.at_sec

FINE_P = ("*Promosi rebat: bayar RM20 sebulan untuk 7 bulan pertama, kemudian RM84 (715L) / RM99 (551L) sebulan, "
          "pelan HEART Service 7 tahun (7+0), termasuk SST. Penghantaran &amp; pemasangan percuma seluruh Malaysia. "
          "Promosi terhad. Tertakluk terma &amp; syarat Coway.")
FINE_PW = FINE_P + " Waranti kompressor 10 tahun tertakluk polisi waranti Coway."
FINE_PH = FINE_P + " ¹Ujian makmal dalam persekitaran terkawal."
TICKS_P = ["BAYAR RM20/BULAN · 7 BULAN PERTAMA*", "KEMUDIAN 715L RM84 · 551L RM99", "HANTAR & PASANG PERCUMA"]

PROMO_715 = ("Sekarang ada promosi rebat: bayar dua puluh ringgit je sebulan, untuk tujuh bulan pertama. Lepas tu, lapan puluh empat ringgit.",
             "Bayar *RM20*/bulan · *7 bulan pertama**", "Harga: RM84 → RM20, lencana 7 bulan")
PROMO_551 = ("Sekarang ada promosi rebat: bayar dua puluh ringgit je sebulan, untuk tujuh bulan pertama. Lepas tu, sembilan puluh sembilan ringgit.",
             "Bayar *RM20*/bulan · *7 bulan pertama**", "Harga: RM99 → RM20, lencana 7 bulan")
PROMO_2 = ("Dua-dua model sekarang ada promosi rebat: bayar dua puluh ringgit sebulan, untuk tujuh bulan pertama.",
           "Dua model: bayar *RM20*/bulan · *7 bulan**", "Harga RM20 + dua model")


def price(at, out, frm, top=360):
    """Harga promo: harga bulanan biasa dipotong -> RM20, lencana 7 bulan pertama."""
    return {"type": "price", "in": at, "out": out, "top": top, "label": "HARGA BULANAN", "from": frm, "strikeAt": f"{at}%35",
            "to": "RM20", "toAt": f"{at}%50", "badge": "7 BULAN PERTAMA*", "badgeAt": f"{at}%70"}


def hantar(at, out, top=1180):
    return pill(at, out, "PENGHANTARAN &amp; PEMASANGAN PERCUMA", top=top)


def cta(at, fine=FINE_P, top=760, btn=None):
    return {"type": "cta", "in": at, "top": top, "ticks": TICKS_P, "button": "WhatsApp saya",
            "btnAt": btn or f"{at}%40", "fine": fine}


V = {}

# ---------------------------------------------------------------- PA26 · 18 Bila satu keluarga balik beraya (kat. 4)
V["PA26"] = dict(no="18", tajuk="Bila satu keluarga balik beraya", kat="4 Situasi hidup", hook="Seru situasi",
  slug="satu-keluarga-balik-beraya", voice="Kore", style=FEM, lines=L(
    ("Bila semua balik kampung, peti yang biasa cukup, tiba-tiba rasa kecil.", "Semua balik… *peti tiba-tiba kecil*", "Flow s18: keluarga sampai beraya"),
    ("Rendang, ketupat, kuih, air sirap satu tong. Semua nak masuk peti.", "Rendang · kuih · *air sirap*", "Flow s19: dapur raya penuh"),
    ("Akhirnya, lauk tidur atas meja, dan air batu kena beli kat kedai.", "Lauk *atas meja*. Air batu *beli kedai*.", "s19 sambung"),
    ("Peti ais Coway tujuh ratus lima belas liter, ruang untuk stok satu keluarga besar, dengan super freezing sampai negatif dua puluh lima.",
     "715L · *Super Freezing −25°C*", "Rasmi 715_spaces + LED"),
    PROMO_715,
    ("Penghantaran dan pemasangan percuma, seluruh Malaysia. WhatsApp saya.", "Hantar & pasang *percuma* · *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s18")), ("@02", S("s19")), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[banner("@01", "@02", "SEMUA BALIK…<br><em>PETI TIBA-TIBA KECIL</em>"),
       {"type": "chips", "in": "@02", "out": "@03", "top": 1080, "items": [{"text": "RENDANG", "color": "#fff", "at": "@02"},
                                                                         {"text": "KUIH", "color": "#fff", "at": "@02%30"},
                                                                         {"text": "AIR SIRAP", "color": YEL, "at": "@02%60"}]},
       pill("@03", "@04", "LAUK ATAS MEJA · AIR BATU BELI KEDAI", top=1180, bg=RED, color="#fff"),
       banner("@04", "@05", "COWAY <em>715L</em>"),
       photo("@04", "@05", "715_spaces.jpg", top=380, w=640, h=640),
       {"type": "led", "in": "@04%45", "out": "@05", "top": 1060, "items": [{"num": "-25", "unit": "°C", "label": "SUPER FREEZING", "at": "@04%50"}]},
       price("@05", "@06", "RM84"), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA27 · 19 Dapur renovate, peti lama (kat. 4)
V["PA27"] = dict(no="19", tajuk="Dah renovate dapur, peti lama tak padan", kat="4 Situasi hidup", hook="Seru situasi",
  slug="dapur-renovate-peti-lama", voice="Orus", style=MALE, lines=L(
    ("Kabinet baru. Jubin baru. Peti ais, dari rumah sewa.", "Kabinet baru… *peti dari rumah sewa*", "Flow s20: dapur baru, peti lama"),
    ("Lepas renovate, peti lama nampak kecil, kekuningan, dan tak padan dengan ruang yang dah diukur.", "Kecil · kuning · *tak padan*", "s20 sambung"),
    ("Sebelum pilih, padankan tiga benda: saiz ruang, arah buka pintu, dan warna dapur.", "Saiz · bukaan pintu · *warna*", "Cip"),
    ("Peti ais Coway lima ratus lima puluh satu liter, warna Black Inox, rekaan built-in, ruang enam milimeter je dengan kabinet.",
     "551L · Black Inox · *built-in 6 mm*", "Rasmi 551_builtin, 551_front"),
    PROMO_551,
    ("Penghantaran dan pemasangan percuma seluruh Malaysia. Hantar gambar dapur awak kat WhatsApp saya.", "Hantar gambar dapur · *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s20")), ("@03", "blue"), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[banner("@01", "@02", "KABINET BARU…<br><em>PETI DARI RUMAH SEWA</em>"),
       pill("@02", "@03", "KECIL · KUNING · TAK PADAN", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "PADANKAN<br>3 BENDA", top=360, size=120),
       {"type": "chips", "in": "@03", "out": "@04", "top": 760, "items": [{"text": "SAIZ RUANG", "color": "#fff", "at": "@03%35"},
                                                                       {"text": "BUKAAN PINTU", "color": "#fff", "at": "@03%55"},
                                                                       {"text": "WARNA", "color": YEL, "at": "@03%75"}]},
       banner("@04", "@05", "COWAY <em>551L</em> · BLACK INOX"),
       photo("@04", "@04%55", "551_front.jpg", top=380),
       photo("@04%55", "@05", "551_builtin.jpg", top=380),
       pill("@04%55", "@05", "BUILT-IN · RUANG 6 MM", top=1180),
       price("@05", "@06", "RM99"), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA28 · 21 Kenali 551L (kat. 5)
V["PA28"] = dict(no="21", tajuk="Kenali peti ais Coway Multi-Door 551L", kat="5 Kenali produk", hook="Seru situasi",
  slug="kenali-coway-551l", voice="Aoede", style=FEM, lines=L(
    ("Kalau awak suka barang dapur tersusun ikut kategori, tengok yang ni.", "Suka *tersusun*? Tengok ni.", "Rasmi 551_wide"),
    ("Peti ais Coway lima ratus lima puluh satu liter, empat pintu, warna Black Inox.", "551L · 4 pintu · *Black Inox*", "Rasmi 551_front"),
    ("Zon bawah boleh tukar: dari lima darjah untuk sayur, sampai negatif dua puluh untuk simpanan lama.",
     "Convertible Zone *5°C → −20°C*", "Rasmi 551_drawers + cip julat"),
    ("Triple inverter, dua kipas, dinding penyejuk logam, untuk sejuk yang konsisten.", "Triple Inverter · *Metal Cooling*", "Rasmi 551_inv_fan, 551_metal"),
    ("Silver ion dan penapis penyahbau, bantu kurangkan bau ikan dalam peti.", "Dual Hygiene¹ · kurang *bau ikan*", "Rasmi 551_deo_cubes"),
    PROMO_551,
    ("Penghantaran dan pemasangan percuma seluruh Malaysia. Nak tengok lebih dekat? WhatsApp saya.", "Hantar & pasang *percuma* · *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@03", "navy"), ("@04", "navy"), ("@05", "navy"), ("@06", "blue"), ("@07", "blue")],
  els=[photo(0, "@02", "551_wide.jpg", top=420, w=900, h=703),
       banner("@01", "@02", "SUKA <em>TERSUSUN</em>?"),
       banner("@02", "@03", "COWAY <em>551L</em> · 4 PINTU"),
       photo("@02", "@03", "551_front.jpg", top=380),
       pill("@02%45", "@03", "BLACK INOX", top=1180),
       banner("@03", "@04", "<em>CONVERTIBLE</em> ZONE"),
       photo("@03", "@04", "551_drawers.jpg", top=380, w=640, h=640),
       {"type": "chips", "in": "@03%30", "out": "@04", "top": 1060, "items": [{"text": "5→3°C BUAH/SAYUR", "color": "#fff", "at": "@03%30"},
                                                                           {"text": "2→0°C MINUMAN", "color": "#fff", "at": "@03%45"},
                                                                           {"text": "−1→−7°C", "color": "#fff", "at": "@03%60"},
                                                                           {"text": "−8→−20°C", "color": YEL, "at": "@03%75"}]},
       banner("@04", "@05", "TRIPLE <em>INVERTER</em>"),
       photo("@04", "@04%50", "551_inv_fan.png", top=360, w=600, h=700, fit="contain", shadow=False),
       photo("@04%50", "@05", "551_metal.jpg", top=380),
       pill("@04%50", "@05", "METAL COOLING", top=1180),
       banner("@05", "@06", "DUAL <em>HYGIENE</em>"),
       photo("@05", "@06", "551_deo_cubes.jpg", top=380),
       pill("@05%30", "@06", "SILVER ION · PENAPIS PENYAHBAU¹", top=1180),
       price("@06", "@07", "RM99"), hantar("@06%70", "@07"),
       cta("@07", fine=FINE_PH)])

# ---------------------------------------------------------------- PA29 · 22 715L besar macam mana? (kat. 5)
V["PA29"] = dict(no="22", tajuk="715L besar macam mana sebenarnya?", kat="5 Kenali produk", hook="Soalan / angka",
  slug="715l-besar-macam-mana", voice="Puck", style=MALE, lines=L(
    ("Tujuh ratus lima belas liter. Besar macam mana sebenarnya?", "*715L* besar macam mana?", "Rasmi 715_kitchen1"),
    ("Lebar sembilan puluh satu sentimeter, tinggi hampir dua meter. Freezer kiri, peti kanan.", "91 cm lebar · *190.5 cm* tinggi", "Rasmi 715_kitchen1 + grid"),
    ("Sebelah peti: rak, laci sayur dengan kawalan kelembapan, dan rak pintu untuk botol.", "Peti: rak · *laci sayur* · rak pintu", "Rasmi 715_kitchen_open"),
    ("Sebelah freezer: stok ayam, ikan dan daging, dengan super freezing sampai negatif dua puluh lima.", "Freezer · *−25°C*", "Rasmi 715_open_dark + LED"),
    PROMO_715,
    ("Hantar dan pasang percuma. Kalau ada ruang sebesar ni, apa benda pertama awak nak simpan? WhatsApp saya.", "Apa nak simpan dulu? *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@03", "navy"), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[photo(0, "@03", "715_kitchen1.jpg", top=380),
       banner("@01", "@02", "<em>715L</em> BESAR MACAM MANA?"),
       {"type": "grid", "in": "@02", "out": "@03", "top": 1160, "items": [{"big": "91", "small": "LEBAR (CM)", "at": "@02"},
                                                                       {"big": "190.5", "small": "TINGGI (CM)", "at": "@02%40"}]},
       banner("@03", "@04", "SEBELAH <em>PETI</em>"),
       photo("@03", "@04", "715_kitchen_open.jpg", top=380),
       {"type": "chips", "in": "@03%25", "out": "@04", "top": 1180, "items": [{"text": "RAK", "color": "#fff", "at": "@03%25"},
                                                                           {"text": "LACI SAYUR", "color": "#fff", "at": "@03%45"},
                                                                           {"text": "RAK PINTU", "color": YEL, "at": "@03%65"}]},
       banner("@04", "@05", "SEBELAH <em>FREEZER</em>"),
       photo("@04", "@05", "715_open_dark.jpg", top=330, w=900, h=706),
       {"type": "led", "in": "@04%40", "out": "@05", "top": 1080, "items": [{"num": "-25", "unit": "°C", "label": "SUPER FREEZING", "at": "@04%45"}]},
       price("@05", "@06", "RM84"), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA30 · 23 Humidity control (kat. 5)
V["PA30"] = dict(no="23", tajuk="Apa fungsi kawalan kelembapan dalam peti?", kat="5 Kenali produk", hook="Soalan",
  slug="fungsi-kawalan-kelembapan", voice="Zephyr", style=FEM, lines=L(
    ("Kenapa laci sayur ada kawalan kelembapan?", "Laci sayur ada *kawalan kelembapan?*", "Seedream s01_layu"),
    ("Sayur berdaun suka lembap. Ada buah pula lebih elok kalau kurang lembap.", "Sayur daun: *lembap* · buah: *kurang lembap*", "Cip"),
    ("Laci peti biasa, satu keadaan untuk semua. Sebab tu ada yang cepat layu, ada yang cepat lembik.", "Satu keadaan untuk *semua*", "Seedream s01_layu"),
    ("Peti ais Coway tujuh ratus lima belas liter ada kawalan kelembapan di laci, bantu sayur dan buah kekal segar lebih lama.",
     "715L · *Humidity Control*", "Rasmi 715_humidity, 715_humid_drawer"),
    PROMO_715,
    ("Hantar dan pasang percuma seluruh Malaysia. Nak tahu fungsi lain? WhatsApp saya.", "Hantar & pasang *percuma* · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("s01_layu")), ("@02", "blue"), ("@03", R("s01_layu")), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[banner("@01", "@02", "LACI SAYUR ADA<br><em>KAWALAN KELEMBAPAN?</em>"),
       {"type": "vs", "in": "@02", "out": "@03", "top": 420,
        "left": {"title": "SAYUR DAUN", "color": "#1faa59", "items": ["Suka lembap"], "at": "@02"},
        "right": {"title": "BUAH", "color": "#E86E5A", "items": ["Kurang lembap"], "at": "@02%50"}},
       pill("@03", "@04", "SATU KEADAAN UNTUK SEMUA", top=1180, bg=RED, color="#fff"),
       banner("@04", "@05", "COWAY <em>715L</em>"),
       photo("@04", "@04%55", "715_humidity.jpg", top=420, w=900, h=675),
       photo("@04%55", "@05", "715_humid_drawer.jpg", top=380),
       pill("@04%30", "@05", "HUMIDITY CONTROL", top=1180),
       price("@05", "@06", "RM84"), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA31 · 24 4 mod 715L (kat. 5, hype kinetic)
V["PA31"] = dict(no="24", tajuk="Smart, Eco, Power Cool, Super Freezing: apa beza?", kat="5 Kenali produk", hook="Listicle",
  slug="4-mod-peti-ais-715l", lines=L(
    ("Bukan semua mod peti ais buat kerja yang sama.", "*4 mod*, 4 kerja", "Kinetic"),
    ("Smart: laraskan suhu peti dan freezer, sendiri.", "*SMART*", "Rasmi 715_panel_touch"),
    ("Eco: guna tenaga dengan lebih cekap.", "*ECO*", "Kinetic"),
    ("Power Cool: sejukkan peti dengan cepat, contoh lepas borong.", "*POWER COOL*", "Kinetic"),
    ("Super Freezing: freezer turun sampai negatif dua puluh lima darjah.", "*SUPER FREEZING −25°C*", "Kinetic"),
    ("Peti ais Coway tujuh ratus lima belas liter. Promosi rebat: bayar dua puluh ringgit sebulan, tujuh bulan pertama. Lepas tu, lapan puluh empat.",
     "715L · bayar *RM20*/bulan · *7 bulan**", "Tag harga"),
    ("Hantar dan pasang percuma. WhatsApp saya sekarang.", "Hantar & pasang *percuma* · *WhatsApp saya*", "CTA")),
  spec={"voice": "Fenrir", "style_tts": MALE_HYPE, "player": "hype", "style": "kinetic", "bpm": 128, "brand": "coway", "cap": True},
  scenes=[(0, "k-ink"), ("@02", "k-white"), ("@03", "k-blue"), ("@04", "k-white"), ("@05", "k-ink"), ("@06", "k-blue"), ("@07", "k-white")],
  els=[W("@01", "@02", 420, ("BUKAN SEMUA MOD", "@01", 100, "#fff", BOX), ("SAMA.", "@01%40", 220, "#fff", BBOX)),
       {"type": "img", "in": "@02", "out": "@03", "src": F + "715_panel_touch.jpg", "w": 640, "top": 300, "anim": "rise"},
       W("@02", "@03", 1020, ("SMART", "@02", 200, BLUE, {"hit": True}), ("LARAS SENDIRI", "@02%40", 100, INK)),
       W("@03", "@04", 520, ("ECO", "@03", 300, "#fff", {"hit": True}), ("TENAGA LEBIH CEKAP", "@03%40", 90, "#fff", BOX)),
       W("@04", "@05", 520, ("POWER", "@04", 200, INK), ("COOL", "@04%20", 240, BLUE, {"hit": True}), ("SEJUK CEPAT", "@04%55", 100, "#fff", BBOX)),
       W("@05", "@06", 420, ("SUPER", "@05", 160, "#fff", BOX), ("FREEZING", "@05%20", 170, "#fff", BBOX), ("-25°C", "@05%50", 230, "#fff", {"hit": True})),
       {"type": "tag", "in": "@06", "out": "@07", "top": 700, "pre": "BAYAR", "big": "RM20", "sub": "SEBULAN · 7 BULAN PERTAMA*", "hit": True},
       W("@06%60", "@07", 1180, ("KEMUDIAN RM84", "@06%70", 90, "#fff", BOX)),
       W("@07", None, 330, ("HANTAR & PASANG", "@07", 100, INK), ("PERCUMA", "@07%20", 170, BLUE, {"hit": True})),
       {"type": "cta", "in": "@07", "top": 760, "button": "WhatsApp saya", "btnAt": "@07%40", "fine": FINE_P}])

# ---------------------------------------------------------------- PA32 · 26 Peti besar sesuai untuk siapa? (kat. 6)
V["PA32"] = dict(no="26", tajuk="Peti besar ni sesuai untuk siapa sebenarnya?", kat="6 Bantahan & conversion", hook="Ejen jujur",
  slug="peti-besar-sesuai-siapa", voice="Achird", style=MALE, lines=L(
    ("Saya tak akan cadang peti besar kepada semua orang.", "Peti besar *bukan untuk semua*", "Tajuk"),
    ("Kalau rumah dua orang, jarang masak, dan dapur sempit, peti besar cuma makan ruang.", "2 orang · jarang masak · dapur sempit → *tak perlu*", "VS"),
    ("Tapi kalau lima orang ke atas, borong seminggu sekali, dan selalu simpan stok, ruang tambahan memang membantu.",
     "5+ orang · borong · stok → *sesuai*", "Seedream pa09_a_keluarga"),
    ("Dan pastikan dapur muat. Tujuh ratus lima belas liter, lebar sembilan puluh satu, dalam tujuh puluh empat sentimeter.", "715L · *91 × 74 cm*", "Rasmi 715_kitchen1"),
    PROMO_715,
    ("Hantar dan pasang percuma. Beritahu saya berapa orang dalam rumah, dan ukuran ruang peti awak. WhatsApp saya.",
     "Berapa orang? Ukuran? *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@02", "blue"), ("@03", R("pa09_a_keluarga")), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[title("@01", "@02", "PETI BESAR<br>BUKAN UNTUK<br>SEMUA", top=480, size=120),
       {"type": "vs", "in": "@02", "out": "@03", "top": 420,
        "left": {"title": "TAK PERLU", "color": INK, "items": ["2 orang", "Jarang masak", "Dapur sempit"], "at": "@02"},
        "right": {"title": "SESUAI", "color": BLUE, "items": ["5+ orang", "Borong seminggu", "Simpan stok"], "at": "@02%55"}},
       *rban("@03", "@04", "✓", "5+ ORANG · BORONG · STOK", "RUANG TAMBAHAN MEMBANTU"),
       banner("@04", "@05", "PASTIKAN <em>MUAT</em>"),
       photo("@04", "@05", "715_kitchen1.jpg", top=380, w=520, h=520),
       {"type": "grid", "in": "@04%30", "out": "@05", "top": 940, "items": [{"big": "91", "small": "LEBAR (CM)", "at": "@04%35"},
                                                                         {"big": "74", "small": "DALAM (CM)", "at": "@04%60"}]},
       price("@05", "@06", "RM84"), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA33 · 28 "Takut tak muat" (kat. 6)
V["PA33"] = dict(no="28", tajuk="\"Saya berminat, tapi takut tak muat\"", kat="6 Bantahan & conversion", hook="Soalan bantahan",
  slug="takut-peti-tak-muat", voice="Laomedeia", style=FEM, lines=L(
    ("Saya berminat, tapi takut peti tak muat.", "\"Takut *tak muat*\"", "Gelembung chat"),
    ("Jangan risau. Kita semak ukuran dulu, sebelum hantar.", "Semak ukuran *dulu*", "Seedream pa10_b_ukur"),
    ("Ukur lebar, dalam dan tinggi ruang. Kemudian pintu rumah, pintu dapur dan lif.", "L · D · T · *laluan*", "Grid + cip"),
    ("Tujuh ratus lima belas liter, dalam tujuh puluh empat sentimeter. Lima ratus lima puluh satu liter lebih nipis, dalam enam puluh je.",
     "715L dalam *74 cm* · 551L dalam *59.7 cm*", "VS dua model"),
    PROMO_2,
    ("Penghantaran dan pemasangan percuma seluruh Malaysia. Hantar ukuran ruang dapur awak, saya semak dulu. WhatsApp saya.",
     "Hantar ukuran · *WhatsApp saya*", "CTA")),
  scenes=[(0, "blue"), ("@02", R("pa10_b_ukur")), ("@03", "blue"), ("@04", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[{"type": "chat", "in": "@01", "out": "@02", "top": 520, "items": [{"side": "L", "text": "Saya berminat, tapi takut peti tak muat 😟", "at": "@01"},
                                                                      {"side": "R", "text": "Jangan risau, kita semak ukuran dulu 👍", "at": "@01%80"}]},
       banner("@02", "@03", "SEMAK UKURAN <em>DULU</em>"),
       {"type": "grid", "in": "@03", "out": "@04", "top": 380, "items": [{"big": "L", "small": "LEBAR", "at": "@03"},
                                                                      {"big": "D", "small": "DALAM", "at": "@03%20"},
                                                                      {"big": "T", "small": "TINGGI", "at": "@03%40"}]},
       {"type": "chips", "in": "@03%55", "out": "@04", "top": 1000, "items": [{"text": "PINTU RUMAH", "color": "#fff", "at": "@03%55"},
                                                                           {"text": "PINTU DAPUR", "color": "#fff", "at": "@03%70"},
                                                                           {"text": "LIF", "color": YEL, "at": "@03%85"}]},
       {"type": "vs", "in": "@04", "out": "@05", "top": 420,
        "left": {"title": "715L", "color": BLUE, "items": ["Lebar 91 cm", "Dalam 74 cm", "Tinggi 190.5 cm"], "at": "@04"},
        "right": {"title": "551L", "color": NAVY, "items": ["Lebar 90.5 cm", "Dalam 59.7 cm", "Tinggi 190.2 cm"], "at": "@04%50"}},
       title("@05", "@06", "BAYAR<br>RM20", top=420, size=170, color="#ffffff"),
       pill("@05%30", "@06", "SEBULAN · 7 BULAN PERTAMA*", top=840),
       pill("@05%50", "@06", "KEMUDIAN 715L RM84 · 551L RM99", top=960), hantar("@05%70", "@06"),
       cta("@06")])

# ---------------------------------------------------------------- PA34 · 29 Jangan banding harga bulanan sahaja (kat. 6)
V["PA34"] = dict(no="29", tajuk="Jangan banding peti ais ikut harga bulanan sahaja", kat="6 Bantahan & conversion", hook="Angka / kira",
  slug="jangan-banding-bulanan-sahaja", voice="Algieba", style=MALE, lines=L(
    ("Beza sepuluh ringgit sebulan, bukan benda paling penting nak banding.", "Beza RM10? *Bukan paling penting*", "Seedream pa15_a_kira"),
    ("Banding juga: tempoh kontrak, jumlah bayaran, servis, waranti, dan pemasangan.", "Tempoh · jumlah · servis · waranti · *pasang*", "Steps"),
    ("Contoh, peti ais Coway tujuh ratus lima belas liter dengan promosi: tujuh bulan pertama dua puluh ringgit, lepas tu lapan puluh empat.",
     "7 bulan × *RM20*, kemudian *RM84*", "Kira"),
    ("Jumlah tujuh tahun, enam ribu enam ratus lapan ringgit.", "Jumlah 7 tahun *RM6,608**", "Counter"),
    ("Dalam tu, Cody servis berkala tujuh tahun, kompressor waranti sepuluh tahun, hantar dan pasang percuma.",
     "Cody *7 tahun* · kompressor *10 tahun** · pasang *percuma*", "Kad"),
    ("Itu yang patut dibanding. Nak checklist banding dua model? WhatsApp saya.", "Banding *keseluruhan* · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa15_a_kira")), ("@02", "blue"), ("@03", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[banner("@01", "@02", "BEZA RM10 SEBULAN?<br><em>BUKAN PALING PENTING</em>"),
       {"type": "steps", "in": "@02", "out": "@03", "top": 300, "items": [{"text": "TEMPOH KONTRAK", "at": "@02%10"},
                                                                       {"text": "JUMLAH BAYARAN", "at": "@02%28"},
                                                                       {"text": "SERVIS", "at": "@02%46"},
                                                                       {"text": "WARANTI", "at": "@02%62"},
                                                                       {"text": "PEMASANGAN", "at": "@02%78"}]},
       title("@03", "@04", "715L DENGAN PROMOSI", top=340, size=80),
       {"type": "grid", "in": "@03", "out": "@04", "top": 520, "items": [{"big": "RM20", "small": "× 7 BULAN", "at": "@03%35"},
                                                                      {"big": "RM84", "small": "× 77 BULAN", "at": "@03%70"}]},
       title("@04", "@05", "JUMLAH 7 TAHUN", top=360, size=90),
       {"type": "counter", "in": "@04", "out": "@05", "top": 540, "from": 0, "to": 6608, "prefix": "RM", "decimals": 0, "dur": 0.9, "size": 220},
       pill("@04%60", "@05", "7 × RM20 + 77 × RM84 = RM6,608*", top=880),
       card("@05", "@06", "tech", "CODY 7 TAHUN", "Servis berkala", top=380),
       card("@05%30", "@06", "shield", "KOMPRESSOR 10 TAHUN", "Waranti kompressor*", top=620),
       card("@05%60", "@06", "home", "HANTAR & PASANG", "Percuma seluruh Malaysia", top=860),
       cta("@06", fine=FINE_PW + " Jumlah 7 tahun 715L dengan promosi: RM6,608.")])

# ---------------------------------------------------------------- PA35 · 30 551L atau 715L? 3 soalan (kat. 6)
V["PA35"] = dict(no="30", tajuk="Peti ais Coway mana sesuai: 551L atau 715L?", kat="6 Bantahan & conversion", hook="Kuiz",
  slug="551l-atau-715l-3-soalan", voice="Vindemiatrix", style=FEM, lines=L(
    ("Sebelum pilih peti ais Coway, jawab tiga soalan ni.", "Jawab *3 soalan* ni", "Tajuk"),
    ("Berapa orang dalam rumah? Berapa banyak stok yang awak simpan? Dan berapa dalam ruang dapur?", "Orang · stok · *ruang*", "Cip"),
    ("Suka tersusun ikut kategori, ruang tak berapa dalam: lima ratus lima puluh satu liter, empat pintu.", "551L · tersusun · dalam *59.7 cm*", "Rasmi 551_open_food"),
    ("Keluarga besar, stok banyak, ruang cukup dalam: tujuh ratus lima belas liter, side-by-side.", "715L · stok banyak · dalam *74 cm*", "Rasmi 715_spaces"),
    PROMO_2,
    ("Lepas tu lapan puluh empat atau sembilan puluh sembilan. Hantar dan pasang percuma. WhatsApp saya, saya bantu pilih.",
     "Kemudian *RM84* / *RM99* · *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@02", "blue"), ("@03", "navy"), ("@05", "blue"), ("@06", "blue")],
  els=[title("@01", "@02", "JAWAB<br>3 SOALAN", top=520, size=170),
       {"type": "chips", "in": "@02", "out": "@03", "top": 600, "items": [{"text": "BERAPA ORANG?", "color": "#fff", "at": "@02"},
                                                                       {"text": "BERAPA STOK?", "color": "#fff", "at": "@02%35"},
                                                                       {"text": "BERAPA DALAM RUANG?", "color": YEL, "at": "@02%65"}]},
       banner("@03", "@04", "<em>551L</em> · 4 PINTU"),
       photo("@03", "@04", "551_open_food.jpg", top=380),
       pill("@03%40", "@04", "TERSUSUN · DALAM 59.7 CM", top=1180),
       banner("@04", "@05", "<em>715L</em> · SIDE-BY-SIDE"),
       photo("@04", "@05", "715_spaces.jpg", top=380),
       pill("@04%40", "@05", "STOK BANYAK · DALAM 74 CM", top=1180),
       title("@05", "@06", "DUA MODEL<br>BAYAR RM20", top=420, size=130, color="#ffffff"),
       pill("@05%30", "@06", "SEBULAN · 7 BULAN PERTAMA*", top=840),
       hantar("@05%60", "@06", top=1080),
       cta("@06")])


def skrip_md():
    rows, body = [], []
    for vid, v in V.items():
        voice = (v.get("spec") or v)["voice"]
        fmt = (v.get("spec") or {}).get("style") or "scenes"
        words = sum(len(l["text"].split()) for l in v["lines"])
        rows.append(f"| {vid} ({v['no']}) | {v['lines'][0]['text']} | {v['kat']} | {v['hook']} | {voice} | {fmt} | ±{words / 2.4:.0f} |")
        body.append(f"### {vid} · {v['tajuk']}\nVideo pelan: {v['no']} · Kategori: {v['kat']} · Persona: P2 · Suara: {voice} · Format: {fmt}\n\n"
                    "| # | VO | Kapsyen | Visual |\n|---|---|---|---|\n" +
                    "\n".join(f"| {l['id']} | {l['text']} | {l['cap']} | {l['_vis']} |" for l in v["lines"]) + "\n")
    return ("\n\n---\n\n# Batch 3 (PA26–PA35)\n\n"
            "Status: **DILULUSKAN 30 Okt 2026** (user: \"sambung batch 3\" + promo; batch 2 dianggap lulus)\n"
            "Promo (user, 30 Okt 2026): rebat, bayar RM20 sebulan untuk 7 bulan pertama, kemudian RM84 (715L) / RM99 (551L); "
            "penghantaran & pemasangan percuma seluruh Malaysia; tiada tarikh tamat (\"promosi terhad\").\n"
            "Dijana daripada `videos/peti-ais-p2-01_b3.py`. Shot hidup s18–s20: Google Flow, prompt dalam `shots.md`.\n\n"
            f"Nota kaki CTA: {FINE_P.replace('&amp;', '&')}\n\n"
            "| ID (pelan) | Hook | Kategori | Jenis hook | Suara | Format | ±saat |\n|---|---|---|---|---|---|---|\n" + "\n".join(rows) +
            "\n\n---\n\n" + "\n".join(body))


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        lines = [{k: x for k, x in l.items() if not k.startswith("_")} for l in v["lines"]]
        (d / "lines.json").write_text(json.dumps(lines, ensure_ascii=False, indent=1))
        seg = times(vid)
        starts = [at_sec(a, seg) if seg else None for a, _ in v["scenes"]]
        end = max(b for _, b in seg.values()) + 2.5 if seg else None
        scenes = [{"at": a, "bg": resolve(bg, starts[i], starts[i + 1] if i + 1 < len(starts) else end, vid)}
                  for i, (a, bg) in enumerate(v["scenes"])]
        head = v.get("spec") or {"voice": v["voice"], "style": v["style"]}
        spec = {"slug": v["slug"], **head, "scenes": scenes, "els": v["els"], **({} if v.get("spec") else BRAND)}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in lines)
        clips = sum(1 for s in scenes if "clip" in s["bg"])
        print(f"{vid} {v['slug']:34s} {head['voice']:12s} {len(lines):2d} baris, {words} perkataan (~{words / 2.4:.0f}s), klip Flow {clips}")
    sk = ROOT / "projek" / KOD / "skrip.md"
    txt = sk.read_text().split("\n\n---\n\n# Batch 3 (PA26–PA35)")[0].rstrip("\n")
    sk.write_text(txt + "\n" + skrip_md())
