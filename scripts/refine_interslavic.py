#!/usr/bin/env python3
"""Refine Interslavic (`isv`) fallback files with full English -> Interslavic translation.

Policy: safe manual full values, exact whole-string matches from the pinned Minecraft
Interslavic corpus, then direct full-string translation with the Interslavic-finetuned
NLLB model `salavat/nllb-200-distilled-600M-finetuned-isv_v2`, using `eng_Latn` ->
`isv_Latn`. No isolated-word projection is used. Placeholders and technical/project
tokens are validated and, when necessary, protected through structural fallback.
This is automated translation assistance, not native review.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_interslavic as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "salavat/nllb-200-distilled-600M-finetuned-isv_v2"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "isv_Latn"
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
    neo_121_en = read_json(ROOT / "build/isv-discovery-mc-1.21.1/isv_missing_en.json")
    neo_261_en = read_json(ROOT / "build/isv-discovery-mc-26.1/isv_missing_en.json")
    neo_262_en = read_json(ROOT / "build/isv-discovery-mc-26.2/isv_missing_en.json")

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


class InterslavicTranslator:
    def __init__(self) -> None:
        print(f"Loading Interslavic NLLB model: {MODEL_ID}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.lang2id = self.tokenizer.added_tokens_encoder
        for code in (SOURCE_LANG, TARGET_LANG):
            if code not in self.lang2id:
                raise RuntimeError(f"Required NLLB language token {code!r} missing from tokenizer")

    def translate_batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        encoded = self.tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        )
        encoded["input_ids"][:, 0] = self.lang2id[SOURCE_LANG]
        with torch.inference_mode():
            generated = self.model.generate(
                **encoded,
                forced_bos_token_id=self.lang2id[TARGET_LANG],
                num_beams=4,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [
            value.strip() for value in self.tokenizer.batch_decode(generated, skip_special_tokens=True)
        ]

    @staticmethod
    def split_structural_affixes(piece: str) -> tuple[str, str, str]:
        """Keep punctuation/numeric affixes outside translated natural-language spans.

        This prevents protected tokens such as ``HP`` from being glued to a translated
        neighbouring word when a source segment starts with ``) `` or another delimiter.
        Internal punctuation/numbers remain in the natural-language core so constructs
        such as ``heart (+2 max`` still translate coherently.
        """
        alpha = [index for index, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        first = alpha[0]
        last = alpha[-1]
        return piece[:first], piece[first:last + 1], piece[last + 1:]

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        translated_pieces = list(pieces)
        translatable_indices: list[int] = []
        translatable: list[str] = []
        affixes: dict[int, tuple[str, str]] = {}

        for index, piece in enumerate(pieces):
            prefix, core, suffix = self.split_structural_affixes(piece)
            if not core:
                continue
            translatable_indices.append(index)
            translatable.append(core)
            affixes[index] = (prefix, suffix)

        outputs = self.translate_batch(translatable)
        if len(outputs) != len(translatable_indices):
            raise RuntimeError("Structural Interslavic translation returned the wrong number of spans")
        for index, translated in zip(translatable_indices, outputs):
            prefix, suffix = affixes[index]
            translated_pieces[index] = prefix + translated.strip() + suffix

        output: list[str] = []
        for index, piece in enumerate(translated_pieces):
            output.append(piece)
            if index < len(tokens):
                output.append(tokens[index])
        return "".join(output)


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/isv.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Interslavic files before refinement, found {len(before_files)}")
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
        f"Interslavic refinement pool: {len(unique_sources)} unique strings; "
        f"{len(unique_sources) - len(direct_sources)} manual/corpus hits; "
        f"{len(direct_sources)} direct NLLB translations.",
        flush=True,
    )

    translator = InterslavicTranslator()
    batch_size = 8
    for start in range(0, len(direct_sources), batch_size):
        batch = direct_sources[start:start + batch_size]
        outputs = translator.translate_batch(batch)
        if len(outputs) != len(batch):
            raise SystemExit("NLLB translation batch returned an unexpected number of strings")
        for source, translated in zip(batch, outputs):
            valid = bool(translated.strip())
            valid = valid and base.placeholder_signature(source) == base.placeholder_signature(translated)
            valid = valid and protected_signature(source) == protected_signature(translated)
            if not valid:
                translated = translator.structural_translate(source)
            if not translated.strip():
                raise SystemExit(f"Empty Interslavic translation for {source!r}")
            if base.placeholder_signature(source) != base.placeholder_signature(translated):
                raise SystemExit(f"Interslavic placeholder mismatch: {source!r} -> {translated!r}")
            if protected_signature(source) != protected_signature(translated):
                raise SystemExit(f"Interslavic protected-token mismatch: {source!r} -> {translated!r}")
            translated_by_source[source] = translated
        done = min(start + len(batch), len(direct_sources))
        if done % 160 == 0 or done == len(direct_sources):
            print(f"Direct Interslavic translation progress: {done}/{len(direct_sources)}", flush=True)

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, raw_value in source.items():
            source_value = str(raw_value)
            translated = translated_by_source[source_value]
            if base.placeholder_signature(source_value) != base.placeholder_signature(translated):
                raise SystemExit(f"Placeholder mismatch for {key}: {source_value!r} -> {translated!r}")
            result[key] = translated
        return result

    common_isv = translated_payload(common_en)
    delta_121_isv = translated_payload(delta_121_en)
    delta_261_isv = translated_payload(delta_261_en)
    delta_262_isv = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_isv_common_*/lang/isv.json"):
        path.unlink()
    common_items = list(common_isv.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_isv_common_{index + 1:02d}/lang/isv.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_isv_121/lang/isv.json", delta_121_isv)
    write_json(ASSETS / "neoorigins_26_1/lang/isv.json", delta_261_isv)
    write_json(ASSETS / "neoorigins_26_2/lang/isv.json", delta_262_isv)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/isv.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/isv.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Interslavic files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    source_changed = 0
    total_values = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Interslavic refinement: {path}")
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

    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived full Interslavic translation: only {source_changed} values changed"
        )
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Technical project name Origin Architect was not preserved")

    print(
        f"Interslavic full refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        "no isolated-word projection pipeline.",
        flush=True,
    )


if __name__ == "__main__":
    main()
