#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

project_meta = catalog.get("project", {})
builds = project_meta.get("builds", {})
primary_project = next(
    (project for project in catalog.get("supported_projects", []) if project.get("id") == "neoorigins"),
    {},
)
locale_codes = [
    code
    for code, meta in primary_project.get("languages", {}).items()
    if meta.get("status") == "supported"
]

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
    f"- Les {len(locale_codes)} langues ciblées sont : "
    + ", ".join(f"`{code}`" for code in locale_codes[:-1])
    + (f" et `{locale_codes[-1]}`." if locale_codes else "—."),
    "- Les builds 26.x n'embarquent actuellement que les traductions NeoOrigins.",
    "- Tous les add-ons listés restent inclus uniquement dans le build 1.21.1 tant que leur compatibilité NeoForge 26.x n'est pas validée.",
    "- Les traductions officielles des projets amont gardent toujours la priorité ; notre pack ne fournit que les clés manquantes.",
    "- Les cibles 1.21.1, 26.1.x et 26.2 utilisent leurs deltas de localisation dédiés lorsque nécessaire.",
])

(ROOT / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("CATALOG.md généré.")
