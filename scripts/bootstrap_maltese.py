#!/usr/bin/env python3
"""Generate Maltese fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Maltese")
source = source.replace("Norwegian", "Maltese")
source = source.replace("norwegian_translation_cache.json", "maltese_translation_cache.json")
source = source.replace("build/no-discovery", "build/mt-discovery")
source = source.replace("no_no", "mt_mt")
source = source.replace("neoorigins_no_", "neoorigins_mt_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "mt", True]')
# Numbered printf placeholders may legitimately move in Maltese word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "maltese_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_maltese.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_maltese.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def maltese_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def maltese_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = maltese_protect
namespace["restore"] = maltese_restore

# Preserve canonical mod/product names and pre-seed fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Iftaħ Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Aqsam",
    "Elytra Boost": "Spinta tal-Elytra",
    "Sonic Boom": "Sonic Boom",
    "Pack Bond": "Rabta tal-Grupp",
    "Speed Mining": "Tħaffir Mgħaġġel",
    "Camoflauge": "Kamuflaġġ",
    "Pack Boost": "Tisħiħ tal-Grupp",
    "Max Mana Boost": "Tisħiħ Massimu tal-Mana",
    "Rage Counter.": "Kontatur tar-Rabja.",
    "Rage Counter": "Kontatur tar-Rabja",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Agħfas %s biex taqleb bejn li tordna lill-ħlejjaq imsejħa tiegħek joqogħdu, isegwuk, jew jittrasportaw ruħhom lejk.",
    "§5Void Warp:§r Press %s while holding an ender pearl to rip through the fabric of reality and teleport yourself directly where you're looking, up to 50 blocks away": "§5Void Warp:§r Agħfas %s waqt li żżomm ender pearl biex taqsam id-drapp tar-realtà u tittrasporta ruħek direttament fejn qed tħares, sa 50 blokka 'l bogħod",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s inħaraq għalkollox minn %2$s bl-użu ta' %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s ġie ppurifikat bin-nar tad-dragun ta' %2$s bl-użu ta' %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Ir-ruħ ta' %1$s ġiet imċarrta mill-%3$s ta' %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s iffaċċja l-ġudizzju divin tal-%3$s ta' %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
