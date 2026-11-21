// Démo : le présentateur dans les 4 décors (5 s chacun). Le moteur est dans moteur.js.
const C = window.CONFIG;

// ---------------------------------------------------------------- montage
let courante = -1;
window.seek = function (t) {
  const n = C.scenes.length, i = Math.min(n - 1, Math.floor(t / C.scene)), u = t - i * C.scene, sc = C.scenes[i];
  if (i !== courante) {
    C.scenes.forEach((s, k) => { set($(s.id + '_fond'), 'display', k === i ? 'inline' : 'none'); set($(s.id + '_devant'), 'display', k === i ? 'inline' : 'none'); });
    set($('perso_pos'), 'transform', `translate(${sc.tx} ${sc.ty}) scale(${sc.s})`);
    set($('perso_lum'), 'filter', `url(#f_${sc.id})`);
    $('lab_n').textContent = `DÉCOR ${i + 1} / ${n}`; $('lab_t').textContent = sc.titre; $('lab_s').textContent = sc.sous;
    const w = Math.max($('lab_t').getComputedTextLength(), $('lab_s').getComputedTextLength(), $('lab_n').getComputedTextLength());
    set($('lab_fond'), 'width', (w + 56).toFixed(0));
    courante = i;
  }
  // caméra : lente avancée vers le personnage
  const [fx, fy] = sc.foyer, z = 1 + 0.045 * lisse(u / C.scene);
  set($('cam'), 'transform', `translate(${fx} ${fy}) scale(${z.toFixed(4)}) translate(${-fx} ${-fy})`);
  personnage(sc, u, t);
  ANIM[sc.id](u, t, C.scene);
  // étiquette du décor
  const e = lisse((u - 0.35) / 0.4) * (1 - lisse((u - 4.25) / 0.35));
  set($('etiquette'), 'opacity', e.toFixed(3));
  set($('etiquette'), 'transform', `translate(${(56 - 24 * (1 - e)).toFixed(1)} 56)`);
  // passage au noir entre les décors
  const noir = Math.max(1 - lisse(u / 0.3), lisse((u - (C.scene - 0.3)) / 0.3));
  set($('noir'), 'opacity', noir.toFixed(3));
};
window.ready = document.fonts.ready.then(() => {
  setupDecors();
  C.scenes.forEach((sc, si) => { sc.syl = syllabes(sc.paroles, si * 100); });
  window.seek(0.5);
});

