#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

# README
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = readme.replace(
    "Origins: Classes Extended for NeoOrigins + Origins: Classes ISS for NeoOrigins |",
    "Origins: Classes Extended for NeoOrigins + Origins: Classes ISS for NeoOrigins + Origin Architect (NeoOrigins Addon) |",
)
section = """### Origin Architect (NeoOrigins Addon) — Minecraft 1.21.1

La 0.8.0 Beta ajoute aussi les traductions de **Origin Architect 3.0.1** par **reotpak**. La version CurseForge de référence (project ID `1635001`, file ID `8568110`) est publiée sous licence MIT. Le namespace `originsmodernui` contient **22 clés anglaises** ; aucune des dix langues ciblées par NeoOrigins Localization n'est fournie officiellement en amont, donc le fallback couvre **22/22 clés dans chacune des dix langues**.

L'audit est épinglé sur le commit source `f58a6261292942d4123c46ff221fbdade138a329`. Le mod original reste requis et cette intégration est limitée au build Minecraft 1.21.1 ; les builds 26.x excluent explicitement `originsmodernui`.

"""
if "### Origin Architect (NeoOrigins Addon)" not in readme:
    readme = readme.replace("## Fonctionnement\n", section + "## Fonctionnement\n")
if "audit_origin_architect_upstream.py" not in readme:
    readme = readme.replace(
        "python scripts/audit_origins_classes_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders\n",
        "python scripts/audit_origins_classes_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders\npython scripts/audit_origin_architect_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders\n",
    )
readme_path.write_text(readme, encoding="utf-8")

# Attributions
attr_path = ROOT / "docs/ATTRIBUTIONS.md"
attr = attr_path.read_text(encoding="utf-8")
attr_section = """## Origin Architect (NeoOrigins Addon)

- Projet : Origin Architect (NeoOrigins Addon)
- Auteur : reotpak / ReoTpak
- CurseForge : https://www.curseforge.com/minecraft/mc-mods/origin-architect
- Source : https://github.com/ReoTpak/origin-architect-modern-uI
- Project ID CurseForge : `1635001`
- Version ciblée : fichier CurseForge `originsmodernui-3.0.1-1.21.1.jar` (file ID `8568110`) pour Minecraft 1.21.1
- Référence source auditée : commit `f58a6261292942d4123c46ff221fbdade138a329`
- Namespace : `originsmodernui`
- Licence amont : MIT (déclarée sur la page CurseForge du projet)
- Utilisation ici : localisations `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn` des 22 chaînes de `assets/originsmodernui/lang/en_us.json`.
- Modifications : traduction et adaptation linguistique ; le nom de produit `Origin Architect` est conservé comme nom propre.
- Priorité amont : si une traduction officielle apparaît ensuite pour une langue ciblée, elle doit garder la priorité et les clés correspondantes de notre fallback doivent être retirées.
- Le mod original reste requis pour utiliser ces traductions ; l'intégration est limitée au build Minecraft 1.21.1.

"""
marker = "Aucune attribution ne signifie que les auteurs amont approuvent ou sponsorisent NeoOrigins Localization au-delà des autorisations explicitement mentionnées ci-dessus."
if "## Origin Architect (NeoOrigins Addon)" not in attr:
    attr = attr.replace(marker, attr_section + marker)
attr_path.write_text(attr, encoding="utf-8")

# catalog.json
catalog_path = ROOT / "catalog.json"
data = json.loads(catalog_path.read_text(encoding="utf-8"))
included = data["project"]["builds"]["1.21.1"]["included_projects"]
if "originsmodernui" not in included:
    included.append("originsmodernui")
langs = {
    "fr_fr": "Français", "de_de": "Deutsch", "es_es": "Español", "pt_br": "Português (Brasil)",
    "nl_nl": "Nederlands", "it_it": "Italiano", "pl_pl": "Polski", "ru_ru": "Русский",
    "tr_tr": "Türkçe", "zh_cn": "简体中文"
}
projects = data["supported_projects"]
if not any(project.get("id") == "originsmodernui" for project in projects):
    projects.append({
        "id": "originsmodernui",
        "name": "Origin Architect (NeoOrigins Addon)",
        "author": "reotpak",
        "namespace": "originsmodernui",
        "curseforge": "https://www.curseforge.com/minecraft/mc-mods/origin-architect",
        "source": "https://github.com/ReoTpak/origin-architect-modern-uI",
        "license": {"code_and_localization": "MIT", "attribution_required": True},
        "compatibility": {
            "method": "NeoForge mod in mods/",
            "version": "3.0.1 / Minecraft 1.21.1",
            "minecraft": ["1.21.1"],
            "source_ref": "f58a6261292942d4123c46ff221fbdade138a329",
            "curseforge_file_id": 8568110,
            "in_game_validation": "pending",
            "note": "22/22 clés anglaises couvertes dans les dix langues ; aucune traduction officielle détectée parmi les dix locales ciblées ; absent des builds 26.x."
        },
        "coverage": {"source_keys": 22, "fallback_keys_per_locale": 22},
        "languages": {
            locale: {"name": name, "status": "supported", "file": f"src/main/resources/resourcepacks/fallback_localizations/assets/originsmodernui/lang/{locale}.json"}
            for locale, name in langs.items()
        }
    })
catalog_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
