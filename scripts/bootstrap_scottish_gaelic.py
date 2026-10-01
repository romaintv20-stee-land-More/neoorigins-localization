#!/usr/bin/env python3
"""Generate Scottish Gaelic fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Scottish Gaelic")
source = source.replace("Norwegian", "Scottish Gaelic")
source = source.replace("norwegian_translation_cache.json", "scottish_gaelic_translation_cache.json")
source = source.replace("build/no-discovery", "build/gd-discovery")
source = source.replace("no_no", "gd_gb")
source = source.replace("neoorigins_no_", "neoorigins_gd_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "gd", True]')
# Numbered printf placeholders may legitimately move in Scottish Gaelic word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "scottish_gaelic_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_scottish_gaelic.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_scottish_gaelic.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Fosgail Cruthadair Origin",
    "Mob Origin Creator": "Cruthadair Mob Origin",
    "Split": "Sgar",
    "Elytra Boost": "Brosnachadh Elytra",
    "Sonic Boom": "Spreadhadh Sonach",
    "Speed Mining": "Mèinnearachd Luath",
    "Camoflauge": "Breug-riochd",
    "Max Mana Boost": "Brosnachadh Mana as Àirde",
    "Rage Counter.": "Cunntair Feirge.",
    "Rage Counter": "Cunntair Feirge",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "Chaidh %1$s a losgadh gu luaithre le %2$s a' cleachdadh %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "Chaidh %1$s a ghlanadh le teine dràgon %2$s a' cleachdadh %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Chaidh anam %1$s a reubadh às a chèile le %3$s aig %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "Thug %1$s aghaidh air breitheanas diadhaidh %3$s aig %2$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
