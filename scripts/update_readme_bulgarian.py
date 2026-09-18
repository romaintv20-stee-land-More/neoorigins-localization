#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 22 |": "`0.9.0-beta+1.21.1` | 21 | 23 |",
    "`0.9.0-beta+26.1` | 25 | 22 |": "`0.9.0-beta+26.1` | 25 | 23 |",
    "`0.9.0-beta+26.2` | 25 | 22 |": "`0.9.0-beta+26.2` | 25 | 23 |",
    "**Roumain (`ro_ro`)** et **Grec (`el_gr`)**.": "**Roumain (`ro_ro`)**, **Grec (`el_gr`)** et **Bulgare (`bg_bg`)**.",
    "Les vingt-deux langues sont disponibles": "Les vingt-trois langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

el_block = """Pour le grec :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
bg_block = el_block + """
Pour le bulgare :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le bulgare :" not in text:
    if el_block not in text:
        raise RuntimeError("Greek coverage block not found")
    text = text.replace(el_block, bg_block, 1)

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
            if coverage.count(" · ") == 11:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_bg_common_*/lang/bg_bg.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Bulgarian common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_bg_121/lang/bg_bg.json",
    ASSETS / "neoorigins_26_1/lang/bg_bg.json",
    ASSETS / "neoorigins_26_2/lang/bg_bg.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Bulgarian target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/bg_bg.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/bg_bg.json").exists()
]
bg_121_files = 17 + len(addon_fallback_files)

greek_jar = "- **grec** : 27 fichiers `el_gr` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
bulgarian_jar = greek_jar + f"\n- **bulgare** : {bg_121_files} fichiers fallback `bg_bg` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **bulgare** :" not in text:
    if greek_jar not in text:
        raise RuntimeError("Greek JAR validation line not found")
    text = text.replace(greek_jar, bulgarian_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for bg_bg / 0.9.0-beta ({bg_121_files} fallback files on 1.21.1)")
