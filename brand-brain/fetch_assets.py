"""Tarik aset jenama Coway dari coway.com.my ke dalam brand brain.

Untuk setiap produk: muat turun gambar produk (hero, warna, ciri, spec) ke
  brand-brain/coway/Other Brand Assets/<kategori>/<produk>/
dan simpan teks laman (tajuk, meta, heading, perenggan) ke copy.md.

Jalankan semula bila Coway tukar laman:  python brand-brain/fetch_assets.py
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = "https://www.coway.com.my"
ROOT = Path(__file__).resolve().parent / "coway" / "Other Brand Assets"
MAX_BYTES = 2_500_000  # langkau gambar terlalu besar

PRODUCTS = {
    "water-purifier": ["villaem3", "neoplus", "neon", "coreplus", "coreslim", "cinnamon",
                       "glaze", "lucyplus", "ombak", "ais", "dazzie"],
    "air-purifier": ["storm2", "noble2", "atrium", "lombok3", "studio", "suite"],
    "handsfree-bidet": ["flowlet", "flowletplus"],
    "outdoor": ["outdoorfilter"],
    "refrigerator": ["multidoor551l", "sidebyside715l"],
}

BRAND_FILES = [  # logo & lencana untuk semua iklan
    "/img/coway-malaysia-logo.png",
    "/files/coway-malaysia-seo-logo.jpg",
    "/img/heart-service/coway-heart-service-logo-large.png",
    "/files/Products/water-purifier/ais/coway-malaysia-heart-service-logo.png",
    "/img/logo-halal.png",
    "/files/Products/logo-halal-new.png",
    "/img/logo-nsf.png",
    "/img/logo-wpok.png",
    "/img/logo-water-quality.png",
    "/img/logo-certified-water-specialist.png",
    "/img/logo-kolas.png",
    "/img/logo-tuv.png",
    "/img/logo-red-dot-design-winner.png",
    "/img/logo-good-design.png",
    "/img/logo-international-design-excellence-awards.png",
    "/img/logo-international-forum-design.png",
    "/img/about/coway-malaysia-market-share-2021.png",
    "/img/general-slider/2025-putra-brand-awards-coway.jpg",
    "/files/Products/water-purifier/filter/coway-plus-inno-sense-filter.png",
    "/files/Products/water-purifier/filter/coway-plus-neo-sense-filter.png",
    "/files/Products/water-purifier/filter/coway-ro-membrane-filter.png",
]

IMG_RE = re.compile(r"""(?:src|data-src|data-lazy|href|content|srcset)=["']([^"']+?\.(?:png|jpe?g|webp))["']"""
                    r"""|url\(\s*['"]?([^)'"]+?\.(?:png|jpe?g|webp))""", re.I)
SKIP_RE = re.compile(r"header-menu|menu-header|_header_thumbnail|icon-|loading|app-store|google-play|"
                     r"ar-app|AR-mobile|ar-background|screenshot-of-the-coway-ar|/img/about/|/Header/|eco-lite", re.I)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (brand-brain fetch)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def page_images(src):
    out = []
    for a, b in IMG_RE.findall(src):
        u = re.split(r",\s|\s+\d+[wx]\b", html.unescape(a or b).strip())[0]  # srcset; nama fail boleh ada ruang
        u = urllib.parse.urljoin(BASE + "/", u)
        if u.startswith(BASE) and u not in out:
            out.append(u)
    return out


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def page_copy(src):
    meta = lambda n: (re.search(rf'<meta[^>]+(?:name|property)="{n}"[^>]+content="([^"]*)"', src, re.I) or [None, ""])[1]
    title = strip_tags((re.search(r"<title>(.*?)</title>", src, re.S | re.I) or [None, ""])[1])
    body = re.sub(r"<header.*?</header>|<footer.*?</footer>|<nav.*?</nav>", " ", src, flags=re.S | re.I)
    lines, seen = [], set()
    for tag, inner in re.findall(r"<(h[1-4]|p|li)[^>]*>(.*?)</\1>", body, re.S | re.I):
        t = strip_tags(inner)
        if re.search(r"ENQUIRY FORM|USE COWAY AR", t):
            break  # selepas ini borang & footer
        if t.startswith("Loading") or t in ("Locate Us", "Ask Us", "SelfCare Login"):
            continue
        if 3 <= len(t) <= 400 and t not in seen:
            seen.add(t)
            lines.append(("#" * (int(tag[1]) + 1) + " " if tag[0] == "h" else "- ") + t if tag.lower() != "p" else t)
    return title, html.unescape(meta("description")), lines


def download(url, dest):
    if dest.exists():
        return "ada"
    try:
        data = get(urllib.parse.quote(url, safe=":/?=&%"))
    except Exception as e:  # noqa: BLE001
        return f"gagal ({e})"
    if len(data) > MAX_BYTES:
        return f"langkau ({len(data)//1024} KB)"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return f"{len(data)//1024} KB"


def main():
    only = set(sys.argv[1:])
    pages = {}
    for cat, slugs in PRODUCTS.items():
        for slug in slugs:
            url = f"{BASE}/products/{cat}/{slug}"
            try:
                pages[(cat, slug)] = get(url).decode("utf-8", "replace")
            except Exception as e:  # noqa: BLE001
                print("X", url, e)
    # gambar yang muncul di banyak laman = menu/footer, bukan aset produk
    freq = Counter(u for src in pages.values() for u in set(page_images(src)))
    shared = {u for u, n in freq.items() if n > 2}

    index_path = ROOT / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {}
    for (cat, slug), src in pages.items():
        if only and slug not in only:
            continue
        folder = ROOT / cat / slug
        imgs = [u for u in page_images(src) if u not in shared and not SKIP_RE.search(u)
                and "/files/Products/" in u]
        print(f"\n== {cat}/{slug}: {len(imgs)} gambar")
        names = [urllib.parse.unquote(u.rsplit("/", 1)[1]).replace(" ", "-") for u in imgs]
        with ThreadPoolExecutor(8) as pool:
            results = list(pool.map(lambda un: download(un[0], folder / un[1]), zip(imgs, names)))
        for name, res in zip(names, results):
            print("  ", name, res)
        files = [n for n in names if (folder / n).exists()]
        title, desc, lines = page_copy(src)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "copy.md").write_text(
            f"# {title}\n\nSumber: {BASE}/products/{cat}/{slug}\n\n> {desc}\n\n" + "\n".join(lines) + "\n",
            encoding="utf-8")
        index[f"{cat}/{slug}"] = {"url": f"{BASE}/products/{cat}/{slug}", "title": title,
                                  "description": desc, "images": files}

    if not only:
        print("\n== brand (logo & lencana)")
        with ThreadPoolExecutor(8) as pool:
            results = pool.map(lambda p: download(BASE + p, ROOT / "_brand" / p.rsplit("/", 1)[1]), BRAND_FILES)
            for p, res in zip(BRAND_FILES, results):
                print("  ", p.rsplit("/", 1)[1], res)
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
