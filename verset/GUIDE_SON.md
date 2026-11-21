# Guide son : voix ElevenLabs, rendu « micro podcast », musique Suno

## 1. La voix dans ElevenLabs

**Modèle** : Eleven v3, le modèle qui comprend les balises entre crochets (`[softly]`, `[short pause]`...).
Si ton compte propose un modèle plus récent, fais un test sur un bloc : si les balises sont lues à voix haute au lieu d'être jouées, reste sur v3.

**Choix de la voix** : une seule voix pour toute la série, c'est elle qui devient « le présentateur ».
- Soit dans la Voice Library : filtre Français, homme, catégorie *Narration* ou *Conversational*, et écoute-la sur le bloc `03_verset`.
- Soit avec Voice Design, en collant cette description :

> Homme français, 35 à 40 ans, voix grave, chaude et posée, diction claire, accent neutre. Enregistré dans un studio de podcast avec un micro dynamique placé très près de la bouche : beaucoup de chaleur dans le bas, aucune réverbération, aucun bruit de fond. Ton intime et rassurant, comme une confidence le soir, jamais théâtral.

**Réglages**
- Stabilité : *Natural*. Passe à *Robust* si la voix change de caractère d'un bloc à l'autre.
- Gardez la même voix et les mêmes réglages pour tous les blocs d'un épisode.
- Sortie : WAV 48 kHz si ton abonnement le permet, sinon MP3 44,1 kHz 192 kbps.

**Méthode**
- Un bloc = une génération. Colle le texte de `script_elevenlabs.md` tel quel, balises comprises.
- Écoute chaque bloc. S'il y a une erreur de ton ou de prononciation, régénère ce bloc seulement.
- Nomme le fichier comme le bloc (`05_sens.mp3`) et dépose-le dans `voix/`.
- Balises utilisées : `[softly]`, `[warmly]`, `[slowly]`, `[reverently]`, `[thoughtful]`, `[curious]`, `[short pause]`, `[long pause]`. Les majuscules (« TU es avec moi ») font appuyer le mot, et « … » donne une respiration.

## 2. Le rendu « micro podcast pro »

Une voix de synthèse sort propre mais « à plat ». `render.js` lui applique automatiquement la chaîne d'un studio de podcast :

| Étape | Réglage | Effet |
|---|---|---|
| Passe-haut | 75 Hz | Retire les grondements inutiles |
| Chaleur | +2 dB à 120 Hz | Effet de proximité d'un micro dynamique (type SM7B) |
| Anti-carton | −2,5 dB à 350 Hz | Enlève le son « boîte » |
| Présence | +2,5 dB à 3,5 kHz | La voix passe devant, même sur un téléphone |
| Dé-esseur | intensité 0,4 | Adoucit les « s » et les « ch » |
| Compresseur | 3:1, attaque 8 ms, relâche 120 ms | Voix régulière, intime |
| Limiteur | −1 dB | Aucun pic qui sature |
| Musique | −13 dB sous la voix + baisse automatique quand elle parle | La musique respire entre les phrases |
| Volume final | −14 LUFS, crête −1,5 dB | Norme YouTube et TikTok |

Tu n'as rien à faire : dépose les voix, relance le rendu.
Si tu montes ailleurs (CapCut, Premiere), reprends ces réglages dans le même ordre.

## 3. Musique de fond avec Suno

**Attention à la licence.** Avec l'offre gratuite de Suno, les morceaux ne peuvent pas être utilisés commercialement. Sur une chaîne monétisée, il faut l'offre payante (Pro ou Premier) **au moment de la création** du morceau : passer à l'offre payante plus tard ne couvre pas les morceaux déjà faits.

Dans Suno, en mode *Custom* : coche *Instrumental*, colle le style, colle les styles exclus. Génère 2 ou 3 versions et garde la plus calme.
Dépose-la sous `episodes/<épisode>/musique.mp3`. Elle est bouclée et baissée sous la voix automatiquement.

### Vidéo longue (fond de 3 à 4 min, en boucle)

**Style (version courte, moins de 200 caractères)**
```
ambient worship, soft felt piano, warm analog pads, gentle cello, 68 BPM, D major, intimate night mood, hopeful, minimal, no drums, spacious reverb, loopable
```

**Style (version détaillée, Suno v4.5 et plus)**
```
Instrumental ambient worship bed for a calm Christian podcast at night. Soft felt piano playing sparse broken chords in D major, warm analog pads, a gentle solo cello answering the piano, very slow tempo around 68 BPM. Intimate, hopeful, peaceful, like a candle in a dark room. No drums, no percussion, no vocals. Wide, soft reverb, low-mid warmth, nothing sharp in the highs so the spoken voice stays clear. Even dynamics from start to end, seamless loop.
```

**Styles exclus**
```
vocals, choir, drums, percussion, trap, EDM, rock, guitar solo, bright synth lead
```

### Short et TikTok (60 s, plus d'émotion)

**Style**
```
cinematic worship instrumental, intimate felt piano intro, slow build with warm strings and soft pads, emotional, hopeful, 72 BPM, D major, no drums, gentle swell at 0:35, soft ending
```

**Styles exclus** : les mêmes que ci-dessus.

Sur TikTok, publie avec ce son comme « son original ». Si le compte cible un son tendance, mets-le très bas (−25 dB) sous la voix : la voix porte le message.
