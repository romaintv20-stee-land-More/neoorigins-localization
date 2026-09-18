#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

OVERRIDES = {
    # Core NeoOrigins UI. Keep Origin / NeoOrigins as canonical project terms.
    "neoorigins.toggle.on": "திறன் இயக்கப்பட்டது",
    "neoorigins.toggle.off": "திறன் முடக்கப்பட்டது",
    "neoorigins.night_vision.on": "இரவு பார்வை இயக்கப்பட்டது",
    "neoorigins.night_vision.off": "இரவு பார்வை முடக்கப்பட்டது",
    "neoorigins.night_vision.disabled_by_server": "இந்த சர்வரில் இரவு பார்வை முடக்கப்பட்டுள்ளது.",
    "neoorigins.night_vision.no_power": "உங்கள் Origin-க்கு இரவு பார்வைத் திறன் இல்லை.",
    "neoorigins.ultimine.no_power": "உங்கள் Origin-க்கு Ultimine திறன் இல்லை.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "வகுப்பு",
    "screen.neoorigins.choose_origin": "Origin-ஐத் தேர்ந்தெடுக்கவும்",
    "screen.neoorigins.choose.origins.layer.origin": "Origin-ஐத் தேர்ந்தெடுக்கவும்",
    "screen.neoorigins.choose.origins.layer.class": "வகுப்பைத் தேர்ந்தெடுக்கவும்",
    "gui.neoorigins.search.label": "Origin-ஐத் தேடு",
    "gui.neoorigins.picker.no_results": "உங்கள் தேடலுக்கு பொருந்தும் Origin எதுவும் இல்லை",
    "gui.neoorigins.hint.select": "விவரங்களைப் பார்க்க ஒரு Origin-ஐத் தேர்ந்தெடுக்கவும்",
    "gui.neoorigins.detail.powers_header": "திறன்கள்",
    "gui.neoorigins.sort.class": "வகுப்பு",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "வகுப்பு திறன்",
    "key.neoorigins.view_info": "Origin தகவலைப் பார்",
    "key.neoorigins.open_creator": "Origin உருவாக்கியைத் திற",
    "key.neoorigins.open_mob_creator": "Mob Origin உருவாக்கியைத் திற",
    "key.neoorigins.toggle_night_vision": "இரவு பார்வையை இயக்கு/முடக்கு",
    "key.category.neoorigins.hotkeys": "NeoOrigins (விரைவு விசைகள்)",
    "screen.neoorigins.origin_info": "Origin தகவல்",
    "gui.neoorigins.info.no_origin": "இன்னும் Origin தேர்ந்தெடுக்கப்படவில்லை.",
    "gui.neoorigins.info.your_origin": "உங்கள் Origin",
    "screen.neoorigins.origin_editor": "Origin திருத்தி",
    "gui.neoorigins.editor.layers_header": "Origin அடுக்குகள்",
    "gui.neoorigins.editor.powers_header": "கூடுதல் திறன்கள்",
    "screen.neoorigins.creator": "Origin உருவாக்கி",
    "gui.neoorigins.creator.tab.powers": "திறன்கள்",
    "gui.neoorigins.creator.apply": "பயன்படுத்து",
    "screen.neoorigins.mob_creator": "Mob Origin உருவாக்கி",
    "gui.neoorigins.mob_creator.tab.powers": "திறன்கள்",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "தோன்றும் விதிகள்",
    "gui.neoorigins.mob_creator.tab.drops": "கிடைக்கும் பொருட்கள்",
    "gui.neoorigins.mob_creator.apply": "பயன்படுத்து",
    "gui.neoorigins.debug.powers_header": "வழங்கப்பட்ட திறன்கள்",

    # Medieval Origins visible names left untranslated or awkward by MT.
    "origin.medievalorigins.fae.name": "ஃபே",
    "origin.medievalorigins.yeti.name": "எட்டி",
    "power.medievalorigins.alfiq.on_your_feet.name": "காலில் எழுந்து நில்",
    "power.medievalorigins.banshee.hexed.name": "சாபமிடப்பட்டது",
    "power.medievalorigins.pixie.pixie_properties.name": "மிகச் சிறிய உருவம்",
    "origin.medievalorigins.high_elf.cryomancer.name": "பனிமந்திரவாதி",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "கனமான கம்பளி",
    "entity.ibarnorigins.homing_wither_skull": "இலக்கைப் பின்தொடரும் விதர் மண்டை ஓடு",
    "power.ibarnorigins.witherskull.name": "இலக்கைப் பின்தொடரும் விதர் மண்டை ஓடு",

    # NeoOrigins powers/classes where short English titles are particularly visible.
    "power.neoorigins.draconic_ascended_attack.name": "மேம்பட்ட வலிமை",
    "power.neoorigins.class_merchant_silver_tongue.name": "வாக்குவன்மை",
    "power.neoorigins.class_cleric_turn_undead.name": "இறவாதவர்களை விரட்டு",
    "power.neoorigins.class_paladin_turn_undead.name": "இறவாதவர்களை விரட்டு",
    "power.neoorigins.sporeling_daylight_damage.name": "சூரிய எரிப்பு",
    "power.neoorigins.frostborn_freeze_aura.name": "பனிக்குளிர் வெடிப்பு",
    "power.neoorigins.strider_fire_immunity.name": "லாவாவில் பிறந்தவர்",
    "power.neoorigins.sculkborn_projectile_immunity.name": "ஒலி எதிரொலி",
    "power.neoorigins.enderite_slow_fall.name": "எண்டர் சறுக்கு",
    "power.neoorigins.enderite_water_damage.name": "எண்டர் பலவீனம்",
    "power.neoorigins.enderian_teleport.name": "எண்டர் தொலைப்பெயர்வு",
    "power.neoorigins.feline_no_fall_damage.name": "ஒன்பது உயிர்கள்",
    "power.neoorigins.draconic_fire_immunity.name": "டிராகன் இரத்தம்",
    "power.neoorigins.cave_dragon_apex_hp.name": "உச்ச டிராகன்",
    "power.neoorigins.automaton_ascended_overclock.name": "அதிவேக இயக்கம்",
    "power.neoorigins.gravity_mage_irons_attunement.name": "ஈர்ப்பியல் ஒத்திசைவு",
    "power.neoorigins.necromancer_irons_attunement.name": "மரண ஒத்திசைவு",
    "power.neoorigins.class_rogue_backstab.name": "முதுகுக்குத்து",
    "power.neoorigins.dwarf_darkvision.name": "இருள் பார்வை",
    "power.neoorigins.dwarf_stonecunning.name": "கல் நுண்ணறிவு",
    "power.neoorigins.earth_mage_stonecunning.name": "கல் நுண்ணறிவு",
    "power.neoorigins.stoneguard_stone_mining.name": "கல் உடைப்பவர்",
    "power.neoorigins.umbral_no_hunger_sprint.name": "நிழல் ஓட்டம்",
    "power.neoorigins.air_mage_zephyr.name": "மெல்லிய தென்றல்",
    "power.neoorigins.gravity_mage_unmoored.name": "பிணைப்பற்றவர்",

    # Configuration labels: translate the action/property while retaining canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "மர வெட்டுபவர்",
    "neoorigins.configuration.class_lumberjack": "மர வெட்டுபவர்",
    "neoorigins.configuration.cinderborn_fireball": "Cinderborn தீப்பந்து",
    "neoorigins.configuration.elytrian_elytra_boost": "Elytrian Elytra வேக உயர்வு",
    "neoorigins.configuration.golem_fire_weakness": "Golem தீ பலவீனம்",
    "neoorigins.configuration.gorgon_petrifying_gaze": "Gorgon கல்லாக்கும் பார்வை",
    "neoorigins.configuration.sculkborn_knockback_resist": "Sculkborn பின்னடிப்பு எதிர்ப்பு",
    "neoorigins.configuration.verdant_nether_damage": "Verdant நெதர் சேதம்",
    "neoorigins.configuration.warden_sonic_boom": "Warden ஒலி வெடிப்பு",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "ஃபே",
    "origins.origins_fantasy.fae_two.name": "ஃபே",
    "origins.origins_fantasy.orc.name": "ஆர்க்",
    "power.origins_fantasy.fae_spryness.name": "ஃபே சுறுசுறுப்பு",
    "power.origins_fantasy.ascended_na.name": "மேம்பட்ட கவசம்",
    "origins.origins_classes_iss.shadowcaster.name": "நிழல் மந்திரவாதி",
    "power.origins_classes_iss.mystic_turn_undead.name": "இறவாதவர்களை விரட்டு",
    "power.origins_classes_iss.sorcerer_oakskin.name": "ஓக் தோல் பாதுகாப்பு",
    "origin.origins_backgrounds_two.disenchanter.name": "மந்திரநீக்குபவர்",
    "origins.origins_classes_ex.duskblade.name": "அந்திவாள்",
    "power.origins_classes_ex.heavy_armor_nerf.name": "சிரமமான கவசம்",
    "power.origins_classes_ex.offhand_defense.name": "துணைக் கை பாதுகாப்பு",
    "power.origins_classes_ex.armor_weakness.name": "கவசச் சுமை",
    "power.origins_classes_ex.void_gaze.name": "வெற்றிடப் பார்வை",
}

# Official/current Minecraft Tamil terminology where applicable, plus brand normalization.
VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "இரவு பார்வை",
    "Rotten Flesh": "அழுகிய சதை",
}

# Fix punctuation glued to a following Tamil sentence without disturbing format tokens.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[\u0B80-\u0BFF])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ta_in.json")):
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
print(f"Tamil refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
