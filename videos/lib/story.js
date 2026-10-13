/* Pemain "story": iklan emosi sinematik. Membina halaman daripada window.SPEC + window.V (videos/peti_ais.py)
   dan melukis bingkai pada masa t melalui seek(t). Bergantung pada engine.js. */
const ICONS = {
  snow: '<path d="M32 6 V58 M9.5 19 L54.5 45 M9.5 45 L54.5 19 M24 10 L32 17 L40 10 M24 54 L32 47 L40 54"/>',
  leaf: '<path d="M12 52 C12 24 30 12 54 10 C54 36 40 52 12 52 Z"/><path d="M12 52 L38 26"/>',
  shield: '<path d="M32 6 L54 14 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V14 Z"/><path d="M22 32 L30 40 L43 25"/>',
  wind: '<path d="M8 24 H40 a8 8 0 1 0 -8 -8"/><path d="M8 36 H48 a8 8 0 1 1 -8 8"/><path d="M8 48 H26"/>',
  temp: '<path d="M26 38 V12 a6 6 0 0 1 12 0 V38 a11 11 0 1 1 -12 0 Z"/><path d="M32 22 V44"/>',
  bolt: '<path d="M36 6 L14 36 H30 L26 58 L50 26 H34 Z"/>',
  heart: '<path d="M32 54 C10 40 6 28 10 20 C14 12 26 10 32 20 C38 10 50 12 54 20 C58 28 54 40 32 54 Z"/>',
  drawer: '<rect x="8" y="12" width="48" height="40" rx="6"/><path d="M8 32 H56 M26 22 H38 M26 42 H38"/>',
  doors: '<rect x="12" y="6" width="40" height="52" rx="5"/><path d="M32 6 V34 M12 34 H52 M32 34 V58 M26 18 V24 M38 18 V24 M26 42 V48 M38 42 V48"/>',
  swap: '<path d="M10 22 H50 L40 12 M54 42 H14 L24 52"/>',
  drop: '<path d="M32 8 C44 26 50 34 50 44 a18 18 0 0 1 -36 0 C14 34 20 26 32 8 Z"/>',
  tool: '<path d="M40 8 a12 12 0 0 0 -12 16 L8 44 L20 56 L40 36 a12 12 0 0 0 16 -12 L48 32 L40 24 L48 16 Z"/>',
};
const icon = (k, size = 58, color = '#fff') =>
  `<svg width="${size}" height="${size}" viewBox="0 0 64 64" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">${ICONS[k] || ''}</svg>`;
const WA = `<svg width="78" height="78" viewBox="0 0 64 64"><path d="M32 4 A28 28 0 0 0 8 46 L4 60 L18.5 56 A28 28 0 1 0 32 4 Z" fill="#fff"/>
  <path d="M24 18 c-2 0-4 3-4 6 c0 9 11 20 20 20 c3 0 6-2 6-4 l-1-4 l-6-2 l-3 3 c-4-2-7-5-9-9 l3-3 l-2-6 Z" fill="#25D366"/></svg>`;
const GRADE = {
  warm: 'sepia(.22) saturate(.92) contrast(1.06) brightness(.9)',
  night: 'saturate(.78) contrast(1.1) brightness(.78)',
  vintage: 'sepia(.5) saturate(.75) contrast(.94) brightness(1.02)',
  cool: 'saturate(1.06) contrast(1.04) brightness(1.02)',
  none: '',
};
const KB = {   // [skala mula, skala akhir, x mula, x akhir, y mula, y akhir]
  in: [1.0, 1.12, 0, 0, 0, 0], out: [1.13, 1.0, 0, 0, 0, 0], still: [1.03, 1.05, 0, 0, 0, 0],
  up: [1.12, 1.12, 0, 0, 50, -50], down: [1.12, 1.12, 0, 0, -50, 50], left: [1.12, 1.12, 40, -40, 0, 0], right: [1.12, 1.12, -40, 40, 0, 0],
};
const XF = 0.6;

const SP = window.SPEC;
window.DURATION = V.dur;
Clips.define(SP.clips);
const stage = $('stage');
const add = h => stage.insertAdjacentHTML('beforeend', h);
const hl = s => s.replace(/\*([^*]+)\*/g, '<b>$1</b>');

