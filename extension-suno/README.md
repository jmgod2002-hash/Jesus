# Atelier Suno — extension Chrome

Aide à écrire les prompts Suno, sans quitter la page.

## Ce qu'elle fait
- **Télécharger** : repère les chansons affichées sur la page Suno (ta bibliothèque, une playlist, une page de chanson), tu coches, elle télécharge les MP3 et, en option, les pochettes, dans `Téléchargements/Suno/`. Les téléchargements continuent même si tu fermes la fenêtre de l'extension.
- **Style** : clique des mots-clés (genre, ambiance, voix, instruments, tempo, production), ajoute les tiens, précise ce qu'il faut exclure. Le texte du style se construit tout seul, avec un compteur de caractères.
- **Paroles** : modèles de structure (pop, louange, hip-hop, électro, format court…) et balises Suno (`[Verse]`, `[Chorus]`, `[Bridge]`…) à insérer au curseur.
- **Bibliothèque** : enregistre tes styles et paroles, recherche, export/import en JSON (sauvegarde ou partage).
- **Insérer dans Suno** : écrit directement dans le champ de suno.com (remplacer, ajouter à la fin, ou au curseur). Si le champ est introuvable, le texte est copié dans le presse-papiers.
- Le brouillon est gardé quand on ferme la fenêtre.

## Installer
1. Ouvre `chrome://extensions`.
2. Active **Mode développeur** (en haut à droite).
3. **Charger l'extension non empaquetée** → choisis le dossier `extension-suno`.
4. Épingle l'icône (note orange) dans la barre d'outils.

## Utiliser l'insertion
- Sur suno.com, **clique d'abord dans le champ voulu** (style ou paroles), puis ouvre l'extension et clique « Insérer dans Suno ».
- Sans clic préalable, l'extension cherche le champ par son texte d'aide (« lyrics », « style »…). Ça marche tant que Suno ne change pas ses libellés.

## Utiliser le téléchargement
1. Va sur suno.com, ouvre ta bibliothèque ou une playlist.
2. **Fais défiler jusqu'en bas** : Suno charge les chansons au fur et à mesure, l'extension ne voit que celles déjà affichées.
3. Ouvre l'extension → « Analyser la page » → coche → « Télécharger ».
4. Si Chrome demande « Autoriser plusieurs téléchargements », accepte.

## Limites
- Le MP3 est récupéré à l'adresse publique de Suno (`cdn1.suno.ai/<id>.mp3`). Si un fichier échoue, lance la chanson une fois sur la page puis relance l'analyse : l'extension récupère alors l'adresse réelle utilisée par le lecteur.
- Pas de WAV : c'est une option payante de Suno, l'extension ne la contourne pas.
- Droits : en offre gratuite, Suno réserve l'usage commercial aux abonnés. Télécharger ne change rien à ça. Les chansons des autres restent à eux.
- Suno n'a pas d'API publique : l'insertion dépend de la structure de leur page. Si Suno la modifie, la méthode « clic dans le champ puis Insérer » reste la plus fiable.
- Aucune donnée n'est envoyée ailleurs : tout est stocké localement dans Chrome.

## Personnaliser
Les mots-clés et modèles sont dans `data.js`. Modifie, puis clique « Actualiser » sur `chrome://extensions`.
