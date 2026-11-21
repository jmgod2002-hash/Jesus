"""Animation : le présentateur Feu d'Élévation dans quatre décors hors studio.

Génère animation/index.html (une seule image SVG 1920 x 1080 + animation/anim.js).
Le rendu vidéo se fait ensuite avec : node animation/render.js

- Un seul personnage articulé, tiré de trois_quarts.py (même dessin) : tête, sourcils,
  paupières, bouche, buste qui respire, pied qui se balance.
- Quatre décors, chacun avec sa lumière sur le personnage (teinte + liserés de couleur).
"""
import os, re, sys, json, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "personnage/source"))
import personnage as P
import trois_quarts as TQ
from personnage import K, L

torch, flame = P.logo_parts()
NOM_D = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, "marque/nom_feu_d_elevation.svg")).read()).group(1)
FLAMME = "M0 0 C-0.42 0 -0.56 -0.28 -0.4 -0.5 C-0.28 -0.68 -0.1 -0.78 0 -1 C0.08 -0.8 0.3 -0.66 0.4 -0.46 C0.54 -0.24 0.38 0 0 0 Z"
DUREE_SCENE = 5.0


# ---------------------------------------------------------------- personnage articulé
def rig():
    P._n[0] = 0
    legs, torso, arms, H = TQ.legs(), TQ.torso(), TQ.arms(), TQ.head()
    assert len(legs) == 5 and len(H) == 32, "trois_quarts.py a changé : revoir le découpage du personnage"

    def oeil(parts, cx, cy, rx, n):
        clip, blanc, iris, contour, cil = parts
        paupiere = (f'<clipPath id="pau_{n}"><ellipse cx="{cx}" cy="{cy}" rx="{rx+4}" ry="38"/></clipPath>'
                    f'<g id="paup_{n}" clip-path="url(#pau_{n})" display="none">'
                    f'<rect id="paupr_{n}" x="{cx-rx-6}" y="{cy-40}" width="{2*rx+12}" height="0" fill="{K["skin"]}"/>'
                    f'<path id="paupl_{n}" d="M{cx-rx-6} {cy-40} L{cx+rx+6} {cy-40}" stroke="{K["skinS"]}" stroke-width="3"/></g>')
        return clip + blanc + iris + contour + paupiere + f'<g id="cil_{n}">{cil}</g>'

    bouche = ('<clipPath id="bouche_clip"><path id="bouche_cp" d="M314 386 Z"/></clipPath>'
              '<g id="bouche"><path id="bouche_int" d="M314 386 Z" fill="#4A1A10"/>'
              '<g clip-path="url(#bouche_clip)"><ellipse id="langue" cx="345" cy="404" rx="22" ry="10" fill="#C9604C"/>'
              '<path id="dents" d="M314 386 Z" fill="#FFF8EE"/></g>'
              f'<path id="bouche_ln" d="M314 386 C330 400 356 400 376 384" fill="none" stroke="{L}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
              + H[31] + '</g>')
    tete = ('<g id="tete">' + "".join(H[0:5]) + '<g id="sourcils">' + H[5] + H[6] + '</g>'
            + oeil(H[7:12], 282, 292, 28, "g") + oeil(H[12:17], 398, 290, 21, "d")
            + "".join(H[17:30]) + bouche + '</g>')
    jambes = '<g id="jambes">' + legs[0] + legs[1] + '<g id="pied">' + legs[2] + legs[3] + '</g>' + legs[4] + '</g>'
    buste = '<g id="buste">' + "".join(torso) + "".join(arms) + '</g>'
    return jambes + buste + tete


def filtre_perso(fid, teinte, liseres):
    """Lumière du décor sur le personnage : teinte globale + liserés (dx > 0 : lumière venant de la gauche)."""
    r, g, b = teinte
    s = (f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1100" height="1400">'
         f'<feColorMatrix type="matrix" values="{r} 0 0 0 0  0 {g} 0 0 0  0 0 {b} 0 0  0 0 0 1 0" result="tinte"/>')
    dernier = "tinte"
    for k, (dx, couleur, op) in enumerate(liseres):
        s += (f'<feOffset in="SourceAlpha" dx="{dx}" dy="-2" result="o{k}"/>'
              f'<feComposite in="SourceAlpha" in2="o{k}" operator="out" result="b{k}"/>'
              f'<feGaussianBlur in="b{k}" stdDeviation="2.6" result="f{k}"/>'
              f'<feFlood id="{fid}_r{k}" flood-color="{couleur}" flood-opacity="{op}"/>'
              f'<feComposite in2="f{k}" operator="in" result="c{k}"/>'
              f'<feComposite in="c{k}" in2="SourceAlpha" operator="in" result="d{k}"/>'
              f'<feBlend in="d{k}" in2="{dernier}" mode="screen" result="l{k}"/>')
        dernier = f"l{k}"
    return s + '</filter>'


def flou(fid, sd):
    return f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2720" height="1880"><feGaussianBlur stdDeviation="{sd}"/></filter>'


DEFS_COMMUNS = "".join(flou(f"d_b{n}", n) for n in (2, 3, 4, 6, 10, 16, 24, 40, 70)) + '''
 <filter id="d_halo" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2720" height="1880"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <radialGradient id="d_vig" cx="50%" cy="50%" r="75%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
 <linearGradient id="d_bougie" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFF4D0"/><stop offset=".5" stop-color="#FFC45A"/><stop offset="1" stop-color="#FF7A2A" stop-opacity=".2"/></linearGradient>
 <linearGradient id="d_bois" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8A5A36"/><stop offset=".5" stop-color="#5A3820"/><stop offset="1" stop-color="#2A190E"/></linearGradient>
'''


