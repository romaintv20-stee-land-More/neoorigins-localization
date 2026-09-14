#!/usr/bin/env python3
"""Refine Kölsch (`ksh`) fallback files with direct English -> Kölsch MT.

Uses exact whole-string Minecraft corpus matches first, then the multilingual
Helsinki OPUS model with the required sentence-initial `>>ksh<<` target prefix.
No Standard German pivot and no isolated-word projection are used.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_kolsch as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "Helsinki-NLP/opus-mt-en-mul"
TARGET_TOKEN = ">>ksh<<"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)
SUSPICIOUS_UNKNOWN_RE = re.compile(
    r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE
)


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return PROTECT_RE.findall(text)


def sanitize_output(source: str, translated: str) -> str:
    """Remove model-invented Minecraft section signs when none exist in source.

    Real section formatting is still protected structurally whenever the source
    contains it. Only bare hallucinated `§` characters are removed here, keeping
    the following translated character intact.
    """
    if "§" not in source and "§" in translated:
        translated = translated.replace("§", "")
    return translated.strip()


def build_sources():
    neo_121 = read_json(ROOT / "build/ksh-discovery-mc-1.21.1/ksh_missing_en.json")
    neo_261 = read_json(ROOT / "build/ksh-discovery-mc-26.1/ksh_missing_en.json")
    neo_262 = read_json(ROOT / "build/ksh-discovery-mc-26.2/ksh_missing_en.json")

    common = {
        key: value for key, value in neo_121.items()
        if neo_261.get(key) == value and neo_262.get(key) == value
    }
    delta_121 = {key: value for key, value in neo_121.items() if key not in common}
    delta_261 = {key: value for key, value in neo_261.items() if key not in common}
    delta_262 = {key: value for key, value in neo_262.items() if key not in common}

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
    addons = {namespace: read_json(path) for namespace, path in source_files.items()}
    shared = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {
        key: value for key, value in addons["origins_backgrounds_two"].items()
        if key not in shared
    }
    addons["origins_backgrounds_iss"] = {
        key: value for key, value in addons["origins_backgrounds_iss"].items()
        if key not in shared
    }
    return common, delta_121, delta_261, delta_262, addons


class KolschTranslator:
    def __init__(self) -> None:
        print(f"Loading direct Kölsch OPUS model: {MODEL_ID} target={TARGET_TOKEN}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        print("Kölsch target selection: sentence-initial >>ksh<< prefix", flush=True)

    def translate_batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        tagged = [f"{TARGET_TOKEN} {text}" for text in texts]
        encoded = self.tokenizer(
            tagged,
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
            value.strip()
            for value in self.tokenizer.batch_decode(generated, skip_special_tokens=True)
        ]

    @staticmethod
    def split_affixes(piece: str) -> tuple[str, str, str]:
        alpha = [index for index, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        first, last = alpha[0], alpha[-1]
        return piece[:first], piece[first:last + 1], piece[last + 1:]

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        translated = list(pieces)
        indexes: list[int] = []
        cores: list[str] = []
        affixes: dict[int, tuple[str, str]] = {}
        for index, piece in enumerate(pieces):
            prefix, core, suffix = self.split_affixes(piece)
            if core:
                indexes.append(index)
                cores.append(core)
                affixes[index] = (prefix, suffix)
        outputs = self.translate_batch(cores)
        if len(outputs) != len(indexes):
            raise RuntimeError("Structural Kölsch translation returned the wrong span count")
        for index, output in zip(indexes, outputs):
            prefix, suffix = affixes[index]
            translated[index] = prefix + sanitize_output(source, output) + suffix
        result: list[str] = []
        for index, piece in enumerate(translated):
            result.append(piece)
            if index < len(tokens):
                result.append(tokens[index])
        return "".join(result)


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/ksh.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Kölsch files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    common_en, delta_121_en, delta_261_en, delta_262_en, addons_en = build_sources()
    payloads = [common_en, delta_121_en, delta_261_en, delta_262_en, *addons_en.values()]
    unique_sources = sorted({str(value) for payload in payloads for value in payload.values()})

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
        f"Kölsch refinement pool: {len(unique_sources)} unique strings; "
        f"{len(unique_sources) - len(direct_sources)} manual/corpus hits; "
        f"{len(direct_sources)} direct OPUS translations.", flush=True
    )

    translator = KolschTranslator()
    batch_size = 16
    for start in range(0, len(direct_sources), batch_size):
        batch = direct_sources[start:start + batch_size]
        outputs = translator.translate_batch(batch)
        if len(outputs) != len(batch):
            raise SystemExit("OPUS translation batch returned an unexpected number of strings")
        for source, output in zip(batch, outputs):
            translated = sanitize_output(source, output)
            valid = bool(translated.strip())
            valid &= base.placeholder_signature(source) == base.placeholder_signature(translated)
            valid &= protected_signature(source) == protected_signature(translated)
            if not valid:
                translated = sanitize_output(source, translator.structural_translate(source))
            if not translated.strip():
                raise SystemExit(f"Empty Kölsch translation for {source!r}")
            if base.placeholder_signature(source) != base.placeholder_signature(translated):
                raise SystemExit(f"Kölsch placeholder mismatch: {source!r} -> {translated!r}")
            if protected_signature(source) != protected_signature(translated):
                raise SystemExit(f"Kölsch protected-token mismatch: {source!r} -> {translated!r}")
            if SUSPICIOUS_UNKNOWN_RE.search(translated):
                raise SystemExit(f"Suspicious Kölsch output: {source!r} -> {translated!r}")
            translated_by_source[source] = translated
        done = min(start + len(batch), len(direct_sources))
        if done % 160 == 0 or done == len(direct_sources):
            print(f"Direct Kölsch translation progress: {done}/{len(direct_sources)}", flush=True)

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        return {key: translated_by_source[str(value)] for key, value in source.items()}

    common_ksh = translated_payload(common_en)
    for path in ASSETS.glob("neoorigins_ksh_common_*/lang/ksh.json"):
        path.unlink()
    common_items = list(common_ksh.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_ksh_common_{index + 1:02d}/lang/ksh.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_ksh_121/lang/ksh.json", translated_payload(delta_121_en))
    write_json(ASSETS / "neoorigins_26_1/lang/ksh.json", translated_payload(delta_261_en))
    write_json(ASSETS / "neoorigins_26_2/lang/ksh.json", translated_payload(delta_262_en))
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/ksh.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/ksh.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Kölsch files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    total_values = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly: {path}")
        for key, value in new_data.items():
            total_values += 1
            seen[key] = str(value)
            if old_data[key] != value:
                changed_values += 1

    source_changed = sum(
        1 for payload in payloads for value in payload.values()
        if translated_by_source[str(value)] != str(value)
    )
    text = "\n".join(str(value) for data in after.values() for value in data.values())
    if TARGET_TOKEN in text:
        raise SystemExit("OPUS target marker survived generated Kölsch output")
    if SUSPICIOUS_UNKNOWN_RE.search(text):
        raise SystemExit("Suspicious unknown-character artifacts survived Kölsch output")
    if source_changed < 2500:
        raise SystemExit(f"Too many English values survived: only {source_changed} source values changed")
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Technical project name Origin Architect was not preserved")

    red_translation = exact.get("Red")
    random_translation = seen.get("button.neoorigins.random")
    if red_translation and random_translation and random_translation.casefold() == red_translation.casefold():
        raise SystemExit(f"Semantic smoke test failed: Random == Red ({random_translation!r})")
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"):
        raise SystemExit("Semantic smoke test failed: night-vision on/off labels are identical")

    print(
        f"Kölsch direct refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        "semantic smoke tests and structural gates passed; no German pivot or isolated-word projection.",
        flush=True,
    )


if __name__ == "__main__":
    main()
