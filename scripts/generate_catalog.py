#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

project_meta = catalog.get("project", {})
builds = project_meta.get("builds", {})

lines = [
    "# Catalogue des localisations",
    "",
    "## Builds Minecraft",
    "",
    "| Cible | Version du mod | Java | Contenu inclus | Validation en jeu |",
    "|---|---|---:|---|---|",
]

for target, meta in builds.items():
    included = ", ".join(meta.get("included_projects", [])) or "—"
    tested = meta.get("in_game_tested")
    if tested is True:
        tested_text = "Oui"
    elif isinstance(tested, list):
        tested_text = ", ".join(tested)
    else:
        tested_text = "Non"
    lines.append(
        f"| {target} | `{meta.get('version', '—')}` | {meta.get('java', '—')} | {included} | {tested_text} |"
    )

lines.extend([
    "",
    "## Projets et langues",
    "",
    "| Mod / add-on | Auteur | Versions Minecraft | Langues disponibles |",
    "|---|---|---|---|",
])

for project in catalog.get("supported_projects", []):
    languages = []
    for code, meta in project.get("languages", {}).items():
        if meta.get("status") == "supported":
            languages.append(f"{meta.get('name', code)} (`{code}`)")
    compat = project.get("compatibility", {})
    minecraft = compat.get("minecraft")
    if isinstance(minecraft, list):
        versions = ", ".join(minecraft)
    elif minecraft:
        versions = str(minecraft)
    elif compat.get("version"):
        versions = compat.get("version")
    else:
        versions = "1.21.1"
    link = project.get("curseforge") or project.get("source")
    lines.append(
        f"| [{project['name']}]({link}) | {project.get('author','')} | {versions} | "
        f"{' · '.join(languages) or '—'} |"
    )

lines.extend([
    "",
    "## Notes",
    "",
    "- Les builds 26.x n'embarquent actuellement que les traductions NeoOrigins.",
    "- Medieval Origins Revival et ibarn's quartet origins addon restent inclus uniquement dans le build 1.21.1 tant que leur compatibilité NeoForge 26.x n'est pas validée.",
    "- Les traductions officielles de NeoOrigins gardent toujours la priorité ; notre pack ne fournit que les clés manquantes.",
    "- La cible 26.2 utilise un delta de localisation dédié pour couvrir les nouvelles clés sans les ajouter aux builds plus anciens.",
])

(ROOT / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("CATALOG.md généré.")
