# Plan de test 0.8.0 Beta

## Matrice de validation

| Cible | Java | Référence NeoOrigins 2.2.26 | Contenu du build | État automatisé |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | `860ecdb24e723983e93004ea8ceb5de90ccf0d70` | NeoOrigins + tous les add-ons 1.21.1 pris en charge | CI, audits et build validés |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | 25 | `3c1c7365507679c836d3c14af5d4dd0654652e87` | NeoOrigins uniquement + delta 26.1 | CI, audit et build validés |
| Minecraft 26.2 | 25 | `65864716a5a796fa1c51ec3e8a6d9640abebb4ca` | NeoOrigins uniquement + delta 26.2 | CI, audit et build validés |

La couverture garantie de cette version est basée sur NeoOrigins **2.2.26**. Le mod n'est pas verrouillé par une dépendance dure sur cette version ; une future version peut charger, mais devra être réauditée pour garantir une couverture complète.

## Langues

Les trois builds doivent proposer NeoOrigins dans les onze locales suivantes :

`fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn`, `cs_cz`.

Pour chaque langue contrôlée en jeu, vérifier au minimum :

- l'écran de sélection d'Origin et les nouveaux layouts du sélecteur ;
- un nom d'Origin ;
- une description longue ;
- un pouvoir avec texte long ;
- Step Assist et son interrupteur ;
- les textes Caveborn modifiés en 2.2.26 ;
- les écrans de configuration/HUD lorsqu'ils existent sur la cible.

La validation automatisée garantit la structure, les clés, les placeholders et la compilation ; elle ne remplace pas la vérification visuelle de la qualité des formulations et de la largeur des textes.

## Suédois — NeoOrigins et add-ons

- sélectionner **Svenska (`sv_se`)** dans Minecraft 1.21.1 ;
- vérifier l'écran de sélection des Origins, les descriptions longues, les noms de pouvoirs et les messages de HUD ;
- contrôler au moins une Origin de NeoOrigins et une Origin de chacun des add-ons installés ;
- signaler en priorité les intitulés trop longs, les termes restés en anglais qui ne sont pas des noms propres et les formulations peu naturelles.

Couverture automatisée : **2 296/2 296** clés NeoOrigins en 1.21.1, **2 307/2 307** en 26.1.x et 26.2, plus **1 253** entrées physiques d'add-ons en 1.21.1. Le JAR 1.21.1 doit contenir exactement **27 fichiers `sv_se.json`** ; chaque JAR 26.x doit en contenir **17** et ne contenir aucun namespace d'add-on 1.21.1.

## Tchèque — NeoOrigins

### 1.21.1

Les namespaces `neoorigins_cs_01` à `neoorigins_cs_19` sont complétés par `neoorigins_226/lang/cs_cz.json`. Ensemble, ils couvrent **2 296/2 296 clés** de NeoOrigins 2.2.26.

### 26.1.x

Le build 26.1.x reprend les namespaces communs et `neoorigins_226`, puis ajoute `neoorigins_26_1/lang/cs_cz.json` pour les réglages propres à cette ligne. La couverture effective est de **2 307/2 307 clés**.

### 26.2

Le build 26.2 reprend les namespaces communs et `neoorigins_226`, puis ajoute `neoorigins_26_2/lang/cs_cz.json`. La couverture effective est de **2 307/2 307 clés**.

Trois anciennes clés `reward.neoorigins.loot_pool*` présentes dans la base commune n'existent plus dans les branches 26.x ; leur présence est inoffensive, elles sont signalées comme obsolètes par l'audit et ne doivent pas être considérées comme des clés manquantes.

Contrôle visuel tchèque encore recommandé : écran de sélection, descriptions longues, configuration client, affichage HUD et textes des add-ons 1.21.1.

## Add-ons Minecraft 1.21.1

Tous les projets ci-dessous doivent être absents des builds 26.x et audités uniquement sur 1.21.1.

| Projet | Version / référence | Couverture par langue |
|---|---|---:|
| Medieval Origins Revival | `1.21.1-fabric` | 401/401 |
| ibarn's quartet origins addon | 1.7.1 | 69/69 |
| Origins Fantasy for NeoOrigins | 1.1.3 | 240/240 |
| Origins: Backgrounds for NeoOrigins | 1.0.2 | 65/65 |
| Origins: More Backgrounds for NeoOrigins | 1.0.2 | 39 propres + 5 partagées = 44/44 |
| Origins: Backgrounds ISS for NeoOrigins | 1.0.1 | 77 propres + 2 partagées = 79/79 |
| Origins Furries for NeoOrigins | 1.0.0 | 117/117 |
| Origins: Classes Extended for NeoOrigins | 1.0.1 | 124/124 |
| Origins: Classes ISS for NeoOrigins | 1.0.1 | 99/99 |
| Origin Architect | 3.0.1 / `f58a6261292942d4123c46ff221fbdade138a329` | 22/22 |

