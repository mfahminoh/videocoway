window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "navy",
   "t1": 4.87
  },
  {
   "t0": 4.87,
   "bg": "navy",
   "t1": 9.36
  },
  {
   "t0": 9.36,
   "bg": {
    "clip": "clip5",
    "c0": 0.3,
    "c1": 4.2
   },
   "t1": 14.63
  },
  {
   "t0": 14.63,
   "bg": {
    "clip": "clip5",
    "c0": 4.5,
    "c1": 6.2
   },
   "t1": 17.53
  },
  {
   "t0": 17.53,
   "bg": "navy",
   "t1": 22.98
  },
  {
   "t0": 22.98,
   "bg": {
    "clip": "clip4",
    "c0": 6.0,
    "c1": 10.0
   },
   "t1": 26.77
  },
  {
   "t0": 26.77,
   "bg": "blue",
   "t1": 35.01
  },
  {
   "t0": 35.01,
   "bg": "blue",
   "t1": 40.41
  }
 ],
 "els": [
  {
   "type": "counter",
   "top": 600,
   "from": 0,
   "to": 11.4,
   "suffix": "L",
   "decimals": 1,
   "dur": 1.0,
   "size": 260,
   "t0": 0.23,
   "t1": 4.87
  },
  {
   "type": "title",
   "top": 940,
   "size": 80,
   "html": "BANYAK MANA TU?",
   "t0": 2.241,
   "t1": 4.87
  },
  {
   "type": "title",
   "top": 300,
   "size": 80,
   "html": "BOTOL 1.5L",
   "t0": 4.87,
   "t1": 9.36
  },
  {
   "type": "bottles",
   "top": 470,
   "n": 8,
   "fill": 7.6,
   "dur": 2.2,
   "w": 100,
   "label": "≈ {n} botol",
   "t0": 4.87,
   "t1": 9.36
  },
  {
   "type": "chips",
   "top": 1250,
   "items": [
    {
     "text": "6.1L BILIK",
     "color": "#fff",
     "at": "@03",
     "t": 9.36
    },
    {
     "text": "2.6L SEJUK",
     "color": "#fff",
     "at": "@04",
     "t": 11.85
    },
    {
     "text": "2.7L PANAS",
     "color": "#fff",
     "at": "@05",
     "t": 14.63
    }
   ],
   "t0": 9.36,
   "t1": 17.53
  },
  {
   "type": "title",
   "top": 260,
   "size": 70,
   "html": "HAMPIR <span style='color:var(--yellow)'>8 BOTOL BESAR</span><br>STANDBY SETIAP HARI",
   "t0": 17.53,
   "t1": 22.98
  },
  {
   "type": "bottles",
   "top": 520,
   "n": 8,
   "fill": 7.6,
   "dur": 1.2,
   "delay": 0.1,
   "w": 100,
   "t0": 17.53,
   "t1": 22.98
  },
  {
   "type": "pill",
   "top": 270,
   "html": "ANTARA TANGKI PALING BESAR COWAY",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 22.98,
   "t1": 26.77
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM120",
   "to": "RM74",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "t0": 26.77,
   "t1": 35.01,
   "badgeT": 31.853,
   "strikeT": 28.725,
   "toT": 29.898
  },
  {
   "type": "photo",
   "top": 150,
   "left": 310,
   "w": 460,
   "h": 460,
   "src": "../../assets/img/villaem3-front.png",
   "fit": "contain",
   "shadow": false,
   "radius": 0,
   "t0": 35.01,
   "t1": null
  },
  {
   "type": "cta",
   "top": 760,
   "ticks": [
    "PROMOSI RM74 SEBULAN*",
    "+ REBAT RM20 × 7 BULAN*",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM120/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 35.01,
   "t1": null
  }
 ],
 "clips": {
  "clip5": {
   "dir": "../../out/frames/V304_clip5/",
   "n": 181,
   "start": 0.3
  },
  "clip4": {
   "dir": "../../out/frames/V304_clip4/",
   "n": 120,
   "start": 6.0
  }
 }
};
