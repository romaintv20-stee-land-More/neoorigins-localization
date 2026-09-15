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
WORD_RE = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)?", re.UNICODE)
CLAUSE_SPLIT_RE = re.compile(r"(\s+[—–]\s+|(?<=[.!?])\s+|;\s+)")
UNKNOWN_RE = re.compile(r"(?:^|[\s>+\-•])\?[^\W\d_]", re.MULTILINE | re.UNICODE)

# Keep project names and Minecraft-specific item/effect names stable when the
# generic fallback repairs a damaged prose string. This is safer than letting a
# general MT model collapse a whole list of distinct game items into one noun.
EXTRA_PROTECTED = [
    "Medieval Origins", "Instant Health", "Efficiency I", "wither skeletons",
    "crying obsidian", "cobbled deepslate", "deepslate iron ore", "raw iron blocks",
    "iron ingots", "raw iron", "iron nuggets", "iron ore", "cobblestone", "granite",
    "diorite", "andesite", "tuff", "deepslate", "basalt", "blackstone", "stone",
    "Obsidian", "bedrock", "Regeneration", "Poison",
]
_EXTRA = "|".join(re.escape(value) for value in sorted(EXTRA_PROTECTED, key=len, reverse=True))
REPAIR_PROTECT_RE = re.compile(rf"(?:{rk.PROTECT_RE.pattern}|{_EXTRA})", re.IGNORECASE)

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
    "Medieval Origins: Tertiary Active",
    "NeoOrigins: Grant Loot Pool",
}

# The generic NLLB model leaves this short FTB Quests reward label unchanged.
# Use an attested Kabyle rendering instead of accepting English UI text:
# efk = give/grant, agraw = group, taɣawsa = object/thing.
MANUAL_REPAIRS = {
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Efk agraw n tɣawsiwin",
}


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def words(text: str) -> list[str]:
    return [word.casefold() for word in WORD_RE.findall(text)]


def semantic_words(text: str) -> list[str]:
    return words(REPAIR_PROTECT_RE.sub(" ", text))


def repetition_collapse(source_words: list[str], target_words: list[str]) -> bool:
    if len(target_words) < 8:
        return False
    for index in range(len(target_words) - 2):
        if target_words[index] == target_words[index + 1] == target_words[index + 2]:
            return True

    source_counts = Counter(word for word in source_words if len(word) >= 4)
    target_counts = Counter(word for word in target_words if len(word) >= 4)
    if not target_counts:
        return False
    _, target_count = target_counts.most_common(1)[0]
    source_count = source_counts.most_common(1)[0][1] if source_counts else 0
    source_ratio = source_count / max(1, len(source_words))
    target_ratio = target_count / len(target_words)
    return (
        target_count >= 6
        and target_count >= source_count + 5
        and target_ratio >= max(0.28, source_ratio + 0.18)
    )


def issue(source: str, translated: str) -> str | None:
    sw, tw = semantic_words(source), semantic_words(translated)
    if len(sw) >= 4 and sw == tw:
        return "unchanged English"
    if repetition_collapse(sw, tw):
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
        if not texts:
            return []
        encoded = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.inference_mode():
            generated = self.model.generate(
                **encoded,
                forced_bos_token_id=self.target_id,
                num_beams=4,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [text.strip() for text in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    def translate_text_piece(self, text: str) -> str:
        if not any(char.isalpha() for char in text):
            return text
        split = CLAUSE_SPLIT_RE.split(text)
        clause_indices = [index for index in range(0, len(split), 2) if split[index].strip()]
        clauses = [split[index].strip() for index in clause_indices]
        outputs = self.batch(clauses)
        for index, output in zip(clause_indices, outputs):
            original = split[index]
            prefix = original[: len(original) - len(original.lstrip())]
            suffix = original[len(original.rstrip()):]
            terminal = original.rstrip()[-1:] if original.rstrip()[-1:] in ".!?" else ""
            if terminal and not output.endswith(terminal):
                output += terminal
            split[index] = prefix + output + suffix
        return "".join(split)

    def translate(self, source: str) -> str:
        pieces = REPAIR_PROTECT_RE.split(source)
        tokens = REPAIR_PROTECT_RE.findall(source)
        out: list[str] = []
        for index, piece in enumerate(pieces):
            out.append(self.translate_text_piece(piece))
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
            new = MANUAL_REPAIRS.get(source)
            if new is None:
                new = translator.translate(source)
            else:
                rk.validate_pair(source, new)
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