def bougie(x, y, h=30, w=18, echelle=1.0, lueur=True):
    """Bougie posée en (x, y) = bas de la cire. La flamme s'anime (classe bougie_fl)."""
    o = f'<rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" rx="3" fill="#EDE3D3"/><ellipse cx="{x}" cy="{y-h}" rx="{w/2}" ry="{w/6}" fill="#F8F0E2"/>'
    o += f'<rect x="{x-w/2+2}" y="{y-h+4}" width="{w/4}" height="{h-8}" fill="#FFF" opacity=".35"/>'
    if lueur:
        o += f'<circle class="bougie_gl" cx="{x}" cy="{y-h-12*echelle}" r="{34*echelle}" fill="#FFB860" opacity=".5" filter="url(#d_b10)" style="mix-blend-mode:screen"/>'
    o += f'<path d="M{x} {y-h} L{x} {y-h-5}" stroke="#2A1A10" stroke-width="2"/>'
    o += (f'<g class="bougie_fl" data-x="{x}" data-y="{y-h-2}" data-s="{echelle}" data-ph="{random.random()*6:.2f}">'
          f'<path d="{FLAMME}" fill="url(#d_bougie)"/></g>')
    return o


def tasse(x, y, s=1.0):
    """Mug noir à la torche, posé en (x, y) = bas."""
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 -78 L70 -78 L66 0 C62 8 8 8 4 0 Z" fill="#1E140D"/><ellipse cx="35" cy="-78" rx="35" ry="7" fill="#3B2412"/>'
            f'<path d="M68 -62 C96 -62 98 -20 64 -18" stroke="#1E140D" stroke-width="8" fill="none"/>'
            f'<g transform="translate(24 -58) scale(.05)" fill="#F5EDE0" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g></g>')


def bible_fermee(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 L28 -30 L232 -30 L222 0 Z" fill="#2E1A0E"/>'
            f'<path d="M0 0 L222 0 L222 16 L0 16 Z" fill="#E2C88E"/><path d="M100 -24 L100 -6 M88 -16 L112 -16" stroke="#C9A35A" stroke-width="4" stroke-linecap="round"/></g>')


def bible_ouverte(x, y, s=1.0):
    """Bible ouverte vue de face, posée en (x, y) = milieu du dos du livre."""
    lignes = "".join(f'<path d="M{-88+i*0} {-30+i*7} L-14 {-26+i*7}" stroke="#9A8A74" stroke-width="2"/>' for i in range(4))
    lignes += "".join(f'<path d="M14 {-26+i*7} L88 {-30+i*7}" stroke="#9A8A74" stroke-width="2"/>' for i in range(4))
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-104 4 L104 4 L100 12 L-100 12 Z" fill="#3A1E10"/>'
            f'<path d="M0 6 C-30 -4 -70 -2 -100 4 L-96 -40 C-66 -46 -30 -48 0 -38 Z" fill="#F5EDE0"/>'
            f'<path d="M0 6 C30 -4 70 -2 100 4 L96 -40 C66 -46 30 -48 0 -38 Z" fill="#EFE4D2"/>'
            f'<path d="M0 -38 L0 6" stroke="#B8A48A" stroke-width="2"/>{lignes}'
            f'<path d="M6 -38 L10 30 L16 22 L20 32 L16 -38 Z" fill="#B23A22"/></g>')


# ---------------------------------------------------------------- décor 1 : feu de camp
S1 = dict(s=.8, tx=400, ty=241)

def pin(x, base, h, w, couleur):
    o = []
    for k in range(4):
        y1 = base - h * (0.25 + k * 0.22); ww = w * (1 - k * 0.2)
        o.append(f'<path d="M{x-ww/2:.0f} {y1+h*.32:.0f} L{x} {y1-h*.08:.0f} L{x+ww/2:.0f} {y1+h*.32:.0f} Z" fill="{couleur}"/>')
    o.append(f'<rect x="{x-w*.05:.0f}" y="{base-h*.2:.0f}" width="{w*.1:.0f}" height="{h*.2:.0f}" fill="{couleur}"/>')
    return "".join(o)

