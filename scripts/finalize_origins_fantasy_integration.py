#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
README = ROOT / "README.md"
TEST_PLAN = ROOT / "docs/TEST_PLAN.md"
GENERATOR = ROOT / "scripts/generate_catalog.py"
BUILD_WORKFLOW = ROOT / ".github/workflows/build.yml"

LANGS = {
    "fr_fr": "Français",
    "de_de": "Deutsch",
    "es_es": "Español",
    "pt_br": "Português (Brasil)",
    "nl_nl": "Nederlands",
    "it_it": "Italiano",
    "pl_pl": "Polski",
    "ru_ru": "Русский",
    "tr_tr": "Türkçe",
    "zh_cn": "简体中文",
}
NEW_121 = ("it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")

catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
build121 = catalog["project"]["builds"]["1.21.1"]
build121["version"] = "0.7.0-beta+1.21.1"
build121["in_game_tested"] = False
build121["included_projects"] = ["neoorigins", "medievalorigins", "ibarnorigins", "origins_fantasy"]

projects = {p["id"]: p for p in catalog["supported_projects"]}

# First five expansion locales are published for 1.21.1 only in 0.7.0.
neo = projects["neoorigins"]
for code in NEW_121:
    neo["languages"][code] = {
        "name": LANGS[code],
        "status": "supported",
        "review": "ai_assisted_human_directed_review_pending_native_feedback",
        "targets": ["1.21.1"],
        "note": "Couverture de fallback Minecraft 1.21.1 auditée contre NeoOrigins ; les traductions officielles amont gardent la priorité."
    }

medieval = projects["medievalorigins"]
for code in NEW_121:
    medieval["languages"][code] = {
        "name": LANGS[code],
        "status": "supported",
        "review": "ai_assisted_human_directed_review_pending_native_feedback",
        "targets": ["1.21.1"],
        "coverage_keys": 401,
        "source_keys": 401,
        "note": "Couverture complète des 401 clés anglaises pour Minecraft 1.21.1 ; retours de locuteurs natifs bienvenus."
    }

ibarn = projects["ibarnorigins"]
for code in NEW_121:
    ibarn["languages"][code] = {
        "name": LANGS[code],
        "status": "supported",
        "review": "ai_assisted_human_directed_review_pending_native_feedback",
        "targets": ["1.21.1"],
        "coverage_keys": 69,
        "source_keys": 69,
        "note": "Couverture complète des 69 clés anglaises pour Minecraft 1.21.1 ; retours de locuteurs natifs bienvenus."
    }

origins_fantasy = {
    "id": "origins_fantasy",
    "name": "Origins Fantasy for NeoOrigins",
    "author": "DraconicArcher",
    "namespace": "origins_fantasy",
    "curseforge": "https://www.curseforge.com/minecraft/mc-mods/origins-fantsy-neoorigins",
    "license": {
        "localization_redistribution": "explicit_author_permission",
        "permission_date": "2026-09-06",
        "attribution_required": True
    },
    "compatibility": {
        "method": "NeoForge mod in mods/",
        "version": "1.1.3 / Minecraft 1.21.1",
        "minecraft": ["1.21.1"],
        "in_game_validation": "pending",
        "note": "Les fichiers de localisation sont audités contre le JAR CurseForge 8816068. Le support de traduction n'implique pas une validation complète du gameplay. Le projet n'est pas empaqueté dans les builds 26.x."
    },
    "languages": {}
}
for code, name in LANGS.items():
    origins_fantasy["languages"][code] = {
        "name": name,
        "status": "supported",
        "review": "ai_assisted_human_directed_review_pending_native_feedback",
        "targets": ["1.21.1"],
        "file": f"src/main/resources/resourcepacks/fallback_localizations/assets/origins_fantasy/lang/{code}.json",
        "coverage_keys": 240,
        "source_keys": 240,
        "note": "240/240 clés couvertes ; audit sans overlap, clé manquante ni erreur de placeholder."
    }

if "origins_fantasy" in projects:
    idx = next(i for i, p in enumerate(catalog["supported_projects"]) if p["id"] == "origins_fantasy")
    catalog["supported_projects"][idx] = origins_fantasy
else:
    catalog["supported_projects"].append(origins_fantasy)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

