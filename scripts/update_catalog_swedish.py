#!/usr/bin/env python3
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
catalog["project"]["supported_locale_count"] = 17

for project in catalog["supported_projects"]:
    project_id = project["id"]
    if project_id == "neoorigins":
        project["compatibility"]["fallback_namespaces"].update({
            "swedish_common_glob": "neoorigins_sv_common_*",
            "swedish_mc_1_21_1": "neoorigins_sv_121",
        })
        project["languages"]["sv_se"] = {
            "name": "Svenska",
            "status": "supported",
            "targets": ["1.21.1", "26.1.x", "26.2"],
        }
    else:
        path = ROOT / f"src/main/resources/resourcepacks/fallback_localizations/assets/{project_id}/lang/sv_se.json"
        fallback_keys = len(json.loads(path.read_text(encoding="utf-8")))
        project["languages"]["sv_se"] = {
            "name": "Svenska",
            "status": "supported",
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
            "fallback_keys": fallback_keys,
        }

    def update_language_count(value):
        if not isinstance(value, str):
            return value
        return value.replace("seize langues", "dix-sept langues").replace("16 langues", "17 langues")

    compatibility = project.get("compatibility", {})
    for key in ("note", "status_note"):
        if key in compatibility:
            compatibility[key] = update_language_count(compatibility[key])
    for key in ("note", "status_note"):
        if key in project:
            project[key] = update_language_count(project[key])

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("catalog.json updated for sv_se")
