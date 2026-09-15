#!/usr/bin/env python3
"""Repair rare semantic failures in a generated Kabyle translation shard.

The specialized English->Kabyle 1.3B model remains the primary translator.
This pass detects a small set of high-confidence failure modes (repetition,
large untranslated English spans, severe truncation) and retranslates only
those full sentences/clauses with generic NLLB 1.3B. Structural tokens and
placeholders are preserved and every repaired value is revalidated.
"""
from __future__ import annotations

import argparse
import gc
import json
import re
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_kabyle as base

MODEL_ID = "facebook/nllb-200-distilled-1.3B"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "kab_Latn"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",
    re.IGNORECASE,
)
TECHNICAL_CASEFOLD = {
    "neoorigins", "origin architect", "hud", "json", "xp", "hp",
    "neoforge", "minecraft", "curseforge",
}
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+)?")
SUSPICIOUS_UNKNOWN_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)
CLAUSE_SPLIT_RE = re.compile(r"(\s+[—–]\s+|(?<=[.!?])\s+|;\s+)")

# These are prose signals, not game/item names. Keeping Minecraft item names in
# English is not by itself considered a failure.
ENGLISH_SIGNAL_WORDS = {
    "a", "an", "and", "are", "as", "at", "away", "be", "been", "being", "but",
    "by", "can", "cannot", "commands", "crushing", "death", "drains", "effects",
    "enemies", "fight", "fields", "for", "force", "from", "full", "health", "immune",
    "in", "inside", "instant", "into", "is", "it", "life", "master", "of", "on",
    "other", "own", "passage", "phasing", "poison", "potion", "pull", "regeneration",
    "side", "solid", "space", "spawn", "still", "stomach", "the", "their", "them",
    "these", "through", "to", "toggle", "untethered", "walk", "while", "who", "with",
    "your", "yourself", "apply", "block", "blocks", "body", "bound", "bends", "blast",
    "earth", "freely", "higher", "hunger", "wear", "when", "where", "which",
}


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return [
        token.casefold() if token.casefold() in TECHNICAL_CASEFOLD else token
        for token in PROTECT_RE.findall(text)
    ]


def words(text: str) -> list[str]:
    return [match.group(0).casefold() for match in WORD_RE.finditer(text)]


def quality_issue(source: str, translated: str) -> str | None:
    source_words = words(source)
    translated_words = words(translated)
    if len(source_words) >= 5 and source.strip().casefold() == translated.strip().casefold():
        return "unchanged long English source"

    if len(translated_words) >= 12:
        counts: dict[str, int] = {}
        for word in translated_words:
            if len(word) < 3:
                continue
            counts[word] = counts.get(word, 0) + 1
        if counts:
            top_word, top_count = max(counts.items(), key=lambda item: item[1])
            if top_count >= 5 and top_count / len(translated_words) >= 0.24:
                return f"repetition collapse ({top_word!r} x{top_count})"

    signal_source = [word for word in source_words if word in ENGLISH_SIGNAL_WORDS]
    if len(signal_source) >= 4:
        translated_set = set(translated_words)
        overlap = sum(1 for word in signal_source if word in translated_set)
        if overlap >= 4 and overlap / len(signal_source) >= 0.50:
            return f"large English prose overlap ({overlap}/{len(signal_source)})"

    if len(source_words) >= 18 and len(translated_words) <= max(4, int(len(source_words) * 0.32)):
        return f"severe length collapse ({len(source_words)} -> {len(translated_words)} words)"
    return None


def validate_pair(source: str, translated: str) -> None:
    if not translated.strip():
        raise SystemExit(f"Empty Kabyle repair output for {source!r}")
    if base.placeholder_signature(source) != base.placeholder_signature(translated):
        raise SystemExit(f"Kabyle repair placeholder mismatch: {source!r} -> {translated!r}")
    if protected_signature(source) != protected_signature(translated):
        raise SystemExit(f"Kabyle repair protected-token mismatch: {source!r} -> {translated!r}")
    if SUSPICIOUS_UNKNOWN_RE.search(translated):
        raise SystemExit(f"Suspicious unknown-character artifact after Kabyle repair: {source!r} -> {translated!r}")


