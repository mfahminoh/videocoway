window.SPEC = {
 "scenes": [
  {
   "t0": 0.0,
   "bg": "dark",
   "t1": 6.97
  },
  {
   "t0": 6.97,
   "bg": "dark",
   "t1": 10.5
  },
  {
   "t0": 10.5,
   "bg": {
    "image": "../../assets/img/neon/podium5.jpg",
    "color": "pastel",
    "top": 420,
    "h": 1080,
    "mask": true
   },
   "t1": 13.15
  },
  {
   "t0": 13.15,
   "bg": "navy",
   "t1": 17.08
  },
  {
   "t0": 17.08,
   "bg": {
    "clip": "press_pour",
    "c0": 3.0,
    "c1": 6.6
   },
   "t1": 19.39
  },
  {
   "t0": 19.39,
   "bg": "blue",
   "t1": 22.83
  },
  {
   "t0": 22.83,
   "bg": "blue",
   "t1": 31.12
  }
 ],
 "els": [
  {
   "type": "icon",
   "top": 360,
   "icon": "pipe",
   "size": 300,
   "color": "#9aa6b8",
   "t0": 0.29,
   "t1": 6.97
  },
  {
   "type": "title",
   "top": 760,
   "size": 130,
   "html": "PAIP <span style='color:var(--yellow)'>LAMA?</span>",
   "t0": 0.29,
   "t1": 6.97
  },
  {
   "type": "text",
   "top": 960,
   "size": 50,
   "html": "Air boleh bawa <b style='color:var(--yellow)'>logam berat</b>",
   "t0": 4.03,
   "t1": 6.97
  },
  {
   "type": "title",
   "top": 250,
   "size": 100,
   "html": "LOGAM BERAT",
   "t0": 6.97,
   "t1": 10.5
  },
  {
   "type": "grid",
   "top": 470,
   "items": [
    {
     "big": "Hg",
     "small": "MERKURI",
     "at": "@03",
     "t": 6.97
    },
    {
     "big": "Pb",
     "small": "PLUMBUM",
     "at": "@04",
     "t": 8.5
    },
    {
     "big": "Fe",
     "small": "BESI",
     "at": "@05",
     "t": 9.2
    },
    {
     "big": "Al",
     "small": "ALUMINIUM",
     "at": "@06",
     "t": 9.75
    }
   ],
   "t0": 6.97,
   "t1": 10.5
  },
  {
   "type": "title",
   "top": 180,
   "size": 100,
   "html": "PENAPIS<br><span style='color:#E86E5A'>NANOTRAP</span>",
   "color": "#0B2F6B",
   "shadow": false,
   "t0": 10.5,
   "t1": 13.15
  },
  {
   "type": "icon",
   "top": 330,
   "icon": "shield",
   "size": 260,
   "color": "#fff",
   "t0": 13.15,
   "t1": 17.08
  },
  {
   "type": "chips",
   "top": 700,
   "items": [
    {
     "text": "LOGAM BERAT",
     "color": "#fff",
     "at": "@08%25",
     "t": 14.068
    },
    {
     "text": "BAKTERIA",
     "color": "#fff",
     "at": "@08%55",
     "t": 15.168
    },
    {
     "text": "VIRUS",
     "color": "#fff",
     "at": "@08%75",
     "t": 15.902
    }
   ],
   "t0": 13.15,
   "t1": 17.08
  },
  {
   "type": "pill",
   "top": 270,
   "html": "AIR BERSIH DARI DAPUR",
   "bg": "var(--yellow)",
   "color": "var(--navy)",
   "t0": 17.08,
   "t1": 19.39
  },
  {
   "type": "photo",
   "top": 160,
   "left": 360,
   "w": 360,
   "h": 360,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 19.39,
   "t1": 22.83
  },
  {
   "type": "price",
   "top": 560,
   "label": "DARI",
   "from": "RM54",
   "badge": "DISKAUN 50% · 6 BULAN PERTAMA",
   "to": "RM27",
   "t0": 19.39,
   "t1": 22.83,
   "badgeT": 19.875,
   "strikeT": 20.682,
   "toT": 21.166
  },
  {
   "type": "photo",
   "top": 200,
   "left": 330,
   "w": 420,
   "h": 420,
   "src": "../../assets/img/neon/pink.jpg",
   "t0": 22.83,
   "t1": null
  },
  {
   "type": "cta",
   "top": 720,
   "ticks": [
    "PENAPISAN NANOTRAP",
    "PEMASANGAN PERCUMA"
   ],
   "button": "WhatsApp saya",
   "fine": "*Diskaun 50% untuk 6 bulan pertama. Tertakluk pada terma &amp; promosi semasa Coway.",
   "t0": 22.83,
   "t1": null
  }
 ],
 "clips": {
  "press_pour": {
   "dir": "../../out/frames/NE08_press_pour/",
   "n": 111,
   "start": 3.0
  }
 }
};