README.write_text(r'''# NeoOrigins Localization

Mod client NeoForge fournissant des **traductions complémentaires en priorité basse** pour NeoOrigins et des add-ons compatibles. Une traduction officielle amont garde toujours la priorité ; notre pack ne remplit que les clés absentes.

## Builds Minecraft

| Cible | Version | Java | Langues | Contenu empaqueté |
|---|---|---:|---:|---|
| Minecraft 1.21.1 | `0.7.0-beta+1.21.1` | 21 | 10 | NeoOrigins + Medieval Origins Revival + ibarn's quartet origins addon + Origins Fantasy for NeoOrigins |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.6.0-beta+26.1` | 25 | 5 | NeoOrigins uniquement |
| Minecraft 26.2 | `0.6.0-beta+26.2` | 25 | 5 | NeoOrigins uniquement + delta 26.2 |

Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. Minecraft 26.1.2 et 26.2 ont déjà été validés en jeu avec NeoOrigins Localization ; l'intégration 0.7.0 de Minecraft 1.21.1 doit encore recevoir sa validation finale en jeu après build.

## Langues

Le build **1.21.1 / 0.7.0 Beta** prend en charge : Français (`fr_fr`), Allemand (`de_de`), Espagnol (`es_es`), Portugais brésilien (`pt_br`), Néerlandais (`nl_nl`), Italien (`it_it`), Polonais (`pl_pl`), Russe (`ru_ru`), Turc (`tr_tr`) et Chinois simplifié (`zh_cn`).

Les cinq nouvelles langues de 0.7.0 sont actuellement limitées au build 1.21.1. Les branches 26.x restent sur les cinq langues de 0.6.0 jusqu'à leur extension dédiée.

## Projets pris en charge

### NeoOrigins

NeoOrigins 2.2.25 est requis. Pour les langues déjà traduites officiellement par NeoOrigins, le fallback ne conserve que les clés absentes en amont. Le néerlandais est fourni intégralement par NeoOrigins Localization. La cible 26.2 utilise un delta dédié pour ses clés supplémentaires.

### Medieval Origins Revival — Minecraft 1.21.1

Les **401 clés anglaises** sont couvertes dans les dix langues du build 0.7.0. L'import via `config/originpacks/` et l'affichage traduit d'un Origin ont déjà été validés en jeu sur 1.21.1.

### ibarn's quartet origins addon — Minecraft 1.21.1

Les **69 clés anglaises** sont couvertes dans les dix langues du build 0.7.0. L'add-on NeoForge 1.7.1 s'installe dans `mods/`. La localisation des quatre Origins a déjà été validée en jeu sur 1.21.1 avec la génération précédente.

### Origins Fantasy for NeoOrigins — Minecraft 1.21.1

Avec l'autorisation explicite de **DraconicArcher**, NeoOrigins Localization fournit les traductions des **240 clés anglaises** de la version 1.1.3 dans les dix langues du build 0.7.0. Les dix fichiers sont contrôlés contre le JAR CurseForge de référence : 240/240 clés couvertes, aucune clé manquante, aucun overlap avec une traduction officielle et aucun placeholder invalide.

Cette intégration n'embarque ni code, ni textures, ni modèles, ni données de gameplay d'Origins Fantasy. Le mod original reste nécessaire. La validation en jeu spécifique à Origins Fantasy reste à faire ; l'audit actuel valide la structure et la couverture des localisations, pas le gameplay.

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
```

Lorsqu'un projet amont ajoute une traduction officielle, les clés devenues inutiles doivent être retirées de notre fallback.

## Traduction et retours

Les traductions et leur maintenance utilisent une assistance générative/automatisée importante, avec contrôles de structure et direction humaine. Elles ne sont pas présentées comme des traductions intégralement relues par des locuteurs natifs. Les corrections de formulation et de terminologie sont donc bienvenues.

Un nom d'Origin est traduit seulement lorsque le résultat reste naturel, identifiable et lisible dans l'interface ; sinon le nom anglais peut être conservé.

## Licences et attributions

Le code et la documentation originaux de NeoOrigins Localization sont sous licence MIT. Les éléments dérivés de projets tiers restent soumis aux licences ou autorisations amont applicables. Voir [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

Le fichier [`catalog.json`](catalog.json) est la source de vérité du contenu suivi ; [`CATALOG.md`](CATALOG.md) en est la vue lisible.
''', encoding="utf-8")

