#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Deterministic contextual corrections for high-visibility UI and known machine
# translation ambiguities. Keep product/proper names when translating them would
# make the UI less recognizable.
OVERRIDES = {
    # NeoOrigins core UI.
    "neoorigins.night_vision.on": "Idjaoaidnu lea álggahuvvon",
    "neoorigins.night_vision.off": "Idjaoaidnu lea heaittihuvvon",
    "neoorigins.night_vision.disabled_by_server": "Idjaoaidnu lea deaktiverejuvvon dán bálvaleaddjis.",
    "neoorigins.night_vision.no_power": "Du álgovuođus ii leat idjaoaidnu.",
    "origins.layer.origin": "Álgu",
    "origins.layer.class": "Ámmát",
    "screen.neoorigins.choose_origin": "Vállje iežat álgovuođu",
    "screen.neoorigins.choose.origins.layer.origin": "Vállje iežat álgovuođu",
    "screen.neoorigins.choose.origins.layer.class": "Vállje iežat ámmáha",
    "gui.neoorigins.sort.class": "Ámmát",
    "key.neoorigins.class_skill": "Ámmátmáhttu",
    "key.neoorigins.open_creator": "Raba álgoálgosaš ráhkadeaddji",
    "key.neoorigins.open_mob_creator": "Raba Mob-álgoálgosaš ráhkadeaddji",
    "key.neoorigins.toggle_night_vision": "Idjaoaidnu ala/eret",
    "screen.neoorigins.creator": "Álgoálgosaš ráhkadeaddji",
    "gui.neoorigins.creator.apply": "Geavahit",
    "screen.neoorigins.mob_creator": "Mob-álgoálgosaš ráhkadeaddji",
    "gui.neoorigins.mob_creator.apply": "Geavahit",

    # Configuration / reward wording.
    "neoorigins.configuration.show_cooldown_countdown": "Čájet áigemearri-lohkama",
    "neoorigins.configuration.cooldown_countdown_opacity": "Áigemearri-lohkama opasitehta (%)",
    "reward.neoorigins.loot_pool": "NeoOrigins: addit rievideami",
    "reward.neoorigins.loot_pool.loot_table": "Rievideami tabealla",

    # iBarn internal attribute effects; these were partially left in English.
    "effect.ibarnorigins.grant_soul_mage_attributes": "Addit sielu noaiddi attribuhtaid",
    "effect.ibarnorigins.revoke_soul_mage_attributes": "Heaittihit sielu noaiddi attribuhtaid",
    "effect.ibarnorigins.grant_sand_person_attributes": "Addit sáivaolbmo attribuhtaid",
    "effect.ibarnorigins.revoke_sand_person_attributes": "Heaittihit sáivaolbmo attribuhtaid",

    # Origins Furries: Google confused "night" with the season "summer".
    "power.origins_furries.night_vision.name": "Idjaoaidnu",
    "power.origins_furries.night_vision.description": "Dus lea idjaoaidnu.",

    # High-visibility Medieval Origins names / descriptions.
    "origin.medievalorigins.high_elf.name": "Alla elf",
    "power.medievalorigins.high_elf.ebonbreath.name": "Čáhppes essensa",
    "tooltip.medievalorigins.stab_bonus": "Čiegus falleheami bonus",
}

