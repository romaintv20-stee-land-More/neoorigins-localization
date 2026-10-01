#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 19 |": "`0.9.0-beta+1.21.1` | 21 | 20 |",
    "`0.9.0-beta+26.1` | 25 | 19 |": "`0.9.0-beta+26.1` | 25 | 20 |",
    "`0.9.0-beta+26.2` | 25 | 19 |": "`0.9.0-beta+26.2` | 25 | 20 |",
    "**Danois (`da_dk`)** et **Finnois (`fi_fi`)**.": "**Danois (`da_dk`)**, **Finnois (`fi_fi`)** et **Norvégien bokmål (`no_no`)**.",
    "Les dix-neuf langues sont disponibles": "Les vingt langues sont disponibles",
    "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI | Couverture effective par langue |": "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO | Couverture effective par langue |",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

finnish_block = """Pour le finnois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
norwegian_block = finnish_block + """
Pour le norvégien bokmål :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le norvégien bokmål :" not in text:
    if finnish_block not in text:
        raise RuntimeError("Finnish coverage block not found")
    text = text.replace(finnish_block, norwegian_block, 1)

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
            if len(parts) < 6:
                raise RuntimeError(f"Unexpected project row: {line}")
            coverage = parts[3].strip()
            if coverage.count(" · ") == 8:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_no_common_*/lang/no_no.json")))
if common_chunks == 0:
    raise RuntimeError("No Norwegian common NeoOrigins chunks found")
for required in [
    ASSETS / "neoorigins_no_121/lang/no_no.json",
    ASSETS / "neoorigins_26_1/lang/no_no.json",
    ASSETS / "neoorigins_26_2/lang/no_no.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Norwegian target delta: {required}")

addon_namespaces = [
    "medievalorigins",
    "ibarnorigins",
    "origins_fantasy",
    "origins_backgrounds",
    "origins_backgrounds_two",
    "origins_backgrounds_iss",
    "origins_furries",
    "origins_classes_ex",
    "origins_classes_iss",
    "originsmodernui",
]
for namespace in addon_namespaces:
    path = ASSETS / namespace / "lang/no_no.json"
    if not path.exists():
        raise RuntimeError(f"Missing Norwegian add-on localization: {path}")

jar_121 = common_chunks + 1 + len(addon_namespaces)
jar_26 = common_chunks + 1
fi_jar = "- **finnois** : 27 fichiers `fi_fi` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
no_jar = fi_jar + f"\n- **norvégien bokmål** : {jar_121} fichiers `no_no` dans le JAR 1.21.1 et {jar_26} dans chacun des JAR 26.x, avec les deltas de version corrects ;"
if "- **norvégien bokmål** :" not in text:
    if fi_jar not in text:
        raise RuntimeError("Finnish JAR validation line not found")
    text = text.replace(fi_jar, no_jar, 1)

if "Norvégien bokmål (`no_no`)" not in text or "| 20 |" not in text or "Pour le norvégien bokmål :" not in text:
    raise RuntimeError("Norwegian README update did not produce expected metadata")

README.write_text(text, encoding="utf-8")
print(f"README.md updated for no_no / 0.9.0-beta ({common_chunks} common chunks)")