/* ---------- syot ---------- */
SP.shots.forEach((s, i) => {
  s.id = 'sh' + i;
  const src = s.img ? s.img : s.clip ? Clips.url(s.clip, 1) : null;
  let h = `<div class="layer shot ${s.color ? 'col-' + s.color : ''}" id="${s.id}" style="opacity:0">`;
  if (src && s.fit === 'contain') h += `<img class="blur" id="${s.id}_b" src="${src}">`;
  if (src) h += `<img class="${s.fit === 'contain' ? 'fg' : ''}" id="${s.id}_i" src="${src}" style="transform-origin:${s.zx ?? 50}% ${s.zy ?? 50}%; filter:${GRADE[s.grade || 'none']}">`;
  add(h + '</div>');
});
add('<div class="layer" id="vig"></div><div class="layer" id="shadeB"></div><div class="layer" id="dim"></div>');
{
  const pics = [...new Set([...SP.shots.filter(s => s.img).map(s => s.img), ...SP.els.filter(e => e.src).map(e => e.src)])];
  window.READY = Promise.all([window.READY, ...pics.map(u => { const im = new Image(); im.src = u; return im.decode().catch(() => {}); })]);
}

/* ---------- elemen ---------- */
SP.els.forEach((e, i) => {
  e.id = 'e' + i;
  const top = e.top != null ? `top:${e.top}px;` : '';
  const col = e.color ? `color:${e.color};` : '';
  let h = '';
  switch (e.type) {
    case 'quote': h = `<div class="el c quote" style="${top}${col}${e.size ? `font-size:${e.size}px;` : ''}">${e.lines.map((ln, k) =>
        `<div>${ln.replace(/\*([^*]+)\*/g, '<em>$1</em>').split(/(<em>.*?<\/em>|\s+)/).filter(x => x && !/^\s+$/.test(x))
          .map((w, j) => `<span class="w" data-l="${k}">${w}</span>`).join(' ')}</div>`).join('')}</div>`; break;
    case 'kicker': h = `<div class="el c" style="${top}${col}"><span class="kicker"><i></i>${e.text}<i></i></span></div>`; break;
    case 'big': h = `<div class="el c big" style="${top}${col}${e.size ? `font-size:${e.size}px;` : ''}"><span>${e.text}${e.strikeT != null ? `<i class="strike" id="${e.id}_s"></i>` : ''}</span>${e.sub ? `<small>${e.sub}</small>` : ''}</div>`; break;
    case 'bubble': h = `<div class="el" style="${top} left:${e.left ?? 90}px"><div class="bubble">${e.who ? `<small>${e.who}</small>` : ''}${e.text}</div></div>`; break;
    case 'cal': h = `<div class="el c" style="${top}"><div class="cal"><b>${e.month || 'MINGGU INI'}</b><span id="${e.id}_d">${e.items[0].text}</span></div></div>`; break;
    case 'stamp': h = `<div class="el c" style="${top}"><span class="stamp" style="transform:rotate(${e.rot ?? -7}deg)">${e.text}</span></div>`; break;
    case 'year': h = `<div class="el c year" style="${top}${col}"><span id="${e.id}_n">${e.from}</span>${e.label ? `<small>${e.label}</small>` : ''}</div>`; break;
    case 'prod': h = `<div class="el c prod" style="${top}${col}"><small>${e.small || 'Peti Ais Coway'}</small><h2>${e.title}</h2>${e.sub ? `<p>${e.sub}</p>` : ''}</div>`; break;
    case 'logo': h = `<div class="el c logo" style="${top}${col}">coway</div>`; break;
    case 'feats': h = `<div class="el c" style="${top}">${e.items.map((f, k) => `<div class="feat" id="${e.id}_${k}"><div class="ic">${icon(f.icon)}</div><div>${f.title}${f.sub ? `<small>${f.sub}</small>` : ''}</div></div>`).join('')}</div>`; break;
    case 'photo': h = `<div class="el" style="${top} left:${e.left ?? 140}px; width:${e.w ?? 800}px; height:${e.h ?? 800}px; border-radius:${e.radius ?? 40}px; overflow:hidden;
        box-shadow:0 30px 70px rgba(0,0,0,.5); border:${e.border === false ? 0 : 6}px solid rgba(255,255,255,.92)"><img id="${e.id}_i" src="${e.src}" style="width:100%; height:100%; object-fit:cover; object-position:${e.pos || '50% 50%'}">
        ${e.label ? `<div style="position:absolute; left:0; right:0; bottom:0; padding:22px 26px; font-size:36px; font-weight:700; background:linear-gradient(180deg,transparent,rgba(0,0,0,.75))">${e.label}</div>` : ''}</div>`; break;
    case 'price': h = `<div class="el c" style="${top}"><div class="price"><div class="lab">${e.label || 'SERENDAH'}</div>
        <div class="amt"><sup>RM</sup>${e.amount}</div><div class="per">${e.per || 'sebulan'}</div>
        ${e.note ? `<div class="note" id="${e.id}_n">${e.note}</div>` : ''}${e.note2 ? `<div class="note2" id="${e.id}_n2">${e.note2}</div>` : ''}</div></div>`; break;
    case 'cta': h = `<div class="el c" style="${top}">${e.tag ? `<div class="tag" id="${e.id}_t">${e.tag}</div>` : ''}
        <div id="${e.id}_b"><span class="wa">${WA}${e.button || 'WhatsApp saya'}</span></div>
        <div class="fine" id="${e.id}_f">${e.fine || '*Harga dari, pelan Heart Service 7 tahun. Tertakluk pada kelayakan, terma &amp; promosi semasa Coway.'}</div></div>`; break;
  }
  add(h.replace('class="el', `id="${e.id}" class="el`));
});
add('<div class="el c" id="cap"><div id="capText"></div></div><div class="layer" id="grain"></div><div class="layer" id="flash"></div>');

