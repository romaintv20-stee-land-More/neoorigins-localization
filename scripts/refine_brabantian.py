#!/usr/bin/env python3
"""Contextual refinement for the Brabantian (`brb`) fallback locale.

The bootstrap is corpus-driven and deliberately conservative. This pass fixes a
small set of high-visibility strings that need context rather than word-level
projection and guards against known corpus/alignment corruption patterns.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")

OVERRIDES = {
    # Core origin name: the Dutch semantic source retained the English label.
    "origins.neoorigins.human.name": "Mens",

    # Minecraft's Brabantian corpus uses the infinitive-style "beweireke" in
    # edit contexts; the automatic token projection had truncated this label.
    "gui.neoorigins.info.edit": "Beweireke",
}

DIALECT_MARKER_RE = re.compile(
    r"\b(?:nie|gij|oe|oew|gullie|da|wa|mar|veur|gin|meej|hedde|bende|kunde|unne|ut)\b",
    re.I,
)
MIN_DIALECT_MARKERS = 150

FORBIDDEN_FRAGMENTS = (
    "Beweirek",
    "zaadige ien ut doenker",
    "zaadige ien ut donker",
)


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/brb.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Brabantian files, found {len(files)}")

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
                    f"Placeholder mismatch in Brabantian override {key}: {old_value!r} -> {new_value!r}"
                )
            if old_value != new_value:
                data[key] = new_value
                changed_values += 1
                dirty = True
        if dirty:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed_files += 1

    missing = [key for key, count in found.items() if count == 0]
    duplicates = {key: count for key, count in found.items() if count > 1}
    if missing:
        raise SystemExit(f"Curated Brabantian keys not found: {missing}")
    if duplicates:
        raise SystemExit(f"Curated Brabantian keys unexpectedly duplicated: {duplicates}")

    rows = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.extend((path, key, str(value)) for key, value in data.items())

    bad = [
        (str(path), key, value)
        for path, key, value in rows
        if any(fragment.casefold() in value.casefold() for fragment in FORBIDDEN_FRAGMENTS)
    ]
    if bad:
        raise SystemExit(f"Known Brabantian corruption patterns survived: {bad[:20]}")

    human_hits = [
        (str(path), key, value)
        for path, key, value in rows
        if key == "origins.neoorigins.human.name" and value != "Mens"
    ]
    if human_hits:
        raise SystemExit(f"Brabantian Human origin label was not localized: {human_hits}")

    dialect_text = "\n".join(value for _, _, value in rows)
    marker_count = len(DIALECT_MARKER_RE.findall(dialect_text))
    if marker_count < MIN_DIALECT_MARKERS:
        raise SystemExit(
            f"Brabantian dialect marker sanity too low after refinement: {marker_count} "
            f"(minimum {MIN_DIALECT_MARKERS})"
        )

    print(
        f"Brabantian contextual refinement passed: {changed_values} values in {changed_files} files; "
        f"{marker_count} dialect markers; 0 known corruption patterns."
    )


if __name__ == "__main__":
    main()
