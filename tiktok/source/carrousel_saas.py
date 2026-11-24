"""Carrousel TikTok « Lancer ton SaaS » (mode photo, 1080 x 1920) avec le présentateur, DA plateau de nuit.
Génère carrousel_saas.html ; rendre avec : node rendu.js carrousel_saas"""
import os, base64
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def b64(p): return base64.b64encode(open(os.path.join(ROOT, p), 'rb').read()).decode()
FACE = b64('personnage/presentateur_3q_transparent.png')     # sourire, assis
PENSE = b64('personnage/presentateur_transparent.png')       # main au menton
N = 10

def perso(pose='face', bulle=None):
    img = FACE if pose == 'face' else PENSE
    b = f'<div class="bulle">{bulle}</div>' if bulle else ''
    return f'<div class="perso {pose}"><img src="data:image/png;base64,{img}"></div>{b}'

def etape(n, titre, sous, points, bulle, pose='face'):
    lis = ''.join(f'<li><span class="ck">{k}</span><span>{v}</span></li>' for k, v in points)
    return (f'<div class="pill">ÉTAPE {n} / 5</div><h2>{titre}</h2><p class="sous">{sous}</p>'
            f'<ul class="card">{lis}</ul>' + perso(pose, bulle))

S = []
# 1. Accroche
S.append('<div class="kick">GUIDE COMPLET · 2026</div>'
         '<h1>Lance ton <em>SaaS</em><br>sans savoir coder</h1>'
         '<p class="sous big">Claude, nom de domaine, serveur, paiements : tout ce qu’il te faut, dans l’ordre.</p>'
         + perso('face', 'Garde ce guide, tu vas en avoir besoin.') + '<div class="swipe">Glisse →</div>')
# 2. C'est quoi
S.append('<div class="pill">LA BASE</div><h2>Un SaaS, c’est quoi ?</h2>'
         '<p class="sous">Un logiciel qu’on utilise dans le navigateur et qu’on paie <b>chaque mois</b>.</p>'
         '<ul class="card"><li><span class="ck">→</span><span>Exemples : Notion, Canva, Calendly</span></li>'
         '<li><span class="ck">→</span><span>Rien à installer : un lien, un compte, c’est parti</span></li>'
         '<li><span class="ck">€</span><span>L’intérêt : <b>100 clients à 15 €</b> = 1 500 € qui reviennent tous les mois</span></li></ul>'
         + perso('pense', 'Tu crées l’outil une fois. Tu le vends tous les mois.'))
# 3-7. Étapes
S.append(etape(1, 'L’idée', 'Un problème précis, pour des gens précis.',
    [('✓', 'Pars d’une tâche que des gens font <b>à la main</b> et détestent'),
     ('✓', 'Vise un métier : coiffeurs, coachs, artisans…'),
     ('✓', 'Avant de coder : trouve <b>10 personnes</b> prêtes à payer')],
    'Pas de clients, pas de SaaS. Même avec le plus beau code.', 'pense'))
S.append(etape(2, 'Claude, ton développeur', 'Tu expliques en français, il écrit le code.',
    [('✓', 'Il crée les pages, la logique, la base de données'),
     ('✓', 'Il corrige les bugs et t’explique chaque étape'),
     ('€', 'Abonnement : <b>environ 20 € / mois</b>')],
    'Toi, tu restes le chef de projet : tu testes tout.'))
S.append(etape(3, 'Le nom de domaine', 'L’adresse de ton SaaS sur internet.',
    [('✓', 'Exemple : <b>monsaas.com</b>'),
     ('✓', 'Où l’acheter : OVH, Cloudflare, Namecheap'),
     ('€', 'Prix : <b>10 à 15 € / an</b>')],
    'Court, facile à dire, facile à écrire.'))
