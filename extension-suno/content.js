// Script injecté sur suno.com.
// Rôle : retenir le dernier champ texte cliqué, puis y écrire ce que la fenêtre de l'extension envoie.
// Suno est une application React : on passe par le "setter" natif + un événement "input",
// sinon React ignore la nouvelle valeur.

(() => {
  if (window.__atelierSunoLoaded) return;
  window.__atelierSunoLoaded = true;

  let lastField = null;

  const isTextField = (el) =>
    el &&
    (el.tagName === "TEXTAREA" ||
      (el.tagName === "INPUT" && /^(text|search|)$/i.test(el.type || "")) ||
      el.isContentEditable);

  document.addEventListener(
    "focusin",
    (e) => {
      if (isTextField(e.target)) lastField = e.target;
    },
    true
  );

  // Repère un champ par mots-clés (placeholder, aria-label, name) si aucun n'a été cliqué.
  function findField(kind) {
    const keys =
      kind === "lyrics"
        ? ["lyric", "parole", "song description", "description"]
        : ["style", "genre", "music"];
    const fields = [...document.querySelectorAll("textarea, input[type=text], input:not([type])")].filter(
      (el) => el.offsetParent !== null
    );
    for (const el of fields) {
      const hay = [el.placeholder, el.getAttribute("aria-label"), el.name, el.id]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (keys.some((k) => hay.includes(k))) return el;
    }
    return null;
  }

  function writeValue(el, text, mode) {
    el.focus();
    if (el.isContentEditable) {
      if (mode === "replace") el.textContent = "";
      document.execCommand("insertText", false, text);
      return;
    }
    const proto = el.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
    const setter = Object.getOwnPropertyDescriptor(proto, "value").set;
    let next = text;
    if (mode === "append" && el.value) next = el.value.replace(/\s+$/, "") + "\n\n" + text;
    if (mode === "insert") {
      const s = el.selectionStart ?? el.value.length;
      const e = el.selectionEnd ?? el.value.length;
      next = el.value.slice(0, s) + text + el.value.slice(e);
    }
    setter.call(el, next);
    el.dispatchEvent(new Event("input", { bubbles: true }));
    el.dispatchEvent(new Event("change", { bubbles: true }));
  }

  /* ---------- repérage des chansons pour le téléchargement ---------- */
  const UUID = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;
  const audioById = new Map(); // id -> URL audio réellement jouée par la page

  // Retient l'URL des fichiers audio que la page charge (quand on lance une lecture).
  document.addEventListener(
    "play",
    (e) => {
      const src = e.target?.currentSrc || e.target?.src || "";
      const m = src.match(UUID);
      if (m) audioById.set(m[0].toLowerCase(), src);
    },
    true
  );

  function scanSongs() {
    const songs = new Map();
    const add = (id, title, image) => {
      id = id.toLowerCase();
      const cur = songs.get(id) || { id, title: "", image: "" };
      if (title && title.length > cur.title.length && title.length < 120) cur.title = title;
      if (image && !cur.image) cur.image = image;
      songs.set(id, cur);
    };

    for (const a of document.querySelectorAll('a[href*="/song/"]')) {
      const m = a.getAttribute("href").match(/\/song\/([0-9a-f-]{36})/i);
      if (!m) continue;
      const img = a.querySelector("img");
      const text = (a.getAttribute("title") || a.textContent || img?.alt || "").trim();
      add(m[1], text, img?.src && /suno/.test(img.src) ? img.src : "");
    }

    // Page d'une chanson seule : suno.com/song/<id>
    const here = location.pathname.match(/\/song\/([0-9a-f-]{36})/i);
    if (here) {
      const h1 = document.querySelector("h1");
      const t = (h1?.textContent || document.title.split("|")[0] || "").trim();
      add(here[1], t, "");
    }

    for (const el of document.querySelectorAll("audio[src], audio source[src]")) {
      const m = el.src.match(UUID);
      if (m) {
        add(m[0], "", "");
        audioById.set(m[0].toLowerCase(), el.src);
      }
    }

    return [...songs.values()].map((s) => ({ ...s, audio: audioById.get(s.id) || "" }));
  }

  chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
    if (msg?.type === "atelier-scan") {
      reply({ songs: scanSongs() });
      return;
    }
    if (msg?.type !== "atelier-insert") return;
    const target =
      (msg.target === "focused" && lastField && document.contains(lastField) && lastField) ||
      findField(msg.target) ||
      (lastField && document.contains(lastField) ? lastField : null);
    if (!target) {
      reply({ ok: false, reason: "Aucun champ trouvé. Clique d'abord dans le champ voulu sur Suno." });
      return;
    }
    writeValue(target, msg.text, msg.mode || "replace");
    target.style.outline = "2px solid #e8a33d";
    setTimeout(() => (target.style.outline = ""), 900);
    reply({ ok: true });
  });
})();
