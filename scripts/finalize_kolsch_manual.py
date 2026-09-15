#!/usr/bin/env python3
"""Temporary finalizer for the last stubborn Kölsch semantic labels."""
import bootstrap_kolsch as base

base.MANUAL_VALUES.update({
    "Alchemy II": "Alchemie II",
    "Debug power loading": "Debug-Kraff lade",
    "Ender Drift": "Ender-Letsche",
    "Ender Warp": "Ender-Höpp",
    "Enderite Teleport": "Enderit-Höpp",
    "Foul Aura": "Fiese Aura",
    "Frost Nova": "Kält-Nova",
    "Mana Sponge": "Mana-Schwamm",
    "Mana Well": "Mana-Pötz",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Jevv dä Beute-Pool",
    "Ninja Vanish": "Ninja futsch",
    "Rock Stance": "Stein-Stonn",
    "Rocky Rebound": "Stein-Höpp zoröck",
    "Sic 'Em": "Pack se!",
    "String Arpeggio": "Saite-Arpeggio",
    "Teal Orb": "Blau-jröne Kugel",
    "Tidal Grace": "Welle-Säje",
})

import refine_kolsch

if __name__ == "__main__":
    refine_kolsch.main()
