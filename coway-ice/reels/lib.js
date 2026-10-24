/* Enjin animasi & komponen dikongsi (diekstrak dari src/index.html) untuk video Reels. */
const $ = id => document.getElementById(id);
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const E = {
  lin: x => x,
  out: x => 1 - Math.pow(1 - x, 3),
  inOut: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  in: x => x * x * x,
  back: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  elastic: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI) / 3) + 1,
  bounce: x => { const n = 7.5625, d = 2.75;
    if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75;
    if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; },
};
const p = (t, t0, t1, e = E.out) => e(clamp((t - t0) / (t1 - t0)));
const mix = (a, b, k) => a + (b - a) * k;
const rnd = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

function set(el, { o = 1, x = 0, y = 0, s = 1, r = 0, blur = 0 } = {}) {
  el = typeof el === 'string' ? $(el) : el;
  el.style.opacity = o;
  el.style.visibility = o <= 0.001 ? 'hidden' : 'visible';
  el.style.transform = `translate(${x}px,${y}px) scale(${s}) rotate(${r}deg)`;
  el.style.filter = blur > 0.05 ? `blur(${blur}px)` : '';
}
function inout(id, t, tin, tout, { dy = 60, dur = .45, outDur = .3, pop = false, sFrom = .85, dx = 0 } = {}) {
  const a = p(t, tin, tin + dur, pop ? E.back : E.out);
  const b = tout == null ? 0 : p(t, tout, tout + outDur, E.in);
  set(id, { o: Math.min(clamp(a * 1.4), 1 - b), x: mix(dx, 0, a), y: mix(dy, 0, a) - b * 60,
            s: pop ? mix(sFrom, 1, a) : 1, blur: (1 - clamp(a * 1.3)) * 10 + b * 8 });
}

/* ---------- Gelas berais (SVG) ---------- */
function glassSVG(uid, w, h, liquid, lAlpha, straw) {
  const cubes = [[62, 110, -12], [112, 96, 14], [80, 150, 8], [128, 150, -18], [100, 196, 4]]
    .map(([x, y, r], i) => `<g class="cube" data-i="${i}" data-x="${x}" data-y="${y}" data-r="${r}">
      <rect x="-24" y="-24" width="48" height="48" rx="10" fill="rgba(255,255,255,.72)" stroke="rgba(255,255,255,.95)" stroke-width="3"/>
      <rect x="-14" y="-16" width="14" height="8" rx="4" fill="#fff"/></g>`).join('');
  return `<svg width="${w}" height="${h}" viewBox="0 0 200 280">
    <defs><clipPath id="gc${uid}"><path d="M34 26 L166 26 L155 262 Q154 268 148 268 L52 268 Q46 268 45 262 Z"/></clipPath>
      <linearGradient id="lg${uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${liquid}" stop-opacity="${lAlpha * .75}"/>
      <stop offset="1" stop-color="${liquid}" stop-opacity="${lAlpha}"/></linearGradient></defs>
    ${straw ? `<path d="M120 -20 L140 -20 L112 200 L100 200 Z" fill="${straw}" transform="rotate(8 120 100)"/>` : ''}
    <g clip-path="url(#gc${uid})">
      <rect x="0" y="78" width="200" height="200" fill="url(#lg${uid})"/>
      <rect x="0" y="74" width="200" height="8" fill="rgba(255,255,255,.45)"/>
      ${cubes}
    </g>
    <path d="M30 20 L170 20 L158 264 Q157 274 148 274 L52 274 Q43 274 42 264 Z" fill="rgba(255,255,255,.12)" stroke="rgba(255,255,255,.95)" stroke-width="6" stroke-linejoin="round"/>
    <path d="M30 20 L170 20" stroke="#fff" stroke-width="8" stroke-linecap="round"/>
    <path d="M52 44 L60 230" stroke="rgba(255,255,255,.75)" stroke-width="9" stroke-linecap="round"/>
    <g fill="rgba(255,255,255,.8)"><circle cx="150" cy="120" r="4"/><circle cx="140" cy="170" r="3"/><circle cx="66" cy="250" r="3.5"/></g>
  </svg>`;
}
const DRINK = {
  teh:   ['#C8742F', .95, '#E5322D'],
  kopi:  ['#5A3420', .95, '#2EA7E0'],
  sirap: ['#F2679B', .9,  '#FFD23F'],
  air:   ['#9FD8F5', .35, null],
};
let uid = 0;
const mk = (el, d, w, h) => { const [c, a, s] = DRINK[d]; el.innerHTML = glassSVG(uid++, w, h, c, a, s); };

