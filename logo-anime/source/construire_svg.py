# Génère ../logo_anime.svg à partir du contour vectorisé du T (t_clean.d).
# Entrée unique (0 → 1,4 s) puis boucle de 4 s (regard, clignement, balancement) à l'infini.
from pathlib import Path
here = Path(__file__).parent
T = (here / "t_clean.d").read_text().strip()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1254 1254" width="1254" height="1254">
<title>Logo animé</title>
<style>
  g {{ transform-box: view-box; transform-origin: 0 0; }}
  #disc   {{ animation: pop 0.55s cubic-bezier(.2,.7,.3,1) both; }}
  #drop   {{ animation: drop 0.5s 0.35s cubic-bezier(.55,0,1,.6) both; }}
  #squash {{ animation: squash 1.4s linear both; }}
  #sway   {{ animation: sway 4s 1.4s ease-in-out infinite; }}
  #eyeOpen{{ animation: eyeOpen 1.4s linear both; }}
  #blink  {{ animation: blink 4s 1.4s linear infinite; }}
  #pupil  {{ animation: look 4s 1.4s cubic-bezier(.6,0,.3,1) infinite; }}
  @keyframes pop    {{ 0% {{ transform: translate(626.5px, 623.5px) scale(0.001) translate(-626.5px, -623.5px); }} 70% {{ transform: translate(626.5px, 623.5px) scale(1.02) translate(-626.5px, -623.5px); }} 100% {{ transform: translate(626.5px, 623.5px) scale(1) translate(-626.5px, -623.5px); }} }}
  @keyframes drop   {{ from {{ transform: translateY(-1150px) rotate(-10deg); }} to {{ transform: none; }} }}
  @keyframes squash {{
    0%, 61% {{ transform: translate(690px, 1060px) scale(1, 1.06) translate(-690px, -1060px); }}
    68%  {{ transform: translate(690px, 1060px) scale(1.16, 0.82) translate(-690px, -1060px); }}
    79%  {{ transform: translate(690px, 1060px) scale(0.93, 1.09) translate(-690px, -1060px); }}
    89%  {{ transform: translate(690px, 1060px) scale(1.03, 0.97) translate(-690px, -1060px); }}
    100% {{ transform: translate(690px, 1060px) scale(1, 1) translate(-690px, -1060px); }} }}
  @keyframes eyeOpen {{
    0%, 72% {{ transform: translate(382px, 430px) scaleY(0.06) translate(-382px, -430px); }}
    82%  {{ transform: translate(382px, 430px) scaleY(1.08) translate(-382px, -430px); }}
    90%, 100% {{ transform: translate(382px, 430px) scaleY(1) translate(-382px, -430px); }} }}
  @keyframes sway {{
    0%   {{ transform: translate(690px, 1060px) rotate(0deg) translate(-690px, -1060px); }}
    25%  {{ transform: translate(690px, 1060px) rotate(-2.5deg) translate(-690px, -1060px); }}
    55%  {{ transform: translate(690px, 1060px) rotate(1.8deg) scale(1, 1.03) translate(-690px, -1060px); }}
    80%  {{ transform: translate(690px, 1060px) rotate(-0.6deg) translate(-690px, -1060px); }}
    100% {{ transform: translate(690px, 1060px) rotate(0deg) translate(-690px, -1060px); }} }}
  @keyframes look {{
    0%, 12%  {{ transform: translate(0, 0); }}
    22%, 42% {{ transform: translate(-60px, -4px); }}
    52%, 64% {{ transform: translate(-28px, -40px); }}
    74%, 100% {{ transform: translate(0, 0); }} }}
  @keyframes blink {{
    0%, 80% {{ transform: translate(382px, 430px) scaleY(1) translate(-382px, -430px); }}
    83%  {{ transform: translate(382px, 430px) scaleY(0.06) translate(-382px, -430px); }}
    87%, 100% {{ transform: translate(382px, 430px) scaleY(1) translate(-382px, -430px); }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<defs>
  <clipPath id="clipDisc"><circle cx="626.5" cy="623.5" r="612"/></clipPath>
  <clipPath id="clipT"><path d="{T}"/></clipPath>
  <clipPath id="clipEye"><ellipse cx="382" cy="418" rx="82" ry="122" transform="rotate(3 382 418)"/></clipPath>
</defs>
<g id="disc"><circle cx="626.5" cy="623.5" r="612" fill="#64429e"/></g>
<g clip-path="url(#clipDisc)"><g id="drop"><g id="squash"><g id="sway">
  <path d="{T}" fill="#fe6132"/>
  <g clip-path="url(#clipT)"><g id="eyeOpen"><g id="blink">
    <ellipse cx="382" cy="418" rx="82" ry="122" transform="rotate(3 382 418)" fill="#fff"/>
    <g clip-path="url(#clipEye)"><circle id="pupil" cx="444" cy="458" r="50" fill="#fe6132"/></g>
  </g></g></g>
</g></g></g></g>
</svg>
'''
(here.parent / "logo_anime.svg").write_text(svg)
print("OK → logo_anime.svg")
