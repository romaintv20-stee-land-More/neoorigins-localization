#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 35 |": "`0.9.0-beta+1.21.1` | 21 | 36 |",
    "`0.9.0-beta+26.1` | 25 | 35 |": "`0.9.0-beta+26.1` | 25 | 36 |",
    "`0.9.0-beta+26.2` | 25 | 35 |": "`0.9.0-beta+26.2` | 25 | 36 |",
    "**Estonien (`et_ee`)** et **Lituanien (`lt_lt`)**.": "**Estonien (`et_ee`)**, **Lituanien (`lt_lt`)** et **Letton (`lv_lv`)**.",
    "Les trente-cinq langues sont disponibles": "Les trente-six langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

lt_block = """Pour le lituanien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
lv_block = lt_block + """
Pour le letton :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le letton :" not in text:
    if lt_block not in text:
        raise RuntimeError("Lithuanian coverage block not found")
    text = text.replace(lt_block, lv_block, 1)

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
            # 25 coverage entries are present through Lithuanian.
            if coverage.count(" · ") == 24:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_lv_common_*/lang/lv_lv.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Latvian common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_lv_121/lang/lv_lv.json",
    ASSETS / "neoorigins_26_1/lang/lv_lv.json",
    ASSETS / "neoorigins_26_2/lang/lv_lv.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Latvian target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/lv_lv.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/lv_lv.json").exists()
]
lv_121_files = 17 + len(addon_fallback_files)

lt_jar = "- **lituanien** : 27 fichiers fallback `lt_lt` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
lv_jar = lt_jar + f"\n- **letton** : {lv_121_files} fichiers fallback `lv_lv` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **letton** :" not in text:
    if lt_jar not in text:
        raise RuntimeError("Lithuanian JAR validation line not found")
    text = text.replace(lt_jar, lv_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for lv_lv / 0.9.0-beta ({lv_121_files} fallback files on 1.21.1)")