S.append(etape(4, 'Le serveur : VPS ou cloud ?', 'La maison où ton SaaS tourne 24 h / 24.',
    [('A', '<b>Cloud clé en main</b> (Vercel, Render) : simple, gratuit pour tester, ~20 € / mois en pro'),
     ('B', '<b>VPS</b> (Hetzner, OVH) : un serveur loué, dès ~5 € / mois, mais tu gères tout'),
     ('→', 'Débutant : commence par le cloud')],
    'Le VPS coûte moins cher, mais te demande plus de travail.', 'pense'))
S.append(etape(5, 'Comptes et paiements', 'Les deux briques qui font de ton site un business.',
    [('✓', '<b>Supabase</b> : connexion des clients + base de données (gratuit au départ)'),
     ('✓', '<b>Stripe</b> : abonnements et carte bancaire'),
     ('€', 'Stripe prend une commission sur chaque paiement, rien de fixe')],
    'Claude sait brancher les deux pour toi.'))
# 8. Schéma
flux = [('Ton client', 'tape monsaas.com'), ('Nom de domaine', 'l’envoie au bon endroit'),
        ('Serveur', 'fait tourner ton app'), ('Ton app', 'codée avec Claude'), ('Stripe', 'encaisse l’abonnement')]
fl = '<div class="fl">' + '<div class="arr">↓</div>'.join(f'<div class="node"><b>{a}</b><span>{b}</span></div>' for a, b in flux) + '</div>'
S.append('<div class="pill">LE SCHÉMA</div><h2>Comment tout se relie</h2>' + fl)
# 9. Réalité
S.append('<div class="pill">LA VÉRITÉ</div><h2>Ce que ça coûte vraiment</h2>'
         '<div class="tot"><span>Budget de départ</span><b>≈ 30 € / mois</b></div>'
         '<ul class="card"><li><span class="ck">!</span><span>Le vrai coût, c’est <b>ton temps</b> : des semaines, pas un week-end</span></li>'
         '<li><span class="ck">!</span><span>Le plus dur n’est pas le code : c’est <b>trouver des clients</b></span></li>'
         '<li><span class="ck">!</span><span>La sécurité et les données clients, ça ne s’improvise pas</span></li></ul>'
         + perso('pense', 'Seul, on bloque souvent au même endroit.'))
# 10. CTA
S.append('<h1 class="cta">Tu veux lancer <em>ton</em> SaaS ?</h1>'
         '<p class="sous big">Je t’accompagne étape par étape : l’idée, Claude, le domaine, le serveur, les paiements.</p>'
         '<div class="com">Écris <b>« SAAS »</b> en commentaire</div>'
         '<p class="sous">et je t’envoie un message.</p>' + perso('face'))

