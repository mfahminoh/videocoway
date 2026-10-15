window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": {
    "clip": "bottle_to_baby",
    "c0": 7.0,
    "c1": 8.6
   },
   "t1": 1.34
  },
  {
   "t0": 1.34,
   "bg": {
    "clip": "bottles_busy",
    "c0": 0.0,
    "c1": 2.6
   },
   "t1": 3.81
  },
  {
   "t0": 3.81,
   "bg": "navy",
   "t1": 6.32
  },
  {
   "t0": 6.32,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 10.72
  },
  {
   "t0": 10.72,
   "bg": "navy",
   "t1": 13.16
  },
  {
   "t0": 13.16,
   "bg": "navy",
   "t1": 15.37
  },
  {
   "t0": 15.37,
   "bg": "blue",
   "t1": 21.77
  },
  {
   "t0": 21.77,
   "bg": "blue",
   "t1": 25.94
  }
 ],
 "els": [
  {
   "type": "banner",
   "top": 230,
   "html": "ADA <em>ANAK KECIL</em><br>KAT RUMAH?",
   "t0": 0.09,
   "t1": 1.34
  },
  {
   "type": "banner",
   "top": 230,
   "html": "<em>3 SEBAB</em> NEON<br>SESUAI UNTUK KORANG",
   "t0": 1.34,
   "t1": 3.81
  },
  {
   "type": "reason",
   "top": 300,
   "num": "1",
   "title": "KUNCI<br>KESELAMATAN",
   "sub": "untuk air panas",
   "t0": 3.81,
   "t1": 6.32
  },
  {
   "type": "icon",
   "top": 880,
   "icon": "lock",
   "size": 260,
   "color": "#0B2F6B",
   "hit": true,
   "t0": 4.524,
   "t1": 6.32
  },
  {
   "type": "reason",
   "top": 250,
   "num": "2",
   "title": "BANCUH SUSU",
   "sub": "satu tekan je",
   "t0": 6.32,
   "t1": 10.72
  },
  {
   "type": "reason",
   "top": 250,
   "num": "3",
   "title": "FILTER BARU<br>SETIAP <span style='color:var(--yellow)'>8 BULAN</span>",
   "t0": 10.72,
   "t1": 13.16
  },
  {
   "type": "delivery",
   "top": 720,
   "t0": 10.72,
   "t1": 13.16
  },
  {
   "type": "stamp",
   "top": 1300,
   "html": "PERCUMA",
   "t0": 12.468,
   "t1": 13.16
  },
  {
   "type": "card",
   "top": 760,
   "icon": "tech",
   "title": "PILIH TECHNICIAN",
   "sub": "Datang servis ke rumah",
   "t0": 13.16,
   "t1": 15.37
  },
  {
   "type": "stamp",
   "top": 1080,
   "html": "BOLEH ✓",
   "color": "#1faa59",
   "rot": -8,
   "t0": 14.366,
   "t1": 15.37
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 15.37,
   "t1": 21.77
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM104",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "to": "RM54",
   "t0": 15.37,
   "t1": 21.77,
   "badgeT": 19.23,
   "strikeT": 16.693,
   "toT": 17.714
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/mint.jpg",
   "t0": 21.77,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PROMOSI RM54 SEBULAN*",
    "+ REBAT RM20 × 7 BULAN*",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM104/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 21.77,
   "t1": null,
   "btnT": 22.358
  }
 ],
 "clips": {
  "bottle_to_baby": {
   "dir": "../../out/frames/NL02_bottle_to_baby/",
   "n": 51,
   "start": 7.0
  },
  "bottles_busy": {
   "dir": "../../out/frames/NL02_bottles_busy/",
   "n": 81,
   "start": 0.0
  },
  "press_pour": {
   "dir": "../../out/frames/NL02_press_pour/",
   "n": 111,
   "start": 3.0
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably.",
 "style": "Say in Malaysian Malay, as a warm, cheerful young woman chatting on TikTok, relaxed and fairly quick, smiling"
};
