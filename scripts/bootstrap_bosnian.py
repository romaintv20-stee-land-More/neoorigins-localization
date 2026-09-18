#!/usr/bin/env python3
"""Generate Bosnian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Bosnian")
source = source.replace("Norwegian", "Bosnian")
source = source.replace("norwegian_translation_cache.json", "bosnian_translation_cache.json")
source = source.replace("build/no-discovery", "build/bs-discovery")
source = source.replace("no_no", "bs_ba")
source = source.replace("neoorigins_no_", "neoorigins_bs_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "bs", True]')
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "bosnian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_bosnian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_bosnian.py"), "exec"), namespace)

# Protect formatting/printf/tag tokens with punctuation-digit sentinels.
def bosnian_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def bosnian_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = bosnian_protect
namespace["restore"] = bosnian_restore

# Preserve branding and pre-seed fragile/high-visibility strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Otvori kreator Origina",
    "Mob Origin Creator": "Kreator Mob Origina",
    "Origin Architect": "Origin Architect",
    "Split": "Podjela",
    "Elytra Boost": "Pojačanje Elytre",
    "Sonic Boom": "Zvučni udar",
    "Pack Bond": "Veza čopora",
    "Speed Mining": "Brzo kopanje",
    "Camoflauge": "Kamuflaža",
    "Pack Boost": "Pojačanje čopora",
    "Max Mana Boost": "Povećanje maksimalne mane",
    "Rage Counter.": "Brojač bijesa.",
    "Rage Counter": "Brojač bijesa",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s je spaljen do pepela od strane %2$s koristeći %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s je pročišćen zmajevom vatrom igrača %2$s koristeći %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s je ostao bez duše zbog %3$s igrača %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s se suočio s božanskim sudom %3$s igrača %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
