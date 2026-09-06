#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/neoorigins_26_2/lang"

DATA = {
    "it_it": {
        "skill": "Abilità",
        "category": "NeoOrigins (Scorciatoie)",
        "hotkey": "Scorciatoia",
        "orb": "Reimposta tutte le selezioni dell'origine e riapre la schermata di scelta dell'origine. Costa 5 livelli di XP per ogni utilizzo precedente (il primo utilizzo è gratuito). Si consuma all'uso.",
    },
    "pl_pl": {
        "skill": "Umiejętność",
        "category": "NeoOrigins (Skróty klawiszowe)",
        "hotkey": "Skrót",
        "orb": "Resetuje wszystkie wybory pochodzenia i ponownie otwiera ekran wyboru pochodzenia. Kosztuje 5 poziomów PD za każde wcześniejsze użycie (pierwsze użycie jest darmowe). Zostaje zużyta po użyciu.",
    },
    "ru_ru": {
        "skill": "Навык",
        "category": "NeoOrigins (Горячие клавиши)",
        "hotkey": "Горячая клавиша",
        "orb": "Сбрасывает все выбранные происхождения и снова открывает экран выбора происхождения. Стоимость — 5 уровней опыта за каждое предыдущее использование (первое использование бесплатно). Расходуется при использовании.",
    },
    "zh_cn": {
        "skill": "技能",
        "category": "NeoOrigins（快捷键）",
        "hotkey": "快捷键",
        "orb": "重置所有起源选择并重新打开起源选择界面。每次此前使用都会增加 5 级经验消耗（首次使用免费）。使用后会被消耗。",
    },
}

for locale, values in DATA.items():
    path = LANG / f"{locale}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["key.neoorigins.skill_5"] = f"{values['skill']} 5"
    data["key.neoorigins.skill_6"] = f"{values['skill']} 6"
    data["key.category.neoorigins.hotkeys"] = values["category"]
    for i in range(1, 65):
        data[f"key.neoorigins.hotkey.{i}"] = f"{values['hotkey']} {i:02d}"
    data["emi.neoorigins.orb_of_origin.info"] = values["orb"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

tr_path = LANG / "tr_tr.json"
tr = json.loads(tr_path.read_text(encoding="utf-8"))
tr.update({
    "neoorigins.configuration.section.neoorigins.gameplay.toml": "Oynanış",
    "neoorigins.configuration.section.neoorigins.gameplay.toml.title": "NeoOrigins Oynanış Ayarları",
    "neoorigins.configuration.section.neoorigins.admin.toml": "Yönetici ve İzinler",
    "neoorigins.configuration.section.neoorigins.admin.toml.title": "NeoOrigins Yönetici Ayarları",
    "neoorigins.configuration.section.neoorigins.power.overrides.toml": "Güç Geçersiz Kılmaları",
    "neoorigins.configuration.section.neoorigins.power.overrides.toml.title": "NeoOrigins Güç Geçersiz Kılmaları",
    "neoorigins.configuration.section.neoorigins.content.toml": "Originler ve Sınıflar",
    "neoorigins.configuration.section.neoorigins.content.toml.title": "NeoOrigins Origin ve Sınıf Açma/Kapama Ayarları",
    "neoorigins.configuration.section.neoorigins.client.toml": "İstemci Görünümü",
    "neoorigins.configuration.section.neoorigins.client.toml.title": "NeoOrigins İstemci Ayarları",
    "neoorigins.configuration.show_cooldown_countdown": "Bekleme süresi geri sayımını göster",
    "neoorigins.configuration.cooldown_countdown_opacity": "Bekleme süresi geri sayımı opaklığı (%)",
    "neoorigins.configuration.hud_ability_display": "Yetenek HUD görüntüleme modu",
    "neoorigins.configuration.always_show_ability_icons": "Yetenek simgelerini her zaman göster",
})
tr_path.write_text(json.dumps(tr, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("26.2 delta translations applied for it_it, pl_pl, ru_ru, tr_tr and zh_cn.")
