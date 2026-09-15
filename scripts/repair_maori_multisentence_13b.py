#!/usr/bin/env python3
"""Repair multi-sentence Māori MT values using sentence-complete NLLB 1.3B.

The first full 1.3B pass is strong on individual sentences but can drop later
sentences in multi-sentence descriptions. This repair keeps all existing good
single-sentence/corpus/manual values and regenerates only direct-MT source values
that contain two or more complete sentences, one full sentence at a time.
"""
from __future__ import annotations

from collections import defaultdict
import json
import re
from pathlib import Path

import refine_maori_13b as core

ASSETS = core.ASSETS
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")


def sentence_count(text: str) -> int:
    return len(re.findall(r"[.!?](?=\s|$)", text))


def safe_translate(mt: core.Translator, source: str) -> str:
    value = mt.batch([source])[0]
    valid = bool(value.strip())
    valid = valid and core.BASE.placeholder_signature(source) == core.BASE.placeholder_signature(value)
    valid = valid and core.protected_signature(source) == core.protected_signature(value)
    if not valid:
        value = mt.structural(source)
    core.validate_pair(source, value)
    return value


def translate_sentences(mt: core.Translator, source: str) -> str:
    result: list[str] = []
    cursor = 0
    boundaries = list(SENTENCE_BOUNDARY_RE.finditer(source))
    if not boundaries:
        return safe_translate(mt, source)
    for match in boundaries:
        piece = source[cursor:match.start()]
        result.append(safe_translate(mt, piece) if piece.strip() else piece)
        result.append(match.group(0))
        cursor = match.end()
    tail = source[cursor:]
    result.append(safe_translate(mt, tail) if tail.strip() else tail)
    value = "".join(result)
    core.validate_pair(source, value)
    return value


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/mi_nz.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Māori files, found {len(files)}")
    data_by_path = {path: core.read_json(path) for path in files}
    key_locations: dict[str, list[Path]] = defaultdict(list)
    current_by_key: dict[str, str] = {}
    for path, data in data_by_path.items():
        for key, value in data.items():
            key_locations[key].append(path)
            current_by_key[key] = str(value)

    common, d121, d261, d262, addons, payloads, exact, translated, direct = core.build_pool()
    source_maps = [common, d121, d261, d262, *addons.values()]
    direct_set = set(direct)
    candidates = sorted({
        str(raw)
        for source_map in source_maps
        for raw in source_map.values()
        if str(raw) in direct_set and sentence_count(str(raw)) >= 2
    })
    print(f"Māori sentence-complete repair candidates: {len(candidates)}", flush=True)

    mt = core.Translator()
    repairs: dict[str, str] = {}
    for index, source in enumerate(candidates, 1):
        value = translate_sentences(mt, source)
        repairs[source] = value
        if index % 20 == 0 or index == len(candidates):
            print(f"Māori sentence repair progress: {index}/{len(candidates)}", flush=True)

    touched_keys = 0
    touched_files: set[Path] = set()
    source_to_keys: dict[str, set[str]] = defaultdict(set)
    for source_map in source_maps:
        for key, raw in source_map.items():
            source_to_keys[str(raw)].add(key)

    for source, value in repairs.items():
        for key in source_to_keys[source]:
            locations = key_locations.get(key, [])
            if not locations:
                raise SystemExit(f"Māori repair key not found in fallback files: {key}")
            for path in locations:
                if key not in data_by_path[path]:
                    continue
                data_by_path[path][key] = value
                touched_files.add(path)
                touched_keys += 1

    for path in touched_files:
        core.write_json(path, data_by_path[path])

    # Verify every repaired source maps to exactly the sentence-complete value and
    # no placeholder/protected-token corruption was introduced.
    after = {path: core.read_json(path) for path in files}
    seen_repaired: set[str] = set()
    for source, value in repairs.items():
        core.validate_pair(source, value)
        for key in source_to_keys[source]:
            for path in key_locations.get(key, []):
                if after[path].get(key) == value:
                    seen_repaired.add(source)
                    break
    if seen_repaired != set(repairs):
        missing = sorted(set(repairs) - seen_repaired)
        raise SystemExit(f"Māori repaired values missing after write: {missing[:3]!r}")

    print(
        f"Māori sentence-complete repair passed: {len(repairs)} source strings; "
        f"{touched_keys} key occurrences across {len(touched_files)} files",
        flush=True,
    )


if __name__ == "__main__":
    main()
