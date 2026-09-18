#!/usr/bin/env python3
"""Generate Faroese fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Faroese")
source = source.replace("Norwegian", "Faroese")
source = source.replace("norwegian_translation_cache.json", "faroese_translation_cache.json")
source = source.replace("build/no-discovery", "build/fo-discovery")
source = source.replace("no_no", "fo_fo")
source = source.replace("neoorigins_no_", "neoorigins_fo_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "fo", True]')
# Numbered printf placeholders may legitimately move in Faroese word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "faroese_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_faroese.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_faroese.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def faroese_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def faroese_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = faroese_protect
namespace["restore"] = faroese_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Opna Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Být",
    "Elytra Boost": "Elytra-skund",
    "Sonic Boom": "Ljóðbrestur",
    "Pack Bond": "Flokssamband",
    "Speed Mining": "Skjót graving",
    "Camoflauge": "Kamuflasja",
    "Pack Boost": "Flokksstyrking",
    "Max Mana Boost": "Øking av mesta mana",
    "Rage Counter.": "Vreiðiteljari.",
    "Rage Counter": "Vreiðiteljari",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Trýst á %s fyri at skifta millum at geva teimum, tú hevur kallað fram, boð um at sita, fylgja tær ella teleportera til tín.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s varð brendur upp av %2$s við %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s varð reinsaður av drekaeldinum hjá %2$s við %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Sálin hjá %1$s varð skrædd sundur av %3$s hjá %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s møtti guddómliga dóminum hjá %2$s við %3$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
