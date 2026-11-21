// Verset du jour : dessine l'image au temps t pour une page générée par verset/source/construire.py.
// S'appuie sur animation/moteur.js (personnage, décors animés). Déterministe : même t → même image.
const C = window.CONFIG;
const ST = $('st'), CV = $('cv'), CARTE = $('carte'), CTA = $('cta'), COM = $('com'), NOIR = $('noir');
const IDS = ['s1', 's2', 's3', 's4'];
const CLOCHE = '<svg viewBox="0 0 24 24" width="0.9em" height="0.9em" fill="currentColor"><path d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2z"/></svg>';
let segCourant = null, sousCourant = null, carteCourante = null;

// suites de blocs dans le même décor : le décor continue de vivre sans saut (soleil, nuages...)
C.segments.forEach((s, i) => {
  const p = C.segments[i - 1];
  s.r0 = p && p.decor === s.decor && !(C.intro && Math.abs(C.intro.t1 - s.t0) < 0.01) ? p.r0 : s.t0;
});
for (let i = C.segments.length - 1; i >= 0; i--) {
  const s = C.segments[i], n = C.segments[i + 1];
  s.r1 = n && n.r0 === s.r0 ? n.r1 : s.t1;
}

function segment(t) { for (const s of C.segments) if (t >= s.t0 && t < s.t1) return s; return C.segments[C.segments.length - 1]; }
const fondu = (t, a, b) => lisse((t - a) / 0.4) * (1 - lisse((t - (b - 0.4)) / 0.4));

function plan(s, t) {
  if (!s.coupes) return s.plan;
  let p = s.plan;
  for (const [tc, pc] of s.coupes) if (t >= tc) p = pc;
  return p;
}

function camera(s, t, d) {
  const u = t - s.t0, k = lisse(u / (s.t1 - s.t0)), pl = plan(s, t);
  let fx, fy, z;
  if (pl === 'serre') { fx = d.tete[0]; fy = d.tete[1] + (C.vertical ? 140 : 20); z = (C.vertical ? 1.24 : 1.55) + 0.035 * k; }
  else if (pl === 'fin') { [fx, fy] = d.foyer; z = 1; }
  else { [fx, fy] = C.vertical ? [d.tete[0], 640] : d.foyer; z = 1 + 0.045 * k; }
  set($('cam'), 'transform', `translate(${fx} ${fy}) scale(${z.toFixed(4)}) translate(${-fx} ${-fy})`);
}

function sousTitres(t, s) {
  let g = null;
  const masque = s.carte_verset || (C.vertical && s === C.segments[0]);   // accroche des Shorts : le gros titre sert de sous-titre
  if (!masque) for (const x of C.soustitres) if (t >= x.t0 && t < x.t1) { g = x; break; }
  if (g !== sousCourant) {
    ST.innerHTML = g ? (C.vertical ? g.mots.map(m => `<span class="m">${m.txt}</span>`).join(' ')
      : `<span style="background:rgba(0,0,0,.58);padding:6px 18px;border-radius:12px;box-decoration-break:clone;-webkit-box-decoration-break:clone">${g.mots.map(m => `<span class="m">${m.txt}</span>`).join(' ')}</span>`) : '';
    sousCourant = g;
  }
  if (!g) return;
  const spans = ST.querySelectorAll('span.m');
  g.mots.forEach((m, i) => {
    const actif = t >= m.t0 - 0.03 && t < Math.max(m.t1, m.t0 + 0.12);
    spans[i].style.color = actif ? (C.vertical ? '#FFD36A' : '#FFB46A') : (C.vertical || t >= m.t0 ? '#fff' : 'rgba(255,255,255,.72)');
    if (C.vertical) spans[i].style.transform = actif ? 'scale(1.08)' : 'none';
  });
  ST.style.paddingRight = s.fin ? '900px' : '';
}

