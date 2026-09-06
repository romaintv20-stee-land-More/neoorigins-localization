# Plan de test 0.7.0 Beta

## Matrice de validation

| Cible | Java | NeoOrigins | Contenu du build | État |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | 2.2.25 | NeoOrigins + Medieval Origins Revival + ibarn + Origins Fantasy | Build/CI validé ; test final en jeu de la nouvelle intégration Origins Fantasy à faire |
| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement, 10 langues | Build/CI à valider ; test visuel final de l'extension 0.7.0 à faire sur 26.1.2 |
| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2, 5 langues | Validé en jeu en 0.6.0 ; adaptation 0.7.0 à faire séparément |

## Priorité du fallback

Installer NeoOrigins et NeoOrigins Localization. Vérifier dans une langue officiellement prise en charge par NeoOrigins qu'une clé officielle reste inchangée, puis qu'une clé absente en amont est bien fournie par notre fallback.

## Langues 1.21.1 et 26.1.x

Les builds 0.7.0 doivent proposer les ressources pour `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Pour chaque langue testée, contrôler au minimum l'écran de sélection, un nom d'Origin et une description longue afin de repérer les problèmes de coupure ou de formulation.

Les références NeoOrigins `1.21.1` et `v2.2.25` pointant vers le même commit amont, les fichiers du premier lot de cinq langues sont partagés entre 1.21.1 et 26.1.x. Le CI doit néanmoins auditer les dix langues séparément sur chaque cible.

## Medieval Origins Revival — 1.21.1

Installer/importer Medieval Origins Revival via la méthode prise en charge par NeoOrigins (`config/originpacks/`). Vérifier qu'un Origin importé affiche correctement son nom et sa description traduits. Cette intégration a déjà été validée en jeu sur Minecraft 1.21.1.

## ibarn's quartet origins addon — 1.21.1

Installer la version NeoForge 1.7.1 dans `mods/`. Vérifier Ghaster, Sand Person, Soul Sorcerer et Wither Wraith. La localisation des quatre Origins a déjà été validée en jeu sur Minecraft 1.21.1 avec la génération précédente.

## Origins Fantasy for NeoOrigins — 1.21.1

Installer Origins Fantasy 1.1.3 avec NeoOrigins et NeoOrigins Localization. Vérifier au moins plusieurs Origins, leurs noms, descriptions et pouvoirs dans plusieurs des dix langues. L'audit automatisé doit confirmer 240/240 clés, zéro overlap, zéro clé manquante et zéro erreur de placeholder. La validation en jeu spécifique à cette nouvelle intégration reste distincte de l'audit structurel.

## Minecraft 26.1.x

Le JAR `0.7.0-beta+26.1` doit inclure les namespaces d'expansion du premier lot (`assets/neoorigins_121_batch1/**` et `assets/neoorigins_tr_*/**`) afin de fournir les cinq nouvelles langues, tout en excluant tous les add-ons 1.21.1. Vérifier le chargement sur Minecraft 26.1.2 avec Java 25.

## Minecraft 26.2

Vérifier que le delta `neoorigins_26_2` est chargé sur 26.2. Tant que la cible reste en 0.6.0, elle doit continuer à exclure les namespaces du premier lot 0.7.0 (`assets/neoorigins_121_batch1/**` et `assets/neoorigins_tr_*/**`). Son passage aux dix langues fera l'objet de l'étape suivante.

## Absence des add-ons dans les builds 26.x

Les JAR 26.1.x et 26.2 ne doivent contenir aucun fichier sous :

- `assets/medievalorigins/**` et `assets/medievalorigins_*/**` ;
- `assets/ibarnorigins/**` ;
- `assets/origins_fantasy/**`.

## Client uniquement

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour qu'un client bénéficie des traductions.

## CI

Chaque cible doit passer la validation JSON, l'audit NeoOrigins, la compilation avec sa version Java et la génération du JAR. Sur 1.21.1, les audits Medieval Origins Revival, ibarn et Origins Fantasy doivent aussi réussir sans overlap, clé manquante ni erreur de placeholder. Sur 26.1.x, l'audit NeoOrigins doit couvrir les dix langues de 0.7.0.
