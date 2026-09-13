#!/usr/bin/env python3
"""Refine Ido (`io_en`) fallback files with full English -> Ido translation.

Policy: safe manual full values, exact whole-string matches from the pinned Minecraft
Ido corpus, then direct full-string translation with Helsinki-NLP/opus-mt-en-mul
(target token `>>ido<<`). No isolated-word projection is used. Placeholders and
technical/project tokens are validated and, when necessary, protected through
structural fallback. This is automated translation assistance, not native review.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_ido as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "Helsinki-NLP/opus-mt-en-mul"
TARGET_PREFIX = ">>ido<< "
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return PROTECT_RE.findall(text)


def build_sources():
    neo_121_en = read_json(ROOT / "build/io-discovery-mc-1.21.1/io_en_missing_en.json")
    neo_261_en = read_json(ROOT / "build/io-discovery-mc-26.1/io_en_missing_en.json")
    neo_262_en = read_json(ROOT / "build/io-discovery-mc-26.2/io_en_missing_en.json")

    common_en = {
        key: value for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}

    source_files = {
        "medievalorigins": ROOT / "build/medievalorigins-upstream-audit/upstream_en_us.json",
        "ibarnorigins": ROOT / "build/ibarnorigins-upstream-audit/upstream_en_us.json",
        "origins_fantasy": ROOT / "build/origins-fantasy-upstream-audit/upstream_en_us.json",
        "origins_backgrounds": ROOT / "build/origins-backgrounds-upstream-audit/upstream_en_us.json",
        "origins_backgrounds_two": ROOT / "build/origins-more-backgrounds-upstream-audit/upstream_en_us.json",
        "origins_backgrounds_iss": ROOT / "build/origins-backgrounds-iss-upstream-audit/upstream_en_us.json",
        "origins_furries": ROOT / "build/origins-furries-upstream-audit/upstream_en_us.json",
        "origins_classes_ex": ROOT / "build/origins-classes-extended-upstream-audit/upstream_en_us.json",
        "origins_classes_iss": ROOT / "build/origins-classes-iss-upstream-audit/upstream_en_us.json",
        "originsmodernui": ROOT / "build/origin-architect-upstream-audit/upstream_en_us.json",
    }
    addons_en = {namespace: read_json(path) for namespace, path in source_files.items()}
    shared_background_keys = set(addons_en["origins_backgrounds"])
    addons_en["origins_backgrounds_two"] = {
        key: value for key, value in addons_en["origins_backgrounds_two"].items()
        if key not in shared_background_keys
    }
    addons_en["origins_backgrounds_iss"] = {
        key: value for key, value in addons_en["origins_backgrounds_iss"].items()
        if key not in shared_background_keys
    }
    return common_en, delta_121_en, delta_261_en, delta_262_en, addons_en


class IdoTranslator:
    def __init__(self) -> None:
        print(f"Loading Ido-capable OPUS model: {MODEL_ID}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()

    def translate_batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        encoded = self.tokenizer(
            [TARGET_PREFIX + text for text in texts],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        with torch.inference_mode():
            generated = self.model.generate(
                **encoded,
                num_beams=4,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [
            value.strip() for value in self.tokenizer.batch_decode(generated, skip_special_tokens=True)
        ]

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        translated_pieces: list[str] = []
        translatable_indices: list[int] = []
        translatable: list[str] = []
        for index, piece in enumerate(pieces):
            translated_pieces.append(piece)
            if piece.strip() and re.search(r"[A-Za-z]", piece):
                translatable_indices.append(index)
                translatable.append(piece)
        for index, translated in zip(translatable_indices, self.translate_batch(translatable)):
            translated_pieces[index] = translated

        output: list[str] = []
        for index, piece in enumerate(translated_pieces):
            output.append(piece)
            if index < len(tokens):
                output.append(tokens[index])
        return "".join(output)


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/io_en.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Ido files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    common_en, delta_121_en, delta_261_en, delta_262_en, addons_en = build_sources()
    source_payloads: list[dict[str, str]] = [common_en, delta_121_en, delta_261_en, delta_262_en]
    source_payloads.extend(addons_en.values())
    unique_sources = sorted({str(value) for payload in source_payloads for value in payload.values()})

    exact = base.build_corpus_map()
    translated_by_source: dict[str, str] = {}
    direct_sources: list[str] = []
    for source in unique_sources:
        if source in base.MANUAL_VALUES:
            translated_by_source[source] = base.MANUAL_VALUES[source]
        elif source in exact:
            translated_by_source[source] = exact[source]
        else:
            direct_sources.append(source)

    print(
        f"Ido refinement pool: {len(unique_sources)} unique strings; "
        f"{len(unique_sources) - len(direct_sources)} manual/corpus hits; "
        f"{len(direct_sources)} direct OPUS translations.",
        flush=True,
    )

    translator = IdoTranslator()
    batch_size = 16
    for start in range(0, len(direct_sources), batch_size):
        batch = direct_sources[start:start + batch_size]
        outputs = translator.translate_batch(batch)
        if len(outputs) != len(batch):
            raise SystemExit("OPUS translation batch returned an unexpected number of strings")
        for source, translated in zip(batch, outputs):
            valid = bool(translated.strip())
            valid = valid and base.placeholder_signature(source) == base.placeholder_signature(translated)
            valid = valid and protected_signature(source) == protected_signature(translated)
            if not valid:
                translated = translator.structural_translate(source)
            if not translated.strip():
                raise SystemExit(f"Empty Ido translation for {source!r}")
            if base.placeholder_signature(source) != base.placeholder_signature(translated):
                raise SystemExit(f"Ido placeholder mismatch: {source!r} -> {translated!r}")
            if protected_signature(source) != protected_signature(translated):
                raise SystemExit(f"Ido protected-token mismatch: {source!r} -> {translated!r}")
            translated_by_source[source] = translated
        done = min(start + len(batch), len(direct_sources))
        if done % 160 == 0 or done == len(direct_sources):
            print(f"Direct Ido translation progress: {done}/{len(direct_sources)}", flush=True)

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, raw_value in source.items():
            source_value = str(raw_value)
            translated = translated_by_source[source_value]
            if base.placeholder_signature(source_value) != base.placeholder_signature(translated):
                raise SystemExit(f"Placeholder mismatch for {key}: {source_value!r} -> {translated!r}")
            result[key] = translated
        return result

    common_io = translated_payload(common_en)
    delta_121_io = translated_payload(delta_121_en)
    delta_261_io = translated_payload(delta_261_en)
    delta_262_io = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_io_common_*/lang/io_en.json"):
        path.unlink()
    common_items = list(common_io.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_io_common_{index + 1:02d}/lang/io_en.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_io_121/lang/io_en.json", delta_121_io)
    write_json(ASSETS / "neoorigins_26_1/lang/io_en.json", delta_261_io)
    write_json(ASSETS / "neoorigins_26_2/lang/io_en.json", delta_262_io)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/io_en.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/io_en.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Ido files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    source_changed = 0
    total_values = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Ido refinement: {path}")
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
    if ">>ido<<" in text:
        raise SystemExit("OPUS Ido target token survived generated output")
    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived full Ido translation: only {source_changed} values changed"
        )
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Technical project name Origin Architect was not preserved")

    print(
        f"Ido full refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        "no isolated-word projection pipeline.",
        flush=True,
    )


if __name__ == "__main__":
    main()
