#!/usr/bin/env python3
"""Generate Tatar fallback localization by adapting the hardened Igbo bootstrap."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_igbo.py").read_text(encoding="utf-8")

# Reuse the hardened separator-probing/token-isolation bootstrap while changing
# only language identifiers, Google target and high-visibility seed terms.
source = source.replace("Igbo", "Tatar")
source = source.replace("igbo", "tatar")
source = source.replace("ig_ng", "tt_ru")
source = source.replace("neoorigins_ig_", "neoorigins_tt_")
source = source.replace("build/ig-discovery", "build/tt-discovery")
source = source.replace('[[text, "en", "ig", True]', '[[text, "en", "tt", True]')
source = source.replace('"tl": "ig"', '"tl": "tt"')
source = source.replace("{'sl': 'en', 'tl': 'ig', 'q': text}", "{'sl': 'en', 'tl': 'tt', 'q': text}")
source = source.replace('{"sl": "en", "tl": "ig", "q": text}', '{"sl": "en", "tl": "tt", "q": text}')

seed_replacements = {
    "Mepee onye okike Origin": "Origin төзүчесен ачу",
    "Onye okike Mob Origin": "Mob Origin төзүчесе",
    "Kewaa": "Бүлү",
    "Nkwalite Elytra": "Elytra көчәйтүе",
    "Mgbawa ụda": "Тавыш дулкыны",
    "Njikọ otu": "Төркем бәйләнеше",
    "Ngwuputa ngwa ngwa": "Тиз казу",
    "Mkpuchi": "Камуфляж",
    "Nkwalite otu": "Төркем көчәйтүе",
    "Nkwalite mana kachasị": "Максималь Mana көчәйтүе",
    "Onụọgụ iwe.": "Ярсу исәпләгече.",
    "Onụọgụ iwe": "Ярсу исәпләгече",
}
for old, new in seed_replacements.items():
    source = source.replace(old, new)

namespace = {"__name__": "tatar_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_tatar.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_tatar.py"), "exec"), namespace)
