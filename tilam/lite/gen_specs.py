"""Jana spesifikasi 15 video Prime Lite -> tilam/b/l01..l15.json (dibina dengan tilam/build_b.py).

    python tilam/lite/gen_specs.py && python tilam/build_b.py l01
Fakta: laman rasmi Prime Lite + pengesahan ejen 6 Okt (lihat tilam/lite/analisis_dan_plan.md §5).
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "b"
A = "assets/tilam/primelite/"
A2 = "assets/tilam/prime2/"
PV = A + "video/coway-prime-lite-product-video3.mp4"
THEME = {"bg": "#0e2238", "bg2": "#2d5a86", "accent": "#9fd3f7", "accent2": "#d3ecff", "ink": "#0e2238"}
PRODUCT = {"name": "COWAY <b>PRIME LITE</b>", "sub": "Medium Firm · Queen &amp; King", "img": A + "prime-lite-panel1-desktop.jpg", "ctaSize": 80}
CLIPS = {
    "sheets": {"src": PV, "from": 30.0, "to": 33.6}, "cooling": {"src": PV, "from": 34.0, "to": 37.6},
    "zone5": {"src": PV, "from": 38.0, "to": 45.8}, "topper": {"src": PV, "from": 51.0, "to": 56.6},
    "wake": {"src": PV, "from": 10.0, "to": 13.0}, "room": {"src": PV, "from": 59.0, "to": 61.8},
    "positions": {"src": A + "prime-lite-video2.mp4", "from": 0, "to": 5.0},
    "press": {"src": A + "prime-lite-video3.mp4", "from": 0, "to": 3.6},
    "kid": {"src": A + "prime-lite-video3.mp4", "from": 4.0, "to": 9.0},
}
IMG = {
    "unzip": A + "white-mattress-topper-getting-unzipped-from-a-blue-mattress-to-get-changed.jpg",
    "layers": A + "an-image-of-layers-for-the-coway-prime-lite-series-mattress-with-descriptions.png",
    "zones": A + "an-image-showing-a-side-sleeper-and-a-back-sleeper-on-the-coway-prime-lite-series-mattress-with-5-zones-separated.png",
    "motion": A + "coway-prime-lite-with-superior-motion-cancellation.jpg",
    "gap": A + "an-image-of-a-gap-between-the-bed-and-the-wooden-floor-with-the-measurement-of-12cm-and-a-robot-vacuum-cleaner-at-the-side.jpg",
    "corners": A + "high-view-of-the-coway-prime-lite-series-mattress-on-a-wooden-floor-featuring-its-round-corners.jpg",
    "fabric": A + "an-image-of-high-quality-durable-blue-fabric-for-the-coway-prime-lite-series-mattress.jpg",
    "closeup": A + "a-close-up-view-of-the-coway-prime-lite-series-mattress-white-fabric.jpg",
    "care": A + "coway-mattress-care-service-for-prime-lite.jpg",
    "step1": A + "first-step-of-coway-seven-step-mattress-care-service-dust-level-measuring.jpg",
    "step5": A + "fifth-step-of-coway-seven-step-mattress-care-service-mattress-cleaning.jpg",
    "step7": A + "seventh-step-of-coway-seven-step-mattress-care-service-ultraviolet-sterilisation.jpg",
    "family": A + "family-of-three-laying-down-on-the-coway-prime-lite-series-mattress-without-any-bedsheets.jpg",
    "panel1": A + "prime-lite-panel1-desktop.jpg", "wakeup": A + "wake-up-effortlessly-with-coway-prime-lite.jpg",
    "blueframe": A + "blue-bedframe-against-the-wall-with-two-pillows-against-it-and-a-lamp-on-the-side.jpg",
    "p2zones": A2 + "coway-prime2-7-zone-pocket-spring.png", "p2bed": A2 + "prime2-panel3-desktop.jpg",
}
MB = [0, 600, 1080, 608]          # kotak media lebar penuh 16:9
TOPNOTE = "*Untuk pelanggan sewa. Tertakluk kepada terma &amp; syarat."
SVCNOTE = "*Untuk pakej termasuk servis."


def L(i, text, **scene): return {"id": f"{i:02d}", "text": text, "scene": scene}
def H(t=None, k=None, s=None, y=170, **kw): return dict({k2: v for k2, v in [("t", t), ("k", k), ("s", s)] if v}, y=y, **kw)
def M(img=None, clip=None, box=MB, **kw): return dict({"img": IMG[img]} if img else {"clip": clip}, box=box, **kw)
def chips(*xs, y=1260, gap=105): return [{"t": t, "at": at, "y": y + i * gap} for i, (t, at) in enumerate(xs)]
def W(t, at=0.05, size=120, y=640, **kw): return dict(t=t, at=at, size=size, y=y, **kw)
def item(t, at, y, icon=None, x=False): return dict({"t": t, "at": at, "y": y}, **({"icon": icon} if icon else {}), **({"x": True} if x else {}))
def cta(t, img=None): return {"cta": dict({"at": 0.1, "t": t}, **({"img": IMG[img]} if img else {}))}


V = {}
V["l01"] = ("3 sebab ramai pilih Prime Lite", "3-sebab-ramai-pilih-prime-lite", "calm", ["r1", "r6"], [
    L(1, "Tilam dua belas inci, topper ber-zip, servis Coway. Biar betul? Ni tiga sebab ramai pilih Coway Prime Lite.",
      bg={"clip": "sheets", "dim": 1}, head=H("3 sebab<br><b>ramai pilih</b>", k="COWAY PRIME LITE", y=200, at="tiga sebab")),
    L(2, "Satu, pocket spring lima zon. Sokong ikut bentuk badan, dari kepala sampai kaki.",
      head=H("Pocket spring <b>5 zon</b>", k="SEBAB 1"), media=M(clip="zone5")),
    L(3, "Dan bila pasangan bergerak, you kurang terasa.", cont=True, chips=chips(("Kurang gangguan pasangan", "pasangan"))),
    L(4, "Dua, tebal dua belas inci. Tidur rasa macam dekat hotel.",
      head=H("<b>12 inci</b> tebal", k="SEBAB 2"), media=M(clip="press", box=[90, 560, 900, 760]), chips=chips(("Rasa macam hotel", "hotel"), y=1400)),
    L(5, "Tiga, topper dia ber-zip. Boleh tanggal, cuci di rumah, dan ditukar percuma tiga tahun sekali.",
      head=H("Topper <b>ber-zip</b>", k="SEBAB 3"), media=M("unzip", box=[190, 520, 700, 700]),
      chips=chips(("Cuci di rumah", "cuci"), ("Tukar percuma 3 tahun sekali*", "ditukar"), y=1260), note={"t": TOPNOTE, "y": 1480, "at": "ditukar"}),
    L(6, "Nak tidur atas tilam macam ni? WhatsApp saya.", **cta("Tanya dulu. Tak ada paksa.")),
])
V["l02"] = ("Patutlah ramai order", "patutlah-ramai-order", "drive", ["r3"], [
    L(1, "Patutlah lately ni ramai order tilam Coway Prime Lite.", words=[W("PATUTLAH", size=130, y=560), W("RAMAI <b>ORDER.</b>", at="ramai", size=130, y=740)]),
    L(2, "Tebal dua belas inci.", bg={"clip": "room", "dim": 1}, words=[W("<b>12 INCI</b> TEBAL", size=120, y=760)]),
    L(3, "Pocket spring lima zon, untuk sokong tulang belakang.", head=H("Pocket spring <b>5 zon</b>"), media=M(clip="zone5")),
    L(4, "Permukaan fabrik penyejuk, tidur lebih nyaman.", head=H("Fabrik <b>penyejuk</b>"), media=M(clip="cooling")),
    L(5, "Topper ber-zip, boleh tanggal dan cuci di rumah.", head=H("Topper <b>ber-zip</b>"), media=M("unzip", box=[190, 520, 700, 700])),
    L(6, "Walaupun barang besar, penghantaran dan pemasangan percuma. Sabah dan Sarawak pun termasuk.",
      words=[W("HANTAR &amp; PASANG", at="penghantaran", size=100, y=600), W("<b>PERCUMA.</b>", at="percuma", size=150, y=760),
             W("Sabah &amp; Sarawak termasuk", at="Sabah", size=62, y=960, anim="up")]),
    L(7, "Nak tahu kenapa ramai pilih? WhatsApp saya.", **cta("Hantar &amp; pasang percuma.")),
])
V["l03"] = ("Anak terkencing? Buka zip je", "anak-terkencing-buka-zip", "warm", ["#87", "r5"], [
    L(1, "Anak terkencing atas tilam. Nak cuci macam mana?",
      comment={"t": "Kalau anak terkencing atas tilam, korang biasanya cuci macam mana?", "src": "Threads · 2025", "y": 600, "at": 0.1}),
    L(2, "Kalau tilam biasa, memang pening. Nak basuh satu tilam, tak boleh.", words=[W("TILAM BIASA?", size=120, y=620), W("<b>PENING.</b>", at="pening", size=160, y=800)]),
    L(3, "Prime Lite lain. Topper dia ber-zip, dan boleh ditanggal sepenuhnya.", head=H("Topper <b>ber-zip</b>", k="COWAY PRIME LITE"), media=M("unzip", box=[190, 520, 700, 700])),
    L(4, "Jadi yang dicuci, topper je. Cuci di rumah, bukan seluruh tilam.", cont=True, chips=chips(("Cuci topper di rumah", "cuci di rumah"), ("Bukan seluruh tilam", "bukan"), y=1260)),
    L(5, "Fabrik rangka pun tahan lama, dan mudah dibersihkan.", head=H("Fabrik <b>mudah dibersihkan</b>"), media=M("fabric")),
    L(6, "Dan setiap empat bulan, technician Coway datang untuk servis penjagaan tilam.",
      head=H("Servis <b>setiap 4 bulan*</b>"), media=M("care"), note={"t": SVCNOTE, "y": 1260, "at": "empat"}),
    L(7, "Ada anak kecil kat rumah? WhatsApp saya.", **cta("Topper zip, cuci di rumah.", "family")),
])
V["l04"] = ("Prime Lite vs Prime II: beza 30 saat", "lite-vs-prime2-30-saat", "calm", ["r4"], [
    L(1, "Prime Lite atau Prime 2? Ni beza dia dalam tiga puluh saat.",
      words=[W("PRIME <b>LITE</b>", size=130, y=520), W("atau", at="atau", size=70, y=690, anim="up"), W("PRIME <b>II</b>?", at="Prime 2", size=130, y=790)]),
    L(2, "Spring. Prime Lite lima zon. Prime 2 tujuh zon.",
      head=H("Spring", k="1"), items=[item("Prime Lite: <b>5 zon</b>", "Lite", 560, "L"), item("Prime II: <b>7 zon</b>", "Prime 2", 710, "II")]),
    L(3, "Lapisan. Prime Lite ada fabrik penyejuk, foam berliang dan felt. Prime 2 tambah latex asli dan sabut kelapa.",
      head=H("Lapisan", k="2"), items=[item("Lite: fabrik sejuk, foam berliang, felt", "Lite", 560, "L"), item("II: tambah <b>latex asli</b> &amp; <b>sabut kelapa</b>", "Prime 2", 710, "II")]),
    L(4, "Kekerasan. Prime Lite medium firm, sesuai untuk banyak cara tidur. Prime 2, pilih soft atau firm.",
      head=H("Kekerasan", k="3"), items=[item("Lite: <b>Medium Firm</b> all-rounder", "Lite", 560, "L"), item("II: pilih <b>Soft</b> atau <b>Firm</b>", "Prime 2", 710, "II")]),
    L(5, "Ketebalan. Prime Lite dua belas inci. Prime 2 tiga belas inci.",
      head=H("Ketebalan", k="4"), items=[item("Lite: <b>12 inci</b>", "Lite", 560, "L"), item("II: <b>13 inci</b>", "Prime 2", 710, "II")]),
    L(6, "Rangka. Prime Lite fabrik biru muda. Prime 2 velvet biru gelap, atau kulit PU kelabu gelap.",
      head=H("Rangka", k="5"), items=[item("Lite: fabrik <b>biru muda</b>", "Lite", 560, "L"), item("II: velvet biru gelap / PU kelabu", "Prime 2", 710, "II")]),
    L(7, "Dua-dua dapat topper boleh tukar, dan servis penjagaan tilam tujuh langkah.",
      words=[W("DUA-DUA <b>DAPAT:</b>", size=96, y=520)], chips=chips(("Topper boleh ditukar", "topper"), ("Servis 7 langkah", "servis"), y=760)),
    L(8, "Tak pasti yang mana sesuai? WhatsApp saya, kita pilih sama-sama.", **cta("Kita pilih sama-sama.")),
])
V["l05"] = ("Lite atau Prime II? Pilih dalam 10 saat", "lite-atau-prime2-pilih", "drive", ["#57", "#70"], [
    L(1, "Tengah survey tilam Coway? Jawab tiga soalan ni.", words=[W("SURVEY TILAM COWAY?", size=80, y=600), W("JAWAB <b>3 SOALAN.</b>", at="Jawab", size=110, y=760)]),
    L(2, "Satu. Nak latex asli dan spring tujuh zon? Kalau ya, pilih Prime 2.",
      head=H("Nak latex asli<br>&amp; <b>7 zon</b>?", k="SOALAN 1", y=220), items=[item("Ya: pilih <b>Prime II</b>", "Kalau", 760, "II")]),
    L(3, "Dua. Nak pilih sendiri, lebih lembut atau lebih keras? Prime 2 ada Soft dan Firm.",
      head=H("Nak pilih sendiri<br><b>soft atau firm</b>?", k="SOALAN 2", y=220), items=[item("Ya: pilih <b>Prime II</b>", "Prime 2", 760, "II")]),
    L(4, "Tiga. Kongsi tilam dengan pasangan yang cara tidurnya lain? Prime Lite medium firm, all-rounder.",
      head=H("Cara tidur<br><b>lain-lain</b>?", k="SOALAN 3", y=220), items=[item("Ya: pilih <b>Prime Lite</b>", "Prime Lite", 760, "L")], media=M(clip="positions", box=[90, 940, 900, 506])),
    L(5, "Dua-dua ada topper boleh tukar, servis setiap empat bulan, dan hantar pasang percuma.",
      words=[W("DUA-DUA <b>ADA:</b>", size=96, y=480)],
      chips=chips(("Topper boleh ditukar", "topper"), ("Servis setiap 4 bulan*", "servis"), ("Hantar &amp; pasang percuma", "hantar"), y=700),
      note={"t": SVCNOTE, "y": 1080, "at": "servis"}),
    L(6, "Masih tak pasti? WhatsApp saya.", **cta("Jawab 3 soalan, saya cadangkan.")),
])
V["l06"] = ("5 zon vs 7 zon", "5-zon-vs-7-zon", "calm", ["#62", "#66"], [
    L(1, "Lima zon, tujuh zon. Ni bukan nombor kosong.", words=[W("5 ZON? 7 ZON?", size=130, y=600), W("Bukan nombor kosong.", at="Ni", size=70, y=790, anim="up")]),
    L(2, "Zon maksudnya, spring dibahagi ikut bahagian badan. Ada yang lebih lembut, ada yang lebih padu.",
      head=H("Apa itu <b>zon</b>?"), media=M("zones", bgc="#000")),
    L(3, "Prime Lite ada lima zon. Kepala, bahu, pinggang, pinggul, dan kaki.",
      head=H("Prime Lite: <b>5 zon</b>"), media=M(clip="zone5"),
      chips=[{"t": "Kepala · Bahu · Pinggang · Pinggul · Kaki", "at": "Kepala", "y": 1260}]),
    L(4, "Prime 2 ada tujuh zon. Bahagian kaki dipecahkan lagi, kepada lutut, betis, dan buku lali.",
      head=H("Prime II: <b>7 zon</b>"), media=M("p2zones", bgc="#cfd9ea", kb="none"),
      chips=[{"t": "Kaki dipecah: lutut · betis · buku lali", "at": "kaki", "y": 1260}]),
    L(5, "Dua-dua guna pocket spring, jadi kurang gangguan bila pasangan bergerak.",
      words=[W("DUA-DUA", size=110, y=600), W("<b>POCKET SPRING.</b>", at="pocket", size=110, y=760)], chips=chips(("Kurang gangguan pasangan", "kurang"), y=980)),
    L(6, "Nak tahu yang mana sesuai dengan badan you? WhatsApp saya.", **cta("Tanya yang sesuai dengan badan you.")),
])
V["l07"] = ("Suami mengiring, isteri terlentang", "suami-mengiring-isteri-terlentang", "warm", ["#23", "#164"], [
    L(1, "Suami tidur mengiring. Isteri tidur terlentang. Nak pilih soft ke firm?",
      words=[W("Suami: <b>mengiring.</b>", size=96, y=520, anim="up"), W("Isteri: <b>terlentang.</b>", at="Isteri", size=96, y=670, anim="up"),
             W("SOFT KE FIRM?", at="Nak", size=120, y=860)]),
    L(2, "Ramai pening bab ni. Ni antara soalan yang paling kerap ditanya.",
      comment={"t": "mana paling keras mana satu yg bagus soft n firm apa beza", "src": "TikTok · 2026", "y": 620, "at": 0.1, "tag": "SOALAN"}),
    L(3, "Prime Lite datang dengan satu kekerasan, medium firm. Jenis all-rounder.",
      head=H("<b>Medium Firm</b>", k="COWAY PRIME LITE", s="All-rounder"), media=M(clip="positions")),
    L(4, "Sesuai untuk banyak posisi tidur. Mengiring, terlentang, atau tukar-tukar sepanjang malam.",
      cont=True, chips=chips(("Mengiring", "Mengiring"), ("Terlentang", "terlentang"), ("Tukar-tukar sepanjang malam", "tukar"), y=1250)),
    L(5, "Spring lima zon sokong ikut bentuk badan masing-masing. Bila seorang pusing, seorang lagi kurang terasa.",
      head=H("Spring <b>5 zon</b>", s="Ikut bentuk badan masing-masing"), media=M("zones", bgc="#000"), chips=chips(("Kurang gangguan pasangan", "pusing"))),
    L(6, "Satu tilam, dua cara tidur. Tak perlu bertekak.", words=[W("SATU TILAM.", size=130, y=560), W("<b>DUA CARA TIDUR.</b>", at="dua", size=110, y=730),
                                                               W("Tak perlu bertekak.", at="Tak", size=70, y=920, anim="up")]),
    L(7, "Nak cuba tilam all-rounder ni? WhatsApp saya.", **cta("Satu tilam untuk berdua.", "family")),
])
V["l08"] = ("12 inci: tidur rasa hotel", "12-inci-rasa-hotel", "calm", ["r1", "r5"], [
    L(1, "Siapa suka tilam tebal, tidur rasa macam dekat hotel?", bg={"clip": "wake", "dim": 1}, head=H("Suka tilam <b>tebal</b>?", y=220, s="Tidur rasa macam hotel")),
    L(2, "Coway Prime Lite tebal dua belas inci.", words=[W("<b>12 INCI</b>", size=180, y=330)], media=M(clip="press", box=[90, 640, 900, 760])),
    L(3, "Dalam dua belas inci tu, ada empat lapisan.", head=H("<b>4 lapisan</b>", k="DALAM 12 INCI"), media=M("layers", bgc="#000", box=[0, 560, 1080, 694])),
    L(4, "Fabrik penyejuk di atas, dan foam berliang untuk aliran udara.", cont=True, chips=chips(("Fabrik penyejuk", "Fabrik"), ("Foam berliang", "foam"), y=1290)),
    L(5, "Pocket spring lima zon, dan felt di bawah untuk lindungi lapisan.", cont=True, chips=chips(("Pocket spring 5 zon", "Pocket"), ("Felt pelindung", "felt"), y=1490)),
    L(6, "Nak lagi tebal? Prime 2 tiga belas inci, dengan latex dan sabut kelapa.",
      head=H("Nak lagi tebal?", s="Prime II: 13 inci + latex &amp; sabut kelapa", y=200), media=M("p2bed")),
    L(7, "Nak tidur macam hotel setiap malam? WhatsApp saya.", **cta("Rasa hotel, setiap malam.")),
])
V["l09"] = ("Robot vakum masuk bawah katil", "robot-vakum-bawah-katil", "calm", ["#93", "#89"], [
    L(1, "Bawah katil you penuh habuk? Robot vakum tak boleh masuk?", words=[W("BAWAH KATIL", size=120, y=560), W("<b>PENUH HABUK?</b>", at="penuh", size=120, y=720)]),
    L(2, "Rangka Prime Lite ada jarak dua belas sentimeter dari lantai.", head=H("Jarak <b>12 cm</b>", k="RANGKA PRIME LITE"), media=M("gap")),
    L(3, "Cukup untuk robot vakum masuk, dan bersihkan bawah katil.", cont=True, chips=chips(("Robot vakum boleh masuk", "robot"), ("Bawah katil bersih", "bersihkan"))),
    L(4, "Fabrik rangka pula tahan lama, dan mudah dibersihkan.", head=H("Fabrik <b>mudah dibersihkan</b>"), media=M("fabric")),
    L(5, "Bucu dia lembut dan melengkung.", head=H("Bucu <b>lembut</b>"), media=M("corners")),
    L(6, "Untuk tilam pula, servis penjagaan Coway setiap empat bulan.", head=H("Servis tilam<br><b>setiap 4 bulan*</b>"), media=M("care"),
      note={"t": SVCNOTE, "y": 1260, "at": "empat"}),
    L(7, "Rumah kemas, tidur pun bersih. WhatsApp saya.", **cta("Rumah kemas, tidur pun bersih.")),
])
V["l10"] = ("Anak lasak? Bucu lembut", "anak-lasak-bucu-lembut", "warm", ["#164", "#165"], [
    L(1, "Anak lari keliling katil. Terhantuk bucu, menangis lagi.", bg={"clip": "kid", "dim": 1}, head=H("Anak <b>lasak?</b>", y=200)),
    L(2, "Rangka Prime Lite dibalut fabrik lembut, dengan bucu melengkung.", head=H("Bucu <b>melengkung</b>", k="RANGKA PRIME LITE"), media=M("corners")),
    L(3, "Untuk lindungi dari terhantuk secara tak sengaja.", cont=True, chips=chips(("Fabrik lembut", "lindungi"), ("Lindungi dari terhantuk", "terhantuk"))),
    L(4, "Anak melompat atas katil? Pocket spring lima zon bergerak secara individu.", head=H("Spring <b>bergerak sendiri</b>"), media=M(clip="kid", box=[140, 520, 800, 900])),
    L(5, "Jadi bila anak bergerak, mak ayah kurang terasa.", cont=True, chips=chips(("Mak ayah kurang terasa", "kurang"), y=1470)),
    L(6, "Topper pula ber-zip, boleh tanggal dan cuci di rumah.", head=H("Topper <b>ber-zip</b>"), media=M("unzip", box=[190, 520, 700, 700]), chips=chips(("Cuci di rumah", "cuci"))),
    L(7, "Untuk keluarga yang aktif. WhatsApp saya.", **cta("Untuk keluarga yang aktif.", "family")),
])
V["l11"] = ("Pasangan pusing, you terjaga?", "pasangan-pusing-terjaga", "calm", ["#164", "#166"], [
    L(1, "Dia pusing, you terjaga. Setiap malam.", words=[W("DIA PUSING.", size=130, y=560), W("YOU <b>TERJAGA.</b>", at="you", size=130, y=730), W("Setiap malam.", at="Setiap", size=70, y=910, anim="up")]),
    L(2, "Tilam spring biasa, springnya bersambung. Seorang bergerak, gegaran merebak.",
      head=H("Spring biasa:<br><b>bersambung</b>", y=200), items=[item("Seorang bergerak, <b>gegaran merebak</b>", "Seorang", 640, x=True)]),
    L(3, "Prime Lite guna pocket spring. Setiap spring dalam poket sendiri, fleksibel ikut bentuk badan.",
      head=H("Pocket spring<br><b>dalam poket sendiri</b>", k="COWAY PRIME LITE"), media=M("motion")),
    L(4, "Pindahan gerakan dikurangkan, jadi you boleh tidur lena dengan orang tersayang.", cont=True, chips=chips(("Kurang pindahan gerakan", "Pindahan"), ("Tidur lena berdua", "lena"))),
    L(5, "Medium firm pula sesuai untuk dua cara tidur yang berbeza.", head=H("<b>Medium Firm</b>", s="Sesuai cara tidur berbeza"), media=M(clip="positions")),
    L(6, "Nak tidur lena berdua? WhatsApp saya.", **cta("Tidur lena berdua.")),
])
V["l12"] = ("Bilik panas, kipas satu je", "bilik-panas-cooling", "calm", ["#160", "#161", "#162"], [
    L(1, "Malaysia ni panas. Bilik tak ada aircond, kipas satu je.",
      comment={"t": "Malaysia ni hangatt benor, maaf cakap, memang I akan grab semua yg ada perkataan \"cooling\"", "src": "Threads · 2026", "y": 600, "at": 0.1}),
    L(2, "Tilam pun boleh jadi punca bahang.", words=[W("TILAM PUN", size=120, y=640), W("<b>BAHANG?</b>", at="bahang", size=160, y=800)]),
    L(3, "Prime Lite guna cooling ticking, fabrik dengan benang penyejuk, supaya permukaan tilam kekal sejuk.",
      head=H("<b>Cooling ticking</b>", k="COWAY PRIME LITE"), media=M(clip="cooling"), chips=chips(("Permukaan kekal sejuk", "kekal"))),
    L(4, "Di bawahnya, foam berliang untuk aliran udara antara lapisan.", head=H("Foam <b>berliang</b>"), media=M("layers", bgc="#000", box=[0, 560, 1080, 694]),
      chips=chips(("Udara mengalir", "aliran"), y=1300)),
    L(5, "Jujurnya, tilam bukan aircond. Tapi ia bantu kurangkan rasa bahang.",
      words=[W("JUJURNYA:", size=90, y=560), W("TILAM ≠ AIRCOND.", at="bukan", size=104, y=710), W("Tapi <b>kurang bahang.</b>", at="Tapi", size=90, y=880, anim="up")]),
    L(6, "Nak tidur lebih selesa malam ni? WhatsApp saya.", **cta("Tidur lebih selesa.")),
])
V["l13"] = ("Topper tukar percuma, tilam kekal segar", "topper-tukar-percuma", "calm", ["#73", "#117"], [
    L(1, "Tilam lama-lama rasa nipis? Kena beli baru?", words=[W("TILAM DAH NIPIS?", size=110, y=600), W("Kena beli <b>baru?</b>", at="Kena", size=96, y=770, anim="up")]),
    L(2, "Dengan Prime Lite, tak perlu. Topper dia ber-zip, dan boleh ditanggal sepenuhnya.", head=H("Topper <b>ber-zip</b>", k="COWAY PRIME LITE"), media=M(clip="topper")),
    L(3, "Untuk pelanggan sewa, topper ditukar percuma, tiga tahun sekali.", cont=True,
      chips=chips(("Tukar percuma 3 tahun sekali*", "percuma"), y=1270), note={"t": TOPNOTE, "y": 1400, "at": "percuma"}),
    L(4, "Jadi lapisan atas sentiasa segar, tanpa perlu buang tilam.", words=[W("LAPISAN ATAS <b>SEGAR.</b>", size=96, y=620), W("Tak perlu buang tilam.", at="tanpa", size=70, y=790, anim="up")]),
    L(5, "Topper dia juga ada lapisan lembut, untuk tidur yang lebih selesa.", head=H("Lapisan <b>lembut</b>"), media=M("closeup")),
    L(6, "Nak tilam yang kekal segar? WhatsApp saya.", **cta("Tukar topper, bukan tilam.")),
])
V["l14"] = ("Rumah pertama, set biru lembut", "rumah-pertama-set-biru", "warm", ["#2", "#57"], [
    L(1, "Rumah pertama. Bilik masih kosong.", bg={"img": IMG["blueframe"], "dim": 1}, head=H("Rumah <b>pertama?</b>", y=700)),
    L(2, "Prime Lite datang dengan rekaan biru muda yang minimalis, padan dengan mana-mana bilik.",
      bg={"img": IMG["panel1"], "pos": "60% 50%", "dim": 1}, head=H("Biru muda,<br><b>minimalis</b>", y=200)),
    L(3, "Boleh ambil tilam sahaja, atau set dengan rangka katil.", head=H("Tilam atau <b>set lengkap</b>"), media=M("wakeup"),
      chips=chips(("Tilam sahaja", "tilam sahaja"), ("Tilam + rangka katil", "rangka"))),
    L(4, "Ada saiz Queen dan King.", cont=True, chips=chips(("Queen &amp; King", "Queen"), y=1470)),
    L(5, "Penghantaran dan pemasangan percuma, termasuk Sabah dan Sarawak.",
      words=[W("HANTAR &amp; PASANG", size=100, y=600), W("<b>PERCUMA.</b>", at="percuma", size=150, y=760), W("Sabah &amp; Sarawak termasuk", at="Sabah", size=62, y=960, anim="up")]),
    L(6, "Mula rumah baru dengan tidur yang betul. WhatsApp saya.", **cta("Mula rumah baru dengan tidur yang betul.", "blueframe")),
])
V["l15"] = ("Tilam Lite, servis tetap penuh", "lite-servis-tetap-penuh", "calm", ["#93", "#114"], [
    L(1, "Prime Lite. Lite tu maksudnya servis pun lite?", words=[W("PRIME <b>LITE</b>…", size=120, y=600), W("SERVIS PUN LITE?", at="servis", size=110, y=770, strike=1.9)]),
    L(2, "Tak. Prime Lite dapat servis penjagaan tilam tujuh langkah, sama macam model lain.", head=H("Servis <b>7 langkah</b>", k="SAMA MACAM MODEL LAIN"), media=M("care")),
    L(3, "Ukur tahap habuk, bersihkan rangka, dan bersihkan tilam.", head=H("Habuk, rangka<br>&amp; <b>tilam</b>"), media=M("step1"), chips=chips(("Ukur tahap habuk", "Ukur"), ("Bersihkan rangka &amp; tilam", "rangka"))),
    L(4, "Penghalau hama, sterilisasi UV, dan nyahkuman fogging.", head=H("Hama, <b>UV</b><br>&amp; fogging"), media=M("step7"),
      chips=chips(("Penghalau hama", "Penghalau"), ("Sterilisasi UV", "UV"), ("Nyahkuman fogging", "fogging"))),
    L(5, "Setiap empat bulan, untuk pakej termasuk servis.", words=[W("SETIAP", size=110, y=620), W("<b>4 BULAN.</b>", at="empat", size=160, y=780)], note={"t": SVCNOTE, "y": 1020, "at": "pakej"}),
    L(6, "Tilam Lite, servis tetap penuh. WhatsApp saya.", **cta("Tilam Lite, servis tetap penuh.")),
])

for vid, (title, slug, mood, pain, lines) in V.items():
    spec = {"id": vid, "slug": slug, "title": f"{vid.upper()} — {title}", "pain": pain, "mood": mood,
            "theme": THEME, "product": PRODUCT, "clips": CLIPS, "lines": lines}
    (OUT / f"{vid}.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1))
print(len(V), "spec ditulis")
