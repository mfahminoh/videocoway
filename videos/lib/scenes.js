/* Pemain video berasaskan data: membina halaman daripada window.SPEC (dihasilkan oleh videos/build_video.py)
   dan melukis bingkai pada masa t melalui seek(t). Bergantung pada engine.js. */
const ICON = {
  tech: '<circle cx="32" cy="18" r="10"/><path d="M12 56 c0-12 9-20 20-20 s20 8 20 20"/><path d="M44 30 l10 -10 m-4 -4 l8 8"/>',
  box: '<path d="M8 20 L32 8 L56 20 V46 L32 58 L8 46 Z"/><path d="M8 20 L32 32 L56 20 M32 32 V58"/>',
  drop: '<path d="M32 8 C44 26 50 34 50 44 a18 18 0 0 1 -36 0 C14 34 20 26 32 8 Z"/>',
  home: '<path d="M8 30 L32 10 L56 30"/><path d="M14 26 V56 H50 V26"/><path d="M27 56 V40 H37 V56"/>',
  clock: '<circle cx="32" cy="32" r="24"/><path d="M32 18 V32 L42 38"/>',
  shield: '<path d="M32 6 L54 14 V30 C54 44 44 54 32 58 C20 54 10 44 10 30 V14 Z"/><path d="M22 32 L30 40 L43 25"/>',
  lock: '<rect x="14" y="28" width="36" height="28" rx="6"/><path d="M22 28 V20 a10 10 0 0 1 20 0 V28"/>',
  filter: '<rect x="20" y="8" width="24" height="48" rx="8"/><path d="M20 20 H44 M20 44 H44"/>',
  money: '<circle cx="32" cy="32" r="24"/><path d="M38 24 c-2-3-11-4-12 1 c-1 6 13 4 12 11 c-1 5-10 5-13 1 M32 16 V48"/>',
  baby: '<rect x="22" y="22" width="20" height="34" rx="6"/><path d="M26 22 V16 h12 V22 M28 16 c0-6 8-6 8 0"/><path d="M22 34 H42"/>',
  cup: '<path d="M14 22 H44 V40 a14 14 0 0 1 -14 14 h-2 a14 14 0 0 1 -14 -14 Z"/><path d="M44 28 h4 a6 6 0 0 1 0 12 h-4"/><path d="M22 8 c-3 4 3 6 0 10 M32 8 c-3 4 3 6 0 10"/>',
  pipe: '<path d="M6 24 H34 a10 10 0 0 1 10 10 V58"/><path d="M6 38 H26 a4 4 0 0 1 4 4 V58"/><path d="M6 20 V42 M40 58 H52"/>',
  phone: '<rect x="18" y="6" width="28" height="52" rx="6"/><path d="M28 50 H36"/>',
  palette: '<path d="M32 8 a24 24 0 1 0 0 48 c4 0 5-4 3-7 c-2-3 0-7 4-7 h6 a11 11 0 0 0 11-11 C56 18 45 8 32 8 Z"/><circle cx="20" cy="30" r="3"/><circle cx="26" cy="20" r="3"/><circle cx="38" cy="18" r="3"/>',
  check: '<path d="M14 34 L27 46 L50 20"/>', x: '<path d="M18 18 L46 46 M46 18 L18 46"/>',
  ruler: '<rect x="6" y="22" width="52" height="20" rx="3"/><path d="M14 22 v8 M22 22 v12 M30 22 v8 M38 22 v12 M46 22 v8"/>',
};
const svgIcon = (k, color = '#0B4DA2', size = 90) =>
  `<svg width="${size}" height="${size}" viewBox="0 0 64 64" fill="none" stroke="${color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">${ICON[k] || ''}</svg>`;
const WA_SVG = `<svg width="74" height="74" viewBox="0 0 64 64"><path d="M32 4 A28 28 0 0 0 8 46 L4 60 L18.5 56 A28 28 0 1 0 32 4 Z" fill="#fff"/>
  <path d="M24 18 c-2 0-4 3-4 6 c0 9 11 20 20 20 c3 0 6-2 6-4 l-1-4 l-6-2 l-3 3 c-4-2-7-5-9-9 l3-3 l-2-6 Z" fill="#25D366"/></svg>`;
const NEON_UNIT = { mint: 150, ciel: 430, pink: 715, white: 1020, gray: 1262, all: 732 };
const NEON_NAME = { pink: ['Peach Pink', '#F3C9BD'], mint: ['Mint Green', '#C5DCCB'], ciel: ['Ciel Blue', '#BFD5E8'],
                    gray: ['Pebble Gray', '#3a3d42'], white: ['Porcelain White', '#F4F3EF'] };

