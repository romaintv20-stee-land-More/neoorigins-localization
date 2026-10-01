#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms. Core
# Minecraft wording follows the current Asturian client where practical.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Poder activáu",
    "neoorigins.toggle.off": "Poder desactiváu",
    "neoorigins.night_vision.on": "Visión nocherniego activada",
    "neoorigins.night_vision.off": "Visión nocherniego desactivada",
    "neoorigins.night_vision.disabled_by_server": "La visión nocherniego ta desactivada nesti sirvidor.",
    "neoorigins.night_vision.no_power": "El to Origin nun tien el poder Visión nocherniego.",
    "neoorigins.ultimine.no_power": "El to Origin nun tien el poder Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Clase",
    "screen.neoorigins.choose_origin": "Escueyi un Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Escueyi un Origin",
    "screen.neoorigins.choose.origins.layer.class": "Escueyi una clase",
    "gui.neoorigins.search.label": "Buscar Origins",
    "gui.neoorigins.picker.no_results": "Nun hai nengún Origin que concase cola busca",
    "gui.neoorigins.hint.select": "Escueyi un Origin pa ver los detalles",
    "gui.neoorigins.detail.powers_header": "Poderes",
    "gui.neoorigins.sort.class": "Clase",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Habilidá de clase",
    "key.neoorigins.view_info": "Ver información del Origin",
    "key.neoorigins.open_creator": "Abrir el creador d'Origin",
    "key.neoorigins.open_mob_creator": "Abrir el creador d'Origin de mobs",
    "key.neoorigins.toggle_night_vision": "Activar/desactivar visión nocherniego",
    "key.category.neoorigins.hotkeys": "NeoOrigins (atayos)",
    "screen.neoorigins.origin_info": "Información del Origin",
    "gui.neoorigins.info.no_origin": "Entá nun s'escoyó nengún Origin.",
    "gui.neoorigins.info.your_origin": "El to Origin",
    "screen.neoorigins.origin_editor": "Editor d'Origin",
    "gui.neoorigins.editor.layers_header": "Capes d'Origin",
    "gui.neoorigins.editor.powers_header": "Poderes adicionales",
    "screen.neoorigins.creator": "Creador d'Origin",
    "gui.neoorigins.creator.tab.powers": "Poderes",
    "gui.neoorigins.creator.apply": "Aplicar",
    "screen.neoorigins.mob_creator": "Creador d'Origin de mobs",
    "gui.neoorigins.mob_creator.tab.powers": "Poderes",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Regles d'apaición",
    "gui.neoorigins.mob_creator.tab.drops": "Botín",
    "gui.neoorigins.mob_creator.apply": "Aplicar",
    "gui.neoorigins.debug.powers_header": "Poderes concedíos",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "De pie",
    "power.medievalorigins.banshee.hexed.name": "Embruxáu",
    "power.medievalorigins.pixie.pixie_properties.name": "Cuerpu diminutu",
    "origin.medievalorigins.high_elf.cryomancer.name": "Criomante",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Llana pesada",
    "entity.ibarnorigins.homing_wither_skull": "Calaveres Wither guiaes",
    "power.ibarnorigins.witherskull.name": "Calaveres Wither guiaes",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Fuercia ascendida",
    "power.neoorigins.class_merchant_silver_tongue.name": "Llingua de plata",
    "power.neoorigins.class_cleric_turn_undead.name": "Repeler muertos vivientes",
    "power.neoorigins.class_paladin_turn_undead.name": "Repeler muertos vivientes",
    "power.neoorigins.sporeling_daylight_damage.name": "Quema a la lluz del día",
    "power.neoorigins.frostborn_freeze_aura.name": "Fola de xelu",
    "power.neoorigins.strider_fire_immunity.name": "Nacíu na lava",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Defensa d'ecu",
    "power.neoorigins.enderite_slow_fall.name": "Planeu Ender",
    "power.neoorigins.enderite_water_damage.name": "Debilidá Ender",
    "power.neoorigins.enderian_teleport.name": "Teleporte Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Nueve vides",
    "power.neoorigins.draconic_fire_immunity.name": "Sangre de dragón",
    "power.neoorigins.cave_dragon_apex_hp.name": "Dragón cimeru",
    "power.neoorigins.automaton_ascended_overclock.name": "Sobrecarga",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Afinidá cola gravedá",
    "power.neoorigins.necromancer_irons_attunement.name": "Afinidá necrótica",
    "power.neoorigins.class_rogue_backstab.name": "Ataque pel llombu",
    "power.neoorigins.dwarf_darkvision.name": "Visión na escuridá",
    "power.neoorigins.earth_mage_stonecunning.name": "Conocencia de la piedra",
    "power.neoorigins.dwarf_stonecunning.name": "Conocencia de la piedra",
    "power.neoorigins.stoneguard_stone_mining.name": "Minería de piedra",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Carrera ente les solombres",
    "power.neoorigins.air_mage_zephyr.name": "Céfiru",
    "power.neoorigins.gravity_mage_unmoored.name": "Desancláu",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Lleñador",
    "neoorigins.configuration.class_lumberjack": "Lleñador",
    "neoorigins.configuration.cinderborn_fireball": "Bola de fueu Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Impulsu d'élitros Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Debilidá al fueu Golem",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Mirada petrificante Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Resistencia al retrocesu Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Dañu del Nether Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Estruendu sónicu Warden",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Orcu",
    "power.origins_fantasy.fae_spryness.name": "Axilidá Fae",
    "power.origins_fantasy.ascended_na.name": "Armadura ascendida",
    "origins.origins_classes_iss.shadowcaster.name": "Llanzador de solombres",
    "power.origins_classes_iss.mystic_turn_undead.name": "Repeler muertos vivientes",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Piel de carbayu",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Visión nocherniego",
    "Rotten Flesh": "Carne podre",
}

# Repair missing spaces between sentences without touching placeholders.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-Þ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ast_es.json")):
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

print(f"Asturian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