def feu_de_camp():
    rnd = random.Random(21)
    d = '''
 <linearGradient id="c1_ciel" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="900"><stop offset="0" stop-color="#05070F"/><stop offset=".5" stop-color="#0E1128"/><stop offset=".8" stop-color="#211A38"/><stop offset="1" stop-color="#3A2232"/></linearGradient>
 <linearGradient id="c1_sol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16100E"/><stop offset="1" stop-color="#070505"/></linearGradient>
 <radialGradient id="c1_lueur"><stop offset="0" stop-color="#FF9A3D" stop-opacity=".75"/><stop offset=".45" stop-color="#E0602A" stop-opacity=".25"/><stop offset="1" stop-color="#E0602A" stop-opacity="0"/></radialGradient>
 <radialGradient id="c1_lune"><stop offset="0" stop-color="#FFF6E2" stop-opacity=".5"/><stop offset="1" stop-color="#FFF6E2" stop-opacity="0"/></radialGradient>
 <linearGradient id="c1_fo" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFB347"/><stop offset=".55" stop-color="#F06A2A"/><stop offset="1" stop-color="#C0322B" stop-opacity="0"/></linearGradient>
 <linearGradient id="c1_fm" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFE08A"/><stop offset=".6" stop-color="#FF9A3D"/><stop offset="1" stop-color="#FF7A2A" stop-opacity="0"/></linearGradient>
 <linearGradient id="c1_fi" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFFBEA"/><stop offset=".6" stop-color="#FFE7A0"/><stop offset="1" stop-color="#FFD27A" stop-opacity="0"/></linearGradient>
 <linearGradient id="c1_buche" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A4E2E"/><stop offset=".45" stop-color="#4E301B"/><stop offset="1" stop-color="#1E120A"/></linearGradient>
 <mask id="c1_lune_m"><rect width="1920" height="1080" fill="#000"/><circle cx="1010" cy="140" r="44" fill="#fff"/><circle cx="1028" cy="128" r="40" fill="#000"/></mask>
'''
    b = ['<rect width="1920" height="1080" fill="url(#c1_ciel)"/>']
    # étoiles
    for _ in range(170):
        x, y = rnd.uniform(0, 1920), rnd.uniform(0, 640) ** 1.0
        r = rnd.choice([.8, .9, 1, 1.1, 1.3, 1.6, 2.1])
        b.append(f'<circle class="etoile" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#FFF3DC" data-o="{rnd.uniform(.35, .95):.2f}" data-ph="{rnd.uniform(0, 6.3):.2f}" data-sp="{rnd.uniform(1.2, 3.5):.2f}"/>')
    for _ in range(7):
        x, y = rnd.uniform(80, 1880), rnd.uniform(40, 420)
        b.append(f'<g class="etoile" data-o=".9" data-ph="{rnd.uniform(0, 6.3):.2f}" data-sp="{rnd.uniform(1, 2):.2f}"><circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="#FFF3DC" opacity=".25" filter="url(#d_b4)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2.2" fill="#FFFBF0"/></g>')
    # lune
    b.append('<circle cx="1010" cy="140" r="150" fill="url(#c1_lune)" opacity=".5"/><g mask="url(#c1_lune_m)"><circle cx="1010" cy="140" r="44" fill="#F3E9D8"/></g>')
    # montagnes, collines, pins
    b.append('<path d="M0 720 L140 650 L260 690 L420 590 L560 660 L700 610 L860 680 L1020 600 L1180 670 L1330 560 L1500 650 L1640 610 L1800 680 L1920 640 L1920 900 L0 900 Z" fill="#0E0C20"/>')
    b.append('<path d="M0 720 L140 650 L260 690 L420 590 L560 660 L700 610 L860 680 L1020 600 L1180 670 L1330 560 L1500 650 L1640 610 L1800 680 L1920 640" fill="none" stroke="#2E2850" stroke-width="3" opacity=".5"/>')
    b.append('<path d="M0 800 C200 760 420 790 640 770 C900 748 1160 790 1400 760 C1600 740 1780 770 1920 750 L1920 900 L0 900 Z" fill="#08070F"/>')
    for x, h in ((40, 300), (130, 380), (230, 260), (1700, 320), (1800, 400), (1890, 280)):
        b.append(pin(x, 860, h, h * .42, "#08070E"))
    for x, h in ((330, 150), (390, 120), (1560, 140), (1620, 170)):
        b.append(pin(x, 820, h, h * .42, "#0B0A16"))
    # sol et lueur du feu au sol
    b.append('<path d="M0 840 C400 830 800 845 1200 835 C1500 828 1750 838 1920 832 L1920 1080 L0 1080 Z" fill="url(#c1_sol)"/>')
    b.append('<ellipse class="c1_lum" data-b=".9" cx="1270" cy="990" rx="760" ry="170" fill="url(#c1_lueur)" style="mix-blend-mode:screen"/>')
    b.append('<ellipse class="c1_lum" data-b=".55" cx="1270" cy="820" rx="560" ry="460" fill="url(#c1_lueur)" style="mix-blend-mode:screen"/>')
    # bûche où il est assis
    b.append('<ellipse cx="740" cy="968" rx="330" ry="24" fill="#000" opacity=".55" filter="url(#d_b10)"/>')
    b.append('<rect x="460" y="872" width="560" height="90" rx="44" fill="url(#c1_buche)"/>')
    for k in range(7):
        x = 500 + k * 72
        b.append(f'<path d="M{x} 884 C{x+14} 900 {x+10} 930 {x+26} 950" stroke="#24150C" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>')
    b.append('<path class="c1_lum" data-b=".8" d="M560 876 C700 870 880 870 1000 880" stroke="#FFA050" stroke-width="5" fill="none" opacity=".8" filter="url(#d_b3)"/>')
    b.append('<ellipse cx="1012" cy="917" rx="24" ry="45" fill="#B07A48"/><ellipse cx="1012" cy="917" rx="16" ry="32" fill="none" stroke="#7A4E2E" stroke-width="3"/><ellipse cx="1012" cy="917" rx="8" ry="16" fill="none" stroke="#7A4E2E" stroke-width="3"/>')
    b.append('<ellipse class="c1_lum" data-b=".5" cx="1018" cy="917" rx="22" ry="44" fill="#FF8A3D" style="mix-blend-mode:screen"/>')
    b.append(bible_fermee(845, 876, .55))
    b.append(tasse(1060, 1010, .7))
    # pierres du foyer, bûches, braises, flammes
    for k in range(12):
        a = k / 12 * 2 * math.pi
        x, y = 1270 + 150 * math.cos(a), 996 + 30 * math.sin(a)
        if y < 990 and abs(x - 1270) < 110:
            continue
        rx, ry = rnd.uniform(26, 36), rnd.uniform(15, 20)
        b.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="#2E2624"/><ellipse class="c1_lum" data-b=".7" cx="{x:.0f}" cy="{y-ry*.45:.0f}" rx="{rx*.7:.0f}" ry="{ry*.35:.0f}" fill="#E07A3A" opacity=".7" filter="url(#d_b3)"/>')
    b.append('<ellipse cx="1270" cy="992" rx="120" ry="20" fill="#5A1A0A"/><ellipse class="c1_lum" data-b="1" cx="1270" cy="990" rx="110" ry="16" fill="#FF6A1A" filter="url(#d_b6)"/>')
    for x1, y1, x2, y2 in ((1170, 1000, 1330, 930), (1370, 1000, 1210, 930), (1200, 1010, 1350, 1000)):
        b.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#2A190E" stroke-width="30" stroke-linecap="round"/><path d="M{x1} {y1} L{x2} {y2}" stroke="#FF7A2A" stroke-width="6" stroke-linecap="round" opacity=".6" stroke-dasharray="18 26" filter="url(#d_b2)"/>')
    fl = []
    for couche, grad, op, tiges in (("o", "c1_fo", .85, ((-44, 130, 230, 0.0), (40, 120, 260, 1.3), (0, 160, 320, 2.1))),
                                    ("m", "c1_fm", .95, ((-26, 96, 190, 0.7), (26, 86, 210, 2.6), (0, 116, 240, 3.3))),
                                    ("i", "c1_fi", 1, ((-10, 54, 120, 1.9), (12, 50, 130, 4.1), (0, 64, 160, 5.0)))):
        for dx, w, h, ph in tiges:
            fl.append(f'<g class="flamme" data-x="{1270+dx}" data-y="985" data-w="{w}" data-h="{h}" data-ph="{ph}"><path d="{FLAMME}" fill="url(#{grad})" opacity="{op}"/></g>')
    b.append(f'<g filter="url(#d_b2)">{"".join(fl)}</g>')
    # devant : braises qui montent, herbes sombres
    f = []
    for k in range(46):
        f.append(f'<circle class="braise" r="{rnd.uniform(1.6, 3.4):.1f}" fill="#FFC46A" data-x="{1270+rnd.uniform(-70, 70):.0f}" data-l="{rnd.uniform(1.4, 3.0):.2f}" '
                 f'data-off="{rnd.uniform(0, 3):.2f}" data-v="{rnd.uniform(90, 170):.0f}" data-a="{rnd.uniform(8, 32):.0f}" data-f="{rnd.uniform(1.5, 4):.2f}" data-ph="{rnd.uniform(0, 6.3):.2f}"/>')
    devant = f'<g filter="url(#d_halo)">{"".join(f)}</g>'
    for x0, sens in ((0, 1), (1920, -1)):
        for k in range(14):
            x = x0 + sens * rnd.uniform(0, 240); h = rnd.uniform(40, 110); c = rnd.uniform(-30, 30)
            devant += f'<path d="M{x-6:.0f} 1080 Q{x+c*.4:.0f} {1080-h*.6:.0f} {x+c:.0f} {1080-h:.0f} Q{x+c*.3+4:.0f} {1080-h*.5:.0f} {x+6:.0f} 1080 Z" fill="#050404"/>'
    return d, "".join(b), devant


