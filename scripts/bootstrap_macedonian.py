#!/usr/bin/env python3
"""Generate Macedonian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Macedonian")
source = source.replace("Norwegian", "Macedonian")
source = source.replace("norwegian_translation_cache.json", "macedonian_translation_cache.json")
source = source.replace("build/no-discovery", "build/mk-discovery")
source = source.replace("no_no", "mk_mk")
source = source.replace("neoorigins_no_", "neoorigins_mk_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "mk", True]')
# Numbered printf placeholders may legitimately move in Macedonian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "macedonian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_macedonian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_macedonian.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def macedonian_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def macedonian_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = macedonian_protect
namespace["restore"] = macedonian_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Отвори го создавачот на Origin",
    "Mob Origin Creator": "Создавач на Mob Origin",
    "Split": "Поделба",
    "Elytra Boost": "Забрзување со Elytra",
    "Sonic Boom": "Звучен бум",
    "Pack Bond": "Врска со глутницата",
    "Speed Mining": "Брзо копање",
    "Camoflauge": "Камуфлажа",
    "Pack Boost": "Засилување на глутницата",
    "Max Mana Boost": "Зголемување на максималната мана",
    "Rage Counter.": "Бројач на бес.",
    "Rage Counter": "Бројач на бес",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Притисни %s за да менуваш меѓу наредбите повиканите суштества да седат, да те следат или да се телепортираат до тебе.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s беше изгорен до пепел од %2$s со помош на %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s беше прочистен од змејскиот оган на %2$s со помош на %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Душата на %1$s беше растргната од %3$s на %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s се соочи со божествениот суд на %3$s од %2$s",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
