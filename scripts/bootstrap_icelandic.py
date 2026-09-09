#!/usr/bin/env python3
"""Generate Icelandic fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Icelandic")
source = source.replace("Norwegian", "Icelandic")
source = source.replace("norwegian_translation_cache.json", "icelandic_translation_cache.json")
source = source.replace("build/no-discovery", "build/is-discovery")
source = source.replace("no_no", "is_is")
source = source.replace("neoorigins_no_", "neoorigins_is_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "is", True]')
# Numbered printf placeholders may legitimately move in Icelandic word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "icelandic_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_icelandic.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_icelandic.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Split": "Skipta",
    "Elytra Boost": "Elytra-aukning",
    "Sonic Boom": "Hljóðsprenging",
    "Speed Mining": "Hraðnám",
    "Camoflauge": "Felulitur",
    "Max Mana Boost": "Hámarks mana-aukning",
    "Rage Counter.": "Reiðimælir.",
    "Rage Counter": "Reiðimælir",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s fékk sál sína rifna í sundur af %3$s hjá %2$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
