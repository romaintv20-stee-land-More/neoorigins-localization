#!/usr/bin/env python3
"""Generate Esperanto fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Esperanto")
source = source.replace("Norwegian", "Esperanto")
source = source.replace("norwegian_translation_cache.json", "esperanto_translation_cache.json")
source = source.replace("build/no-discovery", "build/eo-discovery")
source = source.replace("no_no", "eo_uy")
source = source.replace("neoorigins_no_", "neoorigins_eo_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "eo", True]')
# Numbered printf placeholders may legitimately move in Esperanto word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "esperanto_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_esperanto.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_esperanto.py"), "exec"), namespace)

# Preserve branded/project terminology and known fragile placeholder strings.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Malfermi Origin Creator",
    "Mob Origin Creator": "Mob Origin Creator",
    "Origin Architect": "Origin Architect",
    "Split": "Dividi",
    "Elytra Boost": "Elytra-akcelo",
    "Sonic Boom": "Sona Eksplodo",
    "Pack Bond": "Grega Ligo",
    "Speed Mining": "Rapida Minado",
    "Camoflauge": "Kamuflado",
    "Pack Boost": "Grega Akcelo",
    "Max Mana Boost": "Plialtigo de Maksimuma Mana",
    "Rage Counter.": "Kolerega Nombrilo.",
    "Rage Counter": "Kolerega Nombrilo",
    "Press %s to cycle between commanding your summons to sit, follow, or teleport to you.": "Premu %s por ŝanĝi inter ordonoj al viaj alvokitoj sidi, sekvi aŭ teletransportiĝi al vi.",
    "§5Void Warp:§r Press %s while holding an ender pearl to rip through the fabric of reality and teleport yourself directly where you're looking, up to 50 blocks away": "§5Vakua Transŝovo:§r Premu %s tenante ender-perlon por ŝiri la teksaĵon de la realo kaj teletransporti vin rekte tien, kien vi rigardas, ĝis 50 blokojn for",
    "%1$s was burnt to a crisp by %2$s using %3$s": "%1$s estis forbruligita de %2$s per %3$s",
    "%1$s was purified by %2$s's dragonfire using %3$s": "%1$s estis purigita de la drakfajro de %2$s per %3$s",
    "%1$s had their soul ripped apart by %2$s's %3$s": "La animo de %1$s estis disŝirita de la %3$s de %2$s",
    "%1$s faced the divine judgment of %2$s's %3$s": "%1$s alfrontis la dian juĝon de la %3$s de %2$s",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
