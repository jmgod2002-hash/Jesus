"""Carrousel TikTok « Lance ton SaaS » (mode photo, 1080 x 1920), DA du compte Claudio :
fond crème à points, étiquettes à contour noir et ombre tramée, personnage plat au bureau.
Génère carrousel_saas.html ; rendre avec : node rendu_saas.js"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
N = 10
K = '#141414'
SKIN, HAIR, LID = '#BA8059', '#17110C', '#3A3A39'

def perso(w=480, bulle=None):
    """Personnage de face, derrière son ordinateur, posé sur un bureau (repère 500 x 600)."""
    st = f'stroke="{K}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"'
    curls = ''.join(f'<path d="M{x} {y} a9 9 0 1 1 9 9" fill="none" stroke="#4A3B30" stroke-width="4" stroke-linecap="round"/>'
                    for x, y in [(170,120),(215,95),(265,92),(312,105),(350,135),(190,155),(240,135),(292,140),(335,170),(150,175)])
    bumps = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in
                    [(250,150,118),(135,175,34),(150,130,36),(190,98,38),(240,82,40),(292,86,40),(338,108,38),(368,148,34),(372,190,28),(128,215,24)])
    svg = f'''<svg viewBox="0 0 500 600" width="{w}" class="psvg">
<defs><pattern id="tr" width="11" height="11" patternUnits="userSpaceOnUse"><circle cx="5.5" cy="5.5" r="3.6" fill="{K}"/></pattern>
<pattern id="mar" width="40" height="34" patternUnits="userSpaceOnUse"><rect width="40" height="34" fill="#FBFAF7"/><rect y="20" width="40" height="12" fill="#3A3F66"/></pattern></defs>
<g transform="translate(-26 8)" fill="url(#tr)">{bumps}<ellipse cx="250" cy="250" rx="128" ry="135"/></g>
<path d="M70 600 C70 500 120 450 200 440 L300 440 C380 450 430 500 430 600Z" fill="url(#mar)" {st}/>
<path d="M212 330 L212 445 Q250 470 288 445 L288 330Z" fill="{SKIN}" {st}/>
<circle cx="124" cy="258" r="28" fill="{SKIN}" {st}/><circle cx="376" cy="258" r="28" fill="{SKIN}" {st}/>
<g fill="{HAIR}" stroke="{K}" stroke-width="7">{bumps}</g>
<g fill="{HAIR}">{bumps}</g>{curls}
<path d="M126 205 Q130 168 175 170 Q250 176 325 170 Q370 168 374 205 L372 280 Q366 352 300 385 Q250 402 200 385 Q134 352 128 280Z" fill="{SKIN}" {st}/>
<path d="M158 212 Q192 192 228 206" fill="none" stroke="{K}" stroke-width="17" stroke-linecap="round"/>
<path d="M272 206 Q308 192 342 212" fill="none" stroke="{K}" stroke-width="17" stroke-linecap="round"/>
<clipPath id="eg"><ellipse cx="195" cy="250" rx="38" ry="25"/></clipPath><clipPath id="ed"><ellipse cx="305" cy="250" rx="38" ry="25"/></clipPath>
<ellipse cx="195" cy="250" rx="38" ry="25" fill="#FCFDFC"/><ellipse cx="305" cy="250" rx="38" ry="25" fill="#FCFDFC"/>
<g clip-path="url(#eg)"><circle cx="207" cy="258" r="12" fill="{K}"/><rect x="150" y="215" width="90" height="34" fill="{LID}"/></g>
<g clip-path="url(#ed)"><circle cx="317" cy="258" r="12" fill="{K}"/><rect x="260" y="215" width="90" height="34" fill="{LID}"/></g>
<path d="M157 249 L233 249 M267 249 L343 249" stroke="{K}" stroke-width="8" stroke-linecap="round"/>
<ellipse cx="195" cy="250" rx="38" ry="25" fill="none" {st}/><ellipse cx="305" cy="250" rx="38" ry="25" fill="none" {st}/>
<path d="M252 262 Q244 290 236 300 Q248 310 262 302" fill="none" stroke="{K}" stroke-width="5.5" stroke-linecap="round"/>
<path d="M208 325 Q250 312 292 325 Q285 336 250 330 Q215 336 208 325Z" fill="#3B2A1F"/>
<path d="M214 334 Q250 330 286 334 Q276 368 250 370 Q224 368 214 334Z" fill="#7A1F22" {st.replace('7"','5"')}/>
<path d="M226 356 Q250 345 274 356 Q266 368 250 369 Q234 368 226 356Z" fill="#D9545A"/>
<path d="M218 336 Q250 333 282 336 L280 343 Q250 340 220 343Z" fill="#FFF"/>
<path d="M232 382 Q250 400 268 382 Q258 392 250 392 Q242 392 232 382Z" fill="#3B2A1F" opacity=".85"/>
<rect x="140" y="450" width="220" height="150" rx="16" fill="#D0C8BD" {st}/>
<circle cx="250" cy="512" r="16" fill="#FBFAF7" {st.replace('7"','5"')}/>
</svg>'''
    b = f'<div class="bulle"><span>{bulle}</span></div>' if bulle else ''
    return (f'<div class="scene">{b}<div class="perso">{svg}</div>'
            f'<div class="desk"><div class="top"></div><div class="dr"><i></i></div></div></div>')

def pill(ic, txt, cls=''):
    return f'<div class="pl {cls}"><span class="ic">{ic}</span><span class="tx">{txt}</span></div>'

def page(lab, titre, sous='', corps='', bulle=None, perso_on=True):
    s = f'<div class="lab">// {lab}</div><h2>{titre}</h2>'
    if sous: s += f'<p class="sous">{sous}</p>'
    return s + f'<div class="pls">{corps}</div>' + (perso(bulle=bulle) if perso_on else '')

S = []
S.append('<div class="lab">// guide complet · 2026</div><h1>Lance ton <mark>SaaS</mark><br>sans savoir coder</h1>'
         '<div class="pls row">' + pill('1', 'Claude') + pill('2', 'Nom de domaine') + pill('3', 'Serveur') + pill('4', 'Paiements') + '</div>'
         + perso(bulle='Enregistre, tu vas en avoir besoin') + '<div class="swipe">glisse →</div>')
S.append(page('la base', 'Un SaaS, c’est quoi ?', 'Un logiciel dans le navigateur, payé <b>chaque mois</b>.',
    pill('→', 'Notion, Canva, Calendly') + pill('→', 'Rien à installer : un lien, un compte') + pill('€', '100 clients × 15 € = <b>1 500 € / mois</b>', 'mint'),
    'Tu le crées une fois. Tu le vends tous les mois.'))
S.append(page('étape 1 / 5 · l’idée', 'Un problème précis', 'Pour des gens précis.',
    pill('✓', 'Une tâche que des gens font <b>à la main</b>') + pill('✓', 'Un métier : coiffeurs, coachs, artisans') + pill('!', 'Trouve <b>10 personnes</b> prêtes à payer avant de coder', 'mint'),
    'Pas de clients, pas de SaaS.'))
S.append(page('étape 2 / 5 · le code', 'Claude, ton développeur', 'Tu expliques en français, il écrit le code.',
    pill('✓', 'Il crée les pages et la base de données') + pill('✓', 'Il corrige les bugs et explique tout') + pill('€', 'Environ <b>20 € / mois</b>', 'mint'),
    'Toi, tu restes le chef : tu testes tout.'))
S.append(page('étape 3 / 5 · l’adresse', 'Le nom de domaine', 'L’adresse de ton SaaS sur internet.',
    pill('@', '<b>monsaas.com</b>') + pill('✓', 'OVH, Cloudflare, Namecheap') + pill('€', '<b>10 à 15 € / an</b>', 'mint'),
    'Court, facile à dire, facile à écrire.'))
S.append(page('étape 4 / 5 · le serveur', 'VPS ou cloud ?', 'L’endroit où ton SaaS tourne 24 h / 24.',
    pill('A', '<b>Cloud</b> (Vercel, Render) : simple, ~20 € / mois en pro') + pill('B', '<b>VPS</b> (Hetzner, OVH) : dès ~5 € / mois, tu gères tout') + pill('→', 'Débutant : commence par le cloud', 'mint'),
    'Le VPS coûte moins, mais demande plus.'))
S.append(page('étape 5 / 5 · l’argent', 'Comptes et paiements', 'Ce qui transforme ton site en business.',
    pill('✓', '<b>Supabase</b> : comptes clients + données') + pill('✓', '<b>Stripe</b> : abonnements par carte') + pill('€', 'Stripe : une commission par paiement', 'mint'),
    'Claude branche les deux pour toi.'))
fl = ''.join(pill(str(i), t, 'mint' if i == 5 else '') + ('<div class="arr">↓</div>' if i < 5 else '') for i, t in enumerate(
    ['<b>Ton client</b> tape monsaas.com', '<b>Le domaine</b> l’envoie au serveur', '<b>Le serveur</b> fait tourner ton app',
     '<b>Ton app</b>, codée avec Claude', '<b>Stripe</b> encaisse l’abonnement'], 1))
S.append(page('le schéma', 'Comment tout se relie', '', fl, perso_on=False).replace('class="pls"', 'class="pls flux"'))
S.append(page('la vérité', 'Ce que ça coûte vraiment', '',
    pill('€', 'Budget de départ : <b>≈ 30 € / mois</b>', 'mint') + pill('!', 'Le vrai coût : <b>ton temps</b>, des semaines') + pill('!', 'Le plus dur : <b>trouver des clients</b>'),
    'Seul, on bloque souvent au même endroit.'))
S.append('<div class="lab">// et maintenant ?</div><h1 class="cta">Tu veux lancer <mark>ton</mark> SaaS ?</h1>'
         '<p class="sous">Je t’accompagne étape par étape : l’idée, Claude, le domaine, le serveur, les paiements.</p>'
         '<div class="pls">' + pill('💬', 'Écris <b>« SAAS »</b> en commentaire', 'mint big') + '</div>' + perso(bulle='Je te réponds en privé'))

NB = lambda t: (t.replace(' :', ' :').replace(' ?', ' ?').replace(' !', ' !').replace('« ', '« ')
                 .replace(' »', ' »').replace(' / ', ' / ').replace(' €', ' €').replace(' ×', ' ×'))
parts = ''.join(f'<section class="s" id="s{i}"><div class="bar"><i style="width:{i*100/N:.1f}%"></i></div>{NB(b)}</section>'
                for i, b in enumerate(S, 1))
CSS = f'''
html,body{{margin:0;background:#000}}
.s{{width:1080px;height:1920px;position:relative;overflow:hidden;box-sizing:border-box;padding:270px 80px 0;display:flex;flex-direction:column;align-items:center;text-align:center;
 font-family:Inter,Arial,sans-serif;color:{K};background:radial-gradient(circle,#CFCAC0 2.6px,transparent 3.2px) 0 0/48px 48px,#F1EDE5}}
.bar{{position:absolute;top:170px;left:80px;right:80px;height:12px;border-radius:6px;background:#CAC6BF;overflow:hidden}}
.bar i{{display:block;height:100%;background:#D23D26;border-radius:6px}}
.lab{{font-family:"JetBrains Mono",monospace;font-size:38px;font-weight:500;color:#3A3A39;letter-spacing:.02em}}
h1,h2{{margin:18px 0 0;font-weight:900;letter-spacing:-.02em;text-wrap:balance}}
h1{{font-size:116px;line-height:1.02}}h1.cta{{font-size:104px}}
h2{{font-size:92px;line-height:1.04}}
mark{{background:#CFF3E0;color:inherit;padding:0 14px;border-radius:18px;box-shadow:inset 0 0 0 6px {K}}}
.sous{{font-size:42px;line-height:1.3;color:#3A3A39;margin:22px 0 0;font-weight:500;text-wrap:balance}}
.sous b{{color:{K};font-weight:800}}
.pls{{margin-top:46px;display:flex;flex-direction:column;align-items:center;gap:30px}}
.pls.flux{{gap:6px}}
.pls.row{{flex-direction:row;flex-wrap:wrap;justify-content:center;gap:28px 30px;max-width:900px}}
.pl{{position:relative;display:flex;align-items:center;gap:22px;max-width:880px;box-sizing:border-box;padding:18px 34px 18px 18px;background:#FFF;border:6px solid {K};border-radius:60px;text-align:left;font-size:40px;line-height:1.22;font-weight:600}}
.pl::after{{content:"";position:absolute;inset:0;transform:translate(14px,14px);z-index:-1;border-radius:60px;background:radial-gradient(circle,{K} 3px,transparent 3.6px) 0 0/10px 10px}}
.pl b{{font-weight:800}}
.pl.mint{{background:#CFF3E0}}
.pl.big{{font-size:50px;padding:24px 44px 24px 24px}}
.ic{{flex:none;width:66px;height:66px;border-radius:50%;border:5px solid {K};box-sizing:border-box;display:grid;place-items:center;font-weight:800;font-size:34px;background:#FFF}}
.arr{{font-size:44px;font-weight:900;line-height:1}}
.scene{{position:absolute;left:0;right:0;bottom:0;height:720px}}
.perso{{position:absolute;left:110px;bottom:190px}}
.desk{{position:absolute;left:-20px;right:-20px;bottom:0;height:200px}}
.desk .top{{height:44px;background:#C88C5A;border:6px solid {K}}}
.desk .dr{{position:absolute;left:120px;top:44px;width:520px;bottom:-10px;background:#EBC79A;border:6px solid {K};border-top:0}}
.desk .dr i{{position:absolute;left:50%;top:50px;width:110px;height:16px;margin-left:-55px;background:{K};border-radius:8px}}
.bulle{{position:absolute;left:580px;bottom:560px;width:340px}}
.bulle span{{position:relative;display:block;background:#FFF;border:6px solid {K};border-radius:36px;padding:24px 28px;font-size:36px;line-height:1.25;font-weight:700;text-align:left;text-wrap:balance}}
.bulle span::before{{content:"";position:absolute;left:-23px;top:50%;width:36px;height:36px;margin-top:-18px;background:#FFF;border-left:6px solid {K};border-bottom:6px solid {K};transform:rotate(45deg);border-radius:0 0 0 4px}}
.swipe{{position:absolute;right:80px;top:200px;font-family:"JetBrains Mono",monospace;font-size:34px;font-weight:700;color:#D23D26}}
'''
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{parts}</body></html>'
open(os.path.join(ROOT, 'tiktok/source/carrousel_saas.html'), 'w').write(html)
print(len(S), 'images')
