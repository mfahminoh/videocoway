/* Templat siri video model (pecahan spek). Setiap m*.html tetapkan window.M lalu muatkan fail ini.
   M.scenes = 7 babak ikut baris VO dalam voiceover/jerebu/skrip.json:
     story   { photo, lines[] }                 — cerita kesesuaian atas foto B-roll
     reveal  { kick, chips[] }                  — produk + nama + kod
     filters { title, from, items[{k,name,desc,life}] } — pecahan penapis (k = jenis swatch, lihat model.css)
     sides   { items[] }                        — penapis dua sisi (Atrium)
     tiles   { title, tiles[[nilai, label]] }   — kelebihan / spek dalam jubin
     feature { big, sub, bullets[], art }       — satu kelebihan utama (art: haze | 360 | display)
     fit     { photo, chips[] }                 — sesuai untuk
     cta     { price, fine }                                                                       */
(function () {
  const M = window.M, IMG = '../../assets/img/air/', w = s => document.write(s);
  const pct = (i, n, a = 12, b = 88) => `${Math.round(a + (b - a) * i / Math.max(1, n - 1))}%`;
  w(`<img class="logo" src="${IMG}coway-logo.png" id="cwlogo">`);

  const R = {
    story: d => `<div class="scene onph">${K.photo(d.photo, { pos: d.pos || '50% 50%' })}
      <div class="el" style="left:0; bottom:180px; width:1080px; padding:0 60px">
      ${d.lines.map((l, i) => `<div class="h" style="display:block !important; text-align:center; margin-top:${i ? 24 : 0}px; font-size:${i ? 60 : 76}px; line-height:1.1" data-in="${pct(i, d.lines.length, 0, 60)}" data-a="up">${l}</div>`).join('')}</div></div>`,

    reveal: d => `<div class="scene">
      <div class="el c" style="top:190px" data-in="0" data-a="pop"><span class="kick">${d.kick}</span></div>
      <img class="el" src="${IMG}${M.img}" style="top:300px; left:${540 - M.w / 2}px; width:${M.w}px; height:${M.w * 740 / 450}px; filter:drop-shadow(0 40px 40px rgba(20,40,60,.25))" data-in="5%" data-a="zoom">
      <div class="el c h" style="top:${330 + M.w * 740 / 450}px; font-size:118px; line-height:1" data-in="15%" data-a="slam">${M.name}</div>
      <div class="el c code" style="top:${470 + M.w * 740 / 450}px" data-in="25%" data-a="fade">COWAY · ${M.code}</div>
      <div class="el" style="top:${540 + M.w * 740 / 450}px; left:0; width:1080px; display:flex !important; justify-content:center; gap:16px; flex-wrap:wrap; padding:0 60px" data-in="55%" data-a="pop">${d.chips.map(c => `<span class="chipb">${c}</span>`).join('')}</div></div>`,

    filters: d => `<div class="scene">
      <div class="el c" style="top:180px" data-in="0" data-a="pop"><span class="kick">${d.title}</span></div>
      ${d.note ? `<div class="el c" style="top:270px; font-size:34px; color:var(--ink)" data-in="5%" data-a="fade">${d.note}</div>` : ''}
      ${d.items.map((f, i) => `<div class="el frow" style="top:${360 + i * gap(d)}px; left:70px" data-in="${pct(i, d.items.length, 6, 80)}" data-a="left">
        <div class="sw k-${f.k}"><b>${f.n || String((d.from || 1) + i).padStart(2, '0')}</b></div>
        <div><div class="fn">${f.name}</div><div class="fd">${f.desc}</div>${f.life ? `<span class="fl">${f.life}</span>` : ''}</div></div>`).join('')}
      ${d.items.length <= 3 ? prodLow(360 + d.items.length * gap(d) + 20, .55, '70%') : ''}</div>`,

    sides: d => `<div class="scene">
      <div class="el c" style="top:180px" data-in="0" data-a="pop"><span class="kick">${d.title}</span></div>
      <img class="el" src="${IMG}${M.img}" style="top:330px; left:390px; width:300px; height:493px" data-in="0" data-a="zoom">
      ${['SISI A', 'SISI B'].map((sd, j) => `<div class="el" style="top:330px; left:${j ? 720 : 70}px; width:290px; text-align:center" data-in="${j ? '30%' : '15%'}" data-a="${j ? 'left' : 'right'}">
        <div class="h" style="font-size:40px; color:var(--blue)">${sd}</div>
        ${d.items.map(f => `<div class="sw k-${f.k}" style="margin:18px auto 0; width:120px; height:120px"></div><div style="font-family:CW; font-weight:800; font-size:30px; margin-top:6px">${f.name}</div>`).join('')}</div>`).join('')}
      <div class="el c h" style="top:1120px; font-size:72px; line-height:1.1" data-in="45%" data-a="slam">2 motor · sedut 2 sisi</div>
      <div class="el c" style="top:1230px; font-size:40px; color:var(--ink)" data-in="60%" data-a="up">${d.sub}</div></div>`,

    tiles: d => `<div class="scene">
      <div class="el c" style="top:180px" data-in="0" data-a="pop"><span class="kick">${d.title}</span></div>
      ${d.tiles.map((t, i) => `<div class="el tile" style="top:${330 + Math.floor(i / 2) * 290}px; left:${i % 2 ? 560 : 70}px" data-in="${pct(i, d.tiles.length, 5, 82)}" data-a="pop"><div class="v">${t[0]}</div><div class="l">${t[1]}</div></div>`).join('')}
      ${prodLow(330 + Math.ceil(d.tiles.length / 2) * 290 + 30, .62, '40%')}</div>`,

    feature: d => `<div class="scene">
      <div class="el c" style="top:180px" data-in="0" data-a="pop"><span class="kick">${d.kick}</span></div>
      <img class="el" id="ftImg" src="${IMG}${M.img}" style="top:430px; left:${540 - M.w * .8 / 2}px; width:${M.w * .8}px; height:${M.w * .8 * 740 / 450}px; filter:drop-shadow(0 30px 30px rgba(20,40,60,.2))" data-in="0" data-a="zoom">
      ${art(d.art)}
      <div class="el c h fit" style="top:${480 + M.w * .8 * 740 / 450}px; font-size:110px; line-height:1; color:var(--blue); white-space:nowrap" data-in="20%" data-a="slam">${d.big}</div>
      ${d.bullets.map((b, i) => `<div class="el c" style="top:${620 + M.w * .8 * 740 / 450 + i * 70}px; font-size:42px; font-weight:700; color:var(--dark)" data-in="${pct(i, d.bullets.length, 40, 85)}" data-a="up">${b}</div>`).join('')}</div>`,

    fit: d => `<div class="scene onph">${K.photo(d.photo, { pos: d.pos || '50% 50%' })}
      <div class="el c" style="top:1330px" data-in="0" data-a="pop"><span class="kick">SESUAI UNTUK</span></div>
      <div class="el" style="top:1430px; left:0; width:1080px; display:flex !important; justify-content:center; gap:16px; flex-wrap:wrap; padding:0 50px" data-in="20%" data-a="pop">${d.chips.map(c => `<span class="chipb" style="font-size:40px">${c}</span>`).join('')}</div></div>`,

    cta: d => K.cta({ imgs: [M.img], h1: d.h1, fine: d.fine, stampAt: '50%' }),
  };

  function gap(d) { return Math.min(330, Math.floor((1560 - 360) / d.items.length)); }
  /* produk kecil di ruang kosong bawah (hingga 1780px) */
  function prodLow(top, k, at) {
    const h = Math.min(1780 - top, M.w * k * 740 / 450), wd = h * 450 / 740;
    return h < 260 ? '' : `<img class="el" src="${IMG}${M.img}" style="top:${top}px; left:${540 - wd / 2}px; width:${wd}px; height:${h}px; filter:drop-shadow(0 30px 30px rgba(20,40,60,.2))" data-in="${at}" data-a="zoom">`;
  }
  function art(kind) {
    const cx = 540, top = 430, hgt = M.w * .8 * 740 / 450;
    if (kind === 'haze') return `<svg class="el" style="top:${top - 120}px; left:${cx - 300}px" width="600" height="${hgt * .6}" viewBox="0 0 600 400" data-in="35%" data-a="fade">
      <g stroke="#00A4E4" stroke-width="16" fill="none" stroke-linecap="round" stroke-linejoin="round">
      <path d="M300 230 V40 M265 75 L300 40 L335 75"/><path d="M200 260 L50 160 M60 205 L50 160 L95 150"/><path d="M400 260 L550 160 M540 205 L550 160 L505 150"/></g></svg>
      <div class="el" style="top:${top + 40}px; left:60px" data-in="45%" data-a="pop"><span class="chipb">lebar</span></div>
      <div class="el" style="top:${top - 110}px; left:${cx + 60}px" data-in="50%" data-a="pop"><span class="chipb">atas</span></div>
      <div class="el" style="top:${top + 40}px; left:820px" data-in="55%" data-a="pop"><span class="chipb">depan</span></div>`;
    if (kind === '360') return `<div class="el" id="ring360" style="top:${top + hgt * .35}px; left:${cx - 330}px; width:660px; height:180px; border-radius:50%; border:10px dashed rgba(0,164,228,.6)" data-in="30%" data-a="fade"></div>`;
    if (kind === 'display') return `<div class="el" style="top:${top + 40}px; left:700px; width:320px; padding:24px; border-radius:28px; background:#1f2a33; color:#fff; text-align:center; box-shadow:0 20px 40px rgba(0,0,0,.25)" data-in="30%" data-a="pop">
      <div style="font-family:CW; font-weight:800; font-size:30px; color:#7fd3f5">PM2.5</div><div style="font-family:CW; font-weight:900; font-size:96px; line-height:1"><span data-count="58,12,1.6,3.2">58</span></div><div style="font-size:24px; opacity:.7">µg/m³ · ilustrasi</div></div>`;
    return '';
  }

  M.scenes.forEach(sc => w(R[sc.type](sc)));
  w(`<canvas class="layer" id="fx" width="1080" height="1920"></canvas>`);
})();

window.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('fx').getContext('2d');
  K.start(t => {
    K.clear(ctx);
    // logo hanya pada babak berlatar cerah
    const sc = [...document.querySelectorAll('.scene')].find(s => t >= +s.dataset.s && t < +s.dataset.e);
    document.getElementById('cwlogo').style.opacity = sc && !sc.classList.contains('onph') && !sc.classList.contains('cta') ? 1 : 0;
    const r = document.getElementById('ring360');
    if (r) r.style.transform += ` rotate(${t * 20}deg)`;
    const s0 = K.scene(0);
    if (t < s0.e + .3 && M.haze) K.haze(ctx, t, { n: 160, color: '200,180,150', alpha: .3, size: 4, speed: 20 });
  });
});
