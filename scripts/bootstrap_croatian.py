#!/usr/bin/env python3
"""Generate Croatian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Croatian")
source = source.replace("Norwegian", "Croatian")
source = source.replace("norwegian_translation_cache.json", "croatian_translation_cache.json")
source = source.replace("build/no-discovery", "build/hr-discovery")
source = source.replace("no_no", "hr_hr")
source = source.replace("neoorigins_no_", "neoorigins_hr_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "hr", True]')
# Numbered printf placeholders may legitimately move in Croatian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "croatian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_croatian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_croatian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Otvori kreator Origina",
    "Mob Origin Creator": "Kreator mob Origina",
    "Split": "Podijeli",
    "Elytra Boost": "Pojačanje Elytre",
    "Sonic Boom": "Zvučni udar",
    "Pack Bond": "Veza čopora",
    "Speed Mining": "Brzo rudarenje",
    "Camoflauge": "Kamuflaža",
    "Pack Boost": "Pojačanje čopora",
    "Max Mana Boost": "Povećanje maksimalne mane",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Dodijeli skup plijena",
    "Rage Counter.": "Brojač bijesa.",
    "Rage Counter": "Brojač bijesa",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
