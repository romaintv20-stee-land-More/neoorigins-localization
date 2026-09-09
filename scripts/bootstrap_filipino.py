#!/usr/bin/env python3
"""Generate Filipino fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Filipino")
source = source.replace("Norwegian", "Filipino")
source = source.replace("norwegian_translation_cache.json", "filipino_translation_cache.json")
source = source.replace("build/no-discovery", "build/fil-discovery")
source = source.replace("no_no", "fil_ph")
source = source.replace("neoorigins_no_", "neoorigins_fil_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "tl", True]')
# Numbered printf placeholders may legitimately move in Filipino word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "filipino_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_filipino.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_filipino.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Buksan ang Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Split": "Hatiin",
    "Elytra Boost": "Pampalakas ng Elytra",
    "Sonic Boom": "Sonic Boom",
    "Speed Mining": "Mabilis na Pagmimina",
    "Camoflauge": "Kamuflaha",
    "Max Mana Boost": "Pampataas ng Maksimum na Mana",
    "Rage Counter.": "Sukatan ng Galit.",
    "Rage Counter": "Sukatan ng Galit",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "Ang kaluluwa ni %1$s ay winasak ng %3$s ni %2$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
