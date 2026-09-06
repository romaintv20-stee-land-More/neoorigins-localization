# Plan de test 0.6.0 Beta

## Matrice de validation

| Cible | Java | NeoOrigins | Contenu du build | État |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | 2.2.25 | NeoOrigins + Medieval Origins Revival + ibarn | Validé en jeu |
| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement | Validé en jeu sur 26.1.2 |
| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2 | Validé en jeu |

## Test de priorité

Installer :
- NeoOrigins
- NeoOrigins Localization

Passer Minecraft en français.

### Une clé déjà officielle

Vérifier une chaîne déjà traduite officiellement par NeoOrigins.

La traduction officielle doit rester affichée. Notre resource pack intégré est volontairement en priorité basse et ne doit pas remplacer une traduction officielle existante.

### Une clé absente en amont

Vérifier une chaîne récente qui n'existe pas dans la langue officielle suivie.

NeoOrigins Localization doit fournir la traduction de fallback.

## Test néerlandais

Passer Minecraft en néerlandais et ouvrir l'écran de sélection des Origins.

Vérifier notamment :
- le titre de sélection ;
- la recherche ;
- le texte d'aide ;
- les boutons retour, confirmer et aléatoire ;
- les noms/descriptions d'Origins lorsqu'ils doivent être traduits.

Ce test a été validé en jeu sur Minecraft 26.1.2 et 26.2.

## Test Minecraft 26.2

La branche 26.2 possède des clés supplémentaires par rapport aux cibles plus anciennes.

Vérifier :
- que le delta `neoorigins_26_2` est bien chargé ;
- que les nouvelles clés sont traduites ;
- qu'aucune clé du delta 26.2 n'est empaquetée dans les builds 1.21.1 ou 26.1.x.

## Test Medieval Origins Revival — 1.21.1

Installer/importer Medieval Origins Revival selon la méthode prise en charge par NeoOrigins (`config/originpacks/`).

Vérifier qu'un Origin importé affiche correctement son nom et sa description traduits.

La localisation d'un Origin importé a été validée en jeu sur Minecraft 1.21.1.

## Test ibarn's quartet origins addon — 1.21.1

Installer la version NeoForge 1.7.1 dans `mods/`.

Vérifier les quatre Origins :
- Ghaster ;
- Sand Person ;
- Soul Sorcerer ;
- Wither Wraith.

La localisation et le chargement des quatre Origins ont été validés en jeu sur Minecraft 1.21.1. Les éventuels problèmes de gameplay propres à l'add-on ou à son interaction avec NeoOrigins ne doivent pas être confondus avec un problème de traduction.

## Test sans les add-ons sur 26.x

Les builds Minecraft 26.1.x et 26.2 ne doivent pas contenir :
- `assets/medievalorigins/**` ;
- `assets/ibarnorigins/**`.

Ces traductions restent dans le dépôt mais ne sont empaquetées que dans le build 1.21.1 tant qu'une compatibilité NeoForge 26.x n'est pas validée.

## Test serveur

Le mod est client-only.

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour permettre à un client de bénéficier des traductions.

## CI

Chaque cible doit :
- passer la validation JSON ;
- passer l'audit NeoOrigins sans overlap de fallback ;
- passer l'audit de couverture des clés manquantes ;
- compiler avec la version Java correspondante ;
- générer son JAR dédié.

Les audits Medieval Origins Revival et ibarn ne s'exécutent que pour la cible 1.21.1.