const SP = window.SPEC;
window.DURATION = V.dur;
const CH = buildChunks(V.lines);
Clips.define(SP.clips);

/* ---------- bina DOM ---------- */
const stage = $('stage');
function add(html) { stage.insertAdjacentHTML('beforeend', html); }
add('<div class="layer" id="bgColor"></div><img id="bgImg" alt="" style="opacity:0"><div class="layer" id="clipL"><img id="clipImg" alt=""></div><div class="layer" id="shade"></div>');
const $img = $('bgImg');
{
  const first = Object.keys(SP.clips)[0];
  $('clipImg').src = first ? Clips.url(first, 1) : '../../assets/img/neon/podium5.jpg';   // render.py menunggu semua <img> ada kandungan
  $img.src = (SP.scenes.find(s => s.bg && s.bg.image) || { bg: { image: '../../assets/img/neon/podium5.jpg' } }).bg.image;
  const pics = [...new Set([...SP.scenes.filter(s => s.bg && s.bg.image).map(s => s.bg.image), ...SP.els.filter(e => e.src).map(e => e.src), '../../assets/img/neon/lineup5.png'])];
  window.READY = Promise.all([window.READY, ...pics.map(u => { const im = new Image(); im.src = u; return im.decode().catch(() => {}); })]);
}