class GenericKabyleTranslator:
    def __init__(self) -> None:
        print(f"Loading semantic fallback model: {MODEL_ID}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.target_id = self.tokenizer.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tokenizer.unk_token_id:
            raise SystemExit(f"NLLB target language unavailable: {TARGET_LANG}")

    def translate_batch(self, texts: list[str]) -> list[str]:
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

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        cores: list[str] = []
        positions: list[int] = []
        translated_pieces = list(pieces)
        for index, piece in enumerate(pieces):
            if any(char.isalpha() for char in piece):
                cores.append(piece)
                positions.append(index)
        outputs = self.translate_batch(cores) if cores else []
        for index, value in zip(positions, outputs):
            translated_pieces[index] = value
        result: list[str] = []
        for index, piece in enumerate(translated_pieces):
            result.append(piece)
            if index < len(tokens):
                result.append(tokens[index])
        return "".join(result)

    def translate_clause(self, source: str) -> str:
        translated = self.translate_batch([source])[0]
        if (
            base.placeholder_signature(source) != base.placeholder_signature(translated)
            or protected_signature(source) != protected_signature(translated)
        ):
            translated = self.structural_translate(source)
        validate_pair(source, translated)
        return translated

    def translate_by_clauses(self, source: str) -> str:
        pieces = CLAUSE_SPLIT_RE.split(source)
        text_indices = [
            index for index in range(0, len(pieces), 2)
            if pieces[index].strip()
        ]
        clauses = [pieces[index] for index in text_indices]
        outputs: list[str] = []
        for clause in clauses:
            outputs.append(self.translate_clause(clause))
        for index, output in zip(text_indices, outputs):
            # Keep terminal punctuation already present in the source clause if the
            # model omitted it; do not duplicate punctuation it preserved.
            source_clause = pieces[index]
            terminal = source_clause[-1:] if source_clause[-1:] in ".!?" else ""
            if terminal and not output.endswith(terminal):
                output += terminal
            pieces[index] = output
        translated = "".join(pieces)
        validate_pair(source, translated)
        return translated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    payload = read_json(args.path)
    suspects: list[tuple[str, str, str]] = []
    for source, translated in payload.items():
        validate_pair(source, translated)
        reason = quality_issue(source, translated)
        if reason:
            suspects.append((source, translated, reason))

    if not suspects:
        print(f"Kabyle shard semantic repair: 0 suspects in {len(payload)} translations.", flush=True)
        return

    print(f"Kabyle shard semantic repair: {len(suspects)} suspect translations detected.", flush=True)
    for source, _, reason in suspects:
        print(f"  - {reason}: {source[:180]!r}", flush=True)

    translator = GenericKabyleTranslator()
    repaired = 0
    for source, old_value, reason in suspects:
        new_value = translator.translate_by_clauses(source)
        remaining = quality_issue(source, new_value)
        if remaining:
            raise SystemExit(
                f"Kabyle fallback still fails semantic gate ({remaining}; originally {reason}): "
                f"{source!r} -> {new_value!r}"
            )
        if new_value == old_value:
            raise SystemExit(f"Kabyle semantic fallback made no change for suspect source: {source!r}")
        payload[source] = new_value
        repaired += 1
        print(f"Repaired Kabyle outlier: {source[:100]!r} -> {new_value[:180]!r}", flush=True)

    write_json(args.path, payload)
    del translator
    gc.collect()

    # Final complete shard scan after repair.
    for source, translated in payload.items():
        validate_pair(source, translated)
        issue = quality_issue(source, translated)
        if issue:
            raise SystemExit(f"Kabyle shard still has semantic outlier after repair: {issue}: {source!r}")
    print(f"Kabyle shard semantic repair passed: repaired {repaired}/{len(payload)} translations.", flush=True)


if __name__ == "__main__":
    main()
