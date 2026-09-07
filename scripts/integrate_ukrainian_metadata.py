#!/usr/bin/env python3
from copy import deepcopy
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

AUDITS = [
    "scripts/audit_medievalorigins_upstream.py",
    "scripts/audit_ibarnorigins_upstream.py",
    "scripts/audit_origins_fantasy_upstream.py",
    "scripts/audit_origins_backgrounds_upstream.py",
    "scripts/audit_origins_more_backgrounds_upstream.py",
    "scripts/audit_origins_backgrounds_iss_upstream.py",
    "scripts/audit_origins_furries_upstream.py",
    "scripts/audit_origins_classes_extended_upstream.py",
    "scripts/audit_origins_classes_iss_upstream.py",
    "scripts/audit_origin_architect_upstream.py",
]

for rel in AUDITS:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    old = '"ja_jp", "ko_kr")'
    new = '"ja_jp", "ko_kr", "uk_ua")'
    if new not in text:
        if old not in text:
            raise RuntimeError(f"LOCALES marker not found in {rel}")
        text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")

# README
path = ROOT / "README.md"
text = path.read_text(encoding="utf-8")
text = text.replace("| 14 |", "| 15 |")
text = text.replace(
    "**Japonais (`ja_jp`)** et **Coréen (`ko_kr`)**.",
    "**Japonais (`ja_jp`)**, **Coréen (`ko_kr`)** et **Ukrainien (`uk_ua`)**.",
)
text = text.replace("Les quatorze langues", "Les quinze langues")
ko_block = """Pour le coréen :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n"""
uk_block = """\nPour l'ukrainien :\n\n- **1.21.1 : 2 296/2 296 clés** couvertes ;\n- **26.1.x : 2 307/2 307 clés** couvertes ;\n- **26.2 : 2 307/2 307 clés** couvertes.\n"""
if "Pour l'ukrainien" not in text:
    if ko_block not in text:
        raise RuntimeError("README Korean coverage block not found")
    text = text.replace(ko_block, ko_block + uk_block, 1)
text = text.replace("Couverture CS / HU / JA / KO", "Couverture CS / HU / JA / KO / UK")
for n in (401, 69, 240, 65, 44, 79, 117, 124, 99, 22):
    four = " · ".join([f"{n}/{n}"] * 4)
    five = " · ".join([f"{n}/{n}"] * 5)
    text = text.replace(four, five)
path.write_text(text, encoding="utf-8")

# CATALOG.md
path = ROOT / "CATALOG.md"
text = path.read_text(encoding="utf-8")
if "Українська (`uk_ua`)" not in text:
    text = text.replace("한국어 (`ko_kr`) |", "한국어 (`ko_kr`) · Українська (`uk_ua`) |")
text = text.replace("Les quatorze langues", "Les quinze langues")
text = text.replace(
    "`ja_jp` et `ko_kr`.",
    "`ja_jp`, `ko_kr` et `uk_ua`.",
)
ko_note = "- NeoOrigins coréen couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2.\n"
uk_note = "- NeoOrigins ukrainien couvre **2 296/2 296** clés en 1.21.1, **2 307/2 307** en 26.1.x et **2 307/2 307** en 26.2.\n"
if uk_note not in text:
    if ko_note not in text:
        raise RuntimeError("CATALOG Korean coverage note not found")
    text = text.replace(ko_note, ko_note + uk_note, 1)
path.write_text(text, encoding="utf-8")

# catalog.json
path = ROOT / "catalog.json"
data = json.loads(path.read_text(encoding="utf-8"))
data["project"]["supported_locale_count"] = 15
physical_counts = {
    "medievalorigins": 401,
    "ibarnorigins": 69,
    "origins_fantasy": 240,
    "origins_backgrounds": 65,
    "origins_backgrounds_two": 39,
    "origins_backgrounds_iss": 77,
    "origins_furries": 117,
    "origins_classes_ex": 124,
    "origins_classes_iss": 99,
    "originsmodernui": 22,
}
for project in data["supported_projects"]:
    langs = project["languages"]
    if project["id"] == "neoorigins":
        langs["uk_ua"] = {
            "name": "Українська",
            "status": "supported",
            "targets": ["1.21.1", "26.1.x", "26.2"],
        }
        continue
    if project["id"] not in physical_counts:
        raise RuntimeError(f"No Ukrainian physical count for {project['id']}")
    entry = deepcopy(langs["ko_kr"])
    entry["name"] = "Українська"
    entry.pop("official_keys", None)
    entry.pop("files_glob", None)
    entry["fallback_keys"] = physical_counts[project["id"]]
    namespace = project["namespace"]
    entry["file"] = f"src/main/resources/resourcepacks/fallback_localizations/assets/{namespace}/lang/uk_ua.json"
    langs["uk_ua"] = entry

def update_strings(obj):
    if isinstance(obj, dict):
        return {k: update_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [update_strings(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace("quatorze", "quinze")
    return obj

data = update_strings(data)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
