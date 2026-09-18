#!/usr/bin/env python3
"""Generate Tamil fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Tamil")
source = source.replace("Norwegian", "Tamil")
source = source.replace("norwegian_translation_cache.json", "tamil_translation_cache.json")
source = source.replace("build/no-discovery", "build/ta-discovery")
source = source.replace("no_no", "ta_in")
source = source.replace("neoorigins_no_", "neoorigins_ta_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ta", True]')
# Numbered printf placeholders may legitimately move in Tamil word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "tamil_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_tamil.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_tamil.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation by the translation service.
def tamil_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def tamil_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = tamil_protect
namespace["restore"] = tamil_restore

# Preserve project branding and pre-seed strings whose numbered placeholders are
# especially fragile under machine translation. Strict audits still validate them.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin உருவாக்கியைத் திற",
    "Mob Origin Creator": "Mob Origin உருவாக்கி",
    "Origin Architect": "Origin Architect",
    "Split": "பிரி",
    "Elytra Boost": "Elytra வேக உயர்வு",
    "Sonic Boom": "ஒலி வெடிப்பு",
    "Pack Bond": "கூட்டப் பிணைப்பு",
    "Speed Mining": "வேக சுரங்கத் தோண்டல்",
    "Camoflauge": "மறைவேடம்",
    "Pack Boost": "கூட்ட வலுப்படுத்தல்",
    "Max Mana Boost": "அதிகபட்ச Mana வலுப்படுத்தல்",
    "Rage Counter.": "கோப எண்ணி.",
    "Rage Counter": "கோப எண்ணி",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%2$s, %3$s-ஐ பயன்படுத்தி %1$s-ஐ கருகச் செய்தார்",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%2$s-ன் டிராகன் நெருப்பால் %3$s பயன்படுத்தி %1$s தூய்மைப்படுத்தப்பட்டார்",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%2$s-ன் %3$s மூலம் %1$s-ன் ஆன்மா பிளந்தெடுக்கப்பட்டது",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s, %2$s-ன் %3$s வழங்கிய தெய்வீகத் தீர்ப்பை எதிர்கொண்டார்",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