# ---------------------------------------------------------------- décor 2 : chapelle
S2 = dict(s=.8, tx=672, ty=241)
OGIVE = "M1170 650 L1170 330 C1170 220 1240 150 1330 110 C1420 150 1490 220 1490 330 L1490 650 Z"

def chapelle():
    rnd = random.Random(5)
    d = f'''
 <linearGradient id="c2_mur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2A231E"/><stop offset="1" stop-color="#3A3029"/></linearGradient>
 <linearGradient id="c2_sol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E251E"/><stop offset="1" stop-color="#110D0A"/></linearGradient>
 <linearGradient id="c2_rayon" gradientUnits="userSpaceOnUse" x1="1330" y1="300" x2="860" y2="1080"><stop offset="0" stop-color="#FFE9C4" stop-opacity=".75"/><stop offset=".7" stop-color="#FFE0B0" stop-opacity=".22"/><stop offset="1" stop-color="#FFE0B0" stop-opacity="0"/></linearGradient>
 <linearGradient id="c2_banc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4E301B"/><stop offset="1" stop-color="#2A190E"/></linearGradient>
 <radialGradient id="c2_cierges"><stop offset="0" stop-color="#FFA040" stop-opacity=".45"/><stop offset="1" stop-color="#FFA040" stop-opacity="0"/></radialGradient>
 <clipPath id="c2_vitrail"><path d="{OGIVE}"/></clipPath>
'''
    b = ['<rect width="1920" height="1080" fill="url(#c2_mur)"/>']
    # pierres
    pierres = []
    for row, y in enumerate(range(0, 820, 56)):
        x = -rnd.uniform(0, 120) if row % 2 else -60
        while x < 1920:
            w = rnd.uniform(110, 180)
            c = rnd.choice(["#2E2621", "#342B25", "#2A231E", "#3A3029", "#30281F"])
            pierres.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="56" rx="5" fill="{c}" stroke="#16110D" stroke-width="3"/>')
            x += w
    b.append(f'<g>{"".join(pierres)}</g>')
    b.append('<ellipse cx="1330" cy="380" rx="520" ry="420" fill="#FFD9A0" opacity=".14" filter="url(#d_b40)" style="mix-blend-mode:screen"/>')
    # vitrail
    v = [f'<path d="{OGIVE}" fill="#2E4A7A"/>']
    for j in range(0, 24):
        for i in range(-1, 9):
            cx, cy = 1170 + i * 40 + (20 if j % 2 else 0), 100 + j * 28
            e = abs(cx - 1330) / 160
            pal = ["#F2C45A", "#F5EDE0", "#E0A840"] if e < .22 else (["#E0A840", "#C0522B", "#9A3324", "#E07A3A"] if e < .55 else ["#2E4A7A", "#1E3460", "#3E6B3A", "#2E4A7A", "#24406E"])
            v.append(f'<polygon points="{cx},{cy-28} {cx+20},{cy} {cx},{cy+28} {cx-20},{cy}" fill="{rnd.choice(pal)}" opacity="{rnd.uniform(.8, 1):.2f}" stroke="#16110D" stroke-width="3"/>')
    v.append('<circle cx="1330" cy="250" r="78" fill="#1E3460"/>')
    for k in range(12):
        v.append(f'<path d="M1330 250 L{1330+78*math.cos(k*0.5236):.0f} {250+78*math.sin(k*0.5236):.0f}" stroke="#16110D" stroke-width="4"/>')
    v.append(f'<g transform="translate(1294 186) scale(.15)" fill="#F2C45A" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>')
    v.append('<circle cx="1330" cy="250" r="78" fill="none" stroke="#16110D" stroke-width="7"/>')
    v.append('<path d="M1170 380 L1490 380 M1170 520 L1490 520" stroke="#16110D" stroke-width="5"/>')
    v.append('<rect x="1170" y="100" width="320" height="560" fill="#FFF1D8" opacity=".18"/>')
    b.append(f'<path d="{OGIVE}" fill="#FFE8C0" opacity=".55" filter="url(#d_b24)" style="mix-blend-mode:screen"/>')
    b.append(f'<g clip-path="url(#c2_vitrail)">{"".join(v)}</g>')
    b.append('<rect x="1264" y="330" width="14" height="320" fill="#4A4038"/><rect x="1382" y="330" width="14" height="320" fill="#4A4038"/>')
    b.append(f'<path d="{OGIVE}" fill="none" stroke="#4E443B" stroke-width="22"/><path d="{OGIVE}" fill="none" stroke="#6A5E52" stroke-width="5" transform="translate(-3 -3)"/>')
    b.append('<rect x="1144" y="650" width="372" height="26" fill="#4E443B"/>')
    # sol dallé
    b.append('<rect y="820" width="1920" height="260" fill="url(#c2_sol)"/><rect y="814" width="1920" height="10" fill="#1A1410"/>')
    for y in (850, 895, 955, 1035):
        b.append(f'<path d="M0 {y} L1920 {y}" stroke="#0E0A08" stroke-width="3" opacity=".7"/>')
    for x in range(-2200, 4200, 260):
        b.append(f'<path d="M{960+(x-960)*.3:.0f} 820 L{x} 1080" stroke="#0E0A08" stroke-width="3" opacity=".55"/>')
    b.append('<ellipse cx="880" cy="1010" rx="420" ry="70" fill="#FFD9A0" opacity=".18" filter="url(#d_b24)" style="mix-blend-mode:screen"/>')
    # présentoir à cierges
    b.append('<ellipse cx="330" cy="740" rx="380" ry="260" fill="url(#c2_cierges)" style="mix-blend-mode:screen"/>')
    b.append('<path d="M150 1040 L170 690 M510 1040 L490 690" stroke="#121010" stroke-width="10"/>')
    for k, y in enumerate((700, 770, 840)):
        b.append(f'<path d="M{130+k*0} {y} L{530} {y}" stroke="#141210" stroke-width="10" stroke-linecap="round"/>')
        for j in range(6 + (k % 2)):
            x = 160 + j * 60 + (30 if k % 2 == 0 else 0)
            if x > 505:
                continue
            b.append(bougie(x, y - 5, h=rnd.uniform(22, 40), w=16, echelle=.8))
    # banc (dossier derrière lui, assise)
    b.append('<ellipse cx="960" cy="1036" rx="460" ry="26" fill="#000" opacity=".5" filter="url(#d_b10)"/>')
    b.append('<rect x="560" y="720" width="800" height="152" rx="6" fill="url(#c2_banc)"/>')
    for x in range(600, 1350, 125):
        b.append(f'<rect x="{x}" y="740" width="100" height="112" rx="6" fill="none" stroke="#24150C" stroke-width="4"/>')
    b.append('<rect x="548" y="706" width="824" height="22" rx="8" fill="#6A4426"/>')
    b.append('<rect x="580" y="900" width="26" height="132" fill="#2E1C10"/><rect x="1314" y="900" width="26" height="132" fill="#2E1C10"/>')
    b.append('<path d="M580 866 L1340 866 L1362 878 L558 878 Z" fill="#7A5232"/><rect x="556" y="878" width="808" height="26" fill="#5A3820"/>')
    # pupitre avec Bible ouverte
    b.append('<ellipse cx="1660" cy="1040" rx="120" ry="14" fill="#000" opacity=".5" filter="url(#d_b6)"/>')
    b.append('<path d="M1600 1040 L1720 1040 L1700 1024 L1620 1024 Z" fill="#2E1C10"/><rect x="1650" y="790" width="20" height="236" fill="#3A2414"/>')
    b.append('<path d="M1540 800 L1780 800 L1756 762 L1564 762 Z" fill="#5A3820"/><path d="M1540 800 L1780 800 L1780 812 L1540 812 Z" fill="#3A2414"/>')
    b.append(bible_ouverte(1660, 768, .95))
    # devant : rayons de lumière et poussières
    f = []
    for pts, ph in (("1180,330 1290,650 860,1080 430,1080", 0), ("1260,280 1420,650 1200,1080 880,1080", 2.1), ("1380,320 1490,650 1470,1080 1250,1080", 4.0)):
        f.append(f'<polygon class="rayon" data-b=".55" data-ph="{ph}" points="{pts}" fill="url(#c2_rayon)" style="mix-blend-mode:screen" filter="url(#d_b16)"/>')
    for k in range(90):
        y = rnd.uniform(320, 1040); t = (y - 300) / 780
        gauche, droite = 1180 + (430 - 1180) * t, 1490 + (1460 - 1490) * t
        x = rnd.uniform(gauche, droite)
        f.append(f'<circle class="poussiere" cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1, 2.6):.1f}" fill="#FFF2D8" data-x="{x:.0f}" data-y="{y:.0f}" data-a="{rnd.uniform(6, 20):.0f}" data-ph="{rnd.uniform(0, 6.3):.2f}" data-sp="{rnd.uniform(.3, .9):.2f}"/>')
    return d, "".join(b), "".join(f)


