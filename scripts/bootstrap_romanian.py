#!/usr/bin/env python3
"""Generate Romanian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

# Reuse the already-audited bootstrap implementation, changing only locale-specific
# paths/labels and the Google Translate target. Execute it as a module so its main()
# does not auto-run until Romanian-specific overrides are installed.
source = source.replace("Norwegian Bokmål", "Romanian")
source = source.replace("Norwegian", "Romanian")
source = source.replace("norwegian_translation_cache.json", "romanian_translation_cache.json")
source = source.replace("build/no-discovery", "build/ro-discovery")
source = source.replace("no_no", "ro_ro")
source = source.replace("neoorigins_no_", "neoorigins_ro_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ro", True]')
source = source.replace('uses "no" for Romanian.', 'uses "ro" for Romanian.')

namespace = {"__name__": "romanian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_romanian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_romanian.py"), "exec"), namespace)

# Avoid carrying Norwegian wording overrides into Romanian. Keep product/canonical
# names stable and add only a few obvious Romanian UI terms where useful.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Deschide creatorul de origini",
    "Mob Origin Creator": "Creator de origini pentru mobi",
    "Split": "Împarte",
    "Elytra Boost": "Impuls Elytra",
    "Sonic Boom": "Explozie sonică",
    "Speed Mining": "Minerit rapid",
    "Camoflauge": "Camuflaj",
    "Max Mana Boost": "Creștere maximă de mană",
    "Rage Counter.": "Contor de furie.",
    "Rage Counter": "Contor de furie",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
