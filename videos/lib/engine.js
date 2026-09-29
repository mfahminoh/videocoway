/* Enjin animasi deterministik yang dikongsi oleh videos/<ID>/index.html.
   Setiap halaman mentakrif window.V (timing.js) dan fungsi seek(t) sendiri; render.py memanggil seek(t)
   bagi setiap bingkai dan menunggu Promise yang dipulangkan (bingkai klip). */
const $ = id => document.getElementById(id);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const E = {
  lin: x => x,
  out: x => 1 - Math.pow(1 - x, 3), in: x => x * x * x,
  inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  back: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  elastic: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1,
};
const p = (t, t0, t1, e = E.out) => e(clamp((t - t0) / (t1 - t0)));
const mix = (a, b, k) => a + (b - a) * k;
const interp = (x, pts) => {
  if (x <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) if (x <= pts[i][0]) { const [a, u] = pts[i - 1], [b, v] = pts[i]; return u + (v - u) * (x - a) / (b - a); }
  return pts[pts.length - 1][1];
};

function set(el, { o = 1, x = 0, y = 0, s = 1, r = 0, blur = 0 } = {}) {
  el = typeof el === 'string' ? $(el) : el;
  el.style.opacity = o;
  el.style.visibility = o <= 0.001 ? 'hidden' : 'visible';
  el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
  el.style.filter = blur > 0.05 ? `blur(${blur}px)` : '';
}
/* masuk pada tin, keluar pada tout (null = kekal) */
function inout(id, t, tin, tout, { dy = 60, dur = .45, outDur = .3, pop = false, sFrom = .8, dx = 0 } = {}) {
  const a = p(t, tin, tin + dur, pop ? E.back : E.out);
  const b = tout == null ? 0 : p(t, tout, tout + outDur, E.in);
  set(id, { o: Math.min(clamp(a * 1.4), 1 - b), x: mix(dx, 0, a), y: mix(dy, 0, a) - b * 50,
            s: pop ? mix(sFrom, 1, a) : 1, blur: (1 - clamp(a * 1.3)) * 8 + b * 8 });
}

/* ===== Klip: jujukan JPG (out/frames/<nama>/0001.jpg ...) dipramuat ===== */
const Clips = {
  defs: {},
  define(defs) {
    this.defs = defs;
    window.READY = Promise.all(Object.entries(defs).flatMap(([k, d]) => Array.from({ length: d.n }, (_, i) => {
      const im = new Image(); im.src = this.url(k, i + 1); return im.decode().catch(() => {});
    })));
  },
  url(k, i) { return `${this.defs[k].dir}${String(i).padStart(4, '0')}.jpg`; },
  /* papar klip k pada saat-klip c dalam <img id=imgId>; pulangkan Promise decode */
  show(imgId, k, c) {
    const d = this.defs[k], idx = clamp(Math.round(c * 30) + 1, 1, d.n);
    const u = new URL(this.url(k, idx), location.href).href, img = $(imgId);
    if (img.src !== u) { img.src = u; return img.decode().catch(() => {}); }
    return Promise.resolve();
  },
};

/* ===== Kapsyen: frasa [a, b, "teks *sorot*"] -> potongan 1-3 perkataan ===== */
function buildChunks(phrases) {
  const out = [];
  phrases.forEach(([a, b, text]) => {
    // perkataan + bendera sorot (sorotan *dua perkataan* boleh merentas potongan)
    let on = false;
    const words = text.split(' ').map(raw => {
      const start = raw.startsWith('*'), end = raw.replace(/[,.?!]+$/, '').endsWith('*');
      if (start) on = true;
      const w = { txt: raw.replace(/\*/g, ''), hl: on };
      if (end) on = false;
      return w;
    });
    const groups = []; let cur = [];
    words.forEach(w => { cur.push(w); const len = cur.map(x => x.txt).join(' ').length;
      if (cur.length >= 3 || len >= 16 || /[,.?!]$/.test(w.txt)) { groups.push(cur); cur = []; } });
    if (cur.length) groups.push(cur);
    const len = g => g.map(x => x.txt).join(' ').length;
    const tot = groups.reduce((s, g) => s + len(g), 0);
    let t0 = a;
    groups.forEach(g => { const d = (b - a) * len(g) / tot;
      out.push({ t0, t1: t0 + d, html: g.map(x => x.hl ? `<b>${x.txt}</b>` : x.txt).join(' ') }); t0 += d; });
  });
  out.forEach((c, i) => { c.hold = i + 1 < out.length ? Math.min(out[i + 1].t0, c.t1 + .45) : c.t1 + .6; });
  return out;
}
function caption(chunks, t, boxId = 'cap', textId = 'capText') {
  const c = chunks.filter(c => c.t0 <= t && t < c.hold).pop();
  if (!c) return set(boxId, { o: 0 });
  $(textId).innerHTML = c.html;
  const a = p(t, c.t0, c.t0 + .18, E.back);
  set(boxId, { o: 1, s: mix(.75, 1, a), y: mix(18, 0, a) });
}
