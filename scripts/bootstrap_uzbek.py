#!/usr/bin/env python3
"""Generate Uzbek fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Uzbek")
source = source.replace("Norwegian", "Uzbek")
source = source.replace("norwegian_translation_cache.json", "uzbek_translation_cache.json")
source = source.replace("build/no-discovery", "build/uz-discovery")
source = source.replace("no_no", "uz_uz")
source = source.replace("neoorigins_no_", "neoorigins_uz_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "uz", True]')
# Numbered printf placeholders may legitimately move in Uzbek word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "uzbek_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_uzbek.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_uzbek.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def uzbek_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def uzbek_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = uzbek_protect
namespace["restore"] = uzbek_restore

# Preserve canonical mod/product names and pre-seed fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin Creator'ni ochish",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Ajratish",
    "Elytra Boost": "Elytra kuchaytirishi",
    "Sonic Boom": "Sonic Boom",
    "Pack Bond": "To'da rishtasi",
    "Speed Mining": "Tez qazish",
    "Camoflauge": "Kamuflyaj",
    "Pack Boost": "To'da kuchaytirishi",
    "Max Mana Boost": "Maksimal mana kuchaytirishi",
    "Rage Counter.": "G'azab hisoblagichi.",
    "Rage Counter": "G'azab hisoblagichi",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Chaqirilgan mavjudotlaringizga o'tirish, ergashish yoki yoningizga teleport bo'lish buyrug'ini almashtirish uchun %s ni bosing.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s %2$s tomonidan %3$s yordamida kul qilib kuydirildi",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s %2$s ning ajdarho olovi bilan %3$s yordamida poklandi",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s ning ruhi %2$s ning %3$s si tomonidan parchalandi",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s %2$s ning %3$s si orqali ilohiy hukmga duch keldi",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
