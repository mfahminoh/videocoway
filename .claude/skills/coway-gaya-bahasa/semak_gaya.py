#!/usr/bin/env python3
"""Penyemak gaya bahasa copy Coway (stdlib sahaja).

  python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py fail.md [fail2.txt ...]   # semak fail
  echo "teks" | python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py -          # semak stdin
  python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py --bank ads/autopilot/bank.json [--status DRAF]
  python3 .claude/skills/coway-gaya-bahasa/semak_gaya.py --senarai                  # cetak senarai frasa kaku

Keluar dengan kod 1 jika ada isu MERAH (frasa kaku/terjemahan). KUNING = amaran (ayat panjang, emoji banyak, "anda").
Baris T&C ("*Tertakluk ...") tidak disemak.
"""
from __future__ import annotations

import json
import re
import sys

# frasa kaku / terjemahan -> ganti yang lebih natural. Huruf kecil; padanan ikut sempadan perkataan.
KAKU = {
    "jom kenali": "terus sebut produk: \"Ni Coway NeoN.\"",
    "kenali coway": "\"Ni Coway NeoN.\" / \"Coway NeoN ni...\"",
    "apa kata kenali": "\"Cuba tengok Coway NeoN.\"",
    "pilihan penapis air untuk": "sebut manfaat terus: \"senang nak minum air\"",
    "kemudahan air minuman": "\"senang nak minum\"",
    "rutin air minuman": "\"hari-hari kena isi botol\" (sebut rutin sebenar)",
    "rutin harian": "sebut benda sebenar yang dibuat setiap hari",
    "melengkapkan": "buang, atau sebut benda sebenar",
    "memudahkan": "\"senang\" / \"tak payah ... lagi\"",
    "mudahkan rutin": "\"tak payah ... lagi\"",
    "sesuai dipertimbangkan": "\"ngam untuk\" / \"sesuai untuk\"",
    "dipertimbangkan": "\"fikir-fikir\" / buang",
    "mempunyai": "\"ada\"",
    "bagaimana pula": "\"habis tu, ... macam mana?\"",
    "bagaimana": "\"macam mana\"",
    "dapatkan maklumat lanjut": "\"tanya saya\" / \"semak pakej\"",
    "maklumat lanjut": "\"detail\" / \"tanya saya\"",
    "untuk ketahui": "\"nak tahu\"",
    "ketahui": "\"tahu\" / \"tengok\"",
    "selamat tinggal": "\"Dulu: ...\" / \"Tak payah ... dah\"",
    "say goodbye": "\"Dulu: ... Sekarang: ...\"",
    "hello,": "\"Sekarang: ...\"",
    "sedia bila-bila masa": "\"nak bila-bila pun ada\"",
    "bila-bila masa sahaja": "\"bila-bila pun boleh\"",
    "nikmati": "sebut apa yang dapat: \"terus minum\"",
    "rasai": "buang / sebut apa yang dirasa",
    "tingkatkan": "\"upgrade\" / sebut perubahan sebenar",
    "pastikan": "buang, atau \"jangan lupa\"",
    "sertai": "buang",
    "anda patut": "jangan mengajar; tanya soalan",
    "tak perlu terus buat keputusan": "\"Tanya dulu pun takpe.\"",
    "bonus promosi": "\"Siap hantar & pasang free*\"",
    "pelbagai pilihan": "sebut pilihannya: \"panas, sejuk, suhu bilik\"",
    "pelbagai": "sebut benda sebenar",
    "rekaan kompak": "\"kecik je\" / \"lebar 19.5 cm je\"",
    "ruang terhad": "\"dapur sempit\" / \"tak banyak ruang\"",
    "persiapkan": "\"siapkan\"",
    "dipersiapkan": "\"disiapkan\" / \"nak kena siap\"",
    "persediaan rumah": "\"barang rumah\" / \"benda nak beli\"",
    "keperluan air minuman": "\"air minum\"",
    "merupakan": "\"ialah\" / buang",
    "adalah": "buang, ayat BM jarang perlu \"adalah\"",
    "sahaja!": "\"je\" (\"RM20 je*\")",
    "klik whatsapp untuk": "\"WhatsApp saya, ...\"",
    "hubungi kami": "\"WhatsApp saya\"",
    "kami": "\"saya\" (ejen bercakap seorang)",
    "paling laris": "dakwaan tanpa sumber Coway: buang",
    "terlaris": "dakwaan tanpa sumber Coway: buang",
    "ramai dah pasang": "bukti sosial tak disahkan: buang",
    "19.5 cm": "jangan sebut ukuran cm; guna \"sejengkal je\" (keputusan user 12 Nov 2026)",
    "kertas a4": "buang perbandingan ukuran; guna \"sejengkal je\"",
    "nah,": "\"nah\" dalam BM = \"nah, ambik\"; guna \"Tak payah dah.\" / \"Dah tak zaman.\"",
    "berkualiti tinggi": "sebut fakta (penapis Nanotrap, servis HEART)",
    "gaya hidup": "sebut situasi sebenar",
    "keluarga tersayang": "\"family\" / \"anak-anak\"",
    "kehadiran": "\"bila baby dah sampai\"",
    "menyediakan": "\"bagi\" / \"ada\"",
    "sekiranya": "\"kalau\"",
    "apabila": "\"bila\"",
    "tidak": "\"tak\"",
    "hendak": "\"nak\"",
    "sudah": "\"dah\"",
    "sahaja": "\"je\"",
}

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]")
TNC = re.compile(r"^\s*\*")


