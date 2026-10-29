"""Peti ais Coway, pakej video untuk ejen (projek/peti-ais-p2-01), batch 2: PA16-PA25
-> videos/PA16..PA25/{lines.json, spec.json} dan bahagian Batch 2 dalam projek/peti-ais-p2-01/skrip.md.

    python3 videos/peti-ais-p2-01_b2.py
    python3 videos/build_video.py PA16 --tts
    python3 videos/peti-ais-p2-01_b2.py            # jalan semula selepas VO: masa klip ikut segments.json
    python3 videos/build_video.py PA16 --render --review out/peti-ais-p2-01

Brief: projek/peti-ais-p2-01/brief.md, batch 2 = video pelan 02, 03, 04, 06, 07, 09, 10, 12, 15, 17.
Shot hidup (sNN) dijana user di Google Flow (Veo) daripada bingkai pertama Seedream; prompt dalam projek/peti-ais-p2-01/shots.md.
Selagi assets/clips/peti-ais-p2-01_sNN.mp4 belum ada, latar guna bingkai Seedream assets/img/peti-ais-p2-01/sNN_*.jpg.
Helper, harga dan nota kaki dikongsi dengan batch 1 (videos/peti-ais-p2-01_batch.py).
Sumber tips: FDA "Chill" (peti <= 4°C, freezer -18°C), TNB (isi ± 2/3, getah pintu), SEDA (ruang untuk haba).
"""
import importlib.util
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("b1", HERE / "peti-ais-p2-01_batch.py")
b1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b1)
from_b1 = ("KOD", "F", "NAVY", "YEL", "BLUE", "RED", "INK", "BRAND", "FEM", "FEM_STORY", "MALE", "MALE_HYPE", "FINE", "FINE_W",
           "FINE_551", "TICKS", "TICKS_W", "L", "R", "banner", "title", "pill", "photo", "reason", "rban", "card", "stamp", "cta",
           "lakonan", "W", "BOX", "BBOX")
globals().update({k: getattr(b1, k) for k in from_b1})

SHOTS = {  # shot -> fail bingkai Seedream (assets/img/peti-ais-p2-01/<nama>.jpg)
    "s01": "s01_layu", "s02": "s02_balut", "s03": "s03_periuk", "s04": "s04_bekas", "s05": "s05_cari", "s06": "s06_lutsinar",
    "s07": "s07_mentah", "s08": "s08_tersusun", "s09": "s09_termometer", "s10": "s10_periuk_panas", "s11": "s11_ruang",
    "s12": "s12_lap", "s13": "s13_buang", "s15": "s15_kedai", "s16": "s16_mealprep", "s17": "s17_bekal"}


def S(shot, color="navy"):
    """Latar shot hidup: klip Flow jika sudah dimuat naik, jika belum bingkai pertama Seedream."""
    return {"_shot": shot, "color": color}


def resolve(bg, a, b, vid):
    """Tukar S() kepada bg sebenar; a/b = saat mula/tamat babak (dari segments.json) atau None."""
    if not (isinstance(bg, dict) and "_shot" in bg):
        return bg
    shot, color = bg["_shot"], bg["color"]
    clip = ROOT / "assets" / "clips" / f"{KOD}_{shot}.mp4"
    if not clip.exists() or a is None:
        return R(SHOTS[shot], color)
    cd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                              capture_output=True, text=True).stdout or 0)
    dur = max(b - a, 0.5)
    c1 = round(min(max(dur, 0.55 * dur), cd, 1.9 * dur), 2)
    return {"clip": f"{KOD}_{shot}", "c0": 0, "c1": c1, "color": color, "shade": True}


V = {}