/* ---------- kapsyen: ayat penuh, ayat panjang dipecah dua ---------- */
const CAPS = [];
V.lines.forEach(([a, b, text]) => {
  if (!text) return;
  let parts = [text];
  if (text.replace(/\*/g, '').length > 70) {
    const cuts = [...text.matchAll(/[.?!,]\s/g)].map(m => m.index + 1);
    if (cuts.length) {
      const mid = text.length / 2, k = cuts.reduce((x, y) => Math.abs(y - mid) < Math.abs(x - mid) ? y : x);
      parts = [text.slice(0, k).trim(), text.slice(k).trim()];
    }
  }
  const tot = parts.reduce((s, x) => s + x.length, 0);
  let t0 = a;
  parts.forEach(x => { const d = (b - a) * x.length / tot; CAPS.push({ t0, t1: t0 + d, html: hl(x) }); t0 += d; });
});
CAPS.forEach((c, i) => { c.hold = i + 1 < CAPS.length ? Math.min(CAPS[i + 1].t0, c.t1 + .5) : c.t1 + .6; });

/* ---------- lukis ---------- */
function drawShots(t) {
  const i = SP.shots.findIndex(s => t >= s.t0 && t < s.t1);
  const cur = i < 0 ? SP.shots.length - 1 : i;
  const pend = [];
  SP.shots.forEach((s, k) => {
    const el = $(s.id);
    const xf = s.cut ? 0.001 : XF;
    let o = 0;
    if (k === cur) o = k === 0 ? 1 : p(t, s.t0, s.t0 + xf, E.inOut);
    else if (k === cur - 1 && t < SP.shots[cur].t0 + (SP.shots[cur].cut ? 0.001 : XF)) o = 1;
    el.style.opacity = o;
    el.style.visibility = o > 0 ? 'visible' : 'hidden';
    el.style.zIndex = k === cur ? 2 : 1;
    if (o <= 0) return;
    const [s0, s1, x0, x1, y0, y1] = KB[s.kb || 'in'];
    const k2 = clamp((t - s.t0 + XF) / (s.t1 - s.t0 + XF * 2));
    const tr = `translate(${mix(x0, x1, k2)}px,${mix(y0, y1, k2) + (s.oy || 0)}px) scale(${mix(s0, s1, E.inOut(k2) * .6 + k2 * .4) * (s.sc || 1)})`;
    const im = $(s.id + '_i');
    if (im) im.style.transform = tr;
    if (s.clip) {
      const c = mix(s.c0, s.c1, clamp((t - s.t0) / (s.t1 - s.t0))) - SP.clips[s.clip].start;
      pend.push(Clips.show(s.id + '_i', s.clip, c));
      if (s.fit === 'contain') pend.push(Clips.show(s.id + '_b', s.clip, c));
    }
  });
  const sc = SP.shots[cur];
  document.body.classList.toggle('light', !!sc.light);
  set('vig', { o: sc.light ? 0 : 1 }); set('shadeB', { o: sc.light ? 0 : (sc.shade ?? 1) });
  return Promise.all(pend);
}