def pecah_ayat(teks):
    return [a.strip() for a in re.split(r"(?<=[.!?])\s+|\n+", teks) if a.strip()]


def semak(teks, nama="teks"):
    isu = []
    baris = [b for b in teks.splitlines() if not TNC.match(b)]
    badan = "\n".join(baris)
    rendah = badan.lower()
    for frasa, ganti in KAKU.items():
        pola = r"(?<![\w-])" + re.escape(frasa) + (r"(?![\w-])" if frasa[-1].isalnum() else "")
        n = len(re.findall(pola, rendah))
        if n:
            isu.append(("MERAH", f"\"{frasa}\" ×{n} → {ganti}"))
    for a in pecah_ayat(badan):
        kata = len(re.findall(r"[\wÀ-ÿ'-]+", a))
        if kata > 18:
            isu.append(("KUNING", f"ayat {kata} perkataan (maks ±15): \"{a[:70]}…\""))
    e = len(EMOJI.findall(badan))
    if e > 4:
        isu.append(("KUNING", f"{e} emoji (maks 3–4; satu di hook sudah cukup)"))
    n_anda = len(re.findall(r"\banda\b", rendah))
    if n_anda > 1:
        isu.append(("KUNING", f"\"anda\" ×{n_anda}: buang kata ganti, atau panggil terus (\"Abang\", \"Mak-mak\", \"awak\")"))
    if "tertakluk terma" not in teks.lower() and re.search(r"rm\s?\d", teks.lower()):
        isu.append(("MERAH", "ada harga tapi tiada baris \"*Tertakluk terma & syarat.\""))
    return isu


def cetak(nama, isu):
    if not isu:
        print(f"✓ {nama}")
        return 0
    print(f"✗ {nama}")
    for tahap, m in isu:
        print(f"   {'🔴' if tahap == 'MERAH' else '🟡'} {m}")
    return sum(1 for t, _ in isu if t == "MERAH")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--senarai":
        for f, g in KAKU.items():
            print(f"- \"{f}\" → {g}")
        return 0
    merah = 0
    if argv[0] == "--bank":
        bank = json.load(open(argv[1], encoding="utf-8"))
        status = argv[argv.index("--status") + 1] if "--status" in argv else None
        for i in bank["item"]:
            if "copy" not in i or (status and i.get("status") != status):
                continue
            c = i["copy"]
            teks = "\n".join([c.get("headline", ""), c.get("description", ""), c.get("teks", "")])
            merah += cetak(i["id"], semak(teks, i["id"]))
        return 1 if merah else 0
    for f in argv:
        teks = sys.stdin.read() if f == "-" else open(f, encoding="utf-8").read()
        merah += cetak(f, semak(teks, f))
    return 1 if merah else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
