#!/usr/bin/env python3
"""Sharded direct English -> Māori refinement with NLLB 1.3B.

Reuses the pinned source discovery and exact Minecraft corpus logic from the
existing Māori pipeline, while translating only unmatched whole strings with
facebook/nllb-200-distilled-1.3B. No pivot and no isolated-word projection.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import refine_maori as legacy

ROOT = legacy.ROOT
ASSETS = legacy.ASSETS
BASE = legacy.base
MODEL_ID = "facebook/nllb-200-distilled-1.3B"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "mri_Latn"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",
    re.IGNORECASE,
)
TECHNICAL_CASEFOLD = {
    "neoorigins", "origin architect", "hud", "json", "xp", "hp",
    "neoforge", "minecraft", "curseforge",
}
SUSPICIOUS_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return [
        token.casefold() if token.casefold() in TECHNICAL_CASEFOLD else token
        for token in PROTECT_RE.findall(text)
    ]


def build_pool():
    common, d121, d261, d262, addons = legacy.build_sources()
    payloads = [common, d121, d261, d262, *addons.values()]
    unique = sorted({str(v) for payload in payloads for v in payload.values()})
    exact = BASE.build_corpus_map()
    translated: dict[str, str] = {}
    direct: list[str] = []
    for source in unique:
        if source == "":
            translated[source] = ""
        elif source in BASE.MANUAL_VALUES:
            translated[source] = BASE.MANUAL_VALUES[source]
        elif source in exact:
            translated[source] = exact[source]
        else:
            direct.append(source)
    return common, d121, d261, d262, addons, payloads, exact, translated, direct


class Translator:
    def __init__(self) -> None:
        print(f"Loading Māori 1.3B: {SOURCE_LANG}->{TARGET_LANG}", flush=True)
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.target_id = self.tok.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tok.unk_token_id:
            raise RuntimeError(f"Missing NLLB target token {TARGET_LANG}")

    def batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        enc = self.tok(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.inference_mode():
            out = self.model.generate(
                **enc,
                forced_bos_token_id=self.target_id,
                num_beams=4,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [v.strip() for v in self.tok.batch_decode(out, skip_special_tokens=True)]

    @staticmethod
    def affixes(piece: str) -> tuple[str, str, str]:
        alpha = [i for i, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        return piece[:alpha[0]], piece[alpha[0]:alpha[-1] + 1], piece[alpha[-1] + 1:]

    def structural(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        out = list(pieces)
        indices: list[int] = []
        cores: list[str] = []
        aff: dict[int, tuple[str, str]] = {}
        for i, piece in enumerate(pieces):
            pre, core, suf = self.affixes(piece)
            if core:
                indices.append(i)
                cores.append(core)
                aff[i] = (pre, suf)
        vals = self.batch(cores)
        if len(vals) != len(indices):
            raise RuntimeError("Māori structural span mismatch")
        for i, value in zip(indices, vals):
            pre, suf = aff[i]
            out[i] = pre + value.strip() + suf
        result: list[str] = []
        for i, piece in enumerate(out):
            result.append(piece)
            if i < len(tokens):
                result.append(tokens[i])
        return "".join(result)


def validate_pair(source: str, value: str) -> None:
    if source == "" and value == "":
        return
    if not value.strip():
        raise SystemExit(f"Empty Māori translation: {source!r}")
    if BASE.placeholder_signature(source) != BASE.placeholder_signature(value):
        raise SystemExit(f"Māori placeholder mismatch: {source!r}->{value!r}")
    if protected_signature(source) != protected_signature(value):
        raise SystemExit(f"Māori protected-token mismatch: {source!r}->{value!r}")
    if SUSPICIOUS_RE.search(value):
        raise SystemExit(f"Suspicious Māori output: {source!r}->{value!r}")


def translate_sources(sources: list[str]) -> dict[str, str]:
    mt = Translator()
    result: dict[str, str] = {}
    batch_size = 4
    for start in range(0, len(sources), batch_size):
        batch = sources[start:start + batch_size]
        values = mt.batch(batch)
        if len(values) != len(batch):
            raise SystemExit("Māori 1.3B batch size mismatch")
        for source, value in zip(batch, values):
            valid = bool(value.strip())
            valid = valid and BASE.placeholder_signature(source) == BASE.placeholder_signature(value)
            valid = valid and protected_signature(source) == protected_signature(value)
            if not valid:
                value = mt.structural(source)
            validate_pair(source, value)
            result[source] = value
        done = min(start + len(batch), len(sources))
        if done % 40 == 0 or done == len(sources):
            print(f"Māori 1.3B progress: {done}/{len(sources)}", flush=True)
    return result


def write_shard(index: int, count: int, output: Path) -> None:
    if count < 1 or not 0 <= index < count:
        raise SystemExit(f"Invalid shard {index}/{count}")
    *_, direct = build_pool()
    selected = direct[index::count]
    print(f"Māori shard {index + 1}/{count}: {len(selected)} of {len(direct)} direct strings", flush=True)
    translated = translate_sources(selected)
    if set(translated) != set(selected):
        raise SystemExit("Māori shard coverage mismatch")
    write_json(output, {k: translated[k] for k in sorted(translated)})
    print(f"Māori shard {index + 1}/{count} passed", flush=True)


def collect_shards(directory: Path, expected: list[str]) -> dict[str, str]:
    files = sorted(directory.glob("*.json"))
    if not files:
        raise SystemExit("No Māori shard artifacts found")
    combined: dict[str, str] = {}
    for path in files:
        for source, value in read_json(path).items():
            if source in combined and combined[source] != value:
                raise SystemExit(f"Conflicting Māori shard value for {source!r}")
            combined[source] = value
    if set(combined) != set(expected):
        missing = sorted(set(expected) - set(combined))
        extra = sorted(set(combined) - set(expected))
        raise SystemExit(f"Māori shard coverage mismatch: missing={len(missing)} extra={len(extra)} sample={missing[:3]!r}")
    for source, value in combined.items():
        validate_pair(source, value)
    print(f"Merged {len(files)} Māori shards covering {len(combined)} direct strings", flush=True)
    return combined


def apply_and_validate(shard_map: dict[str, str]) -> None:
    before_files = sorted(ASSETS.glob("**/lang/mi_nz.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Māori files, found {len(before_files)}")
    before = {p: read_json(p) for p in before_files}
    common, d121, d261, d262, addons, payloads, exact, translated, direct = build_pool()
    if set(shard_map) != set(direct):
        raise SystemExit("Māori merged map does not exactly cover direct pool")
    translated.update(shard_map)

    def payload(src: dict[str, str]) -> dict[str, str]:
        out: dict[str, str] = {}
        for key, raw in src.items():
            source = str(raw)
            value = translated[source]
            validate_pair(source, value)
            out[key] = value
        return out

    items = list(payload(common).items())
    for p in ASSETS.glob("neoorigins_mi_common_*/lang/mi_nz.json"):
        p.unlink()
    for i in range((len(items) + 149) // 150):
        write_json(ASSETS / f"neoorigins_mi_common_{i + 1:02d}/lang/mi_nz.json", dict(items[i * 150:(i + 1) * 150]))
    write_json(ASSETS / "neoorigins_mi_121/lang/mi_nz.json", payload(d121))
    write_json(ASSETS / "neoorigins_26_1/lang/mi_nz.json", payload(d261))
    write_json(ASSETS / "neoorigins_26_2/lang/mi_nz.json", payload(d262))
    for namespace, src in addons.items():
        write_json(ASSETS / namespace / "lang/mi_nz.json", payload(src))

    after_files = sorted(ASSETS.glob("**/lang/mi_nz.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Māori file count changed: {len(after_files)}")
    after = {p: read_json(p) for p in after_files}
    seen: dict[str, str] = {}
    changed = total = 0
    for p, data in after.items():
        if set(before[p]) != set(data):
            raise SystemExit(f"Māori key set changed: {p}")
        for key, value in data.items():
            total += 1
            seen[key] = str(value)
            changed += before[p][key] != value

    source_changed = sum(
        1 for src in payloads for raw in src.values()
        if translated[str(raw)] != str(raw)
    )
    text = "\n".join(str(v) for data in after.values() for v in data.values())
    if TARGET_LANG in text or SUSPICIOUS_RE.search(text):
        raise SystemExit("Māori 1.3B target marker/artifact survived")
    if source_changed < 2500:
        raise SystemExit(f"Too many English values survived Māori 1.3B: {source_changed}")
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Origin Architect changed")
    red = exact.get("Red")
    random = seen.get("button.neoorigins.random")
    if red and random and red.casefold() == random.casefold():
        raise SystemExit("Random translated as Red")
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"):
        raise SystemExit("Night vision on/off identical")
    print(f"Māori 1.3B refinement passed: {total} values; {changed} prior values changed; {source_changed} source values changed", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard-index", type=int)
    parser.add_argument("--shard-count", type=int)
    parser.add_argument("--shard-output", type=Path)
    parser.add_argument("--merge-shards", type=Path)
    args = parser.parse_args()
    shard_args = (args.shard_index, args.shard_count, args.shard_output)
    if any(v is not None for v in shard_args):
        if not all(v is not None for v in shard_args) or args.merge_shards is not None:
            raise SystemExit("Invalid Māori shard arguments")
        write_shard(args.shard_index, args.shard_count, args.shard_output)
        return
    if args.merge_shards is not None:
        *_, direct = build_pool()
        apply_and_validate(collect_shards(args.merge_shards, direct))
        return
    raise SystemExit("Use shard mode or --merge-shards for Māori 1.3B")


if __name__ == "__main__":
    main()
