#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative global corrections for clear Bokmål forms or UI false friends.
SUBSTRING_REPLACEMENTS = {
    "Åpne ": "Opna ",
    "åpne ": "opna ",
    "Vanlig ": "Vanleg ",
    "vanlig ": "vanleg ",
}

# Context-specific Minecraft terminology and obvious machine-conversion mistakes.
OVERRIDES = {
    "effect.neoorigins.suppression": "Undertrykking",
    "neoorigins.suppression.blocked": "Evnene dine er undertrykte.",
    "neoorigins.toggle.on": "Kraft aktivert",
    "neoorigins.toggle.off": "Kraft deaktivert",
    "neoorigins.night_vision.on": "Nattsyn på",
    "neoorigins.night_vision.off": "Nattsyn av",
    "neoorigins.night_vision.no_power": "Opphavet ditt har ikkje nattsynskraft.",
    "neoorigins.ultimine.no_power": "Opphavet ditt kan ikkje grava ut heile malmåra på éin gong.",
    "origins.layer.origin": "Opphav",
    "screen.neoorigins.choose_origin": "Vel opphavet ditt",
    "screen.neoorigins.choose.origins.layer.origin": "Vel opphavet ditt",
    "key.neoorigins.open_mob_creator": "Opna Mob Origin-opprettaren",
    "screen.neoorigins.origin_info": "Opphavsinformasjon",
    "gui.neoorigins.info.your_origin": "Opphavet ditt",
    "screen.neoorigins.origin_editor": "Opphavsredigering",
    "gui.neoorigins.editor.layers_header": "Opphavslag",
    "screen.neoorigins.creator": "Origin-opprettar",
    "gui.neoorigins.creator.apply": "Bruk",
    "gui.neoorigins.mob_creator.apply": "Bruk",
    "gui.neoorigins.mob_creator.tab.drops": "Dropp",
    "origins.gui.impact.low": "Låg",
    "origins.gui.impact.high": "Høg",

    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.blazeling.description": "Fødd av elden i Nether – dekt av svovel, styrkt i det mørke riket, men vatn og regn er giftig.",
    "power.neoorigins.blazeling_nether_born.name": "Netherfødd",
    "power.neoorigins.blazeling_stone_fists.description": "Bare nevar bryt som ei steinhakke – knus stein, malm og netherrack utan verktøy.",
    "power.neoorigins.blazeling_water_damage.name": "Vassveikskap",
    "power.neoorigins.blazeling_water_damage.description": "Vatn er giftig – du tek 1,5 skade per sekund i vatn eller regn.",
    "power.neoorigins.merling_dries_out.description": "Luftmålaren minkar når du er ute av vatnet; blir du verande for lenge på land, byrjar du å kvelast. Regn, ei vassfylt gryte, vasspusting eller ein aktiv conduit i nærleiken hindrar dette.",
    "power.neoorigins.abyssal_dries_out.description": "Luftmålaren minkar når du er ute av vatnet; blir du verande for lenge på land, byrjar du å kvelast. Regn, ei vassfylt gryte, vasspusting eller ein aktiv conduit i nærleiken hindrar dette.",
    "power.neoorigins.enderian_projectile_dodge.name": "Void-steg",
    "power.neoorigins.shulk_levitation_burst.name": "Levitasjonsutbrot",
    "power.neoorigins.shulk_shell_retreat.name": "Skalretrett",

    "secret.inventory": "Hemmeleg lomme",
    "power.origins_furries.charge.name": "Stormløp",
    "power.origins_furries.chicken_xp.name": "Kyllingerfaring",
    "power.origins_furries.eat_trash.name": "Et søppel",
    "power.origins_furries.fish_bonus.name": "Fiskeernæring",
    "power.origins_furries.mutton.name": "Fårekjøtdiett",
    "power.origins_furries.fragile.description": "Du har 2 færre hjarte enn eit menneske.",
    "power.origins_furries.hates_skels.name": "Hatar skjelett",
    "power.origins_furries.heavy_wool.description": "Den tjukke ulla di gir deg +2 naturleg rustning.",
    "power.origins_furries.ignore_water.name": "Som ein fisk i vatnet",
    "power.origins_furries.low_light_vision.description": "Du får nattsyn over havnivå.",
    "power.origins_furries.pavlov.name": "Pavlov-respons",
    "power.origins_furries.poison_attack.name": "Giftangrep",
    "power.origins_furries.raccoon_jump.name": "Vaskebjørnhopp",
    "power.origins_furries.safe_meat.description": "Rote kjøt og rått fårekjøt er trygt å eta.",
    "power.origins_furries.safe_fishes.description": "Rå fisk og kulefisk er trygt å eta.",
    "power.origins_furries.scales.name": "Skjel",
    "power.origins_furries.scales.description": "Skjela dine gir deg +4 naturleg rustning.",
    "power.origins_furries.secret_pocket.name": "Hemmeleg lomme",
    "power.origins_furries.soft.description": "Du har 1 færre hjarte enn eit menneske.",
    "power.origins_furries.starting_wool.name": "Startull",
    "power.origins_furries.water_vision.name": "Vassyn",
}

changed_files = 0
changed_values = 0
for path in sorted(ASSETS.glob("**/lang/nn_no.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = value
        for old, new in SUBSTRING_REPLACEMENTS.items():
            new_value = new_value.replace(old, new)
        if key in OVERRIDES:
            new_value = OVERRIDES[key]
        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Nynorsk refinement complete: {changed_values} values changed across {changed_files} files")
