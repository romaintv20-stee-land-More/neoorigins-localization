#!/usr/bin/env python3
"""Conservatively refine the generated Gallo (`go_fr`) fallback locale.

The bootstrap is corpus-driven and intentionally leaves French semantic text in place
when the pinned Minecraft fr_fr -> go_fr corpus does not provide strong evidence.
This pass only fixes high-visibility output that is clearly unsafe, then validates the
generated-file count, placeholders, dialect presence, and visible UI labels. This is
deterministic assistance, not native-speaker review.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import bootstrap_gallo as base

ASSETS = base.ASSETS

# `Phantom` is a NeoOrigins origin/proper name and must not be projected through an
# unrelated corpus word mapping. The bootstrap produced `Sebllan`. Only exact
# `Sebllan` values on keys explicitly referring to `phantom` are rewritten.
PHANTOM_BAD_VALUE = "Sebllan"
PHANTOM_SAFE_VALUE = "Phantom"

FORBIDDEN_PATTERNS = (
    re.compile(r"^Sebllan$", re.I),
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/go_fr.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Gallo files, found {len(files)}")

    changed = 0
    total = 0
    seen: dict[str, str] = {}
    for path in files:
        data = read_json(path)
        dirty = False
        for key, raw_value in list(data.items()):
            value = str(raw_value)
            if "phantom" in key.casefold() and value.casefold() == PHANTOM_BAD_VALUE.casefold():
                if base.placeholder_signature(value) != base.placeholder_signature(PHANTOM_SAFE_VALUE):
                    raise SystemExit(f"Placeholder mismatch for Phantom correction {key}: {value!r}")
                data[key] = PHANTOM_SAFE_VALUE
                changed += 1
                dirty = True
        if dirty:
            write_json(path, data)
        for key, value in data.items():
            value = str(value)
            total += 1
            seen[key] = value
            for pattern in FORBIDDEN_PATTERNS:
                if pattern.search(value):
                    raise SystemExit(f"Known unsafe Gallo projection survived for {key}: {value!r}")

    text = "\n".join(str(value) for path in files for value in read_json(path).values())
    marker_count = len(base.GALLO_MARKER_RE.findall(text))
    if marker_count < 250:
        raise SystemExit(f"Gallo dialect marker sanity too low after refinement: {marker_count}")

    expected_values = {
        "origins.neoorigins.phantom.name": "Phantom",
        "neoorigins.configuration.origins.phantom": "Phantom",
        "gui.neoorigins.button.back": "< Retour",
        "gui.neoorigins.info.close": "Fermer",
        "gui.neoorigins.creator.save": "Saover",
        "gui.neoorigins.info.edit": "Amender",
        "screen.originsmodernui.select": "Chouézi",
        "screen.originsmodernui.search_hint": "Gheter des origines...",
    }
    for key, expected in expected_values.items():
        actual = seen.get(key)
        if actual != expected:
            raise SystemExit(f"High-visibility Gallo QA failed for {key}: {actual!r}, expected {expected!r}")

    print(
        f"Gallo conservative refinement passed: checked {total} values across {len(files)} files; "
        f"changed {changed} unsafe Phantom values; {marker_count} dialect markers; "
        "0 known unsafe visible projections."
    )


if __name__ == "__main__":
    main()
