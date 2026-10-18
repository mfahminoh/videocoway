"""Bina halaman pelan posting Threads (pelan.html) daripada posts.json.

    python promo/threads/build_page.py
"""
import html
import json
import pathlib

HERE = pathlib.Path(__file__).parent
POSTS = json.loads((HERE / "posts.json").read_text())


def media(m):
    if m.endswith(".mp4"):
        return f'<video src="out/{m}" controls playsinline muted preload="metadata"></video>'
    if m.startswith("p10_N"):
        return "".join(f'<img src="out/p10_{n}.png" alt="Poster panggilan terakhir, tinggal {n} slot" loading="lazy">' for n in (10, 5, 3))
    return f'<img src="out/{m}" alt="Poster posting" loading="lazy">'


def card(p):
    reply = ""
    if p.get("reply"):
        reply = f"""<div class="sub">Balasan dalam thread yang sama (post sebaik saja post utama naik)</div>
      <div class="copybox"><pre id="r{p['n']}">{html.escape(p['reply'])}</pre>
      <button type="button" data-copy="r{p['n']}">Salin balasan</button></div>"""
    return f"""<article class="post" id="post{p['n']}">
    <header><span class="no">{p['n']:02d}</span><div><div class="when">{html.escape(p['day'])}</div><h2>{html.escape(p['type'])}</h2></div>
      <span class="tag">Topik: {html.escape(p['tag'])}</span></header>
    <div class="body">
      <div class="media {'multi' if len(p['media']) > 1 or p['media'][0].startswith('p10_N') else ''}">{''.join(media(m) for m in p['media'])}</div>
      <div class="copy">
        <div class="sub">Copy post · <span class="chars">{len(p['text'])}/500 aksara</span></div>
        <div class="copybox"><pre id="t{p['n']}">{html.escape(p['text'])}</pre>
        <button type="button" data-copy="t{p['n']}">Salin copy</button></div>
        {reply}
      </div>
    </div></article>"""