function carteVerset(s, t) {
  const a = s.carte_verset ? fondu(t, s.t0, s.t1) : 0;
  CV.style.opacity = a;
  CV.style.transform = `translateY(${((1 - a) * 30).toFixed(1)}px)`;
  const voile = $('voile'); if (voile) voile.style.opacity = a;
  if (!s.carte_verset) return;
  if (CV._seg !== s) { CV.querySelector('.v').innerHTML = s.mots.map(m => `<span>${m.txt}</span>`).join(' '); CV._seg = s; }
  CV.querySelectorAll('.v span').forEach((sp, i) => sp.classList.toggle('on', t >= s.mots[i].t0 - 0.05));
}

function cartes(t) {
  let c = null;
  for (const x of C.cartes) if (t >= x.t0 && t < x.t1) { c = x; break; }
  if (c !== carteCourante) {
    const g = C.vertical ? 1.15 : 1;
    CARTE.innerHTML = !c ? '' : c.type === 'mot'
      ? `<div class="ref" style="font-size:${20 * g}px">Le mot hébreu</div>
         <div style="font-family:'DejaVu Sans',sans-serif;font-size:${92 * g}px;line-height:1.3;margin:14px 0 4px;direction:rtl">${c.hebreu}</div>
         <div class="serif" style="font-size:${50 * g}px;color:#FFB46A">${c.translit}</div>
         <div class="src" style="font-size:${26 * g}px;margin-top:14px;line-height:1.35">${c.sens}</div>`
      : `<div class="serif" style="font-size:${40 * g}px;line-height:1.25">${c.texte}</div>
         <div class="ref" style="font-size:${20 * g}px;margin-top:22px">${c.source}</div>`;
    carteCourante = c;
  }
  const a = c ? fondu(t, c.t0, c.t1) : 0;
  CARTE.style.opacity = a;
  CARTE.style.transform = `scale(${(0.95 + 0.05 * a).toFixed(3)})`;
}

function chapitre(s, t) {
  const el = $('chap'); if (!el) return;
  const a = s.chapitre ? lisse((t - s.t0 - 0.3) / 0.4) * (1 - lisse((t - s.t0 - 3.6) / 0.4)) : 0;
  el.style.opacity = a;
  el.style.transform = `translateX(${(-30 * (1 - a)).toFixed(1)}px)`;
  if (s.chapitre && el._seg !== s) {
    el.querySelector('.n').textContent = `CHAPITRE ${s.chapitre_n} / ${s.chapitres}`;
    el.querySelector('.t').textContent = s.chapitre; el._seg = s;
  }
}

function appel(s, t) {
  const u = t - s.t0, dur = s.t1 - s.t0;
  const a = s.cta ? lisse((u - 0.2) / 0.35) * (1 - lisse((u - (dur - 0.5)) / 0.4)) : 0;
  CTA.style.opacity = a;
  if (s.cta) {
    const clic = u > 1.7, bump = Math.exp(-Math.pow((u - 1.7) / 0.12, 2));
    const yt = s.cta === 'youtube';
    const etat = (yt ? 'y' : 't') + (clic ? '1' : '0');
    if (CTA._etat !== etat) {
      CTA.innerHTML = `<div class="sur">Un verset par jour</div><span class="bouton ${clic ? 'fait' : (yt ? 'youtube' : 'tiktok')}">`
        + (yt ? `<span class="cloche">${CLOCHE}</span>${clic ? 'ABONNÉ ✓' : "S'ABONNER"}` : (clic ? '✓ SUIVI' : '+ SUIS-NOUS')) + '</span>';
      CTA._etat = etat;
    }
    CTA.style.transform = `translateY(${((1 - a) * 40).toFixed(1)}px) scale(${(1 + 0.08 * bump).toFixed(3)})`;
    const cl = CTA.querySelector('.cloche');
    if (cl) cl.style.transform = clic ? `rotate(${(18 * Math.sin((u - 1.7) * 18) * Math.exp(-(u - 1.7) * 2.2)).toFixed(1)}deg)` : 'none';
  }
  const b = s.commentaire ? lisse((u - dur * 0.42) / 0.35) * (1 - lisse((u - (dur - 0.5)) / 0.4)) : 0;
  COM.style.opacity = b;
  if (s.commentaire) {
    COM.innerHTML = `Écris en commentaire :<br><span style="color:#C0522B">« ${s.commentaire} »</span>`;
    COM.style.transform = `translateY(${((1 - b) * 24).toFixed(1)}px)`;
  }
}

