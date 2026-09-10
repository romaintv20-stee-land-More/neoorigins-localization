#!/usr/bin/env python3
"""Generate Lao fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Lao")
source = source.replace("Norwegian", "Lao")
source = source.replace("norwegian_translation_cache.json", "lao_translation_cache.json")
source = source.replace("build/no-discovery", "build/lo-discovery")
source = source.replace("no_no", "lo_la")
source = source.replace("neoorigins_no_", "neoorigins_lo_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "lo", True]')
# Numbered printf placeholders may legitimately move in Lao word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "lao_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_lao.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_lao.py"), "exec"), namespace)

# Use punctuation/digit-only sentinels so printf, formatting and tag tokens survive
# translation without accidental mutation by the translation service.
def lao_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟦{index:04d}⟧"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def lao_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟦\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟧"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟦{digits}⟧", token)
    return text

namespace["protect"] = lao_protect
namespace["restore"] = lao_restore

# Preserve project branding and pre-seed short/fragile strings. Strict audits
# still validate placeholders and coverage after generation.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "ເປີດຕົວສ້າງ Origin",
    "Mob Origin Creator": "ຕົວສ້າງ Mob Origin",
    "Origin Architect": "Origin Architect",
    "Split": "ແບ່ງ",
    "Elytra Boost": "ເພີ່ມພະລັງ Elytra",
    "Sonic Boom": "ຄື້ນສຽງລະເບີດ",
    "Pack Bond": "ສາຍສຳພັນຝູງ",
    "Speed Mining": "ຂຸດໄວ",
    "Camoflauge": "ພາງຕົວ",
    "Pack Boost": "ເສີມພະລັງຝູງ",
    "Max Mana Boost": "ເພີ່ມ Mana ສູງສຸດ",
    "Rage Counter.": "ຕົວນັບຄວາມໂກດ.",
    "Rage Counter": "ຕົວນັບຄວາມໂກດ",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s ຖືກ %2$s ເຜົາຈົນໄໝ້ເກຣຍມດ້ວຍ %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s ຖືກຊຳລະໂດຍໄຟມັງກອນຂອງ %2$s ດ້ວຍ %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "ວິນຍານຂອງ %1$s ຖືກ %3$s ຂອງ %2$s ສີກຂາດ",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s ປະເຊີນກັບການພິພາກສາອັນສັກສິດຈາກ %3$s ຂອງ %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
