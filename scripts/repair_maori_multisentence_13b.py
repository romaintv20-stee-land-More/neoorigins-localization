#!/usr/bin/env python3
"""Repair multi-sentence Māori MT values using sentence-complete NLLB 1.3B.

The first full 1.3B pass is strong on individual sentences but can drop later
sentences in multi-sentence descriptions. This repair preserves all existing
single-sentence/corpus/manual values and regenerates only direct-MT source values
with two or more complete sentences, one full sentence at a time.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import re
from pathlib import Path

import refine_maori_13b as core

ASSETS = core.ASSETS
SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")
COMMON_LABEL = "__common__"


def sentence_count(text: str) -> int:
    return len(re.findall(r"[.!?](?=\s|$)", text))


def build_candidates():
    common, d121, d261, d262, addons, payloads, exact, translated, direct = core.build_pool()
    named_maps = [
        (COMMON_LABEL, common),
        ("neoorigins_mi_121", d121),
        ("neoorigins_26_1", d261),
        ("neoorigins_26_2", d262),
        *addons.items(),
    ]
    direct_set = set(direct)
    candidates = sorted({
        str(raw)
        for _, source_map in named_maps
        for raw in source_map.values()
        if str(raw) in direct_set and sentence_count(str(raw)) >= 2
    })
    return named_maps, candidates


def safe_batch(mt: core.Translator, sources: list[str]) -> list[str]:
    values = mt.batch(sources)
    if len(values) != len(sources):
        raise SystemExit("Māori sentence repair batch-size mismatch")
    result: list[str] = []
    for source, value in zip(sources, values):
        valid = bool(value.strip())
        valid = valid and core.BASE.placeholder_signature(source) == core.BASE.placeholder_signature(value)
        valid = valid and core.protected_signature(source) == core.protected_signature(value)
        if not valid:
            value = mt.structural(source)
        core.validate_pair(source, value)
        result.append(value)
    return result


def sentence_pieces(source: str) -> list[tuple[str, bool]]:
    result: list[tuple[str, bool]] = []
    cursor = 0
    for match in SENTENCE_BOUNDARY_RE.finditer(source):
        body = source[cursor:match.start()]
        if body:
            result.append((body, True))
        result.append((match.group(0), False))
        cursor = match.end()
    tail = source[cursor:]
    if tail:
        result.append((tail, True))
    return result


def translate_sentences(mt: core.Translator, source: str) -> str:
    pieces = sentence_pieces(source)
    bodies = [piece for piece, translatable in pieces if translatable and piece.strip()]
    translated_bodies = iter(safe_batch(mt, bodies))
    output: list[str] = []
    for piece, translatable in pieces:
        if translatable and piece.strip():
            output.append(next(translated_bodies))
        else:
            output.append(piece)
    value = "".join(output)
    core.validate_pair(source, value)
    return value


def write_shard(index: int, count: int, output: Path) -> None:
    if count < 1 or not 0 <= index < count:
        raise SystemExit(f"Invalid Māori repair shard {index}/{count}")
    _, candidates = build_candidates()
    selected = candidates[index::count]
    print(
        f"Māori sentence-repair shard {index + 1}/{count}: "
        f"{len(selected)} of {len(candidates)} multi-sentence sources",
        flush=True,
    )
    mt = core.Translator()
    repairs: dict[str, str] = {}
    for pos, source in enumerate(selected, 1):
        repairs[source] = translate_sentences(mt, source)
        if pos % 10 == 0 or pos == len(selected):
            print(f"Māori repair shard progress: {pos}/{len(selected)}", flush=True)
    core.write_json(output, {source: repairs[source] for source in sorted(repairs)})
    print(f"Māori repair shard {index + 1}/{count} passed", flush=True)


def collect_shards(directory: Path, candidates: list[str]) -> dict[str, str]:
    files = sorted(directory.glob("*.json"))
    if not files:
        raise SystemExit("No Māori sentence-repair shard artifacts found")
    combined: dict[str, str] = {}
    for path in files:
        for source, value in core.read_json(path).items():
            if source in combined and combined[source] != value:
                raise SystemExit(f"Conflicting Māori repaired value for {source!r}")
            combined[source] = value
    if set(combined) != set(candidates):
        missing = sorted(set(candidates) - set(combined))
        extra = sorted(set(combined) - set(candidates))
        raise SystemExit(
            f"Māori repair coverage mismatch: missing={len(missing)} extra={len(extra)} "
            f"sample={missing[:3]!r}"
        )
    for source, value in combined.items():
        core.validate_pair(source, value)
    print(f"Merged {len(files)} Māori repair shards covering {len(combined)} sources", flush=True)
    return combined


def build_exact_occurrences(named_maps, data_by_path):
    common_paths = [
        path for path in data_by_path
        if path.parent.parent.name.startswith("neoorigins_mi_common_")
    ]
    occurrences: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    for namespace, source_map in named_maps:
        if namespace == COMMON_LABEL:
            for key, raw in source_map.items():
                locations = [path for path in common_paths if key in data_by_path[path]]
                if len(locations) != 1:
                    raise SystemExit(
                        f"Expected one Māori common location for {key}, found {len(locations)}"
                    )
                occurrences[str(raw)].append((locations[0], key))
            continue

        path = ASSETS / namespace / "lang/mi_nz.json"
        if path not in data_by_path:
            raise SystemExit(f"Missing Māori namespace file for repair: {path}")
        for key, raw in source_map.items():
            if key not in data_by_path[path]:
                raise SystemExit(f"Māori key {key} missing from expected namespace {namespace}")
            occurrences[str(raw)].append((path, key))
    return occurrences


def apply_repairs(repairs: dict[str, str]) -> None:
    files = sorted(ASSETS.glob("**/lang/mi_nz.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Māori files, found {len(files)}")
    data_by_path = {path: core.read_json(path) for path in files}

    named_maps, candidates = build_candidates()
    if set(repairs) != set(candidates):
        raise SystemExit("Māori repair map does not exactly cover multi-sentence direct pool")
    occurrences = build_exact_occurrences(named_maps, data_by_path)

    touched_keys = 0
    touched_files: set[Path] = set()
    for source, value in repairs.items():
        core.validate_pair(source, value)
        exact_occurrences = occurrences.get(source, [])
        if not exact_occurrences:
            raise SystemExit(f"No exact Māori occurrence found for repaired source: {source!r}")
        for path, key in exact_occurrences:
            data_by_path[path][key] = value
            touched_files.add(path)
            touched_keys += 1

    for path in touched_files:
        core.write_json(path, data_by_path[path])

    after = {path: core.read_json(path) for path in files}
    for source, value in repairs.items():
        for path, key in occurrences[source]:
            if after[path].get(key) != value:
                raise SystemExit(
                    f"Māori repaired value missing at exact occurrence {path}:{key}"
                )

    print(
        f"Māori sentence-complete repair passed: {len(repairs)} source strings; "
        f"{touched_keys} exact key occurrences across {len(touched_files)} files",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--shard-output", type=Path)
    parser.add_argument("--merge-shards", type=Path)
    args = parser.parse_args()

    shard_args = (args.shard_index, args.shard_count, args.shard_output)
    if any(value is not None for value in shard_args):
        if not all(value is not None for value in shard_args) or args.merge_shards is not None:
            raise SystemExit("Invalid Māori repair shard arguments")
        write_shard(args.shard_index, args.shard_count, args.shard_output)
        return

    if args.merge_shards is not None:
        _, candidates = build_candidates()
        apply_repairs(collect_shards(args.merge_shards, candidates))
        return

    raise SystemExit("Use Māori repair shard mode or --merge-shards")


if __name__ == "__main__":
    main()
