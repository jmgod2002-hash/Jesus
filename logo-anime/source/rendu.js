// Rendu du logo animé : Playwright fige les animations CSS du SVG à chaque instant t.
// node rendu.js --planche  → planche d'images clés (renders/planche.jpg, non versionnée)
// node rendu.js            → MP4 1080 (entrée + boucle), GIF en boucle, WebM transparent
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = path.join(__dirname, ".."), SVG = path.join(ROOT, "logo_anime.svg"), TMP = path.join(__dirname, "renders");
const SIZE = 1080, FPS = 60, ENTREE = 1.4, CYCLE = 4, FIN = 0.6;
const ff = (args) => execFileSync("ffmpeg", ["-v", "error", "-y", ...args], { stdio: "inherit" });

async function page(browser) {
  const p = await browser.newPage({ viewport: { width: SIZE, height: SIZE } });
  p.on("pageerror", (e) => console.log("[erreur]", e.message));
  await p.goto("file://" + SVG);
  await p.evaluate(() => { document.documentElement.setAttribute("width", innerWidth); document.documentElement.setAttribute("height", innerHeight); });
  return p;
}
const seek = (p, t) => p.evaluate((ms) => document.getAnimations().forEach((a) => { a.pause(); a.currentTime = ms; }), t * 1000);

async function frames(browser, t0, dur, fps, dir, transparent) {
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const N = Math.round(dur * fps), W = 4, pages = await Promise.all(Array.from({ length: W }, () => page(browser)));
  await Promise.all(pages.map(async (p, w) => { for (let n = w; n < N; n += W) { await seek(p, t0 + n / fps);
    await p.screenshot({ path: path.join(dir, `f${String(n).padStart(4, "0")}.png`), omitBackground: transparent }); } }));
  await Promise.all(pages.map((p) => p.close()));
}

(async () => {
  const browser = await chromium.launch(); fs.mkdirSync(TMP, { recursive: true });
  if (process.argv.includes("--planche")) {
    const p = await page(browser), times = [0.2, 0.45, 0.7, 0.85, 0.95, 1.1, 1.3, 2.4, 2.8, 3.7, 4.4, 4.75];
    for (const [i, t] of times.entries()) { await seek(p, t); await p.screenshot({ path: path.join(TMP, `s${String(i).padStart(2, "0")}.png`) }); }
    ff(["-i", path.join(TMP, "s%02d.png"), "-vf", "scale=360:-2,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{n}':x=8:y=8:fontsize=22:fontcolor=black,tile=6x2", "-frames:v", "1", path.join(TMP, "planche.jpg")]);
    return browser.close();
  }
  // 1) MP4 carré : entrée + un cycle complet + pause (fond blanc comme le logo d'origine)
  const dA = path.join(TMP, "mp4"); await frames(browser, 0, ENTREE + CYCLE + FIN, FPS, dA, false);
  ff(["-framerate", String(FPS), "-i", path.join(dA, "f%04d.png"), "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", path.join(ROOT, "logo_anime_1080.mp4")]);
  // 2) WebM transparent (montage vidéo) : même séquence, fond retiré
  const dB = path.join(TMP, "alpha"); await frames(browser, 0, ENTREE + CYCLE + FIN, 30, dB, true);
  ff(["-framerate", "30", "-i", path.join(dB, "f%04d.png"), "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "28", "-auto-alt-ref", "0", path.join(ROOT, "logo_anime_transparent.webm")]);
  // 3) GIF : uniquement le cycle (boucle sans coupure), 600 px, 25 i/s
  const dC = path.join(TMP, "gif"); await frames(browser, ENTREE, CYCLE, 25, dC, false);
  ff(["-framerate", "25", "-i", path.join(dC, "f%04d.png"), "-vf", "scale=600:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=full[p];[b][p]paletteuse=dither=none", "-loop", "0", path.join(ROOT, "logo_anime_boucle.gif")]);
  await browser.close(); fs.rmSync(TMP, { recursive: true, force: true });
  console.log("OK");
})();
