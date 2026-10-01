#!/usr/bin/env python3
"""Generate Armenian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Armenian")
source = source.replace("Norwegian", "Armenian")
source = source.replace("norwegian_translation_cache.json", "armenian_translation_cache.json")
source = source.replace("build/no-discovery", "build/hy-discovery")
source = source.replace("no_no", "hy_am")
source = source.replace("neoorigins_no_", "neoorigins_hy_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "hy", True]')
# Numbered printf placeholders may legitimately move in Armenian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "armenian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_armenian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_armenian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Բացել Origin ստեղծիչը",
    "Mob Origin Creator": "Mob Origin ստեղծիչ",
    "Split": "Բաժանել",
    "Elytra Boost": "Elytra արագացում",
    "Sonic Boom": "Ձայնային պայթյուն",
    "Speed Mining": "Արագ հանքարդյունահանում",
    "Camoflauge": "Քողարկում",
    "Max Mana Boost": "Առավելագույն Mana-ի ուժեղացում",
    "Rage Counter.": "Զայրույթի հաշվիչ։",
    "Rage Counter": "Զայրույթի հաշվիչ",
    "Origin Architect": "Origin Architect",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s-ը %2$s-ի կողմից %3$s-ի միջոցով այրվեց մինչև մոխիր",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s-ը մաքրվեց %2$s-ի վիշապի կրակով՝ օգտագործելով %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s-ի հոգին պատռվեց %2$s-ի %3$s-ի կողմից",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s-ը ենթարկվեց %2$s-ի %3$s-ի աստվածային դատաստանին",
}

# Pre-seed fragile wording so the translation service cannot duplicate, drop,
# or reorder numbered placeholders incorrectly. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
