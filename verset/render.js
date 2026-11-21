// Rendu d'un épisode « verset du jour ».
//   python3 verset/source/construire.py verset/episodes/<épisode>        (à refaire après chaque changement de texte ou de voix)
//   node verset/render.js verset/episodes/<épisode>                      → les 3 vidéos + miniature + couverture
//   node verset/render.js <épisode> --format long|short_youtube|short_tiktok
//   node verset/render.js <épisode> --format long --stills 3,40,120      → images de contrôle
//   node verset/render.js <épisode> --images                             → miniature et couverture seulement
// Son : voix ElevenLabs (voix/*.mp3) traitées « micro podcast » + musique (musique.mp3 si présent, sinon nappe provisoire)
// baissée automatiquement sous la voix, puis normalisation -14 LUFS (YouTube, TikTok).
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");

const args = process.argv.slice(2);
const EP = path.resolve(args.find(a => !a.startsWith("--") && !/^[\d.,]+$/.test(a)) || path.join(__dirname, "episodes/psaume-23-4"));
const opt = (k) => (args.includes(k) ? args[args.indexOf(k) + 1] : null);
const FORMATS = opt("--format") ? [opt("--format")] : ["short_youtube", "short_tiktok", "long"];
const ID = path.basename(EP), FPS = 30, WORKERS = 4;
const OUT = path.join(EP, "rendu"), TMP = path.join(EP, "renders");
const NOMS = { long: `${ID}_youtube_long.mp4`, short_youtube: `${ID}_youtube_short.mp4`, short_tiktok: `${ID}_tiktok.mp4` };
const INTRO = path.join(__dirname, "..", "youtube", "intro_1920x1080.mp4");
const ff = (a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });

// chaîne « micro podcast » : coupe des graves inutiles, chaleur de proximité, moins de « carton », présence, dé-essage, compression douce, limiteur
const PODCAST = "highpass=f=75,equalizer=f=120:t=q:w=0.9:g=2,equalizer=f=350:t=q:w=1.2:g=-2.5,equalizer=f=3500:t=q:w=1:g=2.5," +
  "deesser=i=0.4,acompressor=threshold=0.1:ratio=3:attack=8:release=120:makeup=2:knee=3,alimiter=limit=0.89";

async function ouvrir(browser, fichier, w, h) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.log("[erreur page]", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.log("[console]", m.text()); });
  await page.goto("file://" + fichier);
  await page.evaluate(() => window.ready);
  return page;
}
const cliché = async (page, t, file, sel = "#stage") => { await page.evaluate((tt) => window.seek(tt), t); await page.locator(sel).screenshot({ path: file, type: "jpeg", quality: 92 }); };

async function images(browser) {
  fs.mkdirSync(OUT, { recursive: true });
  for (const [nom, w, h, sortie] of [["miniature", 1280, 720, "miniature_youtube_1280x720.jpg"], ["couverture", 1080, 1920, "couverture_short_1080x1920.jpg"]]) {
    const page = await ouvrir(browser, path.join(EP, "pages", nom + ".html"), w, h);
    await page.locator("#m").screenshot({ path: path.join(OUT, sortie), type: "jpeg", quality: 93 });
    await page.close(); console.log("image →", path.join(OUT, sortie));
  }
}

