#!/usr/bin/env python3
"""Generate Mongolian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Mongolian")
source = source.replace("Norwegian", "Mongolian")
source = source.replace("norwegian_translation_cache.json", "mongolian_translation_cache.json")
source = source.replace("build/no-discovery", "build/mn-discovery")
source = source.replace("no_no", "mn_mn")
source = source.replace("neoorigins_no_", "neoorigins_mn_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "mn", True]')
# Numbered printf placeholders may legitimately move in Mongolian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "mongolian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_mongolian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_mongolian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Origin бүтээгчийг нээх",
    "Mob Origin Creator": "Mob Origin бүтээгч",
    "Split": "Хуваах",
    "Elytra Boost": "Elytra хурдасгал",
    "Sonic Boom": "Дууны тэсрэлт",
    "Speed Mining": "Хурдан олборлолт",
    "Camoflauge": "Өнгөлөн далдлалт",
    "Max Mana Boost": "Mana-гийн дээд нэмэгдэл",
    "Rage Counter.": "Уур хилэнгийн тоолуур.",
    "Rage Counter": "Уур хилэнгийн тоолуур",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s-ийг %2$s %3$s ашиглан үнс болгож шатаав",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s-ийг %2$s-ын лууны гал %3$s ашиглан ариусгав",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s-ын сүнсийг %2$s-ын %3$s урж таслав",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s %2$s-ын %3$s-ийн тэнгэрлэг шүүлттэй тулгарав",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
