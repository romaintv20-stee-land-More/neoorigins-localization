#!/usr/bin/env python3
"""Generate Chuvash fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Chuvash")
source = source.replace("Norwegian", "Chuvash")
source = source.replace("norwegian_translation_cache.json", "chuvash_translation_cache.json")
source = source.replace("build/no-discovery", "build/cv-discovery")
source = source.replace("no_no", "cv_cu")
source = source.replace("neoorigins_no_", "neoorigins_cv_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "cv", True]')
# Numbered printf placeholders may legitimately move in Chuvash word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "chuvash_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_chuvash.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_chuvash.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def chuvash_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def chuvash_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = chuvash_protect
namespace["restore"] = chuvash_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin Creator уҫ",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Уйӑр",
    "Elytra Boost": "Элитра хӑвӑртлатни",
    "Sonic Boom": "Соник шартлаттарни",
    "Pack Bond": "Ушкӑн ҫыхӑнӑвӗ",
    "Speed Mining": "Хӑвӑрт чавни",
    "Camoflauge": "Маскировка",
    "Pack Boost": "Ушкӑн вӑйлантарни",
    "Max Mana Boost": "Мана максимумне вӑйлантарни",
    "Rage Counter.": "Тарӑху шутлавӗ.",
    "Rage Counter": "Тарӑху шутлавӗ",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Чӗр чунсене ларма, хыҫҫӑн пыма е сан патна телепортланма хушмаллине улӑштарма %s пус.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%2$s %3$s-па %1$s-а пӗтӗмпех ҫунтарса ячӗ",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%2$s %3$s-па хӑйӗн дракон вутӗпе %1$s-а тасатрӗ",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%2$s хӑйӗн %3$s-па %1$s чунне татса салатрӗ",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s %2$s хӑйӗн %3$s урлӑ панӑ турӑ судӗпе хирӗҫрӗ",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
