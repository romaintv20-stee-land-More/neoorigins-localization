#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

# Conservative context-specific corrections for obvious MT false friends and
# Minecraft/Origins terminology. Overrides are keyed so legitimate meanings of
# the same Malay word elsewhere are left untouched.
OVERRIDES = {
    "neoorigins.toggle.on": "Kuasa didayakan",
    "neoorigins.toggle.off": "Kuasa dinyahdayakan",
    "neoorigins.night_vision.on": "Penglihatan Malam didayakan",
    "neoorigins.night_vision.off": "Penglihatan Malam dinyahdayakan",
    "neoorigins.night_vision.no_power": "Asal anda tidak mempunyai kuasa Penglihatan Malam.",
    "neoorigins.ultimine.no_power": "Asal anda tidak mempunyai kuasa Ultimine.",
    "origins.layer.origin": "Asal",
    "button.neoorigins.random": "Rawak",
    "gui.neoorigins.button.back": "< Kembali",
    "gui.neoorigins.picker.back_to_grid": "< Kembali ke Grid",
    "gui.neoorigins.hint.scroll": "Tatal untuk melihat lagi",
    "gui.neoorigins.info.close": "Tutup",
    "key.neoorigins.open_creator": "Buka Pencipta Asal",
    "key.neoorigins.open_mob_creator": "Buka Pencipta Asal Mob",
    "screen.neoorigins.creator": "Pencipta Asal",
    "gui.neoorigins.creator.save": "Simpan",
    "gui.neoorigins.creator.apply": "Gunakan",
    "screen.neoorigins.mob_creator": "Pencipta Asal Mob",
    "gui.neoorigins.mob_creator.tab.spawn_rules": "Peraturan Kemunculan",
    "gui.neoorigins.mob_creator.tab.drops": "Jatuhan",
    "gui.neoorigins.mob_creator.save": "Simpan",
    "gui.neoorigins.mob_creator.apply": "Gunakan",
    "origins.neoorigins.blazeling.name": "Blazeling",
    "power.neoorigins.merling_land_slowdown.name": "Kaki Darat Lemah",
    "power.neoorigins.blazeling_blaze_scales.name": "Sisik Blaze",
    "power.neoorigins.blazeling_nether_born.name": "Dilahirkan di Nether",
    "power.neoorigins.blazeling_nether_born.description": "Bergerak lebih pantas ketika berada di Nether.",
    "power.neoorigins.enderian_projectile_dodge.name": "Langkah Void",
    "power.neoorigins.strider_stampede.name": "Rempuhan",
    "power.neoorigins.shulk_shell_retreat.name": "Berlindung dalam Cangkerang",
    "power.neoorigins.shulk_levitation_immunity.name": "Berpijak Kukuh",

    "origin.origins_furries.sheep.name": "Biri-biri",
    "origin.origins_furries.dog.name": "Anjing",
    "origin.origins_furries.otter.name": "Memerang",
    "origin.origins_furries.raccoon.description": "Rakun juga dikenali sebagai 'panda sampah'.",
    "origin.origins_furries.cow.name": "Lembu",
    "origin.origins_furries.tiger.name": "Harimau",
    "origin.origins_furries.squirrel.name": "Tupai",
    "power.origins_furries.charge.name": "Serbuan",
    "power.origins_furries.chicken_xp.description": "Anda mendapat dua kali ganda XP daripada membunuh ayam.",
    "power.origins_furries.chicken_xp.name": "XP Ayam",
    "power.origins_furries.flee.name": "Melarikan Diri",
    "power.origins_furries.fragile.description": "Kesihatan maksimum anda dua jantung lebih rendah daripada manusia.",
    "power.origins_furries.hates_skels.name": "Benci Rangka",
    "power.origins_furries.kb_resist.description": "Anda mendapat 10% rintangan tolak balik.",
    "power.origins_furries.kb_resist.name": "Rintangan Tolak Balik",
    "power.origins_furries.pavlov.name": "Tindak Balas Pavlov",
    "power.origins_furries.raccoon_jump.name": "Lompatan Rakun",
    "power.origins_furries.scales.description": "Sisik anda memberi anda +4 Perisai Semula Jadi.",
    "power.origins_furries.scales.name": "Sisik",
    "power.origins_furries.soft.description": "Kesihatan maksimum anda satu jantung lebih rendah daripada manusia.",
    "power.origins_furries.starting_wool.name": "Bulu Permulaan",
    "power.origins_furries.munch_grass.name": "Makan Rumput",

    "screen.originsmodernui.title": "Pilih Asal Anda",
    "screen.originsmodernui.random": "Rawak",
    "originsmodernui.config.hud.position": "Kedudukan HUD",
    "originsmodernui.config.hud.style": "Gaya HUD",
    "originsmodernui.config.hud.scale": "Skala HUD",
    "originsmodernui.config.hud.opacity": "Kelegapan HUD",
    "originsmodernui.config.hud.show_xp_popup": "Tunjukkan pop timbul perolehan XP",
}

# Standardize the numbered hotkey labels, which MT inconsistently rendered as
# both "kekunci panas" and "kekunci pintas".
for i in range(1, 65):
    OVERRIDES[f"key.neoorigins.hotkey.{i}"] = f"Kekunci Pintas {i:02d}"

changed_files = 0
changed_values = 0
for path in sorted(ASSETS.glob("**/lang/ms_my.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False
    for key, new_value in OVERRIDES.items():
        if key in data and data[key] != new_value:
            data[key] = new_value
            changed = True
            changed_values += 1

    # Fix a recurring batch-translation formatting defect where sentence-ending
    # punctuation was glued directly to the next capitalized sentence.
    for key, value in list(data.items()):
        if not isinstance(value, str):
            continue
        fixed = re.sub(r'([.!?])([A-Z])', r'\1 \2', value)
        if fixed != value:
            data[key] = fixed
            changed = True
            changed_values += 1

    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed_files += 1

print(f"Malay refinement complete: {changed_values} values changed across {changed_files} files")
