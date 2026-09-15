#!/usr/bin/env python3
"""Strict semantic QA + targeted 1.3B repair for Limburgish (`li_li`).

Keeps existing branch translations when they pass semantic/structural checks and only
retranslates suspicious values. English remains the direct source; no language pivot
or isolated-word projection is used.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re
import unicodedata

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_limburgish as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "facebook/nllb-200-distilled-1.3B"
SOURCE_LANG = "eng_Latn"
TARGET_LANG = "lim_Latn"

PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)
SUSPICIOUS_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)
WORD_RE = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?", re.UNICODE)
ENGLISH_LEAK = {
    "the", "you", "your", "yours", "when", "while", "with", "without", "from", "into",
    "will", "would", "should", "could", "this", "that", "these", "those", "their", "they",
    "them", "grants", "allows", "increases", "reduces", "deals", "gain", "gains", "nearby",
    "becomes", "become", "using", "used", "instead", "also", "only", "every", "each",
}
ALLOWED_UNCHANGED = set(base.MANUAL_VALUES) | {
    "NeoOrigins", "Minecraft", "NeoForge", "CurseForge", "HUD", "JSON", "XP", "HP",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def words(text: str) -> list[str]:
    return [unicodedata.normalize("NFC", w).casefold() for w in WORD_RE.findall(text)]


def protected_signature(text: str):
    return PROTECT_RE.findall(text)


def sanitize(source: str, value: str) -> str:
    value = value.replace("<unk>", "").strip()
    if not base.placeholder_signature(source):
        value = base.PLACEHOLDER_RE.sub("", value)
    if "§" not in source:
        value = value.replace("§", "")
    return re.sub(r"[ \t]{2,}", " ", value).strip()


def excessive_repetition(source: str, target: str) -> bool:
    sw, tw = words(source), words(target)
    if len(tw) < 4:
        return False
    sc, tc = Counter(sw), Counter(tw)
    for word, count in tc.items():
        if count >= 3 and count >= sc.get(word, 0) + 2:
            return True
    for size in (2, 3):
        if len(tw) >= size * 2:
            for i in range(len(tw) - size * 2 + 1):
                if tw[i:i+size] == tw[i+size:i+size*2]:
                    return True
    return False


def semantic_reasons(source: str, target: str) -> list[str]:
    reasons = []
    source = str(source).strip()
    target = str(target).strip()
    sw, tw = words(source), words(target)

    if not target:
        reasons.append("empty")
        return reasons
    if base.placeholder_signature(source) != base.placeholder_signature(target):
        reasons.append("placeholder")
    if protected_signature(source) != protected_signature(target):
        reasons.append("protected-token")
    if TARGET_LANG in target or "<unk>" in target:
        reasons.append("model-marker")
    if SUSPICIOUS_RE.search(target):
        reasons.append("artifact")

    if source not in ALLOWED_UNCHANGED and len(sw) >= 2 and source.casefold() == target.casefold():
        reasons.append("unchanged-english")

    # Catch English prose leaking through while avoiding short names/technical labels.
    if len(sw) >= 5 and len(tw) >= 4:
        leak = [w for w in tw if w in ENGLISH_LEAK]
        source_leak = {w for w in sw if w in ENGLISH_LEAK}
        if len(leak) >= 2 and len(set(leak) & source_leak) >= 2:
            reasons.append("english-grammar-leak")

    if excessive_repetition(source, target):
        reasons.append("repetition")

    # Limburgish and English are both compact Germanic languages: only flag severe loss.
    if len(sw) >= 9 and (len(tw) < max(3, int(len(sw) * 0.38)) or len(target) < len(source) * 0.30):
        reasons.append("severe-truncation")

    return reasons


def build_sources():
    n121 = read_json(ROOT / "build/li-discovery-mc-1.21.1/li_li_missing_en.json")
    n261 = read_json(ROOT / "build/li-discovery-mc-26.1/li_li_missing_en.json")
    n262 = read_json(ROOT / "build/li-discovery-mc-26.2/li_li_missing_en.json")
    common = {k: v for k, v in n121.items() if n261.get(k) == v and n262.get(k) == v}
    d121 = {k: v for k, v in n121.items() if k not in common}
    d261 = {k: v for k, v in n261.items() if k not in common}
    d262 = {k: v for k, v in n262.items() if k not in common}

    folders = {
        "medievalorigins": "medievalorigins-upstream-audit",
        "ibarnorigins": "ibarnorigins-upstream-audit",
        "origins_fantasy": "origins-fantasy-upstream-audit",
        "origins_backgrounds": "origins-backgrounds-upstream-audit",
        "origins_backgrounds_two": "origins-more-backgrounds-upstream-audit",
        "origins_backgrounds_iss": "origins-backgrounds-iss-upstream-audit",
        "origins_furries": "origins-furries-upstream-audit",
        "origins_classes_ex": "origins-classes-extended-upstream-audit",
        "origins_classes_iss": "origins-classes-iss-upstream-audit",
        "originsmodernui": "origin-architect-upstream-audit",
    }
    addons = {ns: read_json(ROOT / f"build/{folder}/upstream_en_us.json") for ns, folder in folders.items()}
    shared = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {k: v for k, v in addons["origins_backgrounds_two"].items() if k not in shared}
    addons["origins_backgrounds_iss"] = {k: v for k, v in addons["origins_backgrounds_iss"].items() if k not in shared}
    return common, d121, d261, d262, addons


def current_targets(common, d121, d261, d262, addons):
    merged_common = {}
    common_paths = sorted(ASSETS.glob("neoorigins_li_common_*/lang/li_li.json"))
    if len(common_paths) != 16:
        raise SystemExit(f"Expected 16 Limburgish common shards, found {len(common_paths)}")
    for path in common_paths:
        merged_common.update(read_json(path))

    locations = [
        ("common", common, merged_common, common_paths),
        ("1.21.1", d121, read_json(ASSETS / "neoorigins_li_121/lang/li_li.json"), [ASSETS / "neoorigins_li_121/lang/li_li.json"]),
        ("26.1", d261, read_json(ASSETS / "neoorigins_26_1/lang/li_li.json"), [ASSETS / "neoorigins_26_1/lang/li_li.json"]),
        ("26.2", d262, read_json(ASSETS / "neoorigins_26_2/lang/li_li.json"), [ASSETS / "neoorigins_26_2/lang/li_li.json"]),
    ]
    for ns, source in addons.items():
        path = ASSETS / ns / "lang/li_li.json"
        locations.append((ns, source, read_json(path), [path]))
    return locations


class Translator:
    def __init__(self):
        print(f"Loading semantic repair model {MODEL_ID}: {SOURCE_LANG}->{TARGET_LANG}", flush=True)
        self.tok = AutoTokenizer.from_pretrained(MODEL_ID, src_lang=SOURCE_LANG)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()
        self.target_id = self.tok.convert_tokens_to_ids(TARGET_LANG)
        if self.target_id is None or self.target_id == self.tok.unk_token_id:
            raise RuntimeError(f"Missing NLLB target {TARGET_LANG}")

    def batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        enc = self.tok(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.inference_mode():
            gen = self.model.generate(
                **enc,
                forced_bos_token_id=self.target_id,
                num_beams=3,
                max_new_tokens=512,
                early_stopping=True,
            )
        return [x.strip() for x in self.tok.batch_decode(gen, skip_special_tokens=True)]

    @staticmethod
    def affixes(piece: str):
        alpha = [i for i, c in enumerate(piece) if c.isalpha()]
        if not alpha:
            return piece, "", ""
        a, b = alpha[0], alpha[-1]
        return piece[:a], piece[a:b+1], piece[b+1:]

    def structural(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        out = list(pieces)
        indexes, cores, aff = [], [], {}
        for i, piece in enumerate(pieces):
            pre, core, suf = self.affixes(piece)
            if core:
                indexes.append(i)
                cores.append(core)
                aff[i] = (pre, suf)
        vals = self.batch(cores)
        for i, core, val in zip(indexes, cores, vals):
            pre, suf = aff[i]
            out[i] = pre + sanitize(core, val) + suf
        result = []
        for i, piece in enumerate(out):
            result.append(piece)
            if i < len(tokens):
                result.append(tokens[i])
        return "".join(result)

    def candidates(self, source: str) -> list[str]:
        prompts = [source]
        if not source.endswith(('.', '!', '?')):
            prompts.append(source + ".")
        if 2 <= len(words(source)) <= 6:
            prompts.extend([
                f"Ability name: {source}",
                f"Effect name: {source}",
                f"Class name: {source}",
            ])
        raw = self.batch(prompts)
        candidates = []
        for prompt, value in zip(prompts, raw):
            value = sanitize(source, value)
            if prompt != source and prompt.endswith(".") and not source.endswith(".") and value.endswith("."):
                value = value[:-1].rstrip()
            if ":" in prompt and ":" in value:
                value = value.split(":", 1)[1].strip()
            candidates.append(value)
        candidates.append(sanitize(source, self.structural(source)))
        # Preserve order while removing duplicates.
        return list(dict.fromkeys(candidates))


def main():
    files = sorted(ASSETS.glob("**/lang/li_li.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Limburgish files, found {len(files)}")

    common, d121, d261, d262, addons = build_sources()
    locations = current_targets(common, d121, d261, d262, addons)

    suspects = []
    total = 0
    for label, source_payload, target_payload, _paths in locations:
        if set(source_payload) != set(target_payload):
            missing = sorted(set(source_payload) - set(target_payload))[:5]
            extra = sorted(set(target_payload) - set(source_payload))[:5]
            raise SystemExit(f"Key mismatch in {label}: missing={missing}, extra={extra}")
        for key, source in source_payload.items():
            total += 1
            target = str(target_payload[key])
            reasons = semantic_reasons(str(source), target)
            if reasons:
                suspects.append((label, key, str(source), target, reasons))

    print(f"Limburgish semantic scan: {total} values; {len(suspects)} suspects", flush=True)
    for label, key, source, target, reasons in suspects[:30]:
        print(f"SUSPECT [{label}] {key}: {reasons} :: {source!r} -> {target!r}", flush=True)

    if not suspects:
        print("Limburgish semantic repair: nothing to change", flush=True)
        return

    mt = Translator()
    unresolved = []
    repairs: dict[tuple[str, str], str] = {}
    unique_sources = list(dict.fromkeys(source for _, _, source, _, _ in suspects))
    cache = {}
    for index, source in enumerate(unique_sources, 1):
        chosen = None
        candidate_notes = []
        for candidate in mt.candidates(source):
            reasons = semantic_reasons(source, candidate)
            candidate_notes.append((candidate, reasons))
            if not reasons:
                chosen = candidate
                break
        if chosen is None:
            unresolved.append((source, candidate_notes))
        else:
            cache[source] = chosen
        if index % 25 == 0 or index == len(unique_sources):
            print(f"Limburgish semantic repair progress: {index}/{len(unique_sources)}", flush=True)

    if unresolved:
        print(f"UNRESOLVED LIMBURGISH: {len(unresolved)}", flush=True)
        for source, notes in unresolved:
            rendered = " | ".join(f"{candidate!r} => {reasons}" for candidate, reasons in notes)
            print(f"UNRESOLVED LIMBURGISH {source!r}: {rendered}", flush=True)
        raise SystemExit(f"Limburgish semantic QA still has {len(unresolved)} unresolved source strings")

    changed = 0
    for label, key, source, old_target, _reasons in suspects:
        new_target = cache[source]
        if new_target != old_target:
            repairs[(label, key)] = new_target
            changed += 1

    # Write repaired values back to their original fallback files.
    common_target = {}
    common_paths = sorted(ASSETS.glob("neoorigins_li_common_*/lang/li_li.json"))
    for path in common_paths:
        common_target.update(read_json(path))
    for (label, key), value in repairs.items():
        if label == "common":
            common_target[key] = value
        elif label == "1.21.1":
            path = ASSETS / "neoorigins_li_121/lang/li_li.json"
            data = read_json(path); data[key] = value; write_json(path, data)
        elif label == "26.1":
            path = ASSETS / "neoorigins_26_1/lang/li_li.json"
            data = read_json(path); data[key] = value; write_json(path, data)
        elif label == "26.2":
            path = ASSETS / "neoorigins_26_2/lang/li_li.json"
            data = read_json(path); data[key] = value; write_json(path, data)
        else:
            path = ASSETS / label / "lang/li_li.json"
            data = read_json(path); data[key] = value; write_json(path, data)

    if any(label == "common" for label, _key in repairs):
        items = list(common_target.items())
        for i, path in enumerate(common_paths):
            write_json(path, dict(items[i*150:(i+1)*150]))

    # Re-scan after writes; no suspect may survive.
    common, d121, d261, d262, addons = build_sources()
    remaining = []
    for label, source_payload, target_payload, _paths in current_targets(common, d121, d261, d262, addons):
        for key, source in source_payload.items():
            target = str(target_payload[key])
            reasons = semantic_reasons(str(source), target)
            if reasons:
                remaining.append((label, key, source, target, reasons))
    if remaining:
        for item in remaining[:20]:
            print(f"POST-REPAIR SUSPECT: {item}", flush=True)
        raise SystemExit(f"Post-repair Limburgish semantic QA failed for {len(remaining)} values")

    print(f"Limburgish semantic repair passed: {total} values; {len(suspects)} suspects; {changed} changed", flush=True)


if __name__ == "__main__":
    main()
