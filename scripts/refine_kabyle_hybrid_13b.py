#!/usr/bin/env python3
"""Guarded Kabyle refinement using a specialized 1.3B model with generic 1.3B fallback.

Primary translations come from mimech011/nllb-200-kabyle-1.3B. Outputs that
show structural corruption, pathological repetition, or substantial untranslated
English residue are regenerated clause-by-clause with the generic NLLB 1.3B
model. Placeholders and protected technical names are preserved. This remains
automated translation assistance, not native-speaker review.
"""
from __future__ import annotations

import argparse
from collections import Counter
import gc
import re
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import refine_kabyle as core

SOURCE_LANG = core.SOURCE_LANG
TARGET_LANG = core.TARGET_LANG
SPECIALIZED_MODEL = "mimech011/nllb-200-kabyle-1.3B"
TOKENIZER_MODEL = "facebook/nllb-200-distilled-1.3B"
GENERIC_MODEL = "facebook/nllb-200-distilled-1.3B"
BATCH_SIZE = 4
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+)?")
CLAUSE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\s+([—–;])\s+")
ENGLISH_CUES = {
    "the", "and", "you", "your", "with", "while", "other", "still", "into",
    "but", "from", "for", "through", "when", "cannot", "can", "walk", "own",
    "body", "side", "these", "their", "them", "than", "inside", "away",
}


def words(text: str) -> list[str]:
    return [token.casefold() for token in WORD_RE.findall(text)]


def compact_words(text: str) -> str:
    return " ".join(words(text))


def structural_ok(source: str, translated: str) -> bool:
    return bool(translated.strip()) and (
        core.base.placeholder_signature(source) == core.base.placeholder_signature(translated)
        and core.protected_signature(source) == core.protected_signature(translated)
        and not core.SUSPICIOUS_UNKNOWN_RE.search(translated)
    )


