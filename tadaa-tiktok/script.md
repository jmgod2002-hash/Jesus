# Tadaa — vidéo TikTok (20 s, 1080×1920)

Fichiers : `tadaa_tiktok_60fps.mp4` (à publier sur TikTok, flou de mouvement) et `tadaa_tiktok_120fps.mp4` (master 120 i/s).

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

## Calage sur la vidéo (début de chaque phrase)

| Début | Phrase | À l'écran |
|---|---|---|
| 0,0 s | Tu veux des articles de Chine ? | Accroche + mascotte |
| 3,0 s | Trop compliqué ? Trop loin ? | Les deux questions apparaissent puis sont barrées |
| 4,3 s | On s'en occupe ! | Le tampon tombe (4,35 s) |
| 6,8 s | C'est simple : tu choisis ton article… | Étape 1 (6,9 s) |
| 7,8 s | …on l'achète en Chine… | Étape 2 + colis en Chine (7,8 s) |
| 10,3 s | …et tu le reçois à Madagascar ! | Le colis atterrit, étape 3 (10,35 s) |
| 12,4 s | Mode, tech, maison, beauté… | Les 6 icônes tombent |
| 14,0 s | …et bien plus ! | Bulle « …et bien plus ! » |
| 16,1 s | Tadaa ! | Le nom rebondit + confettis |
| 16,8 s | De la Chine à Madagascar. | Slogan |
| 17,3 s | Écris-nous en message privé ! | Bouton |

## Légende TikTok
Tes articles de Chine, reçus à Madagascar 📦 Tu choisis, on s'occupe du reste. Écris-nous en privé !

#Madagascar #Tana #Antananarivo #ImportChine #ShoppingMadagascar #Tadaa #pourtoi

## Refaire la vidéo
`node source/rendu.js` (planche de contrôle : `node source/rendu.js --planche`). Textes et timings : `source/index.html`.
