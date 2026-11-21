const D = window.ATELIER_DATA;
const $ = (s) => document.querySelector(s);
const STORE_KEY = "atelierLibrary";
const DRAFT_KEY = "atelierDraft";

/* ---------- utilitaires ---------- */
function setStatus(text, kind = "") {
  const el = $("#status");
  el.textContent = text;
  el.className = "status " + kind;
  clearTimeout(setStatus.t);
  setStatus.t = setTimeout(() => (el.textContent = ""), 2500);
}
const mode = () => document.querySelector("input[name=mode]:checked").value;
const splitList = (s) => s.split(",").map((x) => x.trim()).filter(Boolean);

async function copy(text) {
  await navigator.clipboard.writeText(text);
  setStatus("Copié", "ok");
}

async function insert(text, target) {
  if (!text.trim()) return setStatus("Rien à insérer", "err");
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.url || !/^https:\/\/([a-z0-9-]+\.)?suno\.com\//.test(tab.url)) {
    await copy(text);
    return setStatus("Pas sur suno.com : texte copié", "err");
  }
  const send = () => chrome.tabs.sendMessage(tab.id, { type: "atelier-insert", text, target, mode: mode() });
  let res;
  try {
    res = await send();
  } catch {
    // Onglet ouvert avant l'installation : on injecte le script puis on réessaie.
    await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
    res = await send();
  }
  if (res?.ok) setStatus("Inséré", "ok");
  else {
    await copy(text);
    setStatus(res?.reason ? "Champ introuvable : copié" : "Échec : copié", "err");
  }
}

/* ---------- onglets ---------- */
document.querySelectorAll(".tabs button").forEach((b) =>
  b.addEventListener("click", () => {
    document.querySelectorAll(".tabs button, .panel").forEach((x) => x.classList.remove("active"));
    b.classList.add("active");
    $("#tab-" + b.dataset.tab).classList.add("active");
    document.body.classList.toggle("dl-mode", b.dataset.tab === "dl");
    if (b.dataset.tab === "library") renderLibrary();
    saveDraft();
  })
);

/* ---------- STYLE ---------- */
const selected = new Set();

function buildChips() {
  const root = $("#chips");
  for (const cat of D.categories) {
    const box = document.createElement("div");
    box.className = "cat";
    box.innerHTML = `<h2>${cat.name}</h2>`;
    const row = document.createElement("div");
    row.className = "chips";
    for (const item of cat.items) {
      const c = document.createElement("button");
      c.className = "chip";
      c.textContent = item;
      c.dataset.value = item;
      c.addEventListener("click", () => {
        selected.has(item) ? selected.delete(item) : selected.add(item);
        c.classList.toggle("on");
        composeStyle();
      });
      row.appendChild(c);
    }
    box.appendChild(row);
    root.appendChild(box);
  }
}

function composeStyle() {
  const parts = [...selected, ...splitList($("#style-free").value)];
  const excl = splitList($("#style-exclude").value);
  let out = parts.join(", ");
  if (excl.length) out += (out ? ". " : "") + "Exclude: " + excl.join(", ");
  $("#style-out").value = out;
  updateStyleCount();
  saveDraft();
}
function updateStyleCount() {
  $("#style-count").textContent = $("#style-out").value.length;
}

$("#style-free").addEventListener("input", composeStyle);
$("#style-exclude").addEventListener("input", composeStyle);
$("#style-out").addEventListener("input", () => { updateStyleCount(); saveDraft(); });
$("#style-clear").addEventListener("click", () => {
  selected.clear();
  document.querySelectorAll(".chip.on").forEach((c) => c.classList.remove("on"));
  $("#style-free").value = $("#style-exclude").value = "";
  composeStyle();
});
$("#style-copy").addEventListener("click", () => copy($("#style-out").value));
$("#style-insert").addEventListener("click", () => insert($("#style-out").value, "style"));
$("#style-save").addEventListener("click", () => saveItem("style", $("#style-out").value));

/* ---------- PAROLES ---------- */
function buildLyrics() {
  const sel = $("#tpl");
  sel.innerHTML = `<option value="">— choisir —</option>` +
    Object.keys(D.templates).map((k) => `<option>${k}</option>`).join("");
  sel.addEventListener("change", () => {
    const t = D.templates[sel.value];
    if (!t) return;
    const ta = $("#lyrics-out");
    if (ta.value.trim() && !confirm("Remplacer les paroles actuelles par ce modèle ?")) {
      sel.value = "";
      return;
    }
    ta.value = t.map((tag) => tag + "\n").join("\n");
    sel.value = "";
    updateLyricsCount();
  });

  const bar = $("#tags");
  for (const tag of D.tags) {
    const b = document.createElement("button");
    b.className = "chip";
    b.textContent = tag;
    b.addEventListener("click", () => insertAtCursor($("#lyrics-out"), tag + "\n"));
    bar.appendChild(b);
  }
}

