// Rendu de la vidéo TikTok Tadaa : Playwright filme window.seek(t) image par image.
// node rendu.js --planche [--at 1,2,3]  → planche d'images clés (renders/planche.jpg)
// node rendu.js                         → ../tadaa_tiktok_1080x1920.mp4 (60 i/s + bruitages)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = __dirname, OUT = path.join(ROOT, "renders"), DUR = 16, FPS = 60, WORKERS = 4;
const ff = (a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });
async function open(browser) {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on("pageerror", (e) => console.log("[erreur page]", e.message));
  await p.goto("file://" + path.join(ROOT, "index.html")); await p.evaluate(() => window.ready); return p;
}
const shot = async (p, t, f) => { await p.evaluate((x) => window.seek(x), t); await p.locator("#stage").screenshot({ path: f, type: "jpeg", quality: 94 }); };
(async () => {
  const browser = await chromium.launch(); fs.mkdirSync(OUT, { recursive: true });
  if (process.argv.includes("--planche")) {
    const i = process.argv.indexOf("--at"), times = i > 0 ? process.argv[i + 1].split(",").map(Number) : [0.5, 1.5, 2.2, 3.2, 4.3, 5.9, 7.6, 9.3, 10.6, 12.0, 13.2, 15.5];
    const p = await open(browser); fs.readdirSync(OUT).filter((f) => f.startsWith("s")).forEach((f) => fs.rmSync(path.join(OUT, f)));
    for (const [k, t] of times.entries()) await shot(p, t, path.join(OUT, `s${String(k).padStart(2, "0")}.jpg`));
    ff(["-i", path.join(OUT, "s%02d.jpg"), "-vf", `scale=360:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{n}':x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black,tile=${Math.min(6, times.length)}x${Math.ceil(times.length / 6)}`, "-frames:v", "1", path.join(OUT, "planche.jpg")]);
    return browser.close();
  }
  const dir = path.join(OUT, "frames"); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const pages = await Promise.all(Array.from({ length: WORKERS }, () => open(browser))), N = DUR * FPS, t0 = Date.now();
  fs.writeFileSync(path.join(OUT, "son.wav"), Buffer.from(await pages[0].evaluate(() => window.renderAudio()), "base64"));
  await Promise.all(pages.map(async (p, w) => { for (let n = w; n < N; n += WORKERS) await shot(p, n / FPS, path.join(dir, `f${String(n).padStart(4, "0")}.jpg`)); }));
  await browser.close();
  ff(["-framerate", String(FPS), "-i", path.join(dir, "f%04d.jpg"), "-i", path.join(OUT, "son.wav"), "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", path.join(ROOT, "..", "tadaa_tiktok_1080x1920.mp4")]);
  fs.rmSync(OUT, { recursive: true, force: true });
  console.log(`OK (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
})();
