# NeoOrigins Localization

Mod client NeoForge fournissant des **traductions complémentaires en priorité basse** pour NeoOrigins et des add-ons compatibles. Une traduction officielle amont garde toujours la priorité ; notre pack ne remplit que les clés absentes.

## Builds Minecraft

| Cible | Version | Java | Langues | Contenu empaqueté |
|---|---|---:|---:|---|
| Minecraft 1.21.1 | `0.8.0-beta+1.21.1` | 21 | 13 | NeoOrigins + Medieval Origins Revival + ibarn's quartet origins addon + Origins Fantasy + Origins: Backgrounds + Origins: More Backgrounds + Origins: Backgrounds ISS + Origins Furries + Origins: Classes Extended + Origins: Classes ISS + Origin Architect |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.8.0-beta+26.1` | 25 | 13 | NeoOrigins uniquement + delta 26.1 |
| Minecraft 26.2 | `0.8.0-beta+26.2` | 25 | 13 | NeoOrigins uniquement + delta 26.2 |

Les builds 26.x n'embarquent aucune traduction des add-ons 1.21.1. La CI construit et audite séparément les trois cibles.

## Langues

La **0.8.0 Beta** prend en charge : Français (`fr_fr`), Allemand (`de_de`), Espagnol (`es_es`), Portugais brésilien (`pt_br`), Néerlandais (`nl_nl`), Italien (`it_it`), Polonais (`pl_pl`), Russe (`ru_ru`), Turc (`tr_tr`), Chinois simplifié (`zh_cn`), **Tchèque (`cs_cz`)**, **Hongrois (`hu_hu`)** et **Japonais (`ja_jp`)**.

Les treize langues sont disponibles sur les trois builds pour NeoOrigins. Les traductions d'add-ons sont empaquetées uniquement sur Minecraft 1.21.1 lorsqu'une version compatible de l'add-on est réellement disponible.

## Référence NeoOrigins

La couverture de la 0.8.0 est auditée contre **NeoOrigins 2.2.26** :

- 1.21.1 : commit `860ecdb24e723983e93004ea8ceb5de90ccf0d70` ;
- 26.1.x : commit `3c1c7365507679c836d3c14af5d4dd0654652e87` ;
- 26.2 : commit `65864716a5a796fa1c51ec3e8a6d9640abebb4ca`.

NeoOrigins Localization n'impose pas de dépendance dure sur la version 2.2.26 : le mod peut charger avec une version NeoOrigins plus récente, mais la **couverture complète garantie ici correspond à 2.2.26**.

La mise à jour 2.2.26 ajoute un delta commun `neoorigins_226` pour les nouvelles chaînes du sélecteur, Step Assist et Caveborn. La ligne 26.1.x possède en plus `neoorigins_26_1` pour ses raccourcis, compétences et réglages propres, tandis que 26.2 conserve `neoorigins_26_2`.

Pour le tchèque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le hongrois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Sur 26.x, trois anciennes clés de récompense restent dans les fichiers de fallback mais n'existent plus en amont ; elles sont signalées comme obsolètes par l'audit et restent sans effet.

## Projets pris en charge sur Minecraft 1.21.1

| Projet | Version/référence | Couverture CS / HU / JA | Couverture effective par langue |
|---|---|---:|---:|
| Medieval Origins Revival | branche `1.21.1-fabric` | 401/401 · 401/401 · 401/401 | 401/401 |
| ibarn's quartet origins addon | 1.7.1 | 69/69 · 69/69 · 69/69 | 69/69 |
| Origins Fantasy for NeoOrigins | 1.1.3 | 240/240 · 240/240 · 240/240 | 240/240 |
| Origins: Backgrounds for NeoOrigins | 1.0.2 | 65/65 · 65/65 · 65/65 | 65/65 |
| Origins: More Backgrounds for NeoOrigins | 1.0.2 | 44/44 · 44/44 · 44/44 | 39 propres + 5 partagées = 44/44 |
| Origins: Backgrounds ISS for NeoOrigins | 1.0.1 | 79/79 · 79/79 · 79/79 | 77 propres + 2 partagées = 79/79 |
| Origins Furries for NeoOrigins | 1.0.0 | 117/117 · 117/117 · 117/117 | 117/117 |
| Origins: Classes Extended for NeoOrigins | 1.0.1 | 124/124 · 124/124 · 124/124 | 124/124 |
| Origins: Classes ISS for NeoOrigins | 1.0.1 | 99/99 · 99/99 · 99/99 | 99/99 |
| Origin Architect | 3.0.1 | 22/22 · 22/22 · 22/22 | 22/22 |

