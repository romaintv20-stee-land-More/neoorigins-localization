#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
if catalog["project"]["supported_locale_count"] != 45:
    raise SystemExit(f"Expected 45-locale baseline, got {catalog['project']['supported_locale_count']}")
catalog["project"]["supported_locale_count"] = 46

def recurse(v):
    if isinstance(v, dict):
        for k, x in list(v.items()): v[k] = recurse(x)
    elif isinstance(v, list):
        v = [recurse(x) for x in v]
    elif isinstance(v, str):
        v = v.replace("quarante-cinq langues", "quarante-six langues").replace("45 langues", "46 langues")
    return v

for project in catalog["supported_projects"]:
    pid = project["id"]
    if "cy_gb" not in project["languages"]:
        raise SystemExit(f"Welsh baseline missing from {pid}")
    if pid == "neoorigins":
        project["compatibility"]["fallback_namespaces"].update({
            "irish_common_glob": "neoorigins_ga_common_*",
            "irish_mc_1_21_1": "neoorigins_ga_121",
        })
        project["languages"]["ga_ie"] = {"name":"Gaeilge","status":"supported","targets":["1.21.1","26.1.x","26.2"]}
    else:
        p = ROOT / f"src/main/resources/resourcepacks/fallback_localizations/assets/{pid}/lang/ga_ie.json"
        if p.exists():
            project["languages"]["ga_ie"] = {"name":"Gaeilge","status":"supported","file":str(p.relative_to(ROOT)).replace('\\','/'),"fallback_keys":len(json.loads(p.read_text(encoding='utf-8')))}
        else:
            project["languages"]["ga_ie"] = {"name":"Gaeilge","status":"supported","coverage_source":"official_upstream","fallback_keys":0}
    recurse(project)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("catalog.json updated for ga_ie / 46 locales")
