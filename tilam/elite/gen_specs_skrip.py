"""Spesifikasi video dari skrip rasmi BEREX Elite (tilam/elite/skrip_elite_9_video.md) -> tilam/b/sNN.json

    python tilam/elite/gen_specs_skrip.py && python tilam/build_b.py s01
Peraturan visual:
- babak masalah/penerangan guna gambar jana realistik (assets/tilam/jana/el_*)
- visual rasmi Coway hanya pada product reveal, dan setiap gambar laman tidak diulang dalam video yang sama
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "b"
EL, J = "assets/tilam/elite/", "assets/tilam/jana/"
EV = EL + "video/"
THEME = {"bg": "#1a1712", "bg2": "#4a3f2e", "accent": "#e8c98a", "accent2": "#f5e6c4", "ink": "#1a1712"}
PRODUCT = {"name": "COWAY <b>BEREX ELITE</b>", "sub": "Soft &amp; Firm · Queen &amp; King", "img": EL + "latest-gallery2.png", "ctaSize": 76}
CLIPS = {
    "orbs": {"src": EV + "16x9_CUTDOWN_02_HIRES.mp4", "from": 5.0, "to": 10.0},
    "hero": {"src": EV + "16x9_CUTDOWN_01_HIRES.mp4", "from": 12.0, "to": 16.0},
    "plush": {"src": EV + "16x9_CUTDOWN_03_HIRES.mp4", "from": 2.0, "to": 8.0},
    "uv": {"src": EV + "16x9_CUTDOWN_04_HIRES.mp4", "from": 8.2, "to": 10.6},
    "cool": {"src": EV + "coolingloop.mp4", "from": 0.0, "to": 5.0},
}
IMG = {
    "penat": J + "el_v1a_bangun_penat.png", "malam": J + "el_v1b_tidur_malam.png", "kedai": J + "el_v1d_kedai_tilam.png",
    "mendap": J + "hook_tilam_mendap.png",
    "layer": EL + "mattreslayer-img.png",
    # gambar jana Seedream untuk Video 2–9 (senarai_gambar_skrip.md)
    "pusing": J + "el_v2a_pasangan_pusing.jpg", "bonnell": J + "el_v2c_spring_bersambung.jpg", "pocket": J + "el_v2d_pocket_spring.jpg",
    "panas": J + "el_v3a_malam_panas.jpg", "fabrik": J + "el_v3c_sentuh_fabrik.jpg",
    "hotel": J + "el_v4a_katil_hotel.jpg", "balik": J + "el_v4b_balik_rumah.jpg",
    "mengiring": J + "el_v5a_baring_mengiring.jpg", "foam": J + "el_v6a_ketul_foam.jpg",
    "cadar": J + "el_v7a_basuh_cadar.jpg", "habuk": J + "el_v7b_habuk_tilam.jpg",
    "banding": J + "el_v8a_banding_pilihan.jpg", "posisi": J + "el_v9a_posisi_tidur.jpg",
    # visual rasmi Elite
    "tebal": EL + "Asset_8.jpg", "sanitized": EL + "s3-img-new.png", "bilik": EL + "galleryloop2.jpg", "rumah": EL + "new-loop1.jpg",
    "sudut": EL + "latest-galleryloop6.png", "permukaan": EL + "latest-galleryloop4.png", "juruteknik": EL + "vid-slide4.jpg",
    "topper": EL + "latest-gallery6.png",
}


def L(i, text, **scene): return {"id": f"{i:02d}", "text": text, "scene": scene}
def H(t=None, k=None, s=None, y=170, **kw): return dict({k2: v for k2, v in [("t", t), ("k", k), ("s", s)] if v}, y=y, **kw)
def BG(img=None, clip=None, dim=1, pos=None): return dict({"img": IMG[img]} if img else {"clip": clip}, dim=dim, **({"pos": pos} if pos else {}))
def M(img=None, clip=None, box=(90, 560, 900, 620), fit="cover", **kw): return dict({"img": IMG[img]} if img else {"clip": clip}, box=list(box), fit=fit, **kw)
def items(*xs, y=640, gap=150): return [dict(t=t, at=at, y=y + i * gap, **({"icon": ic} if ic else {})) for i, (t, at, ic) in enumerate(xs)]
LAYER = dict(img=IMG["layer"], box=[0, 560, 1080, 540], fit="contain", kb="none")
def W(t, at=0.05, size=120, y=640, **kw): return dict(t=t, at=at, size=size, y=y, **kw)
def chips(*xs, y=1260, gap=105): return [{"t": t, "at": at, "y": y + i * gap} for i, (t, at) in enumerate(xs)]


V = {}
# Video 1 (TOFU) — Tidur dah cukup, tapi kenapa masih penat?
V["s01"] = dict(title="Tidur dah cukup, tapi kenapa masih penat?", slug="tidur-cukup-masih-penat", mood="calm", lines=[
    L(1, "Pernah tak, tidur malam rasa macam dah cukup. Tapi bila bangun pagi, badan masih rasa penat?",
      bg=BG("penat"), head=H("Tidur dah cukup…<br>tapi <b>masih penat?</b>", k="PERNAH TAK?", y=200)),
    L(2, "Kadang-kadang kita ingat, asalkan tidur tujuh ke lapan jam, mesti bangun segar, kan?",
      bg=BG("malam"), words=[W("<b>7–8 JAM</b>", at="tujuh", size=170, y=600), W("= bangun segar?", at="segar", size=80, y=800, anim="up")]),
    L(3, "Tapi sebenarnya, banyak benda boleh pengaruhi keselesaan tidur. Salah satunya, tilam yang kita guna setiap malam.",
      bg=BG("mendap", dim=.85), words=[W("SALAH SATUNYA:", at="Salah", size=70, y=600, anim="up"), W("<b>TILAM</b> KITA.", at="tilam", size=140, y=720)]),
    L(4, "Kita tidur atas tilam yang sama setiap hari. Tapi pernah tak, kita betul-betul ambil tahu apa yang ada dalam tilam tu?",
      bg=BG("kedai"), head=H("Apa yang ada<br><b>dalam tilam</b> kita?", y=200, at="pernah")),
    L(5, "Sebab tu, kalau nak pilih tilam, jangan tengok harga dengan rupa luaran je.", cont=True,
      chips=chips(("Bukan harga je", "harga"), ("Bukan rupa luar je", "rupa"), y=1300)),
    L(6, "Ini yang menarik tentang Coway BEREX Elite. Model tilam premium baharu daripada Coway.",
      bg=BG(clip="hero", dim=.55), head=H("Coway <b>BEREX Elite</b>", k="BAHARU", s="Model tilam premium", y=200)),
    L(7, "Dia gabungkan foam, lateks asli dan pocket spring, dengan sistem sokongan sembilan zon.",
      head=H("Sokongan <b>9 zon</b>", k="DALAM ELITE"), media=LAYER,
      chips=chips(("Foam", "foam"), ("Lateks asli", "lateks"), ("Pocket spring", "pocket"), y=1180)),
    L(8, "Kalau tengah survey tilam baru, jom kenali dulu BEREX Elite. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan satu-satu."}),
])

# Video 2 (TOFU) — Pasangan pusing, kita pun terjaga
V["s02"] = dict(title="Pasangan pusing, kita pun terjaga", slug="pasangan-pusing-terjaga", mood="calm", lines=[
    L(1, "Siapa tidur dengan pasangan, mesti pernah rasa benda ni. Pasangan pusing badan je, kita pun terasa sekali!",
      bg=BG("pusing"), head=H("Pasangan pusing…<br>kita pun <b>terjaga?</b>", k="TIDUR BERDUA", y=200)),
    L(2, "Bila tidur berdua, sebenarnya bukan kita je yang kena selesa. Pasangan kita pun sama.",
      bg=BG("posisi", dim=.85), words=[W("BUKAN KITA JE", at="bukan", size=96, y=620, anim="up"), W("PASANGAN <b>PUN SAMA</b>", at="Pasangan", size=84, y=780)]),
    L(3, "Sebab tu, bila pilih tilam, salah satu benda yang boleh kita tengok ialah jenis spring yang digunakan.",
      bg=BG("bonnell"), head=H("Tengok <b>jenis spring</b>", k="BILA PILIH TILAM", y=200)),
    L(4, "Contohnya, pocket spring. Senang cerita, spring ni duduk dalam poket masing-masing, bukan semuanya bersambung macam sistem spring biasa.",
      bg=BG("pocket"), head=H("<b>Pocket spring</b>", k="CONTOHNYA", y=200),
      chips=chips(("Duduk dalam poket sendiri", "poket"), ("Bukan bersambung", "bersambung"), y=1300)),
    L(5, "Coway BEREX Elite menggunakan sistem pocket spring yang direka dengan sembilan zon sokongan.",
      bg=BG(clip="hero", dim=.55), head=H("Coway <b>BEREX Elite</b>", k="POCKET SPRING", s="Direka dengan 9 zon sokongan", y=200)),
    L(6, "Tapi kena faham juga, kesan pergerakan yang kita rasa tetap bergantung pada keseluruhan reka bentuk tilam dan keadaan penggunaan.",
      media=M("sudut"), head=H("Tapi <b>kena faham</b> juga", y=170),
      note={"t": "Kesan pergerakan bergantung pada reka bentuk keseluruhan tilam &amp; cara penggunaan.", "at": "bergantung", "y": 1260}),
    L(7, "Menarik kan? Kalau nak tahu apa lagi yang ada dalam tilam ni, WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya tunjuk satu-satu."}),
])

# Video 3 (TOFU) — Malam dah panas, tilam pun rasa tak selesa?
V["s03"] = dict(title="Malam dah panas, tilam pun rasa tak selesa?", slug="malam-panas-tilam", mood="calm", lines=[
    L(1, "Cuaca Malaysia ni kadang-kadang dah cukup panas. Bila nak tidur, mestilah kita nak rasa selesa, kan?",
      bg=BG("panas"), head=H("Malam dah <b>panas…</b>", k="CUACA MALAYSIA", y=200)),
    L(2, "Bila pilih tilam, ramai orang akan tengok lembut ke keras, tebal ke nipis.",
      bg=BG("kedai", dim=.85), chips=chips(("Lembut ke keras?", "lembut"), ("Tebal ke nipis?", "tebal"), y=1300)),
    L(3, "Tapi ada satu lagi benda yang boleh kita tengok, iaitu bahan yang digunakan pada permukaan tilam tu.",
      bg=BG("fabrik"), head=H("Bahan <b>permukaan</b> tilam", k="SATU LAGI", y=200)),
    L(4, "Sebab permukaan tilam ni lah yang kita sentuh sepanjang kita tidur.", cont=True,
      words=[W("KITA SENTUH", at="sentuh", size=96, y=1150, anim="up"), W("<b>SEPANJANG MALAM</b>", at="sepanjang", size=96, y=1290)]),
    L(5, "Untuk Coway BEREX Elite, dia menggunakan fabrik penyejuk dan turut mempunyai ciri anti-statik.",
      media=M(clip="cool", box=(165, 480, 750, 750), kb="none"), head=H("Coway <b>BEREX Elite</b>", y=150),
      chips=chips(("Fabrik penyejuk", "penyejuk"), ("Anti-statik", "anti"), y=1270)),
    L(6, "Jadi, selain tengok rupa dan ketebalan, kita boleh ambil tahu juga tentang bahan yang digunakan.",
      media=M("permukaan", box=(90, 560, 900, 900)), head=H("Tengok juga <b>bahannya</b>", y=170)),
    L(7, "Kalau tengah cari tilam baru, jangan lupa tengok bahagian ni juga. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya explain apa yang menarik."}),
])

# Video 4 (TOFU) — Tilam dekat rumah, kita pilih betul-betul ke?
V["s04"] = dict(title="Tilam dekat rumah, kita pilih betul-betul ke?", slug="tilam-hotel-tilam-rumah", mood="calm", lines=[
    L(1, "Pernah tak pergi hotel, tidur atas katil dia, lepas tu rasa… eh, sedapnya tilam ni?",
      bg=BG("hotel"), head=H("Eh… <b>sedapnya</b><br>tilam hotel ni!", k="PERNAH TAK?", y=200)),
    L(2, "Kadang-kadang kita pergi hotel, benda yang kita ingat bukan bilik cantik je. Katil dia pun boleh jadi salah satu benda yang kita suka.", cont=True,
      words=[W("BUKAN BILIK JE", at="bukan", size=90, y=1250, anim="up"), W("<b>KATIL DIA PUN</b>", at="Katil", size=96, y=1390)]),
    L(3, "Lepas balik rumah, baru terfikir, kenapa kat rumah sendiri kita tak ambil berat sangat tentang tilam?",
      bg=BG("balik"), head=H("Kat rumah…<br><b>kenapa tak?</b>", y=200)),
    L(4, "Sedangkan tilam ni kita guna setiap hari.", cont=True,
      words=[W("GUNA <b>SETIAP HARI</b>", at="setiap", size=100, y=1300)]),
    L(5, "Sebab tu, kalau nak beli tilam, jangan tengok rupa luar je. Cuba ambil tahu juga apa yang ada dalamnya dan macam mana ia dibina.",
      bg=BG("mendap", dim=.85), head=H("Jangan tengok<br><b>rupa luar</b> je", y=200),
      chips=chips(("Apa yang ada dalamnya", "dalamnya"), ("Macam mana ia dibina", "dibina"), y=1300)),
    L(6, "Contohnya Coway BEREX Elite. Ketebalan dia tiga puluh enam sentimeter, dengan reka bentuk plush top.",
      media=M("tebal", box=(60, 560, 960, 700)), head=H("Coway <b>BEREX Elite</b>", k="CONTOHNYA", y=170),
      chips=chips(("36 cm", "tiga"), ("Plush top", "plush"), y=1340)),
    L(7, "Dan gabungan beberapa lapisan foam, lateks asli serta pocket spring.",
      head=H("Gabungan <b>lapisan</b>", y=170), media=LAYER,
      chips=chips(("Foam", "foam"), ("Lateks asli", "lateks"), ("Pocket spring", "pocket"), y=1180)),
    L(8, "Kalau nak upgrade tilam dekat rumah, boleh mula dengan kenali dulu BEREX Elite. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan satu-satu."}),
])

# Video 5 (MOFU) — Apa benda 9 zon ni sebenarnya?
V["s05"] = dict(title="Apa benda 9 zon ni sebenarnya?", slug="apa-itu-9-zon", mood="warm", lines=[
    L(1, "Bila orang cakap tilam ni ada sembilan zon, pernah tertanya-tanya tak, apa maksud sembilan zon tu sebenarnya?",
      bg=BG(clip="orbs", dim=.6), head=H("Apa benda<br><b>9 zon</b> ni?", k="PERNAH TERTANYA?", y=200)),
    L(2, "Okay, saya explain cara mudah. Bila kita tengok tilam, kita nampak macam satu permukaan je.",
      bg=BG("bilik", dim=.85, pos="50% 50%"), words=[W("SATU PERMUKAAN", at="satu", size=96, y=640, anim="up"), W("<b>JE?</b>", at="je", size=150, y=780)]),
    L(3, "Tapi dalam tilam, ada lapisan-lapisan berbeza yang mempunyai fungsi masing-masing.",
      head=H("Ada <b>lapisan</b> berbeza", k="DALAM TILAM", y=170), media=LAYER),
    L(4, "Dalam BEREX Elite, ada tiga komponen utama yang menggunakan reka bentuk sembilan zon, iaitu PU foam, lateks asli dan pocket spring.",
      head=H("3 komponen <b>9 zon</b>", k="BEREX ELITE", y=170),
      items=items(("PU foam 9 zon", "PU", "1"), ("Lateks asli 9 zon", "lateks", "2"), ("Pocket spring 9 zon", "pocket", "3"), y=640)),
    L(5, "Foam ni sebahagian daripada lapisan keselesaan tilam. Lateks asli pula ada ciri anjal, manakala pocket spring membantu memberi sokongan melalui spring individu.",
      bg=BG("pocket", dim=.8), chips=chips(("Foam: lapisan keselesaan", "Foam"), ("Lateks asli: anjal", "anjal"), ("Pocket spring: spring individu", "individu"), y=1180)),
    L(6, "Jadi, bila kita sebut sembilan zon, maksudnya reka bentuk sokongan tu dibahagikan ikut beberapa zon, bukan semuanya direka dengan cara yang sama.",
      bg=BG("mengiring"), head=H("Sokongan <b>ikut zon</b>", y=200),
      note={"t": "Bukan semua bahagian tilam direka dengan cara yang sama.", "at": "bukan", "y": 1330}),
    L(7, "Kalau dibandingkan dengan BEREX Prime II berdasarkan spesifikasi yang kita ada, pocket spring Elite naik daripada tujuh zon kepada sembilan zon. Lateks asli pula daripada lima zon kepada sembilan zon.",
      head=H("Elite vs <b>Prime II</b>", k="PERBEZAAN", y=170),
      items=items(("Pocket spring: 7 → <b>9 zon</b>", "pocket", "↑"), ("Lateks asli: 5 → <b>9 zon</b>", "Lateks", "↑"), y=700),
      note={"t": "Berdasarkan spesifikasi produk rasmi.", "at": 0.5, "y": 1100}),
    L(8, "Jadi, sembilan zon tu bukan sekadar nombor pada nama produk. Nak tahu apa lagi yang membezakan Elite? WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya tunjuk lapisan dia."}),
])

# Video 6 (MOFU) — Tilam 36 cm, apa yang ada dalamnya?
V["s06"] = dict(title="Tilam 36 cm, apa yang ada dalamnya?", slug="tilam-36cm-dalamnya", mood="warm", lines=[
    L(1, "Kalau nampak tilam setebal tiga puluh enam sentimeter macam ni, mesti ada yang tertanya-tanya, apa sebenarnya yang ada dalam dia?",
      bg=BG(clip="plush", dim=.55), head=H("Tilam <b>36 cm</b>…<br>apa dalam dia?", y=200)),
    L(2, "Okay, jom kita tengok. Bahagian paling atas, BEREX Elite menggunakan fabrik penyejuk dengan perlindungan Sanitized.",
      media=M("sanitized", box=(60, 560, 960, 560)), head=H("Paling <b>atas</b>", k="LAPISAN 1", y=170),
      chips=chips(("Fabrik penyejuk", "penyejuk"), ("Perlindungan Sanitized®", "Sanitized"), y=1200)),
    L(3, "Lepas tu ada lapisan PU foam sembilan zon, diikuti lateks asli sembilan zon.",
      head=H("Lapisan <b>tengah</b>", y=170), media=LAYER,
      chips=chips(("PU foam 9 zon", "PU"), ("Lateks asli 9 zon", "lateks"), y=1180)),
    L(4, "Di bahagian bawah pula ada lagi lapisan PU foam, pocket spring sembilan zon dan lapisan sabut kelapa.",
      bg=BG("pocket", dim=.8), head=H("Bahagian <b>bawah</b>", y=200),
      chips=chips(("PU foam", "PU"), ("Pocket spring 9 zon", "pocket"), ("Sabut kelapa", "sabut"), y=1180)),
    L(5, "Jadi, tilam ni bukan sekadar satu ketul foam tebal. Dia sebenarnya terdiri daripada beberapa lapisan bahan yang berbeza.",
      bg=BG("foam"), words=[W("BUKAN SATU", at="bukan", size=100, y=560, anim="up"), W("<b>KETUL FOAM</b>", at="ketul", size=120, y=700)]),
    L(6, "Setiap bahan tu ada ciri tersendiri dan memainkan peranan dalam keseluruhan reka bentuk tilam.",
      media=M("sudut", box=(90, 560, 900, 900)), head=H("Setiap lapisan<br><b>ada peranan</b>", y=150)),
    L(7, "Kalau nak bandingkan dengan Prime II, ketebalan Elite ialah tiga puluh enam sentimeter, berbanding tiga puluh tiga sentimeter untuk Prime II.",
      media=M("tebal", box=(60, 520, 960, 600)), head=H("Elite vs <b>Prime II</b>", k="PERBEZAAN", y=150),
      items=items(("Elite: <b>36 cm</b>", "Elite", "E"), ("Prime II: 33 cm", "tiga puluh tiga", "II"), y=1180)),
    L(8, "Elite juga menggunakan konfigurasi sembilan zon pada lapisan foam, lateks asli dan pocket spring.",
      head=H("<b>9 zon</b> pada 3 lapisan", y=200),
      items=items(("PU foam", "foam", "9"), ("Lateks asli", "lateks", "9"), ("Pocket spring", "pocket", "9"), y=640)),
    L(9, "Bila dah tahu apa yang ada di dalamnya, barulah kita boleh buat perbandingan dengan lebih jelas. Nak kenali BEREX Elite dengan lebih dekat? WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan setiap lapisan."}),
])

# Video 7 (MOFU) — Cadar kita basuh, tapi tilam macam mana?
V["s07"] = dict(title="Cadar kita basuh, tapi tilam macam mana?", slug="cadar-basuh-tilam-macam-mana", mood="calm", lines=[
    L(1, "Cadar kita rajin basuh, kan?",
      bg=BG("cadar"), head=H("Cadar <b>rajin basuh</b>…", k="KAN?", y=200)),
    L(2, "Tapi bila kali terakhir kita fikir tentang kebersihan tilam di bawah cadar tu?",
      bg=BG("habuk"), head=H("Tilam <b>bawah cadar</b><br>macam mana?", y=200)),
    L(3, "Bila bercakap tentang tilam, kita selalu fikir tentang lembut, keras, selesa atau tak.",
      bg=BG("malam", dim=.85), chips=chips(("Lembut?", "lembut"), ("Keras?", "keras"), ("Selesa atau tak?", "selesa"), y=1180)),
    L(4, "Tapi aspek penjagaan pun boleh jadi salah satu benda yang kita pertimbangkan sebelum membeli.",
      bg=BG("fabrik", dim=.8), words=[W("ASPEK", at="aspek", size=90, y=640, anim="up"), W("<b>PENJAGAAN</b>", at="penjagaan", size=130, y=770)]),
    L(5, "BEREX Elite dilengkapi perlindungan Sanitized, yang dikaitkan dengan ciri anti-bakteria, anti-kulat dan anti-hama habuk.",
      media=M("sanitized", box=(60, 560, 960, 560)), head=H("Perlindungan <b>Sanitized®</b>", k="BEREX ELITE", y=170),
      chips=chips(("Anti-bakteria", "bakteria"), ("Anti-kulat", "kulat"), ("Anti-hama habuk", "hama"), y=1200)),
    L(6, "Cuma, penjagaan tilam secara berkala tetap penting. Ciri pada fabrik bukan bermaksud tilam tak perlu dibersihkan langsung.",
      media=M("permukaan", box=(90, 560, 900, 800)), head=H("Penjagaan berkala<br><b>tetap penting</b>", y=150),
      note={"t": "Ciri fabrik tak bermaksud tilam tak perlu dibersihkan.", "at": "Ciri", "y": 1420}),
    L(7, "Selain tu, ada juga servis penjagaan tilam tujuh langkah oleh juruteknik Coway, tertakluk pada terma dan syarat yang ditetapkan.",
      bg=BG(clip="uv", dim=.55), head=H("Servis <b>7 langkah</b>", k="NILAI TAMBAH", s="Oleh juruteknik Coway", y=200),
      note={"t": "*Tertakluk pada terma &amp; syarat.", "at": "tertakluk", "y": 1330}),
    L(8, "Jadi, masa survey tilam, tanya juga apa ciri perlindungan dan servis yang disertakan sekali. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan servisnya."}),
])

# Video 8 (MOFU) — Lepas beli tilam, habis dekat situ je ke?
V["s08"] = dict(title="Lepas beli tilam, habis dekat situ je ke?", slug="lepas-beli-tilam-servis", mood="warm", lines=[
    L(1, "Bila nak beli tilam, korang biasanya tengok harga dan spesifikasi je ke? Atau korang tengok juga apa yang kita dapat selepas beli?",
      bg=BG("banding"), head=H("Harga &amp; spek <b>je?</b>", k="BILA NAK BELI TILAM", y=200),
      words=[W("SELEPAS BELI?", at="selepas", size=100, y=1350)]),
    L(2, "Saya rasa benda ni pun penting. Sebab bila beli tilam, kita bukan guna sehari dua. Kita nak guna untuk satu tempoh yang panjang.",
      bg=BG("rumah", dim=.85, pos="50% 50%"), words=[W("BUKAN SEHARI DUA", at="bukan", size=90, y=640, anim="up"), W("<b>TEMPOH PANJANG</b>", at="panjang", size=110, y=790)]),
    L(3, "Jadi, selain tengok bahan dan reka bentuk tilam, kita boleh tanya juga tentang servis penjagaan selepas pembelian.",
      media=M("juruteknik", box=(60, 560, 960, 560)), head=H("Servis <b>selepas beli</b>", k="TANYA JUGA", y=170)),
    L(4, "Untuk Coway BEREX Elite, ada servis penjagaan tilam tujuh langkah. Antaranya termasuk pembersihan tilam, rawatan penghalau hama dan pensterilan UV.",
      bg=BG(clip="uv", dim=.55), head=H("<b>7 langkah</b> penjagaan", k="BEREX ELITE", y=200),
      chips=chips(("Pembersihan tilam", "pembersihan"), ("Rawatan penghalau hama", "penghalau"), ("Pensterilan UV", "UV"), y=1180)),
    L(5, "Bagi pelanggan pelan sewaan yang layak, ada juga penukaran topper pada bulan ketiga puluh enam, tertakluk pada terma dan syarat.",
      media=M("topper", box=(90, 560, 900, 800)), head=H("Tukar topper<br><b>bulan ke-36</b>", y=150),
      note={"t": "*Pelanggan pelan sewaan yang layak. Tertakluk pada terma &amp; syarat.", "at": "tertakluk", "y": 1420}),
    L(6, "Jadi, masa nak bandingkan dua tilam, jangan bandingkan produk semata-mata. Tengok juga servis dan manfaat yang disertakan.",
      head=H("Banding <b>semua sekali</b>", y=200),
      items=items(("Produk", "produk", None), ("Servis", "servis", None), ("Manfaat", "manfaat", None), y=640)),
    L(7, "Kalau nak tahu pakej dan syarat yang terpakai untuk BEREX Elite, WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya terangkan pakej &amp; syaratnya."}),
])

# Video 9 (MOFU) — Perbandingan Elite dengan Prime II
V["s09"] = dict(title="Perbandingan Elite dengan Prime II", slug="elite-vs-prime2", mood="warm", lines=[
    L(1, "Kalau korang dah kenal BEREX Prime II, sekarang Coway ada BEREX Elite. Jadi, apa sebenarnya yang berbeza?",
      bg=BG("bilik", dim=.8, pos="50% 50%"), head=H("Prime II vs <b>Elite</b>", k="APA BEZA?", y=200)),
    L(2, "Okay, jom kita bandingkan tiga perkara.", cont=True,
      words=[W("<b>3</b> PERKARA", at=0.1, size=140, y=1250)]),
    L(3, "Pertama, pocket spring. Prime II menggunakan sistem tujuh zon, manakala Elite menggunakan sembilan zon.",
      bg=BG("pocket", dim=.8), head=H("1 · <b>Pocket spring</b>", y=200),
      items=items(("Prime II: 7 zon", "Prime", "II"), ("Elite: <b>9 zon</b>", "Elite", "E"), y=1150)),
    L(4, "Kedua, lateks asli. Untuk Prime II, dia menggunakan reka bentuk lima zon. Elite pula menggunakan sembilan zon.",
      head=H("2 · <b>Lateks asli</b>", y=200),
      items=items(("Prime II: 5 zon", "Prime", "II"), ("Elite: <b>9 zon</b>", "Elite", "E"), y=700)),
    L(5, "Ketiga, ketebalan. Prime II ialah tiga puluh tiga sentimeter, manakala Elite ialah tiga puluh enam sentimeter.",
      media=M("tebal", box=(60, 520, 960, 600)), head=H("3 · <b>Ketebalan</b>", y=150),
      items=items(("Prime II: 33 cm", "Prime", "II"), ("Elite: <b>36 cm</b>", "Elite", "E"), y=1180)),
    L(6, "Selain tu, Elite turut menggunakan PU foam sembilan zon, bersama lateks asli dan pocket spring sembilan zon.",
      head=H("Elite: <b>9 zon</b> pada 3 lapisan", y=170), media=LAYER,
      chips=chips(("PU foam 9 zon", "PU"), ("Lateks asli 9 zon", "lateks"), ("Pocket spring 9 zon", "pocket"), y=1180)),
    L(7, "Tapi adakah model yang lebih baru semestinya sesuai untuk semua orang? Tak semestinya.",
      bg=BG("posisi"), head=H("Yang baru<br><b>semestinya</b> sesuai?", y=200),
      words=[W("TAK SEMESTINYA", at="Tak", size=100, y=1300)]),
    L(8, "Sebab pilihan tilam tetap bergantung pada keselesaan masing-masing, posisi tidur, pilihan rasa lembut atau keras, dan juga bajet.",
      bg=BG("mengiring", dim=.85), head=H("Pilih ikut <b>diri sendiri</b>", y=200),
      chips=chips(("Keselesaan", "keselesaan"), ("Posisi tidur", "posisi"), ("Lembut atau keras", "lembut"), ("Bajet", "bajet"), y=1120)),
    L(9, "Kalau tengah pilih antara Prime II dengan Elite, tanya saya tentang perbezaan kedua-dua model ni. WhatsApp saya.",
      cta={"at": 0.1, "t": "Saya bantu pilih yang sesuai."}),
])

if __name__ == "__main__":
    for vid, d in V.items():
        spec = dict(id=vid, slug=d["slug"], title=f"{vid.upper()} — {d['title']}", mood=d["mood"],
                    theme=THEME, product=PRODUCT, clips=CLIPS, lines=d["lines"])
        (OUT / f"{vid}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
        print("tulis", OUT / f"{vid}.json")
