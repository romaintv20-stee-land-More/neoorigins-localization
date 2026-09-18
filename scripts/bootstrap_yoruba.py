#!/usr/bin/env python3
"""Generate Yoruba fallback localization by adapting the hardened Igbo bootstrap."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_igbo.py").read_text(encoding="utf-8")

# Reuse the immediately previous hardened bootstrap while changing only the
# language-specific identifiers, Google target and high-visibility seed terms.
source = source.replace("Igbo", "Yoruba")
source = source.replace("igbo", "yoruba")
source = source.replace("ig_ng", "yo_ng")
source = source.replace("neoorigins_ig_", "neoorigins_yo_")
source = source.replace("build/ig-discovery", "build/yo-discovery")
source = source.replace('[[text, "en", "ig", True]', '[[text, "en", "yo", True]')
source = source.replace('"tl": "ig"', '"tl": "yo"')
source = source.replace("{'sl': 'en', 'tl': 'ig', 'q': text}", "{'sl': 'en', 'tl': 'yo', 'q': text}")
source = source.replace('{"sl": "en", "tl": "ig", "q": text}', '{"sl": "en", "tl": "yo", "q": text}')

# Replace the Igbo seed wording with Yoruba. Canonical product/project names
# remain untranslated where appropriate.
seed_replacements = {
    "Mepee onye okike Origin": "Ṣí Olùdá Origin",
    "Onye okike Mob Origin": "Olùdá Mob Origin",
    "Kewaa": "Pín",
    "Nkwalite Elytra": "Ìgbéga Elytra",
    "Mgbawa ụda": "Ìbúgbàù Ohùn",
    "Njikọ otu": "Ìsopọ̀ ẹgbẹ́",
    "Ngwuputa ngwa ngwa": "Ìwakùsà Yára",
    "Mkpuchi": "Ìfarapamọ́",
    "Nkwalite otu": "Ìgbéga ẹgbẹ́",
    "Nkwalite mana kachasị": "Ìgbéga Mana Tó Pọ̀ Jù",
    "Onụọgụ iwe.": "Kàǹtà Ìbínú.",
    "Onụọgụ iwe": "Kàǹtà Ìbínú",
}
for old, new in seed_replacements.items():
    source = source.replace(old, new)

namespace = {"__name__": "yoruba_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_yoruba.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_yoruba.py"), "exec"), namespace)
