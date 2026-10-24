/* Pemain "hype": video laju bertenaga tinggi. SPEC.style memilih gaya: kinetic | paper | comic | glow | ugc.
   Elemen: words, img, temps, gift, burst, tag, ticker, cta. Bergantung pada engine.js; dimuat oleh build_video.py
   bila spec.json ada "player": "hype". */
const SP = window.SPEC, ST = SP.style || 'kinetic';
document.body.classList.add('st-' + ST);
window.DURATION = V.dur;
const CH = buildChunks(V.lines);
Clips.define(SP.clips);
const rnd = i => { const x = Math.sin(i * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
const LIGHTBG = ['k-white', 'k-pink', 'k-sky', 'paper-cream', 'paper-pink', 'paper-sky', 'comic-white', 'comic-sky', 'ugc-white'];
const isLight = sc => typeof sc.bg === 'string' && LIGHTBG.includes(sc.bg);
const ICO = {
  hot: '<path d="M32 6 C36 18 48 24 48 38 a16 16 0 0 1 -32 0 c0-8 5-12 8-16 c1 6 4 9 7 9 c-2-8 1-17 1-25 Z"/>',
  cold: '<path d="M32 6 V58 M9.5 19 L54.5 45 M54.5 19 L9.5 45 M24 10 L32 18 L40 10 M24 54 L32 46 L40 54"/>',
  room: '<path d="M32 8 C44 26 50 34 50 44 a18 18 0 0 1 -36 0 C14 34 20 26 32 8 Z"/>',
};
const TEMP = { hot: ['PANAS', 'var(--hot)'], cold: ['SEJUK', 'var(--cold)'], room: ['SUHU BILIK', 'var(--room)'] };
const WA_SVG = `<svg width="84" height="84" viewBox="0 0 64 64"><path d="M32 4 A28 28 0 0 0 8 46 L4 60 L18.5 56 A28 28 0 1 0 32 4 Z" fill="#fff"/>
  <path d="M24 18 c-2 0-4 3-4 6 c0 9 11 20 20 20 c3 0 6-2 6-4 l-1-4 l-6-2 l-3 3 c-4-2-7-5-9-9 l3-3 l-2-6 Z" fill="#25D366"/></svg>`;
const CONF = ['#04A4E4', '#ff8fb1', '#ffd23f', '#ffffff', '#20b58f', '#CEF3FF'];

/* ---------- bina DOM ---------- */
const stage = $('stage');
stage.insertAdjacentHTML('beforeend', `<div class="layer" id="bgColor"></div><div class="layer" id="deco"></div>
  <img id="bgImg" alt="" style="position:absolute; opacity:0"><div class="layer" id="clipL"><img id="clipImg" alt=""></div><div class="layer" id="shade"></div>
  <div class="layer" id="tex"></div><div id="world"></div>`);
{
  const first = Object.keys(SP.clips)[0];
  $('clipImg').src = first ? Clips.url(first, 1) : '../../assets/img/hype/neon_pink.png';   // render.py menunggu semua <img> ada kandungan
  $('bgImg').src = (SP.scenes.find(s => s.bg && s.bg.image) || { bg: { image: '../../assets/img/hype/neon_pink.png' } }).bg.image;
  const pics = [...new Set([...SP.scenes.filter(s => s.bg && s.bg.image).map(s => s.bg.image), ...SP.els.filter(e => e.src).map(e => e.src)])];
  window.READY = Promise.all([window.READY, document.fonts.ready, ...pics.map(u => { const im = new Image(); im.src = u; return im.decode().catch(() => {}); })]);
}
if (ST === 'paper')   // tekstur kertas
  $('tex').style.cssText = `background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .45 0 0 0 0 .4 0 0 0 .55 0'/></filter><rect width='400' height='400' filter='url(%23n)'/></svg>"); opacity:.35; mix-blend-mode:multiply`;

const world = $('world');
const hits = [];
SP.els.forEach((e, i) => {
  e.id = 'e' + i;
  const top = e.top != null ? `top:${e.top}px;` : '';
  let h = '';
  switch (e.type) {
    case 'words': h = `<div class="el c words" style="${top}">${e.items.map((w, k) => `<div class="w${w.box ? ' box' : ''}${w.sans ? ' sans' : ''}${w.inline ? ' in' : ''}" id="${e.id}_${k}"
        style="${w.bg ? `--wbg:${w.bg};` : ''}${w.g || e.g ? `--g:${w.g || e.g};` : ''}"><span style="font-size:${w.size || e.size || 150}px; color:${w.color || e.color || (w.box || w.bg || ST === 'paper' ? 'var(--ink)' : '#fff')}">${w.txt}</span></div>`).join('')}</div>`; break;
    case 'img': h = `<img class="el pic" src="${e.src}" style="${top} left:${e.left != null ? e.left : (1080 - e.w) / 2}px; width:${e.w}px; --g:${e.g || '#04A4E4'}">`; break;
    case 'temps': h = `<div class="el c" style="${top}">${e.items.map((it, k) => `<div class="tp" id="${e.id}_${k}" style="--tc:${TEMP[it.k][1]}">
        <i><svg width="84" height="84" viewBox="0 0 64 64" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">${ICO[it.k]}</svg></i>
        <b><small>AIR</small>${TEMP[it.k][0]}</b></div>`).join('')}</div>`; break;
    case 'gift': {
      const S = e.size || 640, box = e.box || '#04A4E4', rib = e.ribbon || '#ff8fb1', st = ST === 'comic' ? 'stroke="#111" stroke-width="4"' : '';
      const rays = Array.from({ length: 12 }, (_, k) => { const a = k * Math.PI / 6, b = a + .16;
        return `<path d="M100 110 L${100 + 190 * Math.cos(a)} ${110 + 190 * Math.sin(a)} L${100 + 190 * Math.cos(b)} ${110 + 190 * Math.sin(b)} Z"/>`; }).join('');
      h = `<div class="el" style="${top} left:${(1080 - S) / 2}px; width:${S}px; height:${S}px">
        <svg width="${S}" height="${S}" viewBox="0 0 200 200" style="overflow:visible; position:absolute">
          <g id="${e.id}_rays" fill="${e.rays || 'rgba(255,255,255,.55)'}" opacity="0">${rays}</g>
          <g id="${e.id}_body"><rect x="40" y="96" width="120" height="90" rx="6" fill="${box}" ${st}/><rect x="92" y="96" width="16" height="90" fill="${rib}" ${st}/></g>
          <g id="${e.id}_lid"><ellipse cx="84" cy="64" rx="19" ry="11" fill="${rib}" transform="rotate(-25 84 64)" ${st}/><ellipse cx="116" cy="64" rx="19" ry="11" fill="${rib}" transform="rotate(25 116 64)" ${st}/>
            <rect x="30" y="72" width="140" height="28" rx="6" fill="${box}" ${st}/><rect x="92" y="72" width="16" height="28" fill="${rib}" ${st}/><circle cx="100" cy="68" r="8" fill="${rib}" ${st}/></g>
        </svg><div id="${e.id}_conf" style="position:absolute; left:${S / 2}px; top:${S * .4}px">${Array.from({ length: 44 }, (_, k) =>
          `<i id="${e.id}_c${k}" style="position:absolute; width:${14 + 12 * rnd(k)}px; height:${22 + 14 * rnd(k + 50)}px; background:${CONF[k % CONF.length]}; border-radius:3px; opacity:0"></i>`).join('')}</div></div>`;
      break;
    }
    case 'burst': {
      const S = e.size || 420, pts = Array.from({ length: 32 }, (_, k) => { const a = k * Math.PI / 16, r = k % 2 ? 76 + 6 * rnd(k + i) : 100;
        return `${(r * Math.cos(a)).toFixed(1)},${(r * Math.sin(a)).toFixed(1)}`; }).join(' ');
      h = `<div class="el" style="${top} left:${(e.x || 540) - S / 2}px; width:${S}px; height:${S}px"><div class="burst" style="width:${S}px; height:${S}px">
        <svg viewBox="-104 -104 208 208" width="${S}" height="${S}"><polygon points="${pts}" fill="${e.color || '#ffd23f'}" ${ST === 'comic' ? 'stroke="#111" stroke-width="6" stroke-linejoin="round"' : ''}/></svg>
        <div style="font-size:${e.fs || 90}px; color:${e.textColor || '#fff'}">${e.html}</div></div></div>`;
      break;
    }
    case 'tag': h = `<div class="el c" style="${top}"><div id="${e.id}_sw" style="display:inline-block; position:relative; transform-origin:50% -300px">
        <div class="string" style="top:-300px; height:300px"></div><div class="tag" style="${e.bg ? `--tagbg:${e.bg};` : ''}${e.hole ? `--holebg:${e.hole}` : ''}">
        ${e.pre ? `<small style="margin:0 0 6px">${e.pre}</small>` : ''}<big>${e.big}</big><small>${e.sub || ''}</small></div></div></div>`; break;
    case 'ticker': h = `<div class="el" style="${top} left:0; width:1080px; height:130px"><div class="ticker" style="background:${e.bg || '#111'}; color:${e.color || '#fff'}; transform:rotate(${e.rot || 0}deg)">
        <span id="${e.id}_in">${Array(8).fill(e.text).join('&nbsp;&nbsp;★&nbsp;&nbsp;')}&nbsp;&nbsp;★&nbsp;&nbsp;</span></div></div>`; break;
    case 'cta': h = `<div class="el c" style="${top}">
        <div id="${e.id}_btn"><span class="wa">${WA_SVG}${e.button || 'WhatsApp saya'}</span></div>
        <div class="hand" id="${e.id}_hand" style="left:${e.handX || 850}px; top:90px">👆</div>
        <div class="fine" id="${e.id}_fine" style="color:${e.fineColor || 'rgba(255,255,255,.85)'}">${e.fine || '*Tertakluk pada terma &amp; syarat promosi semasa Coway.'}</div></div>`; break;
  }
  world.insertAdjacentHTML('beforeend', h.replace('class="el', `id="${e.id}" class="el`));
  if (e.hit) hits.push(e.t0);
  (e.items || []).forEach(w => { if (w.hit) hits.push(w.t); });
  if (e.openT != null) hits.push(e.openT);
});
if (SP.brand) stage.insertAdjacentHTML('beforeend', `<div class="el" id="brandTag">${SP.brand}</div>`);
stage.insertAdjacentHTML('beforeend', '<div class="el c" id="cap"><div id="capText"></div></div><div class="layer" id="flash" style="opacity:0"></div>');

/* ---------- latar kertas koyak (gaya paper) ---------- */
let decoFor = -1;
const PAPER = { 'paper-blue': ['#0390c9', '#CEF3FF'], 'paper-cream': ['#CEF3FF', '#04A4E4'], 'paper-pink': ['#f7c6d3', '#ffffff'], 'paper-sky': ['#ffffff', '#04A4E4'] };
function paperDeco(idx) {
  if (decoFor === idx) return;
  decoFor = idx;
  const edge = (seed, y0, y1, step = 36) => Array.from({ length: Math.ceil(1080 / step) + 1 }, (_, k) => {
    const x = Math.min(1080, k * step); return `${x},${(mix(y0, y1, x / 1080) + (rnd(seed + k) - .5) * 34).toFixed(0)}`; }).join(' L');
  const a0 = 1250 + rnd(idx) * 250, a1 = 1450 + rnd(idx + 9) * 250, flip = idx % 2;
  const bg = SP.scenes[idx].bg, [pb, pc] = PAPER[bg] || PAPER['paper-cream'];
  $('deco').innerHTML = `<svg width="1080" height="1920"><path d="M${edge(idx * 31, flip ? a1 : a0, flip ? a0 : a1)} L1080,1920 L0,1920 Z" fill="${pb}"/>
    <path d="M${edge(idx * 17 + 5, 330 + 80 * rnd(idx + 3), 120)} L1080,0 L0,0 Z" fill="${pc}" opacity=".55"/></svg>`;
}

/* ---------- animasi ---------- */
const QT = ST === 'paper' ? (t => Math.floor(t * 12) / 12) : (t => t);   // kertas: gerak "stop-motion" 12 fps
function life(e, t, dur = .2) {   // 0..1 keluar
  return e.t1 == null ? 0 : p(t, e.t1 - dur, e.t1, E.in);
}
function wordAnim(id, t, t0, out, k, w) {
  let a = 0, o = 0, s = 1, x = 0, y = 0, blur = 0;
  let r = w.rot != null ? w.rot : 0;
  if (t >= t0) switch (ST) {
    case 'kinetic': a = p(t, t0, t0 + .18, E.out); o = clamp(a * 3); s = mix(2.6, 1, a); blur = (1 - a) * 14; break;
    case 'paper': a = p(t, t0, t0 + .3, E.back); o = 1; y = mix(-220, 0, a); r = (w.rot != null ? w.rot : (k % 2 ? 2.5 : -2.5)) - (1 - a) * 12; break;
    case 'comic': a = p(t, t0, t0 + .3, E.back); o = clamp(a * 3); s = mix(.2, 1, a); r = (w.rot != null ? w.rot : -4) - (1 - a) * 25; break;
    case 'glow': { const d = t - t0; o = d < .4 ? [1, 0, 1, 1, 0, .4, 1, 0, 1][Math.floor(d / .045)] ?? 1 : 1; s = 1 + Math.sin(t * 9 + k) * .006; break; }
    default: a = p(t, t0, t0 + .25, E.back); o = clamp(a * 3); s = mix(.4, 1, a);
  }
  set(id, { o: o * (1 - out), x, y: y - out * 50, s: s * (1 - out * .25), r, blur: blur + out * 6 });
}
function enter(e, t, kind) {   // masuk/keluar elemen tunggal
  const t0 = e.t0, out = life(e, t);
  let a = 0, o = 0, s = 1, x = 0, y = 0, r = e.rot || 0;
  if (t >= t0) {
    const k = kind || e.anim || 'pop';
    if (k === 'pop') { a = p(t, t0, t0 + .32, E.back); o = clamp(a * 3); s = mix(.2, 1, a); }
    else if (k === 'rise') { a = p(t, t0, t0 + .35, E.out); o = clamp(a * 3); y = mix(700, 0, a); }
    else if (k === 'drop') { a = p(t, t0, t0 + .45, E.back); o = 1; y = mix(-1300, 0, a); }
    else if (k === 'slideL' || k === 'slideR') { a = p(t, t0, t0 + .3, E.back); o = 1; x = mix(k === 'slideL' ? -1000 : 1000, 0, a); }
    else if (k === 'spin') { a = p(t, t0, t0 + .4, E.back); o = clamp(a * 3); s = mix(.2, 1, a); r += (1 - a) * -200; }
    else if (k === 'slam') { a = p(t, t0, t0 + .2, E.out); o = clamp(a * 3); s = mix(2.4, 1, a); }
    if (e.float && a >= 1) y += Math.sin((t - t0) * 2.4) * 10;
    if (e.zoom) s *= mix(1, e.zoom, p(t, t0, e.t1 || t0 + 3, E.lin));
  }
  set(e.id, { o: o * (1 - out), x, y: y - out * 60, s: s * (1 - out * .3), r });
}
function drawEl(e, T) {
  const t = QT(T);
  if (T < e.t0 - .01 || (e.t1 != null && T > e.t1 + .05)) { set(e.id, { o: 0 }); return; }
  switch (e.type) {
    case 'words': {
      set(e.id, { o: 1 });
      const out = life(e, t);
      e.items.forEach((w, k) => wordAnim(`${e.id}_${k}`, t, w.t, out, k, w));
      break;
    }
    case 'temps': {
      set(e.id, { o: 1 - life(e, t) });
      e.items.forEach((it, k) => {
        const a = p(t, it.t, it.t + .3, E.back), side = k % 2 ? 1 : -1;
        set(`${e.id}_${k}`, { o: t >= it.t ? 1 : 0, x: (1 - a) * side * 1100, r: ST === 'paper' ? side * 1.5 : 0, s: it.t <= t && t < it.t + .5 ? 1 + .06 * Math.sin(p(t, it.t + .3, it.t + .5, E.lin) * Math.PI) : 1 });
      });
      break;
    }
    case 'gift': {
      enter(e, t, 'pop');
      const op = e.openT, wig = t < op ? Math.sin((t - e.t0) * 32) * 7 * p(t, e.t0 + .3, op, E.in) : 0;
      $(e.id + '_body').setAttribute('transform', `rotate(${wig} 100 186)`);
      const d = t - op, k = p(t, op, op + .4, E.out);
      $(e.id + '_lid').setAttribute('transform', d < 0 ? `rotate(${wig} 100 186)` : `translate(${40 * k} ${-70 * k}) rotate(${-35 * k} 100 86)`);
      $(e.id + '_lid').setAttribute('opacity', 1 - p(t, op + .25, op + .5));
      const rays = $(e.id + '_rays');
      rays.setAttribute('opacity', d < 0 ? 0 : p(t, op, op + .25));
      rays.setAttribute('transform', `rotate(${d < 0 ? 0 : d * 35} 100 110) translate(100 110) scale(${mix(.3, 1, k)}) translate(-100 -110)`);
      for (let c = 0; c < 44; c++) {
        const el = $(`${e.id}_c${c}`);
        if (d < 0) { el.style.opacity = 0; continue; }
        const ang = -Math.PI / 2 + (rnd(c + 7) - .5) * 2.6, v = 900 + rnd(c + 3) * 900;
        const x = Math.cos(ang) * v * d, y = Math.sin(ang) * v * d + 1500 * d * d;
        el.style.opacity = 1 - p(t, op + 1.3, op + 1.9);
        el.style.transform = `translate(${x}px,${y}px) rotate(${d * 720 * (rnd(c) - .5) * 2}deg)`;
      }
      break;
    }
    case 'burst': {
      enter(e, t, e.anim || 'spin');
      const a = p(t, e.t0, e.t0 + .4);
      if (a >= 1) { const cur = $(e.id).style.transform; $(e.id).style.transform = cur + ` rotate(${Math.sin(t * 3) * 3}deg) scale(${1 + Math.max(0, Math.sin(t * 8)) * .04})`; }
      break;
    }
    case 'tag': {
      enter(e, t, 'drop');
      const d = t - e.t0 - .3;
      $(e.id + '_sw').style.transform = `rotate(${d < 0 ? 0 : 16 * Math.exp(-2.6 * d) * Math.sin(8 * d)}deg)`;
      break;
    }
    case 'ticker': {
      enter(e, t, e.anim || (e.rot > 0 ? 'slideR' : 'slideL'));
      const sp = $(e.id + '_in'), unit = sp.offsetWidth / 8;
      sp.style.transform = `translateX(${-((t * (e.speed || 260)) % unit)}px)`;
      break;
    }
    case 'cta': {
      set(e.id, { o: 1 - life(e, t) });
      const bt = e.btnT != null ? e.btnT : e.t0;
      const a = p(t, bt, bt + .35, E.back);
      set(e.id + '_btn', { o: t >= bt ? clamp(a * 3) : 0, s: mix(.2, 1, a) * (t > bt + .4 ? 1 + Math.max(0, Math.sin((t - bt) * 6)) * .06 : 1) });
      const hk = (t - bt - .5) % .9;
      set(e.id + '_hand', { o: t >= bt + .5 ? 1 : 0, y: hk < .15 ? hk / .15 * -30 : hk < .3 ? -30 + (hk - .15) / .15 * 30 : 0, x: 0, s: hk > .12 && hk < .2 ? .92 : 1 });
      set(e.id + '_fine', { o: p(t, bt + .6, bt + 1) });
      break;
    }
    default: enter(e, t);
  }
}

let lastScene = -1;
function seek(T) {
  const t = T - V.off;
  let idx = SP.scenes.findIndex(s => t >= s.t0 && t < s.t1);
  if (idx < 0) idx = t < 0 ? 0 : SP.scenes.length - 1;
  const sc = SP.scenes[idx];
  const bg = sc.bg;
  let pending = Promise.resolve();
  const k = (t - sc.t0) / (sc.t1 - sc.t0);
  if (typeof bg === 'string') {
    $('bgColor').className = 'layer bg-' + bg; set('bgColor', { o: 1 }); set('bgImg', { o: 0 }); set('clipL', { o: 0 }); set('shade', { o: 0 });
  } else if (bg.clip) {
    set('bgColor', { o: 0 }); set('bgImg', { o: 0 });
    pending = Clips.show('clipImg', bg.clip, mix(bg.c0, bg.c1, clamp(k)) - SP.clips[bg.clip].start);
    set('clipL', { o: 1, s: mix(1.04, 1.14, k) }); set('shade', { o: bg.shade === false ? 0 : 1 });
  } else if (bg.image) {
    $('bgColor').className = 'layer bg-' + (bg.color || 'k-white'); set('bgColor', { o: 1 }); set('clipL', { o: 0 }); set('shade', { o: 0 });
    const img = $('bgImg');
    if (!img.src.endsWith(bg.image.replace('../../', ''))) { img.src = bg.image; pending = img.decode().catch(() => {}); }
    Object.assign(img.style, { left: (bg.left || 0) + 'px', top: (bg.top || 0) + 'px', width: (bg.w || 1080) + 'px', height: (bg.h || 1920) + 'px', objectFit: bg.fit || 'cover' });
    set('bgImg', { o: 1, s: mix(1.1, 1.0, k) });
  }
  if (ST === 'paper') { set('deco', { o: typeof bg === 'string' ? 1 : 0 }); paperDeco(idx); } else set('deco', { o: 0 });

  // potongan babak: kilat + "punch zoom"; gegaran pada hentakan
  const since = t - sc.t0, cut = idx > 0 && since < .3;
  const fl = $('flash');
  if (ST === 'glow') { fl.style.background = '#000'; set(fl, { o: cut ? ([.9, .2, .8, 0, .5, 0][Math.floor(since / .05)] ?? 0) : 0 }); }
  else if (ST === 'paper') set(fl, { o: 0 });
  else { fl.style.background = isLight(sc) && ST === 'kinetic' ? '#111' : '#fff'; set(fl, { o: cut && since < .12 ? (1 - since / .12) * (ST === 'kinetic' ? .9 : .5) : 0 }); }
  let sx = 0, sy = 0;
  hits.forEach(h => { const d = t - h; if (d >= 0 && d < .35) { const f = 1 - d / .35; sx += 20 * f * Math.sin(d * 95); sy += 16 * f * Math.cos(d * 83); } });
  const punch = idx > 0 ? 1 + (ST === 'paper' ? 0 : .09) * (1 - p(t, sc.t0, sc.t0 + .3, E.out)) : 1;
  const jit = ST === 'paper' ? (rnd(Math.floor(t * 12)) - .5) * .5 : 0;
  world.style.transform = `translate(${sx}px,${sy}px) scale(${punch}) rotate(${jit}deg)`;
  $('clipL').style.translate = `${sx * .6}px ${sy * .6}px`;

  SP.els.forEach(e => drawEl(e, t));
  if (SP.cap !== false) caption(CH, t); else set('cap', { o: 0 });
  if (SP.brand) {
    const L = isLight(sc);
    $('brandTag').style.color = ST === 'glow' ? '#fff' : L ? '#04A4E4' : '#fff';
    if (ST !== 'glow') $('brandTag').style.textShadow = L ? 'none' : '0 2px 10px rgba(0,0,0,.4)';
  }
  lastScene = idx;
  return pending;
}
window.seek = seek;
