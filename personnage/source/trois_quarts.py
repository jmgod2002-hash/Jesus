"""Présentateur Feu d'Élévation de trois quarts (tourné vers la droite), assis jambes croisées,
mains jointes sur le genou, regard caméra. Repère 700 x 1000. Même style que personnage.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P
from personnage import K, L, ST, zone, blur

def legs():
    k = K; p = []
    # jambe du dessous (pied au sol)
    p.append(zone("M396 812 L466 812 L470 952 L404 952 Z",
                  blur(f'<rect x="440" y="800" width="40" height="160" fill="{k["pantsS"]}" opacity=".9"/>', 8)
                  + blur(f'<rect x="390" y="806" width="90" height="40" fill="#000" opacity=".55"/>', 10), fill=k['pants']))
    p.append(zone("M398 944 L470 944 C502 946 532 956 542 970 C546 980 536 986 520 986 L402 986 C388 982 386 956 398 944 Z",
                  blur(f'<rect x="380" y="972" width="180" height="20" fill="#000" opacity=".6"/>', 4)
                  + blur(f'<ellipse cx="500" cy="958" rx="26" ry="6" fill="#fff" opacity=".4"/>', 3), fill=k['shoe']))
    # jambe du dessus : cuisse vers la droite, tibia qui pend, pied levé
    p.append(zone("M448 790 C474 778 506 790 514 814 L562 914 C568 934 550 950 530 948 L500 944 C490 928 470 870 444 830 Z",
                  blur(f'<path d="M500 800 L570 930 L600 930 L540 800 Z" fill="{k["pantsS"]}"/>', 8)
                  + blur(f'<path d="M452 800 C470 850 488 900 500 940" stroke="{k["pantsL"]}" stroke-width="12" fill="none" opacity=".6"/>', 5), fill=k['pants']))
    p.append(zone("M516 912 C548 904 592 914 614 932 C626 942 620 958 600 960 L530 962 C512 960 504 930 516 912 Z",
                  blur(f'<rect x="500" y="948" width="140" height="20" fill="#000" opacity=".6"/>', 4)
                  + blur(f'<ellipse cx="584" cy="928" rx="20" ry="6" fill="#fff" opacity=".45"/>', 3), fill=k['shoe']))
    p.append(zone("M228 734 C300 726 400 734 462 744 C496 750 510 776 504 802 C498 830 472 842 440 840 C380 836 300 826 238 816 C200 808 192 760 228 734 Z",
                  blur(f'<rect x="200" y="808" width="320" height="40" fill="{k["pantsS"]}" opacity=".9"/>', 10)
                  + blur(f'<ellipse cx="470" cy="770" rx="34" ry="16" fill="{k["pantsL"]}" opacity=".9"/>', 6)
                  + f'<path d="M300 760 C350 762 410 768 460 778" stroke="{k["pantsL"]}" stroke-width="3" fill="none" opacity=".7"/>',
                  fill=k['pants']))
    return p

def torso():
    k = K; p = []
    p.append(zone("M290 396 L290 470 C306 484 352 484 368 470 L368 396 Z",
                  blur(f'<ellipse cx="340" cy="422" rx="60" ry="34" fill="{k["skinD"]}"/>', 8), fill=k['skin']))
    p.append(f'<path d="M262 488 C276 462 306 450 340 450 C372 450 404 462 418 486 L392 470 C376 462 358 458 340 458 C322 458 304 462 290 472 Z" fill="{k["jackS"]}" {ST}/>')
    t = "M210 486 C240 466 300 458 350 458 C400 458 450 466 474 488 C492 520 494 570 488 620 C484 660 482 700 488 752 C420 774 320 776 232 770 C206 760 198 740 198 716 C194 660 188 600 188 560 C188 520 194 500 210 486 Z"
    p.append(zone(t, blur(f'<path d="M430 460 C480 540 496 640 490 790 L540 790 L540 460 Z" fill="{k["jackS"]}"/>', 14)
                  + blur(f'<ellipse cx="226" cy="590" rx="40" ry="150" fill="{k["jackL"]}" opacity=".55"/>', 16)
                  + f'<path d="M392 612 C392 660 394 700 398 760" stroke="{L}" stroke-width="4" fill="none"/>'
                  + f'<circle cx="404" cy="640" r="6.5" fill="#2E1C10" stroke="{L}" stroke-width="2.5"/>', fill=k['jack']))
    vee = "M330 462 L392 610 L418 462 Z"
    p.append(zone(vee, blur(f'<path d="M392 470 L392 620 L430 460 Z" fill="{k["shirtS"]}"/>', 6), fill=k['shirt']))
    tie = "M382 506 L404 506 L414 606 L396 636 L376 604 Z"
    stripes = "".join(f'<path d="M340 {y} L440 {y+100}" stroke="#F3A276" stroke-width="5" opacity=".35"/>' for y in range(430, 660, 24))
    p.append(f'<clipPath id="tq_vee"><path d="{vee}"/></clipPath><g clip-path="url(#tq_vee)">'
             + zone(tie, blur(f'<rect x="398" y="500" width="30" height="150" fill="{k["tieS"]}"/>', 5) + stripes, fill=k['tie']) + '</g>')
    p.append(zone("M384 480 L404 480 L408 498 L394 510 L380 498 Z", blur(f'<rect x="396" y="476" width="16" height="36" fill="{k["tieS"]}"/>', 3), fill=k['tie']))
    p.append(zone("M330 462 L352 512 L382 480 Z", blur(f'<rect x="330" y="500" width="60" height="20" fill="{k["shirtS"]}"/>', 5), fill="#FFFFFF"))
    p.append(zone("M418 462 L408 506 L392 480 Z", blur(f'<rect x="390" y="456" width="40" height="60" fill="{k["shirtS"]}"/>', 5), fill=k['shirt']))
    p.append(zone("M330 462 L392 610 L318 546 L310 526 L326 518 L304 488 L316 466 Z",
                  blur(f'<rect x="300" y="460" width="30" height="160" fill="{k["jackL"]}" opacity=".6"/>', 8), fill="#6E4628"))
    p.append(zone("M418 462 L392 610 L428 546 L432 526 L424 518 L436 490 L428 466 Z",
                  blur(f'<rect x="410" y="460" width="30" height="160" fill="{k["jackS"]}" opacity=".8"/>', 6), fill="#5E3A20"))
    p.append(f'<path d="M316 478 L326 518 M326 534 L384 600" stroke="{k["jackL"]}" stroke-width="2.5" stroke-dasharray="6 6" fill="none"/>')
    torch, flame = P.logo_parts()
    p.append(f'<g transform="translate(318 492) scale(.054)"><g fill="{k["gold"]}" stroke="{L}" stroke-width="40" fill-rule="evenodd" paint-order="stroke"><path d="{torch}"/><path d="{flame}"/></g></g>')
    return p

def arms():
    k = K; p = []
    # bras du fond (droite) : coude puis avant-bras vers le genou
    p.append(zone("M470 490 C495 510 505 560 503 620 C502 660 496 690 480 708 C466 720 446 716 440 702 L452 560 C452 520 458 500 470 490 Z",
                  blur(f'<rect x="480" y="480" width="40" height="240" fill="{k["jackS"]}"/>', 10), fill=k['jack']))
    p.append(zone("M444 700 C454 688 482 690 494 704 L502 760 C488 776 462 776 450 762 Z",
                  blur(f'<rect x="480" y="690" width="30" height="90" fill="{k["jackS"]}"/>', 8), fill=k['jack']))
    # bras de devant (gauche) : épaule, coude, avant-bras vers les mains
    p.append(zone("M192 496 C170 520 165 580 172 640 C176 670 190 700 214 712 C240 722 262 708 266 690 L262 560 C258 520 236 496 210 488 Z",
                  blur(f'<ellipse cx="184" cy="600" rx="18" ry="110" fill="{k["jackL"]}" opacity=".6"/>', 10)
                  + blur(f'<rect x="240" y="480" width="40" height="240" fill="{k["jackS"]}"/>', 12), fill=k['jack']))
    fo = "M214 712 C200 690 210 662 236 656 C300 662 372 690 432 722 L442 790 C380 790 300 754 236 730 C226 726 218 720 214 712 Z"
    p.append(zone(fo, blur(f'<path d="M220 730 C300 760 380 790 450 800 L450 830 L210 830 Z" fill="{k["jackS"]}"/>', 10)
                  + blur(f'<path d="M240 664 C300 670 370 696 430 726" stroke="{k["jackL"]}" stroke-width="12" fill="none" opacity=".55"/>', 6)
                  + f'<path d="M230 676 C240 690 244 704 240 718 M252 668 C262 684 264 700 258 716" stroke="{L}" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".6"/>',
                  fill=k['jack']))
    # manchettes de chemise
    p.append(zone("M426 718 L444 716 L452 792 L436 794 Z", blur(f'<rect x="440" y="710" width="16" height="90" fill="{k["shirtS"]}"/>', 3), fill=k['shirt']))
    # mains jointes sur le genou
    hands = "M436 734 C452 720 492 722 510 738 C526 752 522 786 502 796 C480 806 452 802 438 790 C424 776 424 748 436 734 Z"
    p.append(zone(hands, blur(f'<path d="M430 780 C460 806 500 806 530 776 L540 820 L420 820 Z" fill="{k["skinD"]}" opacity=".8"/>', 6)
                  + blur(f'<ellipse cx="462" cy="742" rx="20" ry="9" fill="{k["skinL"]}"/>', 5)
                  + f'<path d="M454 744 L452 780 M470 742 L470 786 M486 744 L488 786 M500 750 L504 780" stroke="{L}" stroke-width="3" stroke-linecap="round" opacity=".75"/>',
                  fill=k['skin']))
    p.append(zone("M440 740 C446 726 462 722 470 728 C476 736 468 746 456 750 Z",
                  blur(f'<rect x="440" y="740" width="40" height="14" fill="{k["skinS"]}"/>', 3), fill=k['skin']))
    return p

def head():
    k = K; p = []
    p.append(zone("M196 262 C176 262 166 284 170 304 C174 328 188 342 204 336 Z",
                  blur(f'<ellipse cx="186" cy="300" rx="10" ry="22" fill="{k["skinS"]}"/>', 4), fill=k['skin']))
    p.append(f'<path d="M188 282 C180 292 180 308 190 318" stroke="{k["skinD"]}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    face = "M196 230 C196 150 256 112 336 112 C404 112 452 146 464 210 C470 244 468 274 472 300 C474 332 464 362 446 388 C420 422 380 442 346 444 C300 446 252 426 224 396 C200 368 196 330 196 290 Z"
    p.append(zone(face,
        blur(f'<path d="M420 130 C478 220 476 380 380 452 L500 460 L500 120 Z" fill="{k["skinS"]}" opacity=".85"/>', 14)
        + blur(f'<ellipse cx="262" cy="240" rx="70" ry="96" fill="{k["skinL"]}" opacity=".6"/>', 22)
        + blur(f'<path d="M188 158 C260 196 360 206 480 176 L480 214 C360 240 260 236 188 204 Z" fill="{k["skinD"]}" opacity=".55"/>', 9)
        + blur(f'<ellipse cx="370" cy="434" rx="100" ry="26" fill="{k["skinS"]}" opacity=".7"/>', 12)
        + blur(f'<ellipse cx="252" cy="366" rx="26" ry="14" fill="{k["blush"]}" opacity=".38"/>', 6)
        + blur(f'<ellipse cx="428" cy="358" rx="16" ry="11" fill="{k["blush"]}" opacity=".3"/>', 6),
        fill=k['skin']))
    # cheveux
    base = "M184 326 C164 262 164 182 194 136 C224 92 274 70 330 64 C386 58 436 80 460 120 C478 150 482 192 474 228 C466 208 456 192 442 182 C414 194 374 198 334 194 C304 192 274 184 252 174 C236 192 224 216 218 242 C210 272 200 302 190 328 Z"
    p.append(zone(base,
        blur(f'<path d="M180 160 C270 150 370 150 490 170 L490 340 L160 340 Z" fill="{k["hairS"]}" opacity=".7"/>', 14)
        + blur(f'<ellipse cx="226" cy="150" rx="56" ry="26" transform="rotate(-38 226 150)" fill="{k["hairL"]}" opacity=".9"/>', 10)
        + f'<path d="M200 200 C206 172 220 150 240 134 M206 236 C214 212 226 194 242 180" stroke="{k["hairX"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>',
        fill=k['hair']))
    quiff = "M244 150 C250 100 286 64 336 48 C366 38 398 36 422 44 C406 50 396 60 392 72 C414 66 440 70 460 84 C442 88 430 98 426 112 C448 112 468 124 480 142 C450 130 410 128 374 136 C330 144 284 152 244 150 Z"
    p.append(zone(quiff,
        blur(f'<path d="M240 156 C290 146 350 134 490 140 L490 170 L240 170 Z" fill="{k["hairS"]}"/>', 10)
        + blur(f'<path d="M256 120 C280 82 320 58 370 50" stroke="{k["hairL"]}" stroke-width="22" fill="none"/>', 8)
        + f'<path d="M266 112 C288 82 322 62 360 54" stroke="{k["hairX"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + f'<path d="M400 66 C418 62 434 64 448 72 M410 110 C426 108 444 112 460 120" stroke="{k["hairX"]}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".85"/>',
        fill=k['hair']))
    # sourcils
    p.append(f'<path d="M232 248 C250 228 284 222 310 232 C314 238 310 244 302 242 C282 236 260 240 242 252 C234 256 228 252 232 248 Z" fill="{k["hair"]}" stroke="{L}" stroke-width="3"/>')
    p.append(f'<path d="M368 234 C384 222 412 222 428 232 C432 238 428 242 422 240 C408 234 390 236 376 244 C368 248 364 240 368 234 Z" fill="{k["hair"]}" stroke="{L}" stroke-width="3"/>')
    # yeux : celui du fond est plus étroit ; les deux regardent la caméra
    for cx, cy, rx, cid, irx in ((282, 292, 28, "tq_eL", 18), (398, 290, 21, "tq_eR", 13)):
        p.append(f'<clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="34"/></clipPath>')
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="34" fill="#FFFFFF"/>')
        ix = cx - 3
        p.append(f'<g clip-path="url(#{cid})">' + blur(f'<ellipse cx="{cx}" cy="{cy-30}" rx="{rx+10}" ry="16" fill="#D9C8B4"/>', 4)
                 + f'<ellipse cx="{ix}" cy="{cy+3}" rx="{irx}" ry="19" fill="url(#irisG)" stroke="#2A170B" stroke-width="2"/>'
                 + f'<ellipse cx="{ix}" cy="{cy+3}" rx="{irx*.52:.1f}" ry="10" fill="#140B05"/>'
                 + f'<circle cx="{ix+5}" cy="{cy-5}" r="5.5" fill="#fff"/><circle cx="{ix-5}" cy="{cy+11}" r="2.5" fill="#fff" opacity=".9"/></g>')
        p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="34" fill="none" stroke="{L}" stroke-width="3.5"/>')
        p.append(f'<path d="M{cx-rx-1} {cy-2} C{cx-rx+5} {cy-34} {cx+rx-7} {cy-38} {cx+rx+1} {cy-8}" stroke="{L}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    # lunettes : verre proche plein, verre du fond comprimé, branche vers l'oreille
    for x, w, cid in ((228, 104, "tq_gL"), (356, 80, "tq_gR")):
        p.append(f'<clipPath id="{cid}"><rect x="{x}" y="248" width="{w}" height="88" rx="28"/></clipPath>')
        p.append(f'<rect x="{x}" y="248" width="{w}" height="88" rx="28" fill="#CFE6F2" fill-opacity=".13"/>')
        p.append(f'<g clip-path="url(#{cid})" fill="#fff" opacity=".38"><path d="M{x-10} 300 L{x+44} 238 L{x+60} 238 L{x-4} 314 Z"/><path d="M{x+14} 330 L{x+76} 256 L{x+84} 260 L{x+22} 336 Z"/></g>')
        p.append(f'<rect x="{x}" y="248" width="{w}" height="88" rx="28" fill="none" stroke="{K["frame"]}" stroke-width="8"/>')
    p.append(f'<path d="M332 284 Q344 274 356 284" stroke="{K["frame"]}" stroke-width="8" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M228 282 L196 280 M436 278 L452 276" stroke="{K["frame"]}" stroke-width="7" stroke-linecap="round"/>')
    # nez tourné vers la droite
    p.append(blur(f'<ellipse cx="372" cy="362" rx="20" ry="7" fill="{k["skinD"]}" opacity=".55"/>', 3))
    p.append(f'<path d="M350 306 C362 326 380 342 380 354 C380 364 366 366 354 360" stroke="{k["skinD"]}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    p.append(blur(f'<ellipse cx="362" cy="344" rx="8" ry="5" fill="{k["skinL"]}" opacity=".9"/>', 2))
    # sourire
    p.append(f'<path d="M314 386 C330 400 356 400 376 384" stroke="{L}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M310 388 L316 384 M380 382 L374 387" stroke="{L}" stroke-width="4" stroke-linecap="round"/>')
    return p

def fauteuil():
    """Fauteuil crème de trois quarts, derrière le personnage."""
    c = ['<rect x="150" y="860" width="22" height="100" rx="6" fill="#B98552"/><rect x="586" y="850" width="20" height="96" rx="6" fill="#9A6A3E"/>']
    for shape in ('<path d="M120 560 C120 500 160 470 230 466 L520 470 C570 474 590 510 590 560 L590 780 L120 780 Z"/>',
                  '<path d="M150 760 L600 744 C622 744 630 760 628 782 L624 846 C622 860 610 868 596 868 L170 880 C152 880 142 868 142 852 Z"/>',
                  '<rect x="540" y="620" width="96" height="236" rx="46"/>',
                  '<rect x="96" y="636" width="150" height="262" rx="60"/>'):
        c.append(shape.replace('/>', ' fill="url(#tq_chair)"/>'))
        c.append(shape.replace('/>', ' fill="url(#tq_boucle)"/>'))
        c.append(shape.replace('/>', ' fill="none" stroke="#CDBBA5" stroke-width="2"/>'))
    c.append('<rect x="236" y="636" width="20" height="262" fill="#000" opacity=".12" filter="url(#b8)"/>')
    # plaid couleur braise sur l'accoudoir avant
    c.append('<path d="M84 654 C116 632 208 632 252 658 L258 726 C244 786 234 846 226 912 C192 922 142 920 98 912 C102 846 94 786 80 726 Z" fill="#B65A34"/>'
             '<path d="M124 690 C132 760 130 840 126 908 M174 686 C182 760 180 840 176 914 M222 690 C224 750 220 810 214 870" stroke="#8E3F20" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>'
             '<path d="M84 654 C116 632 208 632 252 658" stroke="#D9875C" stroke-width="5" fill="none" stroke-linecap="round"/>')
    return "".join(c)

DEFS_TQ = '''<defs>
 <linearGradient id="tq_chair" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F8F2EA"/><stop offset=".6" stop-color="#EDE3D6"/><stop offset="1" stop-color="#D9CAB7"/></linearGradient>
 <pattern id="tq_boucle" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2.5" cy="2.5" r="1.9" fill="#D6C5AF" opacity=".55"/><circle cx="7" cy="6.5" r="1.9" fill="#FFFFFF" opacity=".55"/></pattern>
</defs>'''

def build(avec_fauteuil=True):
    P._n[0] = 0
    parts = [P.DEFS, DEFS_TQ]
    if avec_fauteuil: parts.append(fauteuil())
    parts += legs() + torso() + arms() + head()
    return "\n".join(parts)

if __name__ == "__main__":
    out = os.path.join(P.ROOT, "personnage/presentateur_3q.svg")
    open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="40 0 700 1000" width="700" height="1000">\n{build()}\n</svg>')
    print("écrit", out)
