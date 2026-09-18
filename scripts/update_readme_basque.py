#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 36 |": "`0.9.0-beta+1.21.1` | 21 | 37 |",
    "`0.9.0-beta+26.1` | 25 | 36 |": "`0.9.0-beta+26.1` | 25 | 37 |",
    "`0.9.0-beta+26.2` | 25 | 36 |": "`0.9.0-beta+26.2` | 25 | 37 |",
    "**Estonien (`et_ee`)**, **Lituanien (`lt_lt`)** et **Letton (`lv_lv`)**.": "**Estonien (`et_ee`)**, **Lituanien (`lt_lt`)**, **Letton (`lv_lv`)** et **Basque (`eu_es`)**.",
    "Les trente-six langues sont disponibles": "Les trente-sept langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

lv_block = """Pour le letton :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
eu_block = lv_block + """
Pour le basque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le basque :" not in text:
    if lv_block not in text:
        raise RuntimeError("Latvian coverage block not found")
    text = text.replace(lv_block, eu_block, 1)

addon_counts = {
    "Medieval Origins Revival": "401/401",
    "ibarn's quartet origins addon": "69/69",
    "Origins Fantasy for NeoOrigins": "240/240",
    "Origins: Backgrounds for NeoOrigins": "65/65",
    "Origins: More Backgrounds for NeoOrigins": "44/44",
    "Origins: Backgrounds ISS for NeoOrigins": "79/79",
    "Origins Furries for NeoOrigins": "117/117",
    "Origins: Classes Extended for NeoOrigins": "124/124",
    "Origins: Classes ISS for NeoOrigins": "99/99",
    "Origin Architect": "22/22",
}
lines = text.splitlines()
for i, line in enumerate(lines):
    for project, count in addon_counts.items():
        if line.startswith(f"| {project} |"):
            parts = line.split("|")
            coverage = parts[3].strip()
            # 26 coverage entries are present through Latvian.
            if coverage.count(" · ") == 25:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_eu_common_*/lang/eu_es.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Basque common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_eu_121/lang/eu_es.json",
    ASSETS / "neoorigins_26_1/lang/eu_es.json",
    ASSETS / "neoorigins_26_2/lang/eu_es.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Basque target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/eu_es.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/eu_es.json").exists()
]
eu_121_files = 17 + len(addon_fallback_files)

lv_jar = "- **letton** : 27 fichiers fallback `lv_lv` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
eu_jar = lv_jar + f"\n- **basque** : {eu_121_files} fichiers fallback `eu_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **basque** :" not in text:
    if lv_jar not in text:
        raise RuntimeError("Latvian JAR validation line not found")
    text = text.replace(lv_jar, eu_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for eu_es / 0.9.0-beta ({eu_121_files} fallback files on 1.21.1)")