# ---------------------------------------------------------------- décor 3 : sommet à l'aube
S3 = dict(s=.82, tx=360, ty=232)
ROCHER = "M0 820 L120 800 L260 838 L420 878 L620 884 L860 896 L980 930 L1080 990 L1180 1080 L0 1080 Z"

def sommet():
    rnd = random.Random(9)
    d = '''
 <linearGradient id="c3_ciel" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="820"><stop offset="0" stop-color="#1A2244"/><stop offset=".3" stop-color="#36386A"/><stop offset=".55" stop-color="#8E6088"/><stop offset=".75" stop-color="#EE8E74"/><stop offset=".9" stop-color="#FFC48A"/><stop offset="1" stop-color="#FFE0A8"/></linearGradient>
 <radialGradient id="c3_soleil"><stop offset="0" stop-color="#FFFDF2"/><stop offset=".7" stop-color="#FFE7AE"/><stop offset="1" stop-color="#FFD28A"/></radialGradient>
 <radialGradient id="c3_halo"><stop offset="0" stop-color="#FFE2A0" stop-opacity=".9"/><stop offset=".3" stop-color="#FFC07A" stop-opacity=".35"/><stop offset="1" stop-color="#FF9A6A" stop-opacity="0"/></radialGradient>
 <linearGradient id="c3_roc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3E2E38"/><stop offset=".4" stop-color="#2A1F2A"/><stop offset="1" stop-color="#140E16"/></linearGradient>
'''
    b = ['<rect width="1920" height="1080" fill="url(#c3_ciel)"/>']
    for _ in range(40):
        b.append(f'<circle class="etoile" cx="{rnd.uniform(0, 1920):.0f}" cy="{rnd.uniform(0, 230):.0f}" r="{rnd.choice([.8, 1, 1.3])}" fill="#FFF3DC" data-o="{rnd.uniform(.15, .45):.2f}" data-ph="{rnd.uniform(0, 6.3):.2f}" data-sp="{rnd.uniform(1, 3):.2f}"/>')
    b.append('<g id="c3_astre"><circle cx="1330" cy="690" r="520" fill="url(#c3_halo)" style="mix-blend-mode:screen"/><circle cx="1330" cy="690" r="170" fill="#FFE8B0" opacity=".45" filter="url(#d_b24)"/><circle cx="1330" cy="690" r="66" fill="url(#c3_soleil)"/></g>')
    # sommets lointains (contre-jour)
    for pts in ("1330,780 1600,520 1680,560 1760,530 1920,640 1920,780", "820,780 1060,575 1150,620 1300,780", "200,780 420,640 520,690 640,780"):
        b.append(f'<polygon points="{pts}" fill="#5A4A78"/>')
        b.append(f'<polyline points="{pts}" fill="none" stroke="#FFC79A" stroke-width="4" opacity=".55" filter="url(#d_b3)"/>')
    for pts in ("1600,520 1330,780 1560,780", "1060,575 1150,620 1300,780 1090,780", "420,640 520,690 640,780 450,780"):
        b.append(f'<polygon points="{pts}" fill="#7C6494" opacity=".8"/>')
    # mer de nuages : 4 bandes de cumulus, de la plus lointaine à la plus proche
    for k, (y0, rmin, rmax, vit, haut, bas) in enumerate(((735, 34, 64, 5, "#FFE8D2", "#DDA8B2"), (790, 50, 90, -8, "#FFE2C8", "#C690A8"),
                                                          (868, 66, 118, 13, "#FCD8C2", "#A97C9E"), (968, 90, 150, -19, "#F6CDBA", "#8A6890"))):
        d += f'<linearGradient id="c3_n{k}" gradientUnits="userSpaceOnUse" x1="0" y1="{y0-rmax}" x2="0" y2="{y0+rmax*1.3:.0f}"><stop offset="0" stop-color="{haut}"/><stop offset=".55" stop-color="{bas}"/><stop offset="1" stop-color="{bas}"/></linearGradient>'
        puffs, x = [], -420
        while x < 1980:
            r = rnd.uniform(rmin, rmax)
            puffs.append(f'<circle cx="{x:.0f}" cy="{y0+r*rnd.uniform(.1, .45):.0f}" r="{r:.0f}"/>')
            x += r * rnd.uniform(1.0, 1.45)
        bande = f'{"".join(puffs)}<rect x="-420" y="{y0+rmax*.35:.0f}" width="2400" height="{1080-y0+40}"/>'
        # deux copies décalées d'une période (2400) : la bande défile en boucle sans trou
        b.append(f'<g class="nuage" data-v="{vit}"><g fill="url(#c3_n{k})" filter="url(#d_b3)">{bande}<g transform="translate(-2400 0)">{bande}</g></g></g>')
    # rocher au premier plan
    b.append(f'<path d="{ROCHER}" fill="url(#c3_roc)"/>')
    b.append('<path d="M0 820 L120 800 L260 838 L420 878 L620 884 L860 896 L980 930 L1080 990 L1180 1080" fill="none" stroke="#FFB070" stroke-width="7" opacity=".75" filter="url(#d_b3)"/>')
    b.append('<path d="M0 836 L120 818 L260 856 L420 896 L620 902 L860 914 L960 944 L900 960 L600 930 L300 900 L0 880 Z" fill="#4A3644" opacity=".7"/>')
    for x1, y1, x2, y2 in ((300, 900, 360, 1000), (720, 930, 700, 1040), (980, 960, 1040, 1060), (160, 860, 120, 980)):
        b.append(f'<path d="M{x1} {y1} L{(x1+x2)/2+10:.0f} {(y1+y2)/2:.0f} L{x2} {y2}" stroke="#120C12" stroke-width="4" fill="none" opacity=".8"/>')
    for x in (90, 250, 880, 1010):
        y = 812 if x < 200 else (850 if x < 300 else (900 if x < 950 else 940))
        b.append(f'<path d="M{x-12} {y} L{x-6} {y-22} L{x} {y} L{x+6} {y-28} L{x+10} {y} L{x+16} {y-18} L{x+20} {y}" fill="#3E4A30"/>')
    b.append('<ellipse cx="660" cy="900" rx="220" ry="14" fill="#000" opacity=".4" filter="url(#d_b6)"/>')
    # oiseaux
    for k in range(4):
        b.append(f'<g class="oiseau" data-x="{rnd.uniform(880, 1250):.0f}" data-y="{rnd.uniform(300, 470):.0f}" data-v="{rnd.uniform(45, 80):.0f}" data-ph="{rnd.uniform(0, 6.3):.2f}" data-s="{rnd.uniform(1.3, 1.8):.2f}">'
                 '<path d="M-16 0 Q-8 -10 0 0 Q8 -10 16 0" stroke="#2A1E34" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>')
    # devant : brume qui passe
    f = []
    for k in range(5):
        f.append(f'<ellipse class="brume" data-v="{rnd.uniform(18, 32):.0f}" data-x="{rnd.uniform(1600, 2300):.0f}" cx="0" cy="{rnd.uniform(960, 1060):.0f}" rx="{rnd.uniform(200, 320):.0f}" ry="{rnd.uniform(40, 70):.0f}" fill="#FFF0E6" opacity=".28" filter="url(#d_b24)"/>')
    return d, "".join(b), "".join(f)


