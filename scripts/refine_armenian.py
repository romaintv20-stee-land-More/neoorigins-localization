#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative contextual corrections for machine-translation false friends and
# Minecraft/Origins terminology. Canonical mod/game names are intentionally kept
# where a literal translation changes the identity or meaning of the term.
OVERRIDES = {
    "neoorigins.toggle.on": "Ուժը միացված է",
    "neoorigins.toggle.off": "Ուժը անջատված է",
    "neoorigins.night_vision.on": "Գիշերային տեսողությունը միացված է",
    "neoorigins.night_vision.off": "Գիշերային տեսողությունը անջատված է",
    "neoorigins.night_vision.disabled_by_server": "Գիշերային տեսողությունն անջատված է այս սերվերում։",
    "neoorigins.night_vision.no_power": "Ձեր Origin-ը չունի Գիշերային տեսողության ուժ։",
    "neoorigins.ultimine.no_power": "Ձեր Origin-ը չունի Ultimine ուժ։",
    "origins.layer.origin": "Origin",
    "origins.layer.class": "Դաս",
    "screen.neoorigins.choose_origin": "Ընտրեք ձեր Origin-ը",
    "screen.neoorigins.choose.origins.layer.origin": "Ընտրեք ձեր Origin-ը",
    "screen.neoorigins.choose.origins.layer.class": "Ընտրեք ձեր դասը",
    "gui.neoorigins.search.label": "Origin-ի որոնում",
    "gui.neoorigins.picker.no_results": "Ոչ մի Origin չի համապատասխանում ձեր որոնմանը",
    "gui.neoorigins.hint.select": "Ընտրեք Origin՝ մանրամասները տեսնելու համար",
    "gui.neoorigins.detail.powers_header": "Ուժեր",
    "gui.neoorigins.sort.class": "Դաս",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "Դասի հմտություն",
    "key.neoorigins.view_info": "Դիտել Origin-ի տեղեկությունները",
    "key.neoorigins.open_creator": "Բացել Origin ստեղծիչը",
    "key.neoorigins.open_mob_creator": "Բացել Mob Origin ստեղծիչը",
    "key.neoorigins.toggle_night_vision": "Միացնել/անջատել Գիշերային տեսողությունը",
    "key.category.neoorigins.hotkeys": "NeoOrigins (արագ ստեղներ)",
    "screen.neoorigins.origin_info": "Origin-ի տեղեկություններ",
    "gui.neoorigins.info.no_origin": "Origin դեռ ընտրված չէ։",
    "gui.neoorigins.info.your_origin": "Ձեր Origin-ը",
    "screen.neoorigins.origin_editor": "Origin խմբագրիչ",
    "gui.neoorigins.editor.layers_header": "Origin շերտեր",
    "gui.neoorigins.editor.powers_header": "Ընտրովի ուժեր",
    "screen.neoorigins.creator": "Origin ստեղծիչ",
    "gui.neoorigins.creator.apply": "Կիրառել",
    "screen.neoorigins.mob_creator": "Mob Origin ստեղծիչ",
    "gui.neoorigins.mob_creator.tab.powers": "Ուժեր",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Spawn-ի կանոններ",
    "gui.neoorigins.mob_creator.tab.drops": "Գցվող իրեր",
    "gui.neoorigins.mob_creator.apply": "Կիրառել",
    "gui.neoorigins.debug.powers_header": "Տրված ուժեր",

    # Canonical Origin identities. Literal MT frequently turns these into
    # ordinary Armenian nouns/adjectives, losing the mod's identity names.
    "origins.neoorigins.human.name": "Մարդ",
    "origins.neoorigins.merling.name": "Merling",
    "origins.neoorigins.avian.name": "Avian",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.elytrian.name": "Elytrian",
    "origins.neoorigins.enderian.name": "Enderian",
    "origins.neoorigins.arachnid.name": "Arachnid",
    "origins.neoorigins.shulk.name": "Shulk",
    "origins.neoorigins.phantom.name": "Phantom",

    "power.neoorigins.merling_water_breathing.name": "Ջրային շնչառություն",
    "power.neoorigins.merling_night_vision.name": "Խորքային տեսողություն",
    "power.neoorigins.merling_land_slowdown.name": "Դանդաղ ցամաքում",
    "power.neoorigins.merling_dries_out.name": "Չորանում է",
    "power.neoorigins.avian_no_fall_damage.name": "Թեթև քաշ",
    "power.neoorigins.avian_hollow_bones.name": "Սնամեջ ոսկորներ",
    "power.neoorigins.blazeling_fire_immunity.name": "Կրակի սիրտ",
    "power.neoorigins.blazeling_nether_born.name": "Ծնված Nether-ում",
    "power.neoorigins.blazeling_nether_born.description": "Դուք ավելի արագ եք շարժվում, երբ Nether-ում եք։",
    "power.neoorigins.blazeling_night_vision.name": "Ջերմային տեսողություն",
    "power.neoorigins.caveborn_night_vision.name": "Վարժված մթությանը",
    "power.neoorigins.caveborn_no_fall_damage.name": "Քարանձավային քայլք",
    "power.neoorigins.caveborn_stone_fists.name": "Քարե բռունցքներ",
    "power.neoorigins.caveborn_mining_fortune.name": "Mining Fortune",
    "power.neoorigins.nether_fungus_diet.name": "Nether սնկերի սննդակարգ",
    "power.neoorigins.caveborn_eat_netherite.name": "Netherite-ի համ",
    "power.neoorigins.caveborn_netherite_bonus.name": "Netherite-ի սիրտ",
    "power.neoorigins.enderian_ender_eyes.name": "Ender Eyes",
    "power.neoorigins.golem_natural_armor.name": "Երկաթե մաշկ",

    "origin.origins_furries.komodo.name": "Կոմոդո վիշապ",
    "origin.origins_furries.raccoon.name": "Ջրարջ",
    "power.origins_furries.charge.name": "Վազքային գրոհ",
    "power.origins_furries.chicken_xp.name": "Հավի XP",
    "power.origins_furries.low_light_vision.name": "Ցածր լուսավորության տեսողություն",
    "power.origins_furries.low_light_vision.description": "Ծովի մակարդակից բարձր դուք ստանում եք Գիշերային տեսողություն։",
    "power.origins_furries.pavlov.name": "Պավլովի արձագանք",
    "power.origins_furries.raccoon_jump.name": "Ջրարջի ցատկ",
    "power.origins_furries.night_vision.name": "Գիշերային տեսողություն",
    "power.origins_furries.night_vision.description": "Դուք ունեք Գիշերային տեսողություն։",
    "power.origins_furries.scales.name": "Թեփուկներ",
    "power.origins_furries.scales.description": "Ձեր թեփուկները տալիս են +4 բնական զրահ։",
    "power.origins_furries.safe_meat.description": "Փտած միսը և հում ոչխարի միսը անվտանգ են ուտելու համար։",
    "power.origins_furries.trash_regen.description": "Փտած միս ուտելիս դուք ստանում եք Regeneration։",

    "screen.originsmodernui.title": "Ընտրեք ձեր Origin-ը",
    "screen.originsmodernui.search_hint": "Որոնել Origin-ներ...",
    "screen.originsmodernui.choose_prompt": "Ընտրեք Origin ցուցակից",
    "screen.originsmodernui.profile": "Կերպարի պրոֆիլ",
    "key.originsmodernui.open_profile": "Բացել կերպարի պրոֆիլը",
    "key.originsmodernui.toggle_hud": "Միացնել/անջատել HUD-ը",
    "originsmodernui.config.hud.position": "HUD-ի դիրք",
    "originsmodernui.config.hud.style": "HUD-ի ոճ",
    "originsmodernui.config.hud.scale": "HUD-ի մասշտաբ",
    "originsmodernui.config.hud.opacity": "HUD-ի անթափանցիկություն",
    "originsmodernui.config.hud.show_level": "Ցույց տալ մակարդակը",
    "originsmodernui.config.hud.show_points": "Ցույց տալ չօգտագործված վիճակագրության միավորները",
    "originsmodernui.config.hud.show_xp_popup": "Ցույց տալ XP-ի ելնող պատուհանը",
    "originsmodernui.config.hud.show_level_popup": "Ցույց տալ մակարդակի բարձրացման ելնող պատուհանը",
}

EXACT_VALUE_REPLACEMENTS = {
    "Գիշերային տեսլական": "Գիշերային տեսողություն",
    "Գիշերային տեսիլք": "Գիշերային տեսողություն",
    "Պավլովեդ": "Պավլովի արձագանք",
}

# Batch translation occasionally joins two sentences. Insert a space only when
# terminal punctuation is immediately followed by an uppercase Armenian letter.
SENTENCE_JOIN = re.compile(r"(?<=[.!?:։])(?=[\u0531-\u0556])")

changed_files = 0
changed_values = 0
spacing_fixes = 0
for path in sorted(ASSETS.glob("**/lang/hy_am.json")):
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

print(f"Armenian refinement complete: {changed_values} values changed across {changed_files} files; {spacing_fixes} spacing fixes")
