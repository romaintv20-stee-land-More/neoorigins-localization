#!/usr/bin/env python3
"""Generate Kazakh fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Kazakh")
source = source.replace("Norwegian", "Kazakh")
source = source.replace("norwegian_translation_cache.json", "kazakh_translation_cache.json")
source = source.replace("build/no-discovery", "build/kk-discovery")
source = source.replace("no_no", "kk_kz")
source = source.replace("neoorigins_no_", "neoorigins_kk_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "kk", True]')
# Numbered printf placeholders may legitimately move in Kazakh word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "kazakh_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_kazakh.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_kazakh.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin жасаушысын ашу",
    "Mob Origin Creator": "Mob Origin жасаушысы",
    "Split": "Бөлу",
    "Elytra Boost": "Elytra үдеуі",
    "Sonic Boom": "Дыбыстық жарылыс",
    "Speed Mining": "Жылдам қазу",
    "Camoflauge": "Камуфляж",
    "Max Mana Boost": "Максималды Mana күшейтуі",
    "Rage Counter.": "Ашу есептегіші.",
    "Rage Counter": "Ашу есептегіші",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s ойыншысын %2$s %3$s қолданып күлге айналдырды",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s ойыншысын %2$s-ның айдаһар оты %3$s көмегімен тазартты",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s ойыншысының жанын %2$s-ның %3$s қаруы жұлып алды",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s ойыншысы %2$s-ның %3$s арқылы құдайлық үкіміне тап болды",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
