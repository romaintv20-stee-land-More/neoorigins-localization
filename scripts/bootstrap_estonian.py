#!/usr/bin/env python3
"""Generate Estonian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Estonian")
source = source.replace("Norwegian", "Estonian")
source = source.replace("norwegian_translation_cache.json", "estonian_translation_cache.json")
source = source.replace("build/no-discovery", "build/et-discovery")
source = source.replace("no_no", "et_ee")
source = source.replace("neoorigins_no_", "neoorigins_et_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "et", True]')
# Numbered printf placeholders may legitimately move in Estonian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "estonian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_estonian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_estonian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Ava päritolu looja",
    "Mob Origin Creator": "Olendipäritolu looja",
    "Split": "Jaga",
    "Elytra Boost": "Elytra kiirendus",
    "Sonic Boom": "Helipauk",
    "Pack Bond": "Karjaside",
    "Speed Mining": "Kiirkaevandamine",
    "Camoflauge": "Kamuflaaž",
    "Pack Boost": "Karjakiirendus",
    "Max Mana Boost": "Maksimaalse mana suurendus",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: anna saagikogum",
    "Rage Counter.": "Raevuloendur.",
    "Rage Counter": "Raevuloendur",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s hing rebiti lõhki %2$s-i %3$s poolt",
}

# Pre-seed targeted wording so the translation service cannot drop/reorder semantic
# actors in fragile strings. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
