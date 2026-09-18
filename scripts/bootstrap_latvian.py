#!/usr/bin/env python3
"""Generate Latvian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Latvian")
source = source.replace("Norwegian", "Latvian")
source = source.replace("norwegian_translation_cache.json", "latvian_translation_cache.json")
source = source.replace("build/no-discovery", "build/lv-discovery")
source = source.replace("no_no", "lv_lv")
source = source.replace("neoorigins_no_", "neoorigins_lv_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "lv", True]')
# Numbered printf placeholders may legitimately move in Latvian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "latvian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_latvian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_latvian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Atvērt izcelsmes veidotāju",
    "Mob Origin Creator": "Mobu izcelsmes veidotājs",
    "Split": "Sadalīt",
    "Elytra Boost": "Elytra paātrinājums",
    "Sonic Boom": "Skaņas trieciens",
    "Pack Bond": "Bara saikne",
    "Speed Mining": "Ātra rakšana",
    "Camoflauge": "Maskēšanās",
    "Pack Boost": "Bara pastiprinājums",
    "Max Mana Boost": "Maksimālās manas palielinājums",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: piešķirt laupījuma fondu",
    "Rage Counter.": "Dusmu skaitītājs.",
    "Rage Counter": "Dusmu skaitītājs",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s dvēseli saplosīja %2$s %3$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
