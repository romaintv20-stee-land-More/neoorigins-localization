#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms. Core
# Minecraft wording follows the current Occitan client where practical.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Poder activat",
    "neoorigins.toggle.off": "Poder desactivat",
    "neoorigins.night_vision.on": "Vision nocturna activada",
    "neoorigins.night_vision.off": "Vision nocturna desactivada",
    "neoorigins.night_vision.disabled_by_server": "La vision nocturna es desactivada sus aqueste servidor.",
    "neoorigins.night_vision.no_power": "Ton Origin a pas lo poder Vision nocturna.",
    "neoorigins.ultimine.no_power": "Ton Origin a pas lo poder Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Classa",
    "screen.neoorigins.choose_origin": "Causissètz un Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Causissètz un Origin",
    "screen.neoorigins.choose.origins.layer.class": "Causissètz una classa",
    "gui.neoorigins.search.label": "Recercar d'Origins",
    "gui.neoorigins.picker.no_results": "Cap d'Origin correspond pas a la recèrca",
    "gui.neoorigins.hint.select": "Seleccionatz un Origin per veire los detalhs",
    "gui.neoorigins.detail.powers_header": "Poders",
    "gui.neoorigins.sort.class": "Classa",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Competéncia de classa",
    "key.neoorigins.view_info": "Veire las informacions de l'Origin",
    "key.neoorigins.open_creator": "Dobrir lo creador d'Origin",
    "key.neoorigins.open_mob_creator": "Dobrir lo creador de Mob Origin",
    "key.neoorigins.toggle_night_vision": "Activar/desactivar la vision nocturna",
    "key.category.neoorigins.hotkeys": "NeoOrigins (acorcis)",
    "screen.neoorigins.origin_info": "Informacions de l'Origin",
    "gui.neoorigins.info.no_origin": "Cap d'Origin es pas encara causit.",
    "gui.neoorigins.info.your_origin": "Ton Origin",
    "screen.neoorigins.origin_editor": "Editor d'Origin",
    "gui.neoorigins.editor.layers_header": "Jaças d'Origin",
    "gui.neoorigins.editor.powers_header": "Poders suplementaris",
    "screen.neoorigins.creator": "Creador d'Origin",
    "gui.neoorigins.creator.tab.powers": "Poders",
    "gui.neoorigins.creator.apply": "Aplicar",
    "screen.neoorigins.mob_creator": "Creador de Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Poders",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Règlas d'aparicion",
    "gui.neoorigins.mob_creator.tab.drops": "Botin",
    "gui.neoorigins.mob_creator.apply": "Aplicar",
    "gui.neoorigins.debug.powers_header": "Poders assignats",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fada",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Sus tos pès",
    "power.medievalorigins.banshee.hexed.name": "Emmascat",
    "power.medievalorigins.pixie.pixie_properties.name": "Còs pichon",
    "origin.medievalorigins.high_elf.cryomancer.name": "Criomancian",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Lana pesuga",
    "entity.ibarnorigins.homing_wither_skull": "Crani de Wither teleguidat",
    "power.ibarnorigins.witherskull.name": "Crani de Wither teleguidat",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Poder transcendit",
    "power.neoorigins.class_merchant_silver_tongue.name": "Lenga d'argent",
    "power.neoorigins.class_cleric_turn_undead.name": "Repelir los mòrts-vivents",
    "power.neoorigins.class_paladin_turn_undead.name": "Repelir los mòrts-vivents",
    "power.neoorigins.sporeling_daylight_damage.name": "Lutz del jorn ardenta",
    "power.neoorigins.frostborn_freeze_aura.name": "Aura de gel",
    "power.neoorigins.strider_fire_immunity.name": "Nascut dins la lava",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Defensa d'eco",
    "power.neoorigins.enderite_slow_fall.name": "Planatge d'Ender",
    "power.neoorigins.enderite_water_damage.name": "Feblesa d'Ender",
    "power.neoorigins.enderian_teleport.name": "Teleportacion d'Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Nòu vidas",
    "power.neoorigins.draconic_fire_immunity.name": "Sang de dragon",
    "power.neoorigins.cave_dragon_apex_hp.name": "Dragon suprèm",
    "power.neoorigins.automaton_ascended_overclock.name": "Subrefrequençatge",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Acordatge gravitacional",
    "power.neoorigins.necromancer_irons_attunement.name": "Acordatge necrotic",
    "power.neoorigins.class_rogue_backstab.name": "Còp dins l'esquina",
    "power.neoorigins.dwarf_darkvision.name": "Vision dins l'escur",
    "power.neoorigins.earth_mage_stonecunning.name": "Coneissença de la pèira",
    "power.neoorigins.dwarf_stonecunning.name": "Coneissença de la pèira",
    "power.neoorigins.stoneguard_stone_mining.name": "Minatge de pèira",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Córrer dins las ombras",
    "power.neoorigins.air_mage_zephyr.name": "Zefir",
    "power.neoorigins.gravity_mage_unmoored.name": "Desancorat",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Boscatièr",
    "neoorigins.configuration.class_lumberjack": "Boscatièr",
    "neoorigins.configuration.cinderborn_fireball": "Bola de fuòc de Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Impulsion d'elitra d'Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Feblesa al fuòc de Golem",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Agach petrificant de Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Resisténcia al recul de Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Damatges del Nether de Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Explosion sonica de Warden",

    # Origins Fantasy / classes.
    "origins.origins_fantasy.fae.name": "Fada",
    "origins.origins_fantasy.fae_two.name": "Fada",
    "origins.origins_fantasy.orc.name": "Òrc",
    "power.origins_fantasy.fae_spryness.name": "Agilitat de fada",
    "power.origins_fantasy.ascended_na.name": "Armadura transcendida",
    "origins.origins_classes_iss.shadowcaster.name": "Invocador d'ombra",
    "power.origins_classes_iss.mystic_turn_undead.name": "Repelir los mòrts-vivents",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Pèl de casse",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Vision nocturna",
    "Rotten Flesh": "Carn poirida",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-Þ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/oc_fr.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        for old, new in VALUE_REPLACEMENTS.items():
            new_value = new_value.replace(old, new)
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

print(f"Occitan refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
