#!/usr/bin/env python3
"""Repair rare semantic failures in specialized Kabyle 1.3B shard output.

The specialized English->Kabyle model is the primary translator. This pass only
retranslates outputs that show clear degeneration (repetition, unchanged English,
English prose leakage, severe truncation, or malformed unknown-token artifacts),
using the generic NLLB 1.3B Kabyle target. Multi-sentence/problematic strings are
translated sentence-by-sentence so the fallback cannot silently drop later clauses.
Placeholders and protected technical tokens are preserved exactly. This is
automated translation assistance, not native-speaker review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from collections import Counter

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import refine_kabyle as rk

MODEL_ID = "facebook/nllb-200-distilled-1.3B"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "kab_Latn"
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ']+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")
SUSPICIOUS_UNKNOWN_RE = re.compile(
    r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE
)
ENGLISH_FUNCTION_WORDS = {
    "a", "an", "the", "and", "or", "but", "your", "you", "yours", "with",
    "without", "while", "when", "where", "who", "which", "that", "this",
    "these", "those", "into", "through", "from", "for", "of", "to", "in",
    "on", "at", "by", "other", "still", "can", "cannot", "will", "not",
    "is", "are", "was", "were", "be", "being", "been", "it", "its",
}
KNOWN_BAD_SOURCES = {
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
    return [w.casefold() for w in WORD_RE.findall(text)]


def repetition_collapse(text: str) -> bool:
    ws = words(text)
    if len(ws) < 8:
        return False
    for i in range(len(ws) - 2):
        if ws[i] == ws[i + 1] == ws[i + 2]:
            return True
    counts = Counter(w for w in ws if len(w) >= 4)
    if not counts:
        return False
    _, top = counts.most_common(1)[0]
    return top >= 6 and top / len(ws) >= 0.20


def english_leakage(text: str) -> bool:
    ws = words(text)
    if len(ws) < 5:
        return False
    hits = sum(w in ENGLISH_FUNCTION_WORDS for w in ws)
    return hits >= 3 and hits / len(ws) >= 0.12


def source_english_overlap(source: str, translated: str) -> bool:
    source_signals = [w for w in words(source) if w in ENGLISH_FUNCTION_WORDS]
    if len(source_signals) < 4:
        return False
    translated_words = set(words(translated))
    overlap = sum(1 for w in source_signals if w in translated_words)
    return overlap >= 4 and overlap / len(source_signals) >= 0.50


def severe_length_collapse(source: str, translated: str) -> bool:
    source_words = words(source)
    translated_words = words(translated)
    return (
        len(source_words) >= 18
        and len(translated_words) <= max(4, int(len(source_words) * 0.32))
    )


def malformed_unknown_artifact(text: str) -> bool:
    return bool(SUSPICIOUS_UNKNOWN_RE.search(text))


def suspicious(source: str, translated: str) -> bool:
    if source in KNOWN_BAD_SOURCES:
        return True
    if repetition_collapse(translated):
        return True
    sw = words(source)
    tw = words(translated)
    if len(sw) >= 4 and sw == tw:
        return True
    if english_leakage(translated) or source_english_overlap(source, translated):
        return True
    if severe_length_collapse(source, translated):
        return True
    if malformed_unknown_artifact(translated):
        return True
    return False


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
        return [x.strip() for x in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    def translate_piece(self, piece: str) -> str:
        alpha = [i for i, ch in enumerate(piece) if ch.isalpha()]
        if not alpha:
            return piece
        prefix = piece[:alpha[0]]
        core = piece[alpha[0]:alpha[-1] + 1]
        suffix = piece[alpha[-1] + 1:]
        clauses = [c for c in SENTENCE_RE.split(core) if c]
        outputs = self.batch(clauses)
        if len(outputs) != len(clauses):
            raise SystemExit("Generic Kabyle fallback returned wrong clause count")
        return prefix + " ".join(outputs) + suffix

    def structural(self, source: str) -> str:
        pieces = rk.PROTECT_RE.split(source)
        tokens = rk.PROTECT_RE.findall(source)
        out: list[str] = []
        for i, piece in enumerate(pieces):
            out.append(self.translate_piece(piece))
            if i < len(tokens):
                out.append(tokens[i])
        return "".join(out)


def validate_repaired(source: str, translated: str) -> None:
    rk.validate_pair(source, translated)
    if repetition_collapse(translated):
        raise SystemExit(f"Kabyle fallback still collapsed into repetition: {source!r} -> {translated!r}")
    if english_leakage(translated) or source_english_overlap(source, translated):
        raise SystemExit(f"Kabyle fallback still contains excessive English prose: {source!r} -> {translated!r}")
    if len(words(source)) >= 4 and words(source) == words(translated):
        raise SystemExit(f"Kabyle fallback remained unchanged English: {source!r}")
    if severe_length_collapse(source, translated):
        raise SystemExit(f"Kabyle fallback is severely truncated: {source!r} -> {translated!r}")
    if malformed_unknown_artifact(translated):
        raise SystemExit(f"Kabyle fallback contains malformed unknown-token artifact: {source!r} -> {translated!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    files = sorted(args.directory.glob("*.json"))
    if not files:
        raise SystemExit(f"No shard JSON files in {args.directory}")

    payloads = {p: read_json(p) for p in files}
    suspects: list[tuple[Path, str, str]] = []
    for path, payload in payloads.items():
        for source, translated in payload.items():
            if suspicious(source, translated):
                suspects.append((path, source, translated))

    total = sum(len(payload) for payload in payloads.values())
    print(f"Kabyle strict semantic repair scan: {total} shard strings, {len(suspects)} suspect outputs.", flush=True)
    if not suspects:
        return

    translator = GenericKabyle()
    repaired = 0
    for path, source, old in suspects:
        new = translator.structural(source)
        validate_repaired(source, new)
        if new == old:
            raise SystemExit(f"Kabyle semantic fallback made no change for suspect source: {source!r}")
        payloads[path][source] = new
        repaired += 1
        print(f"Repaired Kabyle semantic outlier {repaired}/{len(suspects)}: {source[:90]!r}", flush=True)

    for path, payload in payloads.items():
        write_json(path, payload)

    remaining: list[str] = []
    for payload in payloads.values():
        for source, translated in payload.items():
            sw = words(source)
            tw = words(translated)
            if repetition_collapse(translated) or english_leakage(translated):
                remaining.append(source)
            elif source_english_overlap(source, translated):
                remaining.append(source)
            elif len(sw) >= 4 and sw == tw:
                remaining.append(source)
            elif severe_length_collapse(source, translated):
                remaining.append(source)
            elif malformed_unknown_artifact(translated):
                remaining.append(source)
    if remaining:
        raise SystemExit(f"Kabyle strict semantic repair left {len(remaining)} suspect outputs; samples={remaining[:5]!r}")
    print(f"Kabyle strict semantic repair passed: repaired {repaired} outliers and final shard scan is clean.", flush=True)


if __name__ == "__main__":
    main()
