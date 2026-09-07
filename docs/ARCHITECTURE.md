# Architecture

## Objectif

Fournir des localisations manuellement vérifiées sans remplacer les traductions officielles déjà présentes.

## Resource pack de fallback

Les fichiers sont stockés sous :

`src/main/resources/resourcepacks/fallback_localizations/assets/<namespace>/lang/<locale>.json`

Le pack est enregistré via `AddPackFindersEvent` avec :

- `PackType.CLIENT_RESOURCES`
- `alwaysActive = true`
- `Pack.Position.BOTTOM`

Cette position est volontairement basse afin que les ressources officielles des mods restent prioritaires.

## Évolution multilingue

Ajouter une langue ne demande aucun changement de code Java. Exemple :

- `assets/neoorigins/lang/de_de.json`
- `assets/neoorigins/lang/es_es.json`
- `assets/un_addon/lang/fr_fr.json`

Le fichier `catalog.json` décrit les projets et langues réellement supportés.

### Namespaces fractionnés et deltas de version

Une locale volumineuse peut être répartie dans plusieurs namespaces de fallback lorsque cela facilite les ajouts et la maintenance. L'audit recompose alors ces fichiers avant de comparer la couverture aux clés anglaises amont.

La 0.8.0 utilise notamment :

- `neoorigins_tr_*` pour la localisation turque fractionnée ;
- `neoorigins_cs_*` pour la localisation tchèque fractionnée ;
- `neoorigins_121_batch1` pour des compléments communs aux cibles 1.21.1 / 26.1.x ;
- `neoorigins_226` pour les nouvelles chaînes communes à NeoOrigins 2.2.26 ;
- `neoorigins_26_1` pour les clés spécifiques à Minecraft 26.1.x ;
- `neoorigins_26_2` pour les clés spécifiques à Minecraft 26.2.

Les propriétés Gradle d'empaquetage déterminent quels namespaces sont inclus dans chaque JAR. Les add-ons compatibles uniquement avec Minecraft 1.21.1 sont explicitement exclus des builds 26.x. Les deltas 26.1 et 26.2 sont mutuellement exclus afin de ne jamais injecter des clés spécifiques à une autre cible.

La branche 0.8.0 audite NeoOrigins contre des références **2.2.26 épinglées** plutôt que contre des branches mouvantes :

- Minecraft 1.21.1 : `860ecdb24e723983e93004ea8ceb5de90ccf0d70` ;
- Minecraft 26.1.x : `3c1c7365507679c836d3c14af5d4dd0654652e87` ;
- Minecraft 26.2 : `65864716a5a796fa1c51ec3e8a6d9640abebb4ca`.

Cette référence fixe la couverture garantie ; elle ne constitue pas une dépendance dure empêchant le chargement avec une version NeoOrigins ultérieure.

## Politique de traduction

- aucune traduction automatique en jeu ;
- clés JSON inchangées ;
- placeholders `%s`, `%1$s`, `%d`, `%%`, etc. conservés ;
- terminologie Minecraft officielle privilégiée ;
- traduction officielle d'un mod prioritaire ;
- nos corrections d'une traduction existante doivent être proposées séparément à l'auteur plutôt que forcées.

### Noms d'Origins et de classes

La lisibilité de l'interface est prioritaire sur la volonté de tout traduire.

- traduire un nom lorsque la version localisée est naturelle, immédiatement identifiable et tient correctement dans l'interface ;
- privilégier une adaptation courte, de largeur visuelle proche de l'original ;
- conserver le nom anglais canonique lorsque la traduction devient nettement plus longue, artificielle ou risque de dépasser ;
- accepter volontairement un mélange de noms anglais et localisés si cela améliore la lisibilité et facilite les recherches sur les wikis, guides et communautés ;
- ne pas inventer un nouveau nom uniquement pour forcer une traduction.

Choix français de référence actuels :

- Human -> Humain
- Avian -> Avien
- Elytrian -> Élytrien
- Enderian -> Endérien
- Arachnid -> Arachnide
- Dwarf -> Nain
- Gorgon -> Gorgone
- Siren -> Sirène
- Vampire -> Vampire
- Skeleton -> Squelette si la largeur reste correcte dans l'interface
- Wraith -> Spectre si la largeur reste correcte dans l'interface
- Voidwalker -> Voidwalker
- Caveborn -> Caveborn
- Blazeling -> Blazeling
- Sculkborn -> Sculkborn
- Stoneguard -> Stoneguard
