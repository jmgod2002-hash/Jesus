# Kit de montage — Psaume 23:4 (pour MK Cut ou tout autre logiciel)

Une timeline par vidéo, chaque élément sur sa propre piste.
Tous les temps sont en secondes depuis le début de la vidéo finale.

| Dossier | Vidéo | Format | Durée |
|---|---|---|---|
| `long/` | YouTube longue | 1920×1080, 30 i/s | 3 min 45 |
| `short_youtube/` | Short YouTube | 1080×1920, 30 i/s | 42 s |
| `short_tiktok/` | TikTok | 1080×1920, 30 i/s | 42 s |

## Contenu de chaque dossier

| Fichier | Piste | Placement |
|---|---|---|
| `fond.mp4` | Vidéo : décor + personnage animé, **sans aucun texte** (l'intro logo est déjà dedans pour la vidéo longue) | à 0 s |
| `voix.m4a` | Voix ElevenLabs traitée façon micro podcast, −16 LUFS | à 0 s |
| `musique.m4a` | Musique, déjà baissée sous la voix | à 0 s |
| `intro.m4a` | Son de l'intro logo (vidéo longue seulement) | à 0 s |
| `sous_titres.srt` | Sous-titres, groupe par groupe | à importer tel quel |
| `timeline.json` | Toute la timeline : blocs, textes à l'écran, sous-titres mot à mot | — |

Les pistes audio font toutes la durée exacte de la vidéo : posées à 0 s, elles sont déjà synchronisées.
Voix + musique + intro donnent le même son que les vidéos finies de `../rendu/`, à 2 dB près (normalisation finale à −14 LUFS).

## `timeline.json`

- `blocs` : accroche, bienvenue, verset, contexte… avec début, fin, décor et plan. Sert de repères / marqueurs.
- `textes_a_l_ecran` : tout ce qui s'affiche par-dessus la vidéo.
  - `verset` : la carte du verset, avec l'heure d'apparition de chaque mot (`mots`) ;
  - `chapitre` : numéro et titre ;
  - `citation` (Jean 10:11, le passage du « il » au « tu ») et `mot` (le mot hébreu צַלְמָוֶת, tsalmavet) ;
  - `abonnement` : le bouton, avec l'heure du clic (`clic`) ;
  - `commentaire` : la bulle « Écris en commentaire » ;
  - `ecran_de_fin` (vidéo longue) ;
  - `accroche` et `reference` (Shorts).
- `sous_titres` : les mêmes groupes que le `.srt`, avec chaque mot daté. Pour surligner le mot prononcé en doré (#FFB46A), comme dans les vidéos finies.

## Charte, pour refaire les textes à l'identique

| Élément | Réglage |
|---|---|
| Couleurs | braise #C0522B · or #FFB46A · crème #FFF6E8 · fond des cartes #120A06 à 84 % |
| Titres et cartes | Fraunces 700 (`intro/fonts/fraunces-700.woff2`) |
| Sous-titres des Shorts | Inter Tight 900 en majuscules, contour noir (`verset/fonts/intertight-800-900.woff2`) |
| Textes courants | Inter 500 (`intro/fonts/inter-500.woff2`) |
| Zone sûre des Shorts | ne rien placer sous 1 450 px ni dans les 120 px de droite (interface TikTok et YouTube) |

## Demande à faire à la session Claude Code sur ton PC (avec MK Cut connecté)

> Récupère la branche `claude/fervent-bell-foqjsb` du dépôt. Dans MK Cut, crée trois projets à partir de `verset/episodes/psaume-23-4/montage/` (long, short_youtube, short_tiktok). Pour chacun :
> - pose `fond.mp4`, `voix.m4a`, `musique.m4a` (et `intro.m4a` pour long) à 0 s sur des pistes séparées ;
> - importe `sous_titres.srt` ;
> - ajoute un marqueur au début de chaque bloc de `timeline.json` ;
> - recrée les textes de `textes_a_l_ecran` aux temps indiqués, avec la charte de `LISEZMOI.md`.
