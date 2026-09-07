#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

# README
p = ROOT / "README.md"
s = p.read_text(encoding="utf-8")
s = s.replace("| 21 | 12 |", "| 21 | 13 |")
s = s.replace("| 25 | 12 |", "| 25 | 13 |")
s = s.replace("**Hongrois (`hu_hu`)**.", "**Hongrois (`hu_hu`)** et **Japonais (`ja_jp`)**.")
s = s.replace("Les douze langues sont disponibles", "Les treize langues sont disponibles")
s = s.replace("| Projet | Version/référence | Couverture CS / HU | Couverture effective par langue |", "| Projet | Version/référence | Couverture CS / HU / JA | Couverture effective par langue |")
rows = {
    "Medieval Origins Revival": "401/401 · 401/401 · 401/401",
    "ibarn's quartet origins addon": "69/69 · 69/69 · 69/69",
    "Origins Fantasy for NeoOrigins": "240/240 · 240/240 · 240/240",
    "Origins: Backgrounds for NeoOrigins": "65/65 · 65/65 · 65/65",
    "Origins: More Backgrounds for NeoOrigins": "44/44 · 44/44 · 44/44",
    "Origins: Backgrounds ISS for NeoOrigins": "79/79 · 79/79 · 79/79",
    "Origins Furries for NeoOrigins": "117/117 · 117/117 · 117/117",
    "Origins: Classes Extended for NeoOrigins": "124/124 · 124/124 · 124/124",
    "Origins: Classes ISS for NeoOrigins": "99/99 · 99/99 · 99/99",
    "Origin Architect": "22/22 · 22/22 · 22/22",
}
lines = s.splitlines()
for i, line in enumerate(lines):
    for name, cov in rows.items():
        if line.startswith(f"| {name} |"):
            parts = line.split("|")
            if len(parts) >= 6:
                parts[3] = f" {cov} "
                lines[i] = "|".join(parts)
            break
s = "\n".join(lines) + "\n"
p.write_text(s, encoding="utf-8")

# CATALOG.md
p = ROOT / "CATALOG.md"
s = p.read_text(encoding="utf-8")
needle = " · Magyar (`hu_hu`)"
if "日本語 (`ja_jp`)" not in s:
    s = s.replace(needle, needle + " · 日本語 (`ja_jp`)")
s = s.replace("Les douze langues ciblées sont : `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn`, `cs_cz` et `hu_hu`.",
              "Les treize langues ciblées sont : `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr`, `zh_cn`, `cs_cz`, `hu_hu` et `ja_jp`.")
p.write_text(s, encoding="utf-8")

# catalog.json
p = ROOT / "catalog.json"
data = json.loads(p.read_text(encoding="utf-8"))
data["project"]["supported_locale_count"] = 13
for project in data.get("supported_projects", []):
    langs = project.setdefault("languages", {})
    if "ja_jp" not in langs:
        if project.get("id") == "neoorigins":
            langs["ja_jp"] = {
                "name": "日本語",
                "status": "supported",
                "targets": ["1.21.1", "26.1.x", "26.2"]
            }
        else:
            namespace = project.get("namespace") or project.get("id")
            langs["ja_jp"] = {
                "name": "日本語",
                "status": "supported",
                "file": f"src/main/resources/resourcepacks/fallback_localizations/assets/{namespace}/lang/ja_jp.json"
            }
    comp = project.get("compatibility")
    if isinstance(comp, dict) and isinstance(comp.get("note"), str):
        comp["note"] = comp["note"].replace("douze langues", "treize langues")
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("README.md, CATALOG.md and catalog.json finalized for ja_jp / 13 locales")