### Tests en jeu conseillés

- **Medieval Origins Revival** : importer via `config/originpacks/`, sélectionner au moins un Origin et contrôler nom, description et pouvoirs.
- **ibarn** : contrôler Ghaster, Sand Person, Soul Sorcerer et Wither Wraith.
- **Origins Fantasy** : contrôler plusieurs Origins et pouvoirs.
- **Backgrounds / More Backgrounds / Backgrounds ISS** : vérifier que le choix du Background et les pouvoirs associés sont traduits, y compris les clés partagées.
- **Furries** : tester au moins deux Origins animaux et leurs pouvoirs actifs/passifs.
- **Classes Extended** : contrôler au moins deux classes et plusieurs pouvoirs.
- **Classes ISS** : contrôler au moins deux classes, avec Iron's Spells 'n Spellbooks installé.
- **Origin Architect** : contrôler l'écran de sélection, le profil et les réglages HUD.

## Priorité du fallback

Installer NeoOrigins et NeoOrigins Localization. Dans une langue officiellement prise en charge par NeoOrigins :

1. vérifier qu'une clé officielle reste celle de NeoOrigins ;
2. vérifier qu'une clé absente en amont est bien fournie par notre fallback ;
3. vérifier qu'un resource pack utilisateur placé au-dessus peut encore remplacer le texte.

## Empaquetage attendu

### Minecraft 1.21.1

Le JAR doit inclure les namespaces suivants :

- `neoorigins/**` et les namespaces NeoOrigins de fallback ;
- `neoorigins_cs_*/**` ;
- `neoorigins_tr_*/**` ;
- `neoorigins_121_batch1/**` ;
- `neoorigins_226/**` ;
- `medievalorigins/**` et `medievalorigins_*/**` ;
- `ibarnorigins/**` ;
- `origins_fantasy/**` ;
- `origins_backgrounds/**` ;
- `origins_backgrounds_two/**` ;
- `origins_backgrounds_iss/**` ;
- `origins_furries/**` ;
- `origins_classes_ex/**` ;
- `origins_classes_iss/**` ;
- `originsmodernui/**`.

Les deltas `neoorigins_26_1/**` et `neoorigins_26_2/**` doivent être absents.

### Minecraft 26.1.x

Le JAR doit inclure :

- les ressources NeoOrigins communes ;
- `neoorigins_121_batch1/**` ;
- `neoorigins_tr_*/**` ;
- `neoorigins_cs_*/**` ;
- `neoorigins_226/**` ;
- `neoorigins_26_1/**`.

Il doit exclure :

- `neoorigins_26_2/**` ;
- tous les namespaces d'add-ons 1.21.1 listés ci-dessus.

### Minecraft 26.2

Le JAR doit inclure :

- les ressources NeoOrigins communes ;
- `neoorigins_tr_*/**` ;
- `neoorigins_cs_*/**` ;
- `neoorigins_226/**` ;
- `neoorigins_26_2/**`.

Il doit exclure :

- `neoorigins_121_batch1/**` ;
- `neoorigins_26_1/**` ;
- tous les namespaces d'add-ons 1.21.1.

L'inspection automatisée des JAR NeoOrigins 2.2.26 a confirmé **35 fichiers `cs_cz`** dans le JAR 1.21.1, **21** dans le JAR 26.1.x et **21** dans le JAR 26.2, sans fuite des add-ons dans les builds 26.x.

## Client uniquement

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour qu'un client bénéficie des traductions.

## CI

Chaque cible doit passer :

1. l'audit NeoOrigins de toutes les onze langues ;
2. `python3 scripts/validate.py` ;
3. la compilation avec la version Java correspondante ;
4. la génération et l'upload du JAR.

Sur Minecraft 1.21.1, la CI doit en plus réussir les audits dédiés de **tous les add-ons pris en charge** : Medieval Origins Revival, ibarn, Origins Fantasy, Backgrounds, More Backgrounds, Backgrounds ISS, Furries, Classes Extended, Classes ISS et Origin Architect, avec zéro overlap officiel, zéro clé nécessaire manquante et zéro erreur de placeholder.
