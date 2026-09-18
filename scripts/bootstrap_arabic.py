#!/usr/bin/env python3
"""Generate Arabic fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Arabic")
source = source.replace("Norwegian", "Arabic")
source = source.replace("norwegian_translation_cache.json", "arabic_translation_cache.json")
source = source.replace("build/no-discovery", "build/ar-discovery")
source = source.replace("no_no", "ar_sa")
source = source.replace("neoorigins_no_", "neoorigins_ar_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ar", True]')
# Numbered printf placeholders may legitimately move in Arabic word order.
# Compare the same placeholder multiset, matching the strict audit behavior.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "arabic_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_arabic.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_arabic.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "فتح منشئ Origin",
    "Mob Origin Creator": "منشئ Origin للكائنات",
    "Split": "انقسام",
    "Elytra Boost": "تعزيز الإليترا",
    "Sonic Boom": "انفجار صوتي",
    "Pack Bond": "رابطة القطيع",
    "Speed Mining": "تعدين سريع",
    "Camoflauge": "تمويه",
    "Pack Boost": "تعزيز القطيع",
    "Max Mana Boost": "زيادة الحد الأقصى للمانا",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: منح مجموعة الغنائم",
    "Rage Counter.": "عداد الغضب.",
    "Rage Counter": "عداد الغضب",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