# ---------------------------------------------------------------- décor 4 : chambre, soir de pluie
S4 = dict(s=.82, tx=330, ty=226)

def chambre():
    rnd = random.Random(13)
    d = '''
 <linearGradient id="c4_mur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E1610"/><stop offset="1" stop-color="#2E2016"/></linearGradient>
 <linearGradient id="c4_nuit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08101E"/><stop offset="1" stop-color="#1C2C48"/></linearGradient>
 <linearGradient id="c4_rideau" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6A2A18"/><stop offset=".5" stop-color="#A0452A"/><stop offset="1" stop-color="#5A2414"/></linearGradient>
 <linearGradient id="c4_parquet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A2E1A"/><stop offset="1" stop-color="#1E120A"/></linearGradient>
 <radialGradient id="c4_tapis"><stop offset="0" stop-color="#B65A34"/><stop offset=".7" stop-color="#8E3F20"/><stop offset="1" stop-color="#5A2A14"/></radialGradient>
 <radialGradient id="c4_lampe"><stop offset="0" stop-color="#FFC070" stop-opacity=".55"/><stop offset=".5" stop-color="#FF9A40" stop-opacity=".16"/><stop offset="1" stop-color="#FF9A40" stop-opacity="0"/></radialGradient>
 <linearGradient id="c4_cone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD08A" stop-opacity=".35"/><stop offset="1" stop-color="#FFD08A" stop-opacity="0"/></linearGradient>
 <clipPath id="c4_vitre"><rect x="1150" y="120" width="580" height="580"/></clipPath>
'''
    b = ['<rect width="1920" height="1080" fill="url(#c4_mur)"/>']
    b.append('<ellipse cx="200" cy="380" rx="760" ry="620" fill="url(#c4_lampe)" style="mix-blend-mode:screen"/>')
    # fenêtre : nuit, lumières lointaines, pluie, gouttes
    w = ['<rect x="1150" y="120" width="580" height="580" fill="url(#c4_nuit)"/>']
    for _ in range(34):
        w.append(f'<circle cx="{rnd.uniform(1150, 1730):.0f}" cy="{rnd.uniform(470, 700):.0f}" r="{rnd.uniform(6, 18):.0f}" fill="{rnd.choice(["#FFB45A", "#FFE2B0", "#9FB4FF", "#E05A3A", "#7FA0E0"])}" opacity="{rnd.uniform(.2, .55):.2f}"/>')
    w = [w[0], f'<g filter="url(#d_b10)">{"".join(w[1:])}</g>']
    for _ in range(120):
        lg = rnd.uniform(24, 44)
        w.append(f'<path class="pluie" data-x="{rnd.uniform(1150, 1800):.0f}" data-y="{rnd.uniform(0, 640):.0f}" data-v="{rnd.uniform(900, 1300):.0f}" d="M0 0 L-5 {lg:.0f}" stroke="#B8C8E8" stroke-width="{rnd.choice([1.5, 2, 2.5])}" opacity="{rnd.uniform(.25, .55):.2f}" stroke-linecap="round"/>')
    for _ in range(30):
        r = rnd.uniform(3, 7)
        w.append(f'<g class="goutte" data-x="{rnd.uniform(1160, 1720):.0f}" data-y="{rnd.uniform(0, 600):.0f}" data-v="{rnd.uniform(10, 45):.0f}"><ellipse cx="0" cy="0" rx="{r*.8:.1f}" ry="{r:.1f}" fill="#9FB8E0" opacity=".45"/><circle cx="{-r*.3:.1f}" cy="{-r*.35:.1f}" r="{r*.3:.1f}" fill="#fff" opacity=".7"/></g>')
    b.append(f'<g clip-path="url(#c4_vitre)">{"".join(w)}</g>')
    b.append('<rect x="1150" y="120" width="580" height="580" fill="none" stroke="#24160C" stroke-width="22"/><path d="M1440 120 L1440 700 M1150 410 L1730 410" stroke="#24160C" stroke-width="14"/>')
    b.append('<rect x="1120" y="700" width="640" height="24" fill="#4A2E1A"/><rect x="1120" y="722" width="640" height="8" fill="#1E120A"/>')
    b.append('<ellipse cx="1440" cy="560" rx="360" ry="300" fill="#4A6AA8" opacity=".12" filter="url(#d_b40)" style="mix-blend-mode:screen"/>')
    # rideaux
    b.append('<path d="M1030 74 L1870 74" stroke="#120A06" stroke-width="8" stroke-linecap="round"/><circle cx="1030" cy="74" r="10" fill="#3A2414"/><circle cx="1870" cy="74" r="10" fill="#3A2414"/>')
    for x0, x1 in ((1050, 1200), (1690, 1850)):
        b.append(f'<path d="M{x0} 80 L{x1} 80 C{x1-10} 300 {x1+14} 600 {x1-6} 870 L{x0+6} 870 C{x0-10} 600 {x0+8} 300 {x0} 80 Z" fill="url(#c4_rideau)"/>')
        for k in range(1, 5):
            x = x0 + (x1 - x0) * k / 5
            b.append(f'<path d="M{x:.0f} 84 C{x-8:.0f} 300 {x+10:.0f} 600 {x-4:.0f} 866" stroke="#4A1A0C" stroke-width="7" fill="none" opacity=".55" filter="url(#d_b3)"/>')
    # cadre au mur : la torche
    b.append('<rect x="770" y="170" width="170" height="210" rx="4" fill="#2A190E"/><rect x="786" y="186" width="138" height="178" fill="#F1E6D2"/><rect x="786" y="186" width="138" height="178" fill="none" stroke="#B88A50" stroke-width="3"/>')
    b.append(f'<g transform="translate(816 214) scale(.16)" fill="#C0522B" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>')
    # sol, plinthe, tapis
    b.append('<rect y="860" width="1920" height="220" fill="url(#c4_parquet)"/><rect y="850" width="1920" height="14" fill="#1A0F08"/>')
    for y in (900, 950, 1012):
        b.append(f'<path d="M0 {y} L1920 {y}" stroke="#140C06" stroke-width="2" opacity=".7"/>')
    b.append('<ellipse cx="660" cy="1010" rx="560" ry="62" fill="url(#c4_tapis)"/><ellipse cx="660" cy="1010" rx="520" ry="50" fill="none" stroke="#E2C9A6" stroke-width="3" opacity=".45" stroke-dasharray="14 10"/>')
    # lampadaire
    b.append('<polygon points="128,330 272,330 380,1040 20,1040" fill="url(#c4_cone)" style="mix-blend-mode:screen"/>')
    b.append('<path d="M200 330 L200 1030 M150 1040 L200 1010 L250 1040" stroke="#1A120C" stroke-width="8" fill="none" stroke-linejoin="round"/>')
    b.append('<circle cx="200" cy="290" r="150" fill="#FFC070" opacity=".35" filter="url(#d_b40)" style="mix-blend-mode:screen"/>')
    b.append('<path d="M140 228 L260 228 L282 334 L118 334 Z" fill="#F3E3C8"/><path d="M118 334 L282 334" stroke="#FFF4DC" stroke-width="4"/><path d="M140 228 L260 228 L282 334 L118 334 Z" fill="#FFB050" opacity=".25"/>')
    # fauteuil (même pose que le personnage)
    b.append('<ellipse cx="640" cy="1034" rx="300" ry="22" fill="#000" opacity=".55" filter="url(#d_b10)"/>')
    s, tx, ty = S4["s"], S4["tx"], S4["ty"]
    b.append(f'<g transform="translate({tx} {ty}) scale({s})"><g filter="url(#f_s4)">{TQ.fauteuil()}</g></g>')
    # guéridon : Bible ouverte, bougie, tasse
    b.append('<ellipse cx="1000" cy="1032" rx="110" ry="12" fill="#000" opacity=".5" filter="url(#d_b6)"/>')
    b.append('<path d="M960 1030 L1040 1030 L1024 1012 L976 1012 Z" fill="#2E1C10"/><rect x="990" y="852" width="20" height="164" fill="#4A2E1A"/>')
    b.append('<ellipse cx="1000" cy="852" rx="110" ry="18" fill="#3A2414"/><ellipse cx="1000" cy="846" rx="110" ry="18" fill="#8A5A36"/>')
    b.append(bible_ouverte(980, 848, .62))
    b.append(bougie(1076, 846, h=44, w=20, echelle=1.1))
    b.append(tasse(900, 848, .5))
    return d, "".join(b), ""


