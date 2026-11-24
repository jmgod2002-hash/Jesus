# Tadaa — vidéo TikTok (20 s, 1080×1920)

Fichiers (avec voix) : `tadaa_tiktok_60fps.mp4` (à publier sur TikTok, flou de mouvement) et `tadaa_tiktok_120fps.mp4` (master 120 i/s).

## Script voix off — ElevenLabs (Eleven v4)

Texte à coller tel quel (tags en anglais entre crochets, pauses avec « … », MAJUSCULES pour insister) :

```
[excited, curious] Tu veux des articles de Chine ?

[playful] Trop compliqué ? Trop loin ?... [confident] On s'en occupe !

[warm, clear] C'est simple : tu choisis ton article... on l'achète en Chine... et tu le reçois à Madagascar !

[upbeat] Mode, tech, maison, beauté... et bien PLUS !

[triumphant] Tadaa ! [warm] De la Chine à Madagascar. [friendly] Écris-nous en message privé !
```

Si « Tadaa » est mal prononcé, écrire « Ta-daa ».

## Calage sur la vidéo (voix intégrée : `source/voix_elevenlabs.mp3`)

La voix est découpée en 9 blocs et chaque animation part sur le mot prononcé (vérifié par transcription du mixage final).

| Mot | Instant | Animation |
|---|---|---|
| « articles » / « Chine » | 0,6 s / 1,0 s | les mots apparaissent |
| « Trop compliqué » / « Trop loin » | 2,2 s / 3,0 s | les deux questions |
| « occupe » | 4,05 s | le tampon tombe, l'écran tremble |
| « Tu choisis » | 6,0 s | étape 1 |
| « on l'achète en Chine » | 7,3 s | étape 2 + colis en Chine |
| « Madagascar » | 9,7 s | le colis atterrit |
| « Mode / tech / maison / beauté » | 10,7 / 11,45 / 11,9 / 12,5 s | t-shirt et sac / téléphone et casque / casserole / rouge à lèvres |
| « et bien plus » | 12,9 s | bulle |
| « Ta-da » | 14,8 s | les lettres rebondissent + notes « ta-daa » |
| « De la Chine à Madagascar » | 15,7 s | slogan |
| « Écris-nous… » | 17,55 s | bouton |

Mixage : bruitages baissés automatiquement sous la voix, volume final -14 LUFS.

## Légende TikTok
Tes articles de Chine, reçus à Madagascar 📦 Tu choisis, on s'occupe du reste. Écris-nous en privé !

#Madagascar #Tana #Antananarivo #ImportChine #ShoppingMadagascar #Tadaa #pourtoi

## Refaire la vidéo
`node source/rendu.js` (planche de contrôle : `node source/rendu.js --planche`). Textes et timings : `source/index.html`.
