#!/usr/bin/env python3
"""Generate Albanian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Albanian")
source = source.replace("Norwegian", "Albanian")
source = source.replace("norwegian_translation_cache.json", "albanian_translation_cache.json")
source = source.replace("build/no-discovery", "build/sq-discovery")
source = source.replace("no_no", "sq_al")
source = source.replace("neoorigins_no_", "neoorigins_sq_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "sq", True]')
# Numbered printf placeholders may legitimately move in Albanian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "albanian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_albanian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_albanian.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without accidental mutation by the translation service.
def albanian_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def albanian_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = albanian_protect
namespace["restore"] = albanian_restore

# Preserve project branding and pre-seed short/fragile strings. Strict audits
# still validate placeholders and coverage after generation.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Hap Krijuesin e Origin",
    "Mob Origin Creator": "Krijuesi i Mob Origin",
    "Origin Architect": "Origin Architect",
    "Split": "Ndaj",
    "Elytra Boost": "Përforcim Elytra",
    "Sonic Boom": "Shpërthim sonik",
    "Pack Bond": "Lidhja e tufës",
    "Speed Mining": "Nxjerrje e shpejtë",
    "Camoflauge": "Kamuflazh",
    "Pack Boost": "Përforcim i tufës",
    "Max Mana Boost": "Përforcim maksimal i Mana-s",
    "Rage Counter.": "Matësi i tërbimit.",
    "Rage Counter": "Matësi i tërbimit",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s u dogj plotësisht nga %2$s duke përdorur %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s u pastrua nga zjarri i dragoit të %2$s duke përdorur %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s iu copëtua shpirti nga %3$s i %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s u përball me gjykimin hyjnor të %3$s të %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