# ---------------------------------------------------------------- assemblage
SCENES = [
    dict(id="s1", titre="Feu de camp", sous="Témoignages · récits de vie", place=S1, decor=feu_de_camp, foyer=(860, 620),
         lum=((.95, .8, .68), ((-10, "#FFA54A", .8), (8, "#9FB4FF", .1))),
         paroles=[[0.5, 2.4], [2.9, 4.4]], clins=[1.25, 3.7]),
    dict(id="s2", titre="Chapelle", sous="Prière · lecture de la Bible", place=S2, decor=chapelle, foyer=(960, 600),
         lum=((.92, .86, .8), ((-9, "#FFE7B8", .6), (8, "#FFB050", .16))),
         paroles=[[0.6, 2.0], [2.5, 4.3]], clins=[0.3, 2.3, 4.6]),
    dict(id="s3", titre="Sommet à l'aube", sous="Élévation · espérance · motivation", place=S3, decor=sommet, foyer=(820, 640),
         lum=((.9, .82, .84), ((-10, "#FFC27A", .9), (8, "#C8B8F0", .1))),
         paroles=[[0.4, 1.9], [2.6, 4.5]], clins=[1.1, 3.4]),
    dict(id="s4", titre="Chambre, soir de pluie", sous="Confidences · prière du soir", place=S4, decor=chambre, foyer=(760, 620),
         lum=((.95, .85, .74), ((9, "#FFB862", .7), (-8, "#8FAEE8", .13))),
         paroles=[[0.7, 2.6], [3.1, 4.2]], clins=[0.2, 2.8, 4.5]),
]