function words(e, t) {
  const ws = [...$(e.id).querySelectorAll('.w')];
  const per = e.per ?? .09;
  const lineStart = (e.lineAt || []).map(x => x);
  ws.forEach((w, j) => {
    const l = +w.dataset.l;
    const base = lineStart[l] != null ? lineStart[l] : e.t0;
    const idx = ws.filter(x => +x.dataset.l === l).indexOf(w);
    const a = p(t, base + idx * per, base + idx * per + .55, E.out);
    w.style.opacity = a; w.style.transform = `translateY(${(1 - a) * 28}px)`; w.style.filter = a < .99 ? `blur(${(1 - a) * 10}px)` : '';
  });
}

function drawEl(e, t) {
  const out = e.t1 == null ? null : e.t1 - .35;
  const pop = ['stamp', 'big', 'cal', 'year'].includes(e.type);
  inout(e.id, t, e.t0, out, pop ? { pop: true, sFrom: e.type === 'stamp' ? 2.0 : .7, dy: 0 } : { dy: e.type === 'photo' ? 90 : 50, dur: .7, outDur: .4 });
  switch (e.type) {
    case 'quote': words(e, t); break;
    case 'feats': e.items.forEach((f, k) => inout(`${e.id}_${k}`, t, f.t, out, { dx: -90, dy: 0, dur: .55 })); break;
    case 'cal': {
      let cur = e.items[0], ci = 0; e.items.forEach((it, k) => { if (t >= it.t) { cur = it; ci = k; } });
      $(e.id + '_d').textContent = cur.text;
      const k = ci ? p(t, cur.t, cur.t + .4, E.back) : 1;
      set(e.id + '_d', { s: mix(.6, 1, k), o: clamp(k * 2) });
      break;
    }
    case 'big': if (e.strikeT != null) $(e.id + '_s').style.transform = `scaleX(${p(t, e.strikeT, e.strikeT + .35, E.inOut)})`; break;
    case 'year': {
      const k = p(t, e.t0 + (e.delay ?? .3), e.t0 + (e.delay ?? .3) + (e.dur ?? 2.2), E.inOut);
      $(e.id + '_n').textContent = Math.round(mix(e.from, e.to, k));
      break;
    }
    case 'photo': $(e.id + '_i').style.transform = `scale(${mix(1.12, 1, p(t, e.t0, e.t0 + 2.5, E.out))})`; break;
    case 'price': {
      if (e.noteT != null) inout(e.id + '_n', t, e.noteT, null, { pop: true, sFrom: .6, dy: 0 });
      if (e.note2T != null) inout(e.id + '_n2', t, e.note2T, null, { dy: 20 });
      break;
    }
    case 'cta': {
      const bt = e.btnT ?? e.t0 + .5;
      if (e.tag) inout(e.id + '_t', t, e.t0, null, { dy: 30, dur: .8 });
      inout(e.id + '_b', t, bt, null, { pop: true, sFrom: .5, dy: 0 });
      if (t > bt + .7) set(e.id + '_b', { s: 1 + Math.max(0, Math.sin((t - bt) * 4.5)) * .045 });
      inout(e.id + '_f', t, bt + .5, null, { dy: 10 });
      break;
    }
  }
}

function seek(T) {
  const t = T - V.off;
  const pending = drawShots(t);
  SP.els.forEach(e => drawEl(e, t));
  // gelapkan latar bila petikan besar dipapar
  const dims = SP.els.filter(e => e.dim && t >= e.t0 - .2 && (e.t1 == null || t < e.t1));
  set('dim', { o: dims.length ? Math.max(...dims.map(e => e.dim * Math.min(p(t, e.t0 - .2, e.t0 + .5), e.t1 == null ? 1 : 1 - p(t, e.t1 - .5, e.t1)))) : 0 });
  const c = CAPS.filter(c => c.t0 <= t && t < c.hold).pop();
  const hide = SP.els.some(e => e.hideCap && t >= e.t0 && (e.t1 == null || t < e.t1));
  if (!c || hide) set('cap', { o: 0 });
  else { $('capText').innerHTML = c.html; const a = p(t, c.t0, c.t0 + .25), b = p(t, c.hold - .2, c.hold); set('cap', { o: Math.min(a, 1 - b), y: (1 - a) * 14 }); }
  const g = $('grain'); const f = Math.floor(T * 24);
  g.style.transform = `translate(${(f * 73) % 200 - 100}px,${(f * 131) % 200 - 100}px)`;
  set('flash', { o: SP.flashes ? Math.max(0, ...SP.flashes.map(x => t >= x && t < x + .35 ? (1 - (t - x) / .35) * .55 : 0)) : 0 });
  return pending;
}
window.seek = seek;
