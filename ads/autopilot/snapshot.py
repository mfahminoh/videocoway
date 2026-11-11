#!/usr/bin/env python3
"""Bina snapshot enjin daripada output mentah Meta Ads connector (ads_get_ad_entities).

Setiap fail input = hasil tool sebagaimana adanya: sama ada objek penuh {"ad_entities": "<string JSON>", ...}
(termasuk fail yang disimpan sendiri oleh Claude Code bila output terlalu besar) atau senarai baris itu sendiri.

  python3 ads/autopilot/snapshot.py --akaun 990723860427887 --tarikh 2026-11-11 \
      --w2 raw/w2.json --w3 raw/w3.json --w7 raw/w7.json --hayat raw/hayat.json \
      --kempen30 raw/kempen30.json [--akaun-w7 763.96]

Tulis ads/autopilot/data/<tarikh>/<akaun>.json dan cetak ringkasan (bilangan iklan, jumlah belanja setiap tetingkap).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
MESEJ = "actions:onsite_conversion.messaging_conversation_started_7d"
TETINGKAP = ("w2", "w3", "w7", "hayat")


def baris(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(d, dict):
        d = d["ad_entities"]
    if isinstance(d, str):
        d = json.loads(d)
    return d


def nombor(x):
    if x is None:
        return 0.0
    if isinstance(x, dict):
        x = x.get("value")
    try:
        return float(str(x).replace("%", "").replace(",", ""))
    except ValueError:
        return 0.0  # "Not available"


def hasil(r):
    """(adakah iklan mesej, bilangan mesej)."""
    res = r.get("results") or {}
    ind = res.get("indicator")
    n = 0
    if res.get("values"):
        n = int(nombor(res["values"][0].get("value")))
    elif res.get("value") is not None:
        n = int(nombor(res.get("value")))
    return ind == MESEJ, n


def bina(akaun, tarikh, fail, kempen30, akaun_w7=None):
    snap = {"akaun": akaun, "tarikh": tarikh, "sumber": "Meta Ads connector (snapshot.py)",
            "kempen_30h": [], "iklan": {}, "metrik": {w: {} for w in TETINGKAP}}
    if akaun_w7 is not None:
        snap["akaun_belanja"] = {"w7": float(akaun_w7)}
    for w in TETINGKAP:
        for r in baris(fail[w]):
            ad = r["id"]
            mesej_ok, n = hasil(r)
            meta = snap["iklan"].setdefault(ad, {
                "nama": r.get("name", ad), "adset": r.get("adset_id"), "kempen": r.get("campaign_id"),
                "status": r.get("effective_status"), "dibina": (r.get("created_time") or tarikh)[:10],
                "creative": r.get("creative_id"), "mesej": mesej_ok})
            if r.get("results", {}).get("indicator"):
                meta["mesej"] = mesej_ok
            snap["metrik"][w][ad] = [round(nombor(r.get("amount_spent")), 2), int(nombor(r.get("impressions"))),
                                     round(nombor(r.get("ctr")), 2), round(nombor(r.get("cpm")), 2),
                                     round(nombor(r.get("frequency")), 3), n if mesej_ok else 0]
    for r in baris(kempen30):
        ok, n = hasil(r)
        if ok:
            snap["kempen_30h"].append([r["id"], round(nombor(r.get("amount_spent")), 2), n])
    return snap


def main(argv=None):
    a = argparse.ArgumentParser()
    a.add_argument("--akaun", required=True)
    a.add_argument("--tarikh", required=True)
    for w in TETINGKAP:
        a.add_argument(f"--{w}", required=True)
    a.add_argument("--kempen30", required=True)
    a.add_argument("--akaun-w7", type=float)
    a.add_argument("--out")
    o = a.parse_args(argv)
    snap = bina(o.akaun, o.tarikh, {w: getattr(o, w) for w in TETINGKAP}, o.kempen30, o.akaun_w7)
    out = Path(o.out) if o.out else DIR / "data" / o.tarikh / f"{o.akaun}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    jum = {w: round(sum(r[0] for r in snap["metrik"][w].values()), 2) for w in TETINGKAP}
    print(out)
    print(f"{len(snap['iklan'])} iklan · belanja {jum} · {len(snap['kempen_30h'])} kempen mesej (30 hari)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
