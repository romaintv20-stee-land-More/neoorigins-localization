#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

OVERRIDES = {
    "origins.neoorigins.class_nitwit.name": "Аңкоо",
    "neoorigins.configuration.classes.class_nitwit": "Аңкоо",
    "neoorigins.configuration.class_nitwit": "Аңкоо",
    "origins.neoorigins.kraken.name": "Кракен",
    "neoorigins.configuration.kraken": "Кракен",
    "origins.neoorigins.sculkborn.name": "Скалкборн",
    "neoorigins.configuration.sculkborn": "Скалкборн",
    "origins.neoorigins.enderian.name": "Эндериан",
    "neoorigins.configuration.enderian": "Эндериан",
    "origins.neoorigins.sylvan.name": "Сильван",
    "neoorigins.configuration.sylvan": "Сильван",
    "origins.neoorigins.voidwalker.name": "Боштук кезгини",
    "neoorigins.configuration.voidwalker": "Боштук кезгини",
    "origins.neoorigins.class_lumberjack.name": "Токойчу",
    "origins.neoorigins.wraith.name": "Арбак",
}

# A few add-on/configuration labels reuse the raw NeoOrigins identity name under
# a different key. Replace only exact standalone values so branded words inside
# longer sentences remain untouched.
VALUE_OVERRIDES = {
    "Enderian": "Эндериан",
    "Kraken": "Кракен",
    "Sculkborn": "Скалкборн",
    "Sylvan": "Сильван",
    "Voidwalker": "Боштук кезгини",
}

changed_files = 0
changed_values = 0
seen = set()
for path in sorted(ASSETS.glob("**/lang/ky_kg.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, replacement in OVERRIDES.items():
        if key in data:
            seen.add(key)
            if data[key] != replacement:
                data[key] = replacement
                changed = True
                changed_values += 1
    for key, value in list(data.items()):
        if value in VALUE_OVERRIDES:
            data[key] = VALUE_OVERRIDES[value]
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

missing = sorted(set(OVERRIDES) - seen)
if missing:
    raise SystemExit(f"Expected Kyrgyz keys not found: {missing}")
print(f"Final Kyrgyz visible-name pass: {changed_values} values across {changed_files} files")
