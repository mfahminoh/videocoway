"""Ujian enjin autopilot:  python3 ads/autopilot/test_enjin.py"""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import enjin

AKAUN = "111"

DAFTAR = {
    "peraturan": json.loads((Path(__file__).parent / "daftar.json").read_text())["peraturan"],
    "akaun": {AKAUN: {"nama": "Ujian", "autopilot": True, "mod": "auto", "kumpulan": {
        "k1": {"page_id": "P1", "instagram_user_id": "IG1", "awalan": "UJI", "kempen": ["C1"]}}}},
}


def item(id_, cr=None, status="LULUS", media=None, promo="2026-12-31", guna=None, copy_=None):
    d = {"id": id_, "status": status, "kumpulan": "k1", "tajuk": id_, "jenis_media": "image",
         "media": media or f"H-{id_}", "creative_ids": [cr] if cr else [], "promo_sah_hingga": promo,
         "guna": guna or []}
    if cr:
        d["creative_id"] = cr
    if copy_:
        d["copy"] = copy_
    return d


def snap(iklan, metrik, kempen_30h=(("C1", 250, 10),)):
    """iklan: {ad: (adset, creative, dibina)}; metrik: {ad: {w: [belanja, imp, ctr, cpm, freq, mesej]}}"""
    s = {"akaun": AKAUN, "tarikh": "2026-11-11", "kempen_30h": [list(r) for r in kempen_30h],
         "iklan": {}, "metrik": {w: {} for w in enjin.TETINGKAP}}
    for ad, (adset, cr, dibina) in iklan.items():
        s["iklan"][ad] = {"nama": ad, "adset": adset, "kempen": "C1", "status": "ACTIVE", "dibina": dibina,
                          "creative": cr, "mesej": True}
        for w, row in metrik.get(ad, {}).items():
            s["metrik"][w][ad] = row
    return s


def semua(row):
    return {w: row for w in enjin.TETINGKAP}


