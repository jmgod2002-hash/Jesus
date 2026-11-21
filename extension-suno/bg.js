// Service worker : file d'attente d'enregistrement.
//
// Suno chiffre ses fichiers audio : il n'y a plus de lien MP3 direct.
// Méthode : pour chaque chanson, on ouvre sa page dans un onglet en arrière-plan, son coupé,
// on la lit du début à la fin et on enregistre ce que le lecteur joue (record.js).
// Une chanson à la fois ; l'enregistrement prend la durée de la chanson.
//
// L'état de la file est dans chrome.storage.session : il survit à la mise en veille du service worker.

const QKEY = "atelierQueue";
const PKEY = "atelierPageSettings";

// Les scripts de page (boutons ⬇) doivent pouvoir lire l'état de la file pour s'afficher.
chrome.storage.session.setAccessLevel?.({ accessLevel: "TRUSTED_AND_UNTRUSTED_CONTEXTS" });

const clean = (s) =>
  (s || "sans-titre")
    .replace(/[\\/:*?"<>|~\u0000-\u001f]/g, "")
    .replace(/\s+/g, " ")
    .replace(/^\.+|\.+$/g, "")
    .trim()
    .slice(0, 100) || "sans-titre";

/* ---------- état ---------- */
async function getQueue() {
  return (await chrome.storage.session.get(QKEY))[QKEY] || [];
}
async function setQueue(q) {
  await chrome.storage.session.set({ [QKEY]: q });
}

// Toutes les modifications passent par ce verrou pour éviter les écritures croisées.
let lock = Promise.resolve();
function withQueue(fn) {
  const run = lock.then(async () => {
    const q = await getQueue();
    const out = await fn(q);
    await setQueue(q);
    return out;
  });
  lock = run.catch(() => {});
  return run;
}

/* ---------- ajout à la file ---------- */
async function enqueue(songs, opts) {
  const added = await withQueue((q) => {
    let n = 0;
    for (const s of songs) {
      const existing = q.find((j) => j.id === s.id);
      if (existing && ["attente", "enregistrement"].includes(existing.status)) continue;
      if (existing) q.splice(q.indexOf(existing), 1); // relance d'une chanson déjà traitée
      q.push({
        id: s.id,
        title: s.title || "",
        status: "attente",
        progress: 0,
        duration: 0,
        cover: !!opts.cover,
        folder: clean(opts.folder || "Suno"),
        error: "",
        tabId: null,
        added: Date.now()
      });
      n++;
    }
    return n;
  });
  kick();
  return added;
}

/* ---------- lancement de la chanson suivante ---------- */
async function kick() {
  const job = await withQueue((q) => {
    if (q.some((j) => j.status === "enregistrement")) return null;
    const next = q.find((j) => j.status === "attente");
    if (!next) return null;
    next.status = "enregistrement";
    next.started = Date.now();
    return { ...next };
  });
  if (!job) return;
  try {
    // Petite fenêtre séparée, visible mais sans prendre le focus : Chrome retarde la lecture
    // dans un onglet ouvert en arrière-plan qui n'a jamais été affiché, pas dans une fenêtre visible.
    const W = 420, H = 300;
    const place = {};
    try {
      const cur = await chrome.windows.getLastFocused();
      if (cur?.width) {
        place.left = Math.max(0, cur.left + cur.width - W - 16);
        place.top = Math.max(0, cur.top + cur.height - H - 16);
      }
    } catch {}
    const opts = { url: `https://suno.com/song/${job.id}#atelier-rec`, type: "popup", focused: false, width: W, height: H };
    let win;
    try {
      win = await chrome.windows.create({ ...opts, ...place });
    } catch {
      win = await chrome.windows.create(opts); // position refusée (écran multiple…) : Chrome choisit
    }
    const tab = win.tabs[0];
    await chrome.tabs.update(tab.id, { muted: true });
    await withQueue((q) => {
      const j = q.find((x) => x.id === job.id);
      if (j) j.tabId = tab.id;
    });
  } catch (e) {
    await finish(job.id, "erreur", "Impossible d'ouvrir l'onglet : " + (e?.message || e));
  }
}

async function finish(id, status, error = "") {
  const job = await withQueue((q) => {
    const j = q.find((x) => x.id === id);
    if (!j) return null;
    j.status = status;
    j.error = error;
    if (status === "enregistré") j.progress = 1;
    const tabId = j.tabId;
    j.tabId = null;
    return { ...j, tabId };
  });
  if (job?.tabId) chrome.tabs.remove(job.tabId).catch(() => {});
  kick();
}

async function save(job, dataUrl, ext, pageTitle) {
  const title = job.title || pageTitle || "Chanson Suno";
  const base = `${job.folder}/${clean(title)} [${job.id.slice(0, 8)}]`;
  const dl = async (url, filename) => {
    const opts = { url, filename, conflictAction: "uniquify", saveAs: false };
    try {
      return await chrome.downloads.download(opts);
    } catch {
      // Repli : nom sans accents ni caractères spéciaux (certains systèmes les refusent).
      opts.filename = filename.normalize("NFD").replace(/[^\x20-\x7e]/g, "");
      return await chrome.downloads.download(opts);
    }
  };
  await dl(dataUrl, `${base}.${ext}`);
  if (job.cover) {
    await dl(`https://cdn2.suno.ai/image_large_${job.id}.jpeg`, `${base}.jpg`).catch(() => {});
  }
}

/* ---------- messages ---------- */
chrome.runtime.onMessage.addListener((msg, sender, reply) => {
  const tabId = sender.tab?.id;

  (async () => {
    switch (msg?.type) {
      case "atelier-download": {
        const settings = (await chrome.storage.local.get(PKEY))[PKEY] || {};
        const n = await enqueue(msg.songs || [], {
          cover: msg.cover ?? !!settings.withCover,
          folder: msg.folder
        });
        reply({ queued: n });
        break;
      }

      // record.js demande s'il est dans un onglet d'enregistrement.
      case "atelier-rec-hello": {
        const q = await getQueue();
        const job = q.find((j) => j.status === "enregistrement" && j.tabId === tabId);
        reply(job ? { record: true, id: job.id } : { record: false });
        break;
      }

      case "atelier-rec-progress": {
        await withQueue((q) => {
          const j = q.find((x) => x.id === msg.id && x.tabId === tabId);
          if (j) {
            j.progress = msg.progress;
            j.duration = msg.duration;
            j.needClick = false;
          }
        });
        reply({});
        break;
      }

      case "atelier-rec-done": {
        const job = (await getQueue()).find((x) => x.id === msg.id && x.tabId === tabId);
        if (!job) return reply({});
        try {
          await save(job, msg.dataUrl, msg.ext, msg.title);
          await finish(job.id, "enregistré");
        } catch (e) {
          await finish(job.id, "erreur", "Enregistrement OK mais sauvegarde impossible : " + (e?.message || e));
        }
        reply({});
        break;
      }

      // Vrai clic (accepté par Chrome comme un geste de l'utilisateur), via l'outil de débogage.
      // Seulement si l'utilisateur a accordé la permission « debugger » dans l'extension.
      case "atelier-rec-trusted-click": {
        const job = (await getQueue()).find((j) => j.tabId === tabId && j.status === "enregistrement");
        if (!job || !(await chrome.permissions.contains({ permissions: ["debugger"] }))) return reply({ ok: false });
        const target = { tabId };
        try {
          await chrome.debugger.attach(target, "1.3");
          for (const type of ["mousePressed", "mouseReleased"]) {
            await chrome.debugger.sendCommand(target, "Input.dispatchMouseEvent", {
              type, x: msg.x, y: msg.y, button: "left", clickCount: 1
            });
          }
          reply({ ok: true });
        } catch (e) {
          reply({ ok: false, error: e?.message });
        } finally {
          chrome.debugger.detach(target).catch(() => {});
        }
        break;
      }

      // Aucun clic automatique possible : on met la fenêtre d'enregistrement devant l'utilisateur.
      case "atelier-rec-need-click": {
        if (sender.tab?.windowId) {
          await chrome.windows.update(sender.tab.windowId, { focused: true, width: 900, height: 700 }).catch(() => {});
        }
        await withQueue((q) => {
          const j = q.find((x) => x.tabId === tabId);
          if (j) j.needClick = true;
        });
        reply({});
        break;
      }

      case "atelier-rec-error": {
        await finish(msg.id, "erreur", msg.error || "Erreur inconnue");
        reply({});
        break;
      }

      case "atelier-queue-retry": {
        await withQueue((q) => {
          for (const j of q) if (j.status === "erreur") { j.status = "attente"; j.error = ""; j.progress = 0; }
        });
        kick();
        reply({});
        break;
      }

      case "atelier-queue-clear": {
        await withQueue((q) => {
          const keep = q.filter((j) => j.status === "enregistrement");
          q.length = 0;
          q.push(...keep);
        });
        reply({});
        break;
      }

      case "atelier-queue-cancel": {
        const tabs = await withQueue((q) => {
          const ids = q.filter((j) => j.tabId).map((j) => j.tabId);
          q.length = 0;
          return ids;
        });
        tabs.forEach((t) => chrome.tabs.remove(t).catch(() => {}));
        reply({});
        break;
      }

      default:
        return; // pas pour nous
    }
  })();
  return true; // réponse asynchrone
});

// L'utilisateur ferme l'onglet d'enregistrement : on passe à la suite.
chrome.tabs.onRemoved.addListener(async (tabId) => {
  const job = (await getQueue()).find((j) => j.tabId === tabId && j.status === "enregistrement");
  if (job) finish(job.id, "erreur", "Onglet d'enregistrement fermé avant la fin");
});

// Au redémarrage du navigateur, un enregistrement interrompu repasse en attente.
chrome.runtime.onStartup.addListener(async () => {
  await withQueue((q) => {
    for (const j of q) if (j.status === "enregistrement") { j.status = "attente"; j.tabId = null; }
  });
  kick();
});
