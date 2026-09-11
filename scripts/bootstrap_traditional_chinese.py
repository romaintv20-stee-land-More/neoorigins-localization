#!/usr/bin/env python3
"""Generate Traditional Chinese (Taiwan) fallback localization from the hardened Igbo bootstrap."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_igbo.py").read_text(encoding="utf-8")

# Reuse the hardened separator-probing/token-isolation bootstrap while changing
# only language identifiers, Google target and high-visibility seed terms.
source = source.replace("Igbo", "Traditional Chinese")
source = source.replace("igbo", "traditional_chinese")
source = source.replace("ig_ng", "zh_tw")
source = source.replace("neoorigins_ig_", "neoorigins_zhtw_")
source = source.replace("build/ig-discovery", "build/zhtw-discovery")
source = source.replace('[[text, "en", "ig", True]', '[[text, "en", "zh-TW", True]')
source = source.replace('"tl": "ig"', '"tl": "zh-TW"')
source = source.replace("{'sl': 'en', 'tl': 'ig', 'q': text}", "{'sl': 'en', 'tl': 'zh-TW', 'q': text}")
source = source.replace('{"sl": "en", "tl": "ig", "q": text}', '{"sl": "en", "tl": "zh-TW", "q": text}')

# Taiwan Traditional Chinese terminology for short/high-visibility strings.
seed_replacements = {
    "Mepee onye okike Origin": "開啟 Origin 建立器",
    "Onye okike Mob Origin": "Mob Origin 建立器",
    "Kewaa": "分割",
    "Nkwalite Elytra": "鞘翅強化",
    "Mgbawa ụda": "聲波爆發",
    "Njikọ otu": "群體羈絆",
    "Ngwuputa ngwa ngwa": "快速挖掘",
    "Mkpuchi": "偽裝",
    "Nkwalite otu": "群體強化",
    "Nkwalite mana kachasị": "最大魔力強化",
    "Onụọgụ iwe.": "怒氣計數器。",
    "Onụọgụ iwe": "怒氣計數器",
}
for old, new in seed_replacements.items():
    source = source.replace(old, new)

namespace = {
    "__name__": "traditional_chinese_bootstrap",
    "__file__": str(ROOT / "scripts/bootstrap_traditional_chinese.py"),
}
exec(compile(source, str(ROOT / "scripts/bootstrap_traditional_chinese.py"), "exec"), namespace)
