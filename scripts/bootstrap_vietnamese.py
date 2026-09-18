#!/usr/bin/env python3
"""Generate Vietnamese fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Vietnamese")
source = source.replace("Norwegian", "Vietnamese")
source = source.replace("norwegian_translation_cache.json", "vietnamese_translation_cache.json")
source = source.replace("build/no-discovery", "build/vi-discovery")
source = source.replace("no_no", "vi_vn")
source = source.replace("neoorigins_no_", "neoorigins_vi_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "vi", True]')
# Numbered printf placeholders may legitimately move in Vietnamese word order.
# Compare the same placeholder multiset, matching the strict audit behavior.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "vietnamese_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_vietnamese.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_vietnamese.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Mở Trình tạo Origin",
    "Mob Origin Creator": "Trình tạo Mob Origin",
    "Split": "Tách",
    "Elytra Boost": "Tăng cường Elytra",
    "Sonic Boom": "Bùng nổ âm thanh",
    "Pack Bond": "Liên kết bầy đàn",
    "Speed Mining": "Đào nhanh",
    "Camoflauge": "Ngụy trang",
    "Pack Boost": "Tăng cường bầy đàn",
    "Max Mana Boost": "Tăng mana tối đa",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Cấp nhóm chiến lợi phẩm",
    "Rage Counter.": "Bộ đếm cuồng nộ.",
    "Rage Counter": "Bộ đếm cuồng nộ",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