PAGE = f"""<title>AP vs Jerebu Threads</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Poppins:wght@400;500;600;700;800&display=swap">
<style>
/* Susun atur: satu lajur kad posting ikut urutan hari; poster di kiri, copy di kanan (bertindan di telefon). Tema gelap jerebu sahaja. */
:root {{
  --bg:#17110c; --panel:#221912; --panel2:#2c2017; --line:#3d2d20;
  --fg:#f6efe7; --mute:#bfae9c; --orange:#F28C28; --blue:#00A4E4; --yellow:#FFD23F; --red:#E5322D;
  --display:'Anton', Impact, 'Arial Narrow', sans-serif; --body:'Poppins', system-ui, sans-serif;
  color-scheme: dark;
}}
body {{ background:var(--bg); color:var(--fg); font-family:var(--body); font-size:15px; line-height:1.55; }}
.wrap {{ max-width:1080px; margin:0 auto; padding-block:28px 64px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:28px; }}
h1 {{ font-family:var(--display); font-weight:400; font-size:clamp(44px, 9vw, 84px); line-height:1; margin:0; text-wrap:balance; }}
h1 .ap {{ color:var(--blue); }} h1 .vs {{ color:var(--yellow); font-size:.55em; vertical-align:middle; }} h1 .jb {{ color:var(--orange); }}
.lead {{ color:var(--mute); max-width:62ch; margin:10px 0 0; }}
.facts {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; }}
.facts span {{ border:1px solid var(--line); background:var(--panel); padding:6px 14px; border-radius:40px; font-weight:600; font-size:14px; }}
.facts b {{ color:var(--yellow); }}
section h3 {{ font-family:var(--display); font-weight:400; font-size:30px; letter-spacing:.5px; margin:0 0 12px; text-transform:uppercase; }}
.sched {{ overflow-x:auto; border:1px solid var(--line); border-radius:14px; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; min-width:560px; }}
th, td {{ text-align:left; padding:10px 14px; border-bottom:1px solid var(--line); }}
th {{ color:var(--mute); font-weight:600; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; background:var(--panel); }}
tr:last-child td {{ border-bottom:0; }}
td a {{ color:var(--fg); }}
td.n {{ font-variant-numeric:tabular-nums; color:var(--yellow); font-weight:700; }}
.post {{ background:var(--panel); border:1px solid var(--line); border-radius:18px; overflow:hidden; }}
.post header {{ display:flex; align-items:center; gap:16px; padding:16px 20px; border-bottom:1px solid var(--line); flex-wrap:wrap; }}
.no {{ font-family:var(--display); font-size:44px; line-height:1; color:var(--orange); font-variant-numeric:tabular-nums; }}
.when {{ color:var(--mute); font-size:13px; font-weight:600; }}
.post h2 {{ margin:0; font-size:20px; line-height:1.25; }}
.tag {{ margin-left:auto; font-size:12px; font-weight:700; color:var(--blue); border:1px solid var(--blue); border-radius:30px; padding:3px 12px; }}
.body {{ display:grid; grid-template-columns:minmax(0, 360px) minmax(0, 1fr); gap:20px; padding:20px; }}
.media {{ display:grid; gap:10px; align-content:start; }}
.media.multi {{ grid-template-columns:repeat(auto-fit, minmax(110px, 1fr)); }}
.media img, .media video {{ width:100%; max-width:100%; border-radius:10px; display:block; background:#000; }}
.copy {{ min-width:0; display:grid; gap:10px; align-content:start; }}
.sub {{ color:var(--mute); font-size:12px; font-weight:700; letter-spacing:1.2px; text-transform:uppercase; }}
.chars {{ color:var(--yellow); }}
.copybox {{ background:var(--panel2); border:1px solid var(--line); border-radius:12px; padding:14px 16px; display:grid; gap:12px; }}
pre {{ margin:0; white-space:pre-wrap; word-break:break-word; font-family:var(--body); font-size:15px; line-height:1.55; }}
button {{ justify-self:start; font:700 14px var(--body); background:var(--yellow); color:#17110c; border:0; border-radius:30px; padding:9px 20px; cursor:pointer; }}
button:hover {{ filter:brightness(1.08); }}
button:focus-visible {{ outline:3px solid var(--blue); outline-offset:2px; }}
ul.notes {{ margin:0; padding-left:20px; display:grid; gap:8px; max-width:75ch; }}
.notes b {{ color:var(--yellow); }}
@media (max-width:720px) {{ .body {{ grid-template-columns:1fr; }} .tag {{ margin-left:0; }} }}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<div class="wrap">
  <div>
    <h1><span class="ap">AP</span> <span class="vs">VS</span> <span class="jb">JEREBU</span></h1>
    <p class="lead">Pelan 10 posting Threads untuk jual pakej video penapis udara. Setiap kad ada poster, masa cadangan dan copy yang boleh disalin terus. Semua copy bawah had 500 aksara Threads.</p>
    <div class="facts"><span><b>15</b> video (dalam promosi)</span><span>Harga <b>RM30</b></span><span>Terhad <b>25</b> orang</span><span>CTA: komen “JEREBU” / DM</span><span>7 hari · 10 posting</span></div>
  </div>

  <section><h3>Jadual</h3>
    <div class="sched"><table><thead><tr><th>#</th><th>Bila</th><th>Jenis</th><th>Media</th></tr></thead><tbody>
    {''.join(f'<tr><td class="n">{p["n"]:02d}</td><td>{html.escape(p["day"])}</td><td><a href="#post{p["n"]}">{html.escape(p["type"])}</a></td><td>{html.escape(", ".join(p["media"]))}</td></tr>' for p in POSTS)}
    </tbody></table></div>
  </section>

  {''.join(card(p) for p in POSTS)}

  <section><h3>Skrip balas DM</h3>
    <div class="copybox"><pre id="dm">Terima kasih berminat dengan pakej AP vs JEREBU! 🙌

Pakej: 15 video promote penapis udara (9:16, VO BM)
Harga: RM30 sekali bayar

Cara dapatkan:
1. Bayar RM30 ke [akaun / link bayaran]
2. Hantar resit + emel Gmail anda
3. Saya share folder Google Drive ke emel tu, terus boleh download

Slot sekarang: [N]/25</pre>
    <button type="button" data-copy="dm">Salin skrip DM</button></div>
  </section>

  <section><h3>Sebelum post</h3>
    <ul class="notes">
      <li>Isi <b>[N]</b> dalam post 10 dengan baki slot sebenar, dan pilih poster 10, 5 atau 3 yang sepadan.</li>
      <li>Isi <b>[akaun / link bayaran]</b> dalam skrip DM.</li>
      <li>Share folder Drive kepada emel pembeli (akses Viewer), bukan “sesiapa yang ada link”, supaya link tak tersebar.</li>
      <li>Video ada promosi <b>RM20/bulan × 7 bulan</b> dalam babak penutup. Pastikan promosi masih berjalan masa jualan.</li>
      <li>Balas setiap komen “JEREBU” dalam masa sejam. Komen awal bantu post naik.</li>
    </ul>
  </section>
</div>

<script>
document.addEventListener('click', async e => {{
  const b = e.target.closest('button[data-copy]'); if (!b) return;
  const el = document.getElementById(b.dataset.copy), label = b.textContent;
  try {{ await navigator.clipboard.writeText(el.innerText); b.textContent = 'Disalin ✓'; }}
  catch {{ const r = document.createRange(); r.selectNodeContents(el); const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Teks dipilih, tekan salin'; }}
  setTimeout(() => b.textContent = label, 1800);
}});
</script>
"""

(HERE / "pelan.html").write_text(PAGE)
print("pelan.html")
