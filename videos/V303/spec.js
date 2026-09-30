window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "dark",
   "t1": 8.0
  },
  {
   "t0": 8.0,
   "bg": {
    "clip": "clip2",
    "c0": 3.3,
    "c1": 6.2
   },
   "t1": 10.86
  },
  {
   "t0": 10.86,
   "bg": {
    "clip": "clip4",
    "c0": 6.0,
    "c1": 8.3
   },
   "t1": 13.3
  },
  {
   "t0": 13.3,
   "bg": "navy",
   "t1": 18.5
  },
  {
   "t0": 18.5,
   "bg": {
    "clip": "clip5",
    "c0": 4.5,
    "c1": 6.2
   },
   "t1": 21.1
  },
  {
   "t0": 21.1,
   "bg": "navy",
   "t1": 24.55
  },
  {
   "t0": 24.55,
   "bg": {
    "clip": "clip5",
    "c0": 0.3,
    "c1": 4.2
   },
   "t1": 30.24
  },
  {
   "t0": 30.24,
   "bg": "blue",
   "t1": 36.15
  },
  {
   "t0": 36.15,
   "bg": "blue",
   "t1": 41.71
  }
 ],
 "els": [
  {
   "type": "icon",
   "top": 380,
   "icon": "drop",
   "size": 280,
   "color": "#9aa6b8",
   "t0": 0.33,
   "t1": 8.0
  },
  {
   "type": "title",
   "top": 760,
   "size": 120,
   "html": "BOLEH <span style='color:var(--yellow)'>TERCEMAR?</span>",
   "t0": 0.33,
   "t1": 8.0
  },
  {
   "type": "text",
   "top": 1110,
   "size": 50,
   "html": "Air lama tersimpan boleh dicemari <b style='color:var(--yellow)'>bakteria</b>",
   "t0": 3.89,
   "t1": 8.0
  },
  {
   "type": "pill",
   "top": 270,
   "html": "STERILISASI UV DALAM TANGKI",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 8.0,
   "t1": 13.3
  },
  {
   "type": "title",
   "top": 420,
   "size": 70,
   "html": "BAKTERIA DIHAPUSKAN",
   "t0": 13.3,
   "t1": 18.5
  },
  {
   "type": "counter",
   "top": 540,
   "from": 0,
   "to": 99.9,
   "suffix": "%",
   "decimals": 1,
   "dur": 1.2,
   "t0": 13.3,
   "t1": 18.5
  },
  {
   "type": "pill",
   "top": 270,
   "html": "AIR KEKAL BERSIH ✓",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 18.5,
   "t1": 21.1
  },
  {
   "type": "card",
   "top": 760,
   "icon": "filter",
   "title": "PENAPISAN RO",
   "sub": "Sebelum air masuk ke tangki",
   "t0": 21.1,
   "t1": 24.55
  },
  {
   "type": "chips",
   "top": 280,
   "items": [
    {
     "text": "TANGKI 11.4L",
     "color": "#fff",
     "at": "@07",
     "t": 24.55
    },
    {
     "text": "TETAP BERSIH ✓",
     "color": "#fff",
     "at": "@07%50",
     "t": 27.23
    }
   ],
   "t0": 24.55,
   "t1": 30.24
  },
  {
   "type": "price",
   "top": 520,
   "label": "HARGA ASAL",
   "from": "RM120",
   "to": "RM74",
   "badge": "+ REBAT ULANG TAHUN RM20 × 7 BULAN",
   "t0": 30.24,
   "t1": 36.15,
   "badgeT": 33.265,
   "strikeT": 30.79,
   "toT": 31.615
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
   "t0": 36.15,
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
   "t0": 36.15,
   "t1": null
  }
 ],
 "clips": {
  "clip2": {
   "dir": "../../out/frames/V303_clip2/",
   "n": 91,
   "start": 3.3
  },
  "clip4": {
   "dir": "../../out/frames/V303_clip4/",
   "n": 73,
   "start": 6.0
  },
  "clip5": {
   "dir": "../../out/frames/V303_clip5/",
   "n": 181,
   "start": 0.3
  }
 }
};
