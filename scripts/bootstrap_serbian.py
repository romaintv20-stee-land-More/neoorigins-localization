#!/usr/bin/env python3
"""Generate Serbian Cyrillic fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Serbian Cyrillic")
source = source.replace("Norwegian", "Serbian")
source = source.replace("norwegian_translation_cache.json", "serbian_translation_cache.json")
source = source.replace("build/no-discovery", "build/sr-discovery")
source = source.replace("no_no", "sr_sp")
source = source.replace("neoorigins_no_", "neoorigins_sr_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "sr", True]')
# Numbered printf placeholders may legitimately move in Serbian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "serbian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_serbian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_serbian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Отвори креатор порекла",
    "Mob Origin Creator": "Креатор порекла моба",
    "Split": "Подели",
    "Elytra Boost": "Појачање елитре",
    "Sonic Boom": "Звучни удар",
    "Pack Bond": "Веза чопора",
    "Speed Mining": "Брзо рударење",
    "Camoflauge": "Камуфлажа",
    "Pack Boost": "Појачање чопора",
    "Max Mana Boost": "Повећање максималне мане",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Додели скуп плена",
    "Rage Counter.": "Бројач беса.",
    "Rage Counter": "Бројач беса",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
