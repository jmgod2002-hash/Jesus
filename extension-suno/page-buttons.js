// Boutons de téléchargement directement sur suno.com :
//  1. un petit bouton ⬇ à côté de chaque titre de chanson ;
//  2. une pop-up en bas à droite quand une chanson se lance.
// Les deux se désactivent dans l'onglet « Télécharger » de l'extension.

(() => {
  if (window.__atelierButtonsLoaded) return;
  window.__atelierButtonsLoaded = true;

  const UUID = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/i;
  const settings = { inlineButtons: true, playPopup: true, withCover: false };

  /* ---------- outils ---------- */
  function titleFor(id) {
    let best = "";
    for (const a of document.querySelectorAll(`a[href*="/song/${id}"]`)) {
      const t = (a.getAttribute("title") || a.textContent || "").trim();
      if (t.length > best.length && t.length < 120) best = t;
    }
    if (!best && location.pathname.includes(id)) {
      best = (document.querySelector("h1")?.textContent || document.title.split("|")[0] || "").trim();
    }
    return best || "Chanson Suno";
  }

  function download(id, audioUrl, btn) {
    const song = { id, title: titleFor(id), audio: audioUrl || "", image: "" };
    if (btn) { btn.textContent = "…"; btn.disabled = true; }
    chrome.runtime.sendMessage(
      { type: "atelier-download", songs: [song], audio: true, cover: settings.withCover, folder: "Suno" },
      (res) => {
        const ok = res && !res.fail;
        if (btn) {
          btn.textContent = ok ? "✓" : "✕";
          btn.title = ok ? "Téléchargé" : (res?.errors?.[0] || "Échec du téléchargement");
          setTimeout(() => { btn.textContent = "⬇"; btn.disabled = false; }, 2500);
        }
      }
    );
  }

  // Empêche le clic de remonter jusqu'à la ligne Suno (qui lancerait la lecture ou changerait de page).
  const block = (el) =>
    ["pointerdown", "mousedown", "mouseup", "click"].forEach((ev) =>
      el.addEventListener(ev, (e) => { e.stopPropagation(); if (ev === "click") e.preventDefault(); })
    );

  /* ---------- 1. boutons à côté des titres ---------- */
  const BTN_STYLE =
    "display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;" +
    "margin-left:6px;padding:0;border:0;border-radius:50%;background:#e8a33d;color:#1a1206;" +
    "font:700 12px/1 system-ui,sans-serif;cursor:pointer;vertical-align:middle;flex-shrink:0;" +
    "opacity:.85;position:relative;z-index:5;";

  function addInlineButtons() {
    if (!settings.inlineButtons) return;
    for (const a of document.querySelectorAll('a[href*="/song/"]:not([data-atelier])')) {
      a.setAttribute("data-atelier", "1");
      const m = a.getAttribute("href").match(UUID);
      // On ne met le bouton qu'à côté du lien qui porte le titre (pas la vignette).
      if (!m || !a.textContent.trim() || a.querySelector("img")) continue;
      const id = m[0].toLowerCase();
      // Un seul bouton par chanson dans un même bloc.
      if (a.parentElement?.querySelector(`.atelier-dl[data-id="${id}"]`)) continue;
      const b = document.createElement("button");
      b.className = "atelier-dl";
      b.dataset.id = id;
      b.type = "button";
      b.textContent = "⬇";
      b.title = "Télécharger le MP3";
      b.style.cssText = BTN_STYLE;
      b.onmouseenter = () => (b.style.opacity = "1");
      b.onmouseleave = () => (b.style.opacity = ".85");
      block(b);
      b.addEventListener("click", () => download(id, "", b));
      a.insertAdjacentElement("afterend", b);
    }
  }

  function removeInlineButtons() {
    document.querySelectorAll(".atelier-dl").forEach((b) => b.remove());
    document.querySelectorAll("a[data-atelier]").forEach((a) => a.removeAttribute("data-atelier"));
  }

  /* ---------- 2. pop-up à la lecture ---------- */
  let host, root, hideTimer, lastShownId;

  function ensurePopup() {
    if (host) return;
    host = document.createElement("div");
    host.style.cssText = "position:fixed;right:20px;bottom:96px;z-index:2147483647;";
    root = host.attachShadow({ mode: "closed" });
    root.innerHTML = `
      <style>
        .box{display:none;align-items:center;gap:10px;max-width:340px;padding:10px 12px;
             background:#15121a;color:#f1ece4;border:1px solid #342d3f;border-radius:10px;
             box-shadow:0 8px 24px rgba(0,0,0,.45);font:13px/1.3 system-ui,sans-serif;
             animation:in .18s ease-out}
        .box.show{display:flex}
        @keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
        .t{flex:1;min-width:0}
        .t small{display:block;color:#a39cae;font-size:11px}
        .t b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
        button{border:0;border-radius:6px;cursor:pointer;font:inherit}
        .go{background:#e8a33d;color:#1a1206;font-weight:700;padding:6px 10px}
        .x{background:none;color:#a39cae;padding:4px 6px;font-size:15px}
      </style>
      <div class="box">
        <div class="t"><small>Atelier Suno</small><b></b></div>
        <button class="go">⬇ Télécharger</button>
        <button class="x" title="Fermer">✕</button>
      </div>`;
    document.documentElement.appendChild(host);
    const box = root.querySelector(".box");
    block(box);
    root.querySelector(".x").addEventListener("click", () => box.classList.remove("show"));
    box.addEventListener("mouseenter", () => clearTimeout(hideTimer));
    box.addEventListener("mouseleave", () => scheduleHide());
  }

  function scheduleHide() {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => root.querySelector(".box").classList.remove("show"), 8000);
  }

  function showPopup(id, src) {
    if (!settings.playPopup) return;
    ensurePopup();
    const box = root.querySelector(".box");
    // Même chanson relancée alors que la pop-up est encore visible : on ne fait rien.
    if (id === lastShownId && box.classList.contains("show")) return;
    lastShownId = id;
    root.querySelector("b").textContent = titleFor(id);
    const go = root.querySelector(".go");
    go.onclick = () => {
      go.textContent = "…";
      chrome.runtime.sendMessage(
        { type: "atelier-download", songs: [{ id, title: titleFor(id), audio: src, image: "" }],
          audio: true, cover: settings.withCover, folder: "Suno" },
        (res) => {
          go.textContent = res && !res.fail ? "✓ Lancé" : "✕ Échec";
          setTimeout(() => (go.textContent = "⬇ Télécharger"), 2500);
        }
      );
    };
    box.classList.add("show");
    scheduleHide();
  }

  document.addEventListener(
    "play",
    (e) => {
      if (e.target?.tagName !== "AUDIO") return;
      const src = e.target.currentSrc || e.target.src || "";
      const m = src.match(UUID) || location.pathname.match(UUID);
      if (m) showPopup(m[0].toLowerCase(), src.match(UUID) ? src : "");
    },
    true
  );

  /* ---------- réglages + surveillance de la page ---------- */
  chrome.storage.local.get("atelierPageSettings", (r) => {
    Object.assign(settings, r.atelierPageSettings || {});
    addInlineButtons();
  });
  chrome.storage.onChanged.addListener((ch) => {
    if (!ch.atelierPageSettings) return;
    Object.assign(settings, ch.atelierPageSettings.newValue || {});
    if (settings.inlineButtons) addInlineButtons(); else removeInlineButtons();
    if (!settings.playPopup && root) root.querySelector(".box").classList.remove("show");
  });

  // Suno charge les chansons au fil du défilement : on rajoute les boutons au fur et à mesure.
  let pending = false;
  new MutationObserver(() => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(() => { pending = false; addInlineButtons(); });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
