#!/usr/bin/env python3
"""Generate Irish fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Irish")
source = source.replace("Norwegian", "Irish")
source = source.replace("norwegian_translation_cache.json", "irish_translation_cache.json")
source = source.replace("build/no-discovery", "build/ga-discovery")
source = source.replace("no_no", "ga_ie")
source = source.replace("neoorigins_no_", "neoorigins_ga_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ga", True]')
# Numbered printf placeholders may legitimately move in Irish word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "irish_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_irish.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_irish.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Oscail Cruthaitheoir Origin",
    "Mob Origin Creator": "Cruthaitheoir Mob Origin",
    "Split": "Scoilt",
    "Elytra Boost": "Treisiú Elytra",
    "Sonic Boom": "Pléasc Sonach",
    "Speed Mining": "Mianadóireacht Thapa",
    "Camoflauge": "Duaithníocht",
    "Max Mana Boost": "Treisiú Mana Uasta",
    "Rage Counter.": "Méadar Feirge.",
    "Rage Counter": "Méadar Feirge",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "Dódh %1$s go smidiríní ag %2$s agus %3$s á úsáid acu",
    "%1$s was purified by %2$s's dragonfire using %3$s": "Glanadh %1$s le tine dragain %2$s agus %3$s á úsáid acu",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Stróic %3$s %2$s anam %1$s as a chéile",
    "%1$s faced the divine judgment of %2$s's %3$s": "Thug %1$s aghaidh ar bhreithiúnas diaga %3$s %2$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
