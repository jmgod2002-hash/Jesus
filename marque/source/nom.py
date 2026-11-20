"""Logotype « Feu d'Élévation » : la police Anallop n'a pas d'accents ; on dessine des accents aigus
taillés comme ses lettres (même épaisseur de trait, coupes droites), à la bonne hauteur.
Écrit marque/nom_feu_d_elevation.svg (ligne de base à y = 0, mêmes chasses que la police)."""
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
t = TTFont(os.path.join(ROOT, 'marque/Anallop.ttf')); gs = t.getGlyphSet(); cm = t.getBestCmap(); hm = t['hmtx']

def bounds(g):
    p = BoundsPen(gs); gs[g].draw(p); return p.bounds

STEM = bounds('l')[2] - bounds('l')[0]            # épaisseur d'un fût vertical
CAP, XH = bounds('E')[3], bounds('e')[3]

def aigu(cx, base):
    """Accent aigu : biseau plein, aussi épais que les lettres, incliné d'environ 40°."""
    w, h = STEM * 0.92, STEM * 1.15
    dx = h * 0.85
    x0 = cx - (w + dx) / 2
    pts = [(x0, base), (x0 + w, base), (x0 + w + dx, base + h), (x0 + dx * 0.98, base + h)]
    return "M" + " L".join(f"{x:.0f} {-y:.0f}" for x, y in pts) + "Z"

def build():
    pen = SVGPathPen(None); x = 0; acc = []
    for ch in "Feu d’Élévation":
        base = {"É": "E", "é": "e"}.get(ch, ch)
        g = cm[ord(base)] if base != "’" else cm[ord("'")]
        TransformPen(pen, (1, 0, 0, -1, x, 0)); gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        if ch in "Éé":
            b = bounds(g); gap = STEM * 0.38
            cx = x + (b[0] + b[2]) / 2 + (STEM * 0.18 if ch == "É" else STEM * 0.05)
            acc.append(aigu(cx, (CAP if ch == "É" else XH) + gap))
        x += hm[g][0]
    top = CAP + STEM * (0.38 + 1.15) + 12
    return pen.getCommands() + "".join(acc), x, top

if __name__ == "__main__":
    d, w, top = build()
    vb = f"0 {-top:.0f} {w:.0f} {top + 22:.0f}"
    open(os.path.join(ROOT, 'marque/nom_feu_d_elevation.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"><path fill="#3B2412" d="{d}"/></svg>')
    print("fût", STEM, "| capitale", CAP, "| x", XH, "| viewBox", vb)
