#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"

catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

build = catalog["project"]["builds"]["26.1.x"]
build["version"] = "0.7.0-beta+26.1"
# The previous 0.6.0 generation was validated on 26.1.2, but the expanded
# ten-language 0.7.0 artifact still needs its final visual in-game pass.
build["in_game_tested"] = False

projects = {project["id"]: project for project in catalog["supported_projects"]}
neo = projects["neoorigins"]
for code in ("it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn"):
    lang = neo["languages"][code]
    targets = list(lang.get("targets", []))
    for target in ("1.21.1", "26.1.x"):
        if target not in targets:
            targets.append(target)
    lang["targets"] = targets
    lang["note"] = (
        "Couverture de fallback auditée pour Minecraft 1.21.1 et 26.1.x contre NeoOrigins ; "
        "les traductions officielles amont gardent la priorité. Les deux références amont "
        "utilisées pour ces cibles pointent vers le même commit."
    )

compat = neo["compatibility"]
compat["note"] = (
    "Les builds 26.x n'embarquent que la localisation NeoOrigins. Les références amont "
    "1.21.1 et v2.2.25 pointent vers le même commit, ce qui permet de partager le premier "
    "lot 0.7.0 entre 1.21.1 et 26.1.x avec un audit séparé par cible. Minecraft 26.2 "
    "utilise un delta de traduction dédié pour les clés ajoutées ou modifiées sur sa branche."
)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
subprocess.run(["python3", str(ROOT / "scripts/generate_catalog.py")], check=True)
print("catalog.json et CATALOG.md mis à jour pour 26.1.x / 0.7.0")