// ---------------------------------------------------------------- ambiance sonore (rendue hors ligne)
window.renderAudio = async function () {
  const D = C.dur, S = C.scene, sr = 48000, ac = new OfflineAudioContext(2, Math.ceil(D * sr), sr);
  const master = ac.createGain(); master.gain.value = 0.6; master.connect(ac.destination);
  const conv = ac.createConvolver(), ir = ac.createBuffer(2, sr * 2.5, sr);
  for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let i = 0; i < d.length; i++) d[i] = (rnd(i * 7 + c) * 2 - 1) * Math.pow(1 - i / d.length, 2.5); }
  conv.buffer = ir; const wet = ac.createGain(); wet.gain.value = 0.3; conv.connect(wet); wet.connect(master);
  const blanc = (sec, g = 1) => { const b = ac.createBuffer(1, Math.ceil(sr * sec), sr), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = rnd(i * 3.1 + g) * 2 - 1; return b; };
  const brun = (sec) => { const b = ac.createBuffer(1, Math.ceil(sr * sec), sr), d = b.getChannelData(0); let l = 0; for (let i = 0; i < d.length; i++) { l = (l + 0.02 * (rnd(i * 1.7) * 2 - 1)) / 1.02; d[i] = l * 3.5; } return b; };
  // un bus par décor, avec fondu d'entrée et de sortie calé sur les passages au noir
  const bus = (k, rev = 0) => {
    const g = ac.createGain(), a = k * S, b = (k + 1) * S;
    g.gain.setValueAtTime(0, 0); g.gain.setValueAtTime(0, a + 0.001); g.gain.linearRampToValueAtTime(1, a + 0.35);
    g.gain.setValueAtTime(1, b - 0.35); g.gain.linearRampToValueAtTime(0, b);
    g.connect(master); if (rev) { const r = ac.createGain(); r.gain.value = rev; g.connect(r); r.connect(conv); }
    return g;
  };
  const source = (buf, t0, t1, ...chaine) => { const s = ac.createBufferSource(); s.buffer = buf; let n = s; for (const c of chaine) { n.connect(c); n = c; } s.start(t0); s.stop(t1); return n; };
  const filtre = (type, f, q = 0.7) => { const x = ac.createBiquadFilter(); x.type = type; x.frequency.value = f; x.Q.value = q; return x; };
  const gain = (v) => { const g = ac.createGain(); g.gain.value = v; return g; };
  const tic = (out, t, f, a, dec) => { const s = ac.createBufferSource(); s.buffer = blanc(0.08, t * 1000); const bp = filtre('bandpass', f, 1.2), g = ac.createGain();
    g.gain.setValueAtTime(a, t); g.gain.exponentialRampToValueAtTime(0.0005, t + dec); s.connect(bp); bp.connect(g); g.connect(out); s.start(t); s.stop(t + 0.08); };
  const nappe = (out, notes, t0, t1, a, type = 'triangle', fc = 1200) => notes.forEach((f, i) => [-4, 4].forEach(dt => {
    const o = ac.createOscillator(); o.type = type; o.frequency.value = f; o.detune.value = dt; const lp = filtre('lowpass', fc, 0.5), g = ac.createGain();
    g.gain.setValueAtTime(0, t0); g.gain.linearRampToValueAtTime(a, t0 + 1.2); o.connect(lp); lp.connect(g); g.connect(out); o.start(t0); o.stop(t1); }));
  // 1. feu de camp : grondement, souffle, crépitements
  { const o = bus(0, 0.1); source(brun(S), 0, S, filtre('lowpass', 380), gain(0.36)).connect(o); source(blanc(S, 1), 0, S, filtre('bandpass', 2600, 0.6), gain(0.025)).connect(o);
    for (let k = 0; k < 75; k++) tic(o, rnd(k + 0.3) * S, 1200 + rnd(k + 9) * 4800, 0.03 + Math.pow(rnd(k + 4), 3) * 0.2, 0.008 + rnd(k + 6) * 0.03); }
  // 2. chapelle : nappe douce et résonance
  { const o = bus(1, 0.8), a = S; nappe(o, [146.83, 220, 293.66, 369.99, 659.25], a, a + S, 0.022, 'sine', 1400);
    source(brun(S), a, a + S, filtre('lowpass', 180), gain(0.18)).connect(o);
    [[a + 0.5, 587.33], [a + 2.6, 880]].forEach(([t, f]) => [1, 2.01, 3.02].forEach((h, k) => { const os = ac.createOscillator(); os.frequency.value = f * h; const g = ac.createGain();
      g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.03 / (k + 1), t + 0.01); g.gain.exponentialRampToValueAtTime(0.0003, t + 2.5); os.connect(g); g.connect(o); os.start(t); os.stop(t + 2.6); })); }
  // 3. sommet : vent, nappe claire, oiseaux
  { const o = bus(2, 0.3), a = 2 * S, bp = filtre('bandpass', 500, 0.8), g = gain(0);
    source(blanc(S, 2), a, a + S, bp, g).connect(o);
    [[0, 380, 0.2], [1.2, 900, 0.36], [2.4, 520, 0.24], [3.5, 1100, 0.4], [5, 450, 0.2]].forEach(([t, f, v]) => { bp.frequency.linearRampToValueAtTime(f, a + t); g.gain.linearRampToValueAtTime(v, a + t); });
    nappe(o, [293.66, 440, 659.25, 739.99], a, a + S, 0.018, 'sine', 2400);
    [1.2, 1.38, 3.1, 3.3, 3.45].forEach((t, k) => { const os = ac.createOscillator(), gg = ac.createGain(), t0 = a + t; os.frequency.setValueAtTime(2900 + k * 150, t0); os.frequency.exponentialRampToValueAtTime(3900, t0 + 0.07);
      gg.gain.setValueAtTime(0, t0); gg.gain.linearRampToValueAtTime(0.03, t0 + 0.01); gg.gain.exponentialRampToValueAtTime(0.0005, t0 + 0.09); os.connect(gg); gg.connect(o); os.start(t0); os.stop(t0 + 0.1); }); }
  // 4. chambre : pluie sur la vitre, gouttes, nappe grave
  { const o = bus(3, 0.15), a = 3 * S; source(blanc(S, 3), a, a + S, filtre('highpass', 1300), filtre('lowpass', 7000), gain(0.11)).connect(o);
    source(brun(S), a, a + S, filtre('lowpass', 500), gain(0.16)).connect(o);
    for (let k = 0; k < 60; k++) tic(o, a + rnd(k + 50) * S, 3500 + rnd(k + 70) * 3500, 0.02 + rnd(k + 90) * 0.05, 0.006 + rnd(k + 40) * 0.01);
    nappe(o, [146.83, 185, 220], a, a + S, 0.014, 'sine', 700); }
  const buf = await ac.startRendering();
  let pk = 0; for (let c = 0; c < 2; c++) for (const v of buf.getChannelData(c)) pk = Math.max(pk, Math.abs(v));
  const k = 0.89 / pk, Lc = buf.getChannelData(0), Rc = buf.getChannelData(1), n = Lc.length, ab = new ArrayBuffer(44 + n * 4), dv = new DataView(ab);
  const ws = (o, s) => { for (let i = 0; i < s.length; i++) dv.setUint8(o + i, s.charCodeAt(i)); };
  ws(0, 'RIFF'); dv.setUint32(4, 36 + n * 4, true); ws(8, 'WAVE'); ws(12, 'fmt '); dv.setUint32(16, 16, true); dv.setUint16(20, 1, true); dv.setUint16(22, 2, true);
  dv.setUint32(24, sr, true); dv.setUint32(28, sr * 4, true); dv.setUint16(32, 4, true); dv.setUint16(34, 16, true); ws(36, 'data'); dv.setUint32(40, n * 4, true);
  for (let i = 0; i < n; i++) { dv.setInt16(44 + i * 4, cl(Lc[i] * k, -1, 1) * 32767, true); dv.setInt16(46 + i * 4, cl(Rc[i] * k, -1, 1) * 32767, true); }
  let s = ''; const u8 = new Uint8Array(ab); for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768)); return btoa(s);
};
