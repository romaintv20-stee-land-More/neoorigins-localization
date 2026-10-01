#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 18 |": "`0.9.0-beta+1.21.1` | 21 | 19 |",
    "`0.9.0-beta+26.1` | 25 | 18 |": "`0.9.0-beta+26.1` | 25 | 19 |",
    "`0.9.0-beta+26.2` | 25 | 18 |": "`0.9.0-beta+26.2` | 25 | 19 |",
    "**Suédois (`sv_se`)** et **Danois (`da_dk`)**.": "**Suédois (`sv_se`)**, **Danois (`da_dk`)** et **Finnois (`fi_fi`)**.",
    "Les dix-huit langues sont disponibles": "Les dix-neuf langues sont disponibles",
    "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA | Couverture effective par langue |": "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI | Couverture effective par langue |",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

danish_block = """Pour le danois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
finnish_block = danish_block + """
Pour le finnois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le finnois :" not in text:
    if danish_block not in text:
        raise RuntimeError("Danish coverage block not found")
    text = text.replace(danish_block, finnish_block, 1)

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
            if coverage.count(" · ") == 7:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_fi_common_*/lang/fi_fi.json")))
if common_chunks == 0:
    raise RuntimeError("No Finnish common NeoOrigins chunks found")
for required in [
    ASSETS / "neoorigins_fi_121/lang/fi_fi.json",
    ASSETS / "neoorigins_26_1/lang/fi_fi.json",
    ASSETS / "neoorigins_26_2/lang/fi_fi.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Finnish target delta: {required}")

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
    path = ASSETS / namespace / "lang/fi_fi.json"
    if not path.exists():
        raise RuntimeError(f"Missing Finnish add-on localization: {path}")

jar_121 = common_chunks + 1 + len(addon_namespaces)
jar_26 = common_chunks + 1
da_jar = "- **danois** : 27 fichiers `da_dk` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
fi_jar = da_jar + f"\n- **finnois** : {jar_121} fichiers `fi_fi` dans le JAR 1.21.1 et {jar_26} dans chacun des JAR 26.x, avec les deltas de version corrects ;"
if "- **finnois** :" not in text:
    if da_jar not in text:
        raise RuntimeError("Danish JAR validation line not found")
    text = text.replace(da_jar, fi_jar, 1)

if "Finnois (`fi_fi`)" not in text or "| 19 |" not in text or "Pour le finnois :" not in text:
    raise RuntimeError("Finnish README update did not produce expected metadata")

README.write_text(text, encoding="utf-8")
print(f"README.md updated for fi_fi / 0.9.0-beta ({common_chunks} common chunks)")
