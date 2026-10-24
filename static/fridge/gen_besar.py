"""Jana poster 'peti ais besar' (715L) dari 3 layout: A (dapur), B (angka 715), C (gudang).
python static/fridge/gen_besar.py  -> static/fridge/besar_XX_*.html, kemudian render.py"""
import pathlib
HERE = pathlib.Path(__file__).resolve().parent
A = "../../brand-brain/coway/Other Brand Assets/refrigerator/sidebyside715l"
B = "../../brand-brain/coway/Other Brand Assets/_brand"
FOOT = "*Tertakluk terma &amp; syarat."

POSTERS = [  # (fail, layout, headline dengan <br>, subheadline)
    ("01_stor", "C", "Ini bukan peti ais.<br>Ini stor.", "Coway Side-by-Side 715L."),
    ("02_kedai", "C", "Besar macam nak<br>simpan satu kedai.", "715L. Peti ais paling besar dalam barisan Coway."),
    ("03_takhabis", "A", "Ruang dia?<br>Macam tak<br>habis-habis.", "Coway Side-by-Side 715L."),
    ("04_masalahruang", "B", "Peti ais besar,<br>masalah ruang<br>pun kurang.", "Coway Side-by-Side 715L"),
    ("05_bukapintu", "A", "Baru buka pintu,<br>terus nampak<br>besarnya.", "715L. Peti ais paling besar dalam barisan Coway."),
    ("06_ministor", "C", "Bila peti ais dah<br>macam mini stor.", "Coway Side-by-Side 715L."),
    ("07_stokdapur", "A", "Stok barang dapur?<br>Masukkan sahaja.", "Kapasiti 715L untuk seisi keluarga."),
    ("08_besargila", "B", "Besar gila.<br>Muat lebih<br>banyak.", "Kapasiti 715L untuk simpan lebih banyak barang kegemaran anda."),
    ("09_barunamanya", "A", "Ini baru<br>namanya besar!", "Kenali Coway Side-by-Side 715L."),
    ("10_bukanbiasa", "B", "Bukan besar<br>biasa-biasa.", "715 liter kapasiti. Memang puas hati!"),
    ("11_bukanmain", "C", "Besar dia<br>bukan main.", "715L ruang untuk keperluan seisi keluarga."),
    ("12_ternganga", "B", "Besar sampai<br>ternganga.", "Coway Side-by-Side 715L."),
]

COMMON_CSS = """
.hd { font-weight:800; font-style:italic; text-transform:uppercase; -webkit-text-stroke:10px #1E73D8; paint-order:stroke fill;
  filter:drop-shadow(0 8px 18px rgba(0,0,0,.55)); line-height:.95; letter-spacing:-1px; white-space:nowrap; display:inline-block; }
.pricebox { background:linear-gradient(135deg,#0B4DA2,#0B2F6B); border:2px solid rgba(140,200,255,.35); border-radius:22px;
  padding:14px 30px 16px; box-shadow:0 16px 40px rgba(0,0,0,.5); display:inline-block; }
.pricebox .lbl { font-weight:700; font-size:22px; letter-spacing:5px; }
.pricebox .amt { font-weight:800; font-size:96px; line-height:.95; color:#FFD23F; letter-spacing:-2px; }
.pricebox .amt small { font-size:30px; color:#fff; font-weight:600; letter-spacing:0; }
.subt { font-weight:500; font-size:28px; color:#fff; margin-top:14px; text-shadow:0 2px 12px rgba(0,0,0,.8); }
"""
PRICE = '<div class="pricebox"><div class="lbl">BERMULA</div><div class="amt">RM20<small>/bulan*</small></div></div>'
# kecilkan headline sampai muat kotak (lebar & tinggi maksimum)
FIT = """<script>
function fit(id, maxW, maxH, start){ const el=document.getElementById(id); let s=start;
  el.style.fontSize=s+'px'; while((el.scrollWidth>maxW||el.offsetHeight>maxH)&&s>40){ s-=2; el.style.fontSize=s+'px'; } }
</script>"""

