#!/usr/bin/env python3
"""Generate Slovenian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Slovenian")
source = source.replace("Norwegian", "Slovenian")
source = source.replace("norwegian_translation_cache.json", "slovenian_translation_cache.json")
source = source.replace("build/no-discovery", "build/sl-discovery")
source = source.replace("no_no", "sl_si")
source = source.replace("neoorigins_no_", "neoorigins_sl_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "sl", True]')
# Numbered printf placeholders may legitimately move in Slovenian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "slovenian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_slovenian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_slovenian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Odpri ustvarjalnik Originov",
    "Mob Origin Creator": "Ustvarjalnik mob Originov",
    "Split": "Razdeli",
    "Elytra Boost": "Pospešek Elytre",
    "Sonic Boom": "Sonični udar",
    "Pack Bond": "Vez tropa",
    "Speed Mining": "Hitro rudarjenje",
    "Camoflauge": "Kamuflaža",
    "Pack Boost": "Okrepitev tropa",
    "Max Mana Boost": "Povečanje največje mane",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Dodeli zbirko plena",
    "Rage Counter.": "Števec besa.",
    "Rage Counter": "Števec besa",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
