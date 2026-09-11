#!/usr/bin/env python3
"""Refine generated Manx (`gv_im`) fallback output conservatively.

The first bootstrap allowed a tiny set of repeatedly attested single-word corpus
mappings to be projected inside larger English sentences. Contextual QA showed that
this creates grammatically unsafe English/Manx hybrids. This pass therefore rebuilds
all generated Manx fallback files using only whole-string corpus matches and explicit
high-confidence UI values. It is deterministic corpus assistance, not native review.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import bootstrap_manx as base

ASSETS = base.ASSETS

# Concrete mixed-language artifacts observed during contextual QA of the bootstrap.
FORBIDDEN_MIXED_PATTERNS = (
    re.compile(r"\bAquatic Bieauid\b", re.I),
    re.compile(r"\bSky Bieauid\b", re.I),
    re.compile(r"\bflight bieauid\b", re.I),
    re.compile(r"\bthe seihll\b", re.I),
    re.compile(r"\benergy tappee\b", re.I),
    re.compile(r"\bwater coirrey\b", re.I),
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def snapshot() -> dict[Path, dict]:
    files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Manx files before refinement, found {len(files)}")
    return {path: read_json(path) for path in files}


def main() -> None:
    before = snapshot()

    original_builder = base.build_corpus_maps

    def exact_only_builder():
        exact, learned = original_builder()
        print(
            f"Manx refinement policy: retaining {len(exact)} whole-string corpus mappings; "
            f"disabling {len(learned)} reusable single-word projections inside larger strings"
        )
        return exact, {}

    base.build_corpus_maps = exact_only_builder
    base.main()

    after = snapshot()
    changed_values = 0
    total_values = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Manx refinement: {path}")
        for key, value in new_data.items():
            total_values += 1
            seen[key] = str(value)
            if old_data[key] != value:
                changed_values += 1

    text = "\n".join(str(value) for data in after.values() for value in data.values())
    for pattern in FORBIDDEN_MIXED_PATTERNS:
        match = pattern.search(text)
        if match:
            raise SystemExit(f"Known mixed-language Manx projection survived: {match.group(0)!r}")

    marker_count = len(base.MANX_MARKER_RE.findall(text))
    if marker_count < 25:
        raise SystemExit(f"Manx marker sanity too low after exact-only refinement: {marker_count}")

    expected_values = {
        "gui.neoorigins.info.edit": "Reaghey",
        "gui.neoorigins.creator.save": "Sauail",
        "screen.originsmodernui.search": "Ronsee",
        "screen.originsmodernui.search_hint": "Ronsee origins...",
        "key.categories.originsmodernui": "Origin Architect",
    }
    for key, expected in expected_values.items():
        actual = seen.get(key)
        if actual != expected:
            raise SystemExit(
                f"High-visibility Manx QA failed for {key}: {actual!r}, expected {expected!r}"
            )

    print(
        f"Manx exact-only refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; retained {marker_count} Manx lexical markers; "
        "0 known mixed-language projection patterns."
    )


if __name__ == "__main__":
    main()
