#!/usr/bin/env python3
"""Generate Afrikaans fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Afrikaans")
source = source.replace("Norwegian", "Afrikaans")
source = source.replace("norwegian_translation_cache.json", "afrikaans_translation_cache.json")
source = source.replace("build/no-discovery", "build/af-discovery")
source = source.replace("no_no", "af_za")
source = source.replace("neoorigins_no_", "neoorigins_af_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "af", True]')
# Numbered printf placeholders may legitimately move in Afrikaans word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "afrikaans_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_afrikaans.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_afrikaans.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def afrikaans_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def afrikaans_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = afrikaans_protect
namespace["restore"] = afrikaans_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Maak Origin Creator oop",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Verdeel",
    "Elytra Boost": "Elytra-hupstoot",
    "Sonic Boom": "Soniese knal",
    "Pack Bond": "Tropband",
    "Speed Mining": "Vinnige mynbou",
    "Camoflauge": "Kamoeflering",
    "Pack Boost": "Tropversterking",
    "Max Mana Boost": "Maksimum mana-versterking",
    "Rage Counter.": "Woedeteller.",
    "Rage Counter": "Woedeteller",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Druk %s om te wissel tussen opdragte aan jou opgeroepte wesens om te sit, jou te volg of na jou te teleporteer.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s is deur %2$s tot as verbrand met %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s is deur %2$s se draakvuur gesuiwer met %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s se siel is deur %2$s se %3$s uitmekaar geskeur",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s het die goddelike oordeel van %2$s se %3$s in die gesig gestaar",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