# Whole-value/sub-string corrections. Longest/specific phrases are applied first.
VALUE_REPLACEMENTS = [
    ("§l§nOverview§r", "§l§nOppalašgovva§r"),
    ("Unique Abilities", "Erenoamáš návccat"),
    ("Unique Movement", "Erenoamáš lihkadus"),
    ("Unique Flight", "Erenoamáš girdi"),
    ("Dagger Damage", "Dolkkavahágat"),
    ("Doesn't Sleep", "Ii oađđo"),
    ("Unarmed Bonus", "Veahkaválddálaš bonus"),
    ("Nether Bonuses", "Nether-bonusat"),
    ("Ranged Bonuses", "Gaskaboddosaš bonusat"),
    ("Gold Gear Bonuses", "Golliruska-bonusat"),
    ("Crowd Control", "Olmmošjoavkokontrolla"),
    ("Water-Based", "Čáhcevuođđuduvvon"),
    ("Vulnerable Fire", "Buollinváralaš"),
    ("Frost-Based", "Jiekŋavuođđuduvvon"),
    ("Heat Sensitive", "Lieggaceahki"),
    ("Feathered wings", "Dolggiin gokčojuvvon soajit"),
    ("Weak to Undead", "Váibbas jápmániid vuostá"),
    ("Illager Friendly", "Illager-guoibmi"),
    ("Physical Damage", "Fysalaš vahágat"),
    ("Arcane Spell Power", "Čiegus magiijafápmu"),
    ("Frost Spell Power", "Jiekŋamagiijafápmu"),
    ("Soul Sorcerers", "Sielu noaiddit"),
    ("Soul Sorcerer", "Sielu noaidi"),
    ("Sand Person", "Sáivaolmmoš"),
    ("High Elves", "Bajit elliid"),
    ("High Elf", "Alla elf"),
    ("Flight", "Girdi"),
    ("Support", "Doarjja"),
    ("Phasing", "Fásta"),
    ("Undead", "Jápmán"),
    ("Magic", "Magiija"),
    ("Dextrous", "Hárjánan"),
    ("Stealthy", "Čiegus"),
    ("Carnivore", "Biergoealli"),
    ("Mining", "Ruvkedoaibma"),
    ("Caving", "Roggan"),
    ("Speed", "Leahttu"),
    ("Vegetarian", "Vegetariána"),
    ("Loved by Mobs", "Mobbat ráhkistit"),
    ("Ax Bonuses", "Ákšu bonusat"),
    ("Axe Bonuses", "Ákšu bonusat"),
    ("Defense", "Suodjalus"),
    ("Odd", "Eahpedábálaš"),
    ("Summons", "Gohččumat"),
    ("Complex", "Kompleaksa"),
    ("Reputation", "Dovdomearka"),
    ("Utility", "Ávkkástallan"),
    ("Tanky", "Gierdavaš"),
    ("Healing", "Buorideapmi"),
    ("Armor", "Suodjalus"),
]

# Values that are intentionally technical/proper names and should not trigger
# generic replacement decisions.
CANONICAL = {
    "NeoOrigins", "Origin Architect", "JSON", "HUD", "JEI", "EMI", "Ultimine",
    "Alfiq", "Banshee", "Fae", "Pixie", "Yeti", "Cinderborn", "Elytrian",
    "Sculkborn", "Warden", "Wither", "Enderian", "Enderite", "Nether",
}

changed_files = 0
changed_values = 0
hotkey_fixes = 0

for path in sorted(ASSETS.glob("**/lang/se_no.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = OVERRIDES.get(key, str(value))

        # Normalize numbered hotkey labels; the bootstrap translated some but
        # left others as English depending on batching/capitalization.
        match = re.fullmatch(r"key\.neoorigins\.hotkey\.(\d+)", key)
        if match:
            wanted = f"Čujuhus {int(match.group(1)):02d}"
            if new_value != wanted:
                new_value = wanted
                hotkey_fixes += 1

        # Medieval Origins uses compact English feature summaries embedded in
        # otherwise translated prose. Replace only known high-confidence terms.
        if path.parts[-3] == "medievalorigins" or key.startswith("origin.medievalorigins."):
            for old, new in VALUE_REPLACEMENTS:
                new_value = new_value.replace(old, new)

        # A few add-on values contain these role names inside otherwise Sami text.
        if path.parts[-3] == "ibarnorigins":
            new_value = new_value.replace("Soul Sorcerers", "Sielu noaiddit")
            new_value = new_value.replace("Soul Sorcerer", "Sielu noaidi")
            new_value = new_value.replace("Sand Person", "Sáivaolmmoš")

        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(
    f"Northern Sami refinement complete: {changed_values} values changed across "
    f"{changed_files} files; {hotkey_fixes} hotkey labels normalized"
)