TEST_PLAN.write_text(r'''# Plan de test 0.7.0 Beta

## Matrice de validation

| Cible | Java | NeoOrigins | Contenu du build | État |
|---|---:|---|---|---|
| Minecraft 1.21.1 | 21 | 2.2.25 | NeoOrigins + Medieval Origins Revival + ibarn + Origins Fantasy | Build/CI à valider, puis test final en jeu |
| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement | Validé en jeu sur 26.1.2 |
| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2 | Validé en jeu |

## Priorité du fallback

Installer NeoOrigins et NeoOrigins Localization. Vérifier dans une langue officiellement prise en charge par NeoOrigins qu'une clé officielle reste inchangée, puis qu'une clé absente en amont est bien fournie par notre fallback.

## Langues 1.21.1

Le build 0.7.0 doit proposer les ressources pour `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Pour chaque langue testée, contrôler au minimum l'écran de sélection, un nom d'Origin et une description longue afin de repérer les problèmes de coupure ou de formulation.

## Medieval Origins Revival — 1.21.1

Installer/importer Medieval Origins Revival via la méthode prise en charge par NeoOrigins (`config/originpacks/`). Vérifier qu'un Origin importé affiche correctement son nom et sa description traduits. Cette intégration a déjà été validée en jeu sur Minecraft 1.21.1.

## ibarn's quartet origins addon — 1.21.1

Installer la version NeoForge 1.7.1 dans `mods/`. Vérifier Ghaster, Sand Person, Soul Sorcerer et Wither Wraith. La localisation des quatre Origins a déjà été validée en jeu sur Minecraft 1.21.1 avec la génération précédente.

## Origins Fantasy for NeoOrigins — 1.21.1

Installer Origins Fantasy 1.1.3 avec NeoOrigins et NeoOrigins Localization. Vérifier au moins plusieurs Origins, leurs noms, descriptions et pouvoirs dans plusieurs des dix langues. L'audit automatisé doit d'abord confirmer 240/240 clés, zéro overlap, zéro clé manquante et zéro erreur de placeholder. La validation en jeu spécifique à cette nouvelle intégration reste distincte de l'audit structurel.

## Minecraft 26.2

Vérifier que le delta `neoorigins_26_2` est chargé sur 26.2 et absent des builds plus anciens. Le chargement et la localisation ont déjà été validés en jeu sur 26.2.

## Absence des add-ons dans les builds 26.x

Les JAR 26.1.x et 26.2 ne doivent contenir aucun fichier sous :

- `assets/medievalorigins/**` et `assets/medievalorigins_*/**` ;
- `assets/ibarnorigins/**` ;
- `assets/origins_fantasy/**` ;
- les namespaces d'expansion 1.21.1 `assets/neoorigins_121_batch1/**` et `assets/neoorigins_tr_*/**`.

## Client uniquement

Un serveur ne doit pas avoir besoin d'installer NeoOrigins Localization pour qu'un client bénéficie des traductions.

## CI

Chaque cible doit passer la validation JSON, l'audit NeoOrigins, la compilation avec sa version Java et la génération du JAR. Sur 1.21.1, les audits Medieval Origins Revival, ibarn et Origins Fantasy doivent aussi réussir sans overlap, clé manquante ni erreur de placeholder.
''', encoding="utf-8")

# Keep generated catalog notes in sync with the supported 1.21.1 add-ons.
generator = GENERATOR.read_text(encoding="utf-8")
generator = generator.replace(
    '"- Medieval Origins Revival et ibarn\'s quartet origins addon restent inclus uniquement dans le build 1.21.1 tant que leur compatibilité NeoForge 26.x n\'est pas validée.",',
    '"- Medieval Origins Revival, ibarn\'s quartet origins addon et Origins Fantasy for NeoOrigins restent inclus uniquement dans le build 1.21.1 tant que leur compatibilité NeoForge 26.x n\'est pas validée.",'
)
GENERATOR.write_text(generator, encoding="utf-8")

# Wire the Origins Fantasy audit into the permanent CI and archive its report.
workflow = BUILD_WORKFLOW.read_text(encoding="utf-8")
if "Audit Origins Fantasy upstream locales" not in workflow:
    marker = "      - name: Upload upstream locale audits\n"
    step = (
        "      - name: Audit Origins Fantasy upstream locales\n"
        "        if: matrix.audit_addons\n"
        "        run: python3 scripts/audit_origins_fantasy_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders\n\n"
    )
    workflow = workflow.replace(marker, step + marker)
if "build/origins-fantasy-upstream-audit" not in workflow:
    workflow = workflow.replace(
        "            build/ibarnorigins-upstream-audit\n",
        "            build/ibarnorigins-upstream-audit\n            build/origins-fantasy-upstream-audit\n"
    )
BUILD_WORKFLOW.write_text(workflow, encoding="utf-8")

# Regenerate the human-readable catalog from the canonical JSON.
exec(compile(GENERATOR.read_text(encoding="utf-8"), str(GENERATOR), "exec"), {"__name__": "__main__"})

# Remove generation-only helpers/workflows from the branch before merge.
for rel in [
    ".github/workflows/inspect-origins-fantasy.yml",
    ".github/workflows/integrate-origins-fantasy.yml",
    ".github/workflows/translate-origins-fantasy-parallel.yml",
    "scripts/integrate_origins_fantasy_artifacts.py",
]:
    path = ROOT / rel
    if path.exists():
        path.unlink()

print("Origins Fantasy integration metadata, docs and CI finalized.")
