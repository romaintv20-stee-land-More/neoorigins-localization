#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

# Stable Gradle metadata.
props = ROOT / "gradle.properties"
text = props.read_text(encoding="utf-8")
text = text.replace("mod_version=0.9.0-beta", "mod_version=1.0.0")
props.write_text(text, encoding="utf-8")

# Human-facing release documentation.
readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
for old, new in (
    ("`0.9.0-beta+1.21.1`", "`1.0.0+1.21.1`"),
    ("`0.9.0-beta+26.1`", "`1.0.0+26.1`"),
    ("`0.9.0-beta+26.2`", "`1.0.0+26.2`"),
    ("La **0.9.0 Beta** prend en charge", "La **1.0.0** prend en charge"),
    ("| Origins: Backgrounds for NeoOrigins | 1.0.2 |", "| Origins: Backgrounds for NeoOrigins | 1.0.3 |"),
    ("| Origins: More Backgrounds for NeoOrigins | 1.0.2 |", "| Origins: More Backgrounds for NeoOrigins | 1.0.4 |"),
    ("## Validation des JAR 0.9.0", "## Validation des JAR 1.0.0"),
    ("référence NeoOrigins 2.2.26 a confirmé", "référence NeoOrigins 2.2.27 a confirmé"),
):
    text = text.replace(old, new)

context_note = (
    "\nLes versions Origins: Backgrounds 1.0.3 et Origins: More Backgrounds 1.0.4 ajoutent "
    "quatre chaînes contextuelles pour l'`Orb of Background`. Elles sont fournies dans les 91 langues "
    "par un pack intégré activé uniquement lorsqu'un de ces add-ons est chargé, afin de ne pas renommer "
    "l'orbe violette de NeoOrigins lorsqu'ils sont absents.\n"
)
marker = "Les intégrations DraconicArcher sont réalisées avec son autorisation explicite"
if context_note.strip() not in text and marker in text:
    text = text.replace(marker, context_note + "\n" + marker, 1)
readme.write_text(text, encoding="utf-8")

# Machine-readable catalog.
cat_path = ROOT / "catalog.json"
cat = json.loads(cat_path.read_text(encoding="utf-8"))
cat["project"]["builds"]["1.21.1"]["version"] = "1.0.0+1.21.1"
cat["project"]["builds"]["26.1.x"]["version"] = "1.0.0+26.1"
cat["project"]["builds"]["26.2"]["version"] = "1.0.0+26.2"
for project in cat["supported_projects"]:
    if project["id"] == "origins_backgrounds":
        project["compatibility"]["version"] = "1.0.3 / Minecraft 1.21.1"
        project["compatibility"]["note"] = (
            "Audité contre le JAR CurseForge 8875601 ; 65 clés du namespace origins_backgrounds "
            "+ 4 clés contextuelles Orb of Background dans le namespace neoorigins ; absent des builds 26.x."
        )
        project["coverage"]["source_keys"] = 65
        project["coverage"]["fallback_keys_per_locale"] = 65
        project["coverage"]["contextual_keys_per_locale"] = 4
        project["coverage"]["effective_coverage_per_locale"] = 69
    elif project["id"] == "origins_backgrounds_two":
        project["compatibility"]["version"] = "1.0.4 / Minecraft 1.21.1"
        project["compatibility"]["note"] = (
            "Audité contre le JAR CurseForge 8875590 ; 44 clés propres/partagées inchangées "
            "+ les 4 mêmes clés contextuelles Orb of Background ; absent des builds 26.x."
        )
        project["coverage"]["contextual_keys_per_locale"] = 4
        project["coverage"]["effective_coverage_per_locale"] = 48
cat_path.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Regenerate the readable catalog from catalog.json.
subprocess.run([sys.executable, str(ROOT / "scripts/generate_catalog.py")], cwd=ROOT, check=True)
print("1.0.0 release metadata finalized")
