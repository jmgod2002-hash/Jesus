"""Plateau « salon-bibliothèque » Feu d'Élévation : deux fauteuils face à face, bibliothèques éclairées,
niche voûtée avec la torche en néon, ampoules suspendues, table basse, micros sur pied. Repère 1920 x 1080."""
import os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P
import trois_quarts as TQ

ROOT = P.ROOT
VUES = {"16x9": (0, 0, 1920, 1080), "9x16": (172, 0, 608, 1080)}
torch, flame = P.logo_parts()
NOM_D = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, 'marque/nom_feu_d_elevation.svg')).read()).group(1)
S, TX, TY = 0.75, 267, 250.5            # présentateur + fauteuil (repère 700 x 1000)
XM = 1653                                # fauteuil de l'invité, en miroir

def bibliotheque(x0, x1, seed):
    rnd = random.Random(seed); o = []
    o.append(f'<rect x="{x0}" y="90" width="{x1-x0}" height="740" fill="#1A0F08"/>')
    cols = ["#6B3A2A", "#8A6A45", "#3E4A3A", "#C9B48A", "#5A3A2A", "#2F3A44", "#A0522D", "#E2D2B8", "#7A4E2E"]
    for y in (250, 410, 570, 730):
        o.append(f'<rect x="{x0}" y="{y-150}" width="{x1-x0}" height="150" fill="url(#sl_niche)"/>')
        x = x0 + 14
        while x < x1 - 40:
            if rnd.random() < .12:      # objet : bougie ou petite plante
                if rnd.random() < .5:
                    o.append(f'<rect x="{x}" y="{y-34}" width="22" height="34" rx="3" fill="#E9DCC6"/><ellipse cx="{x+11}" cy="{y-44}" rx="14" ry="18" fill="#FFB860" opacity=".5" filter="url(#sl_b6)"/><path d="M{x+11} {y-52} C{x+16} {y-44} {x+16} {y-38} {x+11} {y-36} C{x+6} {y-38} {x+6} {y-44} {x+11} {y-52} Z" fill="#FFD27A"/>')
                else:
                    o.append(f'<path d="M{x} {y} L{x+4} {y-28} L{x+30} {y-28} L{x+34} {y} Z" fill="#A0522D"/>' + "".join(
                        f'<ellipse cx="{x+17}" cy="{y-46}" rx="7" ry="20" fill="#4E6B3A" transform="rotate({a} {x+17} {y-28})"/>' for a in (-40, -10, 20, 45)))
                x += 46; continue
            w = rnd.randint(14, 26); h = rnd.randint(84, 128); c = rnd.choice(cols)
            tilt = rnd.random() < .08
            book = f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="2" fill="{c}"/><rect x="{x+3}" y="{y-h+12}" width="{w-6}" height="3" fill="#E8D3A8" opacity=".45"/>'
            o.append(f'<g transform="rotate(10 {x+w} {y})">{book}</g>' if tilt else book)
            x += w + (12 if tilt else 2)
        o.append(f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="14" fill="#3A2414"/><rect x="{x0}" y="{y-150}" width="{x1-x0}" height="6" fill="#FFC77E" opacity=".55" filter="url(#sl_b6)"/>')
    for x in (x0, x1 - 14):
        o.append(f'<rect x="{x}" y="90" width="14" height="740" fill="#2A190E"/>')
    return "".join(o)

def ampoule_suspendue(x, y):
    pts = " ".join(f"L{x + (6 if i % 2 else -6)} {y + 30 - i * 5}" for i in range(1, 12))
    return (f'<path d="M{x} 0 L{x} {y-50}" stroke="#0A0604" stroke-width="3"/><rect x="{x-10}" y="{y-54}" width="20" height="24" rx="4" fill="#3A2414"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="170" ry="170" fill="#FFB050" opacity=".22" filter="url(#sl_b40)" style="mix-blend-mode:screen"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="38" ry="48" fill="#FFCF8A" opacity=".2" stroke="#FFE2B0" stroke-opacity=".35" stroke-width="2"/>'
            f'<path d="M{x-3} {y+38} L{x-3} {y+30} {pts} L{x+3} {y-30}" stroke="#FFF1C8" stroke-width="2.4" fill="none" filter="url(#sl_glow)"/>'
            f'<ellipse cx="{x}" cy="{y}" rx="18" ry="24" fill="#FFC36A" opacity=".5" filter="url(#sl_b10)"/>')

def micro_sur_pied(xpied, haut, cx, cy, angle):
    o = [f'<path d="M{xpied} 990 L{xpied-46} 1004 M{xpied} 990 L{xpied+46} 1004 M{xpied} 990 L{xpied+6} 980" stroke="#141210" stroke-width="7" stroke-linecap="round"/>',
         f'<rect x="{xpied-5}" y="{haut}" width="10" height="{990-haut}" fill="#1E1C1A"/>',
         f'<path d="M{xpied} {haut} L{cx} {cy}" stroke="#151312" stroke-width="10" stroke-linecap="round"/>',
         f'<g transform="translate({cx} {cy}) rotate({angle})"><rect x="-56" y="-22" width="112" height="44" rx="20" fill="url(#sl_mic)" stroke="#050505" stroke-width="3"/>'
         '<rect x="-56" y="-22" width="48" height="44" rx="20" fill="#26262A"/>'
         + "".join(f'<path d="M{x} -17 L{x} 17" stroke="#0E0E10" stroke-width="2"/>' for x in range(-48, -10, 6))
         + '<rect x="-10" y="-22" width="8" height="44" fill="#C0522B"/><rect x="-50" y="-16" width="98" height="6" rx="3" fill="#FFB46A" opacity=".22"/></g>']
    return "".join(o)

DEFS = '''<defs>
 <linearGradient id="sl_mur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140B06"/><stop offset="1" stop-color="#22140B"/></linearGradient>
 <linearGradient id="sl_niche" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2414"/><stop offset="1" stop-color="#1E120A"/></linearGradient>
 <radialGradient id="sl_arche" cx="50%" cy="45%" r="65%"><stop offset="0" stop-color="#4A2E1A"/><stop offset="1" stop-color="#20130A"/></radialGradient>
 <linearGradient id="sl_sol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2414"/><stop offset="1" stop-color="#170D06"/></linearGradient>
 <radialGradient id="sl_tapis" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#B65A34"/><stop offset=".7" stop-color="#8E3F20"/><stop offset="1" stop-color="#5A2A14"/></radialGradient>
 <linearGradient id="sl_mic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4A50"/><stop offset=".45" stop-color="#232327"/><stop offset="1" stop-color="#0A0A0C"/></linearGradient>
 <linearGradient id="sl_table" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B98552"/><stop offset="1" stop-color="#5A3820"/></linearGradient>
 <radialGradient id="sl_vig" cx="50%" cy="50%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
 <filter id="sl_b6" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="6"/></filter>
 <filter id="sl_b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="sl_b16" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="16"/></filter>
 <filter id="sl_b40" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="sl_dof" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><feGaussianBlur stdDeviation="1.8"/></filter>
 <filter id="sl_glow" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sl_neon" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="a"/><feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b"/>
  <feFlood flood-color="#FF8A3D"/><feComposite in2="b" operator="in" result="c"/>
  <feMerge><feMergeNode in="c"/><feMergeNode in="c"/><feMergeNode in="a"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="sl_perso" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1100" height="1400">
  <feColorMatrix type="matrix" values=".92 0 0 0 0  0 .83 0 0 0  0 0 .72 0 0  0 0 0 1 0" result="tinte"/>
  <feOffset in="SourceAlpha" dx="8" dy="-2" result="off"/>
  <feComposite in="SourceAlpha" in2="off" operator="out" result="bord"/>
  <feGaussianBlur in="bord" stdDeviation="2.5" result="bordf"/>
  <feFlood flood-color="#FFB050" flood-opacity=".65"/><feComposite in2="bordf" operator="in" result="rim"/>
  <feComposite in="rim" in2="SourceAlpha" operator="in" result="rim2"/>
  <feBlend in="rim2" in2="tinte" mode="screen"/></filter>
</defs>'''

def fond():
    o = ['<rect width="1920" height="1080" fill="url(#sl_mur)"/>',
         bibliotheque(40, 560, 3), bibliotheque(1360, 1880, 11)]
    # niche voûtée au centre, avec la torche et le nom en néon
    o.append('<path d="M700 830 L700 330 C700 180 820 110 960 110 C1100 110 1220 180 1220 330 L1220 830 Z" fill="url(#sl_arche)"/>')
    o.append('<path d="M700 830 L700 330 C700 180 820 110 960 110 C1100 110 1220 180 1220 330 L1220 830" fill="none" stroke="#5A3820" stroke-width="10"/>')
    o.append('<ellipse cx="960" cy="380" rx="300" ry="280" fill="#FF8A3D" opacity=".2" filter="url(#sl_b40)" style="mix-blend-mode:screen"/>')
    o.append(f'<g filter="url(#sl_neon)"><g transform="translate(888 176) scale(.3)" fill="none" stroke="#FFE7BE" stroke-width="11" stroke-linejoin="round"><path d="{torch}"/><path d="{flame}"/></g>'
             f'<g transform="translate(784 520) scale(.0552)" fill="#FFEFD4"><path d="{NOM_D}"/></g></g>')
    # sol, plinthe, tapis
    o.append('<rect y="830" width="1920" height="250" fill="url(#sl_sol)"/><rect y="824" width="1920" height="10" fill="#2A190E"/>')
    for y in (880, 940, 1010):
        o.append(f'<path d="M0 {y} L1920 {y}" stroke="#120A05" stroke-width="2" opacity=".6"/>')
    return f'<g filter="url(#sl_dof)">{"".join(o)}</g>'

def scene():
    o = [DEFS, fond(),
         ampoule_suspendue(640, 230), ampoule_suspendue(960, 120), ampoule_suspendue(1280, 230),
         '<ellipse cx="960" cy="985" rx="720" ry="70" fill="url(#sl_tapis)"/>',
         '<ellipse cx="960" cy="985" rx="680" ry="58" fill="none" stroke="#E2C9A6" stroke-width="3" opacity=".5" stroke-dasharray="14 10"/>',
         '<ellipse cx="560" cy="1000" rx="260" ry="26" fill="#000" opacity=".45" filter="url(#sl_b16)"/><ellipse cx="1360" cy="1000" rx="260" ry="26" fill="#000" opacity=".45" filter="url(#sl_b16)"/>',
         # fauteuil de l'invité (en miroir), vide
         f'<g transform="translate({XM} {TY}) scale({-S} {S})"><defs>{TQ.DEFS_TQ[6:-7]}</defs>{TQ.fauteuil()}</g>',
         micro_sur_pied(1250, 700, 1330, 600, 200),
         # présentateur dans son fauteuil, éclairé en chaud
         f'<g filter="url(#sl_perso)"><g transform="translate({TX} {TY}) scale({S})">{TQ.build()}</g></g>',
         micro_sur_pied(780, 700, 612, 592, -20),
         # table basse : Bible, bougies, mugs
         '<ellipse cx="960" cy="1004" rx="120" ry="12" fill="#000" opacity=".4" filter="url(#sl_b10)"/>',
         '<path d="M890 904 L880 1000 M1030 904 L1040 1000 M940 910 L936 1004 M980 910 L984 1004" stroke="#5A3820" stroke-width="9" stroke-linecap="round"/>',
         '<ellipse cx="960" cy="900" rx="160" ry="26" fill="url(#sl_table)"/><ellipse cx="960" cy="896" rx="160" ry="24" fill="#B98552"/><ellipse cx="960" cy="896" rx="150" ry="20" fill="none" stroke="#D9A36A" stroke-width="2" opacity=".6"/>',
         '<path d="M880 896 L898 878 L1008 878 L1000 896 Z" fill="#2E1A0E"/><path d="M880 896 L1000 896 L1000 904 L880 904 Z" fill="#E2C88E"/><path d="M944 882 L944 892 M938 887 L950 887" stroke="#C9A35A" stroke-width="3" stroke-linecap="round"/>',
         '<rect x="1024" y="852" width="26" height="40" rx="4" fill="#E9DCC6"/><rect x="1056" y="864" width="22" height="28" rx="4" fill="#E9DCC6"/>'
         '<ellipse cx="1050" cy="840" rx="40" ry="40" fill="#FFB860" opacity=".45" filter="url(#sl_b10)"/>'
         '<path d="M1037 836 C1043 846 1043 852 1037 856 C1031 852 1031 846 1037 836 Z" fill="#FFD27A"/><path d="M1067 850 C1072 858 1072 862 1067 866 C1062 862 1062 858 1067 850 Z" fill="#FFD27A"/>',
         f'<path d="M830 868 L872 868 L870 896 C868 900 834 900 832 896 Z" fill="#1E140D"/><g transform="translate(843 873) scale(.03)" fill="#F5EDE0" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>',
         '<rect width="1920" height="1080" fill="url(#sl_vig)"/>',
f'<g transform="translate(1590 64) scale(.045)" fill="#FFF6E8"><path d="{NOM_D}"/></g>']
    return "\n".join(o)

if __name__ == "__main__":
    body = scene()
    for n, (x, y, w, h) in VUES.items():
        out = os.path.join(ROOT, f"personnage/plateau_salon_{n}.svg")
        open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">\n{body}\n</svg>')
        print("écrit", out)
