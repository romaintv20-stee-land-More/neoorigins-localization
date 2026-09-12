#!/usr/bin/env python3
"""Refine generated Manx (`gv_im`) fallback output with a local Manx MT model.

Whole-string translations from the pinned Minecraft en_us -> gv_im corpus remain the
highest-priority source. Other English semantic strings are translated locally with
Helsinki-NLP/opus-mt-en-gv (Marian), avoiding anonymous web-service rate limits.
Placeholders and technical/proper project tokens are kept outside MT input and restored
verbatim. This is automated translation assistance, not native-speaker review.
"""
from __future__ import annotations

from pathlib import Path
import os
import json
import re

import bootstrap_manx as base
import refine_manx as previous

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_NAME = "Helsinki-NLP/opus-mt-en-gv"

PROTECT_RE = re.compile(
    r"(%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b)"
)

FORBIDDEN_MIXED_PATTERNS = previous.FORBIDDEN_MIXED_PATTERNS


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_protected(text: str) -> list[tuple[bool, str]]:
    parts = PROTECT_RE.split(text)
    result: list[tuple[bool, str]] = []
    for part in parts:
        if not part:
            continue
        result.append((bool(PROTECT_RE.fullmatch(part)), part))
    return result


def build_sources():
    return previous.build_sources()


def translate_chunks(chunks: list[str]) -> dict[str, str]:
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    torch.set_num_threads(max(1, min(8, os.cpu_count() or 2)))
    print(f"Loading local Manx model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.eval()

    translated: dict[str, str] = {}
    batch_size = 24
    with torch.inference_mode():
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            encoded = tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=384,
            )
            generated = model.generate(
                **encoded,
                max_length=512,
                num_beams=4,
                early_stopping=True,
            )
            decoded = tokenizer.batch_decode(generated, skip_special_tokens=True)
            if len(decoded) != len(batch):
                raise SystemExit(
                    f"Local Manx model returned {len(decoded)} translations for {len(batch)} inputs"
                )
            for source, target in zip(batch, decoded):
                target = target.strip()
                if not target:
                    raise SystemExit(f"Local Manx model returned an empty translation for {source!r}")
                translated[source] = target
            done = min(start + batch_size, len(chunks))
            if done % 240 == 0 or done == len(chunks):
                print(f"Local Manx chunk progress: {done}/{len(chunks)}")
    return translated


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Manx files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    common_en, delta_121_en, delta_261_en, delta_262_en, addons_en = build_sources()
    print(
        f"NeoOrigins Manx source split: common={len(common_en)}, "
        f"1.21.1={len(delta_121_en)}, 26.1={len(delta_261_en)}, 26.2={len(delta_262_en)}"
    )

    exact, learned = base.build_corpus_maps()
    print(
        f"Manx local refinement policy: {len(exact)} exact Minecraft corpus strings take priority; "
        f"{len(learned)} isolated word mappings are disabled; remaining text uses {MODEL_NAME}."
    )

    source_payloads: list[dict[str, str]] = [common_en, delta_121_en, delta_261_en, delta_262_en]
    source_payloads.extend(addons_en.values())
    unique_sources = sorted({str(value) for payload in source_payloads for value in payload.values()})

    segmented: dict[str, list[tuple[bool, str]]] = {}
    chunks_to_translate: set[str] = set()
    direct_values: dict[str, str] = {}

    for source in unique_sources:
        if source in base.MANUAL_VALUES:
            direct_values[source] = base.MANUAL_VALUES[source]
            continue
        if source in exact:
            direct_values[source] = exact[source]
            continue
        parts = split_protected(source)
        segmented[source] = parts
        for protected, part in parts:
            if protected or not part.strip():
                continue
            chunks_to_translate.add(part)

    chunks = sorted(chunks_to_translate)
    print(
        f"Manx local translation pool: {len(unique_sources)} unique strings; "
        f"{len(direct_values)} corpus/manual whole-string hits; {len(segmented)} reconstructed strings; "
        f"{len(chunks)} unique MT chunks."
    )
    chunk_translations = translate_chunks(chunks)

    translated_by_source = dict(direct_values)
    for source, parts in segmented.items():
        rebuilt: list[str] = []
        for protected, part in parts:
            if protected or not part.strip():
                rebuilt.append(part)
            else:
                rebuilt.append(chunk_translations[part])
        target = "".join(rebuilt)
        if base.placeholder_signature(source) != base.placeholder_signature(target):
            raise SystemExit(f"Placeholder mismatch after local MT: {source!r} -> {target!r}")
        translated_by_source[source] = target

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, raw_value in source.items():
            value = str(raw_value)
            target = translated_by_source[value]
            if base.placeholder_signature(value) != base.placeholder_signature(target):
                raise SystemExit(f"Placeholder mismatch for {key}: {value!r} -> {target!r}")
            result[key] = target
        return result

    common_gv = translated_payload(common_en)
    delta_121_gv = translated_payload(delta_121_en)
    delta_261_gv = translated_payload(delta_261_en)
    delta_262_gv = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_gv_common_*/lang/gv_im.json"):
        path.unlink()
    common_items = list(common_gv.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_gv_common_{index + 1:02d}/lang/gv_im.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_gv_121/lang/gv_im.json", delta_121_gv)
    write_json(ASSETS / "neoorigins_26_1/lang/gv_im.json", delta_261_gv)
    write_json(ASSETS / "neoorigins_26_2/lang/gv_im.json", delta_262_gv)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/gv_im.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Manx files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    total_values = 0
    source_changed = 0
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

    for payload in source_payloads:
        for value in payload.values():
            source = str(value)
            if translated_by_source[source] != source:
                source_changed += 1

    text = "\n".join(str(value) for data in after.values() for value in data.values())
    for pattern in FORBIDDEN_MIXED_PATTERNS:
        match = pattern.search(text)
        if match:
            raise SystemExit(f"Known mixed-language Manx projection survived: {match.group(0)!r}")

    marker_count = len(base.MANX_MARKER_RE.findall(text))
    marked_values = sum(
        1 for data in after.values() for value in data.values()
        if base.MANX_MARKER_RE.search(str(value))
    )
    if marker_count < 250 or marked_values < 200:
        raise SystemExit(
            f"Manx differentiation unexpectedly weak after local MT: "
            f"markers={marker_count}, marked_values={marked_values}"
        )
    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived local Manx translation: only {source_changed} values changed"
        )

    expected_values = {
        "gui.neoorigins.info.edit": "Reaghey",
        "gui.neoorigins.creator.save": "Sauail",
        "screen.originsmodernui.search": "Ronsee",
        "key.categories.originsmodernui": "Origin Architect",
    }
    for key, expected in expected_values.items():
        actual = seen.get(key)
        if actual != expected:
            raise SystemExit(
                f"High-visibility Manx QA failed for {key}: {actual!r}, expected {expected!r}"
            )

    print(
        f"Manx local refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        f"{marker_count} Manx lexical markers across {marked_values} values; "
        "0 known mixed-language projection patterns."
    )


if __name__ == "__main__":
    main()
