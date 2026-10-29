"""Peti ais Coway, pakej video untuk ejen (projek/peti-ais-p2-01), batch 1: PA06-PA15
-> videos/PA06..PA15/{lines.json, spec.json} dan projek/peti-ais-p2-01/skrip.md.

    python3 videos/peti-ais-p2-01_batch.py
    python3 videos/build_video.py PA06 --tts
    python3 videos/build_video.py PA06 --render --review out/peti-ais-p2-01

Brief: projek/peti-ais-p2-01/brief.md (pelan 30 video, 6 kategori; batch 1 = video 01, 05, 08, 11, 13, 14, 16, 20, 25, 27).
Harga rasmi tanpa promo (keputusan user 25/10): 715L HEART 7+0 RM84, 551L RM99, tunai RM5,899 / RM6,799.
Waranti kompressor 10 tahun: coway.com.my/warranty-policy. Tips: TNB (isi 2/3, getah pintu), SEDA (ruang belakang untuk haba).
Gambar situasi: Seedream (assets/img/peti-ais-p2-01/, prompts.json). Produk: gambar rasmi assets/img/coway_fridge/.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
KOD = "peti-ais-p2-01"
F = "../../assets/img/coway_fridge/"
NAVY, YEL, BLUE, RED, INK = "#0B2F6B", "#ffd23f", "#04A4E4", "#E5322D", "#2f3337"
BRAND = {"theme": "coway", "brand": "COWAY"}

FEM = "Say in Malaysian Malay, as a warm, friendly young woman sharing a useful tip on TikTok, relaxed, clear and fairly quick"
FEM_STORY = "Say in Malaysian Malay, as a tired but sincere mother telling her own story, soft, warm and natural, not too slow"
MALE = "Say in Malaysian Malay, as a calm, confident Coway agent explaining clearly to a friend, honest and friendly"
MALE_STORY = "Say in Malaysian Malay, as a sincere father telling a frustrating experience, quiet and heartfelt, natural pace"
MALE_HYPE = "Say in Malaysian Malay, as an energetic, punchy young man on TikTok, fast, bold and confident"

FINE = "*Harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Tertakluk terma &amp; syarat Coway."
FINE_W = FINE + " Waranti kompressor 10 tahun tertakluk polisi waranti Coway."
FINE_551 = "*551L: harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Tertakluk terma &amp; syarat Coway."
TICKS = ["715L DARI RM84/BULAN*", "551L DARI RM99/BULAN*", "SERVIS HEART 7 TAHUN"]
TICKS_W = ["PETI AIS COWAY DARI RM84/BULAN*", "KOMPRESSOR WARANTI 10 TAHUN*", "CODY SERVIS 7 TAHUN"]


def L(*rows):
    """baris: (VO, kapsyen, visual untuk skrip.md)"""
    return [{"id": f"{i + 1:02d}", "text": t, "cap": c, "_vis": v} for i, (t, c, v) in enumerate(rows)]


def R(name, color="navy"):
    """Gambar Seedream sebagai latar penuh, tepi digelapkan."""
    return {"image": f"{KOD}/{name}.jpg", "color": color, "shade": True}


def banner(a, o, html, top=230):
    return {"type": "banner", "in": a, "out": o, "top": top, "html": html}


def title(a, o, html, top=700, size=130, **kw):
    return {"type": "title", "in": a, "out": o, "top": top, "size": size, "html": html, **kw}


def pill(a, o, html, top=900, bg="var(--yellow)", color="var(--navy)"):
    return {"type": "pill", "in": a, "out": o, "top": top, "html": html, "bg": bg, "color": color}


def photo(a, o, src, top=420, w=760, h=760, **kw):
    return {"type": "photo", "in": a, "out": o, "top": top, "left": (1080 - w) // 2, "w": w, "h": h, "src": F + src, **kw}


def reason(a, o, num, t, sub=None, top=1080):
    return {"type": "reason", "in": a, "out": o, "top": top, "num": num, "title": t, **({"sub": sub} if sub else {})}


def rban(a, o, num, t, sub=None):
    """Nombor + tajuk untuk babak berlatar foto: banner putih (reason tak terbaca atas foto)."""
    return [banner(a, o, f"<em>{num}</em> · {t}"), *([pill(a.replace("@", "@") + "%25" if "%" not in a else a, o, sub, top=1180,
            bg="rgba(0,0,0,.6)", color="#fff")] if sub else [])]


def card(a, o, icon, t, sub, top=1120):
    return {"type": "card", "in": a, "out": o, "top": top, "icon": icon, "title": t, "sub": sub}


def stamp(a, o, html, top=1000, color=None, rot=-6):
    return {"type": "stamp", "in": a, "out": o, "top": top, "html": html, "rot": rot, **({"color": color} if color else {})}


def cta(a, ticks=TICKS, fine=FINE, top=760, btn=None):
    return {"type": "cta", "in": a, "top": top, "ticks": ticks, "button": "WhatsApp saya",
            "btnAt": btn or a.replace("@", "@") + "%40", "fine": fine}


def lakonan(o="@02"):
    return pill(0, o, "LAKONAN SEMULA", top=150, bg="rgba(0,0,0,.55)", color="#fff")


def W(a, o, top, *items):
    """hype words: item = (txt, at, size, color, extra)"""
    return {"type": "words", "in": a, "out": o, "top": top,
            "items": [{"txt": t, "at": at, "size": z, "color": c, **(x[0] if x else {})} for t, at, z, c, *x in items]}


BOX = {"box": True, "bg": "#111"}
BBOX = {"box": True, "bg": BLUE, "hit": True}

V = {}

# ---------------------------------------------------------------- PA06 · 01 Peti besar, kenapa tak cukup ruang? (kat. 1)
V["PA06"] = dict(no="01", tajuk="Peti besar, kenapa masih tak cukup ruang?", kat="1 Masalah harian", hook="Seru situasi",
  slug="peti-besar-tak-cukup-ruang", voice="Aoede", style=FEM, lines=L(
    ("Baru balik beli barang dapur, buka peti ais, dah tak ada ruang?", "Buka peti… *dah tak ada ruang?*", "Seedream: ibu bertudung pegang beg barang, peti lama sesak"),
    ("Ramai terus salahkan saiz peti. Padahal, selalunya ada tiga punca lain.", "Bukan saiz je. Ada *3 punca lain.*", "Peti sesak; tajuk '3 PUNCA'"),
    ("Satu, bekas terlalu besar. Separuh isi dia, angin je.", "1 · Bekas *terlalu besar*", "Seedream: bekas besar separuh kosong"),
    ("Dua, tiada zon. Ayam, sayur, air kotak, semua bercampur atas satu rak.", "2 · *Tiada zon*", "Seedream: rak bercampur"),
    ("Tiga, sumbat sampai penuh. Isi dua pertiga je, supaya angin sejuk boleh bergerak.", "3 · Isi ± *2/3 sahaja*", "Grafik pengisian 2/3 (tip TNB)"),
    ("Dah susun, tapi masih tak muat? Barulah masalah dia, saiz.", "Masih tak muat? *Barulah saiz.*", "Cop 'BARU SAIZ'"),
    ("Masa tu, peti ais Coway lima ratus lima puluh satu liter ni ada empat pintu, dan satu zon boleh tukar sejuk atau beku, ikut keperluan.",
     "Coway *551L*: 4 pintu, *Convertible Zone*", "Rasmi 551_open_food, 551_drawers"),
    ("Dari sembilan puluh sembilan ringgit sebulan. Punca yang mana satu? Komen, atau WhatsApp saya.", "551L dari *RM99*/bulan · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa06_a_penuh")), ("@03", R("pa06_b_bekas")), ("@04", R("pa06_c_campur")), ("@05", "blue"), ("@07", "navy"), ("@08", "blue")],
  els=[banner("@01", "@02", "BUKA PETI…<br><em>DAH TAK ADA RUANG?</em>"),
       title("@02", "@03", "BUKAN SAIZ JE", top=560, size=110, color="#ffffff"),
       pill("@02%45", "@03", "ADA 3 PUNCA LAIN", top=760),
       *rban("@03", "@04", "1", "BEKAS TERLALU BESAR", "SEPARUH ISI, ANGIN JE"),
       *rban("@04", "@05", "2", "TIADA ZON", "SEMUA BERCAMPUR SATU RAK"),
       reason("@05", "@06", "3", "SUMBAT SAMPAI PENUH", "angin sejuk tak boleh bergerak", top=300),
       {"type": "counter", "in": "@05%30", "out": "@06", "top": 640, "from": 0, "to": 2, "suffix": "/3", "decimals": 0, "dur": 0.6, "size": 300},
       pill("@05%55", "@06", "ISI ± 2/3 SAHAJA", top=1000),
       title("@06", "@07", "MASIH TAK MUAT?", top=520, size=110),
       stamp("@06%50", "@07", "BARU MASALAH SAIZ", top=820),
       banner("@07", "@08", "COWAY <em>551L</em> · 4 PINTU"),
       photo("@07", "@07%55", "551_open_food.jpg", top=400),
       photo("@07%55", "@08", "551_drawers.jpg", top=400),
       pill("@07%55", "@08", "CONVERTIBLE ZONE: SEJUK ↔ BEKU", top=1200),
       cta("@08", ticks=["551L DARI RM99/BULAN*", "4 PINTU · CONVERTIBLE ZONE", "SERVIS HEART 7 TAHUN"], fine=FINE_551)])

# ---------------------------------------------------------------- PA07 · 05 5 tanda peti nazak (kat. 1)
V["PA07"] = dict(no="05", tajuk="5 tanda peti ais lama dah nazak", kat="1 Masalah harian", hook="Listicle",
  slug="5-tanda-peti-ais-nazak", voice="Orus", style=MALE, lines=L(
    ("Jangan tunggu peti ais mati, masa stok tengah penuh. Ni lima tanda dia dah nazak.", "*5 tanda* peti ais dah nazak", "Seedream: peti lama di dapur malam"),
    ("Satu. Getah pintu dah koyak, atau pintu kena tolak kuat, baru rapat.", "1 · Getah pintu *koyak*", "Seedream: getah pintu koyak"),
    ("Dua. Freezer penuh ais tebal. Bukan penuh lauk.", "2 · Ais *tebal* dalam freezer", "Seedream: freezer berais tebal"),
    ("Tiga. Atas sejuk, bawah tak sejuk. Sejuk dah tak sekata.", "3 · Sejuk *tak sekata*", "Grafik termometer atas/bawah"),
    ("Empat. Malam-malam berbunyi kuat, macam dah penat.", "4 · Bunyi *kuat* waktu malam", "Peti lama malam"),
    ("Lima. Dah repair, tapi rosak balik.", "5 · Repair, *rosak balik*", "Seedream: technician"),
    ("Kalau peti awak ada tiga daripada lima, mula survey sekarang, sebelum lauk seminggu yang jadi mangsa.", "3 daripada 5? *Mula survey.*", "Kiraan 3/5"),
    ("Peti ais Coway, kompressor dia waranti sepuluh tahun, dari lapan puluh empat ringgit sebulan.", "Kompressor waranti *10 tahun** · dari *RM84*/bulan", "Rasmi 715_kitchen1"),
    ("Peti ais awak dah berapa tahun? WhatsApp saya, saya bantu semak.", "Dah berapa tahun? *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa07_a_nazak")), ("@02", R("pa07_b_getah")), ("@03", R("pa07_c_ais")), ("@04", "navy"), ("@05", R("pa07_a_nazak", "night")),
          ("@06", R("pa11_a_repair")), ("@07", "navy"), ("@08", "blue"), ("@09", "blue")],
  els=[banner("@01", "@02", "<em>5 TANDA</em><br>PETI AIS DAH NAZAK"),
       *rban("@02", "@03", "1", "GETAH PINTU KOYAK", "TOLAK KUAT BARU RAPAT"),
       *rban("@03", "@04", "2", "AIS TEBAL", "PENUH AIS, BUKAN LAUK"),
       reason("@04", "@05", "3", "SEJUK TAK SEKATA", "atas sejuk, bawah tak", top=300),
       {"type": "led", "in": "@04%20", "out": "@05", "top": 640, "items": [{"num": "3", "unit": "°C", "label": "ATAS", "at": "@04%25"},
                                                                         {"num": "14", "unit": "°C", "label": "BAWAH", "at": "@04%60"}]},
       *rban("@05", "@06", "4", "BUNYI KUAT MALAM", "MACAM DAH PENAT"),
       *rban("@06", "@07", "5", "REPAIR, ROSAK BALIK", "DUIT KELUAR LAGI"),
       title("@07", "@08", "3 DARIPADA 5?", top=520, size=150),
       pill("@07%40", "@08", "MULA SURVEY SEKARANG", top=800),
       banner("@08", "@09", "PETI AIS <em>COWAY</em>"),
       photo("@08", "@09", "715_kitchen1.jpg", top=400),
       pill("@08%30", "@09", "KOMPRESSOR WARANTI 10 TAHUN*", top=1200),
       cta("@09", ticks=TICKS_W, fine=FINE_W)])

# ---------------------------------------------------------------- PA08 · 08 Getah pintu: ujian kertas (kat. 2, hype ugc)
V["PA08"] = dict(no="08", tajuk="Getah pintu: ujian kertas", kat="2 Tips", hook="Arahan / tips",
  slug="ujian-kertas-getah-pintu", lines=L(
    ("Ambil sehelai kertas. Selit kat pintu peti ais, tutup, kemudian tarik.", "Selit *kertas*. Tutup. *Tarik.*", "Seedream: tangan selit kertas"),
    ("Kalau kertas tu keluar senang je, maknanya getah pintu dah tak rapat.", "Keluar senang? Getah *tak rapat*", "Teks besar"),
    ("Angin sejuk terlepas, peti kena kerja lebih kuat, dan lauk pun tak sejuk macam sepatutnya.", "Angin sejuk *terlepas*", "Teks + latar kertas"),
    ("Cuba kat beberapa tempat. Atas, bawah, dan tepi pintu.", "Cuba *atas, bawah, tepi*", "Teks 3 lokasi"),
    ("Kalau kotor, lap dengan kain lembap. Kalau dah koyak atau keras, itu tanda nak tukar.", "Kotor → *lap*. Koyak → *tukar*.", "Seedream: lap getah; getah koyak"),
    ("Simpan video ni, dan pergi check peti ais rumah awak sekarang.", "*Simpan* & check sekarang", "Teks"),
    ("Kalau peti dah tua dan banyak sangat masalah, peti ais Coway dari lapan puluh empat ringgit sebulan, Cody datang servis berkala. WhatsApp saya.",
     "Peti ais Coway dari *RM84*/bulan · *WhatsApp saya*", "Rasmi 715_kitchen2 + CTA")),
  spec={"voice": "Kore", "style_tts": FEM, "player": "hype", "style": "ugc", "bpm": 110, "brand": "coway", "cap": True},
  scenes=[(0, R("pa08_a_kertas", "ugc-white")), ("@02", "ugc-blue"), ("@03", R("pa08_a_kertas", "ugc-white")), ("@04", "ugc-white"),
          ("@05", R("pa08_b_lap", "ugc-white")), ("@05%60", R("pa07_b_getah", "ugc-white")), ("@06", "ugc-blue"), ("@07", "ugc-white")],
  els=[W("@01", "@02", 230, ("UJIAN", "@01", 120, "#fff", BOX), ("KERTAS", "@01%25", 170, "#fff", BBOX)),
       W("@01%35", "@02", 1180, ("SELIT", "@01%35", 110, "#fff", BOX), ("TUTUP", "@01%60", 110, "#fff", BOX), ("TARIK!", "@01%80", 140, "#fff", BBOX)),
       W("@02", "@03", 520, ("KELUAR", "@02", 150, INK), ("SENANG?", "@02%20", 190, BLUE, {"hit": True}),
         ("GETAH TAK RAPAT", "@02%55", 110, "#fff", {"box": True, "bg": RED, "hit": True})),
       W("@03", "@04", 230, ("ANGIN SEJUK", "@03", 120, "#fff", BOX), ("TERLEPAS!", "@03%20", 170, "#fff", {"box": True, "bg": RED, "hit": True})),
       W("@04", "@05", 420, ("CUBA DI", "@04", 120, INK), ("ATAS", "@04%25", 170, BLUE, {"hit": True}),
         ("BAWAH", "@04%50", 170, BLUE, {"hit": True}), ("TEPI", "@04%72", 170, BLUE, {"hit": True})),
       W("@05", "@05%60", 230, ("KOTOR?", "@05", 130, "#fff", BOX), ("LAP KAIN LEMBAP", "@05%20", 110, "#fff", BBOX)),
       W("@05%60", "@06", 230, ("KOYAK / KERAS?", "@05%60", 120, "#fff", BOX), ("TUKAR", "@05%75", 190, "#fff", {"box": True, "bg": RED, "hit": True})),
       W("@06", "@07", 520, ("SIMPAN", "@06", 200, "#fff", {"hit": True}), ("VIDEO NI", "@06%25", 130, "#fff"), ("CHECK SEKARANG!", "@06%55", 110, INK, {"box": True, "bg": YEL})),
       {"type": "img", "in": "@07", "out": "@07%50", "src": F + "715_kitchen2.jpg", "w": 760, "top": 330, "anim": "rise"},
       W("@07", "@07%50", 1180, ("PETI AIS COWAY", "@07", 100, "#fff", BBOX)),
       {"type": "cta", "in": "@07%50", "top": 760, "button": "WhatsApp saya", "btnAt": "@07%70",
        "fine": "*Peti ais Coway 715L, harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Tertakluk terma &amp; syarat Coway."},
       W("@07%50", None, 420, ("DARI RM84", "@07%50", 150, BLUE, {"hit": True}), ("SEBULAN*", "@07%55", 100, INK))])

# ---------------------------------------------------------------- PA09 · 11 Berapa liter sesuai? (kat. 3)
V["PA09"] = dict(no="11", tajuk="Berapa liter peti ais sesuai untuk keluarga awak?", kat="3 Panduan memilih", hook="Soalan / kuiz",
  slug="berapa-liter-peti-ais-sesuai", voice="Laomedeia", style=FEM, lines=L(
    ("Jangan pilih saiz peti ais ikut rupa. Jawab tiga soalan ni dulu.", "Pilih liter? *Jawab 3 soalan* dulu", "Seedream: keluarga punggah barang dapur"),
    ("Satu. Berapa orang dalam rumah?", "1 · Berapa *orang*?", "Ikon rumah"),
    ("Dua. Awak beli barang dapur setiap hari, atau borong seminggu sekali?", "2 · Harian atau *borong*?", "Cip HARIAN / BORONG"),
    ("Tiga. Selalu simpan stok? Daging korban, kuih raya?", "3 · Simpan *stok*?", "Cip stok"),
    ("Empat hingga enam orang, suka barang tersusun, peti empat pintu lima ratus lima puluh satu liter, cukup selesa.",
     "4–6 orang, suka tersusun → *551L, 4 pintu*", "Rasmi 551_open_food"),
    ("Keluarga besar, freezer selalu penuh stok, pergi tujuh ratus lima belas liter.", "Keluarga besar, stok banyak → *715L*", "Rasmi 715_spaces"),
    ("Tapi ukur dapur dulu. Tujuh ratus lima belas liter tu, lebar sembilan puluh satu sentimeter.", "Ukur dapur: 715L lebar *91 cm*", "Ikon pembaris"),
    ("Rumah awak berapa orang? WhatsApp saya, saya bantu pilih.", "Berapa orang? *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa09_a_keluarga")), ("@02", "blue"), ("@05", "navy"), ("@07", "blue"), ("@08", "blue")],
  els=[banner("@01", "@02", "PILIH LITER?<br><em>JAWAB 3 SOALAN</em>"),
       reason("@02", "@03", "1", "BERAPA ORANG?", "dalam rumah", top=300),
       {"type": "icon", "in": "@02", "out": "@03", "top": 620, "icon": "home", "size": 300},
       reason("@03", "@04", "2", "HARIAN ATAU BORONG?", top=300),
       {"type": "chips", "in": "@03", "out": "@04", "top": 700, "items": [{"text": "SETIAP HARI", "color": "#fff", "at": "@03%30"},
                                                                       {"text": "SEMINGGU SEKALI", "color": YEL, "at": "@03%60"}]},
       reason("@04", "@05", "3", "SIMPAN STOK?", top=300),
       {"type": "chips", "in": "@04", "out": "@05", "top": 700, "items": [{"text": "DAGING KORBAN", "color": "#fff", "at": "@04%30"},
                                                                       {"text": "KUIH RAYA", "color": "#fff", "at": "@04%50"}]},
       banner("@05", "@06", "4–6 ORANG · TERSUSUN"),
       photo("@05", "@06", "551_open_food.jpg", top=400),
       pill("@05%50", "@06", "551L · 4 PINTU", top=1200),
       banner("@06", "@07", "KELUARGA BESAR · STOK BANYAK"),
       photo("@06", "@07", "715_spaces.jpg", top=400),
       pill("@06%40", "@07", "715L", top=1200),
       title("@07", "@08", "UKUR DAPUR DULU", top=380, size=100),
       {"type": "icon", "in": "@07", "out": "@08", "top": 600, "icon": "ruler", "size": 260},
       pill("@07%45", "@08", "715L · LEBAR 91 CM", top=960),
       cta("@08")])

# ---------------------------------------------------------------- PA10 · 13 3 ukuran wajib (kat. 3)
V["PA10"] = dict(no="13", tajuk="3 ukuran wajib sebelum beli peti ais", kat="3 Panduan memilih", hook="Cerita pertama",
  slug="3-ukuran-wajib-sebelum-beli", voice="Zephyr", style=FEM, lines=L(
    ("Peti ais dah sampai depan rumah. Tapi tak lepas pintu dapur. Naya.", "Peti dah sampai… *tak lepas pintu.*", "Seedream: penghantar tersangkat di pintu dapur"),
    ("Sebelum beli, ukur tiga benda ni.", "Ukur *3 benda* ni", "Seedream: wanita ukur ruang"),
    ("Satu, lebar. Dua, dalam, dari dinding ke depan kabinet. Tiga, tinggi, kalau ada kabinet atas.", "Lebar · Dalam · *Tinggi*", "Grid L/D/T"),
    ("Lepas tu, ukur laluan. Pintu rumah, pintu dapur, selekoh, dan lif.", "Ukur *laluan*: pintu, selekoh, lif", "Cip laluan"),
    ("Dan tinggalkan ruang sikit di belakang dan tepi, supaya haba boleh keluar.", "Ruang di *belakang* untuk haba", "Ikon"),
    ("Untuk rujukan, Coway tujuh ratus lima belas liter, lebar sembilan puluh satu, dalam tujuh puluh empat, tinggi seratus sembilan puluh sentimeter.",
     "715L: *91 × 74 × 190.5 cm*", "Rasmi 715_kitchen1 + grid"),
    ("Yang lima ratus lima puluh satu liter lebih nipis, dalam dia kurang enam puluh sentimeter je.", "551L: *90.5 × 59.7 × 190.2 cm*", "Rasmi 551_front + grid"),
    ("Hantar ukuran dapur awak kat WhatsApp saya. Saya semak model mana yang muat.", "Hantar ukuran · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa10_a_tak_lepas")), ("@02", R("pa10_b_ukur")), ("@03", "blue"), ("@06", "navy"), ("@08", "blue")],
  els=[lakonan(),
       banner("@01", "@02", "PETI DAH SAMPAI…<br><em>TAK LEPAS PINTU</em>"),
       title("@02", "@03", "UKUR 3 BENDA", top=1000, size=120, color="#ffffff"),
       {"type": "grid", "in": "@03", "out": "@04", "top": 420, "items": [{"big": "L", "small": "LEBAR", "at": "@03"},
                                                                       {"big": "D", "small": "DALAM", "at": "@03%30"},
                                                                       {"big": "T", "small": "TINGGI", "at": "@03%65"}]},
       title("@04", "@05", "UKUR LALUAN", top=300, size=110),
       {"type": "chips", "in": "@04", "out": "@05", "top": 620, "items": [{"text": "PINTU RUMAH", "color": "#fff", "at": "@04%20"},
                                                                       {"text": "PINTU DAPUR", "color": "#fff", "at": "@04%40"},
                                                                       {"text": "SELEKOH", "color": "#fff", "at": "@04%60"},
                                                                       {"text": "LIF", "color": YEL, "at": "@04%80"}]},
       title("@05", "@06", "BERI RUANG<br>DI BELAKANG", top=380, size=110),
       pill("@05%40", "@06", "SUPAYA HABA BOLEH KELUAR", top=760),
       banner("@06", "@07", "COWAY <em>715L</em>"),
       photo("@06", "@07", "715_kitchen1.jpg", top=360, w=520, h=520),
       {"type": "grid", "in": "@06%25", "out": "@07", "top": 920, "items": [{"big": "91", "small": "LEBAR (CM)", "at": "@06%25"},
                                                                          {"big": "74", "small": "DALAM (CM)", "at": "@06%50"},
                                                                          {"big": "190.5", "small": "TINGGI (CM)", "at": "@06%75"}]},
       banner("@07", "@08", "COWAY <em>551L</em>"),
       photo("@07", "@08", "551_front.jpg", top=360, w=520, h=520),
       {"type": "grid", "in": "@07%20", "out": "@08", "top": 920, "items": [{"big": "90.5", "small": "LEBAR (CM)", "at": "@07%20"},
                                                                          {"big": "59.7", "small": "DALAM (CM)", "at": "@07%45"},
                                                                          {"big": "190.2", "small": "TINGGI (CM)", "at": "@07%70"}]},
       cta("@08", ticks=["HANTAR UKURAN DAPUR", "SAYA SEMAK MODEL YANG MUAT", "715L DARI RM84/BULAN*"],
           fine="*Harga sewa bulanan 715L pelan HEART Service 7 tahun (7+0), termasuk SST. 551L dari RM99. Tertakluk terma &amp; syarat Coway.")])

# ---------------------------------------------------------------- PA11 · 14 Kompressor rosak: baiki atau ganti? (kat. 3)
V["PA11"] = dict(no="14", tajuk="Kompressor rosak: baiki atau ganti?", kat="3 Panduan memilih", hook="Angka / kira",
  slug="kompressor-rosak-baiki-atau-ganti", voice="Achird", style=MALE, lines=L(
    ("Kompressor dua ratus lima puluh. Upah gas seratus lima puluh. Baiki, atau beli baru?", "Kompressor *RM250* + gas *RM150*. Baiki atau ganti?", "Seedream: technician belakang peti lama"),
    ("Ada yang kena tunggu alat ganti, dua tiga bulan.", "Tunggu alat ganti *2–3 bulan*", "Seedream: resit repair"),
    ("Macam mana nak decide? Tiga soalan.", "Macam mana nak *decide*?", "Tajuk"),
    ("Satu. Peti ni dah berapa tahun?", "1 · Dah berapa *tahun*?", "Kad"),
    ("Dua. Ini kali pertama rosak, atau dah berulang?", "2 · Rosak *berulang*?", "Kad"),
    ("Tiga. Kos repair dah hampir separuh harga peti baru?", "3 · Kos repair ≈ *separuh harga baru*?", "Kad"),
    ("Peti muda, baru sekali rosak, baiki. Dah tua, berulang, dan mahal, ramai pilih ganti.",
     "Tua + berulang + mahal → *ganti*", "VS: BAIKI / GANTI"),
    ("Kalau ganti, tengok waranti. Peti ais Coway, kompressor waranti sepuluh tahun, Cody datang servis berkala.",
     "Coway: kompressor waranti *10 tahun**", "Rasmi 551_inv_comp, hs_step1"),
    ("Dari lapan puluh empat ringgit sebulan. WhatsApp saya.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa11_a_repair")), ("@02", R("pa11_b_resit")), ("@03", "navy"), ("@07", "navy"), ("@08", "blue"), ("@09", "blue")],
  els=[banner("@01", "@02", "BAIKI<br><em>ATAU GANTI?</em>"),
       {"type": "chips", "in": "@01", "out": "@02", "top": 1040, "items": [{"text": "KOMPRESSOR RM250", "color": "#fff", "at": "@01"},
                                                                         {"text": "GAS RM150", "color": YEL, "at": "@01%30"}]},
       pill("@02", "@03", "TUNGGU ALAT GANTI 2–3 BULAN", top=1040, bg=RED, color="#fff"),
       title("@03", "@04", "MACAM MANA<br>NAK DECIDE?", top=560, size=120),
       reason("@04", "@05", "1", "DAH BERAPA TAHUN?", top=600),
       reason("@05", "@06", "2", "ROSAK BERULANG?", top=600),
       reason("@06", "@07", "3", "KOS REPAIR TINGGI?", "hampir separuh harga peti baru", top=600),
       {"type": "vs", "in": "@07", "out": "@08", "top": 420,
        "left": {"title": "BAIKI", "color": "#1faa59", "items": ["Peti masih muda", "Kali pertama rosak", "Kos rendah"], "at": "@07"},
        "right": {"title": "GANTI", "color": RED, "items": ["Peti dah tua", "Rosak berulang", "Kos tinggi"], "at": "@07%40"}},
       banner("@08", "@09", "KALAU GANTI, TENGOK<br><em>WARANTI KOMPRESSOR</em>"),
       photo("@08", "@08%55", "551_inv_comp.png", top=420, w=600, h=700, fit="contain", shadow=False),
       pill("@08%20", "@08%55", "KOMPRESSOR WARANTI 10 TAHUN*", top=1200),
       photo("@08%55", "@09", "hs_step1.jpg", top=480, w=900, h=515),
       pill("@08%55", "@09", "CODY SERVIS BERKALA", top=1100),
       cta("@09", ticks=TICKS_W, fine=FINE_W)])

# ---------------------------------------------------------------- PA12 · 16 Barang basah selang 2 hari (kat. 4)
V["PA12"] = dict(no="16", tajuk="Beli barang basah selang 2 hari", kat="4 Situasi hidup", hook="Cerita pertama",
  slug="pasar-selang-dua-hari", voice="Sulafat", style=FEM_STORY, lines=L(
    ("Bawah tak sejuk, atas je okay. Jadi saya ke pasar, selang dua hari.", "Bawah *tak sejuk*. Ke pasar *selang 2 hari*.", "Seedream: ibu di pasar beli sikit"),
    ("Ayam beli sikit-sikit. Sayur beli sikit-sikit. Takut rosak.", "Beli *sikit-sikit*. Takut rosak.", "Seedream: peti separuh rosak"),
    ("Penat. Minyak kereta. Masa dengan anak-anak pun habis kat pasar.", "Penat · minyak · *masa*", "Seedream: penat dalam kereta"),
    ("Lepas tukar peti, rutin saya berubah. Borong seminggu sekali je.", "Sekarang: *borong seminggu sekali*", "Seedream: punggah borong"),
    ("Peti ais Coway tujuh ratus lima belas liter. Laci sayur ada kawalan kelembapan, jadi sayur kekal segar lebih lama.", "715L · *Humidity Control*", "Rasmi 715_humidity"),
    ("Freezer pula ada super freezing, sampai negatif dua puluh lima darjah, untuk stok ayam dan ikan.", "Super Freezing *−25°C*", "Rasmi 715_open_dark + LED"),
    ("Cody datang servis berkala, tujuh tahun.", "HEART Service *7 tahun*", "Rasmi hs_step3"),
    ("Dari lapan puluh empat ringgit sebulan. Kalau awak pun ke pasar selang dua hari, WhatsApp saya.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa12_a_pasar")), ("@02", R("pa12_b_separuh")), ("@03", R("pa12_c_penat")), ("@04", R("pa12_d_borong")),
          ("@05", "navy"), ("@06", "navy"), ("@07", "blue"), ("@08", "blue")],
  els=[lakonan(),
       banner("@01", "@02", "KE PASAR<br><em>SELANG 2 HARI</em>"),
       pill("@02", "@03", "TAKUT ROSAK", top=1100, bg=RED, color="#fff"),
       {"type": "chips", "in": "@03", "out": "@04", "top": 1000, "items": [{"text": "PENAT", "color": "#fff", "at": "@03"},
                                                                         {"text": "MINYAK", "color": "#fff", "at": "@03%30"},
                                                                         {"text": "MASA", "color": YEL, "at": "@03%60"}]},
       banner("@04", "@05", "SEKARANG:<br><em>BORONG SEMINGGU SEKALI</em>"),
       banner("@05", "@06", "COWAY <em>715L</em>"),
       photo("@05", "@06", "715_humidity.jpg", top=400, w=900, h=675),
       pill("@05%40", "@06", "HUMIDITY CONTROL", top=1140),
       photo("@06", "@07", "715_open_dark.jpg", top=330, w=900, h=706),
       {"type": "led", "in": "@06%30", "out": "@07", "top": 1080, "items": [{"num": "-25", "unit": "°C", "label": "SUPER FREEZING", "at": "@06%40"}]},
       banner("@07", "@08", "HEART SERVICE <em>7 TAHUN</em>"),
       photo("@07", "@08", "hs_step3.jpg", top=420, w=900, h=515),
       cta("@08", ticks=["715L DARI RM84/BULAN*", "HUMIDITY CONTROL", "SUPER FREEZING −25°C"])])

# ---------------------------------------------------------------- PA13 · 20 Dua hari tak sejuk (kat. 4)
V["PA13"] = dict(no="20", tajuk="Dua hari tak sejuk, lauk seminggu rosak", kat="4 Situasi hidup", hook="Cerita pertama",
  slug="dua-hari-tak-sejuk", voice="Algieba", style=MALE_STORY, lines=L(
    ("Dua hari peti ais tak sejuk. Lauk seminggu, masuk tong sampah.", "Dua hari *tak sejuk*. Lauk seminggu *masuk tong sampah.*", "Seedream: buang lauk ke tong"),
    ("Isteri saya cium satu-satu bekas lauk. Muka dia, saya tak boleh lupa.", "Cium *satu-satu* bekas lauk", "Seedream: isteri cium bekas"),
    ("Malam tu kami makan bungkus. Esok pun, bungkus.", "Makan *bungkus*", "Seedream: keluarga makan bungkus"),
    ("Saya call repair. Datang tengok, kena bayar. Kompressor, kena tunggu.", "Datang tengok, *kena bayar*", "Seedream: technician"),
    ("Masa tu saya cakap, tak boleh jadi ni.", "*Tak boleh jadi ni.*", "Tajuk besar"),
    ("Saya tukar peti ais Coway. Bukan sebab peti dia je.", "Tukar peti ais *Coway*", "Rasmi 551_open_food"),
    ("Kompressor dia waranti sepuluh tahun. Dan Cody datang servis berkala, tujuh tahun. Ada orang yang jaga.",
     "Kompressor waranti *10 tahun** · Cody *7 tahun*", "Rasmi 551_inv_comp, hs_step5"),
    ("Dari lapan puluh empat ringgit sebulan. Kalau peti awak pun dah mula buat hal, WhatsApp saya.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa13_a_tong", "night")), ("@02", R("pa13_b_cium", "night")), ("@03", R("pa13_c_bungkus", "night")),
          ("@04", R("pa11_a_repair", "night")), ("@05", "dark"), ("@06", "navy"), ("@07", "navy"), ("@08", "blue")],
  els=[lakonan(),
       banner("@01", "@02", "DUA HARI <em>TAK SEJUK</em>"),
       pill("@01%50", "@02", "LAUK SEMINGGU MASUK TONG", top=1100, bg=RED, color="#fff"),
       pill("@03", "@04", "MALAM NI BUNGKUS. ESOK PUN BUNGKUS.", top=1100),
       pill("@04", "@05", "DATANG TENGOK, KENA BAYAR", top=1100, bg=RED, color="#fff"),
       title("@05", "@06", "TAK BOLEH<br>JADI NI.", top=640, size=170),
       banner("@06", "@07", "PETI AIS <em>COWAY</em>"),
       photo("@06", "@07", "551_open_food.jpg", top=400),
       card("@07", "@07%55", "shield", "KOMPRESSOR 10 TAHUN", "Waranti kompressor*", top=1120),
       photo("@07", "@07%55", "551_inv_comp.png", top=330, w=600, h=700, fit="contain", shadow=False),
       photo("@07%55", "@08", "hs_step5.jpg", top=420, w=900, h=515),
       card("@07%55", "@08", "tech", "CODY 7 TAHUN", "Ada orang yang jaga", top=1040),
       cta("@08", ticks=TICKS_W, fine=FINE_W)])

# ---------------------------------------------------------------- PA14 · 25 Kompressor 10 tahun + Cody (kat. 5, hype kinetic)
V["PA14"] = dict(no="25", tajuk="Kompressor 10 tahun + siapa jaga lepas beli", kat="5 Kenali produk", hook="Kinetic / situasi",
  slug="kompressor-10-tahun-cody-jaga", lines=L(
    ("Isnin call. Ahad baru datang.", "Isnin call. *Ahad* datang.", "Kinetic, latar technician"),
    ("Datang tengok, kena bayar. Kompressor? Tunggu order.", "Tengok, *bayar*. Kompressor? *Tunggu.*", "Kinetic, latar resit"),
    ("Masa beli peti ais, jangan tengok harga je. Tengok siapa yang jaga lepas tu.", "Tengok *siapa jaga*", "Kinetic"),
    ("Peti ais Coway. Kompressor waranti sepuluh tahun.", "Kompressor waranti *10 TAHUN**", "Rasmi 551_inv_comp"),
    ("Dengan Heart Service, Cody datang servis berkala, tujuh tahun.", "Cody datang · *7 tahun*", "Rasmi hs_step1"),
    ("Semak suhu. Steaming. Tukar penapis bau. Cuci luar, dan letak umpan anti-perosak.", "Semak suhu · *Steaming* · Tukar penapis", "Rasmi hs_step1/3/4/6"),
    ("Cody datang ikut jadual. Bukan tunggu peti rosak.", "Ikut *jadual*. Bukan tunggu rosak.", "Kinetic"),
    ("Dari lapan puluh empat ringgit sebulan. WhatsApp saya sekarang.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  spec={"voice": "Fenrir", "style_tts": MALE_HYPE, "player": "hype", "style": "kinetic", "bpm": 128, "brand": "coway", "cap": True},
  scenes=[(0, R("pa11_a_repair", "k-ink")), ("@02", R("pa11_b_resit", "k-ink")), ("@03", "k-white"), ("@04", "k-blue"),
          ("@05", "k-white"), ("@07", "k-blue"), ("@08", "k-white")],
  els=[W("@01", "@02", 330, ("ISNIN", "@01", 150, "#fff", BOX), ("CALL.", "@01%20", 150, "#fff", BOX),
         ("AHAD", "@01%55", 220, "#fff", {"box": True, "bg": RED, "hit": True}), ("BARU DATANG.", "@01%70", 110, "#fff", BOX)),
       W("@02", "@03", 330, ("TENGOK,", "@02", 140, "#fff", BOX), ("BAYAR.", "@02%20", 190, "#fff", {"box": True, "bg": RED, "hit": True}),
         ("KOMPRESSOR?", "@02%45", 120, "#fff", BOX), ("TUNGGU ORDER.", "@02%70", 120, "#fff", {"box": True, "bg": RED, "hit": True})),
       W("@03", "@04", 420, ("JANGAN TENGOK", "@03", 110, INK), ("HARGA JE.", "@03%25", 150, INK),
         ("TENGOK", "@03%55", 130, BLUE), ("SIAPA JAGA.", "@03%70", 170, BLUE, {"hit": True})),
       {"type": "img", "in": "@04", "out": "@05", "src": F + "551_inv_comp.png", "w": 640, "top": 260, "anim": "rise"},
       W("@04", "@05", 1060, ("KOMPRESSOR WARANTI", "@04%20", 80, "#fff", BOX), ("10 TAHUN*", "@04%45", 220, "#fff", {"hit": True})),
       {"type": "img", "in": "@05", "out": "@06", "src": F + "hs_step1.jpg", "w": 960, "top": 420, "anim": "rise"},
       W("@05", "@06", 1060, ("CODY DATANG", "@05", 110, INK), ("7 TAHUN", "@05%45", 200, BLUE, {"hit": True})),
       {"type": "img", "in": "@06", "out": "@06%25", "src": F + "hs_step1.jpg", "w": 960, "top": 420},
       {"type": "img", "in": "@06%25", "out": "@06%50", "src": F + "hs_step3.jpg", "w": 960, "top": 420},
       {"type": "img", "in": "@06%50", "out": "@06%75", "src": F + "hs_step4.jpg", "w": 960, "top": 420},
       {"type": "img", "in": "@06%75", "out": "@07", "src": F + "hs_step6.jpg", "w": 960, "top": 420},
       W("@06", "@07", 1060, ("SEMAK SUHU", "@06", 90, "#fff", BOX), ("STEAMING", "@06%25", 90, "#fff", BBOX),
         ("TUKAR PENAPIS", "@06%50", 90, "#fff", BOX), ("CUCI + ANTI-PEROSAK", "@06%75", 80, "#fff", BBOX)),
       W("@07", "@08", 420, ("IKUT", "@07", 150, "#fff"), ("JADUAL.", "@07%15", 220, "#fff", {"hit": True}),
         ("BUKAN TUNGGU ROSAK.", "@07%50", 100, "#fff", BOX)),
       W("@08", None, 330, ("DARI RM84", "@08", 150, BLUE, {"hit": True}), ("SEBULAN*", "@08%15", 100, INK)),
       {"type": "cta", "in": "@08", "top": 760, "button": "WhatsApp saya", "btnAt": "@08%40", "fine": FINE_W}])

# ---------------------------------------------------------------- PA15 · 27 Beli atau sewa, kira jujur (kat. 6)
V["PA15"] = dict(no="27", tajuk="Beli terus atau sewa? Kira jujur", kat="6 Bantahan & conversion", hook="Angka / bantahan",
  slug="beli-atau-sewa-kira-jujur", voice="Orus", style=MALE, lines=L(
    ("Peti ais Coway tujuh ratus lima belas liter. Tunai, lima ribu lapan ratus sembilan puluh sembilan.", "715L tunai *RM5,899*", "Seedream: lelaki kira dengan kalkulator"),
    ("Sewa, lapan puluh empat sebulan, tujuh tahun. Jumlah, tujuh ribu lima puluh enam ringgit.", "Sewa RM84 × 84 bulan = *RM7,056*", "Counter"),
    ("Betul. Sewa lagi mahal. Saya ejen Coway, tapi saya kira depan awak.", "Sewa *lagi mahal*. Betul.", "Cop"),
    ("Beza seribu seratus lima puluh tujuh. Lebih kurang empat belas ringgit sebulan.", "Beza *RM1,157* ≈ *RM14*/bulan", "Counter"),
    ("Empat belas ringgit tu, Cody servis berkala tujuh tahun. Beli tunai, servis percuma setahun je.",
     "RM14 → servis *7 tahun*. Tunai: *1 tahun*.", "VS SEWA / TUNAI"),
    ("Dan tak perlu keluar hampir enam ribu sekali gus.", "Tak perlu *RM5,899* sekali gus", "Tajuk"),
    ("Kalau ada tunai, dan tak kisah urus servis sendiri, beli tunai. Itu nasihat jujur saya.", "Ada tunai? *Beli tunai.*", "Cop NASIHAT JUJUR"),
    ("Nak bayar bulanan, dan ada orang yang jaga? WhatsApp saya.", "Nak bulanan? *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa15_a_kira")), ("@02", "navy"), ("@05", "blue"), ("@06", "navy"), ("@08", "blue")],
  els=[banner("@01", "@02", "BELI ATAU SEWA?<br><em>KIRA JUJUR</em>"),
       pill("@01%40", "@02", "715L TUNAI RM5,899", top=1080),
       title("@02", "@03", "SEWA RM84 × 84 BULAN", top=380, size=80),
       {"type": "counter", "in": "@02%40", "out": "@03", "top": 600, "from": 0, "to": 7056, "prefix": "RM", "decimals": 0, "dur": 0.9, "size": 220},
       title("@03", "@04", "RM7,056", top=380, size=150, color=YEL),
       stamp("@03%25", "@04", "SEWA LAGI MAHAL ✓", top=720),
       title("@04", "@05", "BEZA", top=330, size=110),
       {"type": "counter", "in": "@04", "out": "@05", "top": 500, "from": 0, "to": 1157, "prefix": "RM", "decimals": 0, "dur": 0.7, "size": 200},
       pill("@04%55", "@05", "≈ RM14 SEBULAN", top=860),
       {"type": "vs", "in": "@05", "out": "@06", "top": 380,
        "left": {"title": "SEWA", "color": BLUE, "items": ["Cody servis 7 tahun", "Tukar penapis bau", "Bayar bulanan"], "at": "@05"},
        "right": {"title": "TUNAI", "color": INK, "items": ["Servis percuma 1 tahun", "Lebih murah", "Bayar sekali gus"], "at": "@05%55"}},
       title("@06", "@07", "TAK PERLU<br>RM5,899<br>SEKALI GUS", top=480, size=120),
       title("@07", "@08", "ADA TUNAI?<br>BELI TUNAI.", top=520, size=130),
       stamp("@07%45", "@08", "NASIHAT JUJUR", top=900, color="#1faa59"),
       cta("@08", ticks=["715L DARI RM84/BULAN*", "TUNAI RM5,899", "SAYA KIRA UNTUK MODEL AWAK"],
           fine="*Harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Jumlah 84 bulan RM7,056. Beli tunai termasuk servis percuma 1 tahun. Tertakluk terma &amp; syarat Coway.")])


def skrip_md():
    rows, body = [], []
    for vid, v in V.items():
        voice = (v.get("spec") or v)["voice"]
        fmt = (v.get("spec") or {}).get("style") or "scenes"
        words = sum(len(l["text"].split()) for l in v["lines"])
        rows.append(f"| {vid} ({v['no']}) | {v['lines'][0]['text']} | {v['kat']} | {v['hook']} | {voice} | {fmt} | ±{words / 2.6:.0f} |")
        body.append(f"### {vid} · {v['tajuk']}\nVideo pelan: {v['no']} · Kategori: {v['kat']} · Persona: P2 · Suara: {voice} · Format: {fmt}\n\n"
                    "| # | VO | Kapsyen | Visual |\n|---|---|---|---|\n" +
                    "\n".join(f"| {l['id']} | {l['text']} | {l['cap']} | {l['_vis']} |" for l in v["lines"]) + "\n")
    return ("# Skrip: peti-ais-p2-01 — Batch 1 (PA06–PA15)\n\n"
            "Status: **DILULUSKAN 29 Okt 2026** (user: \"terus generate video\") · Brief: brief.md · Harga disahkan: 25 Okt 2026 (coway.com.my, tanpa promo)\n"
            "Dijana daripada `videos/peti-ais-p2-01_batch.py` (sumber sebenar teks VO & kapsyen).\n\n"
            "| ID (pelan) | Hook | Kategori | Jenis hook | Suara | Format | ±saat |\n|---|---|---|---|---|---|---|\n" + "\n".join(rows) +
            "\n\nNota kaki CTA: *Harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Tertakluk terma & syarat Coway. "
            "Waranti kompressor 10 tahun tertakluk polisi waranti Coway.\n"
            "Sumber tips: TNB (isi ± 2/3, jaga getah pintu), SEDA (ruang di belakang untuk haba). Cerita watak dilabel \"LAKONAN SEMULA\".\n\n---\n\n" +
            "\n".join(body))


if __name__ == "__main__":
    for vid, v in V.items():
        d = HERE / vid
        d.mkdir(exist_ok=True)
        lines = [{k: x for k, x in l.items() if not k.startswith("_")} for l in v["lines"]]
        (d / "lines.json").write_text(json.dumps(lines, ensure_ascii=False, indent=1))
        head = v.get("spec") or {"voice": v["voice"], "style": v["style"]}
        spec = {"slug": v["slug"], **head, "scenes": [{"at": a, "bg": b} for a, b in v["scenes"]], "els": v["els"],
                **({} if v.get("spec") else BRAND)}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in lines)
        print(f"{vid} {v['slug']:36s} {head['voice']:9s} {len(lines):2d} baris, {words} perkataan (~{words / 2.6:.0f}s)")
    (ROOT / "projek" / KOD / "skrip.md").write_text(skrip_md())
