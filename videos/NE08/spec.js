window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "dark",
   "t1": 6.06
  },
  {
   "t0": 6.06,
   "bg": "dark",
   "t1": 9.67
  },
  {
   "t0": 9.67,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 11.83
  },
  {
   "t0": 11.83,
   "bg": "navy",
   "t1": 15.39
  },
  {
   "t0": 15.39,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 5.2
   },
   "t1": 17.65
  },
  {
   "t0": 17.65,
   "bg": "blue",
   "t1": 23.46
  },
  {
   "t0": 23.46,
   "bg": "blue",
   "t1": 31.11
  }
 ],
 "els": [
  {
   "type": "icon",
   "top": 360,
   "icon": "pipe",
   "size": 300,
   "color": "#9aa6b8",
   "t0": 0.1,
   "t1": 6.06
  },
  {
   "type": "title",
   "top": 760,
   "size": 130,
   "html": "PAIP <span style='color:var(--yellow)'>LAMA?</span>",
   "t0": 0.1,
   "t1": 6.06
  },
  {
   "type": "text",
   "top": 960,
   "size": 50,
   "html": "Air boleh bawa <b style='color:var(--yellow)'>logam berat</b>",
   "t0": 3.24,
   "t1": 6.06
  },
  {
   "type": "title",
   "top": 250,
   "size": 100,
   "html": "LOGAM BERAT",
   "t0": 6.06,
   "t1": 9.67
  },
  {
   "type": "grid",
   "top": 470,
   "items": [
    {
     "big": "Hg",
     "small": "MERKURI",
     "at": "@03",
     "t": 6.06
    },
    {
     "big": "Pb",
     "small": "PLUMBUM",
     "at": "@04",
     "t": 7.45
    },
    {
     "big": "Fe",
     "small": "BESI",
     "at": "@05",
     "t": 8.0
    },
    {
     "big": "Al",
     "small": "ALUMINIUM",
     "at": "@06",
     "t": 8.32
    }
   ],
   "t0": 6.06,
   "t1": 9.67
  },
  {
   "type": "title",
   "top": 180,
   "size": 100,
   "html": "PENAPIS<br><span style='color:#E86E5A'>NANOTRAP</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 9.67,
   "t1": 11.83
  },
  {
   "type": "icon",
   "top": 330,
   "icon": "shield",
   "size": 260,
   "color": "#fff",
   "t0": 11.83,
   "t1": 15.39
  },
  {
   "type": "chips",
   "top": 700,
   "items": [
    {
     "text": "LOGAM BERAT",
     "color": "#fff",
     "at": "@08%25",
     "t": 12.598
    },
    {
     "text": "BAKTERIA",
     "color": "#fff",
     "at": "@08%55",
     "t": 13.518
    },
    {
     "text": "VIRUS",
     "color": "#fff",
     "at": "@08%75",
     "t": 14.133
    }
   ],
   "t0": 11.83,
   "t1": 15.39
  },
  {
   "type": "pill",
   "top": 270,
   "html": "AIR BERSIH DARI DAPUR",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 15.39,
   "t1": 17.65
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 17.65,
   "t1": 23.46
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM104",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "to": "RM54",
   "t0": 17.65,
   "t1": 23.46,
   "badgeT": 21.516,
   "strikeT": 19.261,
   "toT": 20.066
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 23.46,
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
   "t0": 23.46,
   "t1": null
  }
 ],
 "clips": {
  "press_pour": {
   "dir": "../../out/frames/NE08_press_pour/",
   "n": 70,
   "start": 3.0
  }
 },
 "theme": "coway",
 "brand": "COWAY",
 "tagline": "Own Your Aesthetics, Affordably."
};
