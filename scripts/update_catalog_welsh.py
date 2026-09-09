#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
if catalog["project"]["supported_locale_count"] != 44:
    raise SystemExit(f"Expected 44-locale baseline, got {catalog['project']['supported_locale_count']}")
catalog["project"]["supported_locale_count"] = 45

def recurse(v):
    if isinstance(v, dict):
        for k, x in list(v.items()): v[k] = recurse(x)
    elif isinstance(v, list):
        v = [recurse(x) for x in v]
    elif isinstance(v, str):
        v = v.replace("quarante-quatre langues", "quarante-cinq langues").replace("44 langues", "45 langues")
    return v

for project in catalog["supported_projects"]:
    pid = project["id"]
    if "fil_ph" not in project["languages"]:
        raise SystemExit(f"Filipino baseline missing from {pid}")
    if pid == "neoorigins":
        project["compatibility"]["fallback_namespaces"].update({
            "welsh_common_glob": "neoorigins_cy_common_*",
            "welsh_mc_1_21_1": "neoorigins_cy_121",
        })
        project["languages"]["cy_gb"] = {"name":"Cymraeg","status":"supported","targets":["1.21.1","26.1.x","26.2"]}
    else:
        p = ROOT / f"src/main/resources/resourcepacks/fallback_localizations/assets/{pid}/lang/cy_gb.json"
        if p.exists():
            project["languages"]["cy_gb"] = {"name":"Cymraeg","status":"supported","file":str(p.relative_to(ROOT)).replace('\\','/'),"fallback_keys":len(json.loads(p.read_text(encoding='utf-8')))}
        else:
            project["languages"]["cy_gb"] = {"name":"Cymraeg","status":"supported","coverage_source":"official_upstream","fallback_keys":0}
    recurse(project)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("catalog.json updated for cy_gb / 45 locales")
