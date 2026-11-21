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

  chrome.runtime.onMessage.addListener((msg, _sender, reply) => {
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
