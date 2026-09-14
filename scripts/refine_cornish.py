#!/usr/bin/env python3
"""Refine Cornish (`kw_gb`) fallbacks with direct English -> Cornish MT.

Exact whole-string Minecraft corpus matches win first. Remaining complete strings
are translated with Helsinki-NLP/opus-mt-en-cel using the required `>>cor<<`
sentence prefix. No pivot and no isolated-word projection are used.
"""
from __future__ import annotations

from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_cornish as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "Helsinki-NLP/opus-mt-en-cel"
TARGET_TOKEN = ">>cor<<"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)
SUSPICIOUS_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    return PROTECT_RE.findall(text)


def build_sources():
    n121 = read_json(ROOT / "build/kw-discovery-mc-1.21.1/kw_gb_missing_en.json")
    n261 = read_json(ROOT / "build/kw-discovery-mc-26.1/kw_gb_missing_en.json")
    n262 = read_json(ROOT / "build/kw-discovery-mc-26.2/kw_gb_missing_en.json")
    common = {k: v for k, v in n121.items() if n261.get(k) == v and n262.get(k) == v}
    d121 = {k: v for k, v in n121.items() if k not in common}
    d261 = {k: v for k, v in n261.items() if k not in common}
    d262 = {k: v for k, v in n262.items() if k not in common}
    paths = {
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
    addons = {ns: read_json(path) for ns, path in paths.items()}
    shared = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {k: v for k, v in addons["origins_backgrounds_two"].items() if k not in shared}
    addons["origins_backgrounds_iss"] = {k: v for k, v in addons["origins_backgrounds_iss"].items() if k not in shared}
    return common, d121, d261, d262, addons


class Translator:
    def __init__(self):
        print(f"Loading direct Cornish OPUS model: {MODEL_ID} target={TARGET_TOKEN}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()

    def batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        encoded = self.tokenizer(
            [f"{TARGET_TOKEN} {text}" for text in texts],
            return_tensors="pt", padding=True, truncation=True, max_length=512,
        )
        with torch.inference_mode():
            generated = self.model.generate(**encoded, num_beams=4, max_new_tokens=512, early_stopping=True)
        return [x.strip() for x in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    @staticmethod
    def affixes(piece: str):
        alpha = [i for i, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        first, last = alpha[0], alpha[-1]
        return piece[:first], piece[first:last + 1], piece[last + 1:]

    def structural(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        out = list(pieces)
        indexes, cores, affix = [], [], {}
        for i, piece in enumerate(pieces):
            prefix, core, suffix = self.affixes(piece)
            if core:
                indexes.append(i); cores.append(core); affix[i] = (prefix, suffix)
        translated = self.batch(cores)
        if len(translated) != len(indexes):
            raise RuntimeError("Cornish structural translation span mismatch")
        for i, value in zip(indexes, translated):
            prefix, suffix = affix[i]
            out[i] = prefix + value.strip() + suffix
        result = []
        for i, piece in enumerate(out):
            result.append(piece)
            if i < len(tokens): result.append(tokens[i])
        return "".join(result)


def main():
    before_files = sorted(ASSETS.glob("**/lang/kw_gb.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Cornish files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}
    common, d121, d261, d262, addons = build_sources()
    payloads = [common, d121, d261, d262, *addons.values()]
    unique = sorted({str(v) for p in payloads for v in p.values()})
    exact = base.build_corpus_map()
    translated: dict[str, str] = {}
    direct = []
    for source in unique:
        if source in base.MANUAL_VALUES: translated[source] = base.MANUAL_VALUES[source]
        elif source in exact: translated[source] = exact[source]
        else: direct.append(source)
    print(f"Cornish refinement pool: {len(unique)} unique; {len(unique)-len(direct)} corpus/manual; {len(direct)} direct OPUS", flush=True)

    mt = Translator()
    for start in range(0, len(direct), 16):
        batch = direct[start:start+16]
        outputs = mt.batch(batch)
        if len(outputs) != len(batch): raise SystemExit("Cornish OPUS batch size mismatch")
        for source, value in zip(batch, outputs):
            ok = bool(value.strip())
            ok &= base.placeholder_signature(source) == base.placeholder_signature(value)
            ok &= protected_signature(source) == protected_signature(value)
            if not ok: value = mt.structural(source)
            if not value.strip(): raise SystemExit(f"Empty Cornish translation for {source!r}")
            if base.placeholder_signature(source) != base.placeholder_signature(value): raise SystemExit(f"Cornish placeholder mismatch: {source!r} -> {value!r}")
            if protected_signature(source) != protected_signature(value): raise SystemExit(f"Cornish protected-token mismatch: {source!r} -> {value!r}")
            if SUSPICIOUS_RE.search(value): raise SystemExit(f"Suspicious Cornish output: {source!r} -> {value!r}")
            translated[source] = value
        done = min(start+len(batch), len(direct))
        if done % 160 == 0 or done == len(direct): print(f"Direct Cornish translation progress: {done}/{len(direct)}", flush=True)

    def payload(src): return {k: translated[str(v)] for k, v in src.items()}
    common_kw = payload(common)
    for path in ASSETS.glob("neoorigins_kw_common_*/lang/kw_gb.json"): path.unlink()
    items = list(common_kw.items())
    for i in range((len(items)+149)//150):
        write_json(ASSETS / f"neoorigins_kw_common_{i+1:02d}/lang/kw_gb.json", dict(items[i*150:(i+1)*150]))
    write_json(ASSETS / "neoorigins_kw_121/lang/kw_gb.json", payload(d121))
    write_json(ASSETS / "neoorigins_26_1/lang/kw_gb.json", payload(d261))
    write_json(ASSETS / "neoorigins_26_2/lang/kw_gb.json", payload(d262))
    for ns, src in addons.items(): write_json(ASSETS / ns / "lang/kw_gb.json", payload(src))

    after_files = sorted(ASSETS.glob("**/lang/kw_gb.json"))
    if len(after_files) != 29: raise SystemExit(f"Expected 29 Cornish files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}
    changed = total = 0; seen = {}
    for path, data in after.items():
        if set(before[path]) != set(data): raise SystemExit(f"Cornish key set changed unexpectedly: {path}")
        for key, value in data.items():
            total += 1; seen[key] = str(value); changed += before[path][key] != value
    source_changed = sum(1 for p in payloads for v in p.values() if translated[str(v)] != str(v))
    text = "\n".join(str(v) for data in after.values() for v in data.values())
    if TARGET_TOKEN in text or SUSPICIOUS_RE.search(text): raise SystemExit("Cornish target marker/artifact survived output")
    if source_changed < 2500: raise SystemExit(f"Too many English values survived Cornish MT: {source_changed} changed")
    if seen.get("key.categories.originsmodernui") != "Origin Architect": raise SystemExit("Origin Architect was not preserved")
    red = exact.get("Red"); random = seen.get("button.neoorigins.random")
    if red and random and red.casefold() == random.casefold(): raise SystemExit(f"Cornish semantic smoke failed: Random == Red ({random!r})")
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"): raise SystemExit("Cornish night-vision on/off labels are identical")
    print(f"Cornish refinement passed: {total} values / 29 files; {changed} bootstrap changes; {source_changed} source values changed", flush=True)


if __name__ == "__main__":
    main()
