#!/usr/bin/env python3
"""Repair high-confidence semantic failures in specialized Kabyle 1.3B shards."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import refine_kabyle as rk

MODEL_ID = "facebook/nllb-200-distilled-1.3B"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "kab_Latn"
# Unicode-aware: this keeps Kabyle letters such as ḥ, ṛ and ẓ inside words.
WORD_RE = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)?", re.UNICODE)
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
UNKNOWN_RE = re.compile(r"(?:^|[\s>+\-•])\?[^\W\d_]", re.MULTILINE | re.UNICODE)
ENGLISH = {
    "a", "an", "the", "and", "or", "but", "your", "you", "yours", "with",
    "without", "while", "when", "where", "who", "which", "that", "this",
    "these", "those", "into", "through", "from", "for", "of", "to", "in",
    "on", "at", "by", "other", "still", "can", "cannot", "will", "not",
    "is", "are", "was", "were", "be", "being", "been", "it", "its",
}
KNOWN_BAD = {
    "Can eat cobblestone, stone, granite, diorite, andesite, tuff, deepslate, cobbled deepslate, basalt, and blackstone for modest nutrition. Won't go down on a full stomach.",
    "Spawn with an Efficiency I stone pickaxe.",
    "Immune to Regeneration, Instant Health, and Poison. Other potion effects still apply.",
    "A master of death who commands undead minions — wither skeletons and archers fight at your side, but your own life force is bound to theirs.",
    "A warper of gravitational fields who bends space itself. Pull enemies into a crushing singularity or blast them away — but your own body is untethered from the earth.",
    "Toggle: walk through solid blocks. While inside a block, fly freely (jump = up, shift = down). Obsidian, crying obsidian, and bedrock block your passage. Phasing drains hunger.",
}


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def words(text: str) -> list[str]:
    return [word.casefold() for word in WORD_RE.findall(text)]


def issue(source: str, translated: str) -> str | None:
    sw, tw = words(source), words(translated)
    if len(sw) >= 4 and sw == tw:
        return "unchanged English"
    if len(tw) >= 8:
        for index in range(len(tw) - 2):
            if tw[index] == tw[index + 1] == tw[index + 2]:
                return "repetition collapse"
        counts = Counter(word for word in tw if len(word) >= 4)
        if counts:
            _, count = counts.most_common(1)[0]
            if count >= 6 and count / len(tw) >= 0.20:
                return "repetition collapse"
    english_hits = sum(word in ENGLISH for word in tw)
    if len(tw) >= 5 and english_hits >= 3 and english_hits / len(tw) >= 0.12:
        return "English grammar leakage"
    source_signals = [word for word in sw if word in ENGLISH]
    if len(source_signals) >= 4:
        target = set(tw)
        overlap = sum(word in target for word in source_signals)
        if overlap >= 4 and overlap / len(source_signals) >= 0.50:
            return "large English prose overlap"
    if len(sw) >= 18 and len(tw) <= max(4, int(len(sw) * 0.32)):
        return "severe truncation"
    if UNKNOWN_RE.search(translated):
        return "unknown-token artifact"
    return None


class GenericKabyle:
    def __init__(self) -> None:
        print(f"Loading semantic fallback model: {MODEL_ID}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.target_id = self.tokenizer.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tokenizer.unk_token_id:
            raise SystemExit(f"Missing target token {TARGET_LANG}")

    def batch(self, texts: list[str]) -> list[str]:
        encoded = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.inference_mode():
            generated = self.model.generate(
                **encoded, forced_bos_token_id=self.target_id,
                num_beams=4, max_new_tokens=512, early_stopping=True,
            )
        return [text.strip() for text in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    def piece(self, text: str) -> str:
        alpha = [i for i, char in enumerate(text) if char.isalpha()]
        if not alpha:
            return text
        prefix, core, suffix = text[:alpha[0]], text[alpha[0]:alpha[-1] + 1], text[alpha[-1] + 1:]
        clauses = [part for part in SENTENCE_RE.split(core) if part]
        return prefix + " ".join(self.batch(clauses)) + suffix

    def translate(self, source: str) -> str:
        pieces = rk.PROTECT_RE.split(source)
        tokens = rk.PROTECT_RE.findall(source)
        out: list[str] = []
        for index, piece in enumerate(pieces):
            out.append(self.piece(piece))
            if index < len(tokens):
                out.append(tokens[index])
        translated = "".join(out)
        rk.validate_pair(source, translated)
        return translated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    directory = parser.parse_args().directory
    files = sorted(directory.glob("*.json"))
    if not files:
        raise SystemExit(f"No shard JSON files in {directory}")

    payloads = {path: read_json(path) for path in files}
    suspects: list[tuple[Path, str, str, str]] = []
    for path, payload in payloads.items():
        for source, translated in payload.items():
            rk.validate_pair(source, translated)
            reason = issue(source, translated)
            if source in KNOWN_BAD or reason:
                suspects.append((path, source, translated, reason or "known bad source"))

    total = sum(len(payload) for payload in payloads.values())
    print(f"Kabyle strict semantic scan: {total} strings, {len(suspects)} suspects.", flush=True)
    if suspects:
        translator = GenericKabyle()
        for index, (path, source, old, reason) in enumerate(suspects, 1):
            new = translator.translate(source)
            remaining = issue(source, new)
            if remaining:
                raise SystemExit(f"Kabyle fallback still fails ({remaining}; was {reason}): {source!r} -> {new!r}")
            if new == old:
                raise SystemExit(f"Kabyle repair made no change for suspect: {source!r}")
            payloads[path][source] = new
            print(f"Repaired Kabyle outlier {index}/{len(suspects)}: {reason}: {source[:90]!r}", flush=True)
        for path, payload in payloads.items():
            write_json(path, payload)

    remaining = []
    for payload in payloads.values():
        for source, translated in payload.items():
            rk.validate_pair(source, translated)
            reason = issue(source, translated)
            if reason:
                remaining.append((source, reason))
    if remaining:
        raise SystemExit(f"Kabyle strict semantic scan left {len(remaining)} suspects; samples={remaining[:5]!r}")
    print("Kabyle strict semantic repair passed.", flush=True)


if __name__ == "__main__":
    main()
