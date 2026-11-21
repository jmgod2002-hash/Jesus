// Rendu de l'animation : Playwright dessine window.seek(t) image par image, ffmpeg assemble avec l'ambiance sonore.
// python3 animation/source/decors.py      → régénère animation/index.html
// node animation/render.js --stills        → quelques images + planche de contrôle (renders/stills/planche.jpg)
// node animation/render.js --son           → refait seulement l'ambiance sonore de la vidéo existante
// node animation/render.js                 → vidéo 1920x1080, 30 i/s → animation/personnage_decors_1920x1080.mp4
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");

const ROOT = __dirname, OUT = path.join(ROOT, "renders"), FPS = 30, WORKERS = 4;
const STILLS = process.argv.includes("--stills"), SON = process.argv.includes("--son");
const MP4 = path.join(ROOT, "personnage_decors_1920x1080.mp4");

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.log("[erreur page]", e.message));
  page.on("console", (m) => { if (m.type() === "error") console.log("[console]", m.text()); });
  await page.goto("file://" + path.join(ROOT, "index.html"));
  await page.evaluate(() => window.ready);
  return page;
}
const shot = async (page, t, file) => { await page.evaluate((tt) => window.seek(tt), t); await page.locator("#stage").screenshot({ path: file, type: "jpeg", quality: 93 }); };

(async () => {
  const browser = await chromium.launch();
  const first = await openPage(browser);
  const DUR = await first.evaluate(() => window.CONFIG.dur);
  if (STILLS) {
    const dir = path.join(OUT, "stills"); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
    const times = process.argv.includes("--at") ? process.argv[process.argv.indexOf("--at") + 1].split(",").map(Number) : [1.3, 3.6, 6.3, 8.6, 11.3, 13.6, 16.3, 18.6];
    for (const [i, t] of times.entries()) await shot(first, t, path.join(dir, `s${String(i).padStart(2, "0")}.jpg`));
    await browser.close();
    const cols = Math.min(4, times.length);
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", path.join(dir, "s%02d.jpg"), "-vf", `scale=640:-2,tile=${cols}x${Math.ceil(times.length / cols)}`, "-frames:v", "1", path.join(dir, "planche.jpg")]);
    console.log("planche →", path.join(dir, "planche.jpg"));
    return;
  }
  if (SON) {
    fs.mkdirSync(OUT, { recursive: true });
    fs.writeFileSync(path.join(OUT, "ambiance.wav"), Buffer.from(await first.evaluate(() => window.renderAudio()), "base64"));
    await browser.close();
    const tmp = MP4.replace(".mp4", ".tmp.mp4");
    execFileSync("ffmpeg", ["-v", "error", "-y", "-i", MP4, "-i", path.join(OUT, "ambiance.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
      "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", tmp], { stdio: "inherit" });
    fs.renameSync(tmp, MP4); console.log("son refait →", MP4);
    return;
  }
  const dir = path.join(OUT, "frames"); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const N = Math.round(DUR * FPS), t0 = Date.now();
  const wav = await first.evaluate(() => window.renderAudio());
  fs.writeFileSync(path.join(OUT, "ambiance.wav"), Buffer.from(wav, "base64"));
  const pages = [first, ...(await Promise.all(Array.from({ length: WORKERS - 1 }, () => openPage(browser))))];
  let done = 0;
  await Promise.all(pages.map(async (page, w) => {
    for (let n = w; n < N; n += WORKERS) {
      await shot(page, (n + 0.5) / FPS, path.join(dir, `f${String(n).padStart(5, "0")}.jpg`));
      if (++done % 60 === 0) console.log(`${done}/${N} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
  }));
  await browser.close();
  execFileSync("ffmpeg", ["-v", "error", "-y", "-framerate", String(FPS), "-i", path.join(dir, "f%05d.jpg"), "-i", path.join(OUT, "ambiance.wav"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "192k", "-shortest", MP4], { stdio: "inherit" });
  fs.rmSync(dir, { recursive: true, force: true });
  console.log("OK →", MP4, `(${((Date.now() - t0) / 1000).toFixed(0)} s)`);
})();
