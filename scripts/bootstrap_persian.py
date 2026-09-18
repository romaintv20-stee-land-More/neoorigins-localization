#!/usr/bin/env python3
"""Generate Persian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Persian")
source = source.replace("Norwegian", "Persian")
source = source.replace("norwegian_translation_cache.json", "persian_translation_cache.json")
source = source.replace("build/no-discovery", "build/fa-discovery")
source = source.replace("no_no", "fa_ir")
source = source.replace("neoorigins_no_", "neoorigins_fa_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "fa", True]')
# Numbered printf placeholders may legitimately move in Persian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "persian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_persian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_persian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "باز کردن سازنده اوریجین",
    "Mob Origin Creator": "سازنده اوریجین موب",
    "Split": "تقسیم",
    "Elytra Boost": "تقویت الایترا",
    "Sonic Boom": "انفجار صوتی",
    "Pack Bond": "پیوند گله",
    "Speed Mining": "استخراج سریع",
    "Camoflauge": "استتار",
    "Pack Boost": "تقویت گله",
    "Max Mana Boost": "افزایش حداکثر مانا",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: اعطای مجموعه لوت",
    "Rage Counter.": "شمارنده خشم.",
    "Rage Counter": "شمارنده خشم",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s روحش به‌دست %3$sِ %2$s از هم دریده شد",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