NB = lambda t: t.replace(' :', '\u00a0:').replace(' ?', '\u00a0?').replace(' !', '\u00a0!').replace('« ', '«\u00a0').replace(' »', '\u00a0»').replace(' / ', '\u00a0/\u00a0').replace(' €', '\u00a0€')
S = [NB(x) for x in S]
parts = ''.join(f'<section class="s" id="s{i}">{b}<div class="num">{i}/{N}</div></section>' for i, b in enumerate(S, 1))
CSS = '''
html,body{margin:0;background:#000}
.s{width:1080px;height:1920px;position:relative;overflow:hidden;box-sizing:border-box;padding:230px 90px 0;
 font-family:Inter,Arial,sans-serif;color:#F5EDE0;
 background:radial-gradient(circle at 12% 30%,rgba(217,160,74,.30),transparent 32%),
 radial-gradient(circle at 92% 62%,rgba(192,82,43,.28),transparent 30%),
 radial-gradient(ellipse 90% 60% at 50% 105%,#4A2A14 0%,transparent 70%),#160C06}
.s::after{content:"";position:absolute;inset:0;pointer-events:none;
 background:radial-gradient(circle at 86% 14%,rgba(255,214,140,.55) 0 6px,rgba(255,190,100,.18) 7px,transparent 90px),
 radial-gradient(circle at 70% 9%,rgba(255,214,140,.45) 0 5px,rgba(255,190,100,.14) 6px,transparent 70px)}
.num{position:absolute;top:150px;right:90px;font-size:30px;font-weight:600;color:#B89A7C;letter-spacing:.08em}
.kick,.pill{display:inline-block;font-size:30px;font-weight:700;letter-spacing:.14em;color:#160C06;background:#D9A04A;padding:12px 24px;border-radius:10px}
.pill{background:#C0522B;color:#FBF6EE}
h1{font-size:118px;line-height:1.02;font-weight:800;margin:40px 0 0;letter-spacing:-.02em;text-wrap:balance}
h1 em,h2 em{font-style:normal;color:#F2B45C}
h1.cta{margin-top:20px;font-size:108px}
h2{font-size:84px;line-height:1.06;font-weight:800;margin:34px 0 0;letter-spacing:-.015em;text-wrap:balance}
.sous{font-size:42px;line-height:1.3;color:#E6D5BB;margin:28px 0 0;font-weight:500;text-wrap:balance}
.sous.big{font-size:46px}.sous b{color:#F2B45C}
.card{list-style:none;margin:48px 0 0;padding:34px 38px;background:rgba(251,246,238,.07);border:2px solid rgba(217,160,74,.45);border-radius:28px;display:flex;flex-direction:column;gap:30px}
.card li{display:flex;gap:26px;align-items:flex-start;font-size:40px;line-height:1.3;font-weight:500}
.card b{color:#F2B45C;font-weight:700}
.ck{flex:none;width:58px;height:58px;border-radius:50%;background:#D9A04A;color:#160C06;display:grid;place-items:center;font-weight:800;font-size:32px;margin-top:-4px}
.perso{position:absolute;left:-60px;bottom:-80px;width:690px;height:880px;overflow:hidden}
.perso img{width:100%;display:block;filter:drop-shadow(0 0 40px rgba(217,160,74,.35))}
.perso.pense{width:640px;left:-50px}
.bulle{position:absolute;left:540px;bottom:560px;width:350px;background:#FBF6EE;color:#2A1A10;font-size:36px;line-height:1.28;font-weight:600;padding:30px 34px;border-radius:30px;text-wrap:balance}
.bulle::before{content:"";position:absolute;left:-26px;bottom:44px;border:16px solid transparent;border-right:26px solid #FBF6EE;border-left:0}
.swipe{position:absolute;right:90px;bottom:300px;font-size:38px;font-weight:700;color:#F2B45C}
.fl{margin-top:50px;display:flex;flex-direction:column;align-items:center;gap:6px}
.node{width:780px;box-sizing:border-box;padding:26px 36px;border-radius:24px;background:rgba(251,246,238,.08);border:2px solid rgba(217,160,74,.5);display:flex;justify-content:space-between;align-items:center;gap:20px}
.node b{font-size:44px;font-weight:800;color:#F2B45C}.node span{font-size:34px;color:#E6D5BB;text-align:right}
.node:last-child{background:#C0522B;border-color:#C0522B}.node:last-child b,.node:last-child span{color:#FBF6EE}
.arr{font-size:46px;color:#D9A04A;font-weight:800;line-height:1}
.tot{margin-top:44px;display:flex;justify-content:space-between;align-items:baseline;padding:30px 38px;border-radius:24px;background:#D9A04A;color:#160C06}
.tot span{font-size:38px;font-weight:600}.tot b{font-size:60px;font-weight:800}
.com{margin-top:60px;display:inline-block;font-size:56px;font-weight:700;padding:30px 44px;border-radius:24px;background:#C0522B;color:#FBF6EE}
.com b{color:#FFE3B0}
'''
html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{parts}</body></html>'
open(os.path.join(ROOT, 'tiktok/source/carrousel_saas.html'), 'w').write(html)
print(len(S), 'images')
