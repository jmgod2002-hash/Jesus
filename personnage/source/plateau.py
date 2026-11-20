"""Plateau Feu d'Élévation : le présentateur assis dans un fauteuil, face caméra, sur un plateau photo épuré
(fond coloré en dégradé, rectangle de lumière, lampadaire trépied, guéridon, tapis). Monde 2400 x 1500."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P

ROOT = P.ROOT
VUES = {"16x9": (450, 520, 1600, 900), "4x5": (650, 0, 1200, 1500)}
S, TX, TY = 0.72, 1250 - 300 * 0.72, 1395 - 970 * 0.72   # pieds du personnage posés à (1250, 1395)

def fauteuil():
    """Fauteuil en bouclette crème, repère du personnage (600 x 1000). L'assise arrive sous les hanches."""
    c = []
    c.append('<rect x="6" y="840" width="22" height="116" rx="6" fill="#B98552"/><rect x="572" y="840" width="22" height="116" rx="6" fill="#9A6A3E"/>')
    for shape in ('<rect x="24" y="496" width="552" height="270" rx="96"/>',      # dossier
                  '<rect x="110" y="746" width="380" height="104" rx="26"/>',     # assise
                  '<rect x="-24" y="610" width="160" height="256" rx="64"/>',     # accoudoir gauche
                  '<rect x="464" y="610" width="160" height="256" rx="64"/>'):    # accoudoir droit
        c.append(shape.replace('/>', ' fill="url(#pl_chair)"/>'))
        c.append(shape.replace('/>', ' fill="url(#pl_boucle)"/>'))
        c.append(shape.replace('/>', ' fill="none" stroke="#CDBBA5" stroke-width="2"/>'))
    c.append('<rect x="110" y="746" width="380" height="30" rx="14" fill="#000" opacity=".12" filter="url(#b8)"/>')
    c.append('<rect x="126" y="610" width="22" height="256" fill="#000" opacity=".12" filter="url(#b8)"/><rect x="452" y="610" width="22" height="256" fill="#000" opacity=".16" filter="url(#b8)"/>')
    # plaid drapé sur l'accoudoir gauche
    c.append('<path d="M-34 628 C-2 606 96 606 140 632 L146 702 C132 760 122 820 114 890 C80 900 30 898 -14 890 C-10 820 -18 760 -36 702 Z" fill="#E7B4A2"/>'
             '<path d="M10 660 C18 730 16 810 12 886 M60 656 C68 730 66 810 62 892 M108 660 C110 720 106 780 100 840" stroke="#C98E7A" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>'
             '<path d="M-34 628 C-2 606 96 606 140 632" stroke="#F6D2C4" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return "".join(c)

def decor_arriere():
    d = []
    d.append('<rect width="2400" height="1500" fill="url(#pl_bd)"/>')
    d.append('<rect width="2400" height="1500" fill="url(#pl_top)"/>')
    d.append('<rect width="2400" height="1500" fill="url(#pl_warm)" style="mix-blend-mode:screen"/>')
    # rectangle de lumière projeté sur le mur
    d.append('<polygon points="640,560 1580,520 1600,850 660,890" fill="#FFD9B0" opacity=".34" filter="url(#pl_b10)" style="mix-blend-mode:screen"/>')
    d.append('<rect width="2400" height="1500" fill="url(#pl_mag)"/>')
    d.append('<rect y="1060" width="2400" height="440" fill="url(#pl_floor)"/>')
    # tapis
    d.append('<ellipse cx="1320" cy="1388" rx="720" ry="82" fill="#F3EEF2" filter="url(#pl_b2)"/>')
    d.append('<ellipse cx="1320" cy="1388" rx="720" ry="82" fill="url(#pl_rugtex)" opacity=".6"/>')
    d.append('<ellipse cx="1260" cy="1396" rx="340" ry="34" fill="#5A2340" opacity=".32" filter="url(#pl_b14)"/>')
    d.append('<ellipse cx="1690" cy="1388" rx="110" ry="16" fill="#5A2340" opacity=".3" filter="url(#pl_b10)"/>')
    d.append('<ellipse cx="800" cy="1384" rx="140" ry="18" fill="#5A2340" opacity=".22" filter="url(#pl_b10)"/>')
    # lampadaire trépied
    d.append('<ellipse cx="790" cy="660" rx="340" ry="290" fill="#FFE3BE" opacity=".5" filter="url(#pl_b40)" style="mix-blend-mode:screen"/>')
    for (x2, y2, c) in ((812, 1336, "#A86F3E"), (690, 1388, "#C98A50"), (898, 1382, "#C98A50")):
        d.append(f'<path d="M790 736 L{x2} {y2}" stroke="{c}" stroke-width="15" stroke-linecap="round"/>')
        d.append(f'<path d="M786 740 L{x2-4} {y2-2}" stroke="#E2AC74" stroke-width="3" stroke-linecap="round" opacity=".7"/>')
    d.append('<rect x="781" y="712" width="18" height="34" rx="4" fill="#B07A48"/>')
    d.append('<path d="M680 572 C680 562 900 562 900 572 L900 718 C900 730 680 730 680 718 Z" fill="url(#pl_shade)"/>')
    d.append('<ellipse cx="790" cy="718" rx="110" ry="12" fill="#FFF3DA"/>')
    d.append('<path d="M872 574 L872 716" stroke="#D9C6B0" stroke-width="18" opacity=".5" filter="url(#pl_b4)"/>')
    # guéridon blanc
    d.append('<path d="M1612 1170 C1618 1260 1626 1330 1620 1386 L1740 1386 C1734 1330 1742 1260 1748 1170 Z" fill="url(#pl_table)"/>')
    d.append('<ellipse cx="1680" cy="1386" rx="64" ry="9" fill="#D9D1D6"/>')
    d.append('<path d="M1540 1150 L1540 1170 C1540 1182 1820 1182 1820 1170 L1820 1150 Z" fill="#E4DCE1"/>')
    d.append('<ellipse cx="1680" cy="1150" rx="140" ry="20" fill="#FBF8FA"/>')
    # livres, pot de fleurs roses, photophore
    d.append('<path d="M1566 1146 L1688 1146 L1692 1132 L1570 1132 Z" fill="#C9C1B8"/><path d="M1572 1132 L1684 1132 L1688 1118 L1576 1118 Z" fill="#F1ECE6"/><path d="M1572 1132 L1684 1132" stroke="#B5ACA2" stroke-width="2"/>')
    d.append('<path d="M1604 1118 L1616 1070 L1664 1070 L1676 1118 Z" fill="#BDB6AF"/><path d="M1604 1118 L1616 1070 L1628 1070 L1618 1118 Z" fill="#D2CCC6"/>')
    for (fx, fy, r, col) in ((1618, 1046, 13, "#F5A3C0"), (1640, 1036, 15, "#F7C6D6"), (1662, 1046, 13, "#EF8FB0"), (1630, 1058, 11, "#F9D3E0"), (1652, 1058, 12, "#F5A3C0"), (1604, 1060, 9, "#F7C6D6"), (1676, 1060, 9, "#EF8FB0")):
        d.append(f'<circle cx="{fx}" cy="{fy}" r="{r}" fill="{col}"/><circle cx="{fx-3}" cy="{fy-3}" r="{r*.35:.1f}" fill="#FFF" opacity=".5"/>')
    d.append('<path d="M1608 1066 C1596 1056 1590 1046 1592 1036 M1672 1066 C1684 1054 1690 1044 1688 1034" stroke="#6E8A55" stroke-width="5" fill="none" stroke-linecap="round"/>')
    d.append('<rect x="1722" y="1106" width="46" height="40" rx="6" fill="#A9A3A8"/><path d="M1726 1116 L1764 1116 M1726 1126 L1764 1126 M1726 1136 L1764 1136" stroke="#C8C2C6" stroke-width="3" stroke-dasharray="4 4"/>')
    d.append('<ellipse cx="1745" cy="1104" rx="20" ry="18" fill="#FFD9A0" opacity=".35" filter="url(#pl_b10)"/>')
    return "".join(d)

def premier_plan():
    return ('<ellipse cx="300" cy="1480" rx="620" ry="260" fill="#F2559F" opacity=".55" filter="url(#pl_b80)"/>'
            '<ellipse cx="2250" cy="1520" rx="520" ry="170" fill="#B48BE8" opacity=".45" filter="url(#pl_b80)"/>'
            '<rect width="2400" height="1500" fill="url(#pl_vig)"/>')

DEFS = '''<defs>
 <linearGradient id="pl_bd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D23E4E"/><stop offset=".45" stop-color="#EA6651"/><stop offset="1" stop-color="#F2894F"/></linearGradient>
 <radialGradient id="pl_top" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(300 0) scale(1200 900)"><stop offset="0" stop-color="#A82A45" stop-opacity=".55"/><stop offset="1" stop-color="#A82A45" stop-opacity="0"/></radialGradient>
 <radialGradient id="pl_warm" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1500 640) scale(950 760)"><stop offset="0" stop-color="#F9AC66" stop-opacity=".6"/><stop offset="1" stop-color="#F9AC66" stop-opacity="0"/></radialGradient>
 <radialGradient id="pl_mag" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(200 1500) scale(1000 760)"><stop offset="0" stop-color="#F04A97" stop-opacity=".85"/><stop offset="1" stop-color="#F04A97" stop-opacity="0"/></radialGradient>
 <linearGradient id="pl_floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E9A0D6" stop-opacity="0"/><stop offset=".45" stop-color="#E9A0D6" stop-opacity=".45"/><stop offset="1" stop-color="#B98BE6" stop-opacity=".8"/></linearGradient>
 <radialGradient id="pl_vig" cx="50%" cy="50%" r="72%"><stop offset=".6" stop-color="#3A0F26" stop-opacity="0"/><stop offset="1" stop-color="#3A0F26" stop-opacity=".35"/></radialGradient>
 <linearGradient id="pl_shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFDF8"/><stop offset="1" stop-color="#F4E8D8"/></linearGradient>
 <linearGradient id="pl_table" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FCFAFB"/><stop offset=".6" stop-color="#ECE6EA"/><stop offset="1" stop-color="#D2C8CF"/></linearGradient>
 <linearGradient id="pl_chair" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F8F2EA"/><stop offset=".6" stop-color="#EDE3D6"/><stop offset="1" stop-color="#D9CAB7"/></linearGradient>
 <pattern id="pl_boucle" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.9" fill="#D6C5AF" opacity=".55"/><circle cx="7" cy="6.5" r="1.9" fill="#FFFFFF" opacity=".55"/></pattern>
 <pattern id="pl_rugtex" width="10" height="6" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#D9CCD6"/><circle cx="7" cy="4" r="1.4" fill="#FFFFFF"/></pattern>
 <filter id="pl_b2" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="2"/></filter>
 <filter id="pl_b4" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="pl_b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="pl_b14" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="14"/></filter>
 <filter id="pl_b24" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="24"/></filter>
 <filter id="pl_b40" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="pl_b80" filterUnits="userSpaceOnUse" x="-400" y="-400" width="3200" height="2300"><feGaussianBlur stdDeviation="80"/></filter>
 <filter id="pl_rim" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400">
  <feOffset in="SourceAlpha" dx="-8" dy="2" result="off"/>
  <feComposite in="SourceAlpha" in2="off" operator="out" result="edge"/>
  <feGaussianBlur in="edge" stdDeviation="2.5" result="edgeb"/>
  <feFlood flood-color="#FF9C7A" flood-opacity=".5"/><feComposite in2="edgeb" operator="in" result="rimc"/>
  <feComposite in="rimc" in2="SourceAlpha" operator="in" result="rim"/>
  <feBlend in="rim" in2="SourceGraphic" mode="screen"/>
 </filter>
</defs>'''

def scene():
    return (DEFS + decor_arriere()
            + f'<g transform="translate({TX:.1f} {TY:.1f}) scale({S})">{fauteuil()}'
            + f'{P.build("camera", "assis")}</g>'
            + premier_plan())

if __name__ == "__main__":
    body = scene()
    for nom, (x, y, w, h) in VUES.items():
        out = os.path.join(ROOT, f"personnage/plateau_{nom}.svg")
        open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">\n{body}\n</svg>')
        print("écrit", out)
