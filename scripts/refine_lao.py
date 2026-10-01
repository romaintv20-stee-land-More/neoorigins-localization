#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Context-sensitive cleanup for highly visible UI, power/class names and config
# terminology. Origin / NeoOrigins remain canonical project/product terms.
OVERRIDES = {
    # Core NeoOrigins UI.
    "neoorigins.toggle.on": "ເປີດໃຊ້ຄວາມສາມາດແລ້ວ",
    "neoorigins.toggle.off": "ປິດໃຊ້ຄວາມສາມາດແລ້ວ",
    "neoorigins.night_vision.on": "ເປີດການເບິ່ງເຫັນຕອນກາງຄືນແລ້ວ",
    "neoorigins.night_vision.off": "ປິດການເບິ່ງເຫັນຕອນກາງຄືນແລ້ວ",
    "neoorigins.night_vision.disabled_by_server": "ການເບິ່ງເຫັນຕອນກາງຄືນຖືກປິດໃນເຊີບເວີນີ້.",
    "neoorigins.night_vision.no_power": "Origin ຂອງເຈົ້າບໍ່ມີຄວາມສາມາດເບິ່ງເຫັນຕອນກາງຄືນ.",
    "neoorigins.ultimine.no_power": "Origin ຂອງເຈົ້າບໍ່ມີຄວາມສາມາດ Ultimine.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "ຄລາສ",
    "screen.neoorigins.choose_origin": "ເລືອກ Origin",
    "screen.neoorigins.choose.origins.layer.origin": "ເລືອກ Origin",
    "screen.neoorigins.choose.origins.layer.class": "ເລືອກຄລາສ",
    "gui.neoorigins.search.label": "ຄົ້ນຫາ Origin",
    "gui.neoorigins.picker.no_results": "ບໍ່ພົບ Origin ທີ່ກົງກັບການຄົ້ນຫາຂອງເຈົ້າ",
    "gui.neoorigins.hint.select": "ເລືອກ Origin ເພື່ອເບິ່ງລາຍລະອຽດ",
    "gui.neoorigins.detail.powers_header": "ຄວາມສາມາດ",
    "gui.neoorigins.sort.class": "ຄລາສ",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "ສະກິນຂອງຄລາສ",
    "key.neoorigins.view_info": "ເບິ່ງຂໍ້ມູນ Origin",
    "key.neoorigins.open_creator": "ເປີດຕົວສ້າງ Origin",
    "key.neoorigins.open_mob_creator": "ເປີດຕົວສ້າງ Mob Origin",
    "key.neoorigins.toggle_night_vision": "ເປີດ/ປິດການເບິ່ງເຫັນຕອນກາງຄືນ",
    "key.category.neoorigins.hotkeys": "NeoOrigins (ປຸ່ມລັດ)",
    "screen.neoorigins.origin_info": "ຂໍ້ມູນ Origin",
    "gui.neoorigins.info.no_origin": "ຍັງບໍ່ໄດ້ເລືອກ Origin.",
    "gui.neoorigins.info.your_origin": "Origin ຂອງເຈົ້າ",
    "screen.neoorigins.origin_editor": "ຕົວແກ້ໄຂ Origin",
    "gui.neoorigins.editor.layers_header": "ຊັ້ນ Origin",
    "gui.neoorigins.editor.powers_header": "ຄວາມສາມາດເພີ່ມເຕີມ",
    "screen.neoorigins.creator": "ຕົວສ້າງ Origin",
    "gui.neoorigins.creator.tab.powers": "ຄວາມສາມາດ",
    "gui.neoorigins.creator.apply": "ນຳໃຊ້",
    "screen.neoorigins.mob_creator": "ຕົວສ້າງ Mob Origin",
    "gui.neoorigins.mob_creator.tab.powers": "ຄວາມສາມາດ",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "ກົດການເກີດ",
    "gui.neoorigins.mob_creator.tab.drops": "ໄອເທັມທີ່ດຣອບ",
    "gui.neoorigins.mob_creator.apply": "ນຳໃຊ້",
    "gui.neoorigins.debug.powers_header": "ຄວາມສາມາດທີ່ມອບໃຫ້",

    # Medieval Origins visible names/titles.
    "origin.medievalorigins.fae.name": "Fae",
    "origin.medievalorigins.yeti.name": "Yeti",
    "power.medievalorigins.alfiq.on_your_feet.name": "ລຸກຂຶ້ນ",
    "power.medievalorigins.banshee.hexed.name": "ຕ້ອງຄຳສາບ",
    "power.medievalorigins.pixie.pixie_properties.name": "ຮ່າງກາຍຈິ໋ວ",
    "origin.medievalorigins.high_elf.cryomancer.name": "ນັກເວດນ້ຳແຂງ",

    # Origins Furries / ibarn.
    "power.origins_furries.heavy_wool.name": "ຂົນແກະໜັກ",
    "entity.ibarnorigins.homing_wither_skull": "ຫົວ Wither ຕິດຕາມເປົ້າໝາຍ",
    "power.ibarnorigins.witherskull.name": "ຫົວ Wither ຕິດຕາມເປົ້າໝາຍ",

    # NeoOrigins powers/classes where title context matters.
    "power.neoorigins.draconic_ascended_attack.name": "ພະລັງທີ່ເພີ່ມຂຶ້ນ",
    "power.neoorigins.class_merchant_silver_tongue.name": "ວາຈາຈູງໃຈ",
    "power.neoorigins.class_cleric_turn_undead.name": "ຂັບໄລ່ອັນເດດ",
    "power.neoorigins.class_paladin_turn_undead.name": "ຂັບໄລ່ອັນເດດ",
    "power.neoorigins.sporeling_daylight_damage.name": "ແສງແດດເຜົາ",
    "power.neoorigins.frostborn_freeze_aura.name": "ຄື້ນນ້ຳແຂງ",
    "power.neoorigins.strider_fire_immunity.name": "ເກີດໃນລາວາ",
    "power.neoorigins.sculkborn_projectile_immunity.name": "ສຽງສະທ້ອນປ້ອງກັນ",
    "power.neoorigins.enderite_slow_fall.name": "ລ່ອນແບບ Ender",
    "power.neoorigins.enderite_water_damage.name": "ຈຸດອ່ອນ Ender",
    "power.neoorigins.enderian_teleport.name": "ເທເລພອດ Ender",
    "power.neoorigins.feline_no_fall_damage.name": "ເກົ້າຊີວິດ",
    "power.neoorigins.draconic_fire_immunity.name": "ເລືອດມັງກອນ",
    "power.neoorigins.cave_dragon_apex_hp.name": "ມັງກອນຈ່າຝູງ",
    "power.neoorigins.automaton_ascended_overclock.name": "ເລັ່ງຄວາມໄວເກີນຂີດ",
    "power.neoorigins.gravity_mage_irons_attunement.name": "ປັບຈູນແຮງໂນ້ມຖ່ວງ",
    "power.neoorigins.necromancer_irons_attunement.name": "ປັບຈູນເນໂຄຣຕິກ",
    "power.neoorigins.class_rogue_backstab.name": "ແທງຂ້າງຫຼັງ",
    "power.neoorigins.dwarf_darkvision.name": "ການເບິ່ງໃນຄວາມມືດ",
    "power.neoorigins.dwarf_stonecunning.name": "ຄວາມຊຳນານເລື່ອງຫີນ",
    "power.neoorigins.earth_mage_stonecunning.name": "ຄວາມຊຳນານເລື່ອງຫີນ",
    "power.neoorigins.stoneguard_stone_mining.name": "ນັກທຸບຫີນ",
    "power.neoorigins.umbral_no_hunger_sprint.name": "ແລ່ນໃນເງົາ",
    "power.neoorigins.air_mage_zephyr.name": "ສາຍລົມອ່ອນ",
    "power.neoorigins.gravity_mage_unmoored.name": "ໄຮ້ພັນທະ",

    # Configuration labels: translate the property, retain canonical Origin names.
    "neoorigins.configuration.classes.class_lumberjack": "ຄົນຕັດໄມ້",
    "neoorigins.configuration.class_lumberjack": "ຄົນຕັດໄມ້",
    "neoorigins.configuration.cinderborn_fireball": "ລູກໄຟ Cinderborn",
    "neoorigins.configuration.elytrian_elytra_boost": "ບູສ Elytra ຂອງ Elytrian",
    "neoorigins.configuration.golem_fire_weakness": "ຈຸດອ່ອນຕໍ່ໄຟຂອງ Golem",
    "neoorigins.configuration.gorgon_petrifying_gaze": "ສາຍຕາກາຍເປັນຫີນຂອງ Gorgon",
    "neoorigins.configuration.sculkborn_knockback_resist": "ການຕ້ານແຮງກະແທກຂອງ Sculkborn",
    "neoorigins.configuration.verdant_nether_damage": "ຄວາມເສຍຫາຍ Nether ຂອງ Verdant",
    "neoorigins.configuration.warden_sonic_boom": "ຄື້ນສຽງລະເບີດຂອງ Warden",

    # Origins Fantasy / classes / backgrounds.
    "origins.origins_fantasy.fae.name": "Fae",
    "origins.origins_fantasy.fae_two.name": "Fae",
    "origins.origins_fantasy.orc.name": "ອອກ",
    "power.origins_fantasy.fae_spryness.name": "ຄວາມຄ່ອງແຄ່ວຂອງ Fae",
    "power.origins_fantasy.ascended_na.name": "ເກາະທີ່ເພີ່ມພະລັງ",
    "origins.origins_classes_iss.shadowcaster.name": "ນັກເວດເງົາ",
    "power.origins_classes_iss.mystic_turn_undead.name": "ຂັບໄລ່ອັນເດດ",
    "power.origins_classes_iss.sorcerer_oakskin.name": "ຜິວໄມ້ໂອກ",
    "origin.origins_backgrounds_two.disenchanter.name": "ນັກຖອນເວດ",
    "origins.origins_classes_ex.duskblade.name": "ດາບສົນທະຍາ",
    "power.origins_classes_ex.heavy_armor_nerf.name": "ເກາະໜັກ",
    "power.origins_classes_ex.offhand_defense.name": "ປ້ອງກັນດ້ວຍມືຮອງ",
    "power.origins_classes_ex.armor_weakness.name": "ພາລະຂອງເກາະ",
    "power.origins_classes_ex.void_gaze.name": "ສາຍຕາແຫ່ງຄວາມຫວ່າງເປົ່າ",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Night Vision": "ການເບິ່ງເຫັນຕອນກາງຄືນ",
    "Rotten Flesh": "ເນື້ອເນົ່າ",
}

# Fix punctuation glued to a following Lao sentence without touching placeholders.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[\u0E80-\u0EFF])")
changed_files = changed_values = spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/lo_la.json")):
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

print(f"Lao refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