# ---------------------------------------------------------------- PA16 · 02 Kenapa sayur cepat layu? (kat. 1)
V["PA16"] = dict(no="02", tajuk="Kenapa sayur cepat layu dalam peti ais?", kat="1 Masalah harian", hook="Seru situasi",
  slug="kenapa-sayur-cepat-layu", voice="Aoede", style=b1.FEM, lines=L(
    ("Sayur beli hari Ahad. Rabu dah layu.", "Ahad beli. *Rabu dah layu.*", "Flow s01: ibu keluarkan sayur layu dari laci"),
    ("Selalunya bukan salah sayur. Ada tiga sebab.", "Bukan salah sayur. *3 sebab.*", "s01 sambung, tajuk"),
    ("Satu, simpan basah. Air yang melekat buat sayur cepat lembik.", "1 · Simpan *basah*", "Grafik titisan air"),
    ("Dua, campur dengan buah. Ada buah yang lepaskan gas, cepatkan sayur layu.", "2 · Campur dengan *buah*", "Grafik"),
    ("Tiga, laci terlalu kering, atau terlalu lembap.", "3 · Kelembapan *tak sesuai*", "Grafik"),
    ("Cuba lap kering, balut dengan tisu dapur, dan simpan dalam bekas bertutup.", "Lap kering · balut tisu · *bekas tutup*", "Flow s02: tangan balut sayur"),
    ("Peti ais Coway tujuh ratus lima belas liter ada laci kawalan kelembapan, untuk sayur dan buah.", "715L · *Humidity Control*", "Rasmi 715_humidity"),
    ("Dari lapan puluh empat ringgit sebulan. Nak tips simpan sayur lagi? WhatsApp saya.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s01")), ("@03", "blue"), ("@06", S("s02")), ("@07", "navy"), ("@08", "blue")],
  els=[banner("@01", "@02", "AHAD BELI.<br><em>RABU DAH LAYU.</em>"),
       title("@02", "@03", "3 SEBAB", top=600, size=180, color="#ffffff"),
       reason("@03", "@04", "1", "SIMPAN BASAH", "air melekat, sayur cepat lembik", top=420),
       {"type": "icon", "in": "@03", "out": "@04", "top": 720, "icon": "drop", "size": 280},
       reason("@04", "@05", "2", "CAMPUR DENGAN BUAH", "ada buah lepaskan gas", top=420),
       reason("@05", "@06", "3", "KELEMBAPAN TAK SESUAI", "terlalu kering / terlalu lembap", top=420),
       {"type": "steps", "in": "@06", "out": "@07", "top": 300, "items": [{"text": "LAP KERING", "at": "@06"},
                                                                       {"text": "BALUT TISU DAPUR", "at": "@06%35"},
                                                                       {"text": "BEKAS BERTUTUP", "at": "@06%65"}]},
       banner("@07", "@08", "COWAY <em>715L</em>"),
       photo("@07", "@08", "715_humidity.jpg", top=420, w=900, h=675),
       pill("@07%40", "@08", "HUMIDITY CONTROL", top=1160),
       cta("@08", ticks=["715L DARI RM84/BULAN*", "LACI KAWALAN KELEMBAPAN", "SERVIS HEART 7 TAHUN"])])

# ---------------------------------------------------------------- PA17 · 03 Lauk semalam tak muat (kat. 1)
V["PA17"] = dict(no="03", tajuk="Lauk lebihan tak muat masuk peti", kat="1 Masalah harian", hook="Seru situasi",
  slug="lauk-lebihan-tak-muat", voice="Sulafat", style=FEM, lines=L(
    ("Masak banyak untuk keluarga. Nak simpan lebihan, periuk tak muat masuk peti.", "Lebihan lauk… *periuk tak muat*", "Flow s03: ibu sumbat periuk"),
    ("Ramai simpan terus dengan periuk. Itulah yang makan ruang.", "Simpan dengan *periuk* = makan ruang", "s03 sambung"),
    ("Pindahkan ke bekas leper bertutup. Lebih cepat sejuk, dan boleh susun bertingkat.", "Bekas *leper bertutup*, susun bertingkat", "Flow s04: isi bekas leper"),
    ("Biar lauk sejuk sekejap, kemudian terus masuk peti. Jangan biar atas meja terlalu lama.", "Sejuk sekejap → *terus simpan*", "Grafik jam"),
    ("Kalau selalu masak sekali untuk tiga hari, awak memang perlukan ruang lebih.", "Masak untuk *3 hari*? Perlu ruang lebih", "Grafik"),
    ("Peti ais Coway lima ratus lima puluh satu liter, empat pintu. Satu zon boleh tukar sejuk atau beku.", "551L · *Convertible Zone*", "Rasmi 551_open_food, 551_drawers"),
    ("Dari sembilan puluh sembilan ringgit sebulan. Masak hari-hari, atau sekali untuk beberapa hari? WhatsApp saya.", "551L dari *RM99* · *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s03")), ("@03", S("s04")), ("@04", "blue"), ("@06", "navy"), ("@07", "blue")],
  els=[banner("@01", "@02", "LEBIHAN LAUK…<br><em>PERIUK TAK MUAT</em>"),
       pill("@02", "@03", "PERIUK = MAKAN RUANG", top=1180, bg=RED, color="#fff"),
       banner("@03", "@04", "BEKAS <em>LEPER</em> BERTUTUP"),
       pill("@03%40", "@04", "CEPAT SEJUK · SUSUN BERTINGKAT", top=1180),
       {"type": "icon", "in": "@04", "out": "@05", "top": 380, "icon": "clock", "size": 260},
       title("@04", "@05", "SEJUK SEKEJAP<br>→ TERUS SIMPAN", top=700, size=100),
       title("@05", "@06", "MASAK UNTUK<br>3 HARI?", top=520, size=130),
       pill("@05%40", "@06", "PERLU RUANG LEBIH", top=880),
       banner("@06", "@07", "COWAY <em>551L</em> · 4 PINTU"),
       photo("@06", "@06%55", "551_open_food.jpg", top=400),
       photo("@06%55", "@07", "551_drawers.jpg", top=400),
       pill("@06%55", "@07", "CONVERTIBLE ZONE: SEJUK ↔ BEKU", top=1200),
       cta("@07", ticks=["551L DARI RM99/BULAN*", "4 PINTU · CONVERTIBLE ZONE", "SERVIS HEART 7 TAHUN"], fine=FINE_551)])

