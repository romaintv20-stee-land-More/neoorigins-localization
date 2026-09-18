#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 37 |": "`0.9.0-beta+1.21.1` | 21 | 38 |",
    "`0.9.0-beta+26.1` | 25 | 37 |": "`0.9.0-beta+26.1` | 25 | 38 |",
    "`0.9.0-beta+26.2` | 25 | 37 |": "`0.9.0-beta+26.2` | 25 | 38 |",
    "**Lituanien (`lt_lt`)**, **Letton (`lv_lv`)** et **Basque (`eu_es`)**.": "**Lituanien (`lt_lt`)**, **Letton (`lv_lv`)**, **Basque (`eu_es`)** et **Galicien (`gl_es`)**.",
    "Les trente-sept langues sont disponibles": "Les trente-huit langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

eu_block = """Pour le basque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
gl_block = eu_block + """
Pour le galicien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le galicien :" not in text:
    if eu_block not in text:
        raise RuntimeError("Basque coverage block not found")
    text = text.replace(eu_block, gl_block, 1)

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
            # 27 coverage entries are present through Basque.
            if coverage.count(" · ") == 26:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_gl_common_*/lang/gl_es.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Galician common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_gl_121/lang/gl_es.json",
    ASSETS / "neoorigins_26_1/lang/gl_es.json",
    ASSETS / "neoorigins_26_2/lang/gl_es.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Galician target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/gl_es.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/gl_es.json").exists()
]
gl_121_files = 17 + len(addon_fallback_files)

eu_jar = "- **basque** : 27 fichiers fallback `eu_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
gl_jar = eu_jar + f"\n- **galicien** : {gl_121_files} fichiers fallback `gl_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **galicien** :" not in text:
    if eu_jar not in text:
        raise RuntimeError("Basque JAR validation line not found")
    text = text.replace(eu_jar, gl_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for gl_es / 0.9.0-beta ({gl_121_files} fallback files on 1.21.1)")
