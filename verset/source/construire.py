"""Verset du jour : construit les pages à filmer pour un épisode.

    python3 verset/source/construire.py verset/episodes/psaume-23-4

Lit episode.json et, s'il y en a, les voix ElevenLabs déposées dans voix/ (un fichier par bloc,
nommé comme le bloc : voix/01_accroche.mp3, voix/s5_cta_tiktok.mp3...).
- Avec voix : chaque bloc dure le temps de sa voix, la bouche suit la voix.
- Sans voix (maquette) : durées estimées sur le texte, la bouche bouge par syllabes.

Écrit dans l'épisode :
  pages/long.html, pages/short_youtube.html, pages/short_tiktok.html   (vidéos)
  pages/miniature.html, pages/couverture.html                          (miniature YouTube, couverture Short/TikTok)
  script_elevenlabs.md                                                 (texte à coller dans ElevenLabs, bloc par bloc)
  pages/chapitres.txt                                                  (chapitres YouTube de la vidéo longue)
"""
import os, re, sys, json, random, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "animation/source"))
import decors as D

FPS = 30
INTRO = os.path.join(ROOT, "youtube/intro_1920x1080.mp4")
DECOR = {"feu": ("s1", D.feu_de_camp, D.S1), "chapelle": ("s2", D.chapelle, D.S2), "sommet": ("s3", D.sommet, D.S3), "chambre": ("s4", D.chambre, D.S4)}
FOYER = {sc["id"]: sc["foyer"] for sc in D.SCENES}
LUM = {sc["id"]: sc["lum"] for sc in D.SCENES}
NOM_SVG = open(os.path.join(ROOT, "marque/nom_feu_d_elevation.svg")).read()
NOM_SVG = re.sub(r'fill="#[0-9A-Fa-f]+"', 'fill="currentColor"', NOM_SVG).replace("<svg ", '<svg class="nom" ', 1)
TORCHE_SVG = f'<svg class="torche" viewBox="0 0 486 800" fill="currentColor" fill-rule="evenodd"><path d="{D.torch}"/><path d="{D.flame}"/></svg>'


# ---------------------------------------------------------------- texte → mots, pauses, voix
def pour_voix(texte):
    """Texte à coller dans ElevenLabs : balises gardées, {affiché|prononcé} → prononcé."""
    return re.sub(r"\{([^|}]*)\|([^}]*)\}", r"\2", texte).strip()

def jetons(texte):
    """Liste de ('mot', affiché, prononcé) et ('pause', secondes). Les signes isolés (« » … :) sont collés au mot voisin."""
    out, ouvrant = [], ""
    for m in re.finditer(r"\[([^\]]+)\]|\{([^|}]*)\|([^}]*)\}(\S*)|(\S+)", texte):
        if m.group(1) is not None:
            tag = m.group(1).lower()
            if tag in ("short pause", "pause"): out.append(("pause", 0.45))
            elif tag == "long pause": out.append(("pause", 1.1))
            continue
        aff, dit = (m.group(2) + (m.group(4) or ""), m.group(3)) if m.group(2) is not None else (m.group(5), m.group(5))
        if not re.search(r"\w", aff):              # signe seul
            if aff == "«": ouvrant = "« "; continue
            k = next((i for i in range(len(out) - 1, -1, -1) if out[i][0] == "mot"), None)
            if k is not None:
                prec = out[k]; out[k] = ("mot", prec[1] + " " + aff if aff[0] in "»:;!?" else prec[1] + aff, prec[2])
            continue
        out.append(("mot", ouvrant + aff, dit)); ouvrant = ""
    return out

def pause_ponct(mot):
    m = mot.rstrip(" »")
    if m.endswith("…") or m.endswith("..."): return 0.42
    if m[-1:] in ".!?": return 0.34
    if m[-1:] in ",;:": return 0.14
    return 0.0

def minuter(texte):
    """Temps estimés de chaque mot (débit posé d'une voix ElevenLabs en français)."""
    debit = 10.5 if "[slowly]" in texte else 12.8          # caractères par seconde
    t, mots = 0.0, []
    for j in jetons(texte):
        if j[0] == "pause":
            t += j[1]; continue
        d = (len(re.sub(r"\W", "", j[2])) + 1.5) / debit
        mots.append(dict(t0=t, t1=t + d, txt=j[1], dit=j[2]))
        t += d + pause_ponct(j[1])
    return mots, t


# ---------------------------------------------------------------- sous-titres
# Lisibilité : un groupe reste au moins ~1,8 s (Short) / ~2,2 s (vidéo longue) à l'écran, coupe de préférence
# en fin de phrase ou sur une respiration, et ne dépasse pas une ou deux lignes.
LISIBLE = {True: dict(car=60, mini=2.2), False: dict(car=44, mini=2.4)}

