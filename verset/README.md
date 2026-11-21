# Verset du jour — format et chaîne de production

Un épisode = un verset, décliné en 3 vidéos :
- une vidéo longue YouTube (16:9, environ 5 min) ;
- un Short YouTube (9:16, environ 55 s) ;
- une vidéo TikTok (9:16, environ 55 s).

Seule la fin du Short change entre YouTube et TikTok.

## La structure, corrigée

Ta proposition : extrait + intro logo + présentateur + contexte + CTA + fin.
L'ordre est bon pour la vidéo longue. Trois corrections :

- **Il manque le verset lui-même et l'application.** Sans « le verset à l'écran » et « ce que ça change pour toi », il n'y a pas de raison de rester.
- **Le CTA ne doit pas être à la toute fin.** À la fin, la moitié du public est déjà partie. On le place juste après l'application, avant la prière : la prière garde les gens jusqu'au bout.
- **Le Short n'a ni intro logo ni carte de fin.** Les 2 premières secondes décident si on reste. Un logo à cet endroit fait fuir. Et un Short doit boucler : la dernière phrase relance la première.

### Vidéo longue (YouTube)

| # | Bloc | Durée | Rôle |
|---|---|---|---|
| 1 | Accroche | 15 à 25 s | La situation du spectateur (« il est tard, tu as peur ») et la promesse |
| 2 | Intro logo | 6 s | `youtube/intro_1920x1080.mp4`, insérée telle quelle |
| 3 | Présentateur | 10 à 15 s | Bienvenue, nom de la série, référence du jour |
| 4 | Le verset | 15 à 20 s | Lu lentement, affiché mot à mot (Louis Segond 1910) |
| 5 | Contexte | 45 à 60 s | Qui, quand, pourquoi |
| 6 | Ce que ça veut dire | 60 à 75 s | Un ou deux détails du texte (mot hébreu, construction) |
| 7 | Pour toi aujourd'hui | 40 à 50 s | Application concrète + écho dans le Nouveau Testament |
| 8 | CTA | 10 à 15 s | Abonnement + phrase à écrire en commentaire |
| 9 | Prière | 35 à 45 s | Courte, à répéter |
| 10 | Fin | 20 s | Écran de fin YouTube : vidéo suivante + abonnement |

### Short (YouTube Shorts et TikTok)

| # | Bloc | Durée | Rôle |
|---|---|---|---|
| 1 | Accroche | 2 à 4 s | Gros titre à l'écran, dit à voix haute |
| 2 | Le verset | 10 à 13 s | Carte du verset, mot à mot |
| 3 | Contexte express | 15 à 20 s | Un seul fait marquant |
| 4 | Pour toi | 8 à 10 s | Une phrase à retenir |
| 5 | CTA | 8 à 10 s | YouTube : abonnement + « explication complète en dessous » ; TikTok : suivre + commentaire |

La dernière phrase (« si tu as peur ce soir… ») renvoie à la première : la vidéo boucle.

## Ce qu'il faut savoir avant de lancer la série

- **« Verset du jour » n'est presque pas recherché** (vidIQ : moins de 750 recherches/mois). Les vues viendront du fil des Shorts et de TikTok, pas de la recherche. Les titres visent donc le thème (« quand tu as peur », « dormir en paix ») et la référence (« Psaume 23 », 8 700 recherches/mois).
- **Une vidéo longue par jour n'est pas tenable.** Même avec cette chaîne, il faut écrire, générer la voix, vérifier et publier. Rythme réaliste : **un Short par jour, une vidéo longue par semaine**.
- **Le CTA promet « un verset par jour ».** Ne le dis que si tu tiens le rythme. Sinon, dis « chaque semaine ».
- **Traduction : Louis Segond 1910 uniquement** (domaine public). La Segond 21, la Bible du Semeur et la NBS sont protégées : ne les cite pas en entier sans autorisation.

## Fabriquer un épisode

1. Copier `episodes/psaume-23-4/` sous un nouveau nom, réécrire `episode.json` (verset, textes, décors, cartes).
2. Construire les pages et le script ElevenLabs :
   ```
   python3 verset/source/construire.py verset/episodes/<épisode>
   ```
3. Générer la voix bloc par bloc avec `script_elevenlabs.md` (réglages dans `GUIDE_SON.md`). Déposer les fichiers dans `episodes/<épisode>/voix/`, nommés comme les blocs (`01_accroche.mp3`, `s5_cta_tiktok.mp3`...).
4. Facultatif : déposer la musique Suno sous `episodes/<épisode>/musique.mp3`.
5. Relancer l'étape 2 (les durées suivent alors la voix, la bouche suit la voix), puis :
   ```
   node verset/render.js verset/episodes/<épisode>
   ```
   Sortie dans `episodes/<épisode>/rendu/` : 3 vidéos, la miniature YouTube et la couverture du Short.

Sans voix, la même commande produit une **maquette** : durées estimées sur le texte, bouche animée par syllabes, nappe musicale provisoire.

### Dans `episode.json`

- `[softly]`, `[short pause]`... : directions de jeu pour ElevenLabs v3. Elles ne s'affichent pas à l'écran.
- `{tsalmavet|tsalmavète}` : écrit à gauche à l'écran, prononcé à droite par la voix.
- `decor` : `feu`, `chapelle`, `sommet` ou `chambre`.
- `plan` :
  - `large` : plan d'ensemble ;
  - `serre` : plan rapproché ;
  - `alterne` : on change de plan toutes les 7 s environ, comme un podcast filmé à deux caméras ;
  - `fin` : écran de fin.
- `cartes` : une carte (citation ou mot hébreu) qui apparaît quand la voix prononce `declencheur`.

## Fichiers

- `source/construire.py` : épisode → pages HTML à filmer, script ElevenLabs, chapitres YouTube.
- `scene.js` : ce qui bouge à l'écran (sous-titres, cartes, CTA, caméra). Le personnage et les décors viennent de `animation/moteur.js`.
- `render.js` : filme les pages, insère l'intro, traite la voix façon podcast, mixe la musique sous la voix, normalise à -14 LUFS.
- `GUIDE_SON.md` : réglages ElevenLabs, chaîne « micro podcast », prompts Suno.
