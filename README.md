# NeoOrigins Localization

Mod client NeoForge fournissant des **traductions complémentaires en priorité basse** pour NeoOrigins et des add-ons compatibles. Une traduction officielle amont garde toujours la priorité ; notre pack ne remplit que les clés absentes.

## Builds Minecraft

| Cible | Version | Java | Langues | Contenu empaqueté |
|---|---|---:|---:|---|
| Minecraft 1.21.1 | `0.8.0-beta+1.21.1` | 21 | 10 | NeoOrigins + Medieval Origins Revival + ibarn's quartet origins addon + Origins Fantasy for NeoOrigins + Origins: Backgrounds for NeoOrigins |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.8.0-beta+26.1` | 25 | 10 | NeoOrigins uniquement |
| Minecraft 26.2 | `0.8.0-beta+26.2` | 25 | 10 | NeoOrigins uniquement + delta 26.2 |

Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. Les bases Minecraft 26.1.2 et 26.2 ont déjà été validées en jeu avec NeoOrigins Localization ; les cinq langues ajoutées en 0.7.0 sur les branches 26.x doivent encore recevoir un contrôle visuel en jeu.

## Langues

La **0.8.0 Beta** prend en charge : Français (`fr_fr`), Allemand (`de_de`), Espagnol (`es_es`), Portugais brésilien (`pt_br`), Néerlandais (`nl_nl`), Italien (`it_it`), Polonais (`pl_pl`), Russe (`ru_ru`), Turc (`tr_tr`) et Chinois simplifié (`zh_cn`).

Les dix langues sont disponibles sur les trois builds pour NeoOrigins. Les traductions d'add-ons sont empaquetées uniquement sur 1.21.1 lorsqu'une version compatible de l'add-on est réellement disponible.

## Projets pris en charge

### NeoOrigins

NeoOrigins 2.2.25 est requis. Pour les langues déjà traduites officiellement par NeoOrigins, le fallback ne conserve que les clés absentes en amont. Le néerlandais est fourni intégralement par NeoOrigins Localization. Sur 26.2, l'italien, le polonais, le russe et le chinois simplifié disposent chacun de 2 172 clés officielles ; notre delta couvre uniquement les 120 clés manquantes. Le turc n'a pas de traduction officielle 26.2 : son fallback complet couvre les 2 292 clés grâce aux 14 entrées supplémentaires du delta 26.2.

### Medieval Origins Revival — Minecraft 1.21.1

Les **401 clés anglaises** sont couvertes dans les dix langues. L'import via `config/originpacks/` et l'affichage traduit d'un Origin ont déjà été validés en jeu sur 1.21.1.

### ibarn's quartet origins addon — Minecraft 1.21.1

Les **69 clés anglaises** sont couvertes dans les dix langues. L'add-on NeoForge 1.7.1 s'installe dans `mods/`. La localisation des quatre Origins a déjà été validée en jeu sur 1.21.1 avec la génération précédente.

### Origins Fantasy for NeoOrigins — Minecraft 1.21.1

Avec l'autorisation explicite de **DraconicArcher**, NeoOrigins Localization fournit les traductions des **240 clés anglaises** de la version 1.1.3 dans les dix langues. Les dix fichiers sont contrôlés contre le JAR CurseForge de référence : 240/240 clés couvertes, aucune clé manquante, aucun overlap avec une traduction officielle et aucun placeholder invalide.

Cette intégration n'embarque ni code, ni textures, ni modèles, ni données de gameplay d'Origins Fantasy. Le mod original reste nécessaire.

### Origins: Backgrounds for NeoOrigins — Minecraft 1.21.1

La 0.8.0 Beta ajoute les traductions de **Origins: Backgrounds for NeoOrigins 1.0.2**, également avec l'autorisation de **DraconicArcher**. Le JAR de référence contient **65 clés anglaises** et ne fournit aucune traduction officielle pour les dix langues ciblées : NeoOrigins Localization fournit donc 65/65 clés dans chacune des dix langues.

L'audit compare directement nos fallbacks au JAR CurseForge épinglé, contrôle les clés manquantes, les éventuels overlaps futurs et les placeholders. Seuls les fichiers de localisation traduits sont redistribués ; le mod original reste requis.

## Fonctionnement

Le resource pack intégré est placé en priorité basse :

1. les traductions officielles du mod/add-on sont prioritaires ;
2. les resource packs normaux peuvent les modifier ;
3. NeoOrigins Localization sert de fallback pour les clés restantes.

Aucune traduction n'est générée à l'exécution dans Minecraft.

## Audits et maintenance

Le CI vérifie les JSON, les clés manquantes, les overlaps avec les traductions officielles, les placeholders et la compilation. Les scripts suivis incluent :

```bash
python scripts/validate.py
python scripts/audit_neoorigins_upstream.py --fail-on-overlap --fail-on-missing
python scripts/audit_medievalorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_ibarnorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_fantasy_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
```

Lorsqu'un projet amont ajoute une traduction officielle, les clés devenues inutiles doivent être retirées de notre fallback.

## Traduction et retours

Les traductions et leur maintenance utilisent une assistance générative/automatisée importante, avec contrôles de structure et direction humaine. Elles ne sont pas présentées comme des traductions intégralement relues par des locuteurs natifs. Les corrections de formulation et de terminologie sont donc bienvenues.

Un nom d'Origin est traduit seulement lorsque le résultat reste naturel, identifiable et lisible dans l'interface ; sinon le nom anglais peut être conservé.

## Licences et attributions

Le code et la documentation originaux de NeoOrigins Localization sont sous licence MIT. Les éléments dérivés de projets tiers restent soumis aux licences ou autorisations amont applicables. Voir [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

Le fichier [`catalog.json`](catalog.json) est la source de vérité du contenu suivi ; [`CATALOG.md`](CATALOG.md) en est la vue lisible.
