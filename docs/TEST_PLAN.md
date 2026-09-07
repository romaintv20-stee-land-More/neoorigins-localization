# Plan de test 0.8.0 Beta

## Matrice de validation

| Cible | Java | Référence NeoOrigins 2.2.25 | Contenu du build | État automatisé |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | `2b409f3f9c27250665895cf3d0faa3f7adf9c4ac` | NeoOrigins + tous les add-ons 1.21.1 pris en charge | CI, audits et build validés |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | 25 | `v2.2.25` | NeoOrigins uniquement | CI, audit et build validés |
| Minecraft 26.2 | 25 | `86038d2d1b429255897c2bdac9097ecc50e07215` | NeoOrigins uniquement + delta 26.2 | CI, audit et build validés |

La couverture garantie de cette version est basée sur NeoOrigins **2.2.25**. Le mod n'est pas verrouillé par une dépendance dure sur cette version, mais les clés ajoutées en NeoOrigins 2.2.26 sont suivies séparément.

## Langues

Les trois builds doivent proposer NeoOrigins dans les onze locales suivantes :

`fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn`, `cs_cz`.

Pour chaque langue contrôlée en jeu, vérifier au minimum :

- l'écran de sélection d'Origin ;
- un nom d'Origin ;
- une description longue ;
- un pouvoir avec texte long ;
- les écrans de configuration/HUD lorsqu'ils existent sur la cible.

La validation automatisée garantit la structure, les clés, les placeholders et la compilation ; elle ne remplace pas la vérification visuelle de la qualité des formulations et de la largeur des textes.

## Tchèque — NeoOrigins

### 1.21.1 et 26.1.x

Le tchèque est réparti dans les namespaces `neoorigins_cs_01` à `neoorigins_cs_19`. Ensemble, ils couvrent **2 281/2 281 clés** de NeoOrigins 2.2.25.

### 26.2

Le build 26.2 reprend les 19 namespaces communs et ajoute `neoorigins_26_2/lang/cs_cz.json` avec **14 clés spécifiques à 26.2**, soit **2 292/2 292 clés** couvertes.

Trois anciennes clés `reward.neoorigins.loot_pool*` présentes dans la base commune n'existent plus dans NeoOrigins 26.2 ; leur présence est inoffensive et elles ne doivent pas être considérées comme des clés manquantes.

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

Le delta `neoorigins_26_2/**` doit être absent.

### Minecraft 26.1.x

Le JAR doit inclure :

- les ressources NeoOrigins communes ;
- `neoorigins_121_batch1/**` ;
- `neoorigins_tr_*/**` ;
- `neoorigins_cs_*/**`.

Il doit exclure :

- `neoorigins_26_2/**` ;
- tous les namespaces d'add-ons 1.21.1 listés ci-dessus.

### Minecraft 26.2

Le JAR doit inclure :

- les ressources NeoOrigins communes ;
- `neoorigins_tr_*/**` ;
- `neoorigins_cs_*/**` ;
- `neoorigins_26_2/**`.

Il doit exclure :

- `neoorigins_121_batch1/**` ;
- tous les namespaces d'add-ons 1.21.1.

L'inspection automatisée de la branche 0.8.0 a confirmé **34 fichiers `cs_cz`** dans le JAR 1.21.1, **19** dans le JAR 26.1.x et **20** dans le JAR 26.2, sans fuite des add-ons dans les builds 26.x.

## Client uniquement

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour qu'un client bénéficie des traductions.

## CI

Chaque cible doit passer :

1. l'audit NeoOrigins de toutes les onze langues ;
2. `python3 scripts/validate.py` ;
3. la compilation avec la version Java correspondante ;
4. la génération et l'upload du JAR.

Sur Minecraft 1.21.1, la CI doit en plus réussir les audits dédiés de **tous les add-ons pris en charge** : Medieval Origins Revival, ibarn, Origins Fantasy, Backgrounds, More Backgrounds, Backgrounds ISS, Furries, Classes Extended, Classes ISS et Origin Architect, avec zéro overlap officiel, zéro clé nécessaire manquante et zéro erreur de placeholder.
