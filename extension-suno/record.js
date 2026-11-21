// Enregistreur : ne s'active que dans l'onglet ouvert par l'extension pour une chanson.
// Il lance la lecture sur la page Suno, enregistre la sortie du lecteur audio
// du début à la fin, puis renvoie le fichier au service worker.

(async () => {
  if (window.__atelierRecLoaded) return;
  window.__atelierRecLoaded = true;
  if (!/^\/song\//.test(location.pathname)) return;

  let job;
  try {
    job = await chrome.runtime.sendMessage({ type: "atelier-rec-hello" });
  } catch {
    return;
  }
  if (!job?.record) return; // onglet normal de l'utilisateur : on ne touche à rien

  const id = job.id;
  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
  const send = (msg) => chrome.runtime.sendMessage({ ...msg, id }).catch(() => {});
  const fail = (error) => send({ type: "atelier-rec-error", error });

  async function waitFor(fn, timeoutMs, stepMs = 250) {
    const end = Date.now() + timeoutMs;
    while (Date.now() < end) {
      const v = fn();
      if (v) return v;
      await sleep(stepMs);
    }
    return null;
  }

  // Le lecteur de Suno : un élément <audio> alimenté par un flux "blob:" (audio déchiffré par Suno).
  const findPlayer = () => [...document.querySelectorAll("audio")].find((a) => a.src.startsWith("blob:"));

  // Bandeau affiché dans la fenêtre d'enregistrement quand il faut un clic de l'utilisateur.
  function showBanner(text) {
    let el = document.getElementById("atelier-banner");
    if (!el) {
      el = document.createElement("div");
      el.id = "atelier-banner";
      el.style.cssText =
        "position:fixed;top:0;left:0;right:0;z-index:2147483647;padding:12px 16px;background:#e8a33d;" +
        "color:#1a1206;font:600 14px/1.35 system-ui,sans-serif;text-align:center;box-shadow:0 4px 16px rgba(0,0,0,.4)";
      document.documentElement.appendChild(el);
    }
    el.textContent = text;
  }
  const hideBanner = () => document.getElementById("atelier-banner")?.remove();

  // Titre affiché par Suno : « Titre by artiste | Suno ».
  const pageTitle = () =>
    (document.querySelector("h1")?.textContent || document.title.replace(/\s*\|\s*Suno\s*$/i, "").replace(/\s+by\s+.*$/i, "")).trim();

  // Formats essayés dans l'ordre : AAC (.m4a, lu partout), puis Opus.
  function pickFormat() {
    const options = [
      ["audio/mp4;codecs=mp4a.40.2", "m4a"],
      ["audio/mp4", "m4a"],
      ["audio/webm;codecs=opus", "webm"]
    ];
    return options.find(([t]) => window.MediaRecorder?.isTypeSupported(t)) || null;
  }

  try {
    // 1. Lancer la lecture via le bouton « Play » de la page.
    //    Le bouton existe avant que la page soit « active » : un clic trop tôt est ignoré.
    //    On attend un peu, puis on réessaie tant que le lecteur n'a pas démarré.
    const getBtn = () => document.querySelector('button[aria-label="Play"]');
    if (!(await waitFor(getBtn, 30000)))
      return fail("Bouton Lecture introuvable sur la page Suno (chanson supprimée ou page modifiée ?)");
    await sleep(3000);

    // Le bouton « Play » de Suno alterne lecture/pause : on ne reclique que si rien ne joue.
    const playing = () => {
      const a = findPlayer();
      return a && !a.paused && a.currentTime > 0 && a.duration > 1 ? a : null;
    };
    // Niveau 1 : clic simple. Chrome l'accepte si tu écoutes souvent Suno (il juge le site « habituel »).
    let audio = null;
    for (let attempt = 0; attempt < 2 && !audio; attempt++) {
      if (!playing()) getBtn()?.click();
      audio = await waitFor(playing, 6000);
    }

    // Niveau 2 : vrai clic envoyé par Chrome (permission « démarrage automatique » accordée dans l'extension).
    for (let attempt = 0; attempt < 3 && !audio; attempt++) {
      const btn = getBtn();
      if (!btn) break;
      btn.scrollIntoView({ block: "center" });
      await sleep(300);
      const r = btn.getBoundingClientRect();
      const res = await send({ type: "atelier-rec-trusted-click", x: r.left + r.width / 2, y: r.top + r.height / 2 });
      if (!res?.ok) break; // permission non accordée
      audio = await waitFor(playing, 6000);
    }

    // Niveau 3 : on demande à l'utilisateur de cliquer lui-même dans cette fenêtre.
    if (!audio) {
      await send({ type: "atelier-rec-need-click" });
      showBanner("Atelier Suno : clique sur ▶ Play (sous le titre) pour lancer l'enregistrement. Le son reste coupé.");
      audio = await waitFor(playing, 5 * 60 * 1000, 500);
      hideBanner();
    }
    if (!audio)
      return fail("La lecture n'a pas démarré : Chrome exige un clic (active le démarrage automatique dans l'extension)");

    // 2. Préparer la capture, revenir au début (sans pause, pour ne pas perturber le lecteur Suno), enregistrer.
    const stream = audio.captureStream();
    if (!(await waitFor(() => stream.getAudioTracks().length > 0, 10000, 50))) return fail("Capture audio impossible");

    audio.currentTime = 0;
    await new Promise((r) => (audio.seeking ? audio.addEventListener("seeked", r, { once: true }) : r()));

    const format = pickFormat();
    if (!format) return fail("Ce navigateur ne sait pas encoder l'audio");
    const [mimeType, ext] = format;
    const rec = new MediaRecorder(new MediaStream(stream.getAudioTracks()), {
      mimeType,
      audioBitsPerSecond: 256000
    });
    const chunks = [];
    rec.ondataavailable = (e) => e.data.size && chunks.push(e.data);
    const stopped = new Promise((r) => (rec.onstop = r));

    rec.start(1000);

    // 3. Suivi jusqu'à la fin de la chanson.
    const duration = audio.duration;
    const src = audio.src;
    let lastT = -1, stuckSince = Date.now();

    await new Promise((resolve, reject) => {
      const done = () => { clearInterval(timer); resolve(); };
      audio.addEventListener("ended", done, { once: true });
      const timer = setInterval(() => {
        // Suno a changé de chanson (file de lecture) : on arrête là.
        if (audio.src !== src || !document.contains(audio)) return done();
        if (audio.currentTime >= duration - 0.05) return done();
        send({ type: "atelier-rec-progress", progress: audio.currentTime / duration, duration });
        if (audio.currentTime !== lastT) {
          lastT = audio.currentTime;
          stuckSince = Date.now();
        } else {
          if (audio.paused) audio.play().catch(() => {});
          if (Date.now() - stuckSince > 60000) {
            clearInterval(timer);
            reject(new Error("Lecture bloquée depuis 1 minute (réseau ?)"));
          }
        }
      }, 2000);
    });

    rec.stop();
    await stopped;
    audio.pause();

    const blob = new Blob(chunks, { type: mimeType.split(";")[0] });
    if (blob.size < 10000) return fail("Enregistrement vide");

    const dataUrl = await new Promise((r, j) => {
      const fr = new FileReader();
      fr.onload = () => r(fr.result);
      fr.onerror = () => j(fr.error);
      fr.readAsDataURL(blob);
    });
    await send({ type: "atelier-rec-done", dataUrl, ext, title: pageTitle() });
  } catch (e) {
    fail(e?.message || String(e));
  }
})();