class Ujian(unittest.TestCase):
    def nilai(self, s, bank_items):
        return enjin.nilai(s, copy.deepcopy(DAFTAR), {"item": bank_items})

    def keputusan(self, pelan, ad):
        return next(r for r in pelan["penilaian"] if r["id"] == ad)

    def test_benchmark_akaun_dan_lalai(self):
        p = self.nilai(snap({}, {}), [])
        self.assertEqual(p["benchmark"]["nilai"], 25.0)
        p = self.nilai(snap({}, {}, kempen_30h=(("C1", 50, 2),)), [])
        self.assertEqual(p["benchmark"]["nilai"], 30.0)

    def test_tunggu_iklan_baru_dan_data_sikit(self):
        s = snap({"a": ("S1", "cr-a", "2026-11-10"), "b": ("S1", "cr-b", "2026-11-01")},
                 {"a": semua([80, 3000, 1, 20, 1.1, 0]), "b": semua([15, 400, 1, 20, 1.1, 0])})
        p = self.nilai(s, [])
        self.assertEqual(self.keputusan(p, "a")["keputusan"], "TUNGGU")
        self.assertEqual(self.keputusan(p, "b")["keputusan"], "TUNGGU")
        self.assertEqual(p["tindakan"], [])

    def test_kosong_diganti_dengan_pemenang(self):
        s = snap({"bad": ("S1", "cr-bad", "2026-11-01"), "win": ("S2", "cr-win", "2026-11-01")},
                 {"bad": semua([40, 3000, 0.4, 13, 1.2, 0]), "win": semua([60, 3000, 2.5, 20, 1.2, 6])})
        bank = [item("WIN", cr="cr-win"), item("NEW", cr="cr-new")]
        p = self.nilai(s, bank)
        self.assertEqual(self.keputusan(p, "bad")["keputusan"], "KOSONG")
        self.assertEqual(self.keputusan(p, "win")["keputusan"], "MENANG")
        t = p["tindakan"][0]
        self.assertEqual((t["jenis"], t["bank_item"], t["adset"]), ("GANTI", "WIN", "S1"))
        self.assertEqual(t["iklan_baru"]["creative"], {"creative_id": "cr-win"})
        self.assertTrue(t["iklan_baru"]["ad_name"].startswith("UJI | AUTO | WIN |"))

    def test_mahal_hook_vs_tawaran(self):
        # 3 mesej untuk RM120 = RM40 > 1.3 x 25
        s = snap({"h": ("S1", "cr-h", "2026-11-01"), "t": ("S2", "cr-t", "2026-11-01")},
                 {"h": semua([120, 4000, 0.6, 30, 1.2, 3]), "t": semua([120, 4000, 2.0, 30, 1.2, 3])})
        bank = [item("H", cr="cr-h", media="M-h"), item("T", cr="cr-t", media="M-t"),
                item("T-V2", media="M-t", copy_={"teks": "x", "headline": "y"}),
                item("LAIN", cr="cr-lain", media="M-lain")]
        p = self.nilai(s, bank)
        self.assertEqual(self.keputusan(p, "h")["diagnosis"], "hook")
        self.assertEqual(self.keputusan(p, "t")["diagnosis"], "tawaran")
        ganti = {t["iklan_lama"]: t["bank_item"] for t in p["tindakan"]}
        self.assertEqual(ganti["t"], "T-V2")       # tawaran: media sama, copy baru
        self.assertNotIn(ganti["h"], ("H", "T-V2"))  # hook: media lain
        inline = next(t for t in p["tindakan"] if t["bank_item"] == "T-V2")["iklan_baru"]["creative"]
        spec = inline["object_story_spec"]
        self.assertEqual((spec["page_id"], spec["instagram_user_id"]), ("P1", "IG1"))
        self.assertEqual(spec["link_data"]["call_to_action"]["type"], "WHATSAPP_MESSAGE")

    def test_tetingkap_panjang_untuk_bajet_kecil(self):
        # w2/w3 belanja kecil; w7 cukup (>= 2 x 25) dan murah -> SIHAT, bukan MAHAL
        s = snap({"a": ("S1", "cr-a", "2026-11-01")},
                 {"a": {"w2": [10, 300, 2, 30, 1.1, 0], "w3": [15, 450, 2, 30, 1.1, 0],
                        "w7": [55, 1500, 2, 30, 1.2, 2], "hayat": [60, 1600, 2, 30, 1.2, 2]}})
        r = self.keputusan(self.nilai(s, []), "a")
        self.assertEqual((r["keputusan"], r["tetingkap"]), ("SIHAT", "w7"))

    def test_bank_kosong_iklan_tunggal_dibiar(self):
        s = snap({"a": ("S1", "cr-a", "2026-11-01")}, {"a": semua([120, 4000, 1.2, 30, 1.2, 3])})
        p = self.nilai(s, [])
        self.assertEqual(p["tindakan"], [])
        self.assertTrue(any("bank" in a and "kosong" in a for a in p["amaran"]))

    def test_bocor_dipause_walau_bank_kosong(self):
        s = snap({"a": ("S1", "cr-a", "2026-11-01")}, {"a": semua([160, 4000, 1.2, 30, 1.2, 2])})
        p = self.nilai(s, [])
        self.assertEqual(p["tindakan"][0]["jenis"], "PAUSE")
        self.assertTrue(p["tindakan"][0]["ad_set_kosong"])

    def test_promo_luput_draf_dan_pernah_guna_ditolak(self):
        s = snap({"bad": ("S1", "cr-bad", "2026-11-01")}, {"bad": semua([50, 3000, 0.4, 13, 1.2, 0])})
        bank = [item("LUPUT", cr="c1", promo="2026-11-10"), item("DRAF", cr="c2", status="DRAF"),
                item("GUNA", cr="c3", guna=[{"adset": "S1"}]), item("DIHENTIKAN", cr="c4", status="DIHENTIKAN")]
        p = self.nilai(s, bank)
        self.assertEqual(p["tindakan"][0]["jenis"], "PAUSE")  # KOSONG tetap dipause

    def test_had_harian(self):
        iklan = {f"a{i}": (f"S{i}", f"cr{i}", "2026-11-01") for i in range(5)}
        met = {f"a{i}": semua([50 + i, 3000, 0.4, 13, 1.2, 0]) for i in range(5)}
        bank = [item(f"B{i}", cr=f"n{i}") for i in range(5)]
        p = self.nilai(snap(iklan, met), bank)
        self.assertEqual(len(p["tindakan"]), 3)
        self.assertEqual([t["iklan_lama"] for t in p["tindakan"]], ["a4", "a3", "a2"])  # paling rugi dulu

    def test_luar_skop_tak_disentuh(self):
        s = snap({"x": ("S9", "cr-x", "2026-11-01")}, {"x": semua([90, 3000, 0.3, 13, 1.2, 0])})
        s["iklan"]["x"]["kempen"] = "LAIN"
        p = self.nilai(s, [item("B", cr="n")])
        self.assertEqual(p["tindakan"], [])
        self.assertEqual(p["luar_skop"][0]["id"], "x")

    def test_suis_henti(self):
        d = copy.deepcopy(DAFTAR)
        d["akaun"][AKAUN]["autopilot"] = False
        s = snap({"bad": ("S1", "cr-bad", "2026-11-01")}, {"bad": semua([50, 3000, 0.4, 13, 1.2, 0])})
        p = enjin.nilai(s, d, {"item": [item("B", cr="n")]})
        self.assertEqual(p["tindakan"], [])
        self.assertEqual(self.keputusan(p, "bad")["keputusan"], "KOSONG")

    def test_letih(self):
        s = snap({"a": ("S1", "cr-a", "2026-10-20")},
                 {"a": {"w2": [30, 1000, 1.5, 30, 1.2, 1], "w3": [45, 1500, 1.0, 30, 1.2, 2],
                        "w7": [100, 3500, 1.4, 30, 3.1, 4], "hayat": [300, 10000, 2.0, 30, 3.1, 12]}})
        self.assertEqual(self.keputusan(self.nilai(s, []), "a")["keputusan"], "LETIH")

    def test_rekod_kemas_kini_bank_dan_log(self):
        s = snap({"bad": ("S1", "cr-bad", "2026-11-01")}, {"bad": semua([50, 3000, 0.4, 13, 1.2, 0])})
        bank = {"item": [item("B", cr="n")]}
        pelan = enjin.nilai(s, copy.deepcopy(DAFTAR), bank)
        with tempfile.TemporaryDirectory() as d:
            bp, lp = Path(d) / "bank.json", Path(d) / "log.jsonl"
            bp.write_text(json.dumps(bank))
            enjin.rekod(pelan, [{"tindakan": 0, "berjaya": True, "iklan_baru_id": "NEWAD", "pause_lama": True}], bp, lp)
            self.assertEqual(json.loads(bp.read_text())["item"][0]["guna"][0]["iklan"], "NEWAD")
            self.assertEqual(json.loads(lp.read_text().splitlines()[0])["iklan_baru"], "NEWAD")

    def test_laporan_jalan(self):
        s = snap({"bad": ("S1", "cr-bad", "2026-11-01")}, {"bad": semua([50, 3000, 0.4, 13, 1.2, 0])})
        teks = enjin.laporan(self.nilai(s, [item("B", cr="n")]))
        self.assertIn("Ganti 'bad'", teks)


