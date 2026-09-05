#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))

lines = [
    "# Catalogue des localisations",
    "",
    "| Mod / add-on | Auteur | Lien | Langues disponibles |",
    "|---|---|---|---|",
]

for project in catalog.get("supported_projects", []):
    languages = []
    for code, meta in project.get("languages", {}).items():
        if meta.get("status") == "supported":
            languages.append(f"{meta.get('name', code)} (`{code}`)")
    link = project.get("curseforge") or project.get("source")
    lines.append(
        f"| {project['name']} | {project.get('author','')} | "
        f"[Projet]({link}) | {', '.join(languages) or '—'} |"
    )

(ROOT / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("CATALOG.md généré.")
