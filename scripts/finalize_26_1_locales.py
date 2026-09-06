#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
README = ROOT / "README.md"
TEST_PLAN = ROOT / "docs/TEST_PLAN.md"

NEW_LOCALES = ("it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")

catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

build261 = catalog["project"]["builds"]["26.1.x"]
build261["version"] = "0.7.0-beta+26.1"
# The platform/build line was validated previously on 26.1.2, but the new
# 0.7.0 language expansion still needs a fresh in-game spot check.
build261["in_game_tested"] = False

neo = next(p for p in catalog["supported_projects"] if p["id"] == "neoorigins")
for code in NEW_LOCALES:
    lang = neo["languages"][code]
    lang["targets"] = ["1.21.1", "26.1.x"]
    lang["note"] = (
        "Couverture de fallback auditée pour Minecraft 1.21.1 et 26.1.x contre NeoOrigins ; "
        "les traductions officielles amont gardent la priorité."
    )

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

readme = README.read_text(encoding="utf-8")
readme = readme.replace(
    "| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.6.0-beta+26.1` | 25 | 5 | NeoOrigins uniquement |",
    "| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.7.0-beta+26.1` | 25 | 10 | NeoOrigins uniquement |",
)
readme = readme.replace(
    "Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. Minecraft 26.1.2 et 26.2 ont déjà été validés en jeu avec NeoOrigins Localization ; l'intégration 0.7.0 de Minecraft 1.21.1 doit encore recevoir sa validation finale en jeu après build.",
    "Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. La base Minecraft 26.1.2 et Minecraft 26.2 ont déjà été validées en jeu avec NeoOrigins Localization ; les nouvelles langues de la 0.7.0 sur 26.1.x doivent encore recevoir un contrôle visuel en jeu.",
)
readme = readme.replace(
    "Les cinq nouvelles langues de 0.7.0 sont actuellement limitées au build 1.21.1. Les branches 26.x restent sur les cinq langues de 0.6.0 jusqu'à leur extension dédiée.",
    "Les cinq nouvelles langues de 0.7.0 sont disponibles sur les builds 1.21.1 et 26.1.x. Minecraft 26.2 reste provisoirement sur les cinq langues de 0.6.0 jusqu'à son port dédié.",
)
README.write_text(readme, encoding="utf-8")

test_plan = TEST_PLAN.read_text(encoding="utf-8")
test_plan = test_plan.replace(
    "| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement | Validé en jeu sur 26.1.2 |",
    "| Minecraft 26.1.x | 25 | 2.2.25 | NeoOrigins uniquement, 10 langues en 0.7.0 | Base validée en jeu sur 26.1.2 ; nouvelles langues à contrôler visuellement |",
)
if "## Langues 26.1.x" not in test_plan:
    marker = "## Medieval Origins Revival — 1.21.1"
    section = (
        "## Langues 26.1.x\n\n"
        "Le build `0.7.0-beta+26.1` doit proposer les mêmes dix langues NeoOrigins que la 1.21.1 : "
        "`fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. "
        "Les cinq nouvelles langues sont auditées contre NeoOrigins `v2.2.25`. Vérifier en jeu au minimum l'écran de sélection, "
        "un nom d'Origin et une description longue dans plusieurs de ces langues. Les add-ons 1.21.1 doivent rester absents du JAR 26.1.x.\n\n"
    )
    test_plan = test_plan.replace(marker, section + marker)
TEST_PLAN.write_text(test_plan, encoding="utf-8")

# Regenerate the readable catalog from catalog.json.
namespace = {"__name__": "__main__", "__file__": str(ROOT / "scripts/generate_catalog.py")}
exec(compile((ROOT / "scripts/generate_catalog.py").read_text(encoding="utf-8"), str(ROOT / "scripts/generate_catalog.py"), "exec"), namespace)

print("26.1.x 0.7.0 metadata/docs finalized.")
