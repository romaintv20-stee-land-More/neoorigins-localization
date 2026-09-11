#!/usr/bin/env python3
from pathlib import Path
import json
import re
import time
import urllib.error
import urllib.request

from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
LOCALE = "zh_tw"

# Use the maintained Simplified Chinese NeoOrigins locale as a semantic source,
# then convert it with Taiwan phrase rules. This avoids isolated-word mistakes
# such as Origin -> place of origin, Power -> authority, Class -> school class.
NEO_REFS = {
    "1.21.1": "af467a3bc118f6bbc0970d68f7e03fa631d7e6f2",
    "26.1": "aa207ef14cf3b938e28b4081162701953957c1d5",
    "26.2": "511cadcafe3027d2a56b4448652ec9b74e2f3b07",
}
BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/zh_cn.json"
CONVERTER = OpenCC("s2twp")


def fetch_json(url: str, attempts: int = 4):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Localization-Refiner"})
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.load(response)
        except (urllib.error.URLError, urllib.error.HTTPError, ConnectionResetError, TimeoutError) as exc:
            last_error = exc
            if attempt == attempts:
                raise
            delay = 2 ** (attempt - 1)
            print(f"Transient zh_cn fetch error ({attempt}/{attempts}): {exc}; retrying in {delay}s")
            time.sleep(delay)
    raise last_error


UPSTREAM_ZH_CN = {version: fetch_json(BASE.format(ref=ref)) for version, ref in NEO_REFS.items()}

# Deterministic Taiwan-localized wording for high-visibility UI and keys that
# are absent/newer upstream, plus add-on strings where machine translation lost
# the gameplay meaning.
OVERRIDES = {
    # Core UI / terminology.
    "neoorigins.toggle.on": "能力已啟用",
    "neoorigins.toggle.off": "能力已停用",
    "neoorigins.night_vision.on": "夜視已開啟",
    "neoorigins.night_vision.off": "夜視已關閉",
    "neoorigins.night_vision.disabled_by_server": "此伺服器已停用夜視。",
    "neoorigins.night_vision.no_power": "你的起源沒有夜視能力。",
    "neoorigins.ultimine.no_power": "你的起源無法使用連鎖挖掘。",
    "neoorigins.configuration.sun_damage.helmet_protection": "頭盔防護",
    "neoorigins.configuration.helmet_protection": "頭盔防護",
    "origins.layer.origin": "起源",
    "origins.layer.class": "職業",
    "screen.neoorigins.choose_origin": "選擇你的起源",
    "screen.neoorigins.choose.origins.layer.origin": "選擇你的起源",
    "screen.neoorigins.choose.origins.layer.class": "選擇你的職業",
    "button.neoorigins.edit_hud": "編輯 HUD",
    "gui.neoorigins.search.label": "搜尋起源",
    "gui.neoorigins.picker.no_results": "找不到符合搜尋條件的起源",
    "gui.neoorigins.hint.select": "選擇一個起源以查看詳細資訊",
    "gui.neoorigins.detail.powers_header": "能力",
    "gui.neoorigins.sort.class": "職業",
    "key.category.neoorigins.neoorigins": "NeoOrigins",
    "key.neoorigins.class_skill": "職業技能",
    "key.neoorigins.view_info": "查看起源資訊",
    "key.neoorigins.edit_hud": "編輯 HUD",
    "key.neoorigins.open_creator": "開啟起源建立器",
    "key.neoorigins.open_mob_creator": "開啟生物起源建立器",
    "key.neoorigins.toggle_night_vision": "切換夜視",
    "key.category.neoorigins.hotkeys": "NeoOrigins（快捷鍵）",
    "screen.neoorigins.hud_editor": "HUD 編輯器 - 拖曳以重新定位",
    "screen.neoorigins.hud_editor.scale": "縮放：%s%%",
    "screen.neoorigins.origin_info": "起源資訊",
    "screen.neoorigins.debug_powers": "已啟用的能力（偵錯）",
    "gui.neoorigins.info.no_origin": "尚未選擇起源。",
    "gui.neoorigins.info.your_origin": "你的起源",
    "screen.neoorigins.origin_editor": "起源編輯器",
    "gui.neoorigins.editor.layers_header": "起源層級",
    "gui.neoorigins.editor.powers_header": "切換能力",
    "screen.neoorigins.creator": "起源建立器",
    "gui.neoorigins.creator.tab.powers": "能力",
    "gui.neoorigins.creator.tab.layer": "層級",
    "gui.neoorigins.creator.apply": "套用",
    "screen.neoorigins.mob_creator": "生物起源建立器",
    "gui.neoorigins.mob_creator.tab.powers": "能力",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "生成規則",
    "gui.neoorigins.mob_creator.tab.drops": "掉落物",
    "gui.neoorigins.mob_creator.apply": "套用",
    "gui.neoorigins.debug.capabilities_header": "已啟用的能力",
    "gui.neoorigins.debug.powers_header": "已授予的能力",

    # iBarn Origins: semantic fixes for isolated-word machine translations.
    "effect.ibarnorigins.inflation_effect": "膨脹",
    "effect.ibarnorigins.grant_soul_mage_attributes": "賦予靈魂法師屬性",
    "effect.ibarnorigins.revoke_soul_mage_attributes": "移除靈魂法師屬性",
    "effect.ibarnorigins.grant_sand_person_attributes": "賦予沙人屬性",
    "effect.ibarnorigins.revoke_sand_person_attributes": "移除沙人屬性",
    "entity.ibarnorigins.homing_wither_skull": "追蹤凋零骷髏頭",
    "power.ibarnorigins.ghasterfireball.name": "火球具現",
    "power.ibarnorigins.ghasterinflate.name": "充氣",
    "power.ibarnorigins.sandman_attributes.name": "與沙合一",
    "power.ibarnorigins.sandman_shovel_damage.name": "鏟子弱點",
    "power.ibarnorigins.soulmage_fireweakness.name": "火焰弱點",
    "power.ibarnorigins.soulmage_vegetarian.name": "偏好素食",
    "power.ibarnorigins.witherskull.name": "追蹤凋零骷髏頭",
    "power.ibarnorigins.wp_item_prevention.name": "裝甲限制",
    "power.ibarnorigins.wpairswim.name": "飛行",
}

