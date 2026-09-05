#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "src/main/resources/resourcepacks/fallback_localizations"
CATALOG = ROOT / "catalog.json"

errors = []
stats = []

def load_no_dupes(path: Path):
    duplicates = []
    def hook(pairs):
        out = {}
        for k, v in pairs:
            if k in out:
                duplicates.append(k)
            out[k] = v
        return out
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f, object_pairs_hook=hook)
    if duplicates:
        errors.append(f"{path}: clés dupliquées: {duplicates[:10]}")
    return obj

for path in sorted(PACK.glob("assets/*/lang/*.json")):
    try:
        obj = load_no_dupes(path)
    except Exception as exc:
        errors.append(f"{path}: JSON invalide: {exc}")
        continue
    if not isinstance(obj, dict):
        errors.append(f"{path}: la racine JSON doit être un objet")
        continue
    bad_values = [k for k, v in obj.items() if not isinstance(v, str)]
    if bad_values:
        errors.append(f"{path}: valeurs non textuelles: {bad_values[:10]}")
    stats.append((path, len(obj)))

try:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    for project in catalog.get("supported_projects", []):
        for locale, lang in project.get("languages", {}).items():
            rel = lang.get("file")
            if rel and not (ROOT / rel).exists():
                errors.append(f"catalog.json: fichier absent pour {project['id']} / {locale}: {rel}")
except Exception as exc:
    errors.append(f"catalog.json invalide: {exc}")

print("Validation NeoOrigins Localization")
print("=" * 36)
for path, count in stats:
    print(f"OK  {path.relative_to(ROOT)} : {count} clés")

if errors:
    print("\nERREURS:")
    for msg in errors:
        print("-", msg)
    sys.exit(1)

print("\nAucune erreur détectée.")
