"""Plateau de nuit Feu d'Élévation (sur le modèle des Lueurs) : studio sombre, torche en néon, ampoules à filament,
ville floue derrière la vitre, bureau en bois, deux micros sur bras ; présentateur à gauche, place de l'invité à droite.
Repère 1920 x 1080 ; cadrages 16:9 et 9:16 (Shorts, sur le présentateur)."""
import os, re, sys, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P
import trois_quarts as TQ

ROOT = P.ROOT
VUES = {"16x9": (0, 0, 1920, 1080), "9x16": (345, 0, 608, 1080)}
torch, flame = P.logo_parts()
nom = open(os.path.join(ROOT, 'marque/nom_feu_d_elevation.svg')).read()
NOM_D = re.search(r' d="([^"]+)"', nom).group(1)

def filament(x, y):
    pts = " ".join(f"L{x + (7 if i % 2 else -7)} {y + 34 - i * 5}" for i in range(1, 14))
    return (f'<path d="M{x-4} {y+44} L{x-4} {y+34} {pts} L{x+4} {y-36}" stroke="#FFF1C8" stroke-width="2.6" fill="none" stroke-linejoin="round" filter="url(#n_glow)"/>'
            f'<path d="M{x+4} {y-36} C{x+18} {y-20} {x+18} {y+20} {x+4} {y+44}" stroke="#FFE2A8" stroke-width="1.5" fill="none" opacity=".7"/>')

def ampoule(x, ybulb, ydesk):
    return (f'<ellipse cx="{x}" cy="{ybulb}" rx="150" ry="150" fill="#FFB050" opacity=".28" filter="url(#n_b40)" style="mix-blend-mode:screen"/>'
            f'<path d="M{x} {ybulb+70} L{x} {ydesk-30}" stroke="#7A5232" stroke-width="10"/>'
            f'<path d="M{x-46} {ydesk} L{x} {ydesk-60} L{x+46} {ydesk}" stroke="#8A5A36" stroke-width="9" fill="none" stroke-linejoin="round"/>'
            f'<rect x="{x-12}" y="{ybulb+44}" width="24" height="28" rx="4" fill="#5A3E26"/>'
            f'<ellipse cx="{x}" cy="{ybulb}" rx="44" ry="54" fill="#FFCF8A" opacity=".18" stroke="#FFE2B0" stroke-opacity=".35" stroke-width="2"/>'
            + filament(x, ybulb) +
            f'<ellipse cx="{x}" cy="{ybulb}" rx="20" ry="26" fill="#FFC36A" opacity=".55" filter="url(#n_b10)"/>')

def micro(cx, cy, angle, bras):
    s = f'<path d="{bras}" stroke="#151312" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    s += f'<path d="{bras}" stroke="#4A4642" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round" transform="translate(-2 -3)"/>'
    s += (f'<g transform="translate({cx} {cy}) rotate({angle})">'
          '<rect x="-60" y="-24" width="120" height="48" rx="22" fill="url(#n_mic)" stroke="#050505" stroke-width="3"/>'
          '<rect x="-60" y="-24" width="52" height="48" rx="22" fill="#26262A"/>'
          + "".join(f'<path d="M{x} -19 L{x} 19" stroke="#0E0E10" stroke-width="2"/>' for x in range(-52, -10, 6))
          + '<rect x="-10" y="-24" width="8" height="48" fill="#C0522B"/>'
          '<rect x="-54" y="-18" width="106" height="6" rx="3" fill="#FFB46A" opacity=".25"/></g>')
    return s