LAYOUT = {
"A": ("""
body{background:#041029}
.photo{left:150px;top:300px;width:840px;height:790px;overflow:hidden;-webkit-mask-image:linear-gradient(to right,transparent,#000 12%,#000 88%,transparent),linear-gradient(to bottom,transparent,#000 10%);-webkit-mask-composite:source-in}
.photo img{position:absolute;left:-10px;top:-8px;width:820px}
.bot{left:0;bottom:0;width:1080px;height:330px;background:linear-gradient(to top,rgba(4,16,41,.96) 30%,transparent)}
.seal{left:40px;top:400px;width:210px;height:210px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#2EA7E0,#0B2F6B);
  border:5px solid #fff;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 16px 40px rgba(0,0,0,.5);transform:rotate(-8deg)}
.seal b{font-weight:800;font-size:84px;line-height:.9}.seal span{font-weight:700;font-size:26px;letter-spacing:3px}
""", """
<div class="abs photo"><img src="{A}/Coway_SBS715-Refrigerator_Card3_V2.jpg"></div>
<div class="abs bot"></div>
<div class="abs" style="left:52px;top:46px;width:780px"><div id="h" class="hd">{H}</div><div class="subt">{S}</div></div>
<div class="abs seal"><b>715</b><span>LITER</span></div>
<div class="abs" style="left:40px;bottom:96px">{P}</div>
<script>fit('h', 740, 196, 118)</script>
"""),
"B": ("""
body{background:#141414}
.bg{inset:0;background:radial-gradient(ellipse 70% 70% at 70% 55%,#4a4a4a 0%,#262626 50%,#0d0d0d 100%)}
.glow{right:-80px;top:240px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(46,167,224,.35),transparent 65%)}
.num{left:30px;top:120px;font-weight:800;font-size:350px;line-height:.8;letter-spacing:-14px;
  background:linear-gradient(180deg,#fff 30%,#9CC9F0);-webkit-background-clip:text;color:transparent;filter:drop-shadow(0 10px 30px rgba(0,0,0,.6))}
.fr{left:470px;top:225px;width:620px;-webkit-mask-image:linear-gradient(to bottom,#000 82%,transparent);filter:drop-shadow(-20px 20px 40px rgba(0,0,0,.6))}
.chip{display:inline-block;border:2px solid rgba(255,255,255,.35);border-radius:40px;padding:6px 18px;font-weight:600;font-size:22px;margin-right:10px;background:rgba(0,0,0,.45)}
.subt{font-size:24px;color:#ddd;max-width:560px}
""", """
<div class="abs bg"></div><div class="abs glow"></div>
<div class="abs num">715</div>
<img class="abs fr" src="img/sbs715_open_cutout.png">
<div class="abs" style="left:40px;top:410px;width:640px">
  <div id="h" class="hd">{H}</div>
  <div style="margin-top:18px"><span class="chip">715 Liter</span><span class="chip">Tinggi 1.9 m</span><span class="chip">Lebar 91 cm</span></div>
  <div class="subt">{S}</div>
  <div style="margin-top:18px">{P}</div>
</div>
<script>fit('h', 640, 230, 88)</script>
"""),
"C": ("""
body{background:#06204F}
.scene{left:-224px;top:110px;width:1500px;transform:perspective(1100px) rotateX(-8deg);transform-origin:50% 100%}
.top{left:0;top:0;width:1080px;height:330px;background:linear-gradient(to bottom,#041029 45%,transparent)}
.bot{left:0;bottom:0;width:1080px;height:300px;background:linear-gradient(to top,rgba(4,16,41,.97) 35%,transparent)}
.callout{left:790px;top:520px;display:flex;align-items:center}
.callout i{display:block;width:70px;height:3px;background:#fff;margin-right:-2px}
.callout div{background:#fff;color:#0B2F6B;border-radius:16px;padding:8px 20px;box-shadow:0 10px 30px rgba(0,0,0,.5);text-align:center}
.callout b{font-weight:800;font-size:64px;line-height:1;display:block}.callout span{font-weight:700;font-size:18px;letter-spacing:3px}
""", """
<img class="abs scene" src="{A}/spaces_for_everything_slide2.jpg">
<div class="abs top"></div><div class="abs bot"></div>
<div class="abs" style="left:52px;top:46px;width:780px"><div id="h" class="hd">{H}</div><div class="subt">{S}</div></div>
<div class="abs callout"><i></i><div><b>715L</b><span>KAPASITI</span></div></div>
<div class="abs" style="left:40px;bottom:96px">{P}</div>
<script>fit('h', 740, 210, 104)</script>
"""),
}

for name, lay, h, s in POSTERS:
    css, body = LAYOUT[lay]
    body = body.replace("{A}", A).replace("{H}", h).replace("{S}", s).replace("{P}", PRICE)
    html = f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>{COMMON_CSS}{css}</style>{FIT}</head>
<body><div class="stage">{body}
<img class="abs logo" src="{B}/coway-logo-white.png">
<div class="abs foot" style="width:420px">{FOOT}</div>
<div class="abs badge"><div><img src="{B}/coway-logo-blue.png"><span>EJEN SAH COWAY</span></div></div>
</div></body></html>'''
    (HERE / f"besar_{name}.html").write_text(html, encoding="utf-8")
    print(f"besar_{name}.html")