def grouper(mots, long):
    r = LISIBLE[long]
    groupes, cur = [], []
    for i, w in enumerate(mots):
        cur.append(w)
        if i == len(mots) - 1:
            groupes.append(cur); break
        suivant, ecart = mots[i + 1], mots[i + 1]["t0"] - w["t1"]
        texte = " ".join(x["txt"] for x in cur)
        duree, p = w["t1"] - cur[0]["t0"], pause_ponct(w["txt"])
        trop_long = len(texte) + 1 + len(suivant["txt"]) > r["car"]
        if trop_long:
            # plutôt que de couper au milieu d'une phrase, on revient à la dernière ponctuation du groupe
            j = max((k for k in range(len(cur) - 1) if pause_ponct(cur[k]["txt"]) > 0 and cur[k]["t1"] - cur[0]["t0"] >= 0.8), default=None)
            if j is not None:
                groupes.append(cur[: j + 1]); cur = cur[j + 1:]
            else:
                groupes.append(cur); cur = []
        elif ecart > 0.9 or (p >= 0.3 and duree >= r["mini"]) or (p > 0 and duree >= r["mini"] * 1.4):
            groupes.append(cur); cur = []
    # les bouts trop courts (« La peur. ») rejoignent leur voisin s'il reste de la place
    fus = []
    for g in groupes:
        if fus:
            d = g[-1]["t1"] - g[0]["t0"]; dp = fus[-1][-1]["t1"] - fus[-1][0]["t0"]
            place = len(" ".join(x["txt"] for x in fus[-1] + g)) <= r["car"] * 1.15
            if place and (d < r["mini"] * 0.7 or dp < r["mini"] * 0.7) and g[0]["t0"] - fus[-1][-1]["t1"] < 0.9:
                fus[-1] = fus[-1] + g; continue
        fus.append(g)
    return [dict(t0=g[0]["t0"] - 0.05, t1=g[-1]["t1"], mots=[dict(t0=x["t0"], t1=x["t1"], txt=x["txt"]) for x in g]) for g in fus]

def tenir(subs):
    """Pas de clignotement : un groupe reste affiché jusqu'au suivant (si la pause est courte), sinon 0,5 s de plus."""
    subs.sort(key=lambda g: g["t0"])
    for g, n in zip(subs, subs[1:] + [None]):
        fin = g["t1"] + 0.5
        g["t1"] = round(n["t0"] if n and n["t0"] - g["t1"] < 1.2 else fin, 3)
        g["t0"] = round(g["t0"], 3)
    return subs


# ---------------------------------------------------------------- voix (facultative)
def lire_voix(chemin):
    """Durée et enveloppe (100 valeurs/s, 0..1) d'un fichier voix."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", chemin, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    n = len(x) // 80
    rms = np.sqrt((x[: n * 80].reshape(n, 80) ** 2).mean(axis=1) + 1e-9)
    db = 20 * np.log10(rms)
    env = np.clip((db + 46) / 30, 0, 1)
    parle = np.where(env > 0.15)[0]
    debut, fin = (parle[0] / 100, parle[-1] / 100) if len(parle) else (0, n / 100)
    return len(x) / 8000, env, debut, fin

def silences(env, d0, d1, seuil=0.12, mini=0.15):
    """Milieux des silences (en s) d'au moins `mini` s entre le début et la fin de la parole."""
    bas = env < seuil
    out, i, n = [], int(d0 * 100), int(d1 * 100)
    while i < n:
        if bas[i]:
            j = i
            while j < n and bas[j]: j += 1
            if (j - i) / 100 >= mini: out.append((i + j) / 200)
            i = j
        else:
            i += 1
    return out

def caler(mots, env, d0, d1):
    """Place les mots estimés sur la vraie voix : les grandes pauses du texte sont accrochées aux silences
    réellement entendus (alignement ordonné), interpolation linéaire entre ces points d'ancrage."""
    e0, e1 = mots[0]["t0"], mots[-1]["t1"]
    coupures = [(mots[i]["t1"] + mots[i + 1]["t0"]) / 2 for i in range(len(mots) - 1) if mots[i + 1]["t0"] - mots[i]["t1"] >= 0.25]
    reels = silences(env, d0, d1)
    pe = [(c - e0) / (e1 - e0) for c in coupures]
    pr = [(c - d0) / (d1 - d0) for c in reels]
    # alignement monotone qui maximise le nombre de paires proches (programmation dynamique)
    n, m, tol = len(pe), len(pr), 0.07
    best = np.zeros((n + 1, m + 1), dtype=int)
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            best[i, j] = max(best[i + 1, j], best[i, j + 1], (1 + best[i + 1, j + 1]) if abs(pe[i] - pr[j]) < tol else -1)
    ancres, i, j = [(e0, d0)], 0, 0
    while i < n and j < m:
        if abs(pe[i] - pr[j]) < tol and best[i, j] == 1 + best[i + 1, j + 1]:
            ancres.append((coupures[i], reels[j])); i += 1; j += 1
        elif best[i + 1, j] >= best[i, j + 1]: i += 1
        else: j += 1
    ancres.append((e1, d1))
    xe, xr = np.array([a for a, _ in ancres]), np.array([b for _, b in ancres])
    for w in mots:
        w["t0"], w["t1"] = float(np.interp(w["t0"], xe, xr)), float(np.interp(w["t1"], xe, xr))
    return len(ancres) - 2, len(coupures)