def fond():
    o = ['<rect width="1920" height="1080" fill="url(#n_mur)"/>']
    # baie vitrée sur la ville de nuit (floue)
    rnd = random.Random(7)
    b = ['<rect x="960" y="70" width="900" height="700" fill="#0B0B14"/>']
    for _ in range(90):
        x = rnd.uniform(970, 1850); y = rnd.uniform(260, 760); r = rnd.uniform(6, 22)
        c = rnd.choice(["#FFB45A", "#FF6A4A", "#FFE2B0", "#E05A3A", "#FFD27A", "#9FB4FF"])
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{c}" opacity="{rnd.uniform(.25, .7):.2f}"/>')
    o.append(f'<g filter="url(#n_bokeh)">{"".join(b)}</g>')
    o.append('<rect x="960" y="70" width="900" height="700" fill="url(#n_vitre)"/>')
    for x in (960, 1185, 1410, 1635, 1860):
        o.append(f'<rect x="{x-7}" y="62" width="14" height="716" fill="#0A0705"/>')
    o.append('<rect x="953" y="400" width="914" height="12" fill="#0A0705"/><rect x="953" y="62" width="914" height="14" fill="#0A0705"/>')
    # torche et nom en néon au mur
    o.append(f'<g filter="url(#n_neon)"><g transform="translate(120 86) scale(.32)" fill="none" stroke="#FFE7BE" stroke-width="10" stroke-linejoin="round"><path d="{torch}"/><path d="{flame}"/></g>'
             f'<g transform="translate(44 420) scale(.046)" fill="#FFEFD4"><path d="{NOM_D}"/></g></g>')
    o.append('<ellipse cx="240" cy="300" rx="280" ry="260" fill="#FF8A3D" opacity=".16" filter="url(#n_b40)" style="mix-blend-mode:screen"/>')
    return f'<g filter="url(#n_dof)">{"".join(o)}</g>'

