#!/usr/bin/env python3
"""Generate Breton fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Breton")
source = source.replace("Norwegian", "Breton")
source = source.replace("norwegian_translation_cache.json", "breton_translation_cache.json")
source = source.replace("build/no-discovery", "build/br-discovery")
source = source.replace("no_no", "br_fr")
source = source.replace("neoorigins_no_", "neoorigins_br_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "br", True]')
# Use punctuation+digits separators so the translation service cannot lexicalize them.
source = source.replace(
    'SEPARATOR_RE = re.compile(r"\\n?ZXQSEP\\d{4}ZXQ\\n?")',
    'SEPARATOR_RE = re.compile(r"\\n?⟦\\s*\\d{4}\\s*⟧\\n?")',
)
source = source.replace(
    'f"\\nZXQSEP{index:04d}ZXQ\\n{value}"',
    'f"\\n⟦{index:04d}⟧\\n{value}"',
)
# Numbered printf placeholders may legitimately move with Breton syntax.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "breton_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_breton.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_breton.py"), "exec"), namespace)

# Protect formatting/printf/tag tokens with punctuation-digit sentinels. Tolerate
# whitespace and stripped delimiter glyphs, while the strict audit still checks all
# resulting placeholders after generation.
def breton_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟪{index:04d}⟫"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def breton_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟪\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟫"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟪{digits}⟫", token)
        if token not in text:
            bare = rf"(?<!\d){re.escape(digits)}(?!\d)"
            text, _ = re.subn(bare, lambda _m, t=token: t, text, count=1)
    return text

namespace["protect"] = breton_protect
namespace["restore"] = breton_restore

# Preserve project branding and pre-seed short/high-visibility wording.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Digeriñ krouer an Origin",
    "Mob Origin Creator": "Krouer Mob Origin",
    "Origin Architect": "Origin Architect",
    "Split": "Rannañ",
    "Elytra Boost": "Kreñvaat an adeskell",
    "Sonic Boom": "Tarzhadenn son",
    "Pack Bond": "Liamm ar bagad",
    "Speed Mining": "Mengleuziañ buan",
    "Camoflauge": "Kamouflage",
    "Pack Boost": "Kreñvaat ar bagad",
    "Max Mana Boost": "Kreñvaat ar mana uc'helañ",
    "Rage Counter.": "Konter kounnar.",
    "Rage Counter": "Konter kounnar",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