SP.els.forEach((e, i) => {
  e.id = 'e' + i;
  const top = e.top != null ? `top:${e.top}px;` : '';
  const light = e.light ? ' light' : '';
  let h = '';
  switch (e.type) {
    case 'title': h = `<div class="el c h1${e.shadow === false ? '' : ' shadow'}" style="${top} font-size:${e.size || 110}px; color:${e.color || '#fff'}">${e.html}</div>`; break;
    case 'text': h = `<div class="el c" style="${top} font-size:${e.size || 44}px; font-weight:${e.weight || 600}; color:${e.color || '#fff'}; padding:0 90px; line-height:1.3">${e.html}</div>`; break;
    case 'banner': h = `<div class="el c" style="${top}"><span class="banner">${e.html}</span></div>`; break;
    case 'pill': h = `<div class="el c" style="${top}"><span class="pill" style="background:${e.bg || 'var(--yellow)'}; color:${e.color || 'var(--navy)'}">${e.html}</span></div>`; break;
    case 'reason': h = `<div class="el c" style="${top}"><div class="reason"><div class="num">${e.num}</div><div class="rt">${e.title}${e.sub ? `<small>${e.sub}</small>` : ''}</div></div></div>`; break;
    case 'chips': h = `<div class="el c" style="${top}">${e.items.map((c, k) => `<span class="chip" id="${e.id}_${k}" style="color:${c.color || '#fff'}">${c.text}</span>`).join('')}</div>`; break;
    case 'card': h = `<div class="el" style="${top} left:${e.left != null ? e.left : 140}px"><div class="card"><div class="ic" style="background:${e.icbg || '#e3eefc'}">${svgIcon(e.icon, e.iccolor)}</div><div><h3>${e.title}</h3>${e.sub ? `<p>${e.sub}</p>` : ''}</div></div></div>`; break;
    case 'stamp': h = `<div class="el c" style="${top}"><span class="stamp" style="border-color:${e.color || 'var(--red)'}; color:${e.color || 'var(--red)'}; transform:rotate(${e.rot != null ? e.rot : -6}deg)">${e.html}</span></div>`; break;
    case 'icon': h = `<div class="el c" style="${top}">${svgIcon(e.icon, e.color || '#fff', e.size || 220)}</div>`; break;
    case 'photo': h = `<div class="el" style="${top} left:${e.left}px; width:${e.w}px; height:${e.h}px; border-radius:${e.radius != null ? e.radius : 40}px; overflow:hidden; ${e.shadow === false ? '' : 'box-shadow:0 24px 60px rgba(0,0,0,.35);'}"><img id="${e.id}_img" src="${e.src}" style="width:100%; height:100%; object-fit:${e.fit || 'cover'}; transform-origin:${e.zx || 50}% ${e.zy || 50}%"></div>`; break;
    case 'lineup': h = `<div class="el" style="left:0; top:0; width:1080px; height:1920px; overflow:hidden"><img id="${e.id}_img" src="../../assets/img/neon/lineup5.png" style="position:absolute; width:1080px"></div>
        <div class="el c" id="${e.id}_lab" style="top:${e.labelTop || 1330}px"><span class="pill" style="background:#fff; color:var(--navy); box-shadow:0 10px 30px rgba(0,0,0,.12)"><i id="${e.id}_dot" style="display:inline-block; width:40px; height:40px; border-radius:50%; vertical-align:-6px; margin-right:16px; border:3px solid rgba(0,0,0,.12)"></i><span id="${e.id}_name"></span></span></div>`; break;
    case 'steps': h = `<div class="el c${light}" style="${top}">${e.items.map((s, k) => `<div class="row" id="${e.id}_${k}"><b>${s.num || k + 1}</b><span>${s.text}</span></div>`).join('')}</div>`; break;
    case 'grid': h = `<div class="el c" style="${top} padding:0 40px">${e.items.map((g, k) => `<div class="tile" id="${e.id}_${k}"><big style="color:${g.color || 'var(--yellow)'}">${g.big}</big><small>${g.small}</small></div>`).join('')}</div>`; break;
    case 'ticks': h = `<div class="el c" style="${top}">${e.items.map((s, k) => `<div id="${e.id}_${k}" style="margin-bottom:26px"><span class="tick"><i>✓</i>${s.text}</span></div>`).join('')}</div>`; break;
    case 'quiz': h = `<div class="el c" style="${top}">${e.options.map((o, k) => `<div class="opt" id="${e.id}_${k}"><b>${'ABCDE'[k]}</b><span>${o.text}</span><i style="background:${o.color}"></i></div>`).join('')}</div>`; break;
    case 'vs': h = `<div class="el c" style="${top}"><div class="vs">${[e.left, e.right].map((col, k) => `<div id="${e.id}_${k}"><h4 style="background:${col.color}">${col.title}</h4><ul>${col.items.map(it => `<li>${it}</li>`).join('')}</ul></div>`).join('')}</div></div>`; break;
    case 'counter': h = `<div class="el c h1 shadow" style="${top} font-size:${e.size || 220}px; color:${e.color || 'var(--yellow)'}"><span id="${e.id}_n"></span></div>`; break;
    case 'price': h = `<div class="el c" style="${top}">
        <div id="${e.id}_l" style="font-size:60px; font-weight:700; letter-spacing:6px">${e.label || 'DARI'}</div>
        <div class="h1" id="${e.id}_f" style="font-size:230px"><span style="position:relative; display:inline-block">${e.from}<i id="${e.id}_s" style="position:absolute; left:-10px; right:-10px; top:48%; height:22px; background:var(--red); border-radius:11px; transform-origin:0 50%; transform:scaleX(0)"></i></span></div>
        <div id="${e.id}_u" style="font-size:56px; font-weight:600">${e.sub || 'sebulan'}</div>
        <div class="h1" id="${e.id}_t" style="font-size:250px; color:var(--yellow); text-shadow:0 10px 40px rgba(0,0,0,.4)">${e.to || ''}</div>
        <div id="${e.id}_b" style="margin-top:10px"><span class="pill" style="background:var(--yellow); color:var(--navy)">${e.badge || ''}</span></div></div>`; break;
    case 'delivery': h = `<div class="el" style="left:0; top:${e.top || 620}px; width:1080px; height:600px">
        <svg style="position:absolute; left:640px; top:20px" width="340" height="340" viewBox="0 0 340 340"><path d="M40 160 L170 50 L300 160" fill="none" stroke="#fff" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/><rect x="75" y="150" width="190" height="160" rx="16" fill="#fff"/><rect x="145" y="210" width="50" height="100" rx="8" fill="#0B4DA2"/></svg>
        <svg id="${e.id}_box" style="position:absolute; left:130px; top:100px" width="230" height="230" viewBox="0 0 64 64"><path d="M8 20 L32 8 L56 20 V46 L32 58 L8 46 Z" fill="#E8B27A" stroke="#8a5a2a" stroke-width="2.5" stroke-linejoin="round"/><path d="M8 20 L32 32 L56 20 M32 32 V58" fill="none" stroke="#8a5a2a" stroke-width="2.5"/></svg>
        <div id="${e.id}_m" style="position:absolute; left:0; width:1080px; top:420px; text-align:center; font-size:56px; font-weight:800; letter-spacing:6px"></div></div>`; break;
    case 'cta': h = `<div class="el c" style="${top}">${(e.ticks || []).map((s, k) => `<div id="${e.id}_k${k}" style="margin-bottom:22px"><span class="tick"><i>✓</i>${s}</span></div>`).join('')}
        <div id="${e.id}_btn" style="margin-top:50px"><span class="wa">${WA_SVG}${e.button || 'WhatsApp saya'}</span></div>
        <div id="${e.id}_fine" style="margin-top:40px; font-size:28px; color:${e.fineColor || 'rgba(255,255,255,.75)'}; padding:0 80px">${e.fine || '*Tertakluk pada terma &amp; promosi semasa Coway.'}</div></div>`; break;
  }
  add(h.replace('class="el', `id="${e.id}" class="el`));
});
add('<div class="el c" id="cap"><div id="capText"></div></div><div class="layer" id="flash" style="background:#fff; opacity:0"></div>');

