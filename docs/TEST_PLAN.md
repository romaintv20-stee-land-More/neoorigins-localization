# Plan de test V1

## Test de priorité

Installer :
- NeoOrigins
- NeoOrigins Localization

Passer Minecraft en français.

### Une clé déjà officielle

Vérifier le nom de l'Origin Avian.

Le `fr_fr.json` officiel actuel de NeoOrigins traduit ce nom en `Avien`, tandis que notre fallback garde `Avian`.
Si `Avien` reste affiché, la priorité de fallback fonctionne comme prévu.

### Une clé manquante dans l'ancien fichier FR

Vérifier une chaîne récente telle que l'activation/désactivation de la vision nocturne.
Notre pack doit fournir la traduction si le mod d'origine ne la possède pas.

## Test sans NeoOrigins

Lancer le client avec uniquement NeoOrigins Localization.
Le jeu doit démarrer normalement ; le mod doit simplement n'avoir aucune traduction NeoOrigins à afficher.

## Test serveur

Le mod est client-only et utilise `IGNORE_ALL_VERSION`.
Un serveur ne doit pas avoir besoin de l'installer.
