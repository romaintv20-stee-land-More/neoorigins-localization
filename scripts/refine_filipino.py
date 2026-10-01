#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative context fixes for machine-translation false friends and common
# Minecraft terminology. Proper game/mod terms are retained where that is clearer.
OVERRIDES = {
    "neoorigins.night_vision.no_power": "Walang kakayahang Night Vision ang Origin mo.",
    "neoorigins.ultimine.no_power": "Walang kakayahang Ultimine ang Origin mo.",
    "gui.neoorigins.editor.powers_header": "Mga Naitotoggle na Kapangyarihan",
    "gui.neoorigins.creator.apply": "Ilapat",
    "gui.neoorigins.mob_creator.apply": "Ilapat",
    "gui.neoorigins.mob_creator.tab.drops": "Mga Drop",

    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.blazeling.description": "Ipinanganak sa apoy ng Nether — pinalakas ng asupre at ng madilim na kaharian, ngunit nakalalason sa kanya ang tubig at ulan.",
    "origins.neoorigins.enderian.description": "Ipinanganak sa mga panlabas na isla ng End — nakakapag-teleport, nakakaiwas sa mga projectile, at hindi pinapansin ng mga enderman. Ang tubig ay nakapapasong parang asido.",
    "power.neoorigins.blazeling_fire_immunity.description": "Imyun sa apoy, lava, magma, at pagkasunog — sinasalubong ng apoy sa loob ang apoy sa labas.",
    "power.neoorigins.blazeling_nether_born.name": "Ipinanganak sa Nether",
    "power.neoorigins.blazeling_nether_born.description": "Mas mabilis kang gumagalaw habang nasa Nether.",
    "power.neoorigins.blazeling_stone_fists.description": "Ang iyong mga hubad na kamay ay kasinghusay ng stone pickaxe — makakabasag ka ng bato, ore, at netherrack nang walang gamit.",
    "power.neoorigins.elytrian_no_kinetic.description": "Imyun sa pinsala mula sa banggaan habang gumagamit ng elytra — makakabangga ka sa pader nang walang pinsala.",
    "power.neoorigins.elytrian_no_heavy_armor.name": "Hindi Makapagsuot ng Mabigat na Baluti",
    "power.neoorigins.enderian_ender_eyes.name": "Ender Eyes",
    "power.neoorigins.golem_natural_armor.name": "Balat na Bakal",
    "power.neoorigins.golem_natural_armor.description": "Permanenteng Resistance I — sinasalo ng baluting bakal ang mga suntok kahit walang suot na armor.",
    "power.neoorigins.golem_effect_immunity.description": "Imyun sa Poison, Wither, at Hunger.",
    "power.neoorigins.caveborn_night_vision.name": "Sanay sa Dilim",
    "power.neoorigins.caveborn_no_fall_damage.name": "Hakbang sa Kuweba",
    "power.neoorigins.caveborn_stone_fists.name": "Mga Kamay na Bato",
    "power.neoorigins.caveborn_mining_fortune.name": "Mining Fortune",
    "power.neoorigins.nether_fungus_diet.name": "Pagkaing Fungus ng Nether",
    "power.neoorigins.caveborn_eat_netherite.name": "Panlasa sa Netherite",
    "power.neoorigins.caveborn_netherite_bonus.name": "Netherite Core",
    "power.neoorigins.draconic_fire_immunity.description": "Imyun sa apoy, lava, magma, at pagkasunog — mainit ang dugong dragon.",

    "power.origins_furries.charge.name": "Pagsugod",
    "power.origins_furries.charge.description": "Mas malaki ang pinsalang nagagawa mo habang sprinting.",
    "power.origins_furries.chicken_xp.name": "XP sa Manok",
    "power.origins_furries.chicken_xp.description": "Dobleng XP ang nakukuha mo sa pagpatay ng manok.",
    "power.origins_furries.low_light_vision.name": "Paningin sa Mababang Liwanag",
    "power.origins_furries.pavlov.name": "Tugon ni Pavlov",
    "power.origins_furries.scales.name": "Mga Kaliskis",
    "power.origins_furries.speed_gain.name": "Pagdulas sa Tubig",
    "power.origins_furries.night_vision.name": "Night Vision",
    "power.origins_furries.milk_self.name": "Gatasan ang Sarili",

    "key.originsmodernui.toggle_hud": "I-toggle ang HUD",
    "originsmodernui.config.hud.show_level": "Ipakita ang level",
    "originsmodernui.config.hud.scale": "Sukat ng HUD",
}

# Google occasionally joins translated sentences without a space. Fix only the
# safe case where sentence punctuation is immediately followed by an uppercase
# Latin letter, leaving decimals such as 1.5 untouched.
SENTENCE_JOIN = re.compile(r"(?<=[.!?])(?=[A-ZÁÉÍÓÚÑ])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/fil_ph.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        spaced = SENTENCE_JOIN.sub(" ", new_value)
        if spaced != new_value:
            spacing_fixes += 1
        new_value = spaced
        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Filipino refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
