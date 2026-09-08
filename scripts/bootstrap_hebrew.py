#!/usr/bin/env python3
"""Generate Hebrew fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Hebrew")
source = source.replace("Norwegian", "Hebrew")
source = source.replace("norwegian_translation_cache.json", "hebrew_translation_cache.json")
source = source.replace("build/no-discovery", "build/he-discovery")
source = source.replace("no_no", "he_il")
source = source.replace("neoorigins_no_", "neoorigins_he_")
# Google Translate's internal web RPC uses the legacy language code "iw" for Hebrew.
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "iw", True]')
# Numbered printf placeholders may legitimately move in Hebrew word order.
# Compare the same placeholder multiset, matching the strict audit behavior.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "hebrew_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_hebrew.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_hebrew.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "פתיחת יוצר Origin",
    "Mob Origin Creator": "יוצר Origin ליצורים",
    "Split": "פיצול",
    "Elytra Boost": "חיזוק אלייטרה",
    "Sonic Boom": "בום קולי",
    "Pack Bond": "קשר הלהקה",
    "Speed Mining": "כרייה מהירה",
    "Camoflauge": "הסוואה",
    "Pack Boost": "חיזוק הלהקה",
    "Max Mana Boost": "הגדלת המאנה המרבית",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: הענקת מאגר שלל",
    "Rage Counter.": "מד זעם.",
    "Rage Counter": "מד זעם",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