def chercher_voix(ep_dir, bid, vitesse=1.0):
    """Fichier voix du bloc. Si vitesse < 1, version ralentie (même hauteur de voix, étirement Rubber Band)
    mise en cache dans renders/voix_lente/ ; le fichier d'origine n'est jamais modifié."""
    for ext in (".mp3", ".wav", ".m4a"):
        p = os.path.join(ep_dir, "voix", bid + ext)
        if os.path.exists(p): break
    else:
        return None
    if abs(vitesse - 1) < 0.005:
        return p
    lent = os.path.join(ep_dir, "renders", "voix_lente", f"{bid}_{vitesse:.2f}.wav")
    if not os.path.exists(lent) or os.path.getmtime(lent) < os.path.getmtime(p):
        os.makedirs(os.path.dirname(lent), exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-af", f"rubberband=tempo={vitesse}:formant=preserved:pitchq=quality",
                        "-ar", "48000", "-c:a", "pcm_s16le", lent], check=True)
    return lent


# ---------------------------------------------------------------- timeline d'un format
def timeline(ep, ep_dir, fmt):
    long = fmt == "long"
    if long:
        blocs = ep["long"]["blocs"]
    else:
        blocs = ep["short"]["blocs"] + [ep["short"]["cta"]["youtube" if fmt == "short_youtube" else "tiktok"]]
    rnd = random.Random(7)
    t, segs, subs, cartes, syl, paroles, voix, intro = 0.0, [], [], [], [], [], [], None
    env_global = []
    chapitres = [b for b in blocs if b.get("chapitre")]
    for b in blocs:
        mots, est = minuter(b["texte"])
        chemin = chercher_voix(ep_dir, b["id"], b.get("vitesse", ep.get("vitesse_voix", 1.0)))
        if chemin:
            duree, env, d0, d1 = lire_voix(chemin)
            calees, pauses = caler(mots, env, d0, d1)
            print(f"   {b['id']:16s} voix {duree:5.1f} s · {calees}/{pauses} pauses du texte calées sur la voix")
            parlee = duree
            voix.append(dict(id=b["id"], fichier=os.path.relpath(chemin, ep_dir), debut=round(t, 3)))
        else:
            env, parlee = None, est
        fin_pause = b.get("fin_pause", ep.get("respiration", 0.45))
        duree_bloc = max(parlee + fin_pause, b.get("duree_min", 0))
        t0 = t
        # enveloppe globale (100/s) : -1 là où il n'y a pas de vraie voix
        env_global += [-1] * (int(round(t0 * 100)) - len(env_global))
        if env is not None:
            env_global += [round(float(v), 2) for v in env]
        for m in mots:
            m["t0"] = round(t0 + m["t0"], 3); m["t1"] = round(t0 + m["t1"], 3)
        # syllables (maquette) et plages de parole
        if env is None:
            for m in mots:
                n = max(1, round(len(re.sub(r"\W", "", m["dit"])) / 3.2)); d = (m["t1"] - m["t0"]) / n
                for i in range(n):
                    syl.append([round(m["t0"] + i * d, 3), round(d * 0.88, 3), round(0.4 + rnd.random() * 0.6, 2)])
        for m in mots:
            if paroles and m["t0"] - paroles[-1][1] < 0.3: paroles[-1][1] = m["t1"]
            else: paroles.append([m["t0"], m["t1"]])
        # sous-titres par groupes de mots (pas pendant la carte du verset : le verset s'écrit dans la carte)
        if not b.get("carte_verset"):
            subs += grouper(mots, long)
        # cartes déclenchées par une phrase du texte
        norme = lambda s: re.sub(r"[^\w ]", "", s.lower()).strip()
        for c in b.get("cartes", []):
            cible = norme(c["declencheur"])
            for i in range(len(mots)):
                if norme(" ".join(x["txt"] for x in mots[i:i + 8])).startswith(cible):
                    c0 = mots[i]["t0"] - 0.2
                    cartes.append(dict(c, t0=round(c0, 3), t1=round(min(c0 + c["duree"], t0 + duree_bloc - 0.2), 3))); break
            else:
                raise SystemExit(f"déclencheur introuvable dans {b['id']} : {c['declencheur']}")
        seg = dict(id=b["id"], t0=round(t0, 3), t1=round(t0 + duree_bloc, 3), decor=DECOR[b["decor"]][0], plan=b["plan"],
                   chapitre=b.get("chapitre"), cta=b.get("cta"), commentaire=b.get("commentaire"), fin=b.get("fin", False),
                   carte_verset=b.get("carte_verset"))
        if b.get("chapitre"):
            seg["chapitre_n"] = chapitres.index(b) + 1; seg["chapitres"] = len(chapitres)
        if b.get("carte_verset"):
            officiel = []
            for w in (ep["verset"] if b["carte_verset"] == "long" else ep["verset_court"]).split():
                if re.search(r"\w", w) or not officiel: officiel.append(w)
                else: officiel[-1] += " " + w          # « : » ou « ; » isolés restent collés au mot précédent
            seg["mots"] = [dict(t0=mots[min(i, len(mots) - 1)]["t0"], txt=w) for i, w in enumerate(officiel)]
        if b["plan"] == "alterne":
            # multicaméra : on change de plan au début d'une phrase, au plus toutes les 7 s ; plan large pendant les cartes
            coupes, plan, dernier = [[round(t0, 3), "large"]], "large", t0
            for g in [x for x in subs if x["t0"] >= t0]:
                carte = any(c["t0"] - 0.5 <= g["t0"] <= c["t1"] for c in cartes)
                voulu = "large" if carte else ("serre" if plan == "large" else "large")
                if voulu != plan and (g["t0"] - dernier >= 7 or carte):
                    coupes.append([g["t0"], voulu]); plan, dernier = voulu, g["t0"]
            seg["coupes"] = coupes
        segs.append(seg)
        t = t0 + duree_bloc
        if long and b["id"] == ep["long"]["intro_apres"]:
            intro = dict(t0=round(t, 3), t1=round(t + 6.0, 3))
            t += 6.0
    # clignements toutes les 2,3 à 5 s
    clins, c = [], 1.2
    while c < t:
        clins.append(round(c, 2)); c += 2.3 + rnd.random() * 2.7
    has_voice = any(v >= 0 for v in env_global)
    return dict(dur=round(t, 3), segments=segs, soustitres=tenir(subs), cartes=cartes, intro=intro, voix=voix,
                piste=dict(syl=syl, paroles=paroles, clins=clins, env=env_global if has_voice else None))


