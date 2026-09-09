#!/usr/bin/env python3
"""Generate Hindi fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Hindi")
source = source.replace("Norwegian", "Hindi")
source = source.replace("norwegian_translation_cache.json", "hindi_translation_cache.json")
source = source.replace("build/no-discovery", "build/hi-discovery")
source = source.replace("no_no", "hi_in")
source = source.replace("neoorigins_no_", "neoorigins_hi_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "hi", True]')
# Numbered printf placeholders may legitimately move in Hindi word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "hindi_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_hindi.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_hindi.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "ओरिजिन क्रिएटर खोलें",
    "Mob Origin Creator": "मॉब ओरिजिन क्रिएटर",
    "Split": "विभाजन",
    "Elytra Boost": "एलाइट्रा बूस्ट",
    "Sonic Boom": "सोनिक बूम",
    "Pack Bond": "झुंड का बंधन",
    "Speed Mining": "तेज़ खनन",
    "Camoflauge": "छलावरण",
    "Pack Boost": "झुंड बूस्ट",
    "Max Mana Boost": "अधिकतम माना वृद्धि",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: लूट पूल प्रदान करें",
    "Rage Counter.": "क्रोध काउंटर.",
    "Rage Counter": "क्रोध काउंटर",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s की आत्मा %2$s के %3$s ने चीर दी",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
