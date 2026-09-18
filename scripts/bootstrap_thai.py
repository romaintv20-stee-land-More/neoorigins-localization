#!/usr/bin/env python3
"""Generate Thai fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Thai")
source = source.replace("Norwegian", "Thai")
source = source.replace("norwegian_translation_cache.json", "thai_translation_cache.json")
source = source.replace("build/no-discovery", "build/th-discovery")
source = source.replace("no_no", "th_th")
source = source.replace("neoorigins_no_", "neoorigins_th_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "th", True]')
# Numbered printf placeholders may legitimately move in Thai word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "thai_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_thai.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_thai.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "เปิดตัวสร้าง Origin",
    "Mob Origin Creator": "ตัวสร้าง Origin ของม็อบ",
    "Split": "แยก",
    "Elytra Boost": "บูสต์ Elytra",
    "Sonic Boom": "โซนิกบูม",
    "Pack Bond": "สายสัมพันธ์ฝูง",
    "Speed Mining": "ขุดเร็ว",
    "Camoflauge": "การพรางตัว",
    "Pack Boost": "บูสต์ฝูง",
    "Max Mana Boost": "เพิ่มมานาสูงสุด",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: มอบ Loot Pool",
    "Rage Counter.": "ตัวนับความโกรธ.",
    "Rage Counter": "ตัวนับความโกรธ",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
