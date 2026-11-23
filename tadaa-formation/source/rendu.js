// Rendu de la vidéo TikTok Tadaa — formation dropshipping : Playwright filme window.seek(t) image par image.
// node rendu.js --planche [--at 1,2,3]  → planche d'images clés (renders/planche.jpg)
// node rendu.js --son                   → mixage voix + bruitages seul (renders/mix.wav)
// node rendu.js                         → ../tadaa_formation_120fps.mp4 (120 i/s) + ../tadaa_formation_60fps.mp4 (60 i/s, flou de mouvement : 2 images fondues)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), { execFileSync } = require("child_process");
const ROOT = __dirname, OUT = path.join(ROOT, "renders"), DUR = 24, FPS = 120, WORKERS = 6;
// Voix ElevenLabs (facultative) : [début parole, fin parole, instant où elle doit commencer dans la vidéo]
// Tant que voix_elevenlabs.mp3 est absent, la vidéo sort avec les bruitages seuls.
const VOIX = path.join(ROOT, "voix_elevenlabs.mp3"), BLOCS = [];
const ff = (a) => execFileSync("ffmpeg", ["-v", "error", "-y", ...a], { stdio: "inherit" });
async function open(browser) {
  const p = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on("pageerror", (e) => console.log("[erreur page]", e.message));
  await p.goto("file://" + path.join(ROOT, "index.html")); await p.evaluate(() => window.ready); return p;
}
function MIX() {
  if (!fs.existsSync(VOIX) || !BLOCS.length) { ff(["-i", path.join(OUT, "son.wav"), "-af", `apad=whole_dur=${DUR},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000`, "-ac", "2", path.join(OUT, "mix.wav")]); return; }
  // mixage : voix placée bloc par bloc, bruitages baissés sous la voix, volume final -14 LUFS
  const parts = BLOCS.map(([s, e, at], k) => { const s0 = Math.max(0, s - 0.06), e0 = e + 0.15, d = e0 - s0, ms = Math.round((at - (s - s0)) * 1000);
    return `[v${k}]atrim=start=${s0}:end=${e0},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=${(d - 0.05).toFixed(3)}:d=0.05,adelay=${ms}:all=1[w${k}]`; });
  const graph = [`[1:a]aresample=48000,pan=stereo|c0=c0|c1=c0,asplit=${BLOCS.length}${BLOCS.map((_, k) => `[v${k}]`).join("")}`, ...parts,
    `${BLOCS.map((_, k) => `[w${k}]`).join("")}amix=inputs=${BLOCS.length}:normalize=0,volume=1.5,asplit=2[voix][sc]`,
    `[0:a]volume=0.6[b]`, `[b][sc]sidechaincompress=threshold=0.03:ratio=5:attack=10:release=300[sfx]`,
    `[voix][sfx]amix=inputs=2:normalize=0:duration=longest,apad=whole_dur=${DUR},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]`].join(";");
  ff(["-i", path.join(OUT, "son.wav"), "-i", VOIX, "-filter_complex", graph, "-map", "[out]", "-ac", "2", path.join(OUT, "mix.wav")]);
}
const shot = async (p, t, f) => { await p.evaluate((x) => window.seek(x), t); await p.locator("#stage").screenshot({ path: f, type: "jpeg", quality: 94 }); };
(async () => {
  const browser = await chromium.launch(); fs.mkdirSync(OUT, { recursive: true });
  if (process.argv.includes("--son")) { // ne refait que le mixage audio (contrôle rapide)
    const p = await open(browser); fs.writeFileSync(path.join(OUT, "son.wav"), Buffer.from(await p.evaluate(() => window.renderAudio()), "base64")); await browser.close(); MIX(); return; }
  if (process.argv.includes("--planche")) {
    const i = process.argv.indexOf("--at"), times = i > 0 ? process.argv[i + 1].split(",").map(Number) : [0, 2.4, 3.4, 3.8, 4.15, 4.9, 7.6, 9.6, 11.6, 13.7, 14.6, 17.8, 20.3, 22.5];
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
  MIX();
  const enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart"];
  const src = ["-framerate", String(FPS), "-i", path.join(dir, "f%04d.jpg"), "-i", path.join(OUT, "mix.wav")];
  ff([...src, "-r", String(FPS), ...enc, path.join(ROOT, "..", "tadaa_formation_120fps.mp4")]);
  ff([...src, "-vf", "tmix=frames=2:weights='1 1',select='eq(mod(n\\,2)\\,1)',setpts=N/(60*TB)", "-r", "60", ...enc, path.join(ROOT, "..", "tadaa_formation_60fps.mp4")]);
  fs.rmSync(OUT, { recursive: true, force: true });
  console.log(`OK (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
})();
