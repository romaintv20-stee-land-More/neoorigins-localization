#!/usr/bin/env python3
"""Generate Bashkir fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Bashkir")
source = source.replace("Norwegian", "Bashkir")
source = source.replace("norwegian_translation_cache.json", "bashkir_translation_cache.json")
source = source.replace("build/no-discovery", "build/ba-discovery")
source = source.replace("no_no", "ba_ru")
source = source.replace("neoorigins_no_", "neoorigins_ba_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ba", True]')
# Google may translate alphabetic separator sentinels for Bashkir. Use a punctuation+digits
# marker instead, with optional spaces tolerated by the splitter.
source = source.replace(
    'SEPARATOR_RE = re.compile(r"\\n?ZXQSEP\\d{4}ZXQ\\n?")',
    'SEPARATOR_RE = re.compile(r"\\n?⟦\\s*\\d{4}\\s*⟧\\n?")',
)
source = source.replace(
    'f"\\nZXQSEP{index:04d}ZXQ\\n{value}"',
    'f"\\n⟦{index:04d}⟧\\n{value}"',
)
# Numbered printf placeholders may legitimately move in Bashkir word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "bashkir_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_bashkir.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_bashkir.py"), "exec"), namespace)

# Bashkir translation transliterates Latin placeholder masks. A punctuation+digits mask
# remains stable; restoration tolerates spaces inserted around the digits.
def bashkir_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟪{index:04d}⟫"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def bashkir_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟪\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟫"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟪{digits}⟫", token)
    return text

namespace["protect"] = bashkir_protect
namespace["restore"] = bashkir_restore

# Preserve branded/project terminology and known fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin булдырыусыны асыу",
    "Mob Origin Creator": "Mob Origin булдырыусы",
    "Origin Architect": "Origin Architect",
    "Split": "Бүлеү",
    "Elytra Boost": "Elytra көсәйтеүе",
    "Sonic Boom": "Тауыш тулҡыны",
    "Pack Bond": "Төркөм бәйләнеше",
    "Speed Mining": "Тиҙ ҡаҙыу",
    "Camoflauge": "Камуфляж",
    "Pack Boost": "Төркөм көсәйтеүе",
    "Max Mana Boost": "Максималь Mana көсәйтеүе",
    "Rage Counter.": "Ярһыу иҫәпләгесе.",
    "Rage Counter": "Ярһыу иҫәпләгесе",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s уйынсыһын %2$s %3$s ҡулланып көлгә әйләндерҙе",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s уйынсыһын %2$s уйынсыһының аждаһа уты %3$s ярҙамында таҙартты",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s уйынсыһының йәнен %2$s уйынсыһының %3$s ҡоралы тартып алды",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s уйынсыһы %2$s уйынсыһының %3$s аша илаһи хөкөмгә дусар булды",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
