#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative context-specific corrections for machine-translation false friends
# and Minecraft terminology. Proper names such as Nether/Netherite are retained
# when that is clearer than an unreliable literal translation.
OVERRIDES = {
    "neoorigins.toggle.on": "Kraftur virkur",
    "neoorigins.toggle.off": "Kraftur óvirkur",
    "neoorigins.night_vision.no_power": "Uppruni þinn hefur ekki nætursjónarkraft.",
    "neoorigins.ultimine.no_power": "Uppruni þinn getur ekki grafið heila málmgrýtisæð í einu.",
    "origins.layer.origin": "Uppruni",
    "origins.layer.class": "Flokkur",
    "screen.neoorigins.choose.origins.layer.class": "Veldu flokkinn þinn",
    "gui.neoorigins.sort.class": "Flokkur",
    "key.neoorigins.open_creator": "Opna upprunaskaparann",
    "key.neoorigins.open_mob_creator": "Opna Mob-upprunaskaparann",
    "screen.neoorigins.origin_info": "Upprunaupplýsingar",
    "screen.neoorigins.origin_editor": "Upprunaritill",
    "screen.neoorigins.creator": "Upprunaskapari",
    "gui.neoorigins.creator.apply": "Nota",
    "screen.neoorigins.mob_creator": "Mob-upprunaskapari",
    "gui.neoorigins.mob_creator.apply": "Nota",
    "gui.neoorigins.mob_creator.tab.drops": "Fengur",

    "origins.neoorigins.blazeling.name": "Blazeling",
    "origins.neoorigins.blazeling.description": "Fæddur úr eldum Nether — hlaðinn brennisteini og styrktur í myrka ríkinu, en vatn og rigning eru honum eitur.",
    "power.neoorigins.merling_land_slowdown.name": "Landkrabbi",
    "power.neoorigins.merling_dries_out.description": "Loftmælirinn lækkar þegar þú ert utan vatns; ef þú ert of lengi á landi byrjarðu að kafna. Rigning, vatnsfylltur ketill, vatnsöndun eða virk conduit í nágrenninu kemur í veg fyrir þetta.",
    "power.neoorigins.blazeling_blaze_scales.name": "Blaze-hreistur",
    "power.neoorigins.blazeling_nether_born.name": "Fæddur í Nether",
    "power.neoorigins.blazeling_nether_born.description": "Þú hreyfir þig hraðar þegar þú ert í Nether.",
    "power.neoorigins.blazeling_stone_fists.description": "Berar hendur þínar brjóta eins og steinhaki — þú getur brotið stein, málmgrýti og netherrack án verkfæra.",
    "power.neoorigins.enderian_projectile_dodge.name": "Void-skref",
    "power.neoorigins.enderian_teleport.description": "Fjarskiptist þangað sem þú horfir, allt að 50 blokkir. Kostar 2 orku. Kólnun: 3 sekúndur.",
    "power.neoorigins.caveborn_mining_speed.name": "Námumannshendur",
    "power.neoorigins.nether_fungus_diet.description": "Warped- og Crimson-sveppir eru góð máltíð í Nether — hægrismelltu til að borða þá og fá 5 hungur og 0,6 mettun. Þú getur ekki borðað þá þegar þú ert saddur.",
    "power.neoorigins.caveborn_eat_gold.description": "Þú getur borðað gullhleifa, hrátt gull, gullmola, gullgrýti, djúpskífugullgrýti, Nether-gullgrýti og hráa gullkubba — þetta er ríkari næring. Þú getur ekki borðað þegar þú ert saddur.",
    "power.neoorigins.caveborn_eat_netherite.name": "Netherít-bragð",
    "power.neoorigins.caveborn_eat_netherite.description": "Þú getur borðað netherít-hleifa, netherít-brot og Ancient Debris — ríkustu máltíðina í heiminum. Þú getur ekki borðað þegar þú ert saddur.",
    "power.neoorigins.caveborn_iron_bonus.description": "Að borða járn veitir Haste I í 60 sekúndur.",
    "power.neoorigins.caveborn_netherite_bonus.name": "Netherít-kjarni",
    "power.neoorigins.caveborn_netherite_bonus.description": "Að borða netherít veitir Strength I og Resistance I í 5 mínútur.",

    "origin.origins_furries.raccoon.description": "Þvottabirnir eru stundum kallaðir „ruslpöndur“.",
    "origin.origins_furries.raccoon.name": "Þvottabjörn",
    "secret.inventory": "Leynivasi",
    "power.origins_furries.charge.description": "Þú veldur meiri skaða þegar þú hleypur á spretti.",
    "power.origins_furries.charge.name": "Áhlaup",
    "power.origins_furries.chicken_xp.description": "Þú færð tvöfalt XP fyrir að drepa hænur.",
    "power.origins_furries.chicken_xp.name": "Kjúklinga-XP",
    "power.origins_furries.eat_trash.description": "Rotið hold og eitraðar kartöflur er óhætt fyrir þig að borða.",
    "power.origins_furries.fish_bonus.name": "Fiskanæring",
    "power.origins_furries.fragile.description": "Hámarksheilsa þín er 2 hjörtum lægri en hjá manneskju.",
    "power.origins_furries.heavy_wool.description": "Þykk ullin þín veitir +2 náttúrulega brynju.",
    "power.origins_furries.ignore_water.name": "Eins og fiskur í vatni",
    "power.origins_furries.low_light_vision.description": "Þú færð nætursjón þegar þú ert yfir sjávarmáli.",
    "power.origins_furries.low_light_vision.name": "Nætursjón",
    "power.origins_furries.pavlov.name": "Pavlov-svörun",
    "power.origins_furries.raccoon_jump.name": "Þvottabjarnarstökk",
    "power.origins_furries.safe_bush.description": "Sætberjarunnar skaða þig ekki.",
    "power.origins_furries.safe_meat.description": "Rotið hold og hrátt kindakjöt er óhætt fyrir þig að borða.",
    "power.origins_furries.scales.name": "Hreistur",
    "power.origins_furries.scales.description": "Hreistrið þitt veitir +4 náttúrulega brynju.",
    "power.origins_furries.secret_pocket.name": "Leynivasi",
    "power.origins_furries.night_vision.description": "Þú hefur nætursjón.",
    "power.origins_furries.night_vision.name": "Nætursjón",
    "power.origins_furries.soft.description": "Hámarksheilsa þín er 1 hjarta lægri en hjá manneskju.",
    "power.origins_furries.water_vision.name": "Vatnssýn",
}

changed_files = 0
changed_values = 0
for path in sorted(ASSETS.glob("**/lang/is_is.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        if key not in OVERRIDES:
            continue
        new_value = OVERRIDES[key]
        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Icelandic refinement complete: {changed_values} values changed across {changed_files} files")
