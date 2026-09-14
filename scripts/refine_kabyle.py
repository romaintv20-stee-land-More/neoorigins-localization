#!/usr/bin/env python3
"""Refine Kabyle (`kab_kab`) fallback files with direct English -> Kabyle NLLB.

The expensive NLLB pool can be split into deterministic shards. Each shard keeps
beam search at 4 and performs the same placeholder/protected-token validation as
the original monolithic refinement. A merge pass requires exact shard coverage,
reconstructs all 29 locale files, and runs semantic/structural smoke gates.
This is automated translation assistance, not native review.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_kabyle as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "facebook/nllb-200-distilled-600M"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "kab_Latn"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)
SUSPICIOUS_UNKNOWN_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return PROTECT_RE.findall(text)


def build_sources():
    neo_121_en = read_json(ROOT / "build/kab-discovery-mc-1.21.1/kab_kab_missing_en.json")
    neo_261_en = read_json(ROOT / "build/kab-discovery-mc-26.1/kab_kab_missing_en.json")
    neo_262_en = read_json(ROOT / "build/kab-discovery-mc-26.2/kab_kab_missing_en.json")

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


def build_pool():
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
    return (
        common_en,
        delta_121_en,
        delta_261_en,
        delta_262_en,
        addons_en,
        source_payloads,
        exact,
        translated_by_source,
        direct_sources,
    )


class KabyleTranslator:
    def __init__(self) -> None:
        print(f"Loading Kabyle-capable NLLB model: {MODEL_ID} ({SOURCE_LANG} -> {TARGET_LANG})", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.target_id = self.tokenizer.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tokenizer.unk_token_id:
            raise RuntimeError(f"NLLB target language token is unavailable: {TARGET_LANG}")

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
        with torch.inference_mode():
            generated = self.model.generate(
                **encoded,
                forced_bos_token_id=self.target_id,
                num_beams=4,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [value.strip() for value in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    @staticmethod
    def split_structural_affixes(piece: str) -> tuple[str, str, str]:
        alpha = [index for index, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        return piece[:alpha[0]], piece[alpha[0]:alpha[-1] + 1], piece[alpha[-1] + 1:]

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        translated_pieces = list(pieces)
        indices: list[int] = []
        cores: list[str] = []
        affixes: dict[int, tuple[str, str]] = {}
        for index, piece in enumerate(pieces):
            prefix, core, suffix = self.split_structural_affixes(piece)
            if not core:
                continue
            indices.append(index)
            cores.append(core)
            affixes[index] = (prefix, suffix)
        outputs = self.translate_batch(cores)
        if len(outputs) != len(indices):
            raise RuntimeError("Structural Kabyle translation returned the wrong number of spans")
        for index, translated in zip(indices, outputs):
            prefix, suffix = affixes[index]
            translated_pieces[index] = prefix + translated.strip() + suffix
        output: list[str] = []
        for index, piece in enumerate(translated_pieces):
            output.append(piece)
            if index < len(tokens):
                output.append(tokens[index])
        return "".join(output)


def validate_pair(source: str, translated: str) -> None:
    if not translated.strip():
        raise SystemExit(f"Empty Kabyle translation for {source!r}")
    if base.placeholder_signature(source) != base.placeholder_signature(translated):
        raise SystemExit(f"Kabyle placeholder mismatch: {source!r} -> {translated!r}")
    if protected_signature(source) != protected_signature(translated):
        raise SystemExit(f"Kabyle protected-token mismatch: {source!r} -> {translated!r}")
    if SUSPICIOUS_UNKNOWN_RE.search(translated):
        raise SystemExit(f"Suspicious unknown-character artifact in Kabyle output: {source!r} -> {translated!r}")


def translate_direct_sources(direct_sources: list[str]) -> dict[str, str]:
    translator = KabyleTranslator()
    translated_by_source: dict[str, str] = {}
    batch_size = 16
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
            validate_pair(source, translated)
            translated_by_source[source] = translated
        done = min(start + len(batch), len(direct_sources))
        if done % 160 == 0 or done == len(direct_sources):
            print(f"Direct Kabyle translation progress: {done}/{len(direct_sources)}", flush=True)
    return translated_by_source


def write_shard(shard_index: int, shard_count: int, output: Path) -> None:
    if shard_count < 1 or not 0 <= shard_index < shard_count:
        raise SystemExit(f"Invalid shard {shard_index}/{shard_count}")
    *_, direct_sources = build_pool()
    shard_sources = direct_sources[shard_index::shard_count]
    print(
        f"Kabyle shard {shard_index + 1}/{shard_count}: "
        f"{len(shard_sources)} of {len(direct_sources)} direct NLLB strings.",
        flush=True,
    )
    translated = translate_direct_sources(shard_sources)
    if set(translated) != set(shard_sources):
        raise SystemExit("Kabyle shard output coverage mismatch")
    write_json(output, {key: translated[key] for key in sorted(translated)})
    print(f"Kabyle shard {shard_index + 1}/{shard_count} passed and wrote {output}", flush=True)


def collect_shards(directory: Path, expected_sources: list[str]) -> dict[str, str]:
    files = sorted(directory.glob("*.json"))
    if not files:
        raise SystemExit(f"No Kabyle shard files found under {directory}")
    combined: dict[str, str] = {}
    for path in files:
        payload = read_json(path)
        for source, translated in payload.items():
            if source in combined and combined[source] != translated:
                raise SystemExit(f"Conflicting Kabyle shard translations for {source!r}")
            combined[source] = translated
    expected = set(expected_sources)
    actual = set(combined)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise SystemExit(
            f"Kabyle shard coverage mismatch: missing={len(missing)} extra={len(extra)}; "
            f"sample_missing={missing[:3]!r} sample_extra={extra[:3]!r}"
        )
    for source, translated in combined.items():
        validate_pair(source, translated)
    print(f"Merged {len(files)} Kabyle shard files covering {len(combined)} direct translations.", flush=True)
    return combined


def apply_and_validate(shard_translations: dict[str, str] | None = None) -> None:
    before_files = sorted(ASSETS.glob("**/lang/kab_kab.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Kabyle files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    (
        common_en,
        delta_121_en,
        delta_261_en,
        delta_262_en,
        addons_en,
        source_payloads,
        exact,
        translated_by_source,
        direct_sources,
    ) = build_pool()

    print(
        f"Kabyle refinement pool: {len(translated_by_source) + len(direct_sources)} unique strings; "
        f"{len(translated_by_source)} manual/corpus hits; {len(direct_sources)} direct NLLB translations.",
        flush=True,
    )
    if shard_translations is None:
        shard_translations = translate_direct_sources(direct_sources)
    if set(shard_translations) != set(direct_sources):
        raise SystemExit("Direct Kabyle translation map does not exactly cover the required source pool")
    translated_by_source.update(shard_translations)

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, raw_value in source.items():
            source_value = str(raw_value)
            translated = translated_by_source[source_value]
            validate_pair(source_value, translated)
            result[key] = translated
        return result

    common_kab = translated_payload(common_en)
    delta_121_kab = translated_payload(delta_121_en)
    delta_261_kab = translated_payload(delta_261_en)
    delta_262_kab = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_kab_common_*/lang/kab_kab.json"):
        path.unlink()
    common_items = list(common_kab.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_kab_common_{index + 1:02d}/lang/kab_kab.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_kab_121/lang/kab_kab.json", delta_121_kab)
    write_json(ASSETS / "neoorigins_26_1/lang/kab_kab.json", delta_261_kab)
    write_json(ASSETS / "neoorigins_26_2/lang/kab_kab.json", delta_262_kab)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/kab_kab.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/kab_kab.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Kabyle files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    source_changed = 0
    total_values = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Kabyle refinement: {path}")
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
    if TARGET_LANG in text or ">>kab<<" in text:
        raise SystemExit("Translation target marker survived generated output")
    if "unit-format" in text:
        raise SystemExit("Known model artifact 'unit-format' survived Kabyle output")
    if SUSPICIOUS_UNKNOWN_RE.search(text):
        raise SystemExit("Suspicious unknown-character artifacts survived Kabyle output")
    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived full Kabyle translation: only {source_changed} values changed"
        )
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Technical project name Origin Architect was not preserved")

    red_translation = exact.get("Red")
    random_translation = seen.get("button.neoorigins.random")
    if red_translation and random_translation and random_translation.casefold() == red_translation.casefold():
        raise SystemExit(
            f"Semantic smoke test failed: Random was translated exactly like Red ({random_translation!r})"
        )
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"):
        raise SystemExit("Semantic smoke test failed: night-vision on/off labels are identical")

    print(
        f"Kabyle NLLB refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} prior values; source translations changed {source_changed} values; "
        "semantic smoke tests and structural gates passed; no isolated-word projection pipeline.",
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
        if not all(value is not None for value in shard_args):
            raise SystemExit("--shard-index, --shard-count and --shard-output must be provided together")
        if args.merge_shards is not None:
            raise SystemExit("Shard translation and shard merge modes are mutually exclusive")
        write_shard(args.shard_index, args.shard_count, args.shard_output)
        return

    if args.merge_shards is not None:
        *_, direct_sources = build_pool()
        apply_and_validate(collect_shards(args.merge_shards, direct_sources))
        return

    apply_and_validate()


if __name__ == "__main__":
    main()
