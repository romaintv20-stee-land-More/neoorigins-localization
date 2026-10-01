#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
if catalog["project"]["supported_locale_count"] != 55:
    raise SystemExit(f"Expected 55-locale baseline, got {catalog['project']['supported_locale_count']}")
catalog["project"]["supported_locale_count"] = 56

def recurse(v):
    if isinstance(v, dict):
        for k, x in list(v.items()):
            v[k] = recurse(x)
    elif isinstance(v, list):
        v = [recurse(x) for x in v]
    elif isinstance(v, str):
        v = v.replace("cinquante-cinq langues", "cinquante-six langues").replace("55 langues", "56 langues")
    return v

for project in catalog["supported_projects"]:
    pid = project["id"]
    if "af_za" not in project["languages"]:
        raise SystemExit(f"Afrikaans baseline missing from {pid}")
    if pid == "neoorigins":
        project["compatibility"]["fallback_namespaces"].update({
            "azerbaijani_common_glob": "neoorigins_az_common_*",
            "azerbaijani_mc_1_21_1": "neoorigins_az_121",
        })
        project["languages"]["az_az"] = {
            "name": "Azərbaycanca",
            "status": "supported",
            "targets": ["1.21.1", "26.1.x", "26.2"],
        }
    else:
        p = ROOT / f"src/main/resources/resourcepacks/fallback_localizations/assets/{pid}/lang/az_az.json"
        if p.exists():
            project["languages"]["az_az"] = {
                "name": "Azərbaycanca",
                "status": "supported",
                "file": str(p.relative_to(ROOT)).replace('\\', '/'),
                "fallback_keys": len(json.loads(p.read_text(encoding='utf-8'))),
            }
        else:
            project["languages"]["az_az"] = {
                "name": "Azərbaycanca",
                "status": "supported",
                "coverage_source": "official_upstream",
                "fallback_keys": 0,
            }
    recurse(project)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("catalog.json updated for az_az / 56 locales")