function insertAtCursor(ta, text) {
  const s = ta.selectionStart, e = ta.selectionEnd;
  const before = ta.value.slice(0, s);
  const prefix = before && !before.endsWith("\n\n") ? (before.endsWith("\n") ? "\n" : "\n\n") : "";
  ta.value = before + prefix + text + ta.value.slice(e);
  const pos = (before + prefix + text).length;
  ta.focus();
  ta.setSelectionRange(pos, pos);
  updateLyricsCount();
}

function updateLyricsCount() {
  const v = $("#lyrics-out").value;
  $("#lyrics-count").textContent = v.length;
  $("#lyrics-lines").textContent = v ? v.split("\n").length : 0;
  saveDraft();
}
$("#lyrics-out").addEventListener("input", updateLyricsCount);
$("#lyrics-clear").addEventListener("click", () => {
  if (!$("#lyrics-out").value || confirm("Effacer les paroles ?")) {
    $("#lyrics-out").value = "";
    updateLyricsCount();
  }
});
$("#lyrics-copy").addEventListener("click", () => copy($("#lyrics-out").value));
$("#lyrics-insert").addEventListener("click", () => insert($("#lyrics-out").value, "lyrics"));
$("#lyrics-save").addEventListener("click", () => saveItem("lyrics", $("#lyrics-out").value));

/* ---------- BIBLIOTHÈQUE ---------- */
async function getLib() {
  return (await chrome.storage.local.get(STORE_KEY))[STORE_KEY] || [];
}
async function setLib(lib) {
  await chrome.storage.local.set({ [STORE_KEY]: lib });
}

async function saveItem(kind, text) {
  if (!text.trim()) return setStatus("Rien à enregistrer", "err");
  const name = prompt("Nom de l'entrée :", text.split("\n").find((l) => l.trim() && !/^\[.*\]$/.test(l.trim()))?.slice(0, 40) || kind);
  if (name === null) return;
  const lib = await getLib();
  lib.unshift({ id: crypto.randomUUID(), kind, name: name.trim() || kind, text, date: Date.now() });
  await setLib(lib);
  setStatus("Enregistré", "ok");
}

async function renderLibrary() {
  const q = $("#lib-search").value.toLowerCase();
  const lib = (await getLib()).filter((i) => !q || (i.name + " " + i.text).toLowerCase().includes(q));
  const ul = $("#lib-list");
  ul.innerHTML = "";
  $("#lib-empty").style.display = lib.length ? "none" : "block";
  for (const item of lib) {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="lib-head">
        <div class="lib-name"><span class="lib-kind"></span><span class="n"></span></div>
        <div class="lib-btns">
          <button data-a="load">Ouvrir</button>
          <button data-a="insert">Insérer</button>
          <button data-a="del">✕</button>
        </div>
      </div>
      <div class="lib-preview"></div>`;
    li.querySelector(".lib-kind").textContent = item.kind === "style" ? "Style" : "Paroles";
    li.querySelector(".n").textContent = item.name;
    li.querySelector(".lib-preview").textContent = item.text;
    li.querySelector("[data-a=load]").onclick = () => {
      const tab = item.kind === "style" ? "style" : "lyrics";
      $(`#${tab}-out`).value = item.text;
      item.kind === "style" ? updateStyleCount() : updateLyricsCount();
      document.querySelector(`.tabs button[data-tab=${tab}]`).click();
    };
    li.querySelector("[data-a=insert]").onclick = () => insert(item.text, item.kind);
    li.querySelector("[data-a=del]").onclick = async () => {
      if (!confirm(`Supprimer « ${item.name} » ?`)) return;
      await setLib((await getLib()).filter((x) => x.id !== item.id));
      renderLibrary();
    };
    ul.appendChild(li);
  }
}
$("#lib-search").addEventListener("input", renderLibrary);