async function video(browser, fmt) {
  const fichier = path.join(EP, "pages", fmt + ".html");
  const first = await ouvrir(browser, fichier, fmt === "long" ? 1920 : 1080, fmt === "long" ? 1080 : 1920);
  const C = await first.evaluate(() => ({ dur: window.CONFIG.dur, w: window.CONFIG.w, h: window.CONFIG.h, intro: window.CONFIG.intro, voix: window.CONFIG.voix }));
  if (opt("--stills")) {
    const dir = path.join(TMP, "stills_" + fmt); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const ts = opt("--stills").split(",").map(Number);
    for (const [i, t] of ts.entries()) await cliché(first, t, path.join(dir, `s${String(i).padStart(2, "0")}.jpg`));
    const cols = Math.min(fmt === "long" ? 3 : 5, ts.length);
    ff(["-i", path.join(dir, "s%02d.jpg"), "-vf", `scale=${fmt === "long" ? 640 : 360}:-2,tile=${cols}x${Math.ceil(ts.length / cols)}`, "-frames:v", "1", path.join(dir, "planche.jpg")]);
    console.log("planche →", path.join(dir, "planche.jpg"));
    await first.close(); return;
  }
  const dir = path.join(TMP, "frames_" + fmt); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  // images (on saute le trou réservé à l'intro : elle est insérée telle quelle au montage)
  const temps = [];
  for (let n = 0; n < Math.round(C.dur * FPS); n++) { const t = (n + 0.5) / FPS; if (!(C.intro && t >= C.intro.t0 && t < C.intro.t1)) temps.push(t); }
  const nAvant = C.intro ? temps.filter(t => t < C.intro.t0).length : 0;
  const bed = path.join(TMP, `fond_${fmt}.wav`);
  fs.writeFileSync(bed, Buffer.from(await first.evaluate(() => window.renderAudio()), "base64"));
  const pages = [first, ...(await Promise.all(Array.from({ length: WORKERS - 1 }, () => ouvrir(browser, fichier, C.w, C.h))))];
  const t0 = Date.now(); let done = 0;
  await Promise.all(pages.map(async (page, w) => {
    for (let n = w; n < temps.length; n += WORKERS) {
      await cliché(page, temps[n], path.join(dir, `f${String(n).padStart(5, "0")}.jpg`));
      if (++done % 300 === 0) console.log(`${fmt} ${done}/${temps.length} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
  }));
  await Promise.all(pages.map(p => p.close()));
  // montage image + son
  const musique = ["musique.mp3", "musique.wav", "musique.m4a"].map(m => path.join(EP, m)).find(fs.existsSync);
  const ins = ["-framerate", String(FPS), "-i", path.join(dir, "f%05d.jpg")];
  ins.push(...(musique ? ["-stream_loop", "-1", "-i", musique] : ["-i", bed]));
  let k = 2, fc = [];
  if (C.intro) { ins.push("-i", INTRO); k++; }
  const voix = C.voix.map(v => ({ ...v, idx: (ins.push("-i", path.join(EP, v.fichier)), k++) }));
  if (C.intro) {
    fc.push(`[0:v]split=2[va0][vb0]`, `[va0]trim=end_frame=${nAvant},setpts=PTS-STARTPTS,format=yuv420p[va]`, `[vb0]trim=start_frame=${nAvant},setpts=PTS-STARTPTS,format=yuv420p[vb]`,
      `[2:v]fps=${FPS},scale=${C.w}:${C.h},setsar=1,format=yuv420p,setpts=PTS-STARTPTS[vi]`, `[va][vi][vb]concat=n=3:v=1:a=0[v]`);
  } else fc.push(`[0:v]format=yuv420p[v]`);
  const muet = C.intro ? `,volume='if(between(t,${C.intro.t0},${C.intro.t1}),0,1)':eval=frame` : "";
  fc.push(`[1:a]atrim=0:${C.dur},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume=${voix.length ? (musique ? 0.22 : 0.3) : 1}${muet}[mus]`);
  const mix = [];
  if (voix.length) {
    voix.forEach((v, i) => fc.push(`[${v.idx}:a]aformat=sample_rates=48000:channel_layouts=mono,adelay=${Math.round(v.debut * 1000)}:all=1[v${i}]`));
    fc.push(`${voix.map((_, i) => `[v${i}]`).join("")}amix=inputs=${voix.length}:normalize=0,${PODCAST},aformat=channel_layouts=stereo,asplit=2[vox][voxsc]`);
    fc.push(`[mus][voxsc]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=450[musd]`);
    mix.push("[vox]", "[musd]");
  } else mix.push("[mus]");
  if (C.intro) { fc.push(`[2:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=${Math.round(C.intro.t0 * 1000)}:all=1[ia]`); mix.push("[ia]"); }
  fc.push(`${mix.join("")}amix=inputs=${mix.length}:normalize=0,atrim=0:${C.dur},loudnorm=I=${voix.length ? -14 : -18}:TP=-1.5:LRA=11[a]`);
  fs.mkdirSync(OUT, { recursive: true });
  const sortie = path.join(OUT, NOMS[fmt]);
  ff([...ins, "-filter_complex", fc.join(";"), "-map", "[v]", "-map", "[a]", "-t", String(C.dur), "-r", String(FPS),
    "-c:v", "libx264", "-preset", "slow", "-crf", fmt === "long" ? "21" : "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", sortie]);
  fs.rmSync(dir, { recursive: true, force: true });
  console.log(`OK ${fmt} → ${sortie} (${((Date.now() - t0) / 1000).toFixed(0)} s, ${voix.length ? "avec voix" : "maquette sans voix"}${musique ? ", musique Suno" : ", nappe provisoire"})`);
}

(async () => {
  fs.mkdirSync(TMP, { recursive: true });
  const browser = await chromium.launch();
  if (args.includes("--images")) { await images(browser); await browser.close(); return; }
  for (const fmt of FORMATS) await video(browser, fmt);
  if (!opt("--stills") && !opt("--format")) await images(browser);
  await browser.close();
})();
