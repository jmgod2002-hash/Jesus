"""Plateau Feu d'Élévation (DA de la marque : crème, sable, brun, lueur et braise).
Présentateur de trois quarts, assis jambes croisées dans un fauteuil, face caméra, micro sur bras articulé.
Monde 2400 x 1500 ; deux cadrages : 16:9 (YouTube) et 4:5 (carrousels)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P
import trois_quarts as TQ

ROOT = P.ROOT
VUES = {"16x9": (450, 520, 1600, 900), "4x5": (690, 0, 1200, 1500)}
S, TX, TY = 0.72, 948, 685.8          # repère du personnage -> monde
LAMPE = 820

def decor_arriere():
    torch, flame = P.logo_parts()
    d = ['<rect width="2400" height="1500" fill="url(#pl_bd)"/>',
         '<rect width="2400" height="1500" fill="url(#pl_top)"/>',
         '<rect width="2400" height="1500" fill="url(#pl_lueur)" style="mix-blend-mode:screen"/>',
         '<rect width="2400" height="1500" fill="url(#pl_braise)"/>']
    # rectangle de lumière au mur, avec l'ombre projetée de la torche
    d.append('<polygon points="660,560 1600,520 1620,850 680,890" fill="#FFF3E0" opacity=".32" filter="url(#pl_b10)" style="mix-blend-mode:screen"/>')
    d.append(f'<g transform="translate(1420 586) rotate(-2) scale(.3)" fill="#8A5A36" opacity=".07" filter="url(#pl_b2)" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>')
    d.append('<rect y="1060" width="2400" height="440" fill="url(#pl_floor)"/>')
    # tapis et ombres au sol
    d.append('<ellipse cx="1320" cy="1388" rx="720" ry="82" fill="#F8F2E8" filter="url(#pl_b2)"/>')
    d.append('<ellipse cx="1320" cy="1388" rx="720" ry="82" fill="url(#pl_rugtex)" opacity=".6"/>')
    d.append('<ellipse cx="1190" cy="1398" rx="330" ry="32" fill="#3B2412" opacity=".28" filter="url(#pl_b14)"/>')
    d.append('<ellipse cx="1790" cy="1388" rx="110" ry="16" fill="#3B2412" opacity=".25" filter="url(#pl_b10)"/>')
    d.append(f'<ellipse cx="{LAMPE}" cy="1384" rx="140" ry="18" fill="#3B2412" opacity=".18" filter="url(#pl_b10)"/>')
    d.append('<ellipse cx="1565" cy="1394" rx="80" ry="12" fill="#3B2412" opacity=".25" filter="url(#pl_b10)"/>')
    # lampadaire trépied
    L0 = LAMPE
    d.append(f'<ellipse cx="{L0}" cy="660" rx="340" ry="290" fill="#FFD9A8" opacity=".5" filter="url(#pl_b40)" style="mix-blend-mode:screen"/>')
    for (dx, y2, c) in ((22, 1336, "#A86F3E"), (-100, 1388, "#C98A50"), (108, 1382, "#C98A50")):
        d.append(f'<path d="M{L0} 736 L{L0+dx} {y2}" stroke="{c}" stroke-width="15" stroke-linecap="round"/>')
        d.append(f'<path d="M{L0-4} 740 L{L0+dx-4} {y2-2}" stroke="#E2AC74" stroke-width="3" stroke-linecap="round" opacity=".7"/>')
    d.append(f'<rect x="{L0-9}" y="712" width="18" height="34" rx="4" fill="#B07A48"/>')
    d.append(f'<path d="M{L0-110} 572 C{L0-110} 562 {L0+110} 562 {L0+110} 572 L{L0+110} 718 C{L0+110} 730 {L0-110} 730 {L0-110} 718 Z" fill="url(#pl_shade)"/>')
    d.append(f'<path d="M{L0-110} 572 C{L0-110} 562 {L0+110} 562 {L0+110} 572 L{L0+110} 718 C{L0+110} 730 {L0-110} 730 {L0-110} 718 Z" fill="none" stroke="#D8C3A6" stroke-width="2"/>')
    d.append(f'<ellipse cx="{L0}" cy="718" rx="110" ry="12" fill="#FFF3DA"/>')
    d.append(f'<path d="M{L0+82} 574 L{L0+82} 716" stroke="#D9C6B0" stroke-width="18" opacity=".5" filter="url(#pl_b4)"/>')
    # guéridon crème avec livres, fleurs séchées aux tons braise, photophore
    T = 1790
    d.append(f'<path d="M{T-68} 1170 C{T-62} 1260 {T-54} 1330 {T-60} 1386 L{T+60} 1386 C{T+54} 1330 {T+62} 1260 {T+68} 1170 Z" fill="url(#pl_table)"/>')
    d.append(f'<ellipse cx="{T}" cy="1386" rx="64" ry="9" fill="#DCCDB8"/>')
    d.append(f'<path d="M{T-140} 1150 L{T-140} 1170 C{T-140} 1182 {T+140} 1182 {T+140} 1170 L{T+140} 1150 Z" fill="#E6D9C6"/>')
    d.append(f'<ellipse cx="{T}" cy="1150" rx="140" ry="20" fill="#FBF6EE"/>')
    d.append(f'<path d="M{T-114} 1146 L{T+8} 1146 L{T+12} 1132 L{T-110} 1132 Z" fill="#8A5A36"/><path d="M{T-108} 1132 L{T+4} 1132 L{T+8} 1118 L{T-104} 1118 Z" fill="#F1E6D4"/><path d="M{T-108} 1132 L{T+4} 1132" stroke="#B5A48C" stroke-width="2"/>')
    d.append(f'<path d="M{T-76} 1118 L{T-64} 1070 L{T-16} 1070 L{T-4} 1118 Z" fill="#C9B79C"/><path d="M{T-76} 1118 L{T-64} 1070 L{T-52} 1070 L{T-62} 1118 Z" fill="#DCCDB4"/>')
    for (fx, fy, r, col) in ((-62, 1046, 13, "#D9875C"), (-40, 1036, 15, "#F2C9A0"), (-18, 1046, 13, "#C0522B"), (-50, 1058, 11, "#F5DDBE"), (-28, 1058, 12, "#D9875C"), (-76, 1060, 9, "#F2C9A0"), (-4, 1060, 9, "#C0522B")):
        d.append(f'<circle cx="{T+fx}" cy="{fy}" r="{r}" fill="{col}"/><circle cx="{T+fx-3}" cy="{fy-3}" r="{r*.35:.1f}" fill="#FFF" opacity=".45"/>')
    d.append(f'<path d="M{T-72} 1066 C{T-86} 1050 {T-92} 1030 {T-90} 1006 M{T-8} 1066 C{T+6} 1048 {T+12} 1028 {T+10} 1004" stroke="#B89A6A" stroke-width="4" fill="none" stroke-linecap="round"/>')
    d.append(f'<rect x="{T+42}" y="1106" width="46" height="40" rx="6" fill="#B8A890"/><path d="M{T+46} 1116 L{T+84} 1116 M{T+46} 1126 L{T+84} 1126 M{T+46} 1136 L{T+84} 1136" stroke="#D8CBB6" stroke-width="3" stroke-dasharray="4 4"/>')
    d.append(f'<ellipse cx="{T+65}" cy="1104" rx="20" ry="18" fill="#FFC77E" opacity=".45" filter="url(#pl_b10)"/>')
    # pied du micro (au sol, entre le fauteuil et le guéridon)
    for (x2, y2) in ((1505, 1398), (1628, 1396), (1575, 1380)):
        d.append(f'<path d="M1565 1300 L{x2} {y2}" stroke="#1A1714" stroke-width="7" stroke-linecap="round"/>')
    d.append('<rect x="1559" y="900" width="12" height="404" fill="#22201D"/><rect x="1559" y="900" width="4" height="404" fill="#5A5650"/>')
    return "".join(d)

def micro():
    """Bras articulé + micro dynamique orienté vers la bouche (coordonnées du monde)."""
    m = []
    # bras (avec contrepoids derrière le pivot) et câble
    m.append('<path d="M1650 838 L1565 900 L1346 1034" stroke="#1C1A18" stroke-width="13" stroke-linecap="round" fill="none"/>')
    m.append('<path d="M1650 834 L1565 896 L1348 1028" stroke="#5E5A54" stroke-width="3" stroke-linecap="round" fill="none"/>')
    m.append('<path d="M1600 868 L1520 926 M1470 962 L1400 1012" stroke="#2E2B28" stroke-width="5" stroke-dasharray="4 5" fill="none"/>')
    m.append('<circle cx="1565" cy="898" r="11" fill="#2A2724" stroke="#0E0D0C" stroke-width="3"/>')
    m.append('<rect x="1640" y="826" width="34" height="24" rx="5" fill="#2A2724" transform="rotate(-36 1657 838)"/>')
    m.append('<path d="M1350 1040 C1420 1064 1470 1020 1520 970" stroke="#111" stroke-width="3" fill="none" opacity=".8"/>')
    # micro (dessiné horizontal, grille à gauche, puis tourné vers la bouche)
    m.append('<g transform="translate(1306 1000) rotate(22)">'
             '<path d="M20 26 C26 44 26 52 40 58" stroke="#1C1A18" stroke-width="9" fill="none" stroke-linecap="round"/>'
             '<rect x="-62" y="-25" width="124" height="50" rx="22" fill="url(#pl_mic)" stroke="#060606" stroke-width="3"/>'
             '<rect x="-62" y="-25" width="54" height="50" rx="22" fill="#2B2B2E"/>'
             + "".join(f'<path d="M{x} -20 L{x} 20" stroke="#121214" stroke-width="2"/>' for x in range(-54, -10, 6))
             + '<rect x="-12" y="-25" width="8" height="50" fill="#8A6A40"/>'
             '<rect x="-56" y="-19" width="110" height="7" rx="3.5" fill="#FFF" opacity=".14"/>'
             '<path d="M-6 25 L-6 34 L30 34 L30 25" stroke="#1C1A18" stroke-width="6" fill="none"/></g>')
    return "".join(m)

def premier_plan():
    return ('<ellipse cx="300" cy="1480" rx="620" ry="260" fill="#8A4A2A" opacity=".4" filter="url(#pl_b80)"/>'
            '<ellipse cx="2250" cy="1520" rx="520" ry="170" fill="#B98552" opacity=".38" filter="url(#pl_b80)"/>'
            '<rect width="2400" height="1500" fill="url(#pl_vig)"/>')

DEFS = '''<defs>
 <linearGradient id="pl_bd" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#D9C19C"/><stop offset=".48" stop-color="#F5EDE0"/><stop offset="1" stop-color="#E6D2B2"/></linearGradient>
 <radialGradient id="pl_top" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(250 0) scale(1200 900)"><stop offset="0" stop-color="#A9855C" stop-opacity=".45"/><stop offset="1" stop-color="#A9855C" stop-opacity="0"/></radialGradient>
 <radialGradient id="pl_lueur" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1250 700) scale(820 640)"><stop offset="0" stop-color="#FFFBF3" stop-opacity=".55"/><stop offset="1" stop-color="#FFFBF3" stop-opacity="0"/></radialGradient>
 <radialGradient id="pl_braise" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(200 1500) scale(1000 760)"><stop offset="0" stop-color="#C0522B" stop-opacity=".45"/><stop offset="1" stop-color="#C0522B" stop-opacity="0"/></radialGradient>
 <linearGradient id="pl_floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#CDB592" stop-opacity="0"/><stop offset=".45" stop-color="#CDB592" stop-opacity=".45"/><stop offset="1" stop-color="#A9855C" stop-opacity=".75"/></linearGradient>
 <radialGradient id="pl_vig" cx="50%" cy="50%" r="72%"><stop offset=".6" stop-color="#3B2412" stop-opacity="0"/><stop offset="1" stop-color="#3B2412" stop-opacity=".32"/></radialGradient>
 <linearGradient id="pl_shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFDF8"/><stop offset="1" stop-color="#F4E8D8"/></linearGradient>
 <linearGradient id="pl_table" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FDF9F2"/><stop offset=".6" stop-color="#EFE5D6"/><stop offset="1" stop-color="#D6C6AE"/></linearGradient>
 <linearGradient id="pl_mic" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4A4A50"/><stop offset=".45" stop-color="#26262A"/><stop offset="1" stop-color="#0E0E10"/></linearGradient>
 <pattern id="pl_rugtex" width="10" height="6" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.6" fill="#E3D6C3"/><circle cx="7" cy="4" r="1.4" fill="#FFFFFF"/></pattern>
 <filter id="pl_b2" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="2"/></filter>
 <filter id="pl_b4" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="pl_b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="pl_b14" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="14"/></filter>
 <filter id="pl_b40" filterUnits="userSpaceOnUse" x="-200" y="-200" width="2800" height="1900"><feGaussianBlur stdDeviation="40"/></filter>
 <filter id="pl_b80" filterUnits="userSpaceOnUse" x="-400" y="-400" width="3200" height="2300"><feGaussianBlur stdDeviation="80"/></filter>
</defs>'''

def scene():
    return (DEFS + decor_arriere()
            + f'<g transform="translate({TX} {TY}) scale({S})">{TQ.build()}</g>'
            + micro() + premier_plan())

if __name__ == "__main__":
    body = scene()
    for nom, (x, y, w, h) in VUES.items():
        out = os.path.join(ROOT, f"personnage/plateau_{nom}.svg")
        open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">\n{body}\n</svg>')
        print("écrit", out)
