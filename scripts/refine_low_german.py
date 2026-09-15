#!/usr/bin/env python3
"""Refine Low German (`nds_de`) with direct English -> Low German OPUS.

Uses the Germanic-target OPUS model with an explicit `>>nds<<` target. Multi-
sentence strings are translated sentence by sentence to prevent semantic
truncation. This is automated translation assistance, not native review.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_low_german as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "Helsinki-NLP/opus-mt-tc-base-gmw-gmw"
TARGET_TOKEN = ">>nds<<"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",
    re.IGNORECASE,
)
SUSPICIOUS_RE = re.compile(r"(?:^|[\s>+\-•])\?[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]", re.MULTILINE)
FOREIGN_SCRIPT_RE = re.compile(r"[\u0370-\u052f\u0600-\u06ff\u0900-\u0dff\u3040-\u30ff\u3400-\u9fff]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿĀ-žƀ-ɏ]+)?")
TECHNICAL_CASEFOLD = {
    "neoorigins", "origin architect", "hud", "json", "xp", "hp",
    "neoforge", "minecraft", "curseforge",
}


def rj(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def wj(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ps(text):
    return [
        token.casefold() if token.casefold() in TECHNICAL_CASEFOLD else token
        for token in PROTECT_RE.findall(text)
    ]


def sanitize(source, value):
    if not base.placeholder_signature(source):
        value = base.PLACEHOLDER_RE.sub("", value)
    if "§" not in source:
        value = value.replace("§", "")
    return re.sub(r"[ \t]{2,}", " ", value).strip()


def pathological_repetition(source: str, value: str) -> bool:
    words = [w.casefold() for w in WORD_RE.findall(value)]
    if len(words) < 10:
        return False
    counts = Counter(words)
    token, count = counts.most_common(1)[0]
    source_count = Counter(w.casefold() for w in WORD_RE.findall(source)).get(token, 0)
    return count >= max(6, (len(words) + 2) // 3) and source_count < 3


def sources():
    a = rj(ROOT / "build/nds-discovery-mc-1.21.1/nds_de_missing_en.json")
    b = rj(ROOT / "build/nds-discovery-mc-26.1/nds_de_missing_en.json")
    c = rj(ROOT / "build/nds-discovery-mc-26.2/nds_de_missing_en.json")
    common = {k: v for k, v in a.items() if b.get(k) == v and c.get(k) == v}
    d1 = {k: v for k, v in a.items() if k not in common}
    d2 = {k: v for k, v in b.items() if k not in common}
    d3 = {k: v for k, v in c.items() if k not in common}
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
    addons = {name: rj(ROOT / f"build/{folder}/upstream_en_us.json") for name, folder in folders.items()}
    shared = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {k: v for k, v in addons["origins_backgrounds_two"].items() if k not in shared}
    addons["origins_backgrounds_iss"] = {k: v for k, v in addons["origins_backgrounds_iss"].items() if k not in shared}
    return common, d1, d2, d3, addons


class MT:
    def __init__(self):
        self.t = AutoTokenizer.from_pretrained(MODEL_ID)
        self.m = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.m.eval()
        print(f"Low German direct model: {MODEL_ID}; target={TARGET_TOKEN}", flush=True)

    def batch(self, texts):
        if not texts:
            return []
        encoded = self.t(
            [f"{TARGET_TOKEN} {source}" for source in texts],
            return_tensors="pt", padding=True, truncation=True, max_length=512,
        )
        with torch.inference_mode():
            generated = self.m.generate(
                **encoded, num_beams=4, max_new_tokens=512, early_stopping=True
            )
        return [value.strip() for value in self.t.batch_decode(generated, skip_special_tokens=True)]

    def structural(self, source):
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        out = list(pieces)
        indices, cores, affixes = [], [], {}
        for index, piece in enumerate(pieces):
            alpha = [i for i, char in enumerate(piece) if char.isalpha()]
            if alpha:
                prefix, core, suffix = piece[:alpha[0]], piece[alpha[0]:alpha[-1] + 1], piece[alpha[-1] + 1:]
                indices.append(index); cores.append(core); affixes[index] = (prefix, suffix)
        values = self.batch(cores)
        for index, core, value in zip(indices, cores, values):
            prefix, suffix = affixes[index]
            out[index] = prefix + sanitize(core, value) + suffix
        result = []
        for index, piece in enumerate(out):
            result.append(piece)
            if index < len(tokens):
                result.append(tokens[index])
        return "".join(result)

    def sentence_complete(self, source: str) -> str:
        # Preserve separators exactly while translating each complete sentence independently.
        matches = list(re.finditer(r"(?<=[.!?])\s+", source))
        if not matches:
            return self.batch([source])[0]
        result = []
        cursor = 0
        for match in matches:
            piece = source[cursor:match.start()]
            result.append(self.batch([piece])[0] if piece.strip() else piece)
            result.append(match.group(0))
            cursor = match.end()
        tail = source[cursor:]
        result.append(self.batch([tail])[0] if tail.strip() else tail)
        return "".join(result)


def safe_pair(source: str, value: str) -> bool:
    return (
        bool(value.strip())
        and base.placeholder_signature(source) == base.placeholder_signature(value)
        and ps(source) == ps(value)
        and not SUSPICIOUS_RE.search(value)
        and not FOREIGN_SCRIPT_RE.search(value)
        and TARGET_TOKEN not in value
        and not pathological_repetition(source, value)
    )


def main():
    before_files = sorted(ASSETS.glob("**/lang/nds_de.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Low German files, found {len(before_files)}")
    before = {p: rj(p) for p in before_files}
    common, d1, d2, d3, addons = sources()
    payloads = [common, d1, d2, d3, *addons.values()]
    unique = sorted({str(v) for payload in payloads for v in payload.values()})
    exact = base.build_corpus_map()
    translated, direct = {}, []
    for source in unique:
        if source == "[%s]":
            translated[source] = source
        elif source in base.MANUAL_VALUES:
            translated[source] = base.MANUAL_VALUES[source]
        elif source in exact:
            translated[source] = exact[source]
        else:
            direct.append(source)

    print(
        f"Low German pool: {len(unique)} unique; {len(unique) - len(direct)} corpus/manual/preserved; "
        f"{len(direct)} direct OPUS", flush=True
    )
    mt = MT()
    batch_size = 24
    for start in range(0, len(direct), batch_size):
        batch = direct[start:start + batch_size]
        # Multi-sentence strings are translated independently to prevent dropped clauses.
        singles = [s for s in batch if len(re.findall(r"[.!?](?=\s|$)", s)) < 2]
        singles_values = dict(zip(singles, mt.batch(singles)))
        for source in batch:
            value = mt.sentence_complete(source) if source not in singles_values else singles_values[source]
            value = sanitize(source, value)
            if not safe_pair(source, value):
                value = sanitize(source, mt.structural(source))
            if not safe_pair(source, value):
                raise SystemExit(f"Unsafe Low German translation: {source!r}->{value!r}")
            translated[source] = value
        done = min(start + len(batch), len(direct))
        if done % 240 == 0 or done == len(direct):
            print(f"Direct Low German progress: {done}/{len(direct)}", flush=True)

    def payload(source_map):
        return {key: translated[str(value)] for key, value in source_map.items()}

    items = list(payload(common).items())
    for path in ASSETS.glob("neoorigins_nds_common_*/lang/nds_de.json"):
        path.unlink()
    for index in range((len(items) + 149) // 150):
        wj(ASSETS / f"neoorigins_nds_common_{index + 1:02d}/lang/nds_de.json", dict(items[index * 150:(index + 1) * 150]))
    wj(ASSETS / "neoorigins_nds_121/lang/nds_de.json", payload(d1))
    wj(ASSETS / "neoorigins_26_1/lang/nds_de.json", payload(d2))
    wj(ASSETS / "neoorigins_26_2/lang/nds_de.json", payload(d3))
    for namespace, source_map in addons.items():
        wj(ASSETS / namespace / "lang/nds_de.json", payload(source_map))

    after = {p: rj(p) for p in sorted(ASSETS.glob("**/lang/nds_de.json"))}
    seen, changed, total = {}, 0, 0
    for path, data in after.items():
        if set(before[path]) != set(data):
            raise SystemExit(f"Low German key set changed: {path}")
        for key, value in data.items():
            total += 1; seen[key] = str(value); changed += before[path][key] != value
    changed_src = sum(1 for payload_map in payloads for value in payload_map.values() if translated[str(value)] != str(value))
    text = "\n".join(str(value) for data in after.values() for value in data.values())
    if TARGET_TOKEN in text or FOREIGN_SCRIPT_RE.search(text) or changed_src < 2500:
        raise SystemExit("Low German final gate failed")
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Origin Architect changed")
    if seen.get("gui.neoorigins.power.key_tag") != "[%s]":
        raise SystemExit("Low German placeholder-only key tag changed")
    red = exact.get("Red"); random = seen.get("button.neoorigins.random")
    if red and random and red.casefold() == random.casefold():
        raise SystemExit("Random translated as Red")
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"):
        raise SystemExit("Night vision labels identical")
    print(
        f"Low German dedicated OPUS refinement passed: {total} values; {changed} bootstrap changes; "
        f"{changed_src} sources changed", flush=True
    )


if __name__ == "__main__":
    main()