# ---------------------------------------------------------------- scène SVG commune (4 décors + personnage)
def scene_svg(w, h, vue):
    random.seed(1)
    defs, fonds, devants = [D.P.DEFS[6:-7], D.TQ.DEFS_TQ[6:-7], D.DEFS_COMMUNS], [], []
    for sid in ("s1", "s2", "s3", "s4"):
        defs.append(D.filtre_perso(f"f_{sid}", *LUM[sid]))
    for nom, (sid, fn, _) in DECOR.items():
        d, b, f = fn()
        defs.append(d)
        fonds.append(f'<g id="{sid}_fond" display="none">{b}</g>')
        devants.append(f'<g id="{sid}_devant" display="none">{f}</g>')
    return (f'<svg id="s" xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vue}" preserveAspectRatio="xMidYMid slice">'
            f'<defs>{"".join(defs)}</defs><g id="cam"><g id="fonds">{"".join(fonds)}</g>'
            f'<g id="perso_pos"><g id="perso_lum">{D.rig()}</g></g><g id="devants">{"".join(devants)}</g></g></svg>')

def decors_config():
    out = {}
    for nom, (sid, _, pl) in DECOR.items():
        out[sid] = dict(pl, foyer=FOYER[sid], tete=[round(pl["tx"] + pl["s"] * 340), round(pl["ty"] + pl["s"] * 300)])
    return out


STYLE = """
@font-face{font-family:"InterT";src:url(../../../fonts/intertight-800-900.woff2) format("woff2");font-weight:800 900}
@font-face{font-family:"InterB";src:url(../../../../intro/fonts/inter-500.woff2) format("woff2")}
@font-face{font-family:"FrauncesB";src:url(../../../../intro/fonts/fraunces-700.woff2) format("woff2")}
:root{--braise:#C0522B;--or:#FFB46A;--creme:#FFF6E8;--nuit:#120A06}
html,body{margin:0;background:#000}
#stage{position:relative;overflow:hidden;background:#000}
#stage>*{position:absolute}
svg#s{left:0;top:0;display:block}
.couche{left:0;top:0;width:100%;height:100%;pointer-events:none}
#vig{background:radial-gradient(ellipse 75% 75% at 50% 50%,transparent 60%,rgba(0,0,0,.5))}
.nom{display:block;color:var(--creme)}
#marque{opacity:.92}
#noir{background:#000;opacity:0}
.inter{font-family:"InterB",Arial,sans-serif}
.fort{font-family:"InterT","InterB",Arial,sans-serif;font-weight:900}
.serif{font-family:"FrauncesB",Georgia,serif}
/* sous-titres */
#st{left:0;right:0;text-align:center}
#st span.m{display:inline-block;margin:0 .09em;transform-origin:50% 60%}
/* cartes */
.carte{opacity:0;color:var(--creme);background:rgba(18,10,6,.84);border:2px solid rgba(255,180,106,.35);border-radius:22px;box-shadow:0 20px 60px rgba(0,0,0,.45)}
.carte .ref{font-family:"InterB",Arial,sans-serif;color:var(--or);letter-spacing:.25em;text-transform:uppercase}
.carte .src{font-family:"InterB",Arial,sans-serif;color:#D9C8B4}
#cv .v span{opacity:.18}
#cv .v span.on{opacity:1}
#chap{opacity:0;background:rgba(18,10,6,.78);border:2px solid rgba(255,180,106,.35);border-radius:16px;color:var(--creme)}
#chap .n{font-family:"InterB",Arial,sans-serif;color:var(--or);letter-spacing:.25em}
#chap .t{font-family:"FrauncesB",Georgia,serif}
/* appel à l'action */
#cta{opacity:0;left:0;right:0;text-align:center}
#cta .bouton{display:inline-flex;align-items:center;gap:.45em;border-radius:999px;padding:.42em 1.1em;font-family:"InterT",Arial,sans-serif;font-weight:900;letter-spacing:.02em;color:#fff;box-shadow:0 10px 40px rgba(0,0,0,.45)}
#cta .bouton.youtube{background:#E1251B}
#cta .bouton.tiktok{background:var(--braise)}
#cta .bouton.fait{background:#5A5450}
#cta .cloche{display:inline-block;transform-origin:50% 10%}
#cta .sur{font-family:"InterT",Arial,sans-serif;font-weight:800;color:var(--creme);text-shadow:0 4px 18px rgba(0,0,0,.6);margin-bottom:.35em}
#com{opacity:0;background:var(--creme);color:#2A1A10;border-radius:22px;font-family:"InterT",Arial,sans-serif;font-weight:800;box-shadow:0 12px 40px rgba(0,0,0,.45)}
/* écran de fin */
#fin{opacity:0}
#fin .zone{position:absolute;border:3px dashed rgba(255,246,232,.55);border-radius:18px;background:rgba(18,10,6,.35)}
#fin .zone.rond{border-radius:50%}
#fin .lab{position:absolute;font-family:"InterB",Arial,sans-serif;color:rgba(255,246,232,.75);letter-spacing:.2em;text-transform:uppercase;font-size:20px}
"""


