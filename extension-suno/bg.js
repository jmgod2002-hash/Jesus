// Service worker : file d'attente de téléchargements.
// Tourne en arrière-plan pour que les téléchargements continuent si on ferme la fenêtre de l'extension.

const clean = (s) =>
  (s || "sans-titre")
    .replace(/[\\/:*?"<>|\u0000-\u001f]/g, "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 100) || "sans-titre";

chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
  if (msg?.type !== "atelier-download") return;
  (async () => {
    const folder = clean(msg.folder || "Suno");
    let ok = 0, fail = 0;
    const errors = [];
    for (const song of msg.songs) {
      const base = `${folder}/${clean(song.title)} [${song.id.slice(0, 8)}]`;
      const jobs = [];
      if (msg.audio) jobs.push({ url: song.audio || `https://cdn1.suno.ai/${song.id}.mp3`, filename: `${base}.mp3` });
      if (msg.cover) jobs.push({ url: song.image || `https://cdn2.suno.ai/image_${song.id}.jpeg`, filename: `${base}.jpg` });
      for (const j of jobs) {
        const opts = { ...j, conflictAction: "uniquify", saveAs: false };
        try {
          try {
            await chrome.downloads.download(opts);
          } catch {
            // Repli : nom sans accents ni caractères spéciaux (certains systèmes les refusent).
            opts.filename = j.filename.normalize("NFD").replace(/[^\x20-\x7e]/g, "");
            await chrome.downloads.download(opts);
          }
          ok++;
        } catch (e) {
          fail++;
          errors.push(`${j.filename} : ${e?.message || e}`);
        }
        await new Promise((r) => setTimeout(r, 350)); // évite de saturer le serveur
      }
    }
    reply({ ok, fail, errors });
  })();
  return true; // réponse asynchrone
});
