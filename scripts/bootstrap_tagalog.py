#!/usr/bin/env python3
"""Generate Tagalog fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Tagalog")
source = source.replace("Norwegian", "Tagalog")
source = source.replace("norwegian_translation_cache.json", "tagalog_translation_cache.json")
source = source.replace("build/no-discovery", "build/tl-discovery")
source = source.replace("no_no", "tl_ph")
source = source.replace("neoorigins_no_", "neoorigins_tl_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "tl", True]')
# Numbered printf placeholders may legitimately move in Tagalog word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "tagalog_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_tagalog.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_tagalog.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation by the translation service.
def tagalog_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def tagalog_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = tagalog_protect
namespace["restore"] = tagalog_restore

# Preserve project branding and pre-seed a few fragile/title-like strings.
# Strict audits still validate every placeholder after generation.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Buksan ang Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Origin Architect": "Origin Architect",
    "Split": "Hatiin",
    "Elytra Boost": "Pagpapabilis ng Elytra",
    "Sonic Boom": "Sonikong Pagsabog",
    "Pack Bond": "Ugnayan ng Grupo",
    "Speed Mining": "Mabilis na Pagmimina",
    "Camoflauge": "Pagbabalatkayo",
    "Pack Boost": "Pagpapalakas ng Grupo",
    "Max Mana Boost": "Pagpapalakas ng Pinakamataas na Mana",
    "Rage Counter.": "Tagabilang ng Galit.",
    "Rage Counter": "Tagabilang ng Galit",
    "%1$s was burnt to a crisp by %2$s using %3$s": "Sinunog ni %2$s si %1$s gamit ang %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "Nilinis si %1$s ng apoy ng dragon ni %2$s gamit ang %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Winasak ang kaluluwa ni %1$s ng %3$s ni %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "Hinarap ni %1$s ang banal na paghatol ng %3$s ni %2$s",
    "§5Void Warp:§r Press %s while holding an ender pearl to rip through the fabric of reality and teleport yourself directly where you're looking, up to 50 blocks away": "§5Void Warp:§r Pindutin ang %s habang may hawak na ender pearl upang punitin ang tela ng realidad at direktang mag-teleport sa tinitingnan mo, hanggang 50 bloke ang layo",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
