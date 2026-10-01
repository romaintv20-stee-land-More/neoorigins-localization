#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.9.0-beta+1.21.1` | 21 | 20 |": "`0.9.0-beta+1.21.1` | 21 | 21 |",
    "`0.9.0-beta+26.1` | 25 | 20 |": "`0.9.0-beta+26.1` | 25 | 21 |",
    "`0.9.0-beta+26.2` | 25 | 20 |": "`0.9.0-beta+26.2` | 25 | 21 |",
    "**Finnois (`fi_fi`)** et **Norvégien bokmål (`no_no`)**.": "**Finnois (`fi_fi`)**, **Norvégien bokmål (`no_no`)** et **Roumain (`ro_ro`)**.",
    "Les vingt langues sont disponibles": "Les vingt et une langues sont disponibles",
    "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO | Couverture effective par langue |": "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO | Couverture effective par langue |",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

no_block = """Pour le norvégien bokmål :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
ro_block = no_block + """
Pour le roumain :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le roumain :" not in text:
    if no_block not in text:
        raise RuntimeError("Norwegian coverage block not found")
    text = text.replace(no_block, ro_block, 1)

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
    "Origin Architect": "22/22 (officiel)",
}
lines = text.splitlines()
for i, line in enumerate(lines):
    for project, count in addon_counts.items():
        if line.startswith(f"| {project} |"):
            parts = line.split("|")
            if len(parts) < 6:
                raise RuntimeError(f"Unexpected project row: {line}")
            coverage = parts[3].strip()
            if coverage.count(" · ") == 9:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

common_chunks = len(list(ASSETS.glob("neoorigins_ro_common_*/lang/ro_ro.json")))
if common_chunks == 0:
    raise RuntimeError("No Romanian common NeoOrigins chunks found")
for required in [
    ASSETS / "neoorigins_ro_121/lang/ro_ro.json",
    ASSETS / "neoorigins_26_1/lang/ro_ro.json",
    ASSETS / "neoorigins_26_2/lang/ro_ro.json",
]:
    if not required.exists():
        raise RuntimeError(f"Missing Romanian target delta: {required}")

# Nine add-ons need our Romanian fallback. Origin Architect already ships 22/22
# Romanian strings officially, so its ro_ro file must stay absent from our JAR.
fallback_addon_namespaces = [
    "medievalorigins", "ibarnorigins", "origins_fantasy", "origins_backgrounds",
    "origins_backgrounds_two", "origins_backgrounds_iss", "origins_furries",
    "origins_classes_ex", "origins_classes_iss",
]
for namespace in fallback_addon_namespaces:
    path = ASSETS / namespace / "lang/ro_ro.json"
    if not path.exists():
        raise RuntimeError(f"Missing Romanian add-on localization: {path}")
oa_path = ASSETS / "originsmodernui/lang/ro_ro.json"
if oa_path.exists():
    raise RuntimeError("Origin Architect Romanian fallback must be absent because upstream already provides 22/22")

jar_121 = common_chunks + 1 + len(fallback_addon_namespaces)
jar_26 = common_chunks + 1
no_jar = "- **norvégien bokmål** : 27 fichiers `no_no` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
ro_jar = no_jar + f"\n- **roumain** : {jar_121} fichiers fallback `ro_ro` dans le JAR 1.21.1 et {jar_26} dans chacun des JAR 26.x ; Origin Architect fournit séparément ses 22/22 chaînes roumaines officielles ;"
if "- **roumain** :" not in text:
    if no_jar not in text:
        raise RuntimeError("Norwegian JAR validation line not found")
    text = text.replace(no_jar, ro_jar, 1)

if "Roumain (`ro_ro`)" not in text or "| 21 |" not in text or "Pour le roumain :" not in text:
    raise RuntimeError("Romanian README update did not produce expected metadata")

README.write_text(text, encoding="utf-8")
print(f"README.md updated for ro_ro / 0.9.0-beta ({common_chunks} common chunks; Origin Architect official upstream)")