class UjianSnapshot(unittest.TestCase):
    """Baris sebenar dari Meta Ads connector (11 Nov 2026), dipendekkan."""
    MENTAH = {"ad_entities": json.dumps([
        {"name": "FIZAH | NeoN Flow | B1 Menyampah Beli Air", "adset_id": "S1", "campaign_id": "C1",
         "effective_status": "ACTIVE", "created_time": "2026-11-05T00:08:12+0800", "creative_id": "cr1", "id": "A1",
         "amount_spent": {"value": "13.36", "unit": "MYR"}, "impressions": "357", "ctr": "1.40%",
         "cpm": {"value": "37.42", "unit": "MYR"}, "frequency": "1.091743",
         "results": {"indicator": "actions:onsite_conversion.messaging_conversation_started_7d",
                     "values": [{"attribution_windows": ["default"], "value": "1"}]}},
        {"name": "FIZAH | Coway Neon", "adset_id": "S2", "campaign_id": "C1", "effective_status": "ACTIVE",
         "created_time": "2026-11-05T00:04:43+0800", "creative_id": "cr2", "id": "A2",
         "amount_spent": {"value": "0", "unit": "MYR"}, "impressions": "0", "ctr": None, "cpm": None, "frequency": "0",
         "results": {"indicator": "actions:onsite_conversion.messaging_conversation_started_7d", "value": "Not available"}},
        {"name": "P05", "adset_id": "S3", "campaign_id": "C9", "effective_status": "ACTIVE",
         "created_time": "2026-10-15T02:35:22+0800", "creative_id": "cr3", "id": "A3",
         "amount_spent": {"value": "8.36", "unit": "MYR"}, "impressions": "3940", "ctr": "3.05%",
         "cpm": {"value": "2.12", "unit": "MYR"}, "frequency": "1.01",
         "results": {"indicator": "video_thruplay_watched_actions", "values": [{"value": "1156"}]}}])}
    KEMPEN = {"ad_entities": json.dumps([
        {"name": "x", "id": "C1", "amount_spent": {"value": "467.39"},
         "results": {"indicator": "actions:onsite_conversion.messaging_conversation_started_7d", "values": [{"value": "12"}]}},
        {"name": "y", "id": "C2", "amount_spent": {"value": "23.3"},
         "results": {"indicator": "actions:onsite_conversion.messaging_conversation_started_7d", "value": "Not available"}},
        {"name": "z", "id": "C3", "amount_spent": {"value": "798.33"},
         "results": {"indicator": "actions:offsite_conversion.fb_pixel_complete_registration", "values": [{"value": "93"}]}}])}

    def test_tukar_mentah(self):
        import snapshot
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "w.json"
            f.write_text(json.dumps(self.MENTAH))
            k = Path(d) / "k.json"
            k.write_text(json.dumps(self.KEMPEN))
            s = snapshot.bina("111", "2026-11-11", {w: f for w in enjin.TETINGKAP}, k, 763.96)
        self.assertEqual(s["metrik"]["w2"]["A1"], [13.36, 357, 1.4, 37.42, 1.092, 1])
        self.assertEqual(s["metrik"]["w2"]["A2"], [0.0, 0, 0.0, 0.0, 0.0, 0])
        self.assertEqual(s["metrik"]["w2"]["A3"][5], 0)          # thruplay bukan mesej
        self.assertFalse(s["iklan"]["A3"]["mesej"])
        self.assertTrue(s["iklan"]["A1"]["mesej"])
        self.assertEqual(s["iklan"]["A1"]["dibina"], "2026-11-05")
        self.assertEqual(s["kempen_30h"], [["C1", 467.39, 12], ["C2", 23.3, 0]])


if __name__ == "__main__":
    unittest.main()
