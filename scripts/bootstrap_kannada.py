#!/usr/bin/env python3
"""Generate Kannada fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Kannada")
source = source.replace("Norwegian", "Kannada")
source = source.replace("norwegian_translation_cache.json", "kannada_translation_cache.json")
source = source.replace("build/no-discovery", "build/kn-discovery")
source = source.replace("no_no", "kn_in")
source = source.replace("neoorigins_no_", "neoorigins_kn_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "kn", True]')
# Numbered printf placeholders may legitimately move in Kannada word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "kannada_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_kannada.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_kannada.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def kannada_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def kannada_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = kannada_protect
namespace["restore"] = kannada_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin Creator ತೆರೆಯಿರಿ",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "ವಿಭಜನೆ",
    "Elytra Boost": "Elytra ಬೂಸ್ಟ್",
    "Sonic Boom": "ಸೋನಿಕ್ ಬೂಮ್",
    "Pack Bond": "ಗುಂಪಿನ ಬಂಧ",
    "Speed Mining": "ವೇಗದ ಗಣಿಗಾರಿಕೆ",
    "Camoflauge": "ಮರೆವೇಷ",
    "Pack Boost": "ಗುಂಪಿನ ಬೂಸ್ಟ್",
    "Max Mana Boost": "ಗರಿಷ್ಠ ಮನಾ ಬೂಸ್ಟ್",
    "Rage Counter.": "ಕೋಪದ ಎಣಿಕೆ.",
    "Rage Counter": "ಕೋಪದ ಎಣಿಕೆ",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "ನೀವು ಕರೆಯಿಸಿದ ಜೀವಿಗಳಿಗೆ ಕುಳಿತುಕೊಳ್ಳಲು, ನಿಮ್ಮನ್ನು ಅನುಸರಿಸಲು ಅಥವಾ ನಿಮ್ಮ ಬಳಿಗೆ ಟೆಲಿಪೋರ್ಟ್ ಆಗಲು ಆದೇಶಗಳನ್ನು ಬದಲಾಯಿಸಲು %s ಒತ್ತಿರಿ.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%2$s ಅವರು %3$s ಬಳಸಿ %1$s ಅವರನ್ನು ಸುಟ್ಟು ಕರಕಲಿಸಿದರು",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%2$s ಅವರ ಡ್ರ್ಯಾಗನ್ ಬೆಂಕಿಯಿಂದ %3$s ಬಳಸಿ %1$s ಶುದ್ಧೀಕರಿಸಲ್ಪಟ್ಟರು",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%2$s ಅವರ %3$s ಮೂಲಕ %1$s ಅವರ ಆತ್ಮ ಚೂರುಚೂರಾಯಿತು",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s ಅವರು %2$s ಅವರ %3$s ನ ದೈವಿಕ ತೀರ್ಪನ್ನು ಎದುರಿಸಿದರು",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
