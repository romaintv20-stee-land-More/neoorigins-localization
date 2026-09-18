#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 34 |": "`0.9.0-beta+1.21.1` | 21 | 35 |",
    "`0.9.0-beta+26.1` | 25 | 34 |": "`0.9.0-beta+26.1` | 25 | 35 |",
    "`0.9.0-beta+26.2` | 25 | 34 |": "`0.9.0-beta+26.2` | 25 | 35 |",
    "**Catalan (`ca_es`)** et **Estonien (`et_ee`)**.": "**Catalan (`ca_es`)**, **Estonien (`et_ee`)** et **Lituanien (`lt_lt`)**.",
    "Les trente-quatre langues sont disponibles": "Les trente-cinq langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

et_block = """Pour l'estonien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
lt_block = et_block + """
Pour le lituanien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le lituanien :" not in text:
    if et_block not in text:
        raise RuntimeError("Estonian coverage block not found")
    text = text.replace(et_block, lt_block, 1)

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
            # 24 coverage entries are present through Estonian.
            if coverage.count(" · ") == 23:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_lt_common_*/lang/lt_lt.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Lithuanian common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_lt_121/lang/lt_lt.json",
    ASSETS / "neoorigins_26_1/lang/lt_lt.json",
    ASSETS / "neoorigins_26_2/lang/lt_lt.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Lithuanian target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/lt_lt.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/lt_lt.json").exists()
]
lt_121_files = 17 + len(addon_fallback_files)

et_jar = "- **estonien** : 27 fichiers fallback `et_ee` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
lt_jar = et_jar + f"\n- **lituanien** : {lt_121_files} fichiers fallback `lt_lt` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **lituanien** :" not in text:
    if et_jar not in text:
        raise RuntimeError("Estonian JAR validation line not found")
    text = text.replace(et_jar, lt_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for lt_lt / 0.9.0-beta ({lt_121_files} fallback files on 1.21.1)")
