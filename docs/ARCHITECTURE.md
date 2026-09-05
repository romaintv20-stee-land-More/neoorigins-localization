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