Les intégrations DraconicArcher sont réalisées avec son autorisation explicite pour redistribuer les **chaînes de localisation traduites**. Aucun code, texture, modèle ou autre asset de gameplay de ces add-ons n'est redistribué ; les mods originaux restent requis.

Origins: Backgrounds ISS et Origins: Classes ISS nécessitent également **Iron's Spells 'n Spellbooks**. Origin Architect est suivi sur le commit source `f58a6261292942d4123c46ff221fbdade138a329`.

## Fonctionnement

Le resource pack intégré est placé en priorité basse :

1. les traductions officielles du mod/add-on sont prioritaires ;
2. les resource packs normaux peuvent les modifier ;
3. NeoOrigins Localization sert de fallback pour les clés restantes.

Aucune traduction n'est générée à l'exécution dans Minecraft.

## Audits et maintenance

La CI vérifie :

- la validité des JSON et l'absence de clés dupliquées ;
- les clés manquantes par rapport aux sources/JAR amont épinglés ;
- les overlaps avec les traductions officielles ;
- les placeholders `%s`, `%1$s`, `%d`, etc. ;
- l'empaquetage par cible ;
- la compilation Java/NeoForge des trois builds.

Les scripts suivis incluent :

```bash
python scripts/validate.py
python scripts/audit_neoorigins_upstream.py --fail-on-overlap --fail-on-missing
python scripts/audit_medievalorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_ibarnorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_fantasy_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_more_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_backgrounds_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_furries_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_classes_extended_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_classes_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origin_architect_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
```

Lorsqu'un projet amont ajoute une traduction officielle, les clés devenues inutiles doivent être retirées de notre fallback.

## Validation des JAR 0.8.0

L'inspection des JAR construits avec la référence NeoOrigins 2.2.26 a confirmé :

- **1.21.1** : 35 fichiers `cs_cz` et **33 fichiers `hu_hu`** empaquetés, couvrant NeoOrigins, Medieval Origins et tous les add-ons listés ;
- **26.1.x** : 21 fichiers `cs_cz` et **20 fichiers `hu_hu`**, uniquement les namespaces NeoOrigins communs + `neoorigins_226` + `neoorigins_26_1` ;
- **26.2** : 21 fichiers `cs_cz` et **20 fichiers `hu_hu`**, uniquement les namespaces NeoOrigins communs + `neoorigins_226` + `neoorigins_26_2` ;
- aucun namespace d'add-on 1.21.1 n'est présent dans les JAR 26.x ;
- les trois builds compilent avec succès et leur contenu de localisation a été ouvert et validé après construction.

La validation automatisée ne remplace pas un contrôle visuel en jeu pour la qualité de formulation ou les problèmes de largeur d'interface.

## Traduction et retours

Les traductions et leur maintenance utilisent une assistance générative/automatisée importante, avec contrôles de structure et direction humaine. Elles ne sont pas présentées comme des traductions intégralement relues par des locuteurs natifs. Les corrections de formulation et de terminologie sont bienvenues.

Un nom d'Origin est traduit seulement lorsque le résultat reste naturel, identifiable et lisible dans l'interface ; sinon le nom anglais peut être conservé.

## Licences et attributions

Le code et la documentation originaux de NeoOrigins Localization sont sous licence MIT. Les éléments dérivés de projets tiers restent soumis aux licences ou autorisations amont applicables. Voir [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

Le fichier [`catalog.json`](catalog.json) est la source de vérité du contenu suivi ; [`CATALOG.md`](CATALOG.md) en est la vue lisible.
