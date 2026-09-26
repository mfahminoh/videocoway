"""Skrip VO penuh Neo Plus + garis masa.

    python neoplus_full/timeline.py

Menulis:
  neoplus_full/lines.json   slot setiap baris (untuk generate_vo.py & mix.py)
  neoplus_full/lines.js     salinan yang sama untuk index.html (window.LINES)
  neoplus_full/neoplus_full.srt

Tempoh setiap baris dianggar daripada panjang teks (CPS aksara/saat + jeda tanda baca).
index.html dan audio.py guna fungsi anggaran yang sama (at(i, 'perkataan')) untuk
meletakkan animasi & SFX tepat pada perkataan yang disebut.
"""
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent

CPS = 16.5          # aksara sesaat (Yasmin, kadar +8%)
P_STOP = 0.35       # jeda selepas . ? ! …
P_COMMA = 0.12      # jeda selepas ,
GAP = 0.35          # senyap antara baris
START = 0.3
HOLD = 2.2          # tahan penutup selepas baris terakhir

# (teks VO, teks sarikata jika berbeza, jeda tambahan sebelum baris)
SCRIPT = [
    # ---------- HOOK ----------
    ("Mak ayah dah lama teringin nak ada penapis air dekat rumah?", None, 0),
    ("Atau mungkin mak dekat kampung sendiri pernah cakap,", None, 0),
    ("Kalau ada penapis air dekat kampung, kan senang…", None, 0),
    # ---------- BODY ----------
    ("Kita yang duduk jauh ni, kadang-kadang rasa serba salah.", None, .3),
    ("Dekat rumah sendiri, air panas, air sejuk, semua dah ada.", None, 0),
    ("Tapi dekat rumah mak ayah di kampung, masih kena masak air, tunggu air panas, atau isi air dalam bekas macam biasa.", None, 0),
    ("Dah lama kita fikir nak bantu. Nak belikan penapis air untuk mak ayah.", None, 0),
    ("Mak ayah tak perlukan produk paling canggih. Tapi apa yang paling senang untuk mak ayah guna.", None, .2),
    ("Sebab bagi kita, model yang banyak elektronik mungkin nampak lagi moden.", None, 0),
    ("Tapi bagi mak ayah, yang dah biasa dengan barang-barang manual…", None, 0),
    ("Pulas tombol suhu, tekan tuil, terus keluar air. Itu yang lagi senang.", None, 0),
    ("Tak perlu pening tengok nombor LED.", None, 0),
    ("Takkan nak ambil air pun, kena ambil spek membaca dulu?", None, 0),
    ("Yang penting, air panas, air sejuk, dan air biasa, semuanya dah tersedia bila diperlukan.", None, .2),
    ("Nak buat kopi? Tekan. Nak buat teh? Tekan. Nak bancuh susu? Air panas dah tersedia.", None, 0),
    ("Dan sebagai anak, kita pun kena fikir satu lagi benda. Bajet mampu milik.", None, .2),
    ("Sebab kalau adik-beradik nak kongsi bayar pun, boleh.", None, 0),
    ("Tahun ni kita bayar. Tahun depan, mungkin abang pula. Tahun seterusnya, adik pula.", None, 0),
    ("Gilir-gilir. Jadi tak terasa sangat membebankan seorang.", None, 0),
    # ---------- SOLUTION ----------
    ("Kalau untuk mak ayah dekat kampung, salah satu model yang boleh dipertimbangkan ialah, Coway Neo Plus.", None, .4),
    ("Ada tiga suhu air. Panas, sejuk, dan suhu bilik.", None, 0),
    ("Saiz pun sesuai untuk keluarga kecil.", None, 0),
    ("Kalau dekat rumah mak ayah cuma dua orang, atau ada adik yang masih tinggal bersama, tak lah perlukan model dengan tangki yang terlalu besar.", None, 0),
    ("Yang penting, cukup, mudah, dan praktikal untuk kegunaan harian.", None, 0),
    ("Dan sekarang, Neo Plus ni ada harga promosi.", None, .3),
    ("Serendah lima puluh sembilan ringgit sebulan. Jimat empat puluh lima ringgit, dari harga asal seratus empat ringgit.",
     "Serendah RM59 sebulan. Jimat RM45, dari harga asal RM104.", 0),
    ("Dan ada double promo. Tujuh bulan pertama, cuma dua puluh ringgit sebulan!",
     "Dan ada double promo. 7 bulan pertama, cuma RM20 sebulan!", 0),
    ("Penghantaran dan pemasangan pun percuma.", None, 0),
    ("Jadi kalau memang dah lama terfikir nak belikan penapis air untuk mak ayah…", None, .3),
    ("mungkin sekarang, masa yang sesuai untuk buatkan hidup mereka sedikit lebih mudah.", None, 0),
    ("Klik WhatsApp sekarang, untuk tanya detail.", None, 0),
]


def est(text):
    """Anggaran tempoh bercakap (saat) untuk teks."""
    stops = len(re.findall(r"[.?!…](?=\s)", text))
    commas = text.count(",")
    return len(text) / CPS + stops * P_STOP + commas * P_COMMA


def build():
    t = START
    rows = []
    for i, (vo, sub, extra) in enumerate(SCRIPT):
        if i:
            t += GAP + extra
        d = round(est(vo) / 0.05) * 0.05
        rows.append({"id": f"{i + 1:02d}", "start": round(t, 2), "end": round(t + d, 2), "text": vo, **({"sub": sub} if sub else {})})
        t += d
    return rows, round(t + HOLD, 2)


def at(rows, i, word=None, occurrence=1):
    """Masa (saat) perkataan `word` disebut dalam baris i (0-based). Tanpa word -> mula baris."""
    r = rows[i]
    if word is None:
        return r["start"]
    idx = -1
    for _ in range(occurrence):
        idx = r["text"].index(word, idx + 1)
    k = (r["end"] - r["start"]) / est(r["text"])
    return round(r["start"] + est(r["text"][:idx]) * k, 3)


def ts(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


if __name__ == "__main__":
    rows, dur = build()
    body = "[\n" + ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in rows) + "\n]\n"
    (HERE / "lines.json").write_text(body)
    (HERE / "lines.js").write_text(
        "// Dijana oleh timeline.py — jangan edit terus.\n"
        f"window.LINES = {body.strip()};\nwindow.DURATION = {dur};\n"
        f"window.TIMING = {{CPS: {CPS}, P_STOP: {P_STOP}, P_COMMA: {P_COMMA}}};\n")
    with open(HERE / "neoplus_full.srt", "w") as f:
        for n, r in enumerate(rows, 1):
            f.write(f"{n}\n{ts(r['start'])} --> {ts(r['end'])}\n{r.get('sub', r['text'])}\n\n")
    for r in rows:
        print(r["id"], f"{r['start']:6.2f}-{r['end']:6.2f}", r["text"][:60])
    print("DURATION", dur)
