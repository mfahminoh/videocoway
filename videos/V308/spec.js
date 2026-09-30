window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "pastel",
   "t1": 3.41
  },
  {
   "t0": 3.41,
   "bg": "pastel",
   "t1": 12.33
  },
  {
   "t0": 12.33,
   "bg": {
    "clip": "clip4",
    "c0": 6.0,
    "c1": 10.0
   },
   "t1": 17.31
  },
  {
   "t0": 17.31,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 22.13
  },
  {
   "t0": 22.13,
   "bg": "blue",
   "t1": 30.67
  },
  {
   "t0": 30.67,
   "bg": "blue",
   "t1": 35.71
  }
 ],
 "els": [
  {
   "type": "title",
   "top": 240,
   "size": 110,
   "html": "VILLAEM 3<br><span style='color:#E86E5A'>ATAU NEON?</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 0.1,
   "t1": 3.41
  },
  {
   "type": "photo",
   "top": 620,
   "left": 40,
   "w": 500,
   "h": 500,
   "src": "../../assets/img/villaem3-front.png",
   "fit": "contain",
   "shadow": false,
   "radius": 0,
   "t0": 0.1,
   "t1": 3.41
  },
  {
   "type": "photo",
   "top": 650,
   "left": 580,
   "w": 440,
   "h": 440,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 0.928,
   "t1": 3.41
  },
  {
   "type": "vs",
   "top": 420,
   "left": {
    "title": "VILLAEM 3",
    "color": "#0B4DA2",
    "items": [
     "Sistem RO",
     "Tangki 11.4L",
     "8 suhu",
     "UV dalam tangki"
    ],
    "at": "@02",
    "t": 3.41
   },
   "right": {
    "title": "NEON",
    "color": "#E86E5A",
    "items": [
     "Nanotrap",
     "Kompak",
     "3 suhu",
     "5 warna"
    ],
    "at": "@03",
    "t": 8.38
   },
   "t0": 3.41,
   "t1": 12.33
  },
  {
   "type": "pill",
   "top": 270,
   "html": "KELUARGA BESAR → VILLAEM 3",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 12.33,
   "t1": 17.31
  },
  {
   "type": "pill",
   "top": 250,
   "html": "RUMAH KECIL → NEON",
   "bg": "#E86E5A",
   "color": "#fff",
   "t0": 17.31,
   "t1": 22.13
  },
  {
   "type": "title",
   "top": 330,
   "size": 80,
   "html": "VILLAEM 3",
   "t0": 22.13,
   "t1": 30.67
  },
  {
   "type": "title",
   "top": 430,
   "size": 180,
   "html": "<span style='color:var(--yellow)'>RM74</span><small style='font-size:50px'> /bulan*</small>",
   "t0": 23.05,
   "t1": 30.67
  },
  {
   "type": "title",
   "top": 730,
   "size": 80,
   "html": "NEON",
   "t0": 27.21,
   "t1": 30.67
  },
  {
   "type": "title",
   "top": 830,
   "size": 180,
   "html": "<span style='color:var(--yellow)'>RM54</span><small style='font-size:50px'> /bulan*</small>",
   "t0": 27.808,
   "t1": 30.67
  },
  {
   "type": "pill",
   "top": 1110,
   "html": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 24.89,
   "t1": 30.67
  },
  {
   "type": "cta",
   "top": 620,
   "ticks": [
    "NASIHAT PERCUMA",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Harga asal RM120/bulan. Rebat ulang tahun Coway RM20 selama 7 bulan. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 30.67,
   "t1": null
  }
 ],
 "clips": {
  "clip4": {
   "dir": "../../out/frames/V308_clip4/",
   "n": 120,
   "start": 6.0
  }
 }
};