def accroche_html(txt):
    """« SI TU AS PEUR|CE SOIR… » : | = retour à la ligne, la dernière ligne en or."""
    lignes = txt.split("|")
    return "<br>".join(lignes[:-1] + [f'<span style="color:#FFB46A">{lignes[-1]}</span>']) if len(lignes) > 1 else txt


def page_video(ep, ep_dir, fmt):
    tl = timeline(ep, ep_dir, fmt)
    vertical = fmt != "long"
    w, h = (1080, 1920) if vertical else (1920, 1080)
    vue = "305 0 608 1080" if vertical else "0 0 1920 1080"
    cfg = dict(format=fmt, w=w, h=h, fps=FPS, vertical=vertical, decors=decors_config(),
               textes=dict(reference=ep["reference"], reference_courte=ep["reference_courte"], traduction=ep["traduction"],
                           verset=ep["verset"], verset_court=ep["verset_court"], accroche=ep["short"].get("accroche", "")), **tl)
    if vertical:
        over = f"""
<div id="vig" class="couche"></div>
<div id="haut" class="couche" style="background:linear-gradient(rgba(0,0,0,.55),transparent 22%,transparent 70%,rgba(0,0,0,.45))"></div>
<div id="barre" style="left:0;top:0;height:10px;width:0;background:var(--braise)"></div>
<div id="marque" style="left:0;right:0;top:64px;display:flex;justify-content:center"><div style="width:250px">{NOM_SVG}</div></div>
<div id="puce" class="inter" style="left:0;right:0;top:132px;text-align:center"><span style="background:rgba(18,10,6,.75);color:var(--or);border:2px solid rgba(255,180,106,.4);border-radius:999px;padding:10px 26px;font-size:30px;letter-spacing:.22em">{ep["reference_courte"]}</span></div>
<div id="acc" class="fort" style="left:70px;right:70px;top:200px;text-align:center;font-size:96px;line-height:1.02;color:var(--creme);text-transform:uppercase;text-shadow:0 8px 40px rgba(0,0,0,.6);opacity:0">{accroche_html(cfg["textes"]["accroche"])}</div>
<div id="voile" class="couche" style="background:rgba(10,6,4,.62);opacity:0"></div>
<div id="cv" class="carte" style="left:60px;right:60px;top:520px;padding:44px 48px"><div class="ref" style="font-size:28px;margin-bottom:22px">{ep["reference_courte"]}</div><div class="v serif" style="font-size:62px;line-height:1.18"></div><div class="src" style="font-size:24px;margin-top:22px">{ep["traduction"]}</div></div>
<div id="carte" class="carte" style="left:70px;right:70px;top:280px;padding:40px 44px;text-align:center"></div>
<div id="st" class="fort" style="top:1090px;padding:0 50px;font-size:64px;line-height:1.12;color:#fff;text-transform:uppercase;-webkit-text-stroke:3px rgba(0,0,0,.85);paint-order:stroke fill;text-shadow:0 8px 30px rgba(0,0,0,.55)"></div>
<div id="com" style="left:120px;right:120px;top:215px;padding:30px 36px;font-size:46px;text-align:center"></div>
<div id="cta" style="top:1290px;font-size:60px"></div>
<div id="noir" class="couche"></div>"""
    else:
        over = f"""
<div id="vig" class="couche"></div>
<div id="marque" style="right:44px;top:34px;width:290px">{NOM_SVG}</div>
<div id="chap" style="left:56px;top:56px;padding:22px 30px"><div class="n" style="font-size:18px"></div><div class="t" style="font-size:40px;margin-top:6px"></div></div>
<div id="voile" class="couche" style="background:rgba(10,6,4,.62);opacity:0"></div>
<div id="cv" class="carte" style="left:230px;right:230px;top:250px;padding:50px 64px;text-align:center"><div class="ref" style="font-size:24px;margin-bottom:26px">{ep["reference_courte"]}</div><div class="v serif" style="font-size:58px;line-height:1.22"></div><div class="src" style="font-size:22px;margin-top:26px">{ep["traduction"]}</div></div>
<div id="carte" class="carte" style="right:60px;top:240px;width:640px;padding:36px 40px;text-align:center"></div>
<div id="st" class="inter" style="bottom:60px;padding:0 260px;font-size:40px;line-height:1.3;color:#fff"></div>
<div id="com" style="right:150px;top:230px;width:560px;padding:26px 34px;font-size:38px;text-align:center"></div>
<div id="cta" style="right:110px;left:auto;width:700px;bottom:330px;font-size:46px"></div>
<div id="fin" class="couche">
  <div style="position:absolute;right:0;top:0;bottom:0;width:900px;background:linear-gradient(90deg,transparent,rgba(10,6,4,.78) 18%)"></div>
  <div class="serif" style="position:absolute;right:120px;top:120px;width:700px;color:var(--creme);font-size:56px;line-height:1.1">À demain pour<br>un nouveau verset</div>
  <div class="zone" style="right:120px;top:300px;width:700px;height:394px"></div><div class="lab" style="right:120px;top:710px;width:700px;text-align:center">vidéo suivante (YouTube Studio)</div>
  <div class="zone rond" style="right:430px;top:790px;width:200px;height:200px"></div><div class="lab" style="right:120px;top:880px;width:280px">s'abonner</div>
</div>
<div id="noir" class="couche"></div>"""
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{ep["reference"]} · {fmt}</title><style>{STYLE}</style></head><body>
<!-- Fichier généré par verset/source/construire.py : ne pas modifier à la main. -->
<div id="stage" style="width:{w}px;height:{h}px">{scene_svg(w, h, vue)}{over}</div>
<script>window.CONFIG={json.dumps(cfg, ensure_ascii=False, separators=(",", ":"))};</script>
<script src="../../../../animation/moteur.js"></script>
<script src="../../../scene.js"></script>
</body></html>"""
    return html, tl


def page_image(ep, kind):
    """Miniature YouTube (1280x720) ou couverture Short/TikTok (1080x1920) : personnage seul, éclairé, sur le cercle braise."""
    random.seed(1)
    perso = (f'<svg class="perso" viewBox="40 20 640 990" xmlns="http://www.w3.org/2000/svg"><defs>{D.P.DEFS[6:-7]}{D.TQ.DEFS_TQ[6:-7]}'
             f'{D.filtre_perso("f_img", (1, .93, .86), ((-10, "#FFB050", .85), (9, "#FFD9A0", .35)))}</defs>'
             f'<g id="perso_lum" filter="url(#f_img)">{D.rig()}</g></svg>')
    fond = ("background:radial-gradient(ellipse 55% 70% at 18% 95%,rgba(192,82,43,.75),transparent 70%),"
            "radial-gradient(ellipse 45% 55% at 52% 0%,rgba(232,137,60,.45),transparent 70%),"
            "radial-gradient(ellipse 60% 80% at 85% 60%,rgba(255,243,224,.10),transparent 70%),linear-gradient(160deg,#24140A 0%,#120A05 60%,#1E110A 100%)")
    etoiles = "".join(f'<i style="position:absolute;left:{random.uniform(0, 100):.1f}%;top:{random.uniform(0, 55):.1f}%;width:{random.choice([2, 2, 3, 4])}px;height:{random.choice([2, 2, 3, 4])}px;border-radius:50%;background:#FFF3DC;opacity:{random.uniform(.25, .8):.2f}"></i>' for _ in range(70))
    if kind == "miniature":
        w, h = 1280, 720
        corps = f"""
