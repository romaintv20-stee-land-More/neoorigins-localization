#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 29 |": "`0.9.0-beta+1.21.1` | 21 | 30 |",
    "`0.9.0-beta+26.1` | 25 | 29 |": "`0.9.0-beta+26.1` | 25 | 30 |",
    "`0.9.0-beta+26.2` | 25 | 29 |": "`0.9.0-beta+26.2` | 25 | 30 |",
    "**Slovaque (`sk_sk`)** et **Slovène (`sl_si`)**.": "**Slovaque (`sk_sk`)**, **Slovène (`sl_si`)** et **Croate (`hr_hr`)**.",
    "Les vingt-neuf langues sont disponibles": "Les trente langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

sl_block = """Pour le slovène :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
hr_block = sl_block + """
Pour le croate :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le croate :" not in text:
    if sl_block not in text:
        raise RuntimeError("Slovenian coverage block not found")
    text = text.replace(sl_block, hr_block, 1)

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
            if coverage.count(" · ") == 18:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_hr_common_*/lang/hr_hr.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Croatian common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_hr_121/lang/hr_hr.json",
    ASSETS / "neoorigins_26_1/lang/hr_hr.json",
    ASSETS / "neoorigins_26_2/lang/hr_hr.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Croatian target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/hr_hr.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/hr_hr.json").exists()
]
hr_121_files = 17 + len(addon_fallback_files)

slovenian_jar = "- **slovène** : 27 fichiers fallback `sl_si` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
croatian_jar = slovenian_jar + f"\n- **croate** : {hr_121_files} fichiers fallback `hr_hr` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **croate** :" not in text:
    if slovenian_jar not in text:
        raise RuntimeError("Slovenian JAR validation line not found")
    text = text.replace(slovenian_jar, croatian_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for hr_hr / 0.9.0-beta ({hr_121_files} fallback files on 1.21.1)")