/* ---------- lukis ---------- */
function lineupCam(e, t) {
  const K = e.keys;
  let i = K.length - 1; while (i > 0 && K[i].t > t) i--;
  const cur = K[i], prev = K[Math.max(0, i - 1)], k = i === 0 ? 1 : p(t, cur.t, cur.t + .4, E.inOut);
  const cx = mix(NEON_UNIT[prev.unit], NEON_UNIT[cur.unit], k), z = mix(prev.zoom || 1, cur.zoom || 1, k);
  const s = 1080 / 1464 * z, im = $(e.id + '_img');
  im.style.width = (1464 * s) + 'px'; im.style.left = (540 - cx * s) + 'px'; im.style.top = ((e.cy || 900) - 700 * s) + 'px';
  const named = cur.unit !== 'all' && k > .35 ? cur.unit : (prev.unit !== 'all' && k <= .35 ? prev.unit : null);
  if (named) { $(e.id + '_name').textContent = NEON_NAME[named][0]; $(e.id + '_dot').style.background = NEON_NAME[named][1]; }
  const on = t >= e.t0 && (e.t1 == null || t < e.t1);
  const lastN = Math.max(...K.filter(q => q.t <= t && q.unit !== 'all').map(q => q.t), -9);
  set(e.id + '_lab', { o: on && named ? 1 : 0, s: mix(.6, 1, p(t, lastN, lastN + .3, E.back)) });
}
function kid(id, t, t0, tout, sFrom = .4) {
  const a = p(t, t0, t0 + .35, E.back), b = tout == null ? 0 : p(t, tout, tout + .3, E.in);
  set(id, { o: Math.min(clamp(a * 2), 1 - b), s: mix(sFrom, 1, a) });
}
function drawEl(e, t) {
  const pop = ['title', 'banner', 'pill', 'reason', 'stamp', 'icon', 'counter'].includes(e.type);
  const opts = pop ? { pop: true, sFrom: e.type === 'stamp' ? 2.2 : .55, dy: 0 } : { dy: e.type === 'card' ? 120 : 60, dx: e.dx || 0 };
  if (e.type === 'lineup') { set(e.id, { o: t >= e.t0 && (e.t1 == null || t < e.t1) ? Math.min(p(t, e.t0, e.t0 + .3), 1 - (e.t1 ? p(t, e.t1 - .3, e.t1, E.in) : 0)) : 0 }); lineupCam(e, t); return; }
  inout(e.id, t, e.t0, e.t1 == null ? null : e.t1 - .3, opts);
  const out = e.t1 == null ? null : e.t1 - .3;
  switch (e.type) {
    case 'chips': case 'steps': case 'grid': case 'ticks': e.items.forEach((c, k) => kid(`${e.id}_${k}`, t, c.t, out, e.type === 'steps' ? .8 : .4)); break;
    case 'vs': [0, 1].forEach(k => kid(`${e.id}_${k}`, t, e[k ? 'right' : 'left'].t, out, .7)); break;
    case 'photo': {
      const a = p(t, e.t0, e.t0 + .6);
      const zk = e.zt0 != null ? p(t, e.zt0, e.zt1, E.inOut) : 0;
      $(e.id + '_img').style.transform = `scale(${mix(1, e.zs || 1, zk) * mix(1.08, 1, a)})`;
      if (e.float !== false && e.t1 == null || (e.float !== false && t < e.t1 - .3)) {
        const cur = $(e.id).style.transform; $(e.id).style.transform = cur + ` translateY(${Math.sin(t * 2) * 5}px)`;
      }
      break;
    }
    case 'quiz': {
      e.options.forEach((o, k) => {
        const a = p(t, o.t, o.t + .35, E.back), right = t >= e.answerT && e.answer.includes(k);
        set(`${e.id}_${k}`, { o: clamp(a * 2) * (t >= e.answerT && !right && e.dimOthers ? .45 : 1), s: mix(.6, 1, a) * (right ? 1 + .04 * p(t, e.answerT, e.answerT + .3, E.back) : 1), x: mix(-80, 0, a) });
      });
      break;
    }
    case 'counter': {
      const k = p(t, e.t0 + (e.delay || 0), e.t0 + (e.delay || 0) + (e.dur || 1), E.out);
      const v = mix(e.from, e.to, k);
      $(e.id + '_n').textContent = (e.prefix || '') + v.toFixed(e.decimals || 0) + (e.suffix || '');
      break;
    }
    case 'price': {
      const o = (id, tin) => kid(`${e.id}_${id}`, t, tin, out, .6);
      o('l', e.t0); o('f', e.t0 + .15); o('u', e.t0 + .4);
      o('b', e.badgeT != null ? e.badgeT : 1e9); o('t', e.toT != null ? e.toT : 1e9);
      $(e.id + '_s').style.transform = `scaleX(${e.strikeT != null ? p(t, e.strikeT, e.strikeT + .3, E.inOut) : 0})`;
      if (e.strikeT != null && t >= e.strikeT) { const k = p(t, e.strikeT, e.strikeT + .4, E.inOut); set(`${e.id}_f`, { s: mix(1, .55, k), o: mix(1, .8, k) }); set(`${e.id}_u`, { o: 1 - k }); }
      break;
    }
    case 'delivery': {
      const f = p(t, e.t0 + .4, e.t0 + 2.0, E.inOut);
      set(e.id + '_box', { o: 1 - p(t, e.t0 + 1.9, e.t0 + 2.1), x: f * 470, y: Math.sin(f * Math.PI) * -180, s: mix(1, .5, f) });
      const m = Math.max(0, Math.min(e.months || 8, Math.floor((t - e.t0 - .4) / 1.6 * (e.months || 8)) + 1));
      $(e.id + '_m').innerHTML = Array.from({ length: e.months || 8 }, (_, i) => `<span style="opacity:${i < m ? 1 : .25}">●</span>`).join(' ')
        + (m >= (e.months || 8) ? `<br><span style="font-size:44px">SETIAP ${e.months || 8} BULAN</span>` : '');
      break;
    }
    case 'cta': {
      (e.ticks || []).forEach((_, k) => inout(`${e.id}_k${k}`, t, e.t0 + .15 + k * .2, null, { dx: -80, dy: 0 }));
      inout(`${e.id}_btn`, t, e.btnT != null ? e.btnT : e.t0 + .8, null, { pop: true, sFrom: .5, dy: 0 });
      const bt = (e.btnT != null ? e.btnT : e.t0 + .8) + .7;
      if (t > bt) set(`${e.id}_btn`, { s: 1 + Math.max(0, Math.sin((t - bt) * 5)) * .05 });
      inout(`${e.id}_fine`, t, e.t0 + 1.0, null, { dy: 10 });
      break;
    }
  }
}

