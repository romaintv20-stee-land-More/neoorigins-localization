#!/usr/bin/env python3
"""Generate Luxembourgish fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Luxembourgish")
source = source.replace("Norwegian", "Luxembourgish")
source = source.replace("norwegian_translation_cache.json", "luxembourgish_translation_cache.json")
source = source.replace("build/no-discovery", "build/lb-discovery")
source = source.replace("no_no", "lb_lu")
source = source.replace("neoorigins_no_", "neoorigins_lb_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "lb", True]')
# Numbered printf placeholders may legitimately move in Luxembourgish word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "luxembourgish_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_luxembourgish.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_luxembourgish.py"), "exec"), namespace)

# Keep formatting, printf placeholders and resource identifiers intact.
def luxembourgish_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def luxembourgish_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = luxembourgish_protect
namespace["restore"] = luxembourgish_restore

# Preserve branded/product terminology and known fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin Creator opmaachen",
    "Mob Origin Creator": "Mob Origin Creator",
    "Origin Architect": "Origin Architect",
    "Split": "Deelen",
    "Elytra Boost": "Elytra-Boost",
    "Sonic Boom": "Sonic Boom",
    "Pack Bond": "Gruppverbindung",
    "Speed Mining": "Séiere Biergbau",
    "Camoflauge": "Tarnung",
    "Pack Boost": "Grupp-Boost",
    "Max Mana Boost": "Max-Mana-Boost",
    "Rage Counter.": "Roserei-Zieler.",
    "Rage Counter": "Roserei-Zieler",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Dréck %s fir tëscht de Befehler ze wiesselen, datt deng geruff Wiesen sëtzen, dir nogoen oder sech bei dech teleportéieren.",
    "§5Void Warp:§r Press %s while holding an ender pearl to rip through the fabric of reality and teleport yourself directly where you're looking, up to 50 blocks away": "§5Void Warp:§r Dréck %s wärend s du eng Enderperel an der Hand hues, fir duerch d'Realitéit ze briechen an dech direkt dohinner ze teleportéieren, wou s du hikucks, bis zu 50 Bléck wäit",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s gouf vu %2$s mat %3$s knusprech verbrannt",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s gouf duerch d'Draachefeier vu %2$s mat %3$s gereinegt",
    "%1$s had their soul ripped apart by %2$s's %3$s": "D'Séil vu %1$s gouf duerch %2$s säi %3$s ausernee gerappt",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s huet sech dem gëttleche Geriicht vu %2$s sengem %3$s gestallt",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
