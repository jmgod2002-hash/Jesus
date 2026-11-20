"""Studio Feu d'Élévation : le présentateur face caméra dans son studio (1920 x 1080)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P

ROOT = P.ROOT
W, H = 1920, 1080

def wordmark():
    s = open(os.path.join(ROOT, 'marque/nom_feu_d_elevation.svg')).read()
    return re.search(r' d="([^"]+)"', s).group(1)

def studio():
    torch, flame = P.logo_parts()
    name = wordmark()
    o = []
    o.append('''<defs>
 <linearGradient id="st_wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#170E08"/><stop offset="1" stop-color="#2A1A0F"/></linearGradient>
 <linearGradient id="st_slat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A2616"/><stop offset=".6" stop-color="#4A3020"/><stop offset="1" stop-color="#2C1C10"/></linearGradient>
 <radialGradient id="st_pool" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1110 470) scale(700 560)"><stop offset="0" stop-color="#F6D9AA" stop-opacity=".75"/><stop offset=".45" stop-color="#E9B678" stop-opacity=".3"/><stop offset="1" stop-color="#E9B678" stop-opacity="0"/></radialGradient>
 <radialGradient id="st_lamp" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(1790 360) scale(340 300)"><stop offset="0" stop-color="#FFC77E" stop-opacity=".7"/><stop offset="1" stop-color="#FFC77E" stop-opacity="0"/></radialGradient>
 <radialGradient id="st_neonwall" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(460 380) scale(380 330)"><stop offset="0" stop-color="#FF9A4A" stop-opacity=".38"/><stop offset="1" stop-color="#FF9A4A" stop-opacity="0"/></radialGradient>
 <linearGradient id="st_shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F9DDB0"/><stop offset="1" stop-color="#E7A35E"/></linearGradient>
 <linearGradient id="st_desk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7A5030"/><stop offset=".25" stop-color="#5A3820"/><stop offset="1" stop-color="#26160B"/></linearGradient>
 <linearGradient id="st_mic" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4A4A50"/><stop offset=".4" stop-color="#26262A"/><stop offset="1" stop-color="#0E0E10"/></linearGradient>
 <linearGradient id="st_mug" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FBF4E8"/><stop offset=".6" stop-color="#EBDDC7"/><stop offset="1" stop-color="#C9B596"/></linearGradient>
 <radialGradient id="st_vig" cx="50%" cy="48%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
 <filter id="st_dof" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080"><feGaussianBlur stdDeviation="2.2"/></filter>
 <filter id="st_b4" filterUnits="userSpaceOnUse" x="-100" y="-100" width="2120" height="1280"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="st_b10" filterUnits="userSpaceOnUse" x="-100" y="-100" width="2120" height="1280"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="st_b24" filterUnits="userSpaceOnUse" x="-100" y="-100" width="2120" height="1280"><feGaussianBlur stdDeviation="24"/></filter>
 <filter id="st_neon" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
  <feGaussianBlur in="SourceGraphic" stdDeviation="3" result="a"/>
  <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b"/>
  <feFlood flood-color="#FF8A3D"/><feComposite in2="b" operator="in" result="c"/>
  <feMerge><feMergeNode in="c"/><feMergeNode in="c"/><feMergeNode in="a"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
 <filter id="st_rim" filterUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080">
  <feOffset in="SourceAlpha" dx="-7" dy="2" result="off"/>
  <feComposite in="SourceAlpha" in2="off" operator="out" result="edge"/>
  <feGaussianBlur in="edge" stdDeviation="2.5" result="edgeb"/>
  <feFlood flood-color="#FFB46A" flood-opacity=".55"/><feComposite in2="edgeb" operator="in" result="rimc"/>
  <feComposite in="rimc" in2="SourceAlpha" operator="in" result="rim"/>
  <feBlend in="rim" in2="SourceGraphic" mode="screen"/>
 </filter>
</defs>''')
    # ---------- arrière-plan (légèrement flou : profondeur de champ) ----------
    bg = []
    bg.append(f'<rect width="{W}" height="{H}" fill="url(#st_wall)"/>')
    for x in range(-10, W, 46):   # lattes acoustiques en bois
        bg.append(f'<rect x="{x}" y="0" width="34" height="{H}" fill="url(#st_slat)"/><rect x="{x}" y="0" width="2" height="{H}" fill="#6A472B" opacity=".55"/>')
    bg.append(f'<rect width="{W}" height="{H}" fill="url(#st_pool)" style="mix-blend-mode:screen"/>')
    bg.append(f'<rect width="{W}" height="{H}" fill="url(#st_lamp)" style="mix-blend-mode:screen"/>')
    bg.append(f'<rect width="{W}" height="{H}" fill="url(#st_neonwall)" style="mix-blend-mode:screen"/>')
    # néon : torche + nom
    bg.append(f'<g filter="url(#st_neon)"><g transform="translate(372 150) scale(.42)" fill="none" stroke="#FFE7BE" stroke-width="9" stroke-linejoin="round"><path d="{torch}"/><path d="{flame}"/></g>'
              f'<g transform="translate(212 590) scale(.0784)" fill="#FFEFD4"><path d="{name}"/></g></g>')
    # étagère
    sh = []
    sh.append('<rect x="120" y="760" width="660" height="16" fill="#6B4426"/><rect x="120" y="776" width="660" height="10" fill="#3A2414"/>')
    books = [(150, 110, "#6B3A2A"), (182, 130, "#8A6A45"), (214, 98, "#3E4A3A"), (240, 124, "#C9B48A"), (272, 104, "#5A3A2A"), (300, 118, "#2F3A44")]
    for bx, bh, c in books:
        sh.append(f'<rect x="{bx}" y="{760-bh}" width="28" height="{bh}" rx="2" fill="{c}"/><rect x="{bx+4}" y="{760-bh+14}" width="20" height="3" fill="#E8D3A8" opacity=".6"/><rect x="{bx+4}" y="{760-bh+22}" width="20" height="2" fill="#E8D3A8" opacity=".4"/>')
    sh.append('<rect x="336" y="656" width="30" height="104" rx="2" fill="#7A3B2A" transform="rotate(12 351 760)"/>')
    # croix en bois
    sh.append('<rect x="420" y="620" width="18" height="140" rx="3" fill="#8A5A36"/><rect x="394" y="652" width="70" height="17" rx="3" fill="#8A5A36"/><rect x="420" y="620" width="5" height="140" fill="#B07A4C" opacity=".7"/><rect x="408" y="752" width="42" height="8" rx="2" fill="#5A3820"/>')
    # bougie
    sh.append('<rect x="500" y="708" width="44" height="52" rx="6" fill="#E9DCC6"/><rect x="500" y="708" width="44" height="10" rx="5" fill="#F7EEDF"/>'
              '<ellipse cx="522" cy="690" rx="26" ry="34" fill="#FFB860" opacity=".35" filter="url(#st_b10)"/>'
              '<path d="M522 672 C530 684 530 696 522 702 C514 696 514 684 522 672 Z" fill="#FFD27A"/><path d="M522 684 C525 690 525 696 522 699 C519 696 519 690 522 684 Z" fill="#FFF4D6"/>')
    # plante
    sh.append('<path d="M600 760 L612 700 L676 700 L688 760 Z" fill="#A0522D"/><rect x="606" y="696" width="76" height="10" rx="3" fill="#B8653A"/>')
    for ang, ln, c in ((-50, 64, "#3B5530"), (-25, 82, "#4E6B3A"), (0, 90, "#3B5530"), (22, 80, "#5A7A44"), (48, 64, "#4E6B3A"), (-70, 50, "#5A7A44"), (70, 52, "#3B5530")):
        sh.append(f'<ellipse cx="644" cy="{700-ln/2}" rx="17" ry="{ln/2}" fill="{c}" transform="rotate({ang} 644 700)"/>')
    bg.append("".join(sh))
    # lampe d'ambiance à droite
    bg.append('<rect x="1786" y="410" width="8" height="680" fill="#1A120C"/><ellipse cx="1790" cy="360" rx="150" ry="120" fill="#FFC77E" opacity=".35" filter="url(#st_b24)"/>'
              '<path d="M1730 300 L1850 300 L1880 410 L1700 410 Z" fill="url(#st_shade)"/><path d="M1700 410 L1880 410" stroke="#FFF1D8" stroke-width="3"/>')
    # bokeh
    for cx, cy, r, op in ((1560, 140, 26, .22), (1640, 230, 16, .3), (1480, 90, 12, .25), (1700, 560, 20, .18), (1600, 700, 30, .12), (90, 120, 22, .15), (820, 120, 14, .2), (1370, 200, 10, .25)):
        bg.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#FFD9A0" opacity="{op}" filter="url(#st_b4)"/>')
    o.append(f'<g filter="url(#st_dof)">{"".join(bg)}</g>')
    # ---------- présentateur, face caméra ----------
    s = 1.25; tx, ty = 1110 - 300 * s, 58 - 30 * s
    o.append(f'<ellipse cx="1110" cy="1000" rx="330" ry="40" fill="#000" opacity=".45" filter="url(#st_b24)"/>')
    o.append(f'<g filter="url(#st_rim)"><g transform="translate({tx} {ty}) scale({s})">{P.build("camera")}</g></g>')
    # ---------- bureau au premier plan ----------
    o.append(f'<path d="M0 978 L{W} 978 L{W} {H} L0 {H} Z" fill="url(#st_desk)"/><path d="M0 980 L{W} 980" stroke="#A47548" stroke-width="3" opacity=".8"/>')
    o.append('<ellipse cx="1110" cy="990" rx="380" ry="10" fill="#000" opacity=".35" filter="url(#st_b4)"/>')
    # micro de podcast sur pied de table, orienté vers lui
    o.append('<ellipse cx="796" cy="992" rx="58" ry="11" fill="#141416"/><rect x="790" y="860" width="12" height="132" fill="#2A2A2E"/><rect x="790" y="860" width="4" height="132" fill="#55555C"/>'
             '<g transform="rotate(46 806 820)"><rect x="772" y="700" width="68" height="170" rx="30" fill="url(#st_mic)" stroke="#060607" stroke-width="3"/>'
             '<rect x="776" y="704" width="60" height="78" rx="27" fill="#3A3A40"/>'
             + "".join(f'<path d="M780 {y} L832 {y}" stroke="#18181B" stroke-width="2"/>' for y in range(716, 782, 8))
             + '<rect x="772" y="788" width="68" height="10" fill="#9A7A4A"/><rect x="784" y="708" width="10" height="150" rx="5" fill="#fff" opacity=".12"/></g>')
    # mug Feu d'Élévation (torche brune)
    o.append(f'<path d="M1440 900 L1520 900 L1514 984 C1510 992 1450 992 1446 984 Z" fill="url(#st_mug)"/><ellipse cx="1480" cy="900" rx="40" ry="8" fill="#3A2213"/>'
             f'<path d="M1518 916 C1550 916 1552 962 1514 964" stroke="#E2D2B8" stroke-width="9" fill="none"/>'
             f'<g transform="translate(1466 922) scale(.06)" fill="#3B2412" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>'
             '<path d="M1470 884 C1460 868 1478 858 1468 840 M1490 884 C1500 866 1482 856 1494 836" stroke="#FFF" stroke-width="3" fill="none" opacity=".18" stroke-linecap="round" filter="url(#st_b4)"/>')
    # Bible posée à plat
    o.append('<path d="M1560 968 L1580 936 L1800 936 L1792 968 Z" fill="#3A2213"/><path d="M1560 968 L1792 968 L1792 984 L1560 984 Z" fill="#E7D2A0"/>'
             '<path d="M1560 984 L1792 984" stroke="#C9A35A" stroke-width="3"/><path d="M1650 944 L1700 944 M1675 939 L1675 962" stroke="#C9A35A" stroke-width="4" stroke-linecap="round"/>')
    # ---------- étalonnage ----------
    o.append(f'<rect width="{W}" height="{H}" fill="url(#st_vig)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="#FF9A4A" opacity=".04" style="mix-blend-mode:screen"/>')
    return "\n".join(o)

if __name__ == "__main__":
    out = os.path.join(ROOT, "personnage/studio_face_cam.svg")
    open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">\n{studio()}\n</svg>')
    print("écrit", out)
