#!/usr/bin/env python3
"""Contextual refinement for the Bavarian (`bar`) fallback locale.

The bootstrap is corpus-driven and deliberately conservative. This pass fixes
high-visibility NeoOrigins/UI terminology where literal Standard German survived,
and curates a few gameplay strings whose context benefits from explicit wording.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"

OVERRIDES = {
    # Core Origins / picker terminology.
    "origins.layer.origin": "Uasprung",
    "origins.layer.class": "Klass",
    "screen.neoorigins.choose_origin": "Wähl dein Uasprung",
    "screen.neoorigins.choose.origins.layer.origin": "Wähl dein Uasprung",
    "screen.neoorigins.choose.origins.layer.class": "Wähl dei Klass",
    "gui.neoorigins.search.label": "Uasprüng durchsua",
    "gui.neoorigins.picker.no_results": "Koane Uasprüng gfundn",
    "gui.neoorigins.hint.select": "Wähl an Uasprung, um Details z'sehn",
    "gui.neoorigins.detail.powers_header": "Kräfd",
    "gui.neoorigins.sort.class": "Klass",
    "key.neoorigins.class_skill": "Klassnfähigkeit",
    "key.neoorigins.open_creator": "Uasprungs-Editor aufmachn",
    "key.neoorigins.open_mob_creator": "Mob-Uasprungs-Editor aufmachn",
    "screen.neoorigins.origin_info": "Uasprungsinfo",
    "gui.neoorigins.info.no_origin": "No koan Uasprung ausgwählt.",
    "gui.neoorigins.info.your_origin": "Dei Uasprung",
    "screen.neoorigins.origin_editor": "Uasprungs-Editor",
    "gui.neoorigins.editor.layers_header": "Uasprungsebenen",
    "gui.neoorigins.editor.powers_header": "Kräfd umschaltn",
    "screen.neoorigins.creator": "Uasprungs-Editor",
    "gui.neoorigins.creator.tab.powers": "Kräfd",
    "gui.neoorigins.creator.apply": "Anwendn",
    "screen.neoorigins.mob_creator": "Mob-Uasprungs-Editor",
    "gui.neoorigins.mob_creator.tab.powers": "Kräfd",
    "gui.neoorigins.mob_creator.apply": "Anwendn",

    # HUD/editor labels: HUD stays technical, surrounding UI is localized.
    "screen.neoorigins.hud_editor": "Ressourcenleistn-Editor – Zum Verschiebn ziang",
    "screen.neoorigins.hud_editor.scale": "Größn: %s%%",

    # Two English fallbacks exposed by contextual QA.
    "neoorigins.configuration.sun_damage.helmet_protection": "Helmschutz",
    "neoorigins.configuration.helmet_protection": "Helmschutz",

    # Add-on/UI terminology.
    "power.origins_fantasy.fae_flight.name": "Feenflug",
    "screen.originsmodernui.title": "Wähl dein Uasprung",
    "originsmodernui.config.hud.position": "HUD-Position",
    "originsmodernui.config.hud.scale": "HUD-Skalierung",

    # Keep these mechanics clearly distinct from economic/transport senses.
    "effect.ibarnorigins.inflation_effect": "Aufblähen",
    "power.ibarnorigins.ghasterinflate.name": "Aufblähen",
    "power.ibarnorigins.wpairswim.name": "Flug",
    "death.attack.ibarnorigins.soul_burn.player": "%1$ss Seele verbrannte beim Versuch, %2$s zu entkomma",
}

PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
ENGLISH_UI_RE = re.compile(
    r"\b(?:Helmet protection|Choose your origin|Search origins|No origins found|Your Origin|No Origin)\b",
    re.I,
)
# Keep the refinement density guard identical to the bootstrap guard so both
# stages measure the same Bavarian lexical signal and use the same quality floor.
DIALECT_MARKER_RE = re.compile(
    r"\b(?:ned|san|ko|kenna|oda|mid|vo|af|fia|üba|unta|imma|scho|no|zruck|oangebn|ois|doaf|viech|schiaß)\b",
    re.I,
)
MIN_DIALECT_MARKERS = 300


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/bar.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Bavarian files, found {len(files)}")

    found = {key: 0 for key in OVERRIDES}
    changed_values = 0
    changed_files = 0

    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        dirty = False
        for key, new_value in OVERRIDES.items():
            if key not in data:
                continue
            found[key] += 1
            old_value = str(data[key])
            if sorted(PLACEHOLDER_RE.findall(old_value)) != sorted(PLACEHOLDER_RE.findall(new_value)):
                raise SystemExit(
                    f"Placeholder mismatch in curated override {key}: {old_value!r} -> {new_value!r}"
                )
            if old_value != new_value:
                data[key] = new_value
                changed_values += 1
                dirty = True
        if dirty:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed_files += 1

    # Each key in this curated set is expected once in the physical fallback layout.
    missing = [key for key, count in found.items() if count == 0]
    duplicates = {key: count for key, count in found.items() if count > 1}
    if missing:
        raise SystemExit(f"Curated Bavarian keys not found: {missing}")
    if duplicates:
        raise SystemExit(f"Curated Bavarian keys unexpectedly duplicated: {duplicates}")

    # Post-refinement semantic sanity.
    rows = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.extend((path, key, str(value)) for key, value in data.items())

    english_hits = [(str(path), key, value) for path, key, value in rows if ENGLISH_UI_RE.search(value)]
    if english_hits:
        raise SystemExit(f"English high-visibility UI survived Bavarian refinement: {english_hits[:20]}")

    forbidden_fragments = [
        "Herkunft durchsuchen",
        "Keine Herkunft gefunden",
        "Wähle einen Ursprung",
    ]
    truncated_token_re = re.compile(r"\bzu\s+s(?:\s|$|[.,;:!?])", re.I)
    bad = [
        (str(path), key, value)
        for path, key, value in rows
        if truncated_token_re.search(value)
        or any(fragment.casefold() in value.casefold() for fragment in forbidden_fragments)
    ]
    if bad:
        raise SystemExit(f"Known Bavarian contextual/corruption patterns survived: {bad[:20]}")

    dialect_text = "\n".join(value for _, _, value in rows)
    marker_count = len(DIALECT_MARKER_RE.findall(dialect_text))
    if marker_count < MIN_DIALECT_MARKERS:
        raise SystemExit(
            f"Bavarian dialect marker sanity too low after refinement: {marker_count} "
            f"(minimum {MIN_DIALECT_MARKERS})"
        )

    print(
        f"Bavarian contextual refinement passed: {changed_values} values in {changed_files} files; "
        f"{marker_count} dialect markers; 0 English UI survivors; 0 known corruption patterns."
    )


if __name__ == "__main__":
    main()