# ---------------------------------------------------------------- PA18 · 04 Buka peti, tak jumpa barang (kat. 1)
V["PA18"] = dict(no="04", tajuk="Buka peti, tak jumpa barang", kat="1 Masalah harian", hook="Seru situasi",
  slug="buka-peti-tak-jumpa-barang", voice="Orus", style=MALE, lines=L(
    ("Barang sebenarnya ada. Kita je yang tak nampak.", "Barang ada. *Kita je tak nampak.*", "Flow s05: lelaki cari dalam peti"),
    ("Cari sos, alih tiga bekas. Pintu terbuka lama, angin sejuk keluar.", "Pintu buka lama = *angin sejuk keluar*", "s05 sambung"),
    ("Cuba tiga cara ni.", "*3 cara* ni", "Tajuk"),
    ("Satu, satu rak, satu kategori. Minuman, lauk, bahan mentah.", "1 · Satu rak, *satu kategori*", "Cip"),
    ("Dua, guna bekas lutsinar, supaya nampak isi tanpa buka.", "2 · Bekas *lutsinar*", "Flow s06: bin lutsinar"),
    ("Tiga, barang lama ke depan, barang baru ke belakang.", "3 · Lama *depan*, baru *belakang*", "Grafik"),
    ("Peti ais Coway lima ratus lima puluh satu liter, empat pintu, senang asingkan ikut kategori. Dari sembilan puluh sembilan ringgit sebulan.",
     "551L · 4 pintu · dari *RM99*", "Rasmi 551_open_food"),
    ("Rate susunan peti ais awak, satu hingga sepuluh. Komen, atau WhatsApp saya.", "Rate 1–10? *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s05")), ("@03", "blue"), ("@05", S("s06")), ("@06", "blue"), ("@07", "navy"), ("@08", "blue")],
  els=[banner("@01", "@02", "BARANG ADA.<br><em>KITA JE TAK NAMPAK.</em>"),
       pill("@02", "@03", "PINTU BUKA LAMA = ANGIN SEJUK KELUAR", top=1180, bg=RED, color="#fff"),
       title("@03", "@04", "3 CARA", top=600, size=200),
       reason("@04", "@05", "1", "SATU RAK, SATU KATEGORI", top=420),
       {"type": "chips", "in": "@04", "out": "@05", "top": 720, "items": [{"text": "MINUMAN", "color": "#fff", "at": "@04%35"},
                                                                       {"text": "LAUK", "color": "#fff", "at": "@04%55"},
                                                                       {"text": "MENTAH", "color": YEL, "at": "@04%75"}]},
       *rban("@05", "@06", "2", "BEKAS LUTSINAR", "NAMPAK ISI TANPA BUKA"),
       reason("@06", "@07", "3", "LAMA DI DEPAN", "baru di belakang", top=600),
       banner("@07", "@08", "COWAY <em>551L</em> · 4 PINTU"),
       photo("@07", "@08", "551_open_food.jpg", top=400),
       pill("@07%40", "@08", "SENANG ASINGKAN IKUT KATEGORI", top=1200),
       cta("@08", ticks=["551L DARI RM99/BULAN*", "4 PINTU", "SERVIS HEART 7 TAHUN"], fine=FINE_551)])

