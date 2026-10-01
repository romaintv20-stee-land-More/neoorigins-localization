#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 26 |": "`0.9.0-beta+1.21.1` | 21 | 27 |",
    "`0.9.0-beta+26.1` | 25 | 26 |": "`0.9.0-beta+26.1` | 25 | 27 |",
    "`0.9.0-beta+26.2` | 25 | 26 |": "`0.9.0-beta+26.2` | 25 | 27 |",
    "**Vietnamien (`vi_vn`)**, **Arabe (`ar_sa`)** et **Hébreu (`he_il`)**.": "**Vietnamien (`vi_vn`)**, **Arabe (`ar_sa`)**, **Hébreu (`he_il`)** et **Thaï (`th_th`)**.",
    "Les vingt-six langues sont disponibles": "Les vingt-sept langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

he_block = """Pour l'hébreu :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
th_block = he_block + """
Pour le thaï :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le thaï :" not in text:
    if he_block not in text:
        raise RuntimeError("Hebrew coverage block not found")
    text = text.replace(he_block, th_block, 1)

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
            if coverage.count(" · ") == 15:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_th_common_*/lang/th_th.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Thai common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_th_121/lang/th_th.json",
    ASSETS / "neoorigins_26_1/lang/th_th.json",
    ASSETS / "neoorigins_26_2/lang/th_th.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Thai target delta: {required}")

addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
addon_fallback_files = [
    ASSETS / namespace / "lang/th_th.json" for namespace in addon_namespaces
    if (ASSETS / namespace / "lang/th_th.json").exists()
]
th_121_files = 17 + len(addon_fallback_files)

hebrew_jar = "- **hébreu** : 27 fichiers fallback `he_il` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
thai_jar = hebrew_jar + f"\n- **thaï** : {th_121_files} fichiers fallback `th_th` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;"
if "- **thaï** :" not in text:
    if hebrew_jar not in text:
        raise RuntimeError("Hebrew JAR validation line not found")
    text = text.replace(hebrew_jar, thai_jar, 1)

README.write_text(text, encoding="utf-8")
print(f"README.md updated for th_th / 0.9.0-beta ({th_121_files} fallback files on 1.21.1)")
