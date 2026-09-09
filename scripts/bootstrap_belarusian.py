#!/usr/bin/env python3
"""Generate Belarusian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Belarusian")
source = source.replace("Norwegian", "Belarusian")
source = source.replace("norwegian_translation_cache.json", "belarusian_translation_cache.json")
source = source.replace("build/no-discovery", "build/be-discovery")
source = source.replace("no_no", "be_by")
source = source.replace("neoorigins_no_", "neoorigins_be_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "be", True]')
# Numbered printf placeholders may legitimately move in Belarusian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "belarusian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_belarusian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_belarusian.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def belarusian_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def belarusian_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = belarusian_protect
namespace["restore"] = belarusian_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Адкрыць стваральнік Origin",
    "Mob Origin Creator": "Стваральнік Mob Origin",
    "Split": "Падзел",
    "Elytra Boost": "Паскарэнне з элітрамі",
    "Sonic Boom": "Гукавы выбух",
    "Pack Bond": "Сувязь са зграяй",
    "Speed Mining": "Хуткае капанне",
    "Camoflauge": "Камуфляж",
    "Pack Boost": "Узмацненне зграі",
    "Max Mana Boost": "Павелічэнне максімальнай маны",
    "Rage Counter.": "Лічыльнік лютасці.",
    "Rage Counter": "Лічыльнік лютасці",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Націсніце %s, каб пераключацца паміж загадамі выкліканым істотам сядзець, ісці за вамі або тэлепартавацца да вас.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s быў спалены дашчэнту %2$s з дапамогай %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s быў ачышчаны драконавым агнём %2$s з дапамогай %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Душа %1$s была разарвана %3$s ад %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s паўстаў перад боскім судом %3$s ад %2$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
