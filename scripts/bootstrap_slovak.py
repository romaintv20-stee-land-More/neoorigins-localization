#!/usr/bin/env python3
"""Generate Slovak fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Slovak")
source = source.replace("Norwegian", "Slovak")
source = source.replace("norwegian_translation_cache.json", "slovak_translation_cache.json")
source = source.replace("build/no-discovery", "build/sk-discovery")
source = source.replace("no_no", "sk_sk")
source = source.replace("neoorigins_no_", "neoorigins_sk_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "sk", True]')
# Numbered printf placeholders may legitimately move in Slovak word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "slovak_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_slovak.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_slovak.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Otvoriť tvorcu Originov",
    "Mob Origin Creator": "Tvorca mob Originov",
    "Split": "Rozdeliť",
    "Elytra Boost": "Zrýchlenie Elytry",
    "Sonic Boom": "Sonický výbuch",
    "Pack Bond": "Puto svorky",
    "Speed Mining": "Rýchla ťažba",
    "Camoflauge": "Kamufláž",
    "Pack Boost": "Posilnenie svorky",
    "Max Mana Boost": "Zvýšenie maximálnej many",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Udeliť loot pool",
    "Rage Counter.": "Počítadlo zúrivosti.",
    "Rage Counter": "Počítadlo zúrivosti",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