# ---------------------------------------------------------------- PA19 · 06 Susun ikut zon (kat. 2)
V["PA19"] = dict(no="06", tajuk="Susun peti ais ikut zon", kat="2 Tips", hook="Tips / arahan",
  slug="susun-peti-ikut-zon", voice="Kore", style=FEM, lines=L(
    ("Kalau semua benda campak masuk peti, memang cepat serabut.", "Campak masuk = *cepat serabut*", "Seedream pa06_c_campur"),
    ("Ini susunan yang lebih selamat.", "Susunan lebih *selamat*", "Flow s08: peti tersusun"),
    ("Rak atas, makanan sedia makan. Lauk masak, kuih, susu.", "Rak atas · *sedia makan*", "Grafik zon"),
    ("Rak bawah, ayam, daging, ikan mentah, dalam bekas bertutup. Supaya air dia tak menitik ke makanan lain.", "Rak bawah · *mentah, bertutup*", "Flow s07: letak ayam mentah"),
    ("Laci, sayur dan buah. Pintu, minuman dan sos.", "Laci · sayur · Pintu · *minuman*", "Grafik zon"),
    ("Simpan video ni untuk hari kemas peti.", "*Simpan* video ni", "s08"),
    ("Nak peti yang memang ada zon? Peti ais Coway, dari lapan puluh empat ringgit sebulan. WhatsApp saya.", "Peti ais Coway dari *RM84* · *WhatsApp saya*", "Rasmi 715_spaces + CTA")),
  scenes=[(0, R("pa06_c_campur")), ("@02", S("s08")), ("@03", "blue"), ("@04", S("s07")), ("@05", "blue"), ("@06", S("s08")), ("@07", "blue")],
  els=[banner("@01", "@02", "CAMPAK MASUK =<br><em>CEPAT SERABUT</em>"),
       banner("@02", "@03", "SUSUNAN LEBIH <em>SELAMAT</em>"),
       {"type": "card", "in": "@03", "out": "@04", "top": 520, "icon": "cup", "title": "RAK ATAS", "sub": "Sedia makan: lauk masak, kuih, susu"},
       *rban("@04", "@05", "↓", "RAK BAWAH: MENTAH", "DALAM BEKAS BERTUTUP"),
       {"type": "card", "in": "@05", "out": "@05%50", "top": 520, "icon": "box", "title": "LACI", "sub": "Sayur dan buah"},
       {"type": "card", "in": "@05%50", "out": "@06", "top": 520, "icon": "drop", "title": "PINTU", "sub": "Minuman dan sos"},
       banner("@06", "@07", "<em>SIMPAN</em> VIDEO NI"),
       banner("@07", None, "PETI AIS <em>COWAY</em>"),
       photo("@07", None, "715_spaces.jpg", top=380, w=520, h=520),
       cta("@07%30", top=960, btn="@07%60")])

# ---------------------------------------------------------------- PA20 · 07 Suhu peti betul ke? (kat. 2)
V["PA20"] = dict(no="07", tajuk="Suhu peti ais awak betul ke?", kat="2 Tips", hook="Mitos vs fakta",
  slug="suhu-peti-ais-betul-ke", voice="Puck", style=MALE, lines=L(
    ("Nombor paling sejuk, tak semestinya setting paling betul.", "Paling sejuk ≠ *paling betul*", "Grafik"),
    ("Garis panduan keselamatan makanan: peti sejuk empat darjah atau kurang. Freezer, negatif lapan belas.", "Peti ≤ *4°C* · Freezer *−18°C*", "LED"),
    ("Terlalu panas, kuman cepat membiak. Terlalu sejuk, sayur boleh beku.", "Panas: *kuman* · Terlalu sejuk: *sayur beku*", "VS"),
    ("Cara semak: letak termometer peti di rak tengah, tunggu beberapa jam, baru baca.", "Termometer di *rak tengah*", "Flow s09: letak termometer"),
    ("Peti lama yang getah pintu dah koyak, selalunya susah nak kekal pada suhu ni.", "Getah koyak = suhu *tak stabil*", "Seedream pa07_b_getah"),
    ("Peti ais Coway lima ratus lima puluh satu liter, ada zon dari lima darjah sampai negatif dua puluh.",
     "551L · Convertible Zone *5°C → −20°C*", "Rasmi 551_cooling"),
    ("Dari sembilan puluh sembilan ringgit sebulan. Nak tahu lagi? WhatsApp saya.", "551L dari *RM99* · *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@02", "navy"), ("@03", "blue"), ("@04", S("s09")), ("@05", R("pa07_b_getah")), ("@06", "navy"), ("@07", "blue")],
  els=[title("@01", "@02", "PALING SEJUK<br>≠ PALING BETUL", top=560, size=120),
       {"type": "led", "in": "@02", "out": "@03", "top": 330, "items": [{"num": "4", "unit": "°C", "label": "PETI SEJUK", "at": "@02%20"},
                                                                     {"num": "-18", "unit": "°C", "label": "FREEZER", "at": "@02%65"}]},
       pill("@02%30", "@03", "GARIS PANDUAN KESELAMATAN MAKANAN", top=1060),
       {"type": "vs", "in": "@03", "out": "@04", "top": 420,
        "left": {"title": "TERLALU PANAS", "color": RED, "items": ["Kuman cepat membiak"], "at": "@03"},
        "right": {"title": "TERLALU SEJUK", "color": BLUE, "items": ["Sayur beku & rosak"], "at": "@03%50"}},
       *rban("@04", "@05", "✓", "TERMOMETER DI RAK TENGAH", "TUNGGU BEBERAPA JAM"),
       *rban("@05", "@06", "!", "GETAH KOYAK", "SUHU TAK STABIL"),
       banner("@06", "@07", "COWAY <em>551L</em>"),
       photo("@06", "@07", "551_cooling.jpg", top=400),
       pill("@06%35", "@07", "CONVERTIBLE ZONE 5°C → −20°C", top=1200),
       cta("@07", ticks=["551L DARI RM99/BULAN*", "CONVERTIBLE ZONE", "SERVIS HEART 7 TAHUN"], fine=FINE_551)])

