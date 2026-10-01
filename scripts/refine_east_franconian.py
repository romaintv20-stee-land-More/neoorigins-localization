#!/usr/bin/env python3
"""Safely refine the generated East Franconian (`fra_de`) fallback locale.

The bootstrap deliberately maximizes dialect coverage. This pass regenerates every
`fra_de` value from the complete German semantic source with stricter corpus learning:
exact Minecraft de_de -> fra_de strings remain usable, but free word substitutions need
strong repeated evidence before they may be projected into NeoOrigins text.

This is deterministic/generative assistance, not native-speaker review.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import json
import re

import bootstrap_east_franconian as base

ROOT = base.ROOT
ASSETS = base.ASSETS

# Common, high-confidence East Franconian forms. Keep this list deliberately small:
# contextual German remains preferable to an uncertain dialect substitution.
MANUAL_WORDS = {
    "nicht": "ned",
    "sind": "san",
    "nur": "nua",
    "von": "vo",
    "server": "seava",
    "befehl": "bfehl",
    "monster": "monsda",
    "mit": "mid",
    "oder": "oda",
    "ist": "is",
    "wird": "wiad",
    "wasser": "wassa",
    "feuer": "feua",
    "welt": "weld",
    "zurück": "zurügg",
}

# Exact one-label values that should stay clear and stable rather than inherit an
# unrelated Minecraft UI spelling through the exact-string corpus map.
PRESERVE_VALUES = {
    "Phantom",
    "Standard",
    "Schließen",
    "Bearbeiten",
    "Speichern",
    "Zurück",
}

# High-visibility labels where clarity is more important than speculative phonetic
# projection. These remain German-compatible and avoid obvious bootstrap artefacts.
KEY_OVERRIDES = {
    "origins.neoorigins.human.name": "Mensch",
    "origins.neoorigins.phantom.name": "Phantom",
    "neoorigins.night_vision.on": "Nachtsicht an",
    "gui.neoorigins.button.back": "< Zurück",
    "gui.neoorigins.sort.manual": "Standard",
    "gui.neoorigins.info.close": "Schließen",
    "gui.neoorigins.info.edit": "Bearbeiten",
    "gui.neoorigins.editor.on": "An",
    "gui.neoorigins.creator.save": "Speichern",
    "gui.neoorigins.mob_creator.save": "Speichern",
}

FORBIDDEN_PATTERNS = (
    re.compile(r"\bteleboadiead\b", re.I),
    re.compile(r"\bphandom\b", re.I),
    re.compile(r"\bschdandard\b", re.I),
    re.compile(r"\bschlieaßa\b", re.I),
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_safe_corpus_maps():
    german = base.fetch_json(f"{base.MC_LOCALES_BASE}/de_de.json")
    franconian = base.fetch_json(f"{base.MC_LOCALES_BASE}/fra_de.json")
    english = base.fetch_json(f"{base.MC_LOCALES_BASE}/en_us.json")
    shared = sorted(set(german) & set(franconian))

    exact: dict[str, str] = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    unchanged = 0
    isolated = 0

    for key in shared:
        source = str(german[key])
        target = str(franconian[key])
        en_value = str(english[key]) if key in english else None
        if not base.safe_pair(source, target, en_value):
            rejected += 1
            continue
        if source == target:
            unchanged += 1
            continue

        # Exact source strings are safe because no context-free word projection occurs.
        exact[source] = target

        for src, dst in base.isolated_word_replacements(source, target):
            if SequenceMatcher(None, src, dst).ratio() < 0.50:
                continue
            votes[src][dst] += 1
            isolated += 1

    learned: dict[str, str] = {}
    for source, counter in votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        share = top / total
        # Considerably stricter than bootstrap. A mapping must be both recurrent and
        # dominant; one-off phonetic spellings do not propagate to unrelated mod text.
        if (top >= 3 and share >= 0.90) or (top >= 8 and share >= 0.75):
            learned[source] = target

    learned.update(MANUAL_WORDS)

    destructive = {
        source: target
        for source, target in learned.items()
        if len(source) >= 5 and (len(target) <= 1 or SequenceMatcher(None, source, target).ratio() < 0.25)
    }
    if destructive:
        raise RuntimeError(f"Destructive East Franconian mappings detected: {destructive}")

    for source, target in learned.items():
        if target.casefold() in {"teleboadiead", "phandom", "schdandard", "schlieaßa"}:
            raise RuntimeError(f"Known bad East Franconian mapping survived learner: {source!r} -> {target!r}")

    print(
        f"Safe East Franconian corpus: {len(shared)} aligned entries, {rejected} rejected pairs, "
        f"{unchanged} unchanged, {len(exact)} exact strings, {isolated} isolated candidates, "
        f"{len(learned)} accepted word mappings"
    )
    return exact, learned


def dialectize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
    if text in PRESERVE_VALUES:
        return text
    if text in base.MANUAL_VALUES:
        return base.MANUAL_VALUES[text]
    if text in exact:
        result = exact[text]
        if base.placeholder_signature(text) != base.placeholder_signature(result):
            raise RuntimeError(f"Exact-map placeholder mismatch: {text!r} -> {result!r}")
        return result

    masked, tokens = base.protect(text)

    def replace_word(match):
        word = match.group(0)
        mapped = learned.get(word.casefold())
        return base.preserve_case(word, mapped) if mapped is not None else word

    result = base.WORD_RE.sub(replace_word, masked)
    result = base.restore(result, tokens)
    if base.placeholder_signature(text) != base.placeholder_signature(result):
        raise RuntimeError(f"East Franconian placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_german() -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in sorted(ASSETS.glob("**/lang/de_de.json")):
        for key, value in read_json(path).items():
            merged.setdefault(key, str(value))
    print(f"Local German fallback pool: {len(merged)} distinct keys")
    return merged


def build_neoorigins_sources(local_german: dict[str, str]):
    result = {}
    for label, ref in base.NEO_REFS.items():
        official = base.fetch_optional_json(base.NEO_BASE.format(ref=ref, locale="de_de"))
        merged = dict(official)
        for key, value in local_german.items():
            merged.setdefault(key, value)
        result[label] = {key: str(value) for key, value in merged.items()}
        print(f"German semantic source {label}: official={len(official)}, merged={len(merged)}")
    return result


def german_value_for(path: Path, key: str, neo_sources: dict[str, dict], local_german: dict[str, str]):
    namespace = path.parents[1].name
    if namespace == "neoorigins_26_1":
        source = neo_sources["mc-26.1"]
    elif namespace == "neoorigins_26_2":
        source = neo_sources["mc-26.2"]
    elif namespace.startswith("neoorigins_fra_"):
        source = neo_sources["mc-1.21.1"]
    else:
        direct = ASSETS / namespace / "lang/de_de.json"
        if direct.exists():
            direct_data = read_json(direct)
            if key in direct_data:
                return str(direct_data[key])
        source = local_german

    if key not in source:
        raise KeyError(f"Missing German semantic source for {namespace}:{key}")
    return str(source[key])


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/fra_de.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 East Franconian files, found {len(files)}")

    local_german = collect_local_german()
    neo_sources = build_neoorigins_sources(local_german)
    exact, learned = build_safe_corpus_maps()

    changed_values = 0
    total_values = 0
    for path in files:
        old_data = read_json(path)
        new_data = {}
        for key in old_data:
            source = german_value_for(path, key, neo_sources, local_german)
            target = KEY_OVERRIDES.get(key, dialectize(source, exact, learned))
            if base.placeholder_signature(source) != base.placeholder_signature(target):
                raise RuntimeError(f"Placeholder mismatch after override for {key}: {source!r} -> {target!r}")
            new_data[key] = target
            total_values += 1
            if str(old_data[key]) != target:
                changed_values += 1
        write_json(path, new_data)

    rows = []
    for path in files:
        data = read_json(path)
        rows.extend((path, key, str(value)) for key, value in data.items())

    bad = []
    for path, key, value in rows:
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(value):
                bad.append((str(path), key, value, pattern.pattern))
                break
    if bad:
        raise SystemExit(f"Known unsafe East Franconian patterns survived refinement: {bad[:20]}")

    text = "\n".join(value for _, _, value in rows)
    marker_count = len(base.DIALECT_MARKER_RE.findall(text))
    if marker_count < 120:
        raise SystemExit(f"East Franconian dialect marker sanity too low after refinement: {marker_count}")

    probes = {key: value for _, key, value in rows}
    expected = {
        "origins.neoorigins.human.name": "Mensch",
        "origins.neoorigins.phantom.name": "Phantom",
        "gui.neoorigins.sort.manual": "Standard",
        "gui.neoorigins.info.close": "Schließen",
        "gui.neoorigins.info.edit": "Bearbeiten",
        "gui.neoorigins.creator.save": "Speichern",
    }
    for key, value in expected.items():
        if probes.get(key) != value:
            raise SystemExit(f"High-visibility QA failed for {key}: {probes.get(key)!r}")

    print(
        f"East Franconian safe refinement passed: regenerated {total_values} values across {len(files)} files; "
        f"{changed_values} values changed from bootstrap; {marker_count} dialect markers; "
        "0 known unsafe projection patterns."
    )


if __name__ == "__main__":
    main()