function seek(T) {
  const t = T - V.off;
  const sc = SP.scenes.find(s => t >= s.t0 && t < s.t1) || SP.scenes[SP.scenes.length - 1];
  const bg = sc.bg;
  let pending = Promise.resolve();
  const k = (t - sc.t0) / (sc.t1 - sc.t0);
  if (typeof bg === 'string') {
    $('bgColor').className = 'layer bg-' + bg; set('bgColor', { o: 1 }); set('bgImg', { o: 0 }); set('clipL', { o: 0 }); set('shade', { o: 0 });
  } else if (bg.clip) {
    set('bgColor', { o: 0 }); set('bgImg', { o: 0 });
    pending = Clips.show('clipImg', bg.clip, mix(bg.c0, bg.c1, clamp(k)) - SP.clips[bg.clip].start);
    set('clipL', { o: 1, s: mix(1.02, 1.07, k) }); set('shade', { o: bg.shade === false ? 0 : 1 });
  } else if (bg.image) {
    $('bgColor').className = 'layer bg-' + (bg.color || 'pastel'); set('bgColor', { o: 1 }); set('clipL', { o: 0 }); set('shade', { o: bg.shade ? 1 : 0 });
    if (!$img.src.endsWith(bg.image.replace('../../', ''))) { $img.src = bg.image; pending = $img.decode().catch(() => {}); }
    Object.assign($img.style, { left: (bg.left || 0) + 'px', top: (bg.top || 0) + 'px', width: (bg.w || 1080) + 'px', height: (bg.h || 1920) + 'px',
      objectFit: bg.fit || 'cover', webkitMaskImage: bg.mask ? 'linear-gradient(180deg, transparent 0, #000 12%, #000 88%, transparent 100%)' : '' });
    set('bgImg', { o: 1, s: mix(1.08, 1.0, k) });
  }
  set('flash', { o: SP.scenes.slice(1).some(s => t >= s.t0 && t < s.t0 + .2) ? (1 - (t - sc.t0) / .2) * .3 : 0 });
  SP.els.forEach(e => drawEl(e, t));
  caption(CH, t);
  return pending;
}
window.seek = seek;
