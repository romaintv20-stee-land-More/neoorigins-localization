#!/usr/bin/env python3
"""Generate Kyrgyz fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Kyrgyz")
source = source.replace("Norwegian", "Kyrgyz")
source = source.replace("norwegian_translation_cache.json", "kyrgyz_translation_cache.json")
source = source.replace("build/no-discovery", "build/ky-discovery")
source = source.replace("no_no", "ky_kg")
source = source.replace("neoorigins_no_", "neoorigins_ky_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ky", True]')
# Numbered printf placeholders may legitimately move in Kyrgyz word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "kyrgyz_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_kyrgyz.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_kyrgyz.py"), "exec"), namespace)

# Preserve branded/project terminology and known fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin түзүүчүсүн ачуу",
    "Mob Origin Creator": "Mob Origin түзүүчүсү",
    "Origin Architect": "Origin Architect",
    "Split": "Бөлүү",
    "Elytra Boost": "Elytra күчөтүүсү",
    "Sonic Boom": "Үн жарылуусу",
    "Pack Bond": "Топтук байланыш",
    "Speed Mining": "Тез казуу",
    "Camoflauge": "Камуфляж",
    "Pack Boost": "Топтук күчөтүү",
    "Max Mana Boost": "Максималдуу Mana күчөтүүсү",
    "Rage Counter.": "Ачуулануу эсептегичи.",
    "Rage Counter": "Ачуулануу эсептегичи",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s оюнчусун %2$s %3$s колдонуп күлгө айлантты",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s оюнчусун %2$s оюнчусунун ажыдаар оту %3$s аркылуу тазалады",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s оюнчусунун жанын %2$s оюнчусунун %3$s куралы жулуп алды",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s оюнчусу %2$s оюнчусунун %3$s аркылуу кудайлык өкүмүнө туш болду",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
