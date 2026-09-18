#!/usr/bin/env python3
"""Generate Azerbaijani fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Azerbaijani")
source = source.replace("Norwegian", "Azerbaijani")
source = source.replace("norwegian_translation_cache.json", "azerbaijani_translation_cache.json")
source = source.replace("build/no-discovery", "build/az-discovery")
source = source.replace("no_no", "az_az")
source = source.replace("neoorigins_no_", "neoorigins_az_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "az", True]')
# Numbered printf placeholders may legitimately move in Azerbaijani word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "azerbaijani_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_azerbaijani.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_azerbaijani.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without transliteration or accidental mutation.
def azerbaijani_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def azerbaijani_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = azerbaijani_protect
namespace["restore"] = azerbaijani_restore

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin Creator-i aç",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Böl",
    "Elytra Boost": "Elytra gücləndirməsi",
    "Sonic Boom": "Səs partlayışı",
    "Pack Bond": "Sürü bağı",
    "Speed Mining": "Sürətli qazma",
    "Camoflauge": "Kamuflyaj",
    "Pack Boost": "Sürü gücləndirməsi",
    "Max Mana Boost": "Maksimum mana gücləndirməsi",
    "Rage Counter.": "Qəzəb sayğacı.",
    "Rage Counter": "Qəzəb sayğacı",
    "Origin Architect": "Origin Architect",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "%s düyməsinə basaraq çağırdıqlarına oturmaq, səni izləmək və ya yanına teleport olmaq əmrləri arasında keçid et.",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s, %2$s tərəfindən %3$s istifadə edilərək külə döndərildi",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s, %2$s-in əjdaha alovu ilə %3$s istifadə edilərək təmizləndi",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s-in ruhu %2$s-in %3$s-i tərəfindən parçalandı",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s, %2$s-in %3$s-i ilə ilahi hökmə məruz qaldı",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