function habillage(s, t) {
  if (C.vertical) {
    $('barre').style.width = (100 * t / C.dur).toFixed(2) + '%';
    const s0 = C.segments[0];
    const acc = s === s0 ? lisse((t - 0.05) / 0.25) * (1 - lisse((t - (s0.t1 - 0.25)) / 0.25)) : 0;
    const el = $('acc'); el.style.opacity = acc; el.style.transform = `scale(${(0.9 + 0.1 * lisse(t / 0.3)).toFixed(3)})`;
    $('puce').style.opacity = s === s0 || s.carte_verset ? 0 : 1;
  } else {
    const f = $('fin'); f.style.opacity = s.fin ? lisse((t - s.t0 - 0.3) / 0.6) : 0;
  }
}

function noir(s, t) {
  const i = C.segments.indexOf(s), p = C.segments[i - 1], n = C.segments[i + 1];
  let v = 0;
  const apresIntro = C.intro && Math.abs(C.intro.t1 - s.t0) < 0.01, avantIntro = C.intro && Math.abs(C.intro.t0 - s.t1) < 0.01;
  if ((p && p.decor !== s.decor) || apresIntro) v = Math.max(v, 1 - lisse((t - s.t0) / 0.25));
  if ((n && n.decor !== s.decor) || avantIntro) v = Math.max(v, lisse((t - (s.t1 - 0.22)) / 0.22));
  if (!n && !C.vertical) v = Math.max(v, lisse((t - (s.t1 - 0.8)) / 0.8));   // la vidéo longue finit au noir ; les Shorts bouclent
  NOIR.style.opacity = v.toFixed(3);
}

window.seek = function (t) {
  if (C.intro && t >= C.intro.t0 && t < C.intro.t1) { NOIR.style.opacity = 1; return; }
  const s = segment(t), d = C.decors[s.decor];
  if (s.decor !== (segCourant && segCourant.decor)) {
    for (const id of IDS) { set($(id + '_fond'), 'display', id === s.decor ? 'inline' : 'none'); set($(id + '_devant'), 'display', id === s.decor ? 'inline' : 'none'); }
    set($('perso_pos'), 'transform', `translate(${d.tx} ${d.ty}) scale(${d.s})`);
    set($('perso_lum'), 'filter', `url(#f_${s.decor})`);
    if (C.vertical) set($('s'), 'viewBox', `${d.tete[0] - 304} 0 608 1080`);
  }
  segCourant = s;
  camera(s, t, d);
  personnage(C.piste, t, t);
  ANIM[s.decor](t - s.r0 + 0.5, t, s.r1 - s.r0);
  sousTitres(t, s); carteVerset(s, t); cartes(t); chapitre(s, t); appel(s, t); habillage(s, t); noir(s, t);
};

window.ready = document.fonts.ready.then(() => {
  setupDecors();
  if (!C.piste.syl) C.piste.syl = [];
  window.seek(0.5);
});

