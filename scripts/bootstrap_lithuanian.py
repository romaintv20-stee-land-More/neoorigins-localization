#!/usr/bin/env python3
"""Generate Lithuanian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Lithuanian")
source = source.replace("Norwegian", "Lithuanian")
source = source.replace("norwegian_translation_cache.json", "lithuanian_translation_cache.json")
source = source.replace("build/no-discovery", "build/lt-discovery")
source = source.replace("no_no", "lt_lt")
source = source.replace("neoorigins_no_", "neoorigins_lt_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "lt", True]')
# Numbered printf placeholders may legitimately move in Lithuanian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "lithuanian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_lithuanian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_lithuanian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Atidaryti kilmės kūrėją",
    "Mob Origin Creator": "Mobų kilmės kūrėjas",
    "Split": "Padalyti",
    "Elytra Boost": "Elytros pagreitis",
    "Sonic Boom": "Garsinis smūgis",
    "Pack Bond": "Gaujos ryšys",
    "Speed Mining": "Greitas kasimas",
    "Camoflauge": "Kamufliažas",
    "Pack Boost": "Gaujos sustiprinimas",
    "Max Mana Boost": "Maksimalios manos padidinimas",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: suteikti grobio fondą",
    "Rage Counter.": "Įniršio skaitiklis.",
    "Rage Counter": "Įniršio skaitiklis",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s sielą išplėšė %2$s %3$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
