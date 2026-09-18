#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

OVERRIDES = {
    "neoorigins.toggle.on": "ძალა ჩართულია",
    "neoorigins.toggle.off": "ძალა გამორთულია",
    "neoorigins.night_vision.on": "ღამის ხედვა ჩართულია",
    "neoorigins.night_vision.off": "ღამის ხედვა გამორთულია",
    "neoorigins.night_vision.disabled_by_server": "ღამის ხედვა გამორთულია ამ სერვერზე.",
    "neoorigins.night_vision.no_power": "თქვენს Origin-ს არ აქვს ღამის ხედვის ძალა.",
    "neoorigins.ultimine.no_power": "თქვენს Origin-ს არ აქვს Ultimine ძალა.",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "კლასი",
    "screen.neoorigins.choose_origin": "აირჩიეთ თქვენი Origin",
    "screen.neoorigins.choose.origins.layer.origin": "აირჩიეთ თქვენი Origin",
    "screen.neoorigins.choose.origins.layer.class": "აირჩიეთ თქვენი კლასი",
    "gui.neoorigins.search.label": "Origin-ის ძიება",
    "gui.neoorigins.picker.no_results": "არცერთი Origin არ შეესაბამება თქვენს ძიებას",
    "gui.neoorigins.hint.select": "დეტალების სანახავად აირჩიეთ Origin",
    "gui.neoorigins.detail.powers_header": "ძალები",
    "gui.neoorigins.sort.class": "კლასი",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "კლასის უნარი",
    "key.neoorigins.view_info": "Origin-ის ინფორმაციის ნახვა",
    "key.neoorigins.open_creator": "Origin-ის შემქმნელის გახსნა",
    "key.neoorigins.open_mob_creator": "Mob Origin-ის შემქმნელის გახსნა",
    "key.neoorigins.toggle_night_vision": "ღამის ხედვის ჩართვა/გამორთვა",
    "key.category.neoorigins.hotkeys": "NeoOrigins (სწრაფი ღილაკები)",
    "screen.neoorigins.origin_info": "Origin-ის ინფორმაცია",
    "gui.neoorigins.info.no_origin": "Origin ჯერ არჩეული არ არის.",
    "gui.neoorigins.info.your_origin": "თქვენი Origin",
    "screen.neoorigins.origin_editor": "Origin-ის რედაქტორი",
    "gui.neoorigins.editor.layers_header": "Origin-ის ფენები",
    "gui.neoorigins.editor.powers_header": "არჩევითი ძალები",
    "screen.neoorigins.creator": "Origin-ის შემქმნელი",
    "gui.neoorigins.creator.apply": "გამოყენება",
    "screen.neoorigins.mob_creator": "Mob Origin-ის შემქმნელი",
    "gui.neoorigins.mob_creator.tab.powers": "ძალები",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "გამოჩენის წესები",
    "gui.neoorigins.mob_creator.tab.drops": "ნადავლი",
    "gui.neoorigins.mob_creator.apply": "გამოყენება",
    "gui.neoorigins.debug.powers_header": "მინიჭებული ძალები",

    # Keep canonical Origin identity names stable where literal MT changes the mod identity.
    "origins.neoorigins.human.name": "ადამიანი",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "წყალქვეშ სუნთქვა",
    "power.neoorigins.merling_night_vision.name": "ღრმა ხედვა",
    "power.neoorigins.merling_land_slowdown.name": "ხმელეთზე შენელება",
    "power.neoorigins.merling_dries_out.name": "შრობა",
    "power.neoorigins.avian_no_fall_damage.name": "მსუბუქი წონა",
    "power.neoorigins.avian_hollow_bones.name": "ღრუ ძვლები",
    "power.neoorigins.blazeling_fire_immunity.name": "ცეცხლის გული",
    "power.neoorigins.blazeling_blaze_scales.name": "Blaze-ის ქერცლები",
    "power.neoorigins.blazeling_nether_born.name": "ნეზერში დაბადებული",
    "power.neoorigins.blazeling_nether_born.description": "ნეზერში ყოფნისას უფრო სწრაფად მოძრაობთ.",
    "power.neoorigins.blazeling_night_vision.name": "თერმული ხედვა",
    "power.neoorigins.caveborn_night_vision.name": "სიბნელეს შეჩვეული",
    "power.neoorigins.caveborn_no_fall_damage.name": "გამოქვაბულის ნაბიჯი",
    "power.neoorigins.caveborn_stone_fists.name": "ქვის მუშტები",
    "power.neoorigins.caveborn_mining_fortune.name": "მოპოვების Fortune",
    "power.neoorigins.nether_fungus_diet.name": "ნეზერის სოკოს დიეტა",
    "power.neoorigins.nether_fungus_diet.description": "მრუდე და ჟოლოსფერი სოკოები ნეზერში სათანადო საკვებია — საჭმელად დააწკაპუნეთ მარჯვენა ღილაკით; აღადგენს 5 შიმშილს და 0.6 გაჯერებას. სავსე კუჭით ვერ შეჭამთ.",
    "power.neoorigins.caveborn_eat_copper.name": "სპილენძის გემო",
    "power.neoorigins.caveborn_eat_iron.name": "რკინის გემო",
    "power.neoorigins.caveborn_eat_gold.name": "ოქროს გემო",
    "power.neoorigins.caveborn_eat_diamond.name": "ალმასის გემო",
    "power.neoorigins.caveborn_eat_emerald.name": "ზურმუხტის გემო",
    "power.neoorigins.caveborn_eat_netherite.name": "ნეზერიტის გემო",
    "power.neoorigins.caveborn_netherite_bonus.name": "ნეზერიტის ბირთვი",
    "power.neoorigins.golem_natural_armor.name": "რკინის კანი",

    "origin.origins_furries.komodo.name": "კომოდოს დრაკონი",
    "origin.origins_furries.raccoon.name": "ენოტი",
    "power.origins_furries.charge.name": "სირბილით შეტევა",
    "power.origins_furries.chicken_xp.name": "ქათმის XP",
    "power.origins_furries.low_light_vision.name": "დაბალი განათების ხედვა",
    "power.origins_furries.low_light_vision.description": "ზღვის დონეზე ზემოთ თქვენ იღებთ ღამის ხედვას.",
    "power.origins_furries.pavlov.name": "პავლოვის რეაქცია",
    "power.origins_furries.raccoon_jump.name": "ენოტის ნახტომი",
    "power.origins_furries.night_vision.name": "ღამის ხედვა",
    "power.origins_furries.night_vision.description": "თქვენ გაქვთ ღამის ხედვა.",
    "power.origins_furries.scales.name": "ქერცლები",
    "power.origins_furries.scales.description": "თქვენი ქერცლები გაძლევთ +4 ბუნებრივ ჯავშანს.",
    "power.origins_furries.safe_meat.description": "დამპალი ხორცი და უმი ცხვრის ხორცი უსაფრთხოა საჭმელად.",
    "power.origins_furries.trash_regen.description": "დამპალი ხორცის ჭამისას თქვენ იღებთ რეგენერაციას.",

    "screen.originsmodernui.title": "აირჩიეთ თქვენი Origin",
    "screen.originsmodernui.search_hint": "Origin-ების ძიება...",
    "screen.originsmodernui.choose_prompt": "აირჩიეთ Origin სიიდან",
    "screen.originsmodernui.profile": "პერსონაჟის პროფილი",
    "key.originsmodernui.open_profile": "პერსონაჟის პროფილის გახსნა",
    "key.originsmodernui.toggle_hud": "Origin Architect HUD-ის ჩართვა/გამორთვა",
    "originsmodernui.config.hud.position": "HUD-ის პოზიცია",
    "originsmodernui.config.hud.style": "HUD-ის სტილი",
    "originsmodernui.config.hud.scale": "HUD-ის მასშტაბი",
    "originsmodernui.config.hud.opacity": "HUD-ის გამჭვირვალობა",
    "originsmodernui.config.hud.x_offset": "ჰორიზონტალური წანაცვლება",
    "originsmodernui.config.hud.y_offset": "ვერტიკალური წანაცვლება",
    "originsmodernui.config.hud.show_level": "Origin Architect-ის დონის ჩვენება",
    "originsmodernui.config.hud.show_points": "დაუხარჯავი სტატისტიკის ქულების ჩვენება",
    "originsmodernui.config.hud.show_xp_popup": "XP-ის მატების ამომხტარი ფანჯრის ჩვენება",
    "originsmodernui.config.hud.show_level_popup": "დონის ამაღლების ამომხტარი ფანჯრის ჩვენება",
}

EXACT_VALUE_REPLACEMENTS = {
    "Ცხელი ღილაკი": "სწრაფი ღილაკი",
    "ცხელი ღილაკი": "სწრაფი ღილაკი",
    "Ცხელი კლავიში": "სწრაფი ღილაკი",
    "ცხელი კლავიში": "სწრაფი ღილაკი",
    "პავლოვედი": "პავლოვის რეაქცია",
    "ნეთერიტ": "ნეზერიტ",
    "ნიდერლანდში": "ნეზერში",
}

# MT frequently joins sentences without a space. Georgian has no case distinction,
# so insert a space only when terminal punctuation is immediately followed by a Georgian letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:])(?=[\u10D0-\u10FF\u1C90-\u1CBF])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/ka_ge.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, value)
        for old, new in EXACT_VALUE_REPLACEMENTS.items():
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

print(f"Georgian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