<div class="etoiles">{etoiles}</div>
<div style="position:absolute;width:540px;height:540px;border-radius:50%;right:60px;top:70px;background:radial-gradient(circle at 40% 35%,#F7B46C,#E07A3A 55%,#C0522B 100%);box-shadow:0 0 120px rgba(232,137,60,.55)"></div>
<div style="position:absolute;right:20px;bottom:-150px;width:560px">{perso}</div>
<div class="fort" style="position:absolute;left:60px;top:120px;width:700px;color:var(--creme);font-size:132px;line-height:.9;text-transform:uppercase;letter-spacing:-.01em;text-shadow:0 6px 30px rgba(0,0,0,.45)">Tu n'es<br>pas <span style="color:#FFB46A">seul</span></div>
<div class="fort" style="position:absolute;left:62px;top:400px;background:var(--braise);color:var(--creme);font-weight:800;font-size:34px;letter-spacing:.04em;padding:10px 26px;border-radius:999px;text-transform:uppercase">Psaume 23 · 4</div>
<div class="inter" style="position:absolute;left:66px;top:486px;color:#E9D8C2;font-size:28px">quand tu as peur la nuit</div>
<div style="position:absolute;right:34px;top:26px;height:70px;width:43px;color:var(--creme)">{TORCHE_SVG}</div>"""
    else:
        w, h = 1080, 1920
        corps = f"""
