#!/usr/bin/env python3
"""Refine Kölsch (`ksh`) fallbacks with direct English -> Kölsch MT.

Exact whole-string Minecraft corpus matches win first. Existing clean Kölsch outputs
are reused so reruns only spend inference on unresolved strings. Remaining whole
strings use Helsinki's 2024 TC+Bible West-Germanic model with the explicit `>>ksh<<`
target. No Standard German pivot and no isolated-word projection are used.
This pass rejects obvious semantic failures such as unchanged multi-word English,
English grammar leakage, repetition collapse, and severe truncation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

import bootstrap_kolsch as base

ROOT = base.ROOT
ASSETS = base.ASSETS
MODEL_ID = "Helsinki-NLP/opus-mt-tc-bible-big-deu_eng_fra_por_spa-gmw"
TARGET_TOKEN = ">>ksh<<"
PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b",
    re.IGNORECASE,
)
SUSPICIOUS_UNKNOWN_RE = re.compile(r"(?:^|[\s>+\-•])\?[^\W\d_]", re.MULTILINE | re.UNICODE)
FOREIGN_SCRIPT_RE = re.compile(r"[\u0370-\u052f\u0590-\u08ff\u0900-\u0fff\u3000-\u9fff]")
BAD_DECORATION_RE = re.compile(r"[♫■]|±(?=\s*[A-Za-z])")
WORD_RE = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)?", re.UNICODE)
CLAUSE_SPLIT_RE = re.compile(r"(\s+[—–]\s+|(?<=[.!?])\s+|;\s+)")
TECHNICAL_CASEFOLD = {"neoorigins", "origin architect", "hud", "json", "xp", "hp", "neoforge", "minecraft", "curseforge"}
ENGLISH_SIGNAL_WORDS = {
    "the", "and", "or", "but", "your", "you", "yours", "with", "without",
    "while", "when", "where", "who", "which", "that", "this", "these",
    "those", "into", "through", "from", "for", "of", "other", "still",
    "cannot", "will", "were", "being", "been", "their", "them", "they",
}


def read_json(path: Path) -> dict[str, str]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protected_signature(text: str) -> list[str]:
    out = []
    for token in PROTECT_RE.findall(text):
        out.append(token.casefold() if token.casefold() in TECHNICAL_CASEFOLD else token)
    return out


def semantic_words(text: str) -> list[str]:
    return [word.casefold() for word in WORD_RE.findall(PROTECT_RE.sub(" ", text))]


def sanitize_output(source: str, translated: str) -> str:
    if "§" not in source:
        translated = translated.replace("§", "")
    return translated.strip()


def valid_output(source: str, value: str) -> bool:
    return (
        bool(value.strip())
        and base.placeholder_signature(source) == base.placeholder_signature(value)
        and protected_signature(source) == protected_signature(value)
        and TARGET_TOKEN not in value
        and not SUSPICIOUS_UNKNOWN_RE.search(value)
        and not FOREIGN_SCRIPT_RE.search(value)
        and not BAD_DECORATION_RE.search(value)
    )


def semantic_issue(source: str, value: str) -> str | None:
    sw = semantic_words(source)
    tw = semantic_words(value)
    if len(sw) >= 2 and sw == tw:
        return "unchanged multi-word English"

    if len(tw) >= 8:
        for i in range(len(tw) - 2):
            if tw[i] == tw[i + 1] == tw[i + 2]:
                return "repetition collapse"
        sc = Counter(word for word in sw if len(word) >= 4)
        tc = Counter(word for word in tw if len(word) >= 4)
        if tc:
            _, target_count = tc.most_common(1)[0]
            source_count = sc.most_common(1)[0][1] if sc else 0
            if target_count >= 6 and target_count >= source_count + 5 and target_count / len(tw) >= 0.28:
                return "repetition collapse"

    hits = sum(word in ENGLISH_SIGNAL_WORDS for word in tw)
    if len(tw) >= 5 and hits >= 3 and hits / len(tw) >= 0.16:
        return "English grammar leakage"

    source_signals = [word for word in sw if word in ENGLISH_SIGNAL_WORDS]
    if len(source_signals) >= 4:
        target_words = set(tw)
        overlap = sum(word in target_words for word in source_signals)
        if overlap >= 4 and overlap / len(source_signals) >= 0.50:
            return "large English prose overlap"

    if len(sw) >= 18 and len(tw) <= max(4, int(len(sw) * 0.32)):
        return "severe truncation"
    return None


def build_sources():
    neo_121 = read_json(ROOT / "build/ksh-discovery-mc-1.21.1/ksh_missing_en.json")
    neo_261 = read_json(ROOT / "build/ksh-discovery-mc-26.1/ksh_missing_en.json")
    neo_262 = read_json(ROOT / "build/ksh-discovery-mc-26.2/ksh_missing_en.json")
    common = {k: v for k, v in neo_121.items() if neo_261.get(k) == v and neo_262.get(k) == v}
    delta_121 = {k: v for k, v in neo_121.items() if k not in common}
    delta_261 = {k: v for k, v in neo_261.items() if k not in common}
    delta_262 = {k: v for k, v in neo_262.items() if k not in common}
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
    addons = {ns: read_json(path) for ns, path in source_files.items()}
    shared = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {k: v for k, v in addons["origins_backgrounds_two"].items() if k not in shared}
    addons["origins_backgrounds_iss"] = {k: v for k, v in addons["origins_backgrounds_iss"].items() if k not in shared}
    return common, delta_121, delta_261, delta_262, addons


class KolschTranslator:
    def __init__(self) -> None:
        print(f"Loading direct Kölsch OPUS model: {MODEL_ID} target={TARGET_TOKEN}", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        self.model.eval()

    def translate_batch(self, texts: list[str]) -> list[str]:
        if not texts:
            return []
        encoded = self.tokenizer(
            [f"{TARGET_TOKEN} {text}" for text in texts],
            return_tensors="pt", padding=True, truncation=True, max_length=512,
        )
        with torch.inference_mode():
            generated = self.model.generate(**encoded, num_beams=4, max_new_tokens=512, early_stopping=True)
        return [v.strip() for v in self.tokenizer.batch_decode(generated, skip_special_tokens=True)]

    @staticmethod
    def split_affixes(piece: str) -> tuple[str, str, str]:
        alpha = [i for i, char in enumerate(piece) if char.isalpha()]
        if not alpha:
            return piece, "", ""
        first, last = alpha[0], alpha[-1]
        return piece[:first], piece[first:last + 1], piece[last + 1:]

    def structural_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        out = list(pieces)
        indexes, cores, affixes = [], [], {}
        for i, piece in enumerate(pieces):
            prefix, core, suffix = self.split_affixes(piece)
            if core:
                indexes.append(i)
                cores.append(core)
                affixes[i] = (prefix, suffix)
        outputs = self.translate_batch(cores)
        if len(outputs) != len(indexes):
            raise RuntimeError("Structural Kölsch translation returned the wrong span count")
        for i, output in zip(indexes, outputs):
            prefix, suffix = affixes[i]
            out[i] = prefix + sanitize_output(source, output) + suffix
        result = []
        for i, piece in enumerate(out):
            result.append(piece)
            if i < len(tokens):
                result.append(tokens[i])
        return "".join(result)

    def clause_translate(self, source: str) -> str:
        pieces = PROTECT_RE.split(source)
        tokens = PROTECT_RE.findall(source)
        result: list[str] = []
        for piece_index, piece in enumerate(pieces):
            split = CLAUSE_SPLIT_RE.split(piece)
            clause_indexes = [i for i in range(0, len(split), 2) if any(ch.isalpha() for ch in split[i])]
            cores = [split[i].strip() for i in clause_indexes]
            outputs = self.translate_batch(cores)
            for i, output in zip(clause_indexes, outputs):
                original = split[i]
                prefix = original[:len(original) - len(original.lstrip())]
                suffix = original[len(original.rstrip()):]
                split[i] = prefix + sanitize_output(source, output) + suffix
            result.append("".join(split))
            if piece_index < len(tokens):
                result.append(tokens[piece_index])
        return "".join(result)

    def contextual_title_candidates(self, source: str) -> list[str]:
        """Translate stubborn title-like labels in sentence context, still en->ksh directly."""
        wrappers = [
            f"Power name: {source}",
            f"Ability name: {source}",
            f"Effect name: {source}",
            f"Class name: {source}",
            f"Game title: {source}",
        ]
        outputs = self.translate_batch(wrappers)
        candidates: list[str] = []
        for output in outputs:
            output = output.strip()
            if ":" not in output:
                continue
            candidate = output.rsplit(":", 1)[1].strip()
            candidate = candidate.strip('"“”')
            if candidate.endswith(".") and not source.rstrip().endswith("."):
                candidate = candidate[:-1].rstrip()
            if candidate:
                candidates.append(candidate)

        # Capitalization can make short labels look like proper names to Marian.
        # A lowercase retry often translates the phrase instead of copying it.
        lowered = source.casefold()
        if lowered != source:
            candidates.extend(self.translate_batch([lowered, lowered + "."]))
        return [sanitize_output(source, candidate).rstrip(".") for candidate in candidates]

    def semantic_retry(self, source: str, first: str) -> tuple[str, str | None]:
        candidates = [first]
        candidates.append(sanitize_output(source, self.structural_translate(source)))
        candidates.append(sanitize_output(source, self.clause_translate(source)))

        stripped = source.rstrip()
        if stripped and stripped[-1:] not in ".!?" and len(semantic_words(source)) >= 2:
            punctuated = self.translate_batch([source + "."])[0]
            punctuated = sanitize_output(source, punctuated)
            if punctuated.endswith("."):
                punctuated = punctuated[:-1].rstrip()
            candidates.append(punctuated)
            candidates.extend(self.contextual_title_candidates(source))

        seen: set[str] = set()
        last_issue: str | None = None
        for candidate in candidates:
            if candidate in seen:
                continue
            seen.add(candidate)
            if not valid_output(source, candidate):
                continue
            last_issue = semantic_issue(source, candidate)
            if last_issue is None:
                return candidate, None
        return first, last_issue or semantic_issue(source, first) or "no valid semantic retry"


def build_existing_candidates(
    before: dict[Path, dict[str, str]], payloads: list[dict[str, str]]
) -> dict[str, Counter[str]]:
    """Align current branch translations by key and collect reusable clean values."""
    existing_by_key: dict[str, list[str]] = defaultdict(list)
    for data in before.values():
        for key, value in data.items():
            existing_by_key[key].append(str(value))

    candidates: dict[str, Counter[str]] = defaultdict(Counter)
    for source_payload in payloads:
        for key, source_value in source_payload.items():
            source = str(source_value)
            for value in existing_by_key.get(key, []):
                if valid_output(source, value) and semantic_issue(source, value) is None:
                    candidates[source][value] += 1
    return candidates


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/ksh.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Kölsch files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}
    common_en, d121_en, d261_en, d262_en, addons_en = build_sources()
    payloads = [common_en, d121_en, d261_en, d262_en, *addons_en.values()]
    unique = sorted({str(v) for payload in payloads for v in payload.values()})
    exact = base.build_corpus_map()
    existing = build_existing_candidates(before, payloads)
    translated: dict[str, str] = {}
    direct = []
    reused = 0
    for source in unique:
        if source == "[%s]":
            translated[source] = source
        elif source in base.MANUAL_VALUES:
            translated[source] = base.MANUAL_VALUES[source]
        elif source in exact:
            translated[source] = exact[source]
        elif source in existing and existing[source]:
            translated[source] = existing[source].most_common(1)[0][0]
            reused += 1
        else:
            direct.append(source)
    print(
        f"Kölsch refinement pool: {len(unique)} unique; "
        f"{len(unique)-len(direct)} corpus/manual/preserved/reused; {reused} clean branch values reused; "
        f"{len(direct)} direct OPUS",
        flush=True,
    )

    mt = KolschTranslator()
    semantic_failures: list[tuple[str, str, str]] = []
    semantic_retries = 0
    for start in range(0, len(direct), 16):
        batch = direct[start:start + 16]
        outputs = mt.translate_batch(batch)
        if len(outputs) != len(batch):
            raise SystemExit("Kölsch OPUS batch size mismatch")
        for source, value in zip(batch, outputs):
            value = sanitize_output(source, value)
            if not valid_output(source, value):
                value = sanitize_output(source, mt.structural_translate(source))
            if not valid_output(source, value):
                raise SystemExit(f"Invalid/contaminated Kölsch translation: {source!r} -> {value!r}")
            reason = semantic_issue(source, value)
            if reason:
                semantic_retries += 1
                value, remaining = mt.semantic_retry(source, value)
                if remaining:
                    semantic_failures.append((source, value, remaining))
            translated[source] = value
        done = min(start + len(batch), len(direct))
        if done % 32 == 0 or done == len(direct):
            print(f"Direct Kölsch translation progress: {done}/{len(direct)}", flush=True)

    print(f"Kölsch semantic retries: {semantic_retries}; unresolved: {len(semantic_failures)}", flush=True)
    if semantic_failures:
        for source, value, reason in semantic_failures:
            print(f"UNRESOLVED KÖLSCH [{reason}] {source!r} -> {value!r}", flush=True)
        raise SystemExit(f"Kölsch semantic QA left {len(semantic_failures)} unresolved translations")

    def payload(src):
        return {k: translated[str(v)] for k, v in src.items()}

    common_ksh = payload(common_en)
    for path in ASSETS.glob("neoorigins_ksh_common_*/lang/ksh.json"):
        path.unlink()
    items = list(common_ksh.items())
    for i in range((len(items) + 149) // 150):
        write_json(ASSETS / f"neoorigins_ksh_common_{i+1:02d}/lang/ksh.json", dict(items[i*150:(i+1)*150]))
    write_json(ASSETS / "neoorigins_ksh_121/lang/ksh.json", payload(d121_en))
    write_json(ASSETS / "neoorigins_26_1/lang/ksh.json", payload(d261_en))
    write_json(ASSETS / "neoorigins_26_2/lang/ksh.json", payload(d262_en))
    for namespace, src in addons_en.items():
        write_json(ASSETS / namespace / "lang/ksh.json", payload(src))

    after_files = sorted(ASSETS.glob("**/lang/ksh.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Kölsch files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}
    total = changed = 0
    seen = {}
    final_semantic_failures: list[tuple[str, str, str]] = []
    for path, data in after.items():
        if set(before[path]) != set(data):
            raise SystemExit(f"Kölsch key set changed unexpectedly: {path}")
        for key, value in data.items():
            total += 1
            seen[key] = str(value)
            changed += before[path][key] != value
    source_changed = sum(1 for p in payloads for v in p.values() if translated[str(v)] != str(v))
    for source in unique:
        value = translated[source]
        reason = semantic_issue(source, value)
        if reason:
            final_semantic_failures.append((source, value, reason))
    if final_semantic_failures:
        raise SystemExit(f"Kölsch final semantic QA left {len(final_semantic_failures)} suspect unique values: {final_semantic_failures[:10]!r}")
    text = "\n".join(str(v) for data in after.values() for v in data.values())
    if TARGET_TOKEN in text or SUSPICIOUS_UNKNOWN_RE.search(text) or FOREIGN_SCRIPT_RE.search(text) or BAD_DECORATION_RE.search(text):
        raise SystemExit("Kölsch target marker/artifact/foreign-script contamination survived output")
    if source_changed < 2500:
        raise SystemExit(f"Too many English values survived: only {source_changed} source values changed")
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Origin Architect was not preserved")
    if seen.get("gui.neoorigins.power.key_tag") != "[%s]":
        raise SystemExit("Kölsch placeholder-only key tag changed")
    red = exact.get("Red")
    random = seen.get("button.neoorigins.random")
    if red and random and random.casefold() == red.casefold():
        raise SystemExit(f"Kölsch semantic smoke failed: Random == Red ({random!r})")
    if seen.get("neoorigins.night_vision.on") == seen.get("neoorigins.night_vision.off"):
        raise SystemExit("Kölsch night-vision on/off labels are identical")
    print(
        f"Kölsch refinement passed: {total} values / 29 files; {changed} branch changes; "
        f"{source_changed} source values changed; reused={reused}; semantic retries={semantic_retries}",
        flush=True,
    )


if __name__ == "__main__":
    main()
