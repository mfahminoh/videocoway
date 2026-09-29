window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 3.81
  },
  {
   "t0": 3.81,
   "bg": "blue",
   "t1": 9.36
  },
  {
   "t0": 9.36,
   "bg": "navy",
   "t1": 21.24
  },
  {
   "t0": 21.24,
   "bg": "navy",
   "t1": 23.67
  },
  {
   "t0": 23.67,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 27.58
  },
  {
   "t0": 27.58,
   "bg": {
    "clip": "presenter",
    "c0": 6.4,
    "c1": 9.6
   },
   "t1": 30.77
  },
  {
   "t0": 30.77,
   "bg": "blue",
   "t1": 35.77
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 300,
   "size": 130,
   "html": "BERAPA<br><span style='color:var(--yellow)'>SEHARI?</span>",
   "t0": 0.1,
   "t1": 3.81
  },
  {
   "type": "photo",
   "top": 760,
   "left": 310,
   "w": 460,
   "h": 460,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 1.264,
   "t1": 3.81
  },
  {
   "type": "price",
   "top": 420,
   "label": "HARGA ASAL",
   "from": "RM104",
   "to": "RM54",
   "t0": 3.81,
   "t1": 9.36,
   "strikeT": 6.48,
   "toT": 7.06
  },
  {
   "type": "title",
   "top": 300,
   "size": 80,
   "html": "SEHARI",
   "t0": 9.36,
   "t1": 21.24
  },
  {
   "type": "text",
   "top": 400,
   "size": 50,
   "weight": 700,
   "html": "RM54 ÷ 30 hari",
   "t0": 9.36,
   "t1": 13.34
  },
  {
   "type": "counter",
   "top": 480,
   "from": 54,
   "to": 1.8,
   "prefix": "RM",
   "decimals": 2,
   "dur": 0.8,
   "color": "#fff",
   "t0": 9.944,
   "t1": 21.24
  },
  {
   "type": "pill",
   "top": 790,
   "html": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 13.34,
   "t1": 21.24
  },
  {
   "type": "text",
   "top": 900,
   "size": 50,
   "weight": 700,
   "html": "7 bulan pertama: (RM54 − RM20) ÷ 30",
   "t0": 17.62,
   "t1": 21.24
  },
  {
   "type": "counter",
   "top": 980,
   "from": 1.8,
   "to": 1.13,
   "prefix": "RM",
   "decimals": 2,
   "dur": 0.8,
   "t0": 18.21,
   "t1": 21.24
  },
  {
   "type": "icon",
   "top": 420,
   "icon": "cup",
   "size": 300,
   "color": "#fff",
   "t0": 21.24,
   "t1": 23.67
  },
  {
   "type": "title",
   "top": 800,
   "size": 76,
   "html": "LEBIH MURAH DARI<br><span style='color:var(--yellow)'>SECAWAN TEH TARIK</span>",
   "t0": 21.24,
   "t1": 23.67
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "PANAS",
     "color": "#ff7a6b",
     "at": "@08%30",
     "t": 24.687
    },
    {
     "text": "SEJUK",
     "color": "#6cc2ff",
     "at": "@08%55",
     "t": 25.535
    },
    {
     "text": "SUHU BILIK",
     "color": "#e9eef5",
     "at": "@08%75",
     "t": 26.212
    }
   ],
   "t0": 23.67,
   "t1": 27.58
  },
  {
   "type": "pill",
   "top": 270,
   "html": "NANOTRAP · PEMASANGAN PERCUMA",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 27.58,
   "t1": 30.77
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 30.77,
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
   "t0": 30.77,
   "t1": null,
   "btnT": 32.15
  }
 ],
 "clips": {
  "press_pour": {
   "dir": "../../out/frames/NE04_press_pour/",
   "n": 111,
   "start": 3.0
  },
  "presenter": {
   "dir": "../../out/frames/NE04_presenter/",
   "n": 101,
   "start": 6.4
  }
 }
};
