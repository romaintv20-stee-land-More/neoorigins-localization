#!/usr/bin/env python3
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.json"
README = ROOT / "README.md"
TEST_PLAN = ROOT / "docs/TEST_PLAN.md"
NEW_LOCALES = ("it_it", "pl_pl", "ru_ru", "tr_tr", "zh_cn")

catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

build262 = catalog["project"]["builds"]["26.2"]
build262["version"] = "0.7.0-beta+26.2"
build262["in_game_tested"] = False

neo = next(p for p in catalog["supported_projects"] if p["id"] == "neoorigins")
for code in NEW_LOCALES:
    lang = neo["languages"][code]
    targets = list(lang.get("targets", []))
    for target in ("1.21.1", "26.1.x", "26.2"):
        if target not in targets:
            targets.append(target)
    lang["targets"] = targets
    if code == "tr_tr":
        lang["note"] = (
            "Couverture complète sur 1.21.1, 26.1.x et 26.2. NeoOrigins 26.2 ne fournit pas de tr_tr : "
            "le fallback existant couvre 2 278 clés et le delta 26.2 ajoute les 14 nouvelles clés, soit 2 292/2 292."
        )
    else:
        lang["note"] = (
            "Couverture auditée sur 1.21.1, 26.1.x et 26.2. Sur 26.2, NeoOrigins fournit 2 172/2 292 clés "
            "officielles ; notre delta basse priorité couvre uniquement les 120 clés absentes."
        )

compat = neo.get("compatibility", {})
compat["note"] = (
    "Les builds 26.x n'embarquent que la localisation NeoOrigins. Minecraft 26.2 utilise un delta dédié. "
    "La base 26.2 a déjà été validée en jeu ; l'extension 0.7.0 des cinq nouvelles langues doit encore recevoir un contrôle visuel."
)

CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

readme = README.read_text(encoding="utf-8")
readme = readme.replace(
    "| Minecraft 26.2 | `0.6.0-beta+26.2` | 25 | 5 | NeoOrigins uniquement + delta 26.2 |",
    "| Minecraft 26.2 | `0.7.0-beta+26.2` | 25 | 10 | NeoOrigins uniquement + delta 26.2 |",
)
readme = readme.replace(
    "Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. La base Minecraft 26.1.2 et Minecraft 26.2 ont déjà été validées en jeu avec NeoOrigins Localization ; les nouvelles langues de la 0.7.0 sur 26.1.x doivent encore recevoir un contrôle visuel en jeu.",
    "Les builds 26.x n'embarquent pas les traductions des add-ons 1.21.1. Les bases Minecraft 26.1.2 et 26.2 ont déjà été validées en jeu avec NeoOrigins Localization ; les cinq langues ajoutées en 0.7.0 sur les branches 26.x doivent encore recevoir un contrôle visuel en jeu.",
)
readme = readme.replace(
    "Les cinq nouvelles langues de 0.7.0 sont disponibles sur les builds 1.21.1 et 26.1.x. Minecraft 26.2 reste provisoirement sur les cinq langues de 0.6.0 jusqu'à son port dédié.",
    "Les dix langues de la 0.7.0 sont maintenant disponibles sur les trois builds : 1.21.1, 26.1.x et 26.2.",
)
readme = readme.replace(
    "NeoOrigins 2.2.25 est requis. Pour les langues déjà traduites officiellement par NeoOrigins, le fallback ne conserve que les clés absentes en amont. Le néerlandais est fourni intégralement par NeoOrigins Localization. La cible 26.2 utilise un delta dédié pour ses clés supplémentaires.",
    "NeoOrigins 2.2.25 est requis. Pour les langues déjà traduites officiellement par NeoOrigins, le fallback ne conserve que les clés absentes en amont. Le néerlandais est fourni intégralement par NeoOrigins Localization. Sur 26.2, l'italien, le polonais, le russe et le chinois simplifié disposent chacun de 2 172 clés officielles ; notre delta couvre uniquement les 120 clés manquantes. Le turc n'a pas de traduction officielle 26.2 : son fallback complet couvre les 2 292 clés grâce aux 14 entrées supplémentaires du delta 26.2.",
)
README.write_text(readme, encoding="utf-8")

test_plan = TEST_PLAN.read_text(encoding="utf-8")
test_plan = test_plan.replace(
    "| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2 | Validé en jeu |",
    "| Minecraft 26.2 | 25 | 2.2.25 | NeoOrigins uniquement + delta 26.2, 10 langues en 0.7.0 | Base validée en jeu ; nouvelles langues à contrôler visuellement |",
)
test_plan = test_plan.replace(
    "## Minecraft 26.2\n\nVérifier que le delta `neoorigins_26_2` est chargé sur 26.2 et absent des builds plus anciens. Le chargement et la localisation ont déjà été validés en jeu sur 26.2.",
    "## Langues Minecraft 26.2\n\nLe build `0.7.0-beta+26.2` doit proposer `fr_fr`, `de_de`, `es_es`, `pt_br`, `nl_nl`, `it_it`, `pl_pl`, `ru_ru`, `tr_tr` et `zh_cn`. Vérifier que le delta `neoorigins_26_2` est chargé sur 26.2 et absent des builds plus anciens. Pour `it_it`, `pl_pl`, `ru_ru` et `zh_cn`, les traductions officielles 26.2 restent prioritaires et notre fallback ne doit fournir que les 120 clés absentes. Pour `tr_tr`, vérifier que les namespaces `neoorigins_tr_*` et le delta de 14 clés couvrent ensemble les 2 292 clés. La base 26.2 a déjà été validée en jeu ; faire un contrôle visuel des nouvelles langues de la 0.7.0.",
)
test_plan = test_plan.replace(
    "- les namespaces d'expansion 1.21.1 `assets/neoorigins_121_batch1/**` et `assets/neoorigins_tr_*/**`.",
    "\nLes JAR 26.x doivent toujours exclure les add-ons ci-dessus. Pour les ressources NeoOrigins spécifiques : le JAR 26.1.x inclut `neoorigins_121_batch1/**` et `neoorigins_tr_*/**` mais exclut `neoorigins_26_2/**` ; le JAR 26.2 exclut `neoorigins_121_batch1/**`, inclut `neoorigins_tr_*/**` pour le turc et inclut `neoorigins_26_2/**` pour son delta dédié.",
)
TEST_PLAN.write_text(test_plan, encoding="utf-8")

# Regenerate the readable catalog from catalog.json.
namespace = {"__name__": "__main__", "__file__": str(ROOT / "scripts/generate_catalog.py")}
exec(compile((ROOT / "scripts/generate_catalog.py").read_text(encoding="utf-8"), str(ROOT / "scripts/generate_catalog.py"), "exec"), namespace)

# Remove all one-off preparation material before the PR is merged.
for path in (
    ROOT / "scripts/prepare_26_2_locales.py",
    ROOT / "scripts/apply_26_2_translations.py",
):
    if path.exists():
        path.unlink()
shutil.rmtree(ROOT / "tmp/26_2_translation_needed", ignore_errors=True)

print("Minecraft 26.2 0.7.0 metadata finalized and temporary preparation files removed.")
