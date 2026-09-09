#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 39 |": "`0.9.0-beta+1.21.1` | 21 | 40 |",
    "`0.9.0-beta+26.1` | 25 | 39 |": "`0.9.0-beta+26.1` | 25 | 40 |",
    "`0.9.0-beta+26.2` | 25 | 39 |": "`0.9.0-beta+26.2` | 25 | 40 |",
    "**Galicien (`gl_es`)** et **Hindi (`hi_in`)**.": "**Galicien (`gl_es`)**, **Hindi (`hi_in`)** et **Norvégien nynorsk (`nn_no`)**.",
    "Les trente-neuf langues sont disponibles": "Les quarante langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

hi_block = """Pour le hindi :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
nn_block = hi_block + """
Pour le norvégien nynorsk :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le norvégien nynorsk :" not in text:
    if hi_block not in text:
        raise RuntimeError("Hindi coverage block not found")
    text = text.replace(hi_block, nn_block, 1)

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
            if coverage.count(" · ") == 28:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_nn_common_*/lang/nn_no.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Nynorsk common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_nn_121/lang/nn_no.json",
    ASSETS / "neoorigins_26_1/lang/nn_no.json",
    ASSETS / "neoorigins_26_2/lang/nn_no.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Nynorsk target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/nn_no.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/nn_no.json").exists()
]
nn_121_files = 17 + len(addon_fallback_files)

hi_jar_prefix = "- **hindi** :"
nn_jar = f"- **norvégien nynorsk** : {nn_121_files} fichiers fallback `nn_no` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **norvégien nynorsk** :" not in text:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(hi_jar_prefix):
            lines.insert(i + 1, nn_jar)
            break
    else:
        raise RuntimeError("Hindi JAR validation line not found")
    text = "\n".join(lines) + "\n"

README.write_text(text, encoding="utf-8")
print(f"README.md updated for nn_no / 0.9.0-beta ({nn_121_files} fallback files on 1.21.1)")