$("#lib-export").addEventListener("click", async () => {
  const blob = new Blob([JSON.stringify(await getLib(), null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `atelier-suno-${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(a.href);
});

$("#lib-import").addEventListener("change", async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  try {
    const data = JSON.parse(await file.text());
    if (!Array.isArray(data)) throw new Error();
    const clean = data
      .filter((i) => i && typeof i.text === "string")
      .map((i) => ({
        id: crypto.randomUUID(),
        kind: i.kind === "style" ? "style" : "lyrics",
        name: String(i.name || "Importé").slice(0, 80),
        text: i.text,
        date: Number(i.date) || Date.now()
      }));
    const lib = await getLib();
    await setLib([...clean, ...lib]);
    setStatus(`${clean.length} importé(s)`, "ok");
    renderLibrary();
  } catch {
    setStatus("Fichier invalide", "err");
  }
  e.target.value = "";
});

/* ---------- brouillon (survit à la fermeture du popup) ---------- */
function saveDraft() {
  clearTimeout(saveDraft.t);
  saveDraft.t = setTimeout(() => {
    chrome.storage.local.set({
      [DRAFT_KEY]: {
        selected: [...selected],
        free: $("#style-free").value,
        exclude: $("#style-exclude").value,
        style: $("#style-out").value,
        lyrics: $("#lyrics-out").value,
        tab: document.querySelector(".tabs button.active").dataset.tab,
        mode: mode()
      }
    });
  }, 200);
}

async function restoreDraft() {
  const d = (await chrome.storage.local.get(DRAFT_KEY))[DRAFT_KEY];
  if (!d) return;
  (d.selected || []).forEach((v) => {
    selected.add(v);
    document.querySelector(`.chip[data-value="${CSS.escape(v)}"]`)?.classList.add("on");
  });
  $("#style-free").value = d.free || "";
  $("#style-exclude").value = d.exclude || "";
  $("#style-out").value = d.style || "";
  $("#lyrics-out").value = d.lyrics || "";
  const m = document.querySelector(`input[name=mode][value="${d.mode}"]`);
  if (m) m.checked = true;
  updateStyleCount();
  updateLyricsCount();
  if (d.tab && d.tab !== "dl") document.querySelector(`.tabs button[data-tab=${d.tab}]`)?.click();
}
document.querySelectorAll("input[name=mode]").forEach((r) => r.addEventListener("change", saveDraft));

/* ---------- TÉLÉCHARGER ---------- */
let found = [];

async function sunoTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab?.url && /^https:\/\/([a-z0-9-]+\.)?suno\.com\//.test(tab.url) ? tab : null;
}

async function scan() {
  const tab = await sunoTab();
  if (!tab) return setStatus("Ouvre d'abord une page suno.com", "err");
  const ask = () => chrome.tabs.sendMessage(tab.id, { type: "atelier-scan" });
  let res;
  try {
    res = await ask();
  } catch {
    await chrome.scripting.executeScript({ target: { tabId: tab.id }, files: ["content.js"] });
    res = await ask();
  }
  found = res?.songs || [];
  renderSongs();
  setStatus(`${found.length} chanson(s) trouvée(s)`, found.length ? "ok" : "err");
}

function renderSongs() {
  const ul = $("#dl-list");
  ul.innerHTML = "";
  $("#dl-empty").style.display = found.length ? "none" : "block";
  for (const s of found) {
    const li = document.createElement("li");
    li.innerHTML = `<input type="checkbox"><img alt=""><span class="t"></span>`;
    const cb = li.querySelector("input");
    cb.checked = true;
    cb.dataset.id = s.id;
    const img = li.querySelector("img");
    img.onerror = () => (img.style.visibility = "hidden");
    if (s.image) img.src = s.image; else img.style.visibility = "hidden";
    li.querySelector(".t").textContent = s.title || s.id;
    li.addEventListener("click", (e) => {
      if (e.target !== cb) cb.checked = !cb.checked;
      updateDlCount();
    });
    ul.appendChild(li);
  }
  $("#dl-all").checked = found.length > 0;
  updateDlCount();
}

function checkedSongs() {
  const ids = new Set([...document.querySelectorAll("#dl-list input:checked")].map((c) => c.dataset.id));
  return found.filter((s) => ids.has(s.id));
}
function updateDlCount() {
  $("#dl-count").textContent = `${checkedSongs().length} sélectionnée(s)`;
}

$("#dl-scan").addEventListener("click", scan);
$("#dl-all").addEventListener("change", (e) => {
  document.querySelectorAll("#dl-list input").forEach((c) => (c.checked = e.target.checked));
  updateDlCount();
});
$("#dl-go").addEventListener("click", async () => {
  const songs = checkedSongs();
  if (!songs.length) return setStatus("Aucune chanson cochée", "err");
  const res = await chrome.runtime.sendMessage({
    type: "atelier-download",
    songs: songs.map((s) => ({ id: s.id, title: s.title })),
    cover: $("#dl-cover").checked,
    folder: $("#dl-folder").value
  });
  setStatus(res?.queued ? `${res.queued} ajoutée(s) à la file` : "Déjà dans la file", res?.queued ? "ok" : "");
});

/* ---------- file d'enregistrement ---------- */
const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

function renderQueue(q) {
  const ul = $("#q-list");
  ul.innerHTML = "";
  $("#q-empty").style.display = q.length ? "none" : "block";
  const ICON = { attente: "⏳", enregistrement: "●", "enregistré": "✓", erreur: "✕" };
  for (const j of q) {
    const li = document.createElement("li");
    li.className = "q-" + j.status.replace("é", "e");
    li.innerHTML = `<span class="q-i"></span><span class="t"></span><span class="q-s"></span>`;
    li.querySelector(".q-i").textContent = ICON[j.status] || "?";
    li.querySelector(".t").textContent = j.title || j.id;
    let s = "";
    if (j.status === "attente") s = "En attente";
    if (j.status === "enregistrement") {
      s = j.needClick
        ? "Clique ▶ dans la fenêtre Suno"
        : j.duration ? `${Math.round(j.progress * 100)} % · reste ${fmt(j.duration * (1 - j.progress))}` : "Démarrage…";
    }
    if (j.status === "enregistré") s = "Enregistré";
    if (j.status === "erreur") { s = "Échec"; li.title = j.error; }
    li.querySelector(".q-s").textContent = s;
    if (j.status === "enregistrement") {
      li.style.setProperty("--p", `${Math.round((j.progress || 0) * 100)}%`);
    }
    ul.appendChild(li);
  }
}

chrome.storage.session.get("atelierQueue").then((r) => renderQueue(r.atelierQueue || []));
chrome.storage.onChanged.addListener((ch, area) => {
  if (area === "session" && ch.atelierQueue) renderQueue(ch.atelierQueue.newValue || []);
});
$("#q-retry").addEventListener("click", () => chrome.runtime.sendMessage({ type: "atelier-queue-retry" }));
$("#q-clear").addEventListener("click", () => chrome.runtime.sendMessage({ type: "atelier-queue-clear" }));
$("#q-cancel").addEventListener("click", () => {
  if (confirm("Arrêter l'enregistrement en cours et vider la file ?")) chrome.runtime.sendMessage({ type: "atelier-queue-cancel" });
});

/* ---------- réglages des boutons sur la page ---------- */
const PAGE_KEY = "atelierPageSettings";
async function loadPageSettings() {
  const s = (await chrome.storage.local.get(PAGE_KEY))[PAGE_KEY] || {};
  $("#set-inline").checked = s.inlineButtons !== false;
  $("#set-popup").checked = s.playPopup !== false;
  $("#dl-cover").checked = !!s.withCover;
}
function savePageSettings() {
  chrome.storage.local.set({
    [PAGE_KEY]: {
      inlineButtons: $("#set-inline").checked,
      playPopup: $("#set-popup").checked,
      withCover: $("#dl-cover").checked
    }
  });
}
["#set-inline", "#set-popup", "#dl-cover"].forEach((s) => $(s).addEventListener("change", savePageSettings));
loadPageSettings();

// Démarrage automatique : permission « debugger » demandée seulement si l'utilisateur coche.
// Chrome affiche alors un bandeau « a commencé le débogage » pendant une fraction de seconde à chaque chanson.
const DBG = { permissions: ["debugger"] };
chrome.permissions.contains(DBG).then((ok) => ($("#set-auto").checked = ok));
$("#set-auto").addEventListener("change", async (e) => {
  if (e.target.checked) {
    e.target.checked = await chrome.permissions.request(DBG).catch(() => false);
    setStatus(e.target.checked ? "Démarrage automatique activé" : "Permission refusée", e.target.checked ? "ok" : "err");
  } else {
    await chrome.permissions.remove(DBG).catch(() => {});
  }
});

/* ---------- init ---------- */
document.body.classList.add("dl-mode");
buildChips();
buildLyrics();
restoreDraft();
