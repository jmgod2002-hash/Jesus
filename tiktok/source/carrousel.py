"""Carrousel TikTok « Jésus est… » (mode photo, 1080 x 1920) dans la DA Feu d'Élévation.
Génère une page HTML contenant toutes les images ; rendre avec rendu.js."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logo_d = re.search(r' d="([^"]+)"', open(os.path.join(ROOT, 'youtube/logo.svg')).read()).group(1)
nom = open(os.path.join(ROOT, 'marque/nom_feu_d_elevation.svg')).read()
nom_vb = re.search(r'viewBox="([^"]+)"', nom).group(1); nom_d = re.search(r' d="([^"]+)"', nom).group(1)

SLIDES = [
    ("JÉSUS SAUVE", None),
    ("JÉSUS GUÉRIT", None),
    ("JÉSUS EST PUISSANT", None),
    ("JÉSUS EST FIDÈLE", None),
    ("JÉSUS T’AIME", None),
    ("JÉSUS EST DIEU", None),
    ("JÉSUS EST LE CHEMIN, LA VÉRITÉ ET LA VIE", "Jean 14:6"),
]
CTA = "Si Jésus compte pour toi, écris « Amen » en commentaire et partage à quelqu’un qui en a besoin aujourd’hui."

def torche(h, op=1):
    return f'<svg viewBox="0 0 486 800" style="height:{h}px;opacity:{op}" fill="#3B2412" fill-rule="evenodd"><path d="{logo_d}"/></svg>'

def slide(i, body):
    return f'<section class="s" id="s{i}">{body}</section>'

parts = []
for i, (txt, ref) in enumerate(SLIDES, 1):
    body = f'<div class="t">{txt}</div>' + (f'<div class="ref">{ref}</div>' if ref else '') + f'<div class="mark">{torche(58, .9)}</div>'
    parts.append(slide(i, body))
parts.append(slide(len(SLIDES) + 1,
    f'<div class="cta">{CTA}</div><div class="sign">{torche(150)}'
    f'<svg viewBox="{nom_vb}" style="width:430px;margin-top:34px" fill="#3B2412"><path d="{nom_d}"/></svg></div>'))

html = f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;background:#000}}
.s{{width:1080px;height:1920px;position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;
  background:radial-gradient(ellipse 70% 45% at 50% 44%,#FFFBF3 0%,#F5EDE0 55%,#E6D5BB 100%);font-family:Inter,Arial,sans-serif;color:#3B2412}}
.t{{position:absolute;top:44%;transform:translateY(-50%);width:860px;text-align:center;font-weight:600;font-size:66px;line-height:1.25;letter-spacing:.06em;text-wrap:balance}}
.ref{{position:absolute;top:calc(44% + 150px);font-weight:500;font-size:38px;letter-spacing:.12em;color:#8A6040}}
.mark{{position:absolute;top:1420px}}
.cta{{position:absolute;top:30%;width:820px;font-weight:500;font-size:52px;line-height:1.4;text-align:center;text-wrap:balance}}
.sign{{position:absolute;top:56%;display:flex;flex-direction:column;align-items:center}}
</style></head><body>{"".join(parts)}</body></html>'''
out = os.path.join(ROOT, 'tiktok/source/carrousel.html')
open(out, 'w').write(html)
print("écrit", out, len(parts), "images")
