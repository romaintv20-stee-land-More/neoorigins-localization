#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative global fixes for unambiguous machine-translation false friends.
EXACT_VALUE_REPLACEMENTS = {
    "बिजली अक्षम": "शक्ति अक्षम",
    "आवेदन करें": "लागू करें",
    "बूँदें": "लूट",
    "एक प्रकार का जानवर": "रैकून",
}

SUBSTRING_REPLACEMENTS = {
    # Google-style translation sometimes interprets Minecraft's Nether as the Netherlands.
    "नीदरलैंड": "नेदर",
}

# Key-specific corrections where English game terminology was mistranslated or lost.
OVERRIDES = {
    "neoorigins.toggle.on": "शक्ति सक्षम",
    "neoorigins.toggle.off": "शक्ति अक्षम",
    "neoorigins.night_vision.no_power": "आपके ओरिजिन में रात्रि दृष्टि की शक्ति नहीं है।",
    "neoorigins.ultimine.no_power": "आपका ओरिजिन एक साथ पूरी अयस्क-शिरा का खनन नहीं कर सकता।",
    "origins.layer.origin": "ओरिजिन",
    "origins.layer.class": "क्लास",
    "screen.neoorigins.choose_origin": "अपना ओरिजिन चुनें",
    "screen.neoorigins.choose.origins.layer.origin": "अपना ओरिजिन चुनें",
    "screen.neoorigins.choose.origins.layer.class": "अपनी क्लास चुनें",
    "gui.neoorigins.search.label": "ओरिजिन खोजें",
    "gui.neoorigins.picker.no_results": "कोई ओरिजिन आपकी खोज से मेल नहीं खाता",
    "gui.neoorigins.hint.select": "विवरण देखने के लिए कोई ओरिजिन चुनें",
    "gui.neoorigins.editor.on": "चालू",
    "gui.neoorigins.editor.off": "बंद",
    "gui.neoorigins.creator.apply": "लागू करें",
    "gui.neoorigins.mob_creator.apply": "लागू करें",
    "gui.neoorigins.mob_creator.tab.drops": "लूट",
    "origins.gui.impact.low": "कम",
    "origins.gui.impact.high": "अधिक",

    "power.neoorigins.feline_mobs_ignore.description": "क्रीपर तुमसे डरते हैं और तुम्हारे पास नहीं आते।",
    "power.neoorigins.merling_land_slowdown.name": "ज़मीन पर धीमापन",
    "power.neoorigins.blazeling_nether_born.name": "नेदर में जन्मा",
    "power.neoorigins.nether_fungus_diet.description": "वार्प्ड और क्रिमसन फंगस नेदर में उचित भोजन हैं — 5 भूख और 0.6 संतृप्ति के लिए खाने हेतु राइट-क्लिक करें। पेट भरा होने पर इन्हें नहीं खाया जा सकता।",
    "power.neoorigins.caveborn_eat_gold.description": "सोने की सिल्लियां, कच्चा सोना, सोने की डली, सोने का अयस्क, डीपस्लेट सोने का अयस्क, नेदर गोल्ड अयस्क और कच्चे सोने के ब्लॉक खा सकते हैं — यह अधिक समृद्ध भोजन है। पेट भरा होने पर इन्हें नहीं खाया जा सकता।",
    "power.neoorigins.caveborn_eat_netherite.name": "नेथराइट का स्वाद",
    "power.neoorigins.caveborn_eat_netherite.description": "नेथराइट की सिल्लियां, नेथराइट स्क्रैप और प्राचीन मलबा खा सकते हैं — यह दुनिया का सबसे समृद्ध भोजन है। पेट भरा होने पर इन्हें नहीं खाया जा सकता।",
    "power.neoorigins.caveborn_iron_bonus.description": "लोहा खाने से 60 सेकंड के लिए जल्दबाज़ी I मिलती है।",
    "power.neoorigins.merling_dries_out.description": "पानी से बाहर रहने पर आपकी हवा लगातार घटती है; बहुत देर बाहर रहने पर आपका दम घुटने लगता है। बारिश, पानी से भरी कड़ाही, जल श्वसन या पास का सक्रिय कंड्यूट इसे रोकते हैं।",
    "power.neoorigins.abyssal_dries_out.description": "पानी से बाहर रहने पर आपकी हवा लगातार घटती है; बहुत देर बाहर रहने पर आपका दम घुटने लगता है। बारिश, पानी से भरी कड़ाही, जल श्वसन या पास का सक्रिय कंड्यूट इसे रोकते हैं।",
    "origins.neoorigins.voidwalker.description": "एंड से स्पर्शित एक प्राणी — ब्लॉकों के आर-पार गुजर सकता है, कम दूरी पर तुरंत टेलीपोर्ट कर सकता है और अधिकांश खतरों की नज़र से बचकर चलता है। बिना थके दौड़ सकता है, लेकिन पानी उसके लिए पीड़ादायक है।",
    "power.neoorigins.voidwalker_active_teleport.description": "जहाँ आप देख रहे हैं वहाँ तुरंत टेलीपोर्ट करता है (अधिकतम 24 ब्लॉक)। 2 ऊर्जा खर्च होती है। कूलडाउन 80 टिक है।",
    "power.neoorigins.voidwalker_water_damage.name": "शून्य-दाह",
    "power.neoorigins.abyssal_land_speed_penalty.name": "स्थलचर",

    "origin.origins_furries.raccoon.name": "रैकून",
    "power.origins_furries.charge.description": "दौड़ते समय आप अधिक क्षति पहुँचाते हैं।",
    "power.origins_furries.charge.name": "धावा",
    "power.origins_furries.chicken_xp.description": "मुर्गियों को मारने पर आपको दोगुना अनुभव मिलता है।",
    "power.origins_furries.fragile.description": "आपका अधिकतम स्वास्थ्य एक इंसान से 2 दिल कम है।",
    "power.origins_furries.low_light_vision.description": "समुद्र तल से ऊपर होने पर आपको रात्रि दृष्टि मिलती है।",
    "power.origins_furries.pavlov.description": "गाँव की घंटी बजाने पर भूख के बदले आपका स्वास्थ्य ठीक होता है।",
    "power.origins_furries.scales.name": "शल्क",
    "power.origins_furries.scales.description": "आपके शल्क आपको +4 प्राकृतिक कवच देते हैं।",
}

changed_files = 0
changed_values = 0
for path in sorted(ASSETS.glob("**/lang/hi_in.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, value in list(data.items()):
        new_value = EXACT_VALUE_REPLACEMENTS.get(value, value)
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

print(f"Hindi refinement complete: {changed_values} values changed across {changed_files} files")