// ---------------------------------------------------------------- fond musical provisoire (remplacé par musique.mp3 si présent)
// Nappe de piano feutré et de cordes douces en ré majeur, ~68 BPM ; silence pendant l'intro (elle a son propre son).
window.renderAudio = async function () {
  const D = C.dur, sr = 48000, ac = new OfflineAudioContext(2, Math.ceil(D * sr), sr);
  const master = ac.createGain(); master.gain.value = 0.5; master.connect(ac.destination);
  const conv = ac.createConvolver(), ir = ac.createBuffer(2, sr * 3, sr);
  for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = (rnd(i * 5 + c) * 2 - 1) * Math.pow(1 - i / d.length, 2.2); }
  conv.buffer = ir; const wet = ac.createGain(); wet.gain.value = 0.45; conv.connect(wet); wet.connect(master);
  const bus = ac.createGain(); bus.connect(master); bus.connect(conv);
  // enveloppe générale : entrée, coupure pendant l'intro, sortie
  bus.gain.setValueAtTime(0, 0); bus.gain.linearRampToValueAtTime(1, 1.5);
  if (C.intro) { bus.gain.setValueAtTime(1, C.intro.t0 - 0.3); bus.gain.linearRampToValueAtTime(0, C.intro.t0); bus.gain.setValueAtTime(0, C.intro.t1); bus.gain.linearRampToValueAtTime(1, C.intro.t1 + 1.2); }
  bus.gain.setValueAtTime(1, Math.max(0, D - 2)); bus.gain.linearRampToValueAtTime(0, D);
  const accords = [[146.83, 220, 293.66, 369.99], [138.59, 220, 277.18, 329.63], [123.47, 246.94, 293.66, 369.99], [98, 246.94, 293.66, 392]]; // ré, la/do#, si m, sol
  const mesure = 60 / 68 * 4, tour = mesure * 2;
  for (let t0 = 0, k = 0; t0 < D; t0 += tour, k++) {
    const ac_ = accords[k % 4];
    ac_.forEach((f, i) => [-6, 6].forEach(dt => {
      const o = ac.createOscillator(); o.type = i === 0 ? 'sine' : 'triangle'; o.frequency.value = f; o.detune.value = dt;
      const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 900; const g = ac.createGain();
      g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(0.018, t0 + 1.6); g.gain.setValueAtTime(0.018, t0 + tour - 1.2); g.gain.linearRampToValueAtTime(0, t0 + tour + 0.4);
      o.connect(lp); lp.connect(g); g.connect(bus); o.start(t0); o.stop(Math.min(D, t0 + tour + 0.5));
    }));
    // piano feutré : quelques notes de l'accord, une octave au-dessus
    for (let j = 0; j < 6; j++) {
      if (rnd(k * 31 + j) < 0.3) continue;
      const tn = t0 + j * (tour / 6) + rnd(k * 7 + j) * 0.08, f = ac_[1 + Math.floor(rnd(k * 13 + j) * 3)] * 2;
      if (tn >= D) break;
      [1, 2, 3].forEach((h, q) => { const o = ac.createOscillator(); o.frequency.value = f * h; const g = ac.createGain();
        g.gain.setValueAtTime(0, tn); g.gain.linearRampToValueAtTime(0.05 / (q * 2 + 1), tn + 0.012); g.gain.exponentialRampToValueAtTime(0.0003, tn + 2.8);
        const lp = ac.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 2200; o.connect(lp); lp.connect(g); g.connect(bus); o.start(tn); o.stop(Math.min(D, tn + 2.9)); });
    }
  }
  const buf = await ac.startRendering();
  let pk = 0; for (let c = 0; c < 2; c++) for (const v of buf.getChannelData(c)) pk = Math.max(pk, Math.abs(v));
  const k = 0.7 / pk, Lc = buf.getChannelData(0), Rc = buf.getChannelData(1), n = Lc.length, ab = new ArrayBuffer(44 + n * 4), dv = new DataView(ab);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
  ws(0, 'RIFF'); dv.setUint32(4, 36 + n * 4, true); ws(8, 'WAVE'); ws(12, 'fmt '); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 2, true);
  dv.setUint32(24, sr, true); dv.setUint32(28, sr * 4, true); dv.setUint16(32, 4, true); dv.setUint16(34, 16, true); ws(36, 'data'); dv.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { dv.setInt16(44 + i * 4, cl(Lc[i] * k, -1, 1) * 32767, true); dv.setInt16(46 + i * 4, cl(Rc[i] * k, -1, 1) * 32767, true); }
  let s = ''; const u8 = new Uint8Array(ab); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768)); return btoa(s);
};
