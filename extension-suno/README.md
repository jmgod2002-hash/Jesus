# Atelier Suno — extension Chrome

Enregistre tes chansons Suno et aide à écrire les prompts, sans quitter la page.

## Ce qu'elle fait
- **Bouton ⬇ à côté de chaque titre** sur suno.com (et dans la barre de lecture). Un clic ajoute la chanson à la file d'enregistrement. Le bouton affiche ensuite ⏳ (en attente), le pourcentage d'avancement, ✓ (enregistré) ou ✕ (échec : survole pour lire l'erreur, clique pour réessayer).
- **Pop-up en bas à droite** quand une chanson se lance, avec « ⬇ Télécharger ».
- **Onglet Télécharger** : file d'enregistrement en direct, analyse de la page pour ajouter plusieurs chansons d'un coup, option pochette, réglages.
- **Style / Paroles / Bibliothèque** : constructeur de style, modèles de structure, prompts enregistrés.

## Comment marche le téléchargement
Suno chiffre ses fichiers audio : il n'existe plus de lien MP3 direct. L'extension fait donc comme l'extension « Bulk Downloader » :
1. elle ouvre la chanson dans une **petite fenêtre Suno**, son coupé ;
2. elle la lit du début à la fin et **enregistre ce que joue le lecteur de Suno** ;
3. elle enregistre le fichier dans `Téléchargements/Suno/Titre [xxxxxxxx].m4a`, puis ferme la fenêtre.

Conséquences :
- **Temps réel** : 3 min de chanson = 3 min d'attente. Les chansons passent une par une.
- **Ne ferme pas la petite fenêtre**, elle se ferme seule. Tu peux continuer à utiliser Suno à côté.
- **Qualité** : le son est ré-encodé à 256 kbit/s à partir du flux de Suno (environ 145 kbit/s). Pas de perte audible, mais ce n'est pas le fichier original. Pour un WAV, il faut passer par l'offre payante de Suno.

## Démarrage automatique (recommandé)
Chrome refuse qu'une page lance un son sans clic de l'utilisateur, sauf sur les sites où tu écoutes souvent. Trois niveaux :
1. **Clic simple** : marche si Chrome considère Suno comme un site que tu écoutes souvent.
2. **Démarrage automatique** (case dans l'onglet Télécharger) : l'extension envoie un vrai clic sur ▶. Chrome demande la permission « déboguer » une seule fois, puis affiche un bandeau « Atelier Suno a commencé le débogage » une fraction de seconde à chaque chanson. C'est normal.
3. **Sinon** : la fenêtre d'enregistrement passe devant avec un bandeau orange. Clique sur ▶ Play, l'enregistrement démarre (son toujours coupé).

## Installer
1. Ouvre `chrome://extensions`.
2. Active **Mode développeur** (en haut à droite).
3. **Charger l'extension non empaquetée** → choisis le dossier `extension-suno`.
4. Épingle l'icône (note orange) dans la barre d'outils.
5. Si une page Suno était ouverte, recharge-la.

Mise à jour : remplace le dossier, puis clique « Actualiser » sur `chrome://extensions` et recharge Suno.

## Limites
- L'extension dépend de la page de Suno (bouton « Play », lecteur audio). Si Suno change son site, ça peut casser.
- Droits : en offre gratuite, Suno réserve l'usage commercial aux abonnés. Enregistrer ne change rien à ça. Les chansons des autres restent à eux.
- Conditions de Suno : enregistrer la lecture contourne l'absence de bouton de téléchargement. Usage personnel ; risque théorique pour le compte en cas d'usage massif.
- Tout reste sur ton ordinateur : aucune donnée envoyée ailleurs.

## Personnaliser
Les mots-clés et modèles de paroles sont dans `data.js`.
