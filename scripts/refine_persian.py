#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

EXACT_VALUE_REPLACEMENTS = {
    "درخواست کنید": "اعمال",
    "قطرات": "دراپ‌ها",
}

SUBSTRING_REPLACEMENTS = {
    "حداکثر اسب بخار": "حداکثر سلامتی",
}

OVERRIDES = {
    "neoorigins.toggle.on": "قدرت فعال است",
    "neoorigins.toggle.off": "قدرت غیرفعال است",
    "neoorigins.night_vision.no_power": "اوریجین شما قدرت دید در شب را ندارد.",
    "neoorigins.ultimine.no_power": "اوریجین شما قابلیت استخراج یک‌جای رگهٔ معدن را ندارد.",
    "origins.layer.origin": "اوریجین",
    "origins.layer.class": "کلاس",
    "screen.neoorigins.choose_origin": "اوریجین خود را انتخاب کنید",
    "screen.neoorigins.choose.origins.layer.origin": "اوریجین خود را انتخاب کنید",
    "screen.neoorigins.choose.origins.layer.class": "کلاس خود را انتخاب کنید",
    "gui.neoorigins.search.label": "جستجوی اوریجین‌ها",
    "gui.neoorigins.picker.no_results": "هیچ اوریجینی با جستجوی شما مطابقت ندارد",
    "gui.neoorigins.hint.select": "برای دیدن جزئیات یک اوریجین را انتخاب کنید",
    "gui.neoorigins.info.no_origin": "هنوز هیچ اوریجینی انتخاب نشده است.",
    "gui.neoorigins.info.your_origin": "اوریجین شما",
    "screen.neoorigins.origin_info": "اطلاعات اوریجین",
    "screen.neoorigins.origin_editor": "ویرایشگر اوریجین",
    "screen.neoorigins.creator": "سازنده اوریجین",
    "key.neoorigins.open_mob_creator": "باز کردن سازنده اوریجین موب",
    "gui.neoorigins.creator.apply": "اعمال",
    "gui.neoorigins.mob_creator.apply": "اعمال",
    "gui.neoorigins.mob_creator.tab.drops": "دراپ‌ها",
    "origins.gui.impact.low": "کم",
    "origins.gui.impact.high": "زیاد",

    "power.neoorigins.feline_mobs_ignore.description": "کریپرها از شما می‌ترسند و نزدیک شما نمی‌شوند.",
    "power.neoorigins.merling_land_slowdown.name": "کندی در خشکی",
    "power.neoorigins.merling_dries_out.description": "وقتی بیرون از آب هستید، هوای شما پیوسته کاهش می‌یابد؛ اگر بیش از حد بیرون بمانید خفه می‌شوید. باران، دیگ آب، تنفس در آب یا یک کاندوئیت فعال در نزدیکی از این وضعیت جلوگیری می‌کند.",
    "power.neoorigins.blazeling_blaze_scales.name": "فلس‌های بلیز",
    "power.neoorigins.blazeling_nether_born.name": "زادهٔ نِدِر",
    "power.neoorigins.blazeling_nether_born.description": "در نِدِر سریع‌تر هستید — وقتی در نِدِر قرار دارید سرعت حرکت شما افزایش می‌یابد.",
    "power.neoorigins.nether_fungus_diet.description": "قارچ‌های وارپد و کریمسون در نِدِر غذای مناسبی هستند — برای خوردن و دریافت ۵ گرسنگی و ۰٫۶ اشباع راست‌کلیک کنید. وقتی کاملاً سیر هستید نمی‌توانید آن‌ها را بخورید.",
    "power.neoorigins.caveborn_eat_gold.description": "می‌توانید شمش طلا، طلای خام، ناگت طلا، سنگ معدن طلا، سنگ معدن طلای دیپ‌اسلیت، سنگ معدن طلای نِدِر و بلوک طلای خام را بخورید — این‌ها غذای غنی‌تری هستند. وقتی کاملاً سیر هستید نمی‌توانید آن‌ها را بخورید.",
    "power.neoorigins.caveborn_eat_netherite.name": "طعم نِدِرایت",
    "power.neoorigins.caveborn_eat_netherite.description": "می‌توانید شمش نِدِرایت، تکهٔ نِدِرایت و Ancient Debris را بخورید — این غنی‌ترین غذای جهان است. وقتی کاملاً سیر هستید نمی‌توانید آن‌ها را بخورید.",
    "power.neoorigins.caveborn_iron_bonus.description": "خوردن آهن به مدت ۶۰ ثانیه Haste I می‌دهد.",
    "power.neoorigins.abyssal_dries_out.description": "وقتی بیرون از آب هستید، هوای شما پیوسته کاهش می‌یابد؛ اگر بیش از حد بیرون بمانید خفه می‌شوید. باران، دیگ آب، تنفس در آب یا یک کاندوئیت فعال در نزدیکی از این وضعیت جلوگیری می‌کند.",
    "origins.neoorigins.voidwalker.description": "موجودی لمس‌شده توسط End — می‌تواند از میان بلوک‌ها عبور کند، در فاصلهٔ کوتاه فوراً تلپورت شود و از دید بیشتر خطرها دور بماند. بدون خستگی می‌دود، اما آب برایش دردناک است.",
    "power.neoorigins.voidwalker_active_teleport.description": "فوراً به جایی که نگاه می‌کنید تلپورت می‌شوید (حداکثر ۲۴ بلوک). ۲ انرژی مصرف می‌کند. زمان بازیابی ۸۰ تیک است.",
    "power.neoorigins.voidwalker_water_damage.name": "سوختگی خلأ",
    "power.neoorigins.abyssal_land_speed_penalty.name": "خشکی‌نشین",

    "origin.origins_furries.raccoon.name": "راکون",
    "power.origins_furries.charge.description": "هنگام دویدن سریع، آسیب بیشتری وارد می‌کنید.",
    "power.origins_furries.charge.name": "یورش",
    "power.origins_furries.chicken_xp.description": "با کشتن مرغ‌ها دو برابر تجربه دریافت می‌کنید.",
    "power.origins_furries.fragile.description": "حداکثر سلامتی شما ۲ قلب کمتر از یک انسان است.",
    "power.origins_furries.low_light_vision.description": "وقتی بالاتر از سطح دریا هستید دید در شب دریافت می‌کنید.",
    "power.origins_furries.pavlov.description": "به صدا درآوردن زنگ روستا در ازای گرسنگی، سلامتی شما را بازیابی می‌کند.",
    "power.origins_furries.pavlov.name": "پاولوف",
    "power.origins_furries.scales.name": "فلس‌ها",
    "power.origins_furries.scales.description": "فلس‌های شما ۴+ زره طبیعی می‌دهند.",
}

changed_files = 0
changed_values = 0
for path in sorted(ASSETS.glob("**/lang/fa_ir.json")):
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

print(f"Persian refinement complete: {changed_values} values changed across {changed_files} files")
