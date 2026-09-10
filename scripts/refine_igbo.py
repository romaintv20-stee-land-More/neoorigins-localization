#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms. Core
# Minecraft wording follows the current Igbo client where practical.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "Agbanyere ike",
    "neoorigins.toggle.off": "Agbanyụrụ ike",
    "neoorigins.night_vision.on": "Agbanyere ọhụụ abalị",
    "neoorigins.night_vision.off": "Agbanyụrụ ọhụụ abalị",
    "neoorigins.night_vision.disabled_by_server": "Agbanyụrụ ọhụụ abalị na sava a.",
    "neoorigins.night_vision.no_power": "Origin gị enweghị ike Ọhụụ abalị.",
    "neoorigins.ultimine.no_power": "Origin gị enweghị ike Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Klas",
    "screen.neoorigins.choose_origin": "Họrọ Origin",
    "screen.neoorigins.choose.origins.layer.origin": "Họrọ Origin",
    "screen.neoorigins.choose.origins.layer.class": "Họrọ klas",
    "gui.neoorigins.search.label": "Chọọ Origins",
    "gui.neoorigins.picker.no_results": "Enweghị Origin dabara na ọchụchọ ahụ",
    "gui.neoorigins.hint.select": "Họrọ Origin iji hụ nkọwa",
    "gui.neoorigins.detail.powers_header": "Ike",
    "gui.neoorigins.sort.class": "Klas",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Nkà klas",
    "key.neoorigins.view_info": "Lee ozi Origin",
    "key.neoorigins.open_creator": "Mepee onye okike Origin",
    "key.neoorigins.open_mob_creator": "Mepee onye okike Mob Origin",
    "key.neoorigins.toggle_night_vision": "Gbanye/gbanyụọ ọhụụ abalị",
    "key.category.neoorigins.hotkeys": "NeoOrigins (ụzọ mkpirisi)",
    "screen.neoorigins.origin_info": "Ozi Origin",
    "gui.neoorigins.info.no_origin": "Ahọrọbeghị Origin.",
    "gui.neoorigins.info.your_origin": "Origin gị",
    "screen.neoorigins.origin_editor": "Onye ndezi Origin",
    "gui.neoorigins.editor.layers_header": "Ọkwa Origin",
    "gui.neoorigins.editor.powers_header": "Ike ndị ọzọ",
    "screen.neoorigins.creator": "Onye okike Origin",
    "gui.neoorigins.creator.tab.powers": "Ike",
    "gui.neoorigins.creator.apply": "Tinye",
    "screen.neoorigins.mob_creator": "Onye okike Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "Ike",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Iwu ịpụta",
    "gui.neoorigins.mob_creator.tab.drops": "Ihe dara",
    "gui.neoorigins.mob_creator.apply": "Tinye",
    "gui.neoorigins.debug.powers_header": "Ike e kenyere",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "Guzoro n'ụkwụ gị",
    "power.medievalorigins.banshee.hexed.name": "A bụrụ ọnụ",
    "power.medievalorigins.pixie.pixie_properties.name": "Obere ahụ",
    "origin.medievalorigins.high_elf.cryomancer.name": "Cryomancer",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "Ajị anụ dị arọ",
    "entity.ibarnorigins.homing_wither_skull": "Okpokoro isi Wither na-achụso",
    "power.ibarnorigins.witherskull.name": "Okpokoro isi Wither na-achụso",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "Ike karịrị akarị",
    "power.neoorigins.class_merchant_silver_tongue.name": "Ire ọlaọcha",
    "power.neoorigins.class_cleric_turn_undead.name": "Chụpụ ndị nwụrụ anwụ",
    "power.neoorigins.class_paladin_turn_undead.name": "Chụpụ ndị nwụrụ anwụ",
    "power.neoorigins.sporeling_daylight_damage.name": "Ìhè ụbọchị na-ere ọkụ",
    "power.neoorigins.frostborn_freeze_aura.name": "Aura oyi",
    "power.neoorigins.strider_fire_immunity.name": "Nguzogide ọkụ",
    "power.neoorigins.sculkborn_projectile_immunity.name": "Nchedo ụda",
    "power.neoorigins.enderite_slow_fall.name": "Ọdịda nwayọọ Ender",
    "power.neoorigins.enderite_water_damage.name": "Adịghị ike Ender n'ime mmiri",
    "power.neoorigins.enderian_teleport.name": "Mbugharị Ender",
    "power.neoorigins.feline_no_fall_damage.name": "Ndụ itoolu",
    "power.neoorigins.draconic_fire_immunity.name": "Ọbara dragọn",
    "power.neoorigins.cave_dragon_apex_hp.name": "Dragọn kachasị elu",
    "power.neoorigins.automaton_ascended_overclock.name": "Overclock",
    "power.neoorigins.gravity_mage_irons_attunement.name": "Njikọ ndọda",
    "power.neoorigins.necromancer_irons_attunement.name": "Njikọ necrotic",
    "power.neoorigins.class_rogue_backstab.name": "Mwakpo n'azụ",
    "power.neoorigins.dwarf_darkvision.name": "Ọhụụ n'ọchịchịrị",
    "power.neoorigins.earth_mage_stonecunning.name": "Amamihe nkume",
    "power.neoorigins.dwarf_stonecunning.name": "Amamihe nkume",
    "power.neoorigins.stoneguard_stone_mining.name": "Ngwuputa nkume",
    "power.neoorigins.umbral_no_hunger_sprint.name": "Ịgba ọsọ n'ọchịchịrị",
    "power.neoorigins.air_mage_zephyr.name": "Zephyr",
    "power.neoorigins.gravity_mage_unmoored.name": "Enweghị arịlịka",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "Onye na-egbutu osisi",
    "neoorigins.configuration.class_lumberjack": "Onye na-egbutu osisi",
    "neoorigins.configuration.cinderborn_fireball": "Bọọlụ ọkụ Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "Nkwalite Elytra nke Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "Adịghị ike Golem n'ọkụ",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Nlele na-eme nkume nke Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "Nguzogide nkwatu nke Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "Mmebi Nether nke Verdant",
    "neoorigins.configuration.warden_sonic_boom": "Mgbawa ụda Warden",

    # Origins Fantasy / classes.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "Orc",
    "power.origins_fantasy.fae_spryness.name": "Ngwa ngwa Fae",
    "power.origins_fantasy.ascended_na.name": "Ekike agha karịrị akarị",
    "origins.origins_classes_iss.shadowcaster.name": "Onye na-akpọ onyinyo",
    "power.origins_classes_iss.mystic_turn_undead.name": "Chụpụ ndị nwụrụ anwụ",
    "power.origins_classes_iss.sorcerer_oakskin.name": "Akpụkpọ oak",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "Ọhụụ abalị",
    "Rotten Flesh": "Anụ Ahụ rere ere",
}

SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[A-ZÀ-ÖØ-ÞỊỌỤṄ])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ig_ng.json")):
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

print(f"Igbo refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
