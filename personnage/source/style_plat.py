"""Présentateur Feu d'Élévation en illustration plate (sans contours, formes simples, membres allongés),
assis à une table ronde, micro de table, ordinateur, fenêtre en arche. 1000 x 1500 (2:3)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import personnage as P
ROOT = P.ROOT
torch, flame = P.logo_parts()

C = dict(fond="#3A2418", ciel="#46301F", nuage="#F5EDE0", cadre="#F5EDE0", oiseau="#E8A06A",
         peau="#C98B5E", peauO="#A86E45", cheveux="#2A170C", veste="#A0673A", vesteO="#7E4C28", bras="#B5793F", chemise="#FBF6EE",
         cravate="#C0522B", pantalon="#24150B", pantalonO="#170D06", chaussure="#0E0804", semelle="#E07A3A",
         chaise="#C0522B", chaiseO="#93391B", pied="#1A100A", bois="#C4874E", boisO="#8A5A36", boisC="#D9A06A",
         micro="#E6D5BB", microO="#B8A07A", ordi="#1E120A", ecran="#F5EDE0", casque="#E07A3A", casqueO="#B65A34", lunettes="#0E0804")

def scene():
    c = C; o = []
    o.append(f'<rect width="1000" height="1500" fill="{c["fond"]}"/>')
    # fenêtre en arche, nuages et oiseaux
    arche = "M330 660 L330 380 C330 250 430 165 560 165 C690 165 790 250 790 380 L790 660 Z"
    o.append(f'<clipPath id="fen"><path d="{arche}"/></clipPath><path d="{arche}" fill="{c["ciel"]}"/>')
    o.append(f'<g clip-path="url(#fen)" fill="{c["nuage"]}">'
             '<circle cx="690" cy="330" r="70"/><circle cx="760" cy="380" r="60"/><circle cx="620" cy="420" r="62"/><circle cx="710" cy="440" r="70"/>'
             '<rect x="560" y="430" width="260" height="90"/><circle cx="470" cy="540" r="55"/><circle cx="540" cy="520" r="62"/><circle cx="400" cy="575" r="40"/>'
             '<rect x="340" y="560" width="470" height="110"/></g>')
    o.append(f'<path d="{arche}" fill="none" stroke="{c["cadre"]}" stroke-width="16"/>')
    o.append(f'<path d="M483 180 L483 660 M637 180 L637 660 M330 330 L790 330 M330 520 L790 520" stroke="{c["cadre"]}" stroke-width="12"/>')
    o.append(f'<path d="M560 270 l14 -12 l6 10 l6 -14 l14 8" stroke="{c["oiseau"]}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<path d="M380 430 l12 -10 l5 8 l5 -12 l12 7" stroke="{c["oiseau"]}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # chaise : dossier
    o.append(f'<path d="M770 700 C770 680 790 668 812 668 L858 668 C884 668 900 686 898 712 L886 1000 L780 1000 Z" fill="{c["chaise"]}"/>')
    o.append(f'<path d="M856 668 C884 668 900 686 898 712 L886 1000 L846 1000 L862 712 C863 690 860 676 856 668 Z" fill="{c["chaiseO"]}"/>')
    # jambe arrière (derrière le pied de table)
    o.append(f'<path d="M690 930 C620 940 540 960 470 980 C450 1000 452 1030 470 1040 C540 1030 620 1010 700 1000 Z" fill="{c["pantalonO"]}"/>')
    o.append(f'<path d="M470 980 C440 1000 430 1030 440 1050 L300 1160 L270 1130 Z" fill="{c["pantalonO"]}"/>')
    o.append(f'<path d="M262 1122 C250 1110 200 1112 168 1128 C150 1140 152 1166 176 1172 L296 1168 C306 1150 290 1128 262 1122 Z" fill="{c["chaussure"]}"/><path d="M160 1170 L298 1166" stroke="{c["semelle"]}" stroke-width="7" stroke-linecap="round"/>')
    # table : pied et socle
    o.append(f'<ellipse cx="370" cy="1286" rx="150" ry="30" fill="{c["boisO"]}"/><ellipse cx="370" cy="1278" rx="150" ry="28" fill="{c["bois"]}"/>')
    o.append(f'<rect x="334" y="860" width="72" height="420" fill="{c["bois"]}"/><rect x="376" y="860" width="30" height="420" fill="{c["boisO"]}"/>')
    # chaise : assise, accoudoir, pied à roulettes
    o.append(f'<rect x="600" y="940" width="290" height="70" rx="26" fill="{c["chaise"]}"/><rect x="600" y="980" width="290" height="30" rx="14" fill="{c["chaiseO"]}"/>')
    o.append(f'<rect x="736" y="1010" width="30" height="110" fill="{c["pied"]}"/>')
    for x2, y2 in ((620, 1170), (690, 1196), (820, 1196), (890, 1170)):
        o.append(f'<path d="M751 1120 L{x2} {y2}" stroke="{c["pied"]}" stroke-width="14" stroke-linecap="round"/><circle cx="{x2}" cy="{y2+14}" r="13" fill="{c["pied"]}"/>')
    o.append(f'<path d="M886 820 L740 820 L736 940" stroke="{c["pied"]}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # buste (penché vers la table), chemise et cravate
    o.append(f'<path d="M640 640 C660 620 720 612 770 626 C800 636 810 680 808 740 L800 950 L640 950 C630 860 618 760 620 700 C620 670 626 650 640 640 Z" fill="{c["veste"]}"/>')
    o.append(f'<path d="M760 626 C800 636 810 680 808 740 L800 950 L748 950 C760 850 770 700 760 626 Z" fill="{c["vesteO"]}"/>')
    o.append(f'<path d="M650 632 L700 626 L676 760 Z" fill="{c["chemise"]}"/><path d="M670 640 L686 640 L690 720 L676 744 L664 718 Z" fill="{c["cravate"]}"/>')
    o.append(f'<path d="M700 626 L676 760 L712 700 Z" fill="{c["vesteO"]}"/><path d="M650 632 L676 760 L640 690 Z" fill="{c["vesteO"]}" opacity=".7"/>')
    # jambe avant (devant le pied de table)
    o.append(f'<path d="M790 940 C700 950 600 980 520 1010 C494 1024 494 1062 520 1074 C600 1060 700 1040 800 1010 Z" fill="{c["pantalon"]}"/>')
    o.append(f'<path d="M520 1010 C496 1030 490 1060 500 1080 L506 1280 L560 1280 L566 1060 Z" fill="{c["pantalon"]}"/>')
    o.append(f'<path d="M500 1272 C470 1268 420 1278 396 1296 C382 1310 390 1330 414 1332 L566 1330 C578 1310 566 1280 540 1274 Z" fill="{c["chaussure"]}"/><path d="M394 1330 L568 1328" stroke="{c["semelle"]}" stroke-width="7" stroke-linecap="round"/>')
    # plateau de table
    o.append(f'<ellipse cx="370" cy="848" rx="272" ry="48" fill="{c["boisO"]}"/><ellipse cx="370" cy="832" rx="272" ry="46" fill="{c["bois"]}"/>')
    o.append(f'<path d="M150 826 C240 806 470 800 600 818" stroke="{c["boisC"]}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>')
    # ordinateur (écran : la torche et une onde sonore)
    o.append(f'<path d="M126 790 L300 760 L420 790 L246 822 Z" fill="{c["ordi"]}"/>')
    o.append(f'<path d="M120 786 L108 620 L292 594 L300 760 Z" fill="{c["ordi"]}"/><path d="M128 770 L118 634 L282 610 L290 748 Z" fill="{c["ecran"]}"/>')
    o.append(f'<g transform="translate(150 640) rotate(-8) scale(.12)" fill="#3B2412" fill-rule="evenodd"><path d="{torch}"/><path d="{flame}"/></g>')
    o.append(f'<path d="M206 690 l8 -14 l8 26 l8 -36 l8 40 l8 -24 l8 12 l8 -8 l8 6" stroke="{c["cravate"]}" stroke-width="4" fill="none" stroke-linejoin="round" transform="rotate(-8 240 690)"/>')
    # micro de table
    o.append(f'<ellipse cx="470" cy="822" rx="54" ry="13" fill="{c["microO"]}"/><path d="M470 818 L466 730" stroke="{c["microO"]}" stroke-width="10"/>')
    o.append(f'<g transform="translate(456 680) rotate(28)"><rect x="-30" y="-58" width="60" height="112" rx="30" fill="{c["micro"]}"/>'
             + "".join(f'<path d="M-26 {y} L26 {y}" stroke="{c["microO"]}" stroke-width="5" stroke-linecap="round"/>' for y in (-42, -28, -14, 0))
             + f'<rect x="-30" y="12" width="60" height="10" fill="{c["microO"]}"/></g>')
    o.append(f'<path d="M466 822 C420 850 330 850 300 796" stroke="{c["ordi"]}" stroke-width="4" fill="none"/>')
    # bras du fond : main posée au bord de la table
    o.append(f'<path d="M780 660 C800 700 790 760 760 800 L700 820 C690 812 690 796 700 790 L748 770 C760 740 760 700 750 668 Z" fill="{c["vesteO"]}"/>')
    o.append(f'<path d="M700 790 C680 790 660 800 664 818 C668 834 692 836 704 824 Z" fill="{c["peauO"]}"/>')
    # bras de devant : coude sur la table, main qui parle vers le micro
    o.append(f'<path d="M640 650 C610 670 600 720 604 780 C606 806 630 818 652 806 C664 760 668 700 664 664 Z" fill="{c["bras"]}"/>')
    o.append(f'<path d="M612 790 C580 770 548 742 528 712 L556 690 C580 718 612 746 646 770 Z" fill="{c["bras"]}"/>')
    o.append(f'<path d="M546 696 L532 710" stroke="{c["chemise"]}" stroke-width="14"/>')
    o.append(f'<path d="M530 706 C512 690 506 664 520 652 C530 642 546 650 552 664 L560 650 C566 642 578 646 576 658 L570 690 Z" fill="{c["peau"]}"/>')
    o.append(f'<path d="M520 652 L512 630 C510 622 520 618 526 626 L532 650" fill="{c["peau"]}"/>')
    # cou et tête (de trois quarts, tournée vers la table)
    o.append(f'<path d="M676 580 L716 580 L720 636 C706 646 688 646 674 636 Z" fill="{c["peauO"]}"/>')
    o.append(f'<path d="M640 520 C636 470 662 438 700 438 C738 438 758 470 756 520 C754 566 730 596 696 598 C664 600 644 572 640 520 Z" fill="{c["peau"]}"/>')
    o.append(f'<path d="M640 520 C638 540 640 552 632 560 C640 566 648 566 652 560 Z" fill="{c["peau"]}"/>')   # nez
    o.append(f'<path d="M660 438 C690 416 740 420 760 450 C772 470 770 500 762 520 L752 520 C748 490 736 470 712 464 C690 470 664 470 648 466 C648 452 652 444 660 438 Z" fill="{c["cheveux"]}"/>')
    o.append(f'<path d="M650 456 C646 418 670 394 706 388 C692 398 688 410 690 420 C712 398 746 396 768 410 C750 414 740 424 740 438 C756 436 772 444 780 458 C750 450 716 452 690 462 C676 466 660 466 650 456 Z" fill="{c["cheveux"]}"/>')
    o.append(f'<path d="M668 430 C680 412 696 404 712 400" stroke="#5A3A24" stroke-width="5" fill="none" stroke-linecap="round"/>')
    # lunettes noires rectangulaires, œil et sourcil
    o.append(f'<rect x="648" y="500" width="40" height="28" rx="6" fill="none" stroke="{c["lunettes"]}" stroke-width="5"/><path d="M648 512 L636 510 M688 512 L740 506" stroke="{c["lunettes"]}" stroke-width="5" stroke-linecap="round"/>')
    o.append(f'<circle cx="666" cy="515" r="5" fill="{c["lunettes"]}"/><path d="M652 490 L680 486" stroke="{c["cheveux"]}" stroke-width="6" stroke-linecap="round"/>')
    o.append(f'<path d="M654 572 C664 578 676 578 684 572" stroke="#7A4528" stroke-width="4" fill="none" stroke-linecap="round"/>')
    # casque couleur braise
    o.append(f'<path d="M684 440 C700 400 770 404 780 470" stroke="{c["casque"]}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="760" cy="514" rx="30" ry="40" fill="{c["casque"]}"/><ellipse cx="770" cy="514" rx="20" ry="32" fill="{c["casqueO"]}"/>')
    return "\n".join(o)

if __name__ == "__main__":
    out = os.path.join(ROOT, "personnage/presentateur_style_plat.svg")
    open(out, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1500" width="1000" height="1500">\n{scene()}\n</svg>')
    print("écrit", out)