def page():
    random.seed(1)
    defs, fonds, devants = [P.DEFS[6:-7], TQ.DEFS_TQ[6:-7], DEFS_COMMUNS], [], []
    for sc in SCENES:
        defs.append(filtre_perso(f"f_{sc['id']}", *sc["lum"]))
    for sc in SCENES:
        d, b, f = sc["decor"]()
        defs.append(d)
        fonds.append(f'<g id="{sc["id"]}_fond" display="none">{b}</g>')
        devants.append(f'<g id="{sc["id"]}_devant" display="none">{f}</g>')
    config = dict(dur=DUREE_SCENE * len(SCENES), scene=DUREE_SCENE,
                  scenes=[dict(id=sc["id"], titre=sc["titre"], sous=sc["sous"], foyer=sc["foyer"], paroles=sc["paroles"], clins=sc["clins"], **sc["place"]) for sc in SCENES])
    svg = (f'<svg id="s" xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">'
           f'<defs>{"".join(defs)}</defs>'
           f'<g id="cam"><g id="fonds">{"".join(fonds)}</g>'
           f'<g id="perso_pos"><g id="perso_lum">{rig()}</g></g>'
           f'<g id="devants">{"".join(devants)}</g></g>'
           '<rect width="1920" height="1080" fill="url(#d_vig)" pointer-events="none"/>'
           f'<g transform="translate(1590 40) scale(.045)" fill="#FFF6E8" opacity=".9"><path d="{NOM_D}"/></g>'
           '<g id="etiquette" transform="translate(56 56)"><rect id="lab_fond" width="420" height="124" rx="16" fill="#120A06" fill-opacity=".72" stroke="#FFB060" stroke-opacity=".35" stroke-width="2"/>'
           '<text id="lab_n" x="28" y="40" font-size="17" letter-spacing="4" fill="#FFB46A" class="inter">DÉCOR</text>'
           '<text id="lab_t" x="28" y="84" font-size="36" fill="#FFF6E8" class="fraunces">Titre</text>'
           '<text id="lab_s" x="28" y="110" font-size="18" fill="#D9C8B4" class="inter">Sous-titre</text></g>'
           '<rect id="noir" width="1920" height="1080" fill="#000" opacity="1"/></svg>')
    html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Personnage en décors</title>
<style>
@font-face{{font-family:"InterB";src:url(../intro/fonts/inter-500.woff2) format("woff2")}}
@font-face{{font-family:"FrauncesB";src:url(../intro/fonts/fraunces-700.woff2) format("woff2")}}
html,body{{margin:0;background:#000}}
#stage{{width:1920px;height:1080px;overflow:hidden}}
svg{{display:block}}
.inter{{font-family:"InterB",Inter,Arial,sans-serif}}
.fraunces{{font-family:"FrauncesB",Georgia,serif}}
</style></head><body>
<!-- Fichier généré par animation/source/decors.py : ne pas modifier à la main. -->
<div id="stage">{svg}</div>
<script>window.CONFIG={json.dumps(config, ensure_ascii=False)};</script>
<script src="moteur.js"></script>
<script src="anim.js"></script>
</body></html>'''
    out = os.path.join(ROOT, "animation/index.html")
    open(out, "w").write(html)
    print("écrit", out, f"({len(html)//1024} Ko)")


if __name__ == "__main__":
    page()