# ---------------------------------------------------------------- PA21 · 09 Jangan sumbat sampai penuh (kat. 2)
V["PA21"] = dict(no="09", tajuk="Jangan sumbat peti sampai penuh", kat="2 Tips", hook="Seru situasi",
  slug="jangan-sumbat-peti-penuh", voice="Laomedeia", style=FEM, lines=L(
    ("Peti penuh rasa puas hati. Tapi angin sejuk tak boleh lalu.", "Peti penuh = angin sejuk *tak boleh lalu*", "Seedream pa06_a_penuh"),
    ("Angin sejuk perlu bergerak. Kalau tersekat, ada bahagian yang tak cukup sejuk.", "Tersekat → *tak cukup sejuk*", "Grafik"),
    ("Isi lebih kurang dua pertiga, dan jangan tutup lubang angin dalam peti.", "Isi *± 2/3* · jangan tutup *lubang angin*", "Flow s11: susun berjarak"),
    ("Jangan masukkan periuk panas banyak-banyak sekali gus. Biar sejuk sekejap dulu.", "Periuk panas? *Sejuk sekejap dulu*", "Flow s10: periuk rendang berasap"),
    ("Kalau selalu tak cukup ruang, itu tanda peti dah kecil untuk keluarga awak.", "Selalu penuh? *Peti dah kecil*", "Grafik"),
    ("Peti ais Coway tujuh ratus lima belas liter, untuk keluarga yang stok banyak. Dari lapan puluh empat ringgit sebulan.", "715L · dari *RM84*/bulan", "Rasmi 715_spaces"),
    ("Awak jenis penuhkan peti, atau suka ruang kosong? WhatsApp saya.", "Penuh atau kosong? *WhatsApp saya*", "CTA")),
  scenes=[(0, R("pa06_a_penuh")), ("@02", "blue"), ("@03", S("s11")), ("@04", S("s10")), ("@05", "navy"), ("@06", "navy"), ("@07", "blue")],
  els=[banner("@01", "@02", "PETI PENUH =<br><em>ANGIN TAK BOLEH LALU</em>"),
       title("@02", "@03", "TERSEKAT →<br>TAK CUKUP SEJUK", top=560, size=110),
       *rban("@03", "@04", "✓", "ISI ± 2/3 SAHAJA", "JANGAN TUTUP LUBANG ANGIN"),
       *rban("@04", "@05", "!", "PERIUK PANAS?", "SEJUK SEKEJAP DULU"),
       title("@05", "@06", "SELALU PENUH?", top=520, size=130),
       stamp("@05%45", "@06", "PETI DAH KECIL", top=820),
       banner("@06", "@07", "COWAY <em>715L</em>"),
       photo("@06", "@07", "715_spaces.jpg", top=400),
       pill("@06%40", "@07", "UNTUK KELUARGA YANG STOK BANYAK", top=1200),
       cta("@07")])

