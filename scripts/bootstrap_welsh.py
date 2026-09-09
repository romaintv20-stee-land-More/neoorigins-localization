#!/usr/bin/env python3
"""Generate Welsh fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Welsh")
source = source.replace("Norwegian", "Welsh")
source = source.replace("norwegian_translation_cache.json", "welsh_translation_cache.json")
source = source.replace("build/no-discovery", "build/cy-discovery")
source = source.replace("no_no", "cy_gb")
source = source.replace("neoorigins_no_", "neoorigins_cy_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "cy", True]')
# Numbered printf placeholders may legitimately move in Welsh word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "welsh_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_welsh.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_welsh.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Agor Crëwr Origin",
    "Mob Origin Creator": "Crëwr Mob Origin",
    "Split": "Rhannu",
    "Elytra Boost": "Hwb Elytra",
    "Sonic Boom": "Ffrwydrad Sonig",
    "Speed Mining": "Cloddio Cyflym",
    "Camoflauge": "Cuddliw",
    "Max Mana Boost": "Hwb Mana Uchaf",
    "Rage Counter.": "Mesurydd Cynddaredd.",
    "Rage Counter": "Mesurydd Cynddaredd",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "Llosgwyd %1$s yn ulw gan %2$s gan ddefnyddio %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "Purwyd %1$s gan dân draig %2$s gan ddefnyddio %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Rhwygwyd enaid %1$s yn ddarnau gan %3$s %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "Wynebodd %1$s farn ddwyfol %3$s %2$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
