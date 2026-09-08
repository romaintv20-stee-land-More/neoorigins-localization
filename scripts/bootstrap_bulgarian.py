#!/usr/bin/env python3
"""Generate Bulgarian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Bulgarian")
source = source.replace("Norwegian", "Bulgarian")
source = source.replace("norwegian_translation_cache.json", "bulgarian_translation_cache.json")
source = source.replace("build/no-discovery", "build/bg-discovery")
source = source.replace("no_no", "bg_bg")
source = source.replace("neoorigins_no_", "neoorigins_bg_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "bg", True]')
source = source.replace('uses "no" for Bulgarian.', 'uses "bg" for Bulgarian.')
# Numbered printf placeholders may legitimately move in Bulgarian word order.
# Compare the same placeholder multiset, matching the strict audit behavior.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "bulgarian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_bulgarian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_bulgarian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Отвори създателя на Origin",
    "Mob Origin Creator": "Създател на Mob Origin",
    "Split": "Разделяне",
    "Elytra Boost": "Усилване на елитрите",
    "Sonic Boom": "Звуков взрив",
    "Pack Bond": "Връзка с глутницата",
    "Speed Mining": "Бързо копаене",
    "Camoflauge": "Камуфлаж",
    "Pack Boost": "Усилване на глутницата",
    "Max Mana Boost": "Увеличение на максималната мана",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Дай таблица за плячка",
    "Rage Counter.": "Брояч на яростта.",
    "Rage Counter": "Брояч на яростта",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
