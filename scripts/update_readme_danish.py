#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
text = README.read_text(encoding="utf-8")

replacements = {
    "`0.8.0-beta+1.21.1` | 21 | 17 |": "`0.9.0-beta+1.21.1` | 21 | 18 |",
    "`0.8.0-beta+26.1` | 25 | 17 |": "`0.9.0-beta+26.1` | 25 | 18 |",
    "`0.8.0-beta+26.2` | 25 | 17 |": "`0.9.0-beta+26.2` | 25 | 18 |",
    "La **0.8.0 Beta** prend en charge :": "La **0.9.0 Beta** prend en charge :",
    "**Indonésien (`id_id`)** et **Suédois (`sv_se`)**.": "**Indonésien (`id_id`)**, **Suédois (`sv_se`)** et **Danois (`da_dk`)**.",
    "Les dix-sept langues sont disponibles": "Les dix-huit langues sont disponibles",
    "La couverture de la 0.8.0 est auditée": "La couverture de la 0.9.0 est auditée",
    "## Validation des JAR 0.8.0": "## Validation des JAR 0.9.0",
    "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV | Couverture effective par langue |": "| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA | Couverture effective par langue |",
}
for old, new in replacements.items():
    if old not in text:
        raise RuntimeError(f"README anchor not found: {old}")
    text = text.replace(old, new, 1)

swedish_block = """Pour le suédois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
dan_block = swedish_block + """
Pour le danois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.
"""
if "Pour le danois :" not in text:
    if swedish_block not in text:
        raise RuntimeError("Swedish coverage block not found")
    text = text.replace(swedish_block, dan_block, 1)

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
            # cells: empty, project, ref, per-language coverage, effective, empty
            if len(parts) < 6:
                raise RuntimeError(f"Unexpected project row: {line}")
            coverage = parts[3].strip()
            if coverage.count(" · ") == 6:
                parts[3] = f" {coverage} · {count} "
                lines[i] = "|".join(parts)
            break
text = "\n".join(lines) + "\n"

sv_jar = "- **suédois** : 27 fichiers `sv_se` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
da_jar = sv_jar + "\n- **danois** : 27 fichiers `da_dk` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;"
if "- **danois** :" not in text:
    if sv_jar not in text:
        raise RuntimeError("Swedish JAR validation line not found")
    text = text.replace(sv_jar, da_jar, 1)

if "Danois (`da_dk`)" not in text or "| 18 |" not in text:
    raise RuntimeError("Danish README update did not produce expected metadata")

README.write_text(text, encoding="utf-8")
print("README.md updated for da_dk / 0.9.0-beta")
