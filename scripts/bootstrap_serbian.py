#!/usr/bin/env python3
"""Generate Serbian Cyrillic fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Serbian Cyrillic")
source = source.replace("Norwegian", "Serbian")
source = source.replace("norwegian_translation_cache.json", "serbian_translation_cache.json")
source = source.replace("build/no-discovery", "build/sr-discovery")
source = source.replace("no_no", "sr_sp")
source = source.replace("neoorigins_no_", "neoorigins_sr_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "sr", True]')
# Serbian translation may rewrite ASCII separator words, so use private-use
# delimiters that survive Google Translate batching unchanged.
source = source.replace(
    'SEPARATOR_RE = re.compile(r"\\n?ZXQSEP\\d{4}ZXQ\\n?")',
    'SEPARATOR_RE = re.compile(r"\\n?\\ue000\\d{4}\\ue001\\n?")',
)
source = source.replace(
    'f"\\nZXQSEP{index:04d}ZXQ\\n{value}"',
    'f"\\n\\ue000{index:04d}\\ue001\\n{value}"',
)
# Protect placeholders with private-use sentinels too: Serbian transliterates
# visible ASCII marker words such as ZXQPH and would otherwise corrupt them.
source = source.replace(
    'return f"ZXQPH{index:04d}ZXQ"',
    'return f"\\ue100{index:04d}\\ue101"',
)
source = source.replace(
    'text = text.replace(f"ZXQPH{index:04d}ZXQ", token)',
    'text = text.replace(f"\\ue100{index:04d}\\ue101", token)',
)
# If a provider response still drops a batch delimiter, retry that batch one
# string at a time rather than failing the whole localization run.
source = source.replace(
    '''        if len(translated) != len(batch):
            raise RuntimeError(
                f"Batch {batch_number}: expected {len(batch)} translated strings, received {len(translated)}"
            )''',
    '''        if len(translated) != len(batch):
            print(
                f"Batch {batch_number}: delimiter loss ({len(translated)}/{len(batch)}); "
                "retrying strings individually"
            )
            translated = [translate_rpc(masked) for masked in protected]''',
)
# Numbered printf placeholders may legitimately move in Serbian word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "serbian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_serbian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_serbian.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Отвори креатор порекла",
    "Mob Origin Creator": "Креатор порекла моба",
    "Split": "Подели",
    "Elytra Boost": "Појачање елитре",
    "Sonic Boom": "Звучни удар",
    "Pack Bond": "Веза чопора",
    "Speed Mining": "Брзо рударење",
    "Camoflauge": "Камуфлажа",
    "Pack Boost": "Појачање чопора",
    "Max Mana Boost": "Повећање максималне мане",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Додели скуп плена",
    "Rage Counter.": "Бројач беса.",
    "Rage Counter": "Бројач беса",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
