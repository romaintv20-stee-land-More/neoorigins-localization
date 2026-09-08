#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 25 |": "`0.9.0-beta+1.21.1` | 21 | 26 |",
    "`0.9.0-beta+26.1` | 25 | 25 |": "`0.9.0-beta+26.1` | 25 | 26 |",
    "`0.9.0-beta+26.2` | 25 | 25 |": "`0.9.0-beta+26.2` | 25 | 26 |",
    "**Bulgare (`bg_bg`)**, **Vietnamien (`vi_vn`)** et **Arabe (`ar_sa`)**.": "**Bulgare (`bg_bg`)**, **Vietnamien (`vi_vn`)**, **Arabe (`ar_sa`)** et **Hébreu (`he_il`)**.",
    "Les vingt-cinq langues sont disponibles": "Les vingt-six langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

ar_block = """Pour l'arabe :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
he_block = ar_block + """
Pour l'hébreu :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour l'hébreu :" not in text:
    if ar_block not in text:
        raise RuntimeError("Arabic coverage block not found")
    text = text.replace(ar_block, he_block, 1)

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
            if coverage.count(" · ") == 14:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_he_common_*/lang/he_il.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Hebrew common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_he_121/lang/he_il.json",
    ASSETS / "neoorigins_26_1/lang/he_il.json",
    ASSETS / "neoorigins_26_2/lang/he_il.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Hebrew target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/he_il.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/he_il.json").exists()
]
he_121_files = 17 + len(addon_fallback_files)

arabic_jar = "- **arabe** : 27 fichiers fallback `ar_sa` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
hebrew_jar = arabic_jar + f"\n- **hébreu** : {he_121_files} fichiers fallback `he_il` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **hébreu** :" not in text:
    if arabic_jar not in text:
        raise RuntimeError("Arabic JAR validation line not found")
    text = text.replace(arabic_jar, hebrew_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for he_il / 0.9.0-beta ({he_121_files} fallback files on 1.21.1)")