# ---------------------------------------------------------------- PA22 · 10 Rutin 10 minit (kat. 2, hype ugc)
V["PA22"] = dict(no="10", tajuk="Rutin 10 minit peti ais bersih", kat="2 Tips", hook="Tips / arahan",
  slug="rutin-10-minit-peti-bersih", lines=L(
    ("Tak payah tunggu peti berbau, baru nak cuci.", "Tunggu *berbau* baru cuci?", "Flow s13: buang lauk lama"),
    ("Ni rutin sepuluh minit, seminggu sekali.", "Rutin *10 minit*, seminggu sekali", "Kinetic"),
    ("Satu, keluarkan makanan lama, dan yang dah lepas tarikh.", "1 · Buang *makanan lama*", "Flow s13"),
    ("Dua, lap tumpahan dengan kain lembap dan sabun lembut.", "2 · Lap *tumpahan*", "Flow s12: lap rak"),
    ("Tiga, cuci bekas yang melekit. Empat, susun semula ikut zon.", "3 · Cuci bekas · 4 · *Susun semula*", "Seedream s08"),
    ("Tag orang rumah yang selalu kena buat kerja ni.", "*Tag* orang rumah", "Kinetic"),
    ("Untuk penjagaan lebih dalam, peti ais Coway ada Cody datang servis berkala, termasuk steaming dan tukar penapis bau.",
     "Cody · *Steaming* · tukar penapis", "Rasmi hs_step3, hs_step4"),
    ("Dari lapan puluh empat ringgit sebulan. WhatsApp saya.", "dari *RM84*/bulan · *WhatsApp saya*", "CTA")),
  spec={"voice": "Zephyr", "style_tts": FEM, "player": "hype", "style": "ugc", "bpm": 110, "brand": "coway", "cap": True},
  scenes=[(0, S("s13", "ugc-white")), ("@02", "ugc-blue"), ("@03", S("s13", "ugc-white")), ("@04", S("s12", "ugc-white")),
          ("@05", S("s08", "ugc-white")), ("@06", "ugc-blue"), ("@07", "ugc-white"), ("@08", "ugc-white")],
  els=[W("@01", "@02", 230, ("TUNGGU", "@01", 120, "#fff", BOX), ("BERBAU?", "@01%30", 170, "#fff", {"box": True, "bg": RED, "hit": True})),
       W("@02", "@03", 480, ("RUTIN", "@02", 150, "#fff"), ("10 MINIT", "@02%20", 220, "#fff", {"hit": True}),
         ("SEMINGGU SEKALI", "@02%55", 100, INK, {"box": True, "bg": YEL})),
       W("@03", "@04", 230, ("1 · BUANG", "@03", 120, "#fff", BOX), ("MAKANAN LAMA", "@03%30", 110, "#fff", BBOX)),
       W("@04", "@05", 230, ("2 · LAP", "@04", 120, "#fff", BOX), ("TUMPAHAN", "@04%30", 130, "#fff", BBOX)),
       W("@05", "@06", 230, ("3 · CUCI BEKAS", "@05", 100, "#fff", BOX), ("4 · SUSUN SEMULA", "@05%50", 100, "#fff", BBOX)),
       W("@06", "@07", 520, ("TAG", "@06", 230, "#fff", {"hit": True}), ("ORANG RUMAH", "@06%30", 120, "#fff")),
       {"type": "img", "in": "@07", "out": "@07%50", "src": F + "hs_step3.jpg", "w": 960, "top": 420, "anim": "rise"},
       {"type": "img", "in": "@07%50", "out": "@08", "src": F + "hs_step4.jpg", "w": 960, "top": 420},
       W("@07", "@08", 1060, ("CODY", "@07", 120, INK), ("STEAMING", "@07%45", 110, "#fff", BBOX), ("TUKAR PENAPIS", "@07%70", 100, "#fff", BOX)),
       W("@08", None, 330, ("DARI RM84", "@08", 150, BLUE, {"hit": True}), ("SEBULAN*", "@08%15", 100, INK)),
       {"type": "cta", "in": "@08", "top": 760, "button": "WhatsApp saya", "btnAt": "@08%40",
        "fine": "*Peti ais Coway 715L, harga sewa bulanan pelan HEART Service 7 tahun (7+0), termasuk SST. Tertakluk terma &amp; syarat Coway."}])

# ---------------------------------------------------------------- PA23 · 12 2 pintu, side-by-side atau 4 pintu? (kat. 3)
V["PA23"] = dict(no="12", tajuk="2 pintu biasa, side-by-side atau 4 pintu?", kat="3 Panduan memilih", hook="Perbandingan",
  slug="2-pintu-side-by-side-4-pintu", voice="Achird", style=MALE, lines=L(
    ("Tiga jenis peti ais. Cara guna tak sama.", "*3 jenis* peti ais", "Grafik"),
    ("Dua pintu biasa: freezer atas, peti bawah. Jimat ruang, tapi terhad.", "2 pintu biasa · *jimat ruang*", "Seedream pa23_atas"),
    ("Side-by-side: freezer kiri, peti kanan, tinggi penuh. Sesuai yang stok banyak.", "Side-by-side · *stok banyak*", "Rasmi 715_kitchen1"),
    ("Empat pintu: peti sejuk di atas, ruang bawah berasingan. Sesuai yang suka susun ikut kategori.", "4 pintu · *ikut kategori*", "Rasmi 551_open_food"),
    ("Semak juga ruang depan, untuk buka pintu sepenuhnya.", "Semak ruang *buka pintu*", "Ikon pembaris"),
    ("Coway ada dua: side-by-side tujuh ratus lima belas liter, dari lapan puluh empat ringgit, dan empat pintu lima ratus lima puluh satu liter, dari sembilan puluh sembilan ringgit sebulan.",
     "715L *RM84* · 551L *RM99*", "Rasmi kedua-dua"),
    ("Awak pilih yang mana? Komen, atau WhatsApp saya.", "Pilih yang mana? *WhatsApp saya*", "CTA")),
  scenes=[(0, "navy"), ("@02", R("pa23_atas")), ("@03", "blue"), ("@05", "navy"), ("@06", "blue"), ("@07", "blue")],
  els=[title("@01", "@02", "3 JENIS<br>PETI AIS", top=560, size=170),
       *rban("@02", "@03", "1", "2 PINTU BIASA", "JIMAT RUANG · TERHAD"),
       banner("@03", "@04", "<em>2</em> · SIDE-BY-SIDE"),
       photo("@03", "@04", "715_kitchen1.jpg", top=400),
       pill("@03%40", "@04", "SESUAI YANG STOK BANYAK", top=1200),
       banner("@04", "@05", "<em>3</em> · 4 PINTU"),
       photo("@04", "@05", "551_open_food.jpg", top=400),
       pill("@04%40", "@05", "SUKA SUSUN IKUT KATEGORI", top=1200),
       {"type": "icon", "in": "@05", "out": "@06", "top": 420, "icon": "ruler", "size": 280},
       title("@05", "@06", "SEMAK RUANG<br>BUKA PINTU", top=760, size=110),
       {"type": "vs", "in": "@06", "out": "@07", "top": 420,
        "left": {"title": "715L", "color": BLUE, "items": ["Side-by-side", "2 pintu", "dari RM84/bulan*"], "at": "@06"},
        "right": {"title": "551L", "color": NAVY, "items": ["4 pintu", "Convertible Zone", "dari RM99/bulan*"], "at": "@06%55"}},
       cta("@07")])

