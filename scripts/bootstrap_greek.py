#!/usr/bin/env python3
"""Generate Greek fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Greek")
source = source.replace("Norwegian", "Greek")
source = source.replace("norwegian_translation_cache.json", "greek_translation_cache.json")
source = source.replace("build/no-discovery", "build/el-discovery")
source = source.replace("no_no", "el_gr")
source = source.replace("neoorigins_no_", "neoorigins_el_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "el", True]')
source = source.replace('uses "no" for Greek.', 'uses "el" for Greek.')

namespace = {"__name__": "greek_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_greek.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_greek.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Άνοιγμα δημιουργού Origin",
    "Mob Origin Creator": "Δημιουργός Mob Origin",
    "Split": "Διαχωρισμός",
    "Elytra Boost": "Ενίσχυση Elytra",
    "Sonic Boom": "Ηχητική έκρηξη",
    "Speed Mining": "Γρήγορη εξόρυξη",
    "Camoflauge": "Καμουφλάζ",
    "Max Mana Boost": "Αύξηση μέγιστης μάνα",
    "Rage Counter.": "Μετρητής οργής.",
    "Rage Counter": "Μετρητής οργής",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
