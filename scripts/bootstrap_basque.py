#!/usr/bin/env python3
"""Generate Basque fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Basque")
source = source.replace("Norwegian", "Basque")
source = source.replace("norwegian_translation_cache.json", "basque_translation_cache.json")
source = source.replace("build/no-discovery", "build/eu-discovery")
source = source.replace("no_no", "eu_es")
source = source.replace("neoorigins_no_", "neoorigins_eu_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "eu", True]')
# Numbered printf placeholders may legitimately move in Basque word order.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "basque_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_basque.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_basque.py"), "exec"), namespace)

namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Ireki jatorri-sortzailea",
    "Mob Origin Creator": "Mob-en jatorri-sortzailea",
    "Split": "Banatu",
    "Elytra Boost": "Elytra bultzada",
    "Sonic Boom": "Soinu-eztanda",
    "Pack Bond": "Talde-lotura",
    "Speed Mining": "Meatzaritza azkarra",
    "Camoflauge": "Kamuflajea",
    "Pack Boost": "Talde-bultzada",
    "Max Mana Boost": "Mana maximoaren handitzea",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: eman harrapakin-multzoa",
    "Rage Counter.": "Amorru-kontagailua.",
    "Rage Counter": "Amorru-kontagailua",
    "Origin Architect": "Origin Architect",
    "%1$s had their soul ripped apart by %2$s's %3$s": "%1$s-ren arima %2$s-ren %3$s-k urratu zuen",
}

# Pre-seed fragile wording so the translation service cannot drop semantic actors
# or numbered placeholders. Structural audits still validate all placeholders.
namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
