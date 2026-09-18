#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup of highly visible UI, powers/classes and terms where
# generic MT is prone to literal or game-context mistakes. Origin / NeoOrigins
# remain canonical product terms, matching the established project convention.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Aftësia u aktivizua",
    "neoorigins.toggle.off": "Aftësia u çaktivizua",
    "neoorigins.night_vision.on": "Shikimi i natës u aktivizua",
    "neoorigins.night_vision.off": "Shikimi i natës u çaktivizua",
    "neoorigins.night_vision.disabled_by_server": "Shikimi i natës është çaktivizuar në këtë server.",
    "neoorigins.night_vision.no_power": "Origin-i yt nuk e ka aftësinë e shikimit të natës.",
    "neoorigins.ultimine.no_power": "Origin-i yt nuk e ka aftësinë Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klasë",
    "screen.neoorigins.choose_origin": "Zgjidh një Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Zgjidh një Origin",
    "screen.neoorigins.choose.origins.layer.class": "Zgjidh një klasë",
    "gui.neoorigins.search.label": "Kërko Origin",
    "gui.neoorigins.picker.no_results": "Asnjë Origin nuk përputhet me kërkimin tënd",
    "gui.neoorigins.hint.select": "Zgjidh një Origin për të parë hollësitë",
    "gui.neoorigins.detail.powers_header": "Aftësitë",
    "gui.neoorigins.sort.class": "Klasë",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Aftësia e klasës",
    "key.neoorigins.view_info": "Shiko informacionin e Origin-it",
    "key.neoorigins.open_creator": "Hap Krijuesin e Origin",
    "key.neoorigins.open_mob_creator": "Hap Krijuesin e Mob Origin",
    "key.neoorigins.toggle_night_vision": "Aktivizo/çaktivizo shikimin e natës",
    "key.category.neoorigins.hotkeys": "NeoOrigins (taste të shpejta)",
    "screen.neoorigins.origin_info": "Informacioni i Origin-it",
    "gui.neoorigins.info.no_origin": "Nuk është zgjedhur ende asnjë Origin.",
    "gui.neoorigins.info.your_origin": "Origin-i yt",
    "screen.neoorigins.origin_editor": "Redaktuesi i Origin-it",
    "gui.neoorigins.editor.layers_header": "Shtresat e Origin-it",
    "gui.neoorigins.editor.powers_header": "Aftësi shtesë",
    "screen.neoorigins.creator": "Krijuesi i Origin",
    "gui.neoorigins.creator.tab.powers": "Aftësitë",
    "gui.neoorigins.creator.apply": "Zbato",
    "screen.neoorigins.mob_creator": "Krijuesi i Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Aftësitë",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Rregullat e shfaqjes",
    "gui.neoorigins.mob_creator.tab.drops": "Objektet e hedhura",
    "gui.neoorigins.mob_creator.apply": "Zbato",
    "gui.neoorigins.debug.powers_header": "Aftësitë e dhëna",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Në këmbë",
    "power.medievalorigins.banshee.hexed.name": "I mallkuar",
    "power.medievalorigins.pixie.pixie_properties.name": "Shtat i imët",
    "origin.medievalorigins.high_elf.cryomancer.name": "Kriomant",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Lesh i rëndë",
    "entity.ibarnorigins.homing_wither_skull": "Kafkë Wither gjurmuese",
    "power.ibarnorigins.witherskull.name": "Kafkë Wither gjurmuese",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Forcë e përforcuar",
    "power.neoorigins.class_merchant_silver_tongue.name": "Gojëmbël",
    "power.neoorigins.class_cleric_turn_undead.name": "Dëbo të pavdekurit",
    "power.neoorigins.class_paladin_turn_undead.name": "Dëbo të pavdekurit",
    "power.neoorigins.sporeling_daylight_damage.name": "Djegie nga dielli",
    "power.neoorigins.frostborn_freeze_aura.name": "Shpërthim akulli",
    "power.neoorigins.strider_fire_immunity.name": "Lindur në lavë",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Rezonancë mbrojtëse",
    "power.neoorigins.enderite_slow_fall.name": "Rrëshqitje Ender",
    "power.neoorigins.enderite_water_damage.name": "Dobësi Ender",
    "power.neoorigins.enderian_teleport.name": "Teleportim Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Nëntë jetë",
    "power.neoorigins.draconic_fire_immunity.name": "Gjak dragoi",
    "power.neoorigins.cave_dragon_apex_hp.name": "Dragoi kulmor",
    "power.neoorigins.automaton_ascended_overclock.name": "Mbingarkim",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Harmonizim gravitacional",
    "power.neoorigins.necromancer_irons_attunement.name": "Harmonizim nekrotik",
    "power.neoorigins.class_rogue_backstab.name": "Goditje pas shpine",
    "power.neoorigins.dwarf_darkvision.name": "Shikim në errësirë",
    "power.neoorigins.dwarf_stonecunning.name": "Njohuri guri",
    "power.neoorigins.earth_mage_stonecunning.name": "Njohuri guri",
    "power.neoorigins.stoneguard_stone_mining.name": "Thyerës guri",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Vrapim hije",
    "power.neoorigins.air_mage_zephyr.name": "Fllad",
    "power.neoorigins.gravity_mage_unmoored.name": "I palidhur",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Druvar",
    "neoorigins.configuration.class_lumberjack": "Druvar",
    "neoorigins.configuration.cinderborn_fireball": "Top zjarri Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Përforcim Elytra i Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Dobësi ndaj zjarrit e Golem",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Vështrim gurëzues i Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Rezistencë ndaj zmbrapsjes e Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Dëmtim nga Nether i Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Shpërthim sonik i Warden",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Ork",
    "power.origins_fantasy.fae_spryness.name": "Shkathtësi Fae",
    "power.origins_fantasy.ascended_na.name": "Armaturë e përforcuar",
    "origins.origins_classes_iss.shadowcaster.name": "Magjistar hijesh",
    "power.origins_classes_iss.mystic_turn_undead.name": "Dëbo të pavdekurit",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Lëkurë lisi",
    "origin.origins_backgrounds_two.disenchanter.name": "Çmagjepsës",
    "origins.origins_classes_ex.duskblade.name": "Teh i muzgut",
    "power.origins_classes_ex.heavy_armor_nerf.name": "Armaturë e rëndë",
    "power.origins_classes_ex.offhand_defense.name": "Mbrojtje me dorën dytësore",
    "power.origins_classes_ex.armor_weakness.name": "Barrë e armaturës",
    "power.origins_classes_ex.void_gaze.name": "Vështrim i zbrazëtisë",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Neoorigjinat": "NeoOrigins",
    "Night Vision": "Shikim nate",
    "Rotten Flesh": "Mish i kalbur",
}

# Normalize spacing after punctuation without touching format tokens/placeholders.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÇË])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/sq_al.json")):
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

print(f"Albanian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