/* ---------- Ruang simpanan ais (SVG) ---------- */
const BIN = { x0: 90, x1: 710, yb: 690, cs: 76 };           // dalaman bekas
const COLS = 8, ROWS = 6;
function buildBin(svg, id) {
  let cubes = '';
  for (let i = 0; i < COLS * ROWS; i++)
    cubes += `<g id="${id}c${i}"><rect x="-34" y="-34" width="68" height="68" rx="16" fill="url(#${id}ice)" stroke="rgba(255,255,255,.95)" stroke-width="3"/>
      <rect x="-22" y="-24" width="20" height="10" rx="5" fill="#fff" opacity=".9"/></g>`;
  svg.innerHTML = `<defs>
      <linearGradient id="${id}ice" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#A9DDF7" stop-opacity=".85"/></linearGradient>
      <clipPath id="${id}clip"><rect x="70" y="150" width="660" height="560" rx="40"/></clipPath>
      <linearGradient id="${id}back" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A2B5E"/><stop offset="1" stop-color="#113F82"/></linearGradient></defs>
    <rect x="200" y="0" width="400" height="120" rx="26" fill="#1c1f22" stroke="#3a4046" stroke-width="4"/>
    <text x="400" y="74" text-anchor="middle" font-family="P" font-weight="700" font-size="34" fill="#A9DDF7" letter-spacing="4">ICE MAKER</text>
    <rect x="340" y="112" width="120" height="44" rx="10" fill="#2a2f34"/>
    <rect x="70" y="150" width="660" height="560" rx="40" fill="url(#${id}back)"/>
    <g clip-path="url(#${id}clip)">${cubes}<rect id="${id}shine" x="-300" y="150" width="160" height="560" fill="rgba(255,255,255,.35)" transform="skewX(-20)"/></g>
    <rect x="70" y="150" width="660" height="560" rx="40" fill="none" stroke="rgba(255,255,255,.85)" stroke-width="10"/>
    <rect x="96" y="180" width="16" height="200" rx="8" fill="rgba(255,255,255,.3)"/>
    <g id="${id}gauge">
      <rect x="752" y="150" width="30" height="560" rx="15" fill="rgba(255,255,255,.15)"/>
      <rect id="${id}lvl" x="752" y="150" width="30" height="560" rx="15" fill="#2EA7E0"/>
    </g>
    <rect x="-10" y="600" width="260" height="96" rx="48" fill="#fff" opacity=".96"/>
    <text id="${id}g" x="120" y="666" text-anchor="middle" font-family="P" font-weight="800" font-size="52" fill="#0B2F6B">0g</text>`;
}
function cubePos(i) {
  const col = i % COLS, row = Math.floor(i / COLS);
  const x = BIN.x0 + 38 + col * ((BIN.x1 - BIN.x0 - 76) / (COLS - 1)) + (row % 2 ? 14 : -6);
  const y = BIN.yb - 40 - row * 72;
  return [x, y, (rnd(i) - .5) * 40];
}
/* lukis kiub dalam bekas; fill(i) -> masa jatuh kiub i (null = tiada) */
function drawBin(id, t, dropAt, gaugeFrom = 0) {
  let landed = 0;
  for (let i = 0; i < COLS * ROWS; i++) {
    const g = $(`${id}c${i}`), td = dropAt(i);
    if (td == null || t < td) { g.setAttribute('visibility', 'hidden'); continue; }
    const [x, y, r] = cubePos(i), k = clamp((t - td) / .42);
    const yy = mix(40, y, E.bounce(k)), rr = mix(r + 90, r, E.out(k));
    g.setAttribute('visibility', 'visible');
    g.setAttribute('transform', `translate(${x} ${yy}) rotate(${rr})`);
    if (k >= 1) landed++;
  }
  const f = clamp(gaugeFrom + landed / (COLS * ROWS) * (1 - gaugeFrom));
  $(`${id}lvl`).setAttribute('y', 150 + 560 * (1 - f)); $(`${id}lvl`).setAttribute('height', 560 * f);
  $(`${id}g`).textContent = `${Math.round(f * 700)}g`;
  return f;
}

/* ---------- Footage (bingkai JPG dari prep.py) ---------- */
const CLIPN = { drop: 73, dispense: 88 };
window.__pending = [];
function clipFrame(name, imgId, t, t0, dur) {
  const n = CLIPN[name], rate = Math.min(1, n / 30 / dur), f = clamp(Math.floor((t - t0) * 30 * rate) + 1, 1, n);
  const src = `../build/frames/${name}/${String(f).padStart(4, '0')}.jpg`, img = $(imgId);
  if (img.getAttribute('src') !== src) { img.setAttribute('src', src); window.__pending.push(img.decode().catch(() => {})); }
}
/* kiub ais dalam gelas terapung perlahan */
function bobCubes(t) {
  document.querySelectorAll('.cube').forEach(c => {
    const i = +c.dataset.i, bob = Math.sin(t * 3.2 + i * 1.3) * 5;
    c.setAttribute('transform', `translate(${c.dataset.x} ${+c.dataset.y + bob}) rotate(${+c.dataset.r + Math.sin(t * 2 + i) * 4})`);
  });
}
/* kilat putih pada pertukaran babak */
function flashAt(t, times, k = .6) {
  let fl = 0;
  for (const tt of times)
    if (t >= tt - .12 && t < tt + .45) fl = Math.max(fl, k * (t < tt ? p(t, tt - .12, tt, E.lin) : 1 - p(t, tt, tt + .45, E.out)));
  set('flash', { o: fl });
}
function boot(seek) {
  window.seek = seek;
  window.render = async t => { window.__pending = []; seek(t); await Promise.all(window.__pending); };
  seek(0);
}
