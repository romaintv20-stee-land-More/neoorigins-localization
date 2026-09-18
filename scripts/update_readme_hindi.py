#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 38 |": "`0.9.0-beta+1.21.1` | 21 | 39 |",
    "`0.9.0-beta+26.1` | 25 | 38 |": "`0.9.0-beta+26.1` | 25 | 39 |",
    "`0.9.0-beta+26.2` | 25 | 38 |": "`0.9.0-beta+26.2` | 25 | 39 |",
    "**Basque (`eu_es`)** et **Galicien (`gl_es`)**.": "**Basque (`eu_es`)**, **Galicien (`gl_es`)** et **Hindi (`hi_in`)**.",
    "Les trente-huit langues sont disponibles": "Les trente-neuf langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

gl_block = """Pour le galicien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
hi_block = gl_block + """
Pour le hindi :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le hindi :" not in text:
    if gl_block not in text:
        raise RuntimeError("Galician coverage block not found")
    text = text.replace(gl_block, hi_block, 1)

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
            # 28 coverage entries are present through Galician.
            if coverage.count(" · ") == 27:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_hi_common_*/lang/hi_in.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Hindi common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_hi_121/lang/hi_in.json",
    ASSETS / "neoorigins_26_1/lang/hi_in.json",
    ASSETS / "neoorigins_26_2/lang/hi_in.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Hindi target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/hi_in.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/hi_in.json").exists()
]
hi_121_files = 17 + len(addon_fallback_files)

gl_jar_prefix = "- **galicien** :"
hi_jar = f"- **hindi** : {hi_121_files} fichiers fallback `hi_in` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **hindi** :" not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(gl_jar_prefix):
            lines.insert(i + 1, hi_jar)
            break
    else:
        raise RuntimeError("Galician JAR validation line not found")
    text = "\n".join(lines) + "\n"

README.write_text(text, encoding="utf-8")
print(f"README.md updated for hi_in / 0.9.0-beta ({hi_121_files} fallback files on 1.21.1)")
