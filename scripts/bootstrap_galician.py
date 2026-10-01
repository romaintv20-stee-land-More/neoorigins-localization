#!/usr/bin/env python3
"""Generate Galician fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Galician")
source = source.replace("Norwegian", "Galician")
source = source.replace("norwegian_translation_cache.json", "galician_translation_cache.json")
source = source.replace("build/no-discovery", "build/gl-discovery")
source = source.replace("no_no", "gl_es")
source = source.replace("neoorigins_no_", "neoorigins_gl_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "gl", True]')
# Numbered printf placeholders may legitimately move in Galician word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "galician_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_galician.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_galician.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Abrir o creador de orixes",
    "Mob Origin Creator": "Creador de orixes de criaturas",
    "Split": "Dividir",
    "Elytra Boost": "Impulso de élitros",
    "Sonic Boom": "Estalido sónico",
    "Pack Bond": "Vínculo da manda",
    "Speed Mining": "Minería rápida",
    "Camoflauge": "Camuflaxe",
    "Pack Boost": "Impulso da manda",
    "Max Mana Boost": "Aumento de maná máximo",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: conceder táboa de botín",
    "Rage Counter.": "Contador de furia.",
    "Rage Counter": "Contador de furia",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s tivo a alma esnaquizada polo %3$s de %2$s",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
