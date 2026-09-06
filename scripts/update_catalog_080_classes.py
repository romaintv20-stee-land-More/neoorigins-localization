#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "catalog.json"
data = json.loads(PATH.read_text(encoding="utf-8"))

langs = {
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

target = data["build_targets"]["1.21.1"]
for project_id in ("origins_classes_ex", "origins_classes_iss"):
    if project_id not in target["included_projects"]:
        target["included_projects"].append(project_id)

projects = {project["id"]: project for project in data["supported_projects"]}

projects["origins_classes_ex"] = {
    "id": "origins_classes_ex",
    "name": "Origins: Classes Extended for NeoOrigins",
    "author": "DraconicArcher",
    "namespace": "origins_classes_ex",
    "curseforge": "https://www.curseforge.com/minecraft/mc-mods/origins-classes-extended-for-neoorigins",
    "license": {
        "localization_redistribution": "explicit_author_permission",
        "permission_date": "2026-09-06",
        "attribution_required": True
    },
    "compatibility": {
        "method": "NeoForge mod in mods/",
        "version": "1.0.1 / Minecraft 1.21.1",
        "minecraft": ["1.21.1"],
        "dependencies": ["NeoOrigins"],
        "in_game_validation": "pending",
        "note": "Audité contre le JAR CurseForge 8393343 ; 124/124 clés dans les dix langues ciblées ; aucune traduction officielle détectée ; absent des builds 26.x."
    },
    "coverage": {
        "source_keys": 124,
        "fallback_keys_per_locale": 124
    },
    "languages": {
        locale: {
            "name": name,
            "path": f"src/main/resources/resourcepacks/fallback_localizations/assets/origins_classes_ex/lang/{locale}.json"
        }
        for locale, name in langs.items()
    }
}

projects["origins_classes_iss"] = {
    "id": "origins_classes_iss",
    "name": "Origins: Classes ISS for NeoOrigins",
    "author": "DraconicArcher",
    "namespace": "origins_classes_iss",
    "curseforge": "https://www.curseforge.com/minecraft/mc-mods/origins-classes-iss-for-neoorigins",
    "license": {
        "localization_redistribution": "explicit_author_permission",
        "permission_date": "2026-09-06",
        "attribution_required": True
    },
    "compatibility": {
        "method": "NeoForge mod in mods/",
        "version": "1.0.1 / Minecraft 1.21.1",
        "minecraft": ["1.21.1"],
        "dependencies": ["NeoOrigins", "Iron's Spells 'n Spellbooks"],
        "in_game_validation": "pending",
        "note": "Audité contre le JAR CurseForge 8592095 ; 99/99 clés dans les dix langues ciblées ; aucune traduction officielle détectée ; absent des builds 26.x."
    },
    "coverage": {
        "source_keys": 99,
        "fallback_keys_per_locale": 99
    },
    "languages": {
        locale: {
            "name": name,
            "path": f"src/main/resources/resourcepacks/fallback_localizations/assets/origins_classes_iss/lang/{locale}.json"
        }
        for locale, name in langs.items()
    }
}

ordered = []
seen = set()
for project in data["supported_projects"]:
    pid = project["id"]
    ordered.append(projects[pid])
    seen.add(pid)
for pid in ("origins_classes_ex", "origins_classes_iss"):
    if pid not in seen:
        ordered.append(projects[pid])

data["supported_projects"] = ordered
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