def fauteuil_invite():
    o = ['<path d="M1318 540 C1318 500 1348 482 1388 482 L1488 482 C1528 482 1556 502 1556 540 L1560 846 L1314 846 Z" fill="url(#n_cuir)"/>']
    for x in (1370, 1437, 1504):
        for y in (540, 620, 700):
            o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#0E0804"/><path d="M{x-30} {y+40} L{x} {y} L{x+30} {y+40}" stroke="#120A06" stroke-width="2" fill="none" opacity=".5"/>')
    o.append('<path d="M1340 512 C1352 498 1372 494 1392 494 L1470 494" stroke="#8A5A36" stroke-width="5" fill="none" opacity=".7" stroke-linecap="round"/>')
    o.append('<path d="M1318 540 C1318 500 1348 482 1388 482 L1488 482 C1528 482 1556 502 1556 540 L1560 846 L1314 846 Z" fill="none" stroke="#0A0604" stroke-width="4"/>')
    o.append('<rect x="1276" y="700" width="60" height="146" rx="24" fill="#24160C" stroke="#0A0604" stroke-width="4"/><rect x="1540" y="700" width="60" height="146" rx="24" fill="#1A0F08" stroke="#0A0604" stroke-width="4"/>')
    o.append('<path d="M1288 712 C1300 706 1316 706 1326 712" stroke="#6B4426" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return "".join(o)

def bureau():
    o = ['<path d="M-20 826 L1940 826 L1940 1090 L-20 1090 Z" fill="url(#n_bois)"/>',
         '<path d="M-20 828 L1940 828" stroke="#E0A86A" stroke-width="3" opacity=".7"/>']
    for y in (864, 910, 968, 1030):
        o.append(f'<path d="M-20 {y} C400 {y-6} 900 {y+8} 1940 {y-4}" stroke="#6B4426" stroke-width="2" fill="none" opacity=".45"/>')
    # fiches de l'animateur
    o.append('<path d="M330 872 L600 858 L612 922 L338 936 Z" fill="#F3ECE0"/><path d="M360 886 L560 876 M362 900 L540 891 M364 914 L520 906" stroke="#8A7A66" stroke-width="3"/>')
    o.append('<path d="M300 900 L540 910 L530 970 L292 958 Z" fill="#FBF6EE" opacity=".95"/>')
    # mugs à la torche
    for (x, y) in ((200, 806), (1640, 812)):
        o.append(f'<path d="M{x} {y} L{x+70} {y} L{x+66} {y+78} C{x+62} {y+86} {x+8} {y+86} {x+4} {y+78} Z" fill="#1E140D"/><ellipse cx="{x+35}" cy="{y}" rx="35" ry="7" fill="#3B2412"/>'
                 f'<path d="M{x+68} {y+16} C{x+96} {y+16} {x+98} {y+58} {x+64} {y+60}" stroke="#1E140D" stroke-width="8" fill="none"/>'
                 f'<g transform="translate({x+24} {y+20}) scale(.05)" fill="#F5EDE0" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>')
    # Bible fermée
    o.append('<path d="M1000 876 L1028 846 L1232 846 L1222 876 Z" fill="#2E1A0E"/><path d="M1000 876 L1222 876 L1222 892 L1000 892 Z" fill="#E2C88E"/><path d="M1100 852 L1100 870 M1088 860 L1112 860" stroke="#C9A35A" stroke-width="4" stroke-linecap="round"/>')
    return "".join(o)

DEFS = '''<defs>
 <linearGradient id="n_mur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140B06"/><stop offset="1" stop-color="#24150B"/></linearGradient>
 <linearGradient id="n_vitre" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".05"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".04"/></linearGradient>
 <linearGradient id="n_bois" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B98552"/><stop offset=".35" stop-color="#8A5A36"/><stop offset="1" stop-color="#3A2414"/></linearGradient>
 <linearGradient id="n_cuir" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4A2E1C"/><stop offset=".5" stop-color="#2C1A0F"/><stop offset="1" stop-color="#160D07"/></linearGradient>
 <linearGradient id="n_mic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4A50"/><stop offset=".45" stop-color="#232327"/><stop offset="1" stop-color="#0A0A0C"/></linearGradient>
 <radialGradient id="n_vig" cx="50%" cy="50%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
 <filter id="n_b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="n_b40" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="n_bokeh" filterUnits="userSpaceOnUse" x="900" y="0" width="1100" height="900"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="n_dof" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><feGaussianBlur stdDeviation="1.6"/></filter>
 <filter id="n_glow" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2400" height="1500"><feGaussianBlur in="SourceGraphic" stdDeviation="3" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="n_neon" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="a"/><feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b"/>
  <feFlood flood-color="#FF8A3D"/><feComposite in2="b" operator="in" result="c"/>
  <feMerge><feMergeNode in="c"/><feMergeNode in="c"/><feMergeNode in="a"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="n_perso" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1100" height="1400">
  <feColorMatrix type="matrix" values=".93 0 0 0 0  0 .84 0 0 0  0 0 .74 0 0  0 0 0 1 0" result="tinte"/>
  <feOffset in="SourceAlpha" dx="8" dy="-2" result="off"/>
  <feComposite in="SourceAlpha" in2="off" operator="out" result="bord"/>
  <feGaussianBlur in="bord" stdDeviation="2.5" result="bordf"/>
  <feFlood flood-color="#FFB050" flood-opacity=".7"/><feComposite in2="bordf" operator="in" result="rim"/>
  <feComposite in="rim" in2="SourceAlpha" operator="in" result="rim2"/>
  <feBlend in="rim2" in2="tinte" mode="screen"/></filter>
</defs>'''

def scene():
    s, tx, ty = 0.95, 560 - 336 * 0.95, 420 - 280 * 0.95
    o = [DEFS, fond(),
         ampoule(960, 590, 840), ampoule(1760, 560, 840),
         fauteuil_invite(),
         micro(1340, 610, 160, "M1375 625 L1470 700 L1560 835"),
         f'<g filter="url(#n_perso)"><g transform="translate({tx:.1f} {ty:.1f}) scale({s})">{TQ.build(avec_fauteuil=False)}</g></g>',
         micro(668, 572, 20, "M700 590 L770 690 L820 834"),
         bureau(),
         ampoule(110, 640, 850),
         f'<g transform="translate(1590 40) scale(.045)" fill="#FFF6E8" opacity=".9"><path d="{NOM_D}"/></g>',
         '<rect width="1920" height="1080" fill="url(#n_vig)"/>']
    return "\n".join(o)

if __name__ == "__main__":
    body = scene()
    for n, (x, y, w, h) in VUES.items():
        out = os.path.join(ROOT, f"personnage/plateau_nuit_{n}.svg")
        open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">\n{body}\n</svg>')
        print("écrit", out)
