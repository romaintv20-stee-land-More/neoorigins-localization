# Plan de test 0.7.0 Beta

## Matrice de validation

| Cible | Java | NeoOrigins | Contenu du build | État |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | 2.2.25 | NeoOrigins + Medieval Origins Revival + ibarn + Origins Fantasy | Build/CI à valider, puis test final en jeu |
| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement, 10 langues en 0.7.0 | Base validée en jeu sur 26.1.2 ; nouvelles langues à contrôler visuellement |
| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2, 10 langues en 0.7.0 | Base validée en jeu ; nouvelles langues à contrôler visuellement |

## Priorité du fallback

Installer NeoOrigins et NeoOrigins Localization. Vérifier dans une langue officiellement prise en charge par NeoOrigins qu'une clé officielle reste inchangée, puis qu'une clé absente en amont est bien fournie par notre fallback.

## Langues 1.21.1

Le build 0.7.0 doit proposer les ressources pour `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Pour chaque langue testée, contrôler au minimum l'écran de sélection, un nom d'Origin et une description longue afin de repérer les problèmes de coupure ou de formulation.

## Langues 26.1.x

Le build `0.7.0-beta+26.1` doit proposer les mêmes dix langues NeoOrigins que la 1.21.1 : `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Les cinq nouvelles langues sont auditées contre NeoOrigins `v2.2.25`. Vérifier en jeu au minimum l'écran de sélection, un nom d'Origin et une description longue dans plusieurs de ces langues. Les add-ons 1.21.1 doivent rester absents du JAR 26.1.x.

## Medieval Origins Revival — 1.21.1

Installer/importer Medieval Origins Revival via la méthode prise en charge par NeoOrigins (`config/originpacks/`). Vérifier qu'un Origin importé affiche correctement son nom et sa description traduits. Cette intégration a déjà été validée en jeu sur Minecraft 1.21.1.

## ibarn's quartet origins addon — 1.21.1

Installer la version NeoForge 1.7.1 dans `mods/`. Vérifier Ghaster, Sand Person, Soul Sorcerer et Wither Wraith. La localisation des quatre Origins a déjà été validée en jeu sur Minecraft 1.21.1 avec la génération précédente.

## Origins Fantasy for NeoOrigins — 1.21.1

Installer Origins Fantasy 1.1.3 avec NeoOrigins et NeoOrigins Localization. Vérifier au moins plusieurs Origins, leurs noms, descriptions et pouvoirs dans plusieurs des dix langues. L'audit automatisé doit d'abord confirmer 240/240 clés, zéro overlap, zéro clé manquante et zéro erreur de placeholder. La validation en jeu spécifique à cette nouvelle intégration reste distincte de l'audit structurel.

## Langues Minecraft 26.2

Le build `0.7.0-beta+26.2` doit proposer `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Vérifier que le delta `neoorigins_26_2` est chargé sur 26.2 et absent des builds plus anciens. Pour `it_it`, `pl_pl`, `ru_ru` et `zh_cn`, les traductions officielles 26.2 restent prioritaires et notre fallback ne doit fournir que les 120 clés absentes. Pour `tr_tr`, vérifier que les namespaces `neoorigins_tr_*` et le delta de 14 clés couvrent ensemble les 2 292 clés. La base 26.2 a déjà été validée en jeu ; faire un contrôle visuel des nouvelles langues de la 0.7.0.

## Absence des add-ons dans les builds 26.x

Les JAR 26.1.x et 26.2 ne doivent contenir aucun fichier sous :

- `assets/medievalorigins/**` et `assets/medievalorigins_*/**` ;
- `assets/ibarnorigins/**` ;
- `assets/origins_fantasy/**` ;

Les JAR 26.x doivent toujours exclure les add-ons ci-dessus. Pour les ressources NeoOrigins spécifiques : le JAR 26.1.x inclut `neoorigins_121_batch1/**` et `neoorigins_tr_*/**` mais exclut `neoorigins_26_2/**` ; le JAR 26.2 exclut `neoorigins_121_batch1/**`, inclut `neoorigins_tr_*/**` pour le turc et inclut `neoorigins_26_2/**` pour son delta dédié.

## Client uniquement

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour qu'un client bénéficie des traductions.

## CI

Chaque cible doit passer la validation JSON, l'audit NeoOrigins, la compilation avec sa version Java et la génération du JAR. Sur 1.21.1, les audits Medieval Origins Revival, ibarn et Origins Fantasy doivent aussi réussir sans overlap, clé manquante ni erreur de placeholder.
