#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 21 |": "`0.9.0-beta+1.21.1` | 21 | 22 |",
    "`0.9.0-beta+26.1` | 25 | 21 |": "`0.9.0-beta+26.1` | 25 | 22 |",
    "`0.9.0-beta+26.2` | 25 | 21 |": "`0.9.0-beta+26.2` | 25 | 22 |",
    "**Norvégien bokmål (`no_no`)** et **Roumain (`ro_ro`)**.": "**Norvégien bokmål (`no_no`)**, **Roumain (`ro_ro`)** et **Grec (`el_gr`)**.",
    "Les vingt et une langues sont disponibles": "Les vingt-deux langues sont disponibles",
    "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO": "Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

ro_block = """Pour le roumain :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
el_block = ro_block + """
Pour le grec :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le grec :" not in text:
    if ro_block not in text:
        raise RuntimeError("Romanian coverage block not found")
    text = text.replace(ro_block, el_block, 1)

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
            if coverage.count(" · ") == 10:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_el_common_*/lang/el_gr.json")))
if common_chunks != 16:
    raise RuntimeError(f"Expected 16 Greek common chunks, found {common_chunks}")
for required in [
    ASSETS / "neoorigins_el_121/lang/el_gr.json",
    ASSETS / "neoorigins_26_1/lang/el_gr.json",
    ASSETS / "neoorigins_26_2/lang/el_gr.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Greek target delta: {required}")
addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss", "originsmodernui",
]
for namespace in addon_namespaces:
    path = ASSETS / namespace / "lang/el_gr.json"
    if not path.exists():
        raise RuntimeError(f"Missing Greek add-on localization: {path}")

ro_jar = "- **roumain** : 26 fichiers fallback `ro_ro` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x ; Origin Architect fournit séparément ses 22/22 chaînes roumaines officielles ;"
el_jar = ro_jar + "\n- **grec** : 27 fichiers `el_gr` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
if "- **grec** :" not in text:
    if ro_jar not in text:
        raise RuntimeError("Romanian JAR validation line not found")
    text = text.replace(ro_jar, el_jar, 1)

README.write_text(text, encoding="utf-8")
print("README.md updated for el_gr / 0.9.0-beta")
