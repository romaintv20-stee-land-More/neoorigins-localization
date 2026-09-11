#!/usr/bin/env python3
"""Safely refine the generated Andalusian (`esan`) fallback locale.

The bootstrap deliberately maximizes dialect coverage, but equal-length positional word
alignment can still learn false correspondences. This refinement regenerates every
`esan` fallback value from the Spanish semantic source using a stricter corpus learner:
only isolated 1-word -> 1-word replacements identified by SequenceMatcher may become
word mappings, and they still need repeated, coherent evidence.

This is automated/generative assistance, not native-speaker review.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import json
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
TOKEN_RE = re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\{[^{}]+\}|<[^<>]+>")
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'’][A-Za-zÀ-ÖØ-öø-ÿ]+)*")
DIALECT_MARKER_RE = re.compile(
    r"(?:\blô\b|\blâ\b|\bpa\b|\bder\b|\bâtta\b|\bçerbid|\bêtt|çç|çión|ôh\b|âh\b)",
    re.IGNORECASE,
)

MC_LOCALES_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_LOCALES_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_LOCALES_REF}/java"
NEO_BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/{locale}.json"
NEO_REFS = {
    "mc-1.21.1": "af467a3bc118f6bbc0970d68f7e03fa631d7e6f2",
    "mc-26.1": "aa207ef14cf3b938e28b4081162701953957c1d5",
    "mc-26.2": "511cadcafe3027d2a56b4448652ec9b74e2f3b07",
}

MANUAL_WORDS = {
    "para": "pa",
    "los": "lô",
    "las": "lâ",
    "del": "der",
}

MANUAL_VALUES = {
    "Origin Architect": "Origin Architect",
}

# High-visibility source strings that should remain semantically explicit even if
# the corpus lacks a safe isolated word mapping.
KEY_OVERRIDES = {
    "origins.neoorigins.human.name": "Humano",
}

# These patterns exposed false positional mappings during contextual QA. They are
# guards, not one-off fixes: the refinement fails if the root problem reappears.
FORBIDDEN_PATTERNS = (
    re.compile(r"\b\d+(?:[.,]\d+)?\s+de\s+de\b", re.I),
    re.compile(r"\brecibe\s+de\s+por\b", re.I),
    re.compile(r"\bde\s+adicional\b", re.I),
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Andalusian-Refinement"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def fetch_optional_json(url: str):
    try:
        return fetch_json(url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {}
        raise


def preserve_case(source: str, target: str) -> str:
    if source.isupper():
        return target.upper()
    if source[:1].isupper() and target:
        return target[:1].upper() + target[1:]
    return target


def protect(text: str):
    tokens = []

    def repl(match):
        token = f"ZXQTK{len(tokens):04d}QXZ"
        tokens.append(match.group(0))
        return token

    return TOKEN_RE.sub(repl, text), tokens


def restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        text = text.replace(f"ZXQTK{index:04d}QXZ", token)
    return text


def has_unsupported_letters(text: str) -> bool:
    for char in text:
        if not char.isalpha():
            continue
        if char.isascii() or "À" <= char <= "ÿ":
            continue
        return True
    return False


def safe_corpus_pair(source: str, target: str) -> bool:
    if not source.strip() or not target.strip() or has_unsupported_letters(target):
        return False
    if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(target)):
        return False
    similarity = SequenceMatcher(None, source.casefold(), target.casefold()).ratio()
    return similarity >= 0.25 or bool(DIALECT_MARKER_RE.search(target))


def build_safe_corpus_maps():
    spanish = fetch_json(f"{MC_LOCALES_BASE}/es_es.json")
    andalusian = fetch_json(f"{MC_LOCALES_BASE}/esan.json")
    shared = sorted(set(spanish) & set(andalusian))
    exact: dict[str, str] = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    isolated_replacements = 0

    for key in shared:
        source = str(spanish[key])
        target = str(andalusian[key])
        if not safe_corpus_pair(source, target):
            rejected += 1
            continue
        if source != target:
            exact[source] = target

        src_words = [word.casefold() for word in WORD_RE.findall(source)]
        dst_words = [word.casefold() for word in WORD_RE.findall(target)]
        if not src_words or not dst_words or max(len(src_words), len(dst_words)) > 50:
            continue

        matcher = SequenceMatcher(None, src_words, dst_words, autojunk=False)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != "replace" or i2 - i1 != 1 or j2 - j1 != 1:
                continue
            src = src_words[i1]
            dst = dst_words[j1]
            if src == dst:
                continue
            word_similarity = SequenceMatcher(None, src, dst).ratio()
            # Andalusian spelling is close enough to Spanish that a genuine isolated
            # orthographic replacement should retain substantial character overlap.
            if len(dst) >= 2 and word_similarity >= 0.42:
                votes[src][dst] += 1
                isolated_replacements += 1

    learned: dict[str, str] = {}
    for source, counter in votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        share = top / total
        # Stronger than bootstrap: two observations require 80% agreement; noisy
        # vocabulary needs at least five observations and 65% agreement.
        if (top >= 2 and share >= 0.80) or (top >= 5 and share >= 0.65):
            learned[source] = target

    learned.update(MANUAL_WORDS)

    # Known false mapping must never be learned again.
    if learned.get("daño") in {"de", "del"}:
        raise RuntimeError(f"Unsafe daño mapping survived safe learner: {learned['daño']!r}")

    print(
        f"Safe Andalusian corpus: {len(shared)} aligned entries, {rejected} rejected pairs, "
        f"{len(exact)} exact strings, {isolated_replacements} isolated replacements, "
        f"{len(learned)} accepted word mappings"
    )
    return exact, learned


def andalusianize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
    if text in MANUAL_VALUES:
        return MANUAL_VALUES[text]
    if text in exact:
        result = exact[text]
        if sorted(PLACEHOLDER_RE.findall(text)) != sorted(PLACEHOLDER_RE.findall(result)):
            raise RuntimeError(f"Exact-map placeholder mismatch: {text!r} -> {result!r}")
        return result

    masked, tokens = protect(text)

    def replace_word(match):
        word = match.group(0)
        mapped = learned.get(word.casefold())
        return word if mapped is None else preserve_case(word, mapped)

    result = WORD_RE.sub(replace_word, masked)
    result = restore(result, tokens)
    if sorted(PLACEHOLDER_RE.findall(text)) != sorted(PLACEHOLDER_RE.findall(result)):
        raise RuntimeError(f"Andalusian placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_spanish() -> dict[str, str]:
    merged = {}
    for path in sorted(ASSETS.glob("**/lang/es_es.json")):
        for key, value in read_json(path).items():
            merged.setdefault(key, value)
    return merged


def build_neoorigins_sources(local_spanish: dict[str, str]):
    result = {}
    for label, ref in NEO_REFS.items():
        official = fetch_optional_json(NEO_BASE.format(ref=ref, locale="es_es"))
        merged = dict(official)
        for key, value in local_spanish.items():
            merged.setdefault(key, value)
        result[label] = merged
        print(f"Spanish semantic source {label}: official={len(official)}, merged={len(merged)}")
    return result


def spanish_value_for(path: Path, key: str, neo_sources: dict[str, dict], local_spanish: dict[str, str]):
    namespace = path.parents[1].name
    if namespace == "neoorigins_26_1":
        source = neo_sources["mc-26.1"]
    elif namespace == "neoorigins_26_2":
        source = neo_sources["mc-26.2"]
    elif namespace.startswith("neoorigins_esan_"):
        source = neo_sources["mc-1.21.1"]
    else:
        direct = ASSETS / namespace / "lang/es_es.json"
        if direct.exists():
            direct_data = read_json(direct)
            if key in direct_data:
                return str(direct_data[key])
        source = local_spanish

    if key not in source:
        raise KeyError(f"Missing Spanish semantic source for {namespace}:{key}")
    return str(source[key])


def main() -> None:
    files = sorted(ASSETS.glob("**/lang/esan.json"))
    if len(files) != 29:
        raise SystemExit(f"Expected 29 Andalusian files, found {len(files)}")

    local_spanish = collect_local_spanish()
    neo_sources = build_neoorigins_sources(local_spanish)
    exact, learned = build_safe_corpus_maps()

    changed_values = 0
    total_values = 0
    for path in files:
        old_data = read_json(path)
        new_data = {}
        for key in old_data:
            source = spanish_value_for(path, key, neo_sources, local_spanish)
            target = KEY_OVERRIDES.get(key, andalusianize(source, exact, learned))
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
        raise SystemExit(f"Known false-alignment patterns survived refinement: {bad[:20]}")

    text = "\n".join(value for _, _, value in rows)
    marker_count = len(DIALECT_MARKER_RE.findall(text))
    if marker_count < 250:
        raise SystemExit(f"Andalusian dialect marker sanity too low after refinement: {marker_count}")

    # Quality probes for the exact problems discovered during contextual QA.
    probes = {key: value for _, key, value in rows}
    if probes.get("origins.neoorigins.human.name") != "Humano":
        raise SystemExit("Human origin label is not correctly localized as Humano")
    damage_keys = [
        "power.neoorigins.avian_no_fall_damage.description",
        "power.neoorigins.enderian_water_damage.description",
    ]
    for key in damage_keys:
        value = probes.get(key, "")
        if "daño" not in value.casefold():
            raise SystemExit(f"Damage semantic check failed for {key}: {value!r}")

    print(
        f"Andalusian safe refinement passed: regenerated {total_values} values across {len(files)} files; "
        f"{changed_values} values changed from bootstrap; {marker_count} dialect markers; "
        "0 known false-alignment patterns."
    )


if __name__ == "__main__":
    main()