def pathological_repetition(source: str, translated: str) -> bool:
    target_words = words(translated)
    if len(target_words) < 8:
        return False
    source_counts = Counter(words(source))
    target_counts = Counter(target_words)
    token, count = target_counts.most_common(1)[0]
    threshold = max(5, (len(target_words) + 3) // 4)
    return count >= threshold and source_counts.get(token, 0) < 3


def untranslated_residue(source: str, translated: str) -> bool:
    source_words = words(source)
    target_words = words(translated)
    if len(source_words) < 5:
        return False
    if compact_words(source) == compact_words(translated):
        return True

    source_compact = compact_words(source)
    target_compact = compact_words(translated)
    source_segments = [
        part.strip(" —–;\t\n")
        for part in re.split(r"(?<=[.!?])\s+|\s+[—–;]\s+", source)
        if part.strip(" —–;\t\n")
    ]
    for segment in source_segments:
        segment_compact = compact_words(segment)
        if len(words(segment)) >= 4 and segment_compact and segment_compact in target_compact:
            return True

    source_set = set(source_words)
    target_set = set(target_words)
    cues = (source_set & target_set) & ENGLISH_CUES
    overlap = len(source_set & target_set) / max(1, len(source_set))
    return len(cues) >= 3 and overlap >= 0.35


def semantic_suspect(source: str, translated: str) -> bool:
    return pathological_repetition(source, translated) or untranslated_residue(source, translated)


class Translator:
    def __init__(self, model_id: str, tokenizer_id: str = TOKENIZER_MODEL) -> None:
        print(f"Loading {model_id} ({SOURCE_LANG} -> {TARGET_LANG})", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_id, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        self.model.eval()
        self.target_id = self.tokenizer.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tokenizer.unk_token_id:
            raise RuntimeError(f"NLLB target language token unavailable: {TARGET_LANG}")

    def translate_batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        encoded = self.tokenizer(
            texts, return_tensors="pt", padding=True, truncation=True, max_length=512
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
        pieces = core.PROTECT_RE.split(source)
        tokens = core.PROTECT_RE.findall(source)
        translated_pieces = list(pieces)
        indices: list[int] = []
        cores: list[str] = []
        affixes: dict[int, tuple[str, str]] = {}
        for index, piece in enumerate(pieces):
            prefix, body, suffix = self.split_structural_affixes(piece)
            if not body:
                continue
            indices.append(index)
            cores.append(body)
            affixes[index] = (prefix, suffix)
        outputs = self.translate_batch(cores)
        if len(outputs) != len(indices):
            raise RuntimeError("Structural fallback returned wrong span count")
        for index, translated in zip(indices, outputs):
            prefix, suffix = affixes[index]
            translated_pieces[index] = prefix + translated.strip() + suffix
        output: list[str] = []
        for index, piece in enumerate(translated_pieces):
            output.append(piece)
            if index < len(tokens):
                output.append(tokens[index])
        return "".join(output)

    def safe_translate(self, source: str) -> str:
        translated = self.translate_batch([source])[0]
        if not structural_ok(source, translated):
            translated = self.structural_translate(source)
        return translated


def split_clauses(source: str) -> list[tuple[str, bool]]:
    """Return (text, translatable) pieces while preserving sentence/clause separators."""
    pieces: list[tuple[str, bool]] = []
    cursor = 0
    for match in re.finditer(r"(?<=[.!?])\s+|\s+[—–;]\s+", source):
        body = source[cursor:match.start()]
        if body:
            pieces.append((body, True))
        pieces.append((match.group(0), False))
        cursor = match.end()
    tail = source[cursor:]
    if tail:
        pieces.append((tail, True))
    return pieces or [(source, True)]


def clause_fallback(translator: Translator, source: str) -> str:
    output: list[str] = []
    for piece, translatable in split_clauses(source):
        if not translatable or not piece.strip():
            output.append(piece)
            continue
        leading = piece[: len(piece) - len(piece.lstrip())]
        trailing = piece[len(piece.rstrip()):]
        body = piece.strip()
        translated = translator.safe_translate(body)
        output.append(leading + translated + trailing)
    return "".join(output)


def final_validate(source: str, translated: str) -> None:
    core.validate_pair(source, translated)
    if pathological_repetition(source, translated):
        raise SystemExit(f"Kabyle repetition gate failed: {source!r} -> {translated!r}")
    if untranslated_residue(source, translated):
        raise SystemExit(f"Kabyle English-residue gate failed: {source!r} -> {translated!r}")


def translate_direct_sources(direct_sources: list[str]) -> dict[str, str]:
    primary = Translator(SPECIALIZED_MODEL)
    translated: dict[str, str] = {}
    fallback_sources: list[str] = []

    for start in range(0, len(direct_sources), BATCH_SIZE):
        batch = direct_sources[start:start + BATCH_SIZE]
        outputs = primary.translate_batch(batch)
        if len(outputs) != len(batch):
            raise SystemExit("Specialized Kabyle batch returned wrong string count")
        for source, candidate in zip(batch, outputs):
            if not structural_ok(source, candidate):
                candidate = primary.structural_translate(source)
            if not structural_ok(source, candidate) or semantic_suspect(source, candidate):
                fallback_sources.append(source)
            else:
                final_validate(source, candidate)
                translated[source] = candidate
        done = min(start + len(batch), len(direct_sources))
        if done % 100 == 0 or done == len(direct_sources):
            print(
                f"Specialized Kabyle progress: {done}/{len(direct_sources)}; "
                f"fallback queued={len(fallback_sources)}",
                flush=True,
            )

    del primary
    gc.collect()

    if fallback_sources:
        print(f"Regenerating {len(fallback_sources)} suspect outputs with generic 1.3B clause fallback", flush=True)
        fallback = Translator(GENERIC_MODEL, GENERIC_MODEL)
        for index, source in enumerate(fallback_sources, 1):
            candidate = clause_fallback(fallback, source)
            if not structural_ok(source, candidate):
                candidate = fallback.structural_translate(source)
            final_validate(source, candidate)
            translated[source] = candidate
            if index % 20 == 0 or index == len(fallback_sources):
                print(f"Generic Kabyle fallback progress: {index}/{len(fallback_sources)}", flush=True)
        del fallback
        gc.collect()

    if set(translated) != set(direct_sources):
        missing = sorted(set(direct_sources) - set(translated))
        raise SystemExit(f"Hybrid Kabyle coverage mismatch; missing={missing[:3]!r}")
    return translated


def write_shard(shard_index: int, shard_count: int, output: Path) -> None:
    if shard_count < 1 or not 0 <= shard_index < shard_count:
        raise SystemExit(f"Invalid shard {shard_index}/{shard_count}")
    *_, direct_sources = core.build_pool()
    shard_sources = direct_sources[shard_index::shard_count]
    print(
        f"Hybrid Kabyle shard {shard_index + 1}/{shard_count}: "
        f"{len(shard_sources)} of {len(direct_sources)} direct strings",
        flush=True,
    )
    translated = translate_direct_sources(shard_sources)
    core.write_json(output, {key: translated[key] for key in sorted(translated)})
    print(f"Hybrid Kabyle shard {shard_index + 1}/{shard_count} wrote {output}", flush=True)


def collect_shards(directory: Path, expected_sources: list[str]) -> dict[str, str]:
    combined = core.collect_shards(directory, expected_sources)
    for source, translated in combined.items():
        final_validate(source, translated)
    return combined


def apply_and_validate(shard_translations: dict[str, str] | None = None) -> None:
    *_, direct_sources = core.build_pool()
    if shard_translations is None:
        shard_translations = translate_direct_sources(direct_sources)
    for source, translated in shard_translations.items():
        final_validate(source, translated)
    core.apply_and_validate(shard_translations)


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
        *_, direct_sources = core.build_pool()
        apply_and_validate(collect_shards(args.merge_shards, direct_sources))
        return

    apply_and_validate()


if __name__ == "__main__":
    main()
