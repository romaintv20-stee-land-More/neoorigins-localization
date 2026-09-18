#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 41 |": "`0.9.0-beta+1.21.1` | 21 | 42 |",
    "`0.9.0-beta+26.1` | 25 | 41 |": "`0.9.0-beta+26.1` | 25 | 42 |",
    "`0.9.0-beta+26.2` | 25 | 41 |": "`0.9.0-beta+26.2` | 25 | 42 |",
    "**Norvégien nynorsk (`nn_no`)** et **Persan (`fa_ir`)**.": "**Norvégien nynorsk (`nn_no`)**, **Persan (`fa_ir`)** et **Islandais (`is_is`)**.",
    "Les quarante et une langues sont disponibles": "Les quarante-deux langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

fa_block = """Pour le persan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
is_block = fa_block + """
Pour l'islandais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour l'islandais :" not in text:
    if fa_block not in text:
        raise RuntimeError("Persian coverage block not found")
    text = text.replace(fa_block, is_block, 1)

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
            if coverage.count(" · ") == 30:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_is_common_*/lang/is_is.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Icelandic common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_is_121/lang/is_is.json",
    ASSETS / "neoorigins_26_1/lang/is_is.json",
    ASSETS / "neoorigins_26_2/lang/is_is.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Icelandic target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/is_is.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/is_is.json").exists()
]
is_121_files = 17 + len(addon_fallback_files)

fa_jar_prefix = "- **persan** :"
is_jar = f"- **islandais** : {is_121_files} fichiers fallback `is_is` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **islandais** :" not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(fa_jar_prefix):
            lines.insert(i + 1, is_jar)
            break
    else:
        raise RuntimeError("Persian JAR validation line not found")
    text = "\n".join(lines) + "\n"

README.write_text(text, encoding="utf-8")
print(f"README.md updated for is_is / 0.9.0-beta ({is_121_files} fallback files on 1.21.1)")
