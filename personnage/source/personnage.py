"""Personnage présentateur Feu d'Élévation : génère le SVG du personnage (repère 600 x 1000)."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def logo_parts():
    d = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, 'youtube/logo.svg')).read()).group(1)
    subs = re.findall(r'M[^M]+', d)
    return "".join(subs[:12]), "".join(subs[12:])   # torche, flamme

L = "#24160D"
K = dict(skin="#D39A6C", skinS="#A86E45", skinD="#8A5634", skinL="#F0C29A", blush="#E07A5F",
         hair="#3A2213", hairS="#1E1209", hairL="#6E4426", hairX="#A0714A",
         jack="#7B4F2E", jackS="#4F301A", jackL="#A47548",
         shirt="#FBF6EE", shirtS="#D9CBB6", tie="#C0522B", tieS="#842F16", tieL="#E57E50",
         pants="#3A2C22", pantsS="#1F1610", pantsL="#5E4A3A", shoe="#2A1A10", shoeL="#7A5C48",
         frame="#1E120A", gold="#D9A04A")
ST = f'stroke="{L}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'

_n = [0]
def zone(path, inner, outline=True, fill=None):
    """Remplit une forme, y peint ombres/reflets flous confinés à la forme, puis trace le contour."""
    _n[0] += 1; cid = f"z{_n[0]}"
    out = f'<clipPath id="{cid}"><path d="{path}"/></clipPath>'
    out += f'<path d="{path}" fill="{fill}"/>' if fill else ''
    out += f'<g clip-path="url(#{cid})">{inner}</g>'
    if outline: out += f'<path d="{path}" fill="none" {ST}/>'
    return out

def blur(shape, b):  # forme floue (ombrage doux)
    return shape.replace('/>', f' filter="url(#b{b})"/>', 1)

def seated_legs():
    """Jambes assises vues de face : tibias, chaussures pointe vers nous, cuisses en raccourci."""
    k = K; p = []
    for x0, x1, xe0, xe1 in ((210, 286, 216, 280), (314, 390, 320, 384)):
        shin = f"M{x0} 812 L{x1} 812 L{xe1} 934 L{xe0} 934 Z"
        p.append(zone(shin, blur(f'<rect x="{x1-26}" y="800" width="40" height="150" fill="{k["pantsS"]}" opacity=".85"/>', 8)
                      + blur(f'<rect x="{x0-8}" y="800" width="20" height="150" fill="{k["pantsL"]}" opacity=".6"/>', 6)
                      + blur(f'<rect x="{x0-10}" y="806" width="{x1-x0+20}" height="26" fill="#000" opacity=".6"/>', 8)
                      + f'<path d="M{x0+14} 904 C{x0+30} 912 {x1-30} 912 {x1-12} 904" stroke="{k["pantsS"]}" stroke-width="4" fill="none" stroke-linecap="round"/>',
                      fill=k['pants']))
    for sx in (206, 310):
        shoe = f"M{sx} 926 L{sx+84} 926 C{sx+96} 940 {sx+96} 962 {sx+80} 972 L{sx+4} 972 C{sx-12} 962 {sx-12} 940 {sx} 926 Z"
        p.append(zone(shoe, blur(f'<rect x="{sx-20}" y="958" width="130" height="20" fill="#000" opacity=".6"/>', 4)
                      + blur(f'<ellipse cx="{sx+34}" cy="940" rx="22" ry="7" fill="#fff" opacity=".45"/>', 3), fill=k['shoe']))
    for x0, x1 in ((196, 298), (302, 404)):
        th = f"M{x0} 736 L{x1} 736 L{x1-2} 806 C{x1-16} 828 {x0+18} 828 {x0+4} 806 Z"
        p.append(zone(th, blur(f'<rect x="{x1-30}" y="730" width="44" height="110" fill="{k["pantsS"]}" opacity=".8"/>', 8)
                      + blur(f'<ellipse cx="{(x0+x1)//2-8}" cy="806" rx="30" ry="12" fill="{k["pantsL"]}" opacity=".9"/>', 6),
                      fill=k['pants']))
    return p

def character(posture="debout"):
    torch, flame = logo_parts()
    k = K
    p = []
    if posture == "assis":
        p.extend(seated_legs())
    else:
        p.append(f'<ellipse cx="300" cy="976" rx="190" ry="20" fill="#000" opacity=".32" filter="url(#b10)"/>')
    # --- jambes ---
    for x0, x1, xs in (((206, 296, 262), (304, 394, 358)) if posture != "assis" else ()):
        leg = f"M{x0} 748 L{x1} 748 L{x1-4} 928 C{x1-24} 935 {x0+20} 935 {x0+4} 928 Z"
        p.append(zone(leg, blur(f'<rect x="{xs}" y="740" width="60" height="200" fill="{k["pantsS"]}" opacity=".85"/>', 10)
                 + blur(f'<rect x="{x0-10}" y="740" width="28" height="200" fill="{k["pantsL"]}" opacity=".7"/>', 8)
                 + blur(f'<rect x="{x0-10}" y="740" width="{x1-x0+20}" height="40" fill="#000" opacity=".55"/>', 10)
                 + f'<path d="M{(x0+x1)//2-6} 790 L{(x0+x1)//2-7} 900" stroke="{k["pantsL"]}" stroke-width="3" opacity=".8"/>'
                 + f'<path d="M{x0+8} 902 C{x0+30} 912 {x1-30} 910 {x1-8} 900 M{x0+12} 916 C{x0+34} 922 {x1-30} 920 {x1-10} 914" stroke="{k["pantsS"]}" stroke-width="4" fill="none" stroke-linecap="round"/>',
                 fill=k['pants']))
    # --- chaussures ---
    for sh, hx in (("M210 922 L292 922 C302 944 294 970 262 972 L190 972 C166 972 160 948 182 936 C192 929 200 925 210 922 Z", 206),
                   ("M308 922 L390 922 C400 925 408 929 418 936 C440 948 434 972 410 972 L338 972 C306 970 298 944 308 922 Z", 394)) if posture != "assis" else ():
        p.append(zone(sh, blur(f'<rect x="150" y="955" width="300" height="30" fill="#000" opacity=".6"/>', 4)
                 + blur(f'<ellipse cx="{hx}" cy="941" rx="24" ry="7" fill="#fff" opacity=".45"/>', 3)
                 + f'<path d="M150 961 L450 961" stroke="#0E0805" stroke-width="5"/>', fill=k['shoe']))
    # --- cou ---
    neck = "M268 398 L268 470 C282 484 318 484 332 470 L332 398 Z"
    p.append(zone(neck, blur(f'<ellipse cx="304" cy="424" rx="58" ry="34" fill="{k["skinD"]}"/>', 8), fill=k['skin']))
    # col de veste (arrière)
    p.append(f'<path d="M226 488 C238 462 268 450 300 450 C332 450 362 462 374 488 L346 472 C332 462 316 458 300 458 C284 458 268 462 254 472 Z" fill="{k["jackS"]}" {ST}/>')
    # --- veste ---
    torso = "M172 486 C198 468 250 460 300 460 C350 460 402 468 428 486 C448 518 452 562 448 612 C444 656 442 704 448 758 C402 770 352 774 300 774 C248 774 198 770 152 758 C158 704 156 656 152 612 C148 562 152 518 172 486 Z"
    p.append(zone(torso,
        blur(f'<path d="M352 460 C418 520 440 640 428 790 L480 790 L480 460 Z" fill="{k["jackS"]}"/>', 14)
        + blur(f'<ellipse cx="196" cy="570" rx="44" ry="150" fill="{k["jackL"]}" opacity=".55"/>', 16)
        + blur(f'<ellipse cx="300" cy="752" rx="170" ry="34" fill="{k["jackS"]}" opacity=".7"/>', 12)
        + f'<path d="M300 612 C299 660 298 700 296 736 C292 752 282 764 264 774" stroke="{L}" stroke-width="4" fill="none"/>'
        + f'<path d="M300 736 C308 752 320 764 338 774" stroke="{L}" stroke-width="4" fill="none"/>'
        + f'<circle cx="310" cy="636" r="6.5" fill="#2E1C10" stroke="{L}" stroke-width="2.5"/><circle cx="308" cy="634" r="2" fill="{k["jackL"]}"/>',
        fill=k['jack']))
    # poche poitrine + pochette
    p.append(f'<path d="M360 566 L372 546 L381 556 L390 542 L396 562 Z" fill="{k["shirt"]}" {ST}/>')
    p.append(f'<path d="M352 562 L400 558 L401 572 L353 576 Z" fill="{k["jackS"]}" {ST}/>')
    # --- chemise ---
    vee = "M256 462 L300 612 L344 462 Z"
    p.append(zone(vee, blur(f'<path d="M300 470 L300 620 L350 460 Z" fill="{k["shirtS"]}"/>', 8)
                  + blur(f'<path d="M256 462 L300 612" stroke="#000" stroke-width="10" opacity=".35"/>', 4)
                  + blur(f'<path d="M344 462 L300 612" stroke="#000" stroke-width="10" opacity=".45"/>', 4), fill=k['shirt']))
    # cravate, coupée par l'ouverture de la veste
    tie = "M286 506 L314 506 L328 612 L300 646 L272 612 Z"
    stripes = "".join(f'<path d="M250 {y} L350 {y+100}" stroke="#F3A276" stroke-width="5" opacity=".35"/>' for y in range(430, 660, 26))
    p.append(f'<clipPath id="veeC"><path d="{vee}"/></clipPath><g clip-path="url(#veeC)">'
             + zone(tie, blur(f'<rect x="302" y="500" width="40" height="160" fill="{k["tieS"]}"/>', 6)
                    + blur(f'<rect x="270" y="500" width="12" height="160" fill="{k["tieL"]}" opacity=".7"/>', 4) + stripes, fill=k['tie'])
             + '</g>')
    knot = "M288 480 L312 480 L317 500 L300 512 L283 500 Z"
    p.append(zone(knot, blur(f'<rect x="302" y="476" width="20" height="40" fill="{k["tieS"]}"/>', 4)
                  + f'<path d="M292 486 L298 504" stroke="{k["tieL"]}" stroke-width="3" opacity=".8"/>', fill=k['tie']))
    # col de chemise
    p.append(zone("M256 462 L276 514 L299 480 Z", blur(f'<rect x="250" y="500" width="60" height="20" fill="{k["shirtS"]}"/>', 5), fill="#FFFFFF"))
    p.append(zone("M344 462 L324 514 L301 480 Z", blur(f'<rect x="300" y="456" width="60" height="70" fill="{k["shirtS"]}"/>', 6), fill=k['shirt']))
    # revers crantés
    p.append(zone("M256 462 L300 612 L238 548 L230 528 L246 520 L226 490 L240 466 Z",
                  blur(f'<rect x="220" y="460" width="30" height="160" fill="{k["jackL"]}" opacity=".6"/>', 8), fill="#6E4628"))
    p.append(zone("M344 462 L300 612 L362 548 L370 528 L354 520 L374 490 L360 466 Z",
                  blur(f'<rect x="340" y="460" width="40" height="160" fill="{k["jackS"]}" opacity=".8"/>', 8), fill="#5E3A20"))
    p.append(f'<path d="M238 476 L250 518 M248 534 L290 596" stroke="{k["jackL"]}" stroke-width="2.5" stroke-dasharray="6 6" fill="none"/>')
    p.append(f'<path d="M362 476 L350 518 M352 534 L310 596" stroke="#8A6040" stroke-width="2.5" stroke-dasharray="6 6" fill="none"/>')
    p.append(f'<g transform="translate(346 500) scale(.058)"><g fill="{k["gold"]}" stroke="{L}" stroke-width="40" fill-rule="evenodd" paint-order="stroke"><path d="{torch}"/><path d="{flame}"/></g></g>')
    # --- bras croisé (gauche du personnage, côté droit de l'image) ---
    upR = "M402 476 C434 486 452 514 456 562 C460 612 458 660 450 692 C444 716 420 728 398 716 L384 560 C384 520 390 490 402 476 Z"
    p.append(zone(upR, blur(f'<path d="M430 470 C470 560 470 660 440 740 L490 740 L490 470 Z" fill="{k["jackS"]}"/>', 12)
                  + blur(f'<ellipse cx="404" cy="590" rx="16" ry="110" fill="{k["jackL"]}" opacity=".5"/>', 10), fill=k['jack']))
    foR = "M454 690 C456 714 440 732 414 734 C360 738 300 738 262 730 L256 676 C300 672 360 668 410 666 C434 664 452 672 454 690 Z"
    p.append(zone(foR, blur(f'<rect x="250" y="712" width="220" height="40" fill="{k["jackS"]}"/>', 10)
                  + blur(f'<rect x="250" y="664" width="220" height="12" fill="{k["jackL"]}" opacity=".6"/>', 6)
                  + f'<path d="M424 672 C434 682 438 694 436 706 M404 668 C412 680 414 692 410 704 M300 674 C304 690 304 708 300 724" stroke="{L}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".6"/>',
                  fill=k['jack']))
    p.append(zone("M256 676 L262 730 L248 732 L242 678 Z", blur(f'<rect x="250" y="670" width="14" height="70" fill="{k["shirtS"]}"/>', 3), fill=k['shirt']))
    # --- bras levé (droite du personnage, côté gauche de l'image) ---
    upL = "M198 476 C166 486 150 514 146 562 C142 612 152 662 176 700 C190 720 222 724 244 708 L252 560 C248 520 232 488 198 476 Z"
    p.append(zone(upL, blur(f'<ellipse cx="170" cy="580" rx="22" ry="120" fill="{k["jackL"]}" opacity=".6"/>', 12)
                  + blur(f'<rect x="226" y="470" width="40" height="260" fill="{k["jackS"]}"/>', 12), fill=k['jack']))
    foL = "M194 692 C188 664 202 642 222 632 C240 592 254 534 262 474 L318 480 C314 542 298 612 270 670 C256 700 232 722 210 714 C200 710 196 702 194 692 Z"
    p.append(zone(foL, blur(f'<path d="M300 470 C296 560 280 640 240 730 L340 730 L340 470 Z" fill="{k["jackS"]}"/>', 12)
                  + blur(f'<path d="M262 470 C254 540 236 610 206 660" stroke="{k["jackL"]}" stroke-width="14" fill="none" opacity=".55"/>', 6)
                  + f'<path d="M210 650 C220 662 232 668 244 668 M204 672 C212 680 222 684 232 684 M236 612 C246 606 252 598 254 590" stroke="{L}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".65"/>',
                  fill=k['jack']))
    # --- main qui tient le coude (doigts posés sur le coude) ---
    p.append(zone("M256 678 C240 672 220 678 212 692 C204 708 210 726 226 734 C242 740 256 734 262 722 Z",
                  blur(f'<rect x="200" y="716" width="70" height="30" fill="{k["skinD"]}"/>', 6), fill=k['skin']))
    for y in (684, 700, 716):
        f_ = f"M250 {y} C236 {y-4} 214 {y-4} 202 {y+2} C194 {y+7} 198 {y+15} 208 {y+15} C224 {y+15} 238 {y+14} 250 {y+12} Z"
        p.append(zone(f_, blur(f'<rect x="190" y="{y+8}" width="70" height="10" fill="{k["skinS"]}"/>', 3)
                      + blur(f'<rect x="196" y="{y-4}" width="40" height="5" fill="{k["skinL"]}" opacity=".8"/>', 2), fill=k['skin']))
    return "\n".join(p), torch, flame

def head():
    k = K; p = []
    # oreilles
    p.append(zone("M158 264 C138 264 128 286 132 306 C136 328 150 340 166 336 Z",
                  blur(f'<ellipse cx="150" cy="300" rx="10" ry="22" fill="{k["skinS"]}"/>', 4), fill=k['skin']))
    p.append(f'<path d="M150 282 C142 292 142 308 152 318" stroke="{k["skinD"]}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    p.append(zone("M442 264 C462 264 472 286 468 306 C464 328 450 340 434 336 Z",
                  blur(f'<ellipse cx="452" cy="300" rx="14" ry="26" fill="{k["skinD"]}"/>', 4), fill=k['skinS']))
    p.append(f'<path d="M450 282 C458 292 458 308 448 318" stroke="#6E4026" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # visage
    face = "M158 230 C158 150 220 112 300 112 C380 112 442 150 442 230 L442 290 C442 350 420 395 380 418 C355 432 330 438 300 438 C270 438 245 432 220 418 C180 395 158 350 158 290 Z"
    p.append(zone(face,
        blur(f'<path d="M398 140 C452 220 452 360 356 446 L480 460 L480 120 Z" fill="{k["skinS"]}" opacity=".85"/>', 16)
        + blur(f'<ellipse cx="226" cy="236" rx="70" ry="96" fill="{k["skinL"]}" opacity=".6"/>', 22)
        + blur(f'<path d="M150 158 C230 196 330 206 450 176 L450 214 C330 240 230 236 150 204 Z" fill="{k["skinD"]}" opacity=".55"/>', 9)
        + blur(f'<ellipse cx="336" cy="430" rx="100" ry="26" fill="{k["skinS"]}" opacity=".7"/>', 12)
        + blur(f'<ellipse cx="222" cy="364" rx="26" ry="14" fill="{k["blush"]}" opacity=".38"/>', 6)
        + blur(f'<ellipse cx="384" cy="360" rx="24" ry="13" fill="{k["blush"]}" opacity=".3"/>', 6)
        + blur(f'<path d="M196 338 C226 348 266 346 296 338" stroke="{k["skinD"]}" stroke-width="10" fill="none" opacity=".3"/>', 5)
        + blur(f'<path d="M306 336 C336 346 376 346 404 336" stroke="{k["skinD"]}" stroke-width="10" fill="none" opacity=".35"/>', 5),
        fill=k['skin']))
    return "\n".join(p)

def hair():
    k = K; p = []
    base = "M152 300 C140 250 138 180 165 138 C190 98 235 72 280 62 C320 54 365 58 400 76 C440 98 462 140 462 196 C462 238 456 272 448 300 C442 276 436 254 428 238 C424 214 414 196 400 184 C378 192 352 196 322 194 C292 192 262 184 236 172 C214 186 198 206 190 232 C182 256 172 280 160 302 Z"
    p.append(zone(base,
        blur(f'<path d="M150 160 C240 150 340 150 470 170 L470 320 L140 320 Z" fill="{k["hairS"]}" opacity=".7"/>', 14)
        + blur(f'<ellipse cx="196" cy="150" rx="56" ry="26" transform="rotate(-38 196 150)" fill="{k["hairL"]}" opacity=".9"/>', 10)
        + f'<path d="M176 196 C182 170 196 148 216 132 M188 226 C196 202 208 184 224 170" stroke="{k["hairX"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>'
        + f'<path d="M420 120 C440 150 448 190 446 236 M398 110 C420 140 430 176 430 214" stroke="{k["hairS"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".8"/>',
        fill=k['hair']))
    quiff = "M214 150 C220 100 256 64 306 48 C336 38 368 36 392 44 C376 50 366 60 362 72 C384 66 410 70 430 84 C412 88 400 98 396 112 C418 112 440 124 452 142 C420 130 380 128 344 136 C300 144 254 152 214 150 Z"
    p.append(zone(quiff,
        blur(f'<path d="M210 156 C260 146 320 134 460 140 L460 170 L210 170 Z" fill="{k["hairS"]}"/>', 10)
        + blur(f'<path d="M226 120 C250 82 290 58 340 50" stroke="{k["hairL"]}" stroke-width="22" fill="none"/>', 8)
        + f'<path d="M236 112 C258 82 292 62 330 54" stroke="{k["hairX"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + f'<path d="M370 66 C388 62 404 64 418 72 M380 110 C396 108 414 112 430 120" stroke="{k["hairX"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".85"/>'
        + f'<path d="M250 140 C290 112 330 96 380 92 M280 146 C320 126 360 118 410 120" stroke="{k["hairS"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".75"/>',
        fill=k['hair']))
    p.append(f'<path d="M214 150 C218 128 228 108 244 92" stroke="{L}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return "\n".join(p)

def iris(cx, cy, cam):
    ix, iy = (cx + 1, cy + 3) if cam else (cx + 9, cy - 12)   # caméra : regard droit vers le spectateur
    return (f'<circle cx="{ix}" cy="{iy}" r="19" fill="url(#irisG)"/>'
            + f'<circle cx="{ix}" cy="{iy}" r="19" fill="none" stroke="#2A170B" stroke-width="2"/>'
            + f'<circle cx="{ix+1}" cy="{iy-1}" r="10" fill="#140B05"/>'
            + f'<circle cx="{ix+7}" cy="{iy-8}" r="6" fill="#fff"/><circle cx="{ix-6}" cy="{iy+9}" r="3" fill="#fff" opacity=".9"/>')

def eyes_glasses(regard="haut"):
    k = K; p = []
    cam = regard == "camera"
    # sourcils (l'un relevé ; les deux au même niveau quand il regarde la caméra)
    p.append(f'<path d="M200 248 C218 228 252 222 280 232 C284 238 280 244 272 242 C250 236 228 240 210 252 C202 256 196 252 200 248 Z" fill="{k["hair"]}" stroke="{L}" stroke-width="3"/>')
    if cam:
        p.append(f'<path d="M400 248 C382 228 348 222 320 232 C316 238 320 244 328 242 C350 236 372 240 390 252 C398 256 404 252 400 248 Z" fill="{k["hair"]}" stroke="{L}" stroke-width="3"/>')
    else:
        p.append(f'<path d="M322 222 C350 198 386 198 404 212 C408 218 404 224 396 222 C378 214 352 216 330 232 C322 236 316 230 322 222 Z" fill="{k["hair"]}" stroke="{L}" stroke-width="3"/>')
    # ombre des montures sur les joues
    p.append(blur(f'<path d="M200 346 C230 356 270 354 296 344 M306 344 C336 354 376 354 404 344" stroke="#5A3420" stroke-width="8" fill="none" opacity=".35"/>', 5))
    for cx, cy, cid in ((248, 292, "eL"), (352, 290, "eR")):
        e = f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="36"/>'
        p.append(f'<clipPath id="{cid}">{e}</clipPath>')
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="36" fill="#FFFFFF"/>')
        p.append(f'<g clip-path="url(#{cid})">'
                 + blur(f'<ellipse cx="{cx}" cy="{cy-32}" rx="40" ry="18" fill="#D9C8B4"/>', 4)
                 + iris(cx, cy, cam) + '</g>')
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="30" ry="36" fill="none" stroke="{L}" stroke-width="3.5"/>')
        p.append(f'<path d="M{cx-31} {cy-2} C{cx-25} {cy-36} {cx+23} {cy-40} {cx+31} {cy-8}" stroke="{L}" stroke-width="8" fill="none" stroke-linecap="round"/>')
        p.append(f'<path d="M{cx+28} {cy-12} L{cx+36} {cy-18}" stroke="{L}" stroke-width="5" stroke-linecap="round"/>')
        p.append(f'<path d="M{cx-20} {cy+33} C{cx-8} {cy+40} {cx+10} {cy+40} {cx+22} {cy+32}" stroke="{k["skinS"]}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    # lunettes (rectangles arrondis)
    for x, cid in ((194, "gL"), (306, "gR")):
        r = f'<rect x="{x}" y="246" width="100" height="90" rx="30"/>'
        p.append(f'<clipPath id="{cid}">{r}</clipPath>')
        p.append(f'<rect x="{x}" y="246" width="100" height="90" rx="30" fill="#CFE6F2" fill-opacity=".13"/>')
        p.append(f'<g clip-path="url(#{cid})" fill="#fff" opacity=".38"><path d="M{x-10} 300 L{x+44} 236 L{x+62} 236 L{x-4} 314 Z"/><path d="M{x+14} 330 L{x+78} 254 L{x+86} 258 L{x+22} 336 Z"/></g>')
        p.append(f'<rect x="{x}" y="246" width="100" height="90" rx="30" fill="none" stroke="{K["frame"]}" stroke-width="8"/>')
        p.append(f'<path d="M{x+8} 286 C{x+8} 262 {x+20} 252 {x+40} 251" stroke="#6E4A34" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M294 284 Q300 274 306 284" stroke="{K["frame"]}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M194 280 L158 274 M406 278 L442 272" stroke="{K["frame"]}" stroke-width="7" stroke-linecap="round"/>')
    # nez
    p.append(blur(f'<ellipse cx="306" cy="358" rx="18" ry="7" fill="{k["skinD"]}" opacity=".55"/>', 3))
    p.append(f'<path d="M306 312 C318 330 322 346 310 354 C304 358 296 357 291 352" stroke="{k["skinD"]}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    p.append(blur(f'<ellipse cx="296" cy="340" rx="7" ry="5" fill="{k["skinL"]}" opacity=".9"/>', 2))
    # bouche (pincée : il réfléchit)
    if cam:   # léger sourire, assuré
        p.append(f'<path d="M278 380 C292 390 312 390 326 379" stroke="{L}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        p.append(f'<path d="M274 382 L279 379 M330 377 L325 381" stroke="{L}" stroke-width="4" stroke-linecap="round"/>')
    else:
        p.append(f'<path d="M278 390 C292 382 312 382 326 391" stroke="{L}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        p.append(f'<path d="M326 391 L331 386" stroke="{L}" stroke-width="4" stroke-linecap="round"/>')
    p.append(f'<path d="M292 402 C302 406 312 404 318 400" stroke="{k["skinS"]}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return "\n".join(p)

def chin_hand():
    k = K; p = []
    p.append(zone("M262 474 L318 480 L320 466 L264 460 Z", blur(f'<rect x="290" y="456" width="40" height="30" fill="{k["shirtS"]}"/>', 4), fill=k['shirt']))
    p.append(blur(f'<ellipse cx="306" cy="440" rx="50" ry="16" fill="{k["skinD"]}" opacity=".5"/>', 8))  # ombre portée sur le menton
    fist = "M258 462 C250 436 258 410 280 400 C300 392 332 394 346 408 C360 422 360 446 350 460 C340 474 316 480 294 478 C278 476 264 472 258 462 Z"
    p.append(zone(fist,
        blur(f'<path d="M262 456 C290 474 330 470 360 440 L370 490 L250 490 Z" fill="{k["skinD"]}" opacity=".8"/>', 8)
        + blur(f'<ellipse cx="282" cy="414" rx="22" ry="12" fill="{k["skinL"]}"/>', 6)
        + f'<path d="M264 422 C284 414 314 414 342 420 M262 442 C284 434 316 434 348 440" stroke="{L}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
        + f'<path d="M290 416 L292 424 M318 416 L318 424 M292 436 L294 444 M320 436 L320 444" stroke="{k["skinS"]}" stroke-width="3" stroke-linecap="round"/>',
        fill=k['skin']))
    finger = "M330 410 C334 392 346 382 358 386 C368 392 364 408 352 418 Z"
    p.append(zone(finger, blur(f'<rect x="346" y="380" width="30" height="40" fill="{k["skinS"]}"/>', 5)
                  + blur(f'<ellipse cx="346" cy="392" rx="6" ry="4" fill="{k["skinL"]}"/>', 2), fill=k['skin']))
    return "\n".join(p)

DEFS = f'''<defs>
 <filter id="b2" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="2"/></filter>
 <filter id="b3" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="3"/></filter>
 <filter id="b4" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="4"/></filter>
 <filter id="b5" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="5"/></filter>
 <filter id="b6" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="6"/></filter>
 <filter id="b8" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="8"/></filter>
 <filter id="b9" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="b10" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="10"/></filter>
 <filter id="b12" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="12"/></filter>
 <filter id="b14" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="14"/></filter>
 <filter id="b16" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="16"/></filter>
 <filter id="b22" filterUnits="userSpaceOnUse" x="-200" y="-200" width="1000" height="1400"><feGaussianBlur stdDeviation="22"/></filter>
 <radialGradient id="irisG" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#A9743F"/><stop offset=".7" stop-color="#5E3A1E"/><stop offset="1" stop-color="#3A2110"/></radialGradient>
</defs>'''

def build(regard="haut", posture="debout"):
    _n[0] = 0
    body, torch, flame = character(posture)
    return DEFS + "\n" + body + "\n" + head() + "\n" + hair() + "\n" + eyes_glasses(regard) + "\n" + chin_hand()

if __name__ == "__main__":
    out = os.path.join(ROOT, "personnage/presentateur.svg")
    open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 1000" width="600" height="1000">\n{build()}\n</svg>')
    print("écrit", out)