# ---------------------------------------------------------------- PA24 · 15 7 perkara sebelum beli (kat. 3, hype kinetic)
V["PA24"] = dict(no="15", tajuk="7 perkara periksa sebelum beli peti ais", kat="3 Panduan memilih", hook="Listicle",
  slug="7-perkara-sebelum-beli-peti-ais", lines=L(
    ("Harga bukan satu-satunya benda nak tengok. Ni tujuh perkara sebelum beli peti ais.", "*7 perkara* sebelum beli", "Flow s15: pasangan di kedai"),
    ("Satu, kapasiti ikut keluarga. Dua, ukuran ruang dan laluan.", "1 Kapasiti · 2 *Ukuran*", "Kinetic"),
    ("Tiga, jenis pintu. Empat, kawalan suhu dan zon.", "3 Jenis pintu · 4 *Zon suhu*", "Kinetic"),
    ("Lima, senang jaga dan bersihkan.", "5 *Senang jaga*", "Kinetic"),
    ("Enam, waranti kompressor, dan siapa yang servis.", "6 *Waranti & servis*", "Kinetic"),
    ("Tujuh, jumlah kos sepanjang tempoh, bukan bayaran bulanan je.", "7 *Jumlah kos*", "Kinetic"),
    ("Peti ais Coway: kompressor waranti sepuluh tahun, Cody servis berkala tujuh tahun, dari lapan puluh empat ringgit sebulan.",
     "Kompressor *10 tahun** · Cody *7 tahun*", "Rasmi 551_inv_comp"),
    ("Simpan checklist ni sebelum survey. WhatsApp saya untuk banding model.", "*Simpan* · *WhatsApp saya*", "CTA")),
  spec={"voice": "Algieba", "style_tts": MALE_HYPE, "player": "hype", "style": "kinetic", "bpm": 128, "brand": "coway", "cap": True},
  scenes=[(0, S("s15", "k-ink")), ("@02", "k-white"), ("@04", "k-blue"), ("@05", "k-white"), ("@07", "k-blue"), ("@08", "k-white")],
  els=[W("@01", "@02", 300, ("HARGA", "@01", 150, "#fff", BOX), ("BUKAN SEMUA.", "@01%20", 120, "#fff", BOX),
         ("7 PERKARA", "@01%55", 200, "#fff", BBOX), ("SEBELUM BELI", "@01%70", 100, "#fff", BOX)),
       W("@02", "@03", 420, ("1 · KAPASITI", "@02", 120, INK), ("2 · UKURAN", "@02%50", 130, BLUE, {"hit": True})),
       W("@03", "@04", 420, ("3 · JENIS PINTU", "@03", 110, INK), ("4 · ZON SUHU", "@03%50", 130, BLUE, {"hit": True})),
       W("@04", "@05", 520, ("5 · SENANG", "@04", 130, "#fff"), ("JAGA", "@04%35", 220, "#fff", {"hit": True})),
       W("@05", "@06", 420, ("6 · WARANTI", "@05", 130, INK), ("& SERVIS", "@05%45", 150, BLUE, {"hit": True})),
       W("@06", "@07", 420, ("7 · JUMLAH", "@06", 130, INK), ("KOS", "@06%30", 230, BLUE, {"hit": True}),
         ("BUKAN BULANAN JE", "@06%65", 90, "#fff", {"box": True, "bg": RED})),
       {"type": "img", "in": "@07", "out": "@08", "src": F + "551_inv_comp.png", "w": 600, "top": 260, "anim": "rise"},
       W("@07", "@08", 1040, ("KOMPRESSOR 10 TAHUN*", "@07%15", 90, "#fff", BOX), ("CODY 7 TAHUN", "@07%55", 110, "#fff", {"hit": True})),
       W("@08", None, 330, ("SIMPAN", "@08", 150, BLUE, {"hit": True}), ("CHECKLIST NI", "@08%15", 100, INK)),
       {"type": "cta", "in": "@08", "top": 760, "button": "WhatsApp saya", "btnAt": "@08%40", "fine": FINE_W}])

