#!/usr/bin/env python3
"""Generate Catalan fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Catalan")
source = source.replace("Norwegian", "Catalan")
source = source.replace("norwegian_translation_cache.json", "catalan_translation_cache.json")
source = source.replace("build/no-discovery", "build/ca-discovery")
source = source.replace("no_no", "ca_es")
source = source.replace("neoorigins_no_", "neoorigins_ca_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ca", True]')
# Numbered printf placeholders may legitimately move in Catalan word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "catalan_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_catalan.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_catalan.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Obre el creador d'orígens",
    "Mob Origin Creator": "Creador d'orígens de criatures",
    "Split": "Divideix",
    "Elytra Boost": "Impuls d'èlitres",
    "Sonic Boom": "Explosió sònica",
    "Pack Bond": "Vincle de manada",
    "Speed Mining": "Mineria ràpida",
    "Camoflauge": "Camuflatge",
    "Pack Boost": "Impuls de manada",
    "Max Mana Boost": "Augment de mana màxim",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Concedeix una reserva de botí",
    "Rage Counter.": "Comptador de fúria.",
    "Rage Counter": "Comptador de fúria",
    "Origin Architect": "Origin Architect",
}

namespace["main"]()