VALUE_REPLACEMENTS = {
    "Neorigins": "NeoOrigins",
    "Neoorigins": "NeoOrigins",
    "Mob Origin Creator": "生物起源建立器",
}


def source_for_path(path: Path):
    namespace = path.parts[path.parts.index("assets") + 1]
    if namespace.startswith("neoorigins_zhtw_common_") or namespace == "neoorigins_zhtw_121":
        return UPSTREAM_ZH_CN["1.21.1"]
    if namespace == "neoorigins_26_1":
        return UPSTREAM_ZH_CN["26.1"]
    if namespace == "neoorigins_26_2":
        return UPSTREAM_ZH_CN["26.2"]
    return None


changed_files = 0
changed_values = 0
upstream_semantic_values = 0
normalized_values = 0
english_candidates = []
english_title = re.compile(r"^[A-Za-z][A-Za-z0-9 &'’:+/()._-]{1,70}$")
allowed_english = {
    "NeoOrigins", "Origin Architect", "JSON", "Ultimine", "Alfiq", "Banshee", "Fae", "Pixie", "Yeti",
    "Cinderborn", "Elytrian", "Sculkborn", "Warden", "Wither", "Enderian", "Enderite",
}

files = sorted(ASSETS.glob(f"**/lang/{LOCALE}.json"))
for path in files:
    data = json.loads(path.read_text(encoding="utf-8"))
    source = source_for_path(path)
    changed = False
    for key, value in list(data.items()):
        new_value = value

        # First normalize every fallback value to Taiwan Traditional Chinese.
        converted = CONVERTER.convert(new_value)
        if converted != new_value:
            normalized_values += 1
        new_value = converted

        # For NeoOrigins, prefer the project's maintained official zh_cn wording
        # as the semantic base, then convert it to Taiwan Traditional Chinese.
        if source is not None and key in source:
            semantic = CONVERTER.convert(str(source[key]))
            if semantic != new_value:
                upstream_semantic_values += 1
            new_value = semantic

        new_value = OVERRIDES.get(key, new_value)
        for old, new in VALUE_REPLACEMENTS.items():
            new_value = new_value.replace(old, new)

        if new_value != value:
            data[key] = new_value
            changed = True
            changed_values += 1

        stripped = re.sub(r"§.", "", new_value).strip()
        if english_title.fullmatch(stripped) and stripped not in allowed_english:
            english_candidates.append((key, stripped))

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(
    "Traditional Chinese refinement complete: "
    f"{changed_values} values changed across {changed_files} files; "
    f"{normalized_values} simplified/phrase normalizations; "
    f"{upstream_semantic_values} NeoOrigins values aligned to official zh_cn semantics"
)
if english_candidates:
    print("Potential English title-like values for manual review:")
    for key, value in english_candidates[:80]:
        print(f"  {key} = {value}")
