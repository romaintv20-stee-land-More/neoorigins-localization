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
