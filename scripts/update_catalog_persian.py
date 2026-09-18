#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
catalog["project"]["supported_locale_count"] = 41


def update_text(value):
    if not isinstance(value, str):
        return value
    return (value
            .replace("quarante langues", "quarante et une langues")
            .replace("40 langues", "41 langues"))


def recurse(value):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            value[key] = recurse(child)
        return value
    if isinstance(value, list):
        return [recurse(child) for child in value]
    return update_text(value)


for project in catalog["supported_projects"]:
    project_id = project["id"]
    if project_id == "neoorigins":
        project["compatibility"]["fallback_namespaces"].update({
            "persian_common_glob": "neoorigins_fa_common_*",
            "persian_mc_1_21_1": "neoorigins_fa_121",
        })
        project["languages"]["fa_ir"] = {
            "name": "فارسی",
            "status": "supported",
            "targets": ["1.21.1", "26.1.x", "26.2"],
        }
    else:
        path = ROOT / f"src/main/resources/resourcepacks/fallback_localizations/assets/{project_id}/lang/fa_ir.json"
        if path.exists():
            project["languages"]["fa_ir"] = {
                "name": "فارسی",
                "status": "supported",
                "file": str(path.relative_to(ROOT)).replace("\\", "/"),
                "fallback_keys": len(json.loads(path.read_text(encoding="utf-8"))),
            }
        else:
            project["languages"]["fa_ir"] = {
                "name": "فارسی",
                "status": "supported",
                "coverage_source": "official_upstream",
                "fallback_keys": 0,
            }
    recurse(project)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("catalog.json updated for fa_ir / 0.9.0-beta")