# ---------------------------------------------------------------- PA25 · 17 Meal prep untuk anak (kat. 4)
V["PA25"] = dict(no="17", tajuk="Mak ayah yang meal prep untuk anak", kat="4 Situasi hidup", hook="Cerita pertama",
  slug="meal-prep-untuk-anak", voice="Vindemiatrix", style=FEM_STORY, lines=L(
    ("Hari Ahad, saya masak untuk tiga hari. Pagi Isnin, tak kelam-kabut.", "Ahad masak *3 hari*. Isnin *tak kelam-kabut.*", "Flow s16: ibu susun bekas"),
    ("Bekal sekolah, sarapan, lauk makan malam. Semua dah siap dalam bekas.", "Bekal · sarapan · *lauk malam*", "s16 sambung"),
    ("Tapi dulu, peti lama tak muat. Separuh bekas terpaksa simpan atas meja.", "Dulu: peti lama *tak muat*", "Seedream s03_periuk"),
    ("Kuncinya, bekas leper sama saiz, dan satu rak untuk setiap hari.", "Bekas *sama saiz* · satu rak sehari", "Grafik"),
    ("Pagi, anak ambil sendiri bekal dia.", "Anak ambil *sendiri*", "Flow s17: anak ambil bekal"),
    ("Peti ais Coway lima ratus lima puluh satu liter, empat pintu. Zon bawah boleh tukar jadi peti sejuk, bila stok lauk lebih.",
     "551L · zon bawah tukar *jadi peti sejuk*", "Rasmi 551_drawers"),
    ("Dari sembilan puluh sembilan ringgit sebulan. Siapa sini suka masak awal-awal? WhatsApp saya.", "551L dari *RM99* · *WhatsApp saya*", "CTA")),
  scenes=[(0, S("s16")), ("@03", R("s03_periuk")), ("@04", "blue"), ("@05", S("s17")), ("@06", "navy"), ("@07", "blue")],
  els=[lakonan(),
       banner("@01", "@02", "AHAD MASAK <em>3 HARI</em>"),
       {"type": "chips", "in": "@02", "out": "@03", "top": 1080, "items": [{"text": "BEKAL", "color": "#fff", "at": "@02"},
                                                                         {"text": "SARAPAN", "color": "#fff", "at": "@02%30"},
                                                                         {"text": "LAUK MALAM", "color": YEL, "at": "@02%60"}]},
       pill("@03", "@04", "DULU: PETI LAMA TAK MUAT", top=1180, bg=RED, color="#fff"),
       {"type": "steps", "in": "@04", "out": "@05", "top": 380, "items": [{"text": "BEKAS LEPER SAMA SAIZ", "at": "@04"},
                                                                       {"text": "SATU RAK, SATU HARI", "at": "@04%45"}]},
       banner("@05", "@06", "ANAK AMBIL <em>SENDIRI</em>"),
       banner("@06", "@07", "COWAY <em>551L</em> · 4 PINTU"),
       photo("@06", "@07", "551_drawers.jpg", top=400),
       pill("@06%40", "@07", "ZON BAWAH: BEKU ↔ SEJUK", top=1200),
       cta("@07", ticks=["551L DARI RM99/BULAN*", "CONVERTIBLE ZONE", "SERVIS HEART 7 TAHUN"], fine=FINE_551)])


def times(vid):
    """'@NN' -> saat mula baris (dari segments.json); None jika VO belum ada."""
    p = HERE / vid / "segments.json"
    if not p.exists():
        return None
    return {s["id"]: (s["a"], s["b"]) for s in json.loads(p.read_text())}


def at_sec(at, seg):
    if at == 0:
        return 0.0
    return seg[at[1:3]][0]


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
    return ("\n\n---\n\n# Batch 2 (PA16–PA25)\n\n"
            "Status: **DILULUSKAN 30 Okt 2026** (user: \"sambung next batch\"; batch 1 dianggap lulus) · Harga disahkan: 25 Okt 2026\n"
            "Dijana daripada `videos/peti-ais-p2-01_b2.py`. Shot hidup `sNN`: Google Flow (Veo), prompt dalam `shots.md`.\n\n"
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
        scenes = []
        for i, (a, bg) in enumerate(v["scenes"]):
            b = starts[i + 1] if i + 1 < len(starts) else end
            scenes.append({"at": a, "bg": resolve(bg, starts[i], b, vid)})
        head = v.get("spec") or {"voice": v["voice"], "style": v["style"]}
        spec = {"slug": v["slug"], **head, "scenes": scenes, "els": v["els"], **({} if v.get("spec") else BRAND)}
        (d / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        words = sum(len(l["text"].split()) for l in lines)
        clips = sum(1 for s in scenes if "clip" in s["bg"])
        print(f"{vid} {v['slug']:34s} {head['voice']:12s} {len(lines):2d} baris, {words} perkataan (~{words / 2.4:.0f}s), klip Flow {clips}")
    sk = ROOT / "projek" / KOD / "skrip.md"
    txt = sk.read_text()
    txt = txt.split("\n\n---\n\n# Batch 2 (PA16–PA25)")[0].rstrip("\n") + "\n" + skrip_md()
    sk.write_text(txt)