<div class="etoiles">{etoiles}</div>
<div style="position:absolute;width:900px;height:900px;border-radius:50%;left:90px;top:860px;background:radial-gradient(circle at 40% 35%,#F7B46C,#E07A3A 55%,#C0522B 100%);box-shadow:0 0 160px rgba(232,137,60,.55)"></div>
<div style="position:absolute;left:150px;bottom:-200px;width:800px">{perso}</div>
<div style="position:absolute;left:0;right:0;top:110px;display:flex;justify-content:center"><div style="width:300px;color:var(--creme)">{NOM_SVG}</div></div>
<div class="fort" style="position:absolute;left:60px;right:60px;top:250px;text-align:center;color:var(--creme);font-size:128px;line-height:.95;text-transform:uppercase;text-shadow:0 8px 40px rgba(0,0,0,.5)">Si tu as peur <span style="color:#FFB46A">ce soir…</span></div>
<div style="position:absolute;left:0;right:0;top:680px;text-align:center"><span class="fort" style="background:var(--braise);color:var(--creme);font-weight:800;font-size:44px;letter-spacing:.05em;padding:12px 34px;border-radius:999px">PSAUME 23 · 4</span></div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{kind}</title><style>{STYLE}
#m{{position:relative;width:{w}px;height:{h}px;overflow:hidden;{fond}}}
.etoiles{{position:absolute;inset:0}}
.perso{{display:block;width:100%;height:auto;filter:drop-shadow(0 20px 40px rgba(0,0,0,.45))}}
.torche{{width:100%;height:100%}}
</style></head><body><div id="m">{corps}</div>
<script src="../../../../animation/moteur.js"></script>
<script>bouche(0.42); set($('sourcils'),'transform','translate(0 -6)'); window.ready=document.fonts.ready;</script>
</body></html>"""


def script_md(ep):
    L = [f"# Script ElevenLabs — {ep['reference']}", "",
         "Un fichier audio par bloc, nommé exactement comme le bloc, déposé dans `voix/` de l'épisode",
         "(ex. `voix/01_accroche.mp3`). Ensuite : `python3 verset/source/construire.py <épisode>` puis `node verset/render.js <épisode>`.", "",
         "Réglages : voir `verset/GUIDE_SON.md`. Les balises entre crochets se collent telles quelles (modèle Eleven v3).", ""]
    for titre, blocs in (("Vidéo longue YouTube", ep["long"]["blocs"]),
                         ("Short (commun YouTube + TikTok)", ep["short"]["blocs"]),
                         ("Fin du Short — version YouTube", [ep["short"]["cta"]["youtube"]]),
                         ("Fin du Short — version TikTok", [ep["short"]["cta"]["tiktok"]])):
        L += [f"## {titre}", ""]
        for b in blocs:
            L += [f"### `{b['id']}`", "", "```", pour_voix(b["texte"]), "```", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- kit de montage (MK Cut, CapCut, Premiere…)
def tc_srt(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s_:02d},{ms:03d}"

def kit_montage(ep, ep_dir, fmt, tl):
    """montage/<format>/ : sous_titres.srt + timeline.json (blocs, textes à l'écran, pistes). Les pistes elles-mêmes
    (fond.mp4 sans texte, voix.m4a, musique.m4a, intro.m4a) sont produites par render.js --fond / --pistes."""
    d = os.path.join(ep_dir, "montage", fmt); os.makedirs(d, exist_ok=True)
    srt = "".join(f"{i}\n{tc_srt(g['t0'])} --> {tc_srt(g['t1'])}\n{' '.join(m['txt'] for m in g['mots'])}\n\n" for i, g in enumerate(tl["soustitres"], 1))
    open(os.path.join(d, "sous_titres.srt"), "w").write(srt)
    r = lambda x: round(x, 3)
    textes = []
    for s_ in tl["segments"]:
        if s_.get("carte_verset"):
            textes.append(dict(type="verset", debut=r(s_["t0"]), fin=r(s_["t1"]), reference=ep["reference"], traduction=ep["traduction"],
                               texte=ep["verset"] if s_["carte_verset"] == "long" else ep["verset_court"], mots=[dict(t=r(m["t0"]), texte=m["txt"]) for m in s_["mots"]]))
        if s_.get("chapitre"):
            textes.append(dict(type="chapitre", debut=r(s_["t0"] + 0.3), fin=r(s_["t0"] + 4.0), numero=s_["chapitre_n"], total=s_["chapitres"], titre=s_["chapitre"]))
        if s_.get("cta"):
            textes.append(dict(type="abonnement", debut=r(s_["t0"] + 0.2), fin=r(s_["t1"] - 0.1), plateforme=s_["cta"], texte="Un verset par jour", clic=r(s_["t0"] + 1.7)))
        if s_.get("commentaire"):
            textes.append(dict(type="commentaire", debut=r(s_["t0"] + 0.42 * (s_["t1"] - s_["t0"])), fin=r(s_["t1"] - 0.1), texte=f"Écris en commentaire : « {s_['commentaire']} »"))
        if s_.get("fin"):
            textes.append(dict(type="ecran_de_fin", debut=r(s_["t0"] + 0.3), fin=r(s_["t1"]), texte="À demain pour un nouveau verset", note="éléments YouTube (vidéo suivante + s'abonner) à poser dans YouTube Studio, à droite"))
    for c in tl["cartes"]:
        textes.append(dict({k: v for k, v in c.items() if k not in ("t0", "t1", "declencheur", "duree")}, debut=r(c["t0"]), fin=r(c["t1"])))
    if fmt != "long":
        s0 = tl["segments"][0]
        textes.append(dict(type="accroche", debut=0.0, fin=r(s0["t1"]), texte=ep["short"]["accroche"].replace("|", " ")))
        textes.append(dict(type="reference", debut=r(s0["t1"]), fin=r(tl["dur"]), texte=ep["reference_courte"]))
    textes.sort(key=lambda x: x["debut"])
    tlj = dict(
        format=fmt, largeur=1920 if fmt == "long" else 1080, hauteur=1080 if fmt == "long" else 1920, fps=FPS, duree=r(tl["dur"]),
        unite="secondes depuis le début de la vidéo finale",
        pistes=dict(video_sans_texte="fond.mp4", voix="voix.m4a", musique="musique.m4a (déjà baissée sous la voix)",
                    intro_son="intro.m4a" if tl["intro"] else None, sous_titres="sous_titres.srt",
                    video_complete=f"../../rendu/{ep['id']}_{dict(long='youtube_long', short_youtube='youtube_short', short_tiktok='tiktok')[fmt]}.mp4"),
        intro=dict(debut=r(tl["intro"]["t0"]), fin=r(tl["intro"]["t1"]), fichier="youtube/intro_1920x1080.mp4", note="déjà incluse dans fond.mp4") if tl["intro"] else None,
        blocs=[dict(id=s_["id"], debut=r(s_["t0"]), fin=r(s_["t1"]), decor={"s1": "feu de camp", "s2": "chapelle", "s3": "sommet", "s4": "chambre"}[s_["decor"]],
                    plan=s_["plan"], chapitre=s_.get("chapitre")) for s_ in tl["segments"]],
        voix=[dict(bloc=v["id"], debut=v["debut"], fichier_original=f"voix/{v['id']}.mp3") for v in tl["voix"]],
        textes_a_l_ecran=textes,
        sous_titres=[dict(debut=r(g["t0"]), fin=r(g["t1"]), texte=" ".join(m["txt"] for m in g["mots"]), mots=[dict(debut=r(m["t0"]), fin=r(m["t1"]), texte=m["txt"]) for m in g["mots"]]) for g in tl["soustitres"]],
    )
    json.dump(tlj, open(os.path.join(d, "timeline.json"), "w"), ensure_ascii=False, indent=1)


def main(ep_dir):
    ep_dir = os.path.abspath(ep_dir)
    ep = json.load(open(os.path.join(ep_dir, "episode.json")))
    pages = os.path.join(ep_dir, "pages"); os.makedirs(pages, exist_ok=True)
    for fmt in ("long", "short_youtube", "short_tiktok"):
        html, tl = page_video(ep, ep_dir, fmt)
        open(os.path.join(pages, f"{fmt}.html"), "w").write(html)
        kit_montage(ep, ep_dir, fmt, tl)
        mode = "voix" if tl["piste"]["env"] else "maquette (sans voix)"
        print(f"{fmt:14s} {tl['dur']:7.1f} s  {len(tl['segments'])} blocs  {mode}")
        if fmt == "long":
            ch, lignes = 0, []
            for s in tl["segments"]:
                if s["id"] == "02_bienvenue": lignes.append((s["t0"], "Introduction"))
                if s.get("chapitre"): lignes.append((s["t0"], s["chapitre"]))
                if s["id"] == "03_verset": lignes.append((s["t0"], f"Le verset : {ep['reference']}"))
            txt = "0:00 " + ep["reference"] + " : le verset à lire quand tu as peur\n" + "".join(f"{int(t // 60)}:{int(t % 60):02d} {n}\n" for t, n in lignes)
            open(os.path.join(pages, "chapitres.txt"), "w").write(txt)
    for kind in ("miniature", "couverture"):
        open(os.path.join(pages, f"{kind}.html"), "w").write(page_image(ep, kind))
    open(os.path.join(ep_dir, "script_elevenlabs.md"), "w").write(script_md(ep))
    print("pages →", pages)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "verset/episodes/psaume-23-4"))
