#!/usr/bin/env python3
"""Generate Georgian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Georgian")
source = source.replace("Norwegian", "Georgian")
source = source.replace("norwegian_translation_cache.json", "georgian_translation_cache.json")
source = source.replace("build/no-discovery", "build/ka-discovery")
source = source.replace("no_no", "ka_ge")
source = source.replace("neoorigins_no_", "neoorigins_ka_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ka", True]')
# Numbered printf placeholders may legitimately move in Georgian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "georgian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_georgian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_georgian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin-ის შემქმნელის გახსნა",
    "Mob Origin Creator": "Mob Origin-ის შემქმნელი",
    "Split": "გაყოფა",
    "Elytra Boost": "Elytra აჩქარება",
    "Sonic Boom": "ხმოვანი აფეთქება",
    "Speed Mining": "სწრაფი მოპოვება",
    "Camoflauge": "კამუფლაჟი",
    "Max Mana Boost": "მაქსიმალური Mana-ის გაძლიერება",
    "Rage Counter.": "რისხვის მრიცხველი.",
    "Rage Counter": "რისხვის მრიცხველი",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s მთლიანად დაწვა %2$s-მა %3$s-ის გამოყენებით",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s განიწმინდა %2$s-ის დრაკონის ცეცხლით %3$s-ის გამოყენებით",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s-ის სული დაგლიჯა %2$s-ის %3$s-მა",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s შეხვდა %2$s-ის %3$s-ის ღვთიურ განაჩენს",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
