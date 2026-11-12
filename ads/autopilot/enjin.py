#!/usr/bin/env python3
"""Enjin keputusan autopilot iklan Coway (stdlib sahaja).

Enjin ini TIDAK memanggil Meta. Ia membaca snapshot metrik yang ditulis oleh
skill coway-autopilot, membuat keputusan ikut peraturan dalam daftar.json, dan
mengeluarkan pelan tindakan. Skill yang laksanakan pelan melalui Meta Ads
connector, kemudian panggil `rekod`.

  python3 ads/autopilot/enjin.py nilai   <snapshot.json>              # tulis pelan/<tarikh>/<akaun>.json, cetak laluan
  python3 ads/autopilot/enjin.py laporan <pelan.json>                 # ringkasan BM untuk laporan pagi
  python3 ads/autopilot/enjin.py rekod   <pelan.json> <hasil.json>    # kemas kini bank.json + log.jsonl

Bentuk snapshot: lihat SKILL.md (bahagian 2) atau test_enjin.py.
"""
from __future__ import annotations

import json
import math
import sys
from datetime import date
from pathlib import Path

DIR = Path(__file__).resolve().parent
TETINGKAP = ("w2", "w3", "w7", "hayat")
INF = math.inf


# ---------------------------------------------------------------- muat fail

