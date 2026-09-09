#!/usr/bin/env python3
"""Generate Somali fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Somali")
source = source.replace("Norwegian", "Somali")
source = source.replace("norwegian_translation_cache.json", "somali_translation_cache.json")
source = source.replace("build/no-discovery", "build/so-discovery")
source = source.replace("no_no", "so_so")
source = source.replace("neoorigins_no_", "neoorigins_so_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "so", True]')
# Numbered printf placeholders may legitimately move in Somali word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "somali_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_somali.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_somali.py"), "exec"), namespace)

# Keep formatting, printf placeholders and resource identifiers intact.
def somali_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def somali_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = somali_protect
namespace["restore"] = somali_restore

# Preserve branded/product terminology and known fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Fur Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Origin Architect": "Origin Architect",
    "Split": "Qaybi",
    "Elytra Boost": "Dardargelinta Elytra",
    "Sonic Boom": "Qarax Sonic",
    "Pack Bond": "Xidhiidhka Kooxda",
    "Speed Mining": "Macdan-qodis Degdeg ah",
    "Camoflauge": "Isqarin",
    "Pack Boost": "Xoojinta Kooxda",
    "Max Mana Boost": "Xoojinta Mana ugu Badan",
    "Rage Counter.": "Tiriyaha Carada.",
    "Rage Counter": "Tiriyaha Carada",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Riix %s si aad ugu kala wareegto amarrada makhluuqaadka aad u yeertay inay fadhiistaan, ku raacaan, ama kuu soo teleport-gareeyaan.",
    "§5Void Warp:§r Press %s while holding an ender pearl to rip through the fabric of reality and teleport yourself directly where you're looking, up to 50 blocks away": "§5Void Warp:§r Riix %s adigoo haya ender pearl si aad xaqiiqada u dhex jebiso oo aad si toos ah ugu teleport-gareyso meesha aad eegayso, ilaa 50 block u jirta",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s waxaa si daran u gubay %2$s isagoo adeegsanaya %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s waxaa lagu nadiifiyey dabka masduulaaga ee %2$s iyadoo la adeegsanayo %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Nafta %1$s waxaa kala jeexay %3$s-ka %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s wuxuu wajahay xukunka rabbaaniga ah ee %3$s-ka %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
