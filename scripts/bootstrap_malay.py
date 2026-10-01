#!/usr/bin/env python3
"""Generate Malay fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Malay")
source = source.replace("Norwegian", "Malay")
source = source.replace("norwegian_translation_cache.json", "malay_translation_cache.json")
source = source.replace("build/no-discovery", "build/ms-discovery")
source = source.replace("no_no", "ms_my")
source = source.replace("neoorigins_no_", "neoorigins_ms_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ms", True]')
# Numbered printf placeholders may legitimately move in Malay word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "malay_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_malay.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_malay.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Split": "Pisah",
    "Elytra Boost": "Rangsangan Elytra",
    "Sonic Boom": "Letupan Sonik",
    "Speed Mining": "Perlombongan Pantas",
    "Camoflauge": "Penyamaran",
    "Max Mana Boost": "Peningkatan Mana Maksimum",
    "Rage Counter.": "Pengira Amarah.",
    "Rage Counter": "Pengira Amarah",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s telah direnggut jiwanya oleh %3$s milik %2$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