def baca(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def tulis(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def tarikh(s):
    return date.fromisoformat(s[:10])


# ---------------------------------------------------------------- metrik

class M:
    """Satu baris metrik: [belanja, impression, ctr%, cpm, frequency, mesej]."""

    __slots__ = ("belanja", "imp", "ctr", "cpm", "freq", "mesej")

    def __init__(self, row=None):
        row = list(row or []) + [0] * 6
        self.belanja = float(row[0] or 0)
        self.imp = int(row[1] or 0)
        self.ctr = float(row[2] or 0)
        self.cpm = float(row[3] or 0)
        self.freq = float(row[4] or 0)
        self.mesej = int(row[5] or 0)

    @property
    def kpm(self):  # kos setiap mesej
        return self.belanja / self.mesej if self.mesej else INF

    def ringkas(self):
        k = "-" if self.kpm == INF else round(self.kpm, 2)
        return {"belanja": round(self.belanja, 2), "imp": self.imp, "ctr": self.ctr,
                "freq": self.freq, "mesej": self.mesej, "kos_mesej": k}


def kos(m, win):
    if m.mesej == 0:
        return f"0 mesej untuk RM{m.belanja:.2f} ({win})"
    return f"RM{m.kpm:.2f}/mesej, {m.mesej} mesej ({win})"


# ---------------------------------------------------------------- konfigurasi

def peraturan(daftar, akaun_id):
    p = dict(daftar["peraturan"])
    p.update(daftar["akaun"][akaun_id].get("peraturan", {}))
    return p


def kumpulan_untuk(akaun_cfg, kempen_id):
    for k_id, k in akaun_cfg["kumpulan"].items():
        if kempen_id in k["kempen"]:
            return k_id
    return None


def benchmark(snap, p):
    belanja = sum(float(r[1] or 0) for r in snap.get("kempen_30h", []))
    mesej = sum(int(r[2] or 0) for r in snap.get("kempen_30h", []))
    if mesej >= p["min_mesej_benchmark"]:
        return {"nilai": round(belanja / mesej, 2), "sumber": "30 hari akaun",
                "belanja_30h": round(belanja, 2), "mesej_30h": mesej}
    return {"nilai": float(p["benchmark_lalai"]), "sumber": "lalai (mesej 30 hari < %d)" % p["min_mesej_benchmark"],
            "belanja_30h": round(belanja, 2), "mesej_30h": mesej}


# ---------------------------------------------------------------- penilaian satu iklan

def nilai_iklan(ad_id, meta, met, B, p, hari_ini):
    """Pulangkan dict keputusan: keputusan, sebab, tetingkap, diagnosis."""
    h = met["hayat"]
    umur = (hari_ini - tarikh(meta["dibina"])).days
    out = {"id": ad_id, "nama": meta["nama"], "adset": meta["adset"], "kempen": meta["kempen"],
           "umur_hari": umur, "hayat": h.ringkas()}

    if umur < p["min_umur_hari"]:
        return {**out, "keputusan": "TUNGGU", "sebab": f"baru {umur} hari (min {p['min_umur_hari']})"}
    if h.belanja < p["min_belanja"] or h.imp < p["min_impression"]:
        return {**out, "keputusan": "TUNGGU",
                "sebab": f"data belum cukup (RM{h.belanja:.2f}, {h.imp} impression)"}

    # 1. Tiada mesej langsung selepas belanja yang cukup
    if h.mesej == 0 and h.belanja >= p["faktor_kosong"] * B:
        return {**out, "keputusan": "KOSONG", "tetingkap": "hayat", "diagnosis": diagnosis(h.ctr, p),
                "sebab": f"0 mesej selepas RM{h.belanja:.2f} (had {p['faktor_kosong']}× benchmark = RM{p['faktor_kosong'] * B:.2f})",
                "rugi": round(h.belanja, 2)}

    # 2. Pilih tetingkap terpendek yang belanjanya cukup untuk menilai kos
    win = next((w for w in TETINGKAP if met[w].belanja >= p["faktor_tetingkap"] * B), None)
    if win is None:
        return {**out, "keputusan": "TUNGGU",
                "sebab": f"belanja RM{h.belanja:.2f} belum capai RM{p['faktor_tetingkap'] * B:.2f} untuk nilai kos"}
    m = met[win]
    out["tetingkap"] = win
    out["metrik"] = m.ringkas()

    if m.kpm > p["faktor_mahal"] * B:
        rugi = m.belanja - m.mesej * B
        return {**out, "keputusan": "MAHAL", "diagnosis": diagnosis(m.ctr, p), "rugi": round(rugi, 2),
                "bocor": m.kpm > p["faktor_bocor"] * B,
                "sebab": f"{kos(m, win)} > had RM{p['faktor_mahal'] * B:.2f}"}

    w7, w3 = met["w7"], met["w3"]
    letih = w7.freq > p["freq_letih"] or (
        umur >= 7 and h.imp >= 3000 and h.ctr > 0 and w3.imp >= 300 and w3.ctr < p["faktor_ctr_jatuh"] * h.ctr)

    if m.kpm <= p["faktor_menang"] * B and m.mesej >= p["min_mesej_menang"]:
        return {**out, "keputusan": "MENANG", "letih": letih,
                "sebab": kos(m, win)}
    if letih:
        return {**out, "keputusan": "LETIH",
                "sebab": f"frequency 7h {w7.freq:.2f} / CTR 3h {w3.ctr:.2f}% vs hayat {h.ctr:.2f}%"}
    return {**out, "keputusan": "SIHAT", "sebab": kos(m, win)}


def diagnosis(ctr, p):
    if ctr < p["ctr_rendah"]:
        return "hook"      # orang tak berhenti scroll: tukar media / jenis hook
    if ctr >= p["ctr_baik"]:
        return "tawaran"   # orang klik tapi tak mesej: tukar copy / tawaran
    return "kreatif"


# ---------------------------------------------------------------- bank

def prestasi_item(item, snap):
    """Gabung metrik hayat semua iklan dalam snapshot yang guna creative item ini."""
    ids = set(item.get("creative_ids", []))
    tot = M()
    for ad_id, meta in snap["iklan"].items():
        if meta.get("creative") in ids:
            h = M(snap["metrik"]["hayat"].get(ad_id))
            tot.belanja += h.belanja
            tot.mesej += h.mesej
            tot.imp += h.imp
    # rekod tersimpan (bila iklan item dah berhenti, snapshot tak nampak dia lagi)
    simpan = item.get("prestasi") or {}
    if float(simpan.get("belanja", 0)) > tot.belanja:
        tot.belanja, tot.mesej = float(simpan["belanja"]), int(simpan.get("mesej", 0))
    return tot


def pilih_item(bank, kumpulan, adset_id, aktif_creatives, media_lama, diag, snap, B, p, hari_ini, sudah):
    calon = []
    for item in bank["item"]:
        if item.get("status") != "LULUS" or item.get("kumpulan") != kumpulan:
            continue
        if item["id"] in sudah:
            continue
        if tarikh(item["promo_sah_hingga"]) < hari_ini:
            continue
        if set(item.get("creative_ids", [])) & aktif_creatives:
            continue  # dah berjalan dalam ad set ini
        if any(g.get("adset") == adset_id for g in item.get("guna", [])):
            continue  # pernah dipasang di ad set ini
        perf = prestasi_item(item, snap)
        kalah = perf.belanja >= p["faktor_tetingkap"] * B and perf.kpm > p["faktor_mahal"] * B
        if kalah:
            continue
        sama_media = item.get("media") == media_lama
        if diag == "tawaran":
            utama = 0 if sama_media else 1     # kekalkan media, tukar copy
        else:
            utama = 1 if sama_media else 0     # tukar media
        terbukti = perf.mesej >= p["min_mesej_menang"] and perf.kpm <= B
        kedudukan = (utama, 0 if terbukti else (1 if perf.belanja == 0 else 2), perf.kpm, item["id"])
        calon.append((kedudukan, item, perf))
    calon.sort(key=lambda c: c[0])
    return calon[0] if calon else None


def creative_untuk(item, k):
    if item.get("creative_id"):
        return {"creative_id": item["creative_id"]}
    c = item["copy"]
    if item["jenis_media"] == "video":
        data = {"video_id": item["media"], "image_hash": item["thumb_hash"], "message": c["teks"],
                "title": c["headline"],
                "call_to_action": {"type": "WHATSAPP_MESSAGE", "value": {"app_destination": "WHATSAPP"}}}
        spec = {"page_id": k["page_id"], "video_data": data}
    else:
        data = {"image_hash": item["media"], "link": "https://api.whatsapp.com/send", "message": c["teks"],
                "name": c["headline"], "description": c.get("description", ""),
                "call_to_action": {"type": "WHATSAPP_MESSAGE", "value": {"app_destination": "WHATSAPP"}}}
        spec = {"page_id": k["page_id"], "link_data": data}
    if k.get("instagram_user_id"):
        spec["instagram_user_id"] = k["instagram_user_id"]
    return {"object_story_spec": spec}


def stok_bank(bank, akaun_cfg, hari_ini, snap=None, B=None, p=None):
    """Kira item LULUS yang masih boleh dipakai (promo sah, dan belum kalah dalam akaun ini)."""
    stok = {}
    for k_id in akaun_cfg["kumpulan"]:
        sah = []
        for i in bank["item"]:
            if i.get("kumpulan") != k_id or i.get("status") != "LULUS" or tarikh(i["promo_sah_hingga"]) < hari_ini:
                continue
            if snap is not None:
                perf = prestasi_item(i, snap)
                if perf.belanja >= p["faktor_tetingkap"] * B and perf.kpm > p["faktor_mahal"] * B:
                    continue
            sah.append(i)
        draf = [i for i in bank["item"] if i.get("kumpulan") == k_id and i.get("status") == "DRAF"]
        stok[k_id] = {"lulus": len(sah), "draf": len(draf),
                      "promo_tamat_terdekat": min((i["promo_sah_hingga"] for i in sah), default=None)}
    return stok


# ---------------------------------------------------------------- nilai akaun

def nilai(snap, daftar, bank):
    akaun_id = snap["akaun"]
    cfg = daftar["akaun"][akaun_id]
    p = peraturan(daftar, akaun_id)
    hari_ini = tarikh(snap["tarikh"])
    B = benchmark(snap, p)
    Bv = B["nilai"]
    pelan = {"akaun": akaun_id, "nama": cfg["nama"], "tarikh": snap["tarikh"], "mod": cfg.get("mod", "cadang"),
             "benchmark": B, "had": {"mahal": round(p["faktor_mahal"] * Bv, 2), "kosong": round(p["faktor_kosong"] * Bv, 2),
                                     "menang": round(p["faktor_menang"] * Bv, 2)},
             "penilaian": [], "luar_skop": [], "tindakan": [], "amaran": [], "menang": []}

    if not cfg.get("autopilot", False):
        pelan["amaran"].append("Autopilot DIMATIKAN untuk akaun ini (daftar.json \"autopilot\": false). Laporan sahaja.")

    # semakan jumlah: belanja iklan dalam snapshot vs belanja akaun
    jum = snap.get("akaun_belanja", {})
    for w in ("w2", "w7"):
        if w in jum:
            s = sum(M(r).belanja for r in snap["metrik"][w].values())
            if abs(s - float(jum[w])) > max(2.0, 0.05 * float(jum[w])):
                pelan["amaran"].append(f"Semakan jumlah {w}: iklan RM{s:.2f} vs akaun RM{float(jum[w]):.2f}. "
                                       "Mungkin ada iklan yang berhenti dalam tempoh ini; semak jika beza besar.")

    # nilai setiap iklan dalam skop
    calon = []
    aktif_ikut_adset = {}
    for ad_id, meta in snap["iklan"].items():
        if meta.get("status") not in ("ACTIVE", "WITH_ISSUES", "IN_PROCESS", "PENDING_REVIEW", "PREAPPROVED"):
            continue
        aktif_ikut_adset.setdefault(meta["adset"], []).append(ad_id)
        k_id = kumpulan_untuk(cfg, meta["kempen"])
        met = {w: M(snap["metrik"].get(w, {}).get(ad_id)) for w in TETINGKAP}
        if k_id is None or not meta.get("mesej", True):
            if met["hayat"].belanja > 0:
                pelan["luar_skop"].append({"id": ad_id, "nama": meta["nama"], "belanja_w7": round(met["w7"].belanja, 2),
                                           "hayat": met["hayat"].ringkas()})
            continue
        r = nilai_iklan(ad_id, meta, met, Bv, p, hari_ini)
        r["kumpulan"] = k_id
        pelan["penilaian"].append(r)
        if r["keputusan"] in ("KOSONG", "MAHAL"):
            calon.append(r)
        if r["keputusan"] == "MENANG":
            pelan["menang"].append({"id": ad_id, "nama": meta["nama"], "creative": meta.get("creative"), "sebab": r["sebab"]})

    if not cfg.get("autopilot", False):
        return pelan

    # susun ikut wang terbuang, kenakan had harian
    calon.sort(key=lambda r: -r.get("rugi", 0))
    dipilih_hari_ini = set()
    pause_kiraan = baru_kiraan = 0
    pause_ikut_adset = {}
    creative_by_ad = {a: m.get("creative") for a, m in snap["iklan"].items()}
    media_by_creative = {}
    for item in bank["item"]:
        for c in item.get("creative_ids", []):
            media_by_creative[c] = item.get("media")

    for r in calon:
        if pause_kiraan >= p["max_pause_sehari"]:
            pelan["amaran"].append(f"Had {p['max_pause_sehari']} pause sehari dicapai; {r['nama']} ditangguh ke esok.")
            continue
        k_id = r["kumpulan"]
        k = cfg["kumpulan"][k_id]
        adset = r["adset"]
        aktif = [a for a in aktif_ikut_adset.get(adset, []) if a not in pause_ikut_adset.get(adset, [])]
        aktif_creatives = {creative_by_ad.get(a) for a in aktif_ikut_adset.get(adset, [])}
        media_lama = media_by_creative.get(creative_by_ad.get(r["id"]))
        pilihan = None
        if baru_kiraan < p["max_iklan_baru_sehari"]:
            pilihan = pilih_item(bank, k_id, adset, aktif_creatives, media_lama, r.get("diagnosis"),
                                 snap, Bv, p, hari_ini, dipilih_hari_ini)
        tinggal = len(aktif) - 1
        if pilihan:
            _, item, perf = pilihan
            dipilih_hari_ini.add(item["id"])
            nama_baru = f"{k['awalan']} | AUTO | {item['id']} | {hari_ini.strftime('%d%m%Y')}"
            pelan["tindakan"].append({
                "jenis": "GANTI", "iklan_lama": r["id"], "nama_lama": r["nama"], "adset": adset,
                "creative_lama": creative_by_ad.get(r["id"]),
                "kumpulan": k_id, "sebab": r["sebab"], "diagnosis": r.get("diagnosis"),
                "keputusan": r["keputusan"],
                "pause_walau_gagal": r["keputusan"] == "KOSONG" or bool(r.get("bocor")),
                "bank_item": item["id"], "bank_tajuk": item.get("tajuk"),
                "bank_prestasi": ({"belanja": round(perf.belanja, 2), "mesej": perf.mesej,
                                   "kos_mesej": None if perf.kpm == INF else round(perf.kpm, 2)}
                                  if perf.belanja else "belum diuji di akaun ini"),
                "iklan_baru": {"ad_set_id": adset, "ad_name": nama_baru, "creative": creative_untuk(item, k)}})
            pause_kiraan += 1
            baru_kiraan += 1
            pause_ikut_adset.setdefault(adset, []).append(r["id"])
        elif r["keputusan"] == "KOSONG" or r.get("bocor") or tinggal >= 1:
            pelan["tindakan"].append({"jenis": "PAUSE", "iklan_lama": r["id"], "nama_lama": r["nama"], "adset": adset,
                                      "creative_lama": creative_by_ad.get(r["id"]),
                                      "kumpulan": k_id, "sebab": r["sebab"] + "; tiada kreatif ganti dalam bank",
                                      "ad_set_kosong": tinggal < 1})
            pause_kiraan += 1
            pause_ikut_adset.setdefault(adset, []).append(r["id"])
            if tinggal < 1:
                pelan["amaran"].append(f"Ad set {adset} akan berhenti (tiada iklan aktif lain, bank {k_id} kosong).")
        else:
            pelan["amaran"].append(f"{r['nama']}: mahal ({r['sebab']}) tapi bank {k_id} kosong dan ia satu-satunya "
                                   "iklan dalam ad set. Dibiarkan; isi bank.")

    pelan["prestasi_bank"] = {}
    for item in bank["item"]:
        perf = prestasi_item(item, snap)
        if perf.belanja > 0:
            pelan["prestasi_bank"][item["id"]] = {"belanja": round(perf.belanja, 2), "mesej": perf.mesej,
                                                  "tarikh": snap["tarikh"]}
    pelan["stok_bank"] = stok_bank(bank, cfg, hari_ini, snap, Bv, p)
    for k_id, s in pelan["stok_bank"].items():
        if s["lulus"] < p["min_stok_bank"]:
            pelan["amaran"].append(f"Bank '{k_id}': {s['lulus']} kreatif LULUS (min {p['min_stok_bank']}), "
                                   f"{s['draf']} DRAF menunggu kelulusan.")
        if s["promo_tamat_terdekat"] and (tarikh(s["promo_tamat_terdekat"]) - hari_ini).days <= 3:
            pelan["amaran"].append(f"Bank '{k_id}': promo perlu disahkan semula sebelum {s['promo_tamat_terdekat']}.")
    return pelan


# ---------------------------------------------------------------- laporan

LABEL = {"KOSONG": "🔴", "MAHAL": "🔴", "LETIH": "🟡", "MENANG": "🟢", "SIHAT": "⚪", "TUNGGU": "⏳"}


def laporan(pelan):
    b = pelan["benchmark"]
    L = [f"*Autopilot {pelan['nama']}* · {pelan['tarikh']} · mod {pelan['mod']}",
         f"Benchmark RM{b['nilai']:.2f}/mesej ({b['sumber']}). Had mahal RM{pelan['had']['mahal']:.2f}.", ""]
    kira = {}
    for r in pelan["penilaian"]:
        kira[r["keputusan"]] = kira.get(r["keputusan"], 0) + 1
    L.append("Iklan: " + ", ".join(f"{LABEL.get(k, '')}{k} {v}" for k, v in sorted(kira.items())))
    if pelan["tindakan"]:
        L.append("")
        L.append("Tindakan:")
        for t in pelan["tindakan"]:
            if t["jenis"] == "GANTI":
                L.append(f"- Ganti '{t['nama_lama']}' → {t['bank_item']} ({t['bank_tajuk']}). Sebab: {t['sebab']}"
                         f" [{t['diagnosis']}]")
            else:
                L.append(f"- Pause '{t['nama_lama']}'. Sebab: {t['sebab']}")
    else:
        L.append("Tiada tindakan hari ini.")
    if pelan["menang"]:
        L.append("")
        L.append("Menang (kekal, hook untuk batch seterusnya): " + "; ".join(m["nama"] for m in pelan["menang"]))
    if pelan["luar_skop"]:
        s7 = sum(x["belanja_w7"] for x in pelan["luar_skop"])
        L.append("")
        L.append(f"Luar skop (tidak disentuh): {len(pelan['luar_skop'])} iklan, RM{s7:.2f} belanja 7 hari.")
    if pelan["amaran"]:
        L.append("")
        L.append("Perlu perhatian:")
        L += [f"- {a}" for a in pelan["amaran"]]
    return "\n".join(L)


# ---------------------------------------------------------------- rekod

def rekod(pelan, hasil, bank_path, log_path):
    bank = baca(bank_path)
    idx = {i["id"]: i for i in bank["item"]}
    log = []
    for h in hasil:
        t = pelan["tindakan"][h["tindakan"]]
        baris = {"tarikh": pelan["tarikh"], "akaun": pelan["akaun"], "jenis": t["jenis"],
                 "iklan_lama": t["iklan_lama"], "nama_lama": t["nama_lama"], "sebab": t["sebab"],
                 "berjaya": bool(h.get("berjaya")), "nota": h.get("nota", "")}
        if t["jenis"] == "GANTI":
            baris.update({"bank_item": t["bank_item"], "iklan_baru": h.get("iklan_baru_id"),
                          "pause_lama": bool(h.get("pause_lama"))})
            if h.get("berjaya") and h.get("iklan_baru_id"):
                idx[t["bank_item"]].setdefault("guna", []).append(
                    {"akaun": pelan["akaun"], "adset": t["adset"], "iklan": h["iklan_baru_id"], "tarikh": pelan["tarikh"]})
        # kreatif yang kalah tak boleh dipilih semula (pepijat 12 Nov: PR09 dipilih kerana iklannya dah berhenti)
        dipause = (t["jenis"] == "GANTI" and h.get("pause_lama")) or (t["jenis"] == "PAUSE" and h.get("berjaya"))
        if dipause and t.get("creative_lama"):
            for item in bank["item"]:
                if t["creative_lama"] in item.get("creative_ids", []) and item.get("status") == "LULUS":
                    item["status"] = "DIHENTIKAN"
                    item["nota"] = f"Kalah {pelan['tarikh']} di {pelan['akaun']}: {t['sebab']}"
                    baris.setdefault("bank_dihentikan", []).append(item["id"])
        log.append(baris)
    for item_id, pr in (pelan.get("prestasi_bank") or {}).items():
        if item_id in idx and float(pr["belanja"]) >= float((idx[item_id].get("prestasi") or {}).get("belanja", 0)):
            idx[item_id]["prestasi"] = pr
    tulis(bank_path, bank)
    with open(log_path, "a", encoding="utf-8") as f:
        for b in log:
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    return log


# ---------------------------------------------------------------- CLI

def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "nilai":
        snap = baca(argv[2])
        pelan = nilai(snap, baca(DIR / "daftar.json"), baca(DIR / "bank.json"))
        out = DIR / "pelan" / snap["tarikh"] / f"{snap['akaun']}.json"
        tulis(out, pelan)
        print(out)
        return 0
    if cmd == "laporan":
        print(laporan(baca(argv[2])))
        return 0
    if cmd == "rekod":
        log = rekod(baca(argv[2]), baca(argv[3]), DIR / "bank.json", DIR / "log.jsonl")
        print(f"{len(log)} tindakan direkod")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
