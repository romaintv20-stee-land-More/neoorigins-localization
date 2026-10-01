#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 32 |": "`0.9.0-beta+1.21.1` | 21 | 33 |",
    "`0.9.0-beta+26.1` | 25 | 32 |": "`0.9.0-beta+26.1` | 25 | 33 |",
    "`0.9.0-beta+26.2` | 25 | 32 |": "`0.9.0-beta+26.2` | 25 | 33 |",
    "**Serbe cyrillique (`sr_sp`)** et **Serbe latin (`sr_cs`)**.": "**Serbe cyrillique (`sr_sp`)**, **Serbe latin (`sr_cs`)** et **Catalan (`ca_es`)**.",
    "Les trente-deux langues sont disponibles": "Les trente-trois langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

sr_lat_block = """Pour le serbe latin :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
ca_block = sr_lat_block + """
Pour le catalan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le catalan :" not in text:
    if sr_lat_block not in text:
        raise RuntimeError("Serbian Latin coverage block not found")
    text = text.replace(sr_lat_block, ca_block, 1)

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
            # 22 coverage entries are present through Serbian Latin.
            if coverage.count(" · ") == 21:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_ca_common_*/lang/ca_es.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Catalan common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_ca_121/lang/ca_es.json",
    ASSETS / "neoorigins_26_1/lang/ca_es.json",
    ASSETS / "neoorigins_26_2/lang/ca_es.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Catalan target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/ca_es.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/ca_es.json").exists()
]
ca_121_files = 17 + len(addon_fallback_files)

sr_lat_jar = "- **serbe latin** : 27 fichiers fallback `sr_cs` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
ca_jar = sr_lat_jar + f"\n- **catalan** : {ca_121_files} fichiers fallback `ca_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **catalan** :" not in text:
    if sr_lat_jar not in text:
        raise RuntimeError("Serbian Latin JAR validation line not found")
    text = text.replace(sr_lat_jar, ca_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for ca_es / 0.9.0-beta ({ca_121_files} fallback files on 1.21.1)")
