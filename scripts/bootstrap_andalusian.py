#!/usr/bin/env python3
"""Generate Andalusian (`esan`) fallback localization from complete Spanish semantics.

The projection is deterministic: the project's Spanish coverage supplies meaning,
while Minecraft's pinned `es_es`/`esan` parallel corpus supplies Andalusian spelling
and vocabulary. This is automated/generative assistance, not native-speaker review.
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

# Only extremely stable forms are forced. Most dialect projection is learned from
# repeated evidence in Minecraft's own Andalusian corpus.
MANUAL_WORDS = {
    "para": "pa",
    "los": "lô",
    "las": "lâ",
    "del": "der",
}

MANUAL_VALUES = {
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Andalusian-Bootstrap"})
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
    # Andalusian orthography used by Minecraft stays within ASCII + Latin-1 letters.
    # Reject corpus rows with unrelated scripts so they cannot poison learned maps.
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
    # `esan` is a close Spanish dialect/orthography. Very low-similarity rows without
    # any Andalusian marker are treated as accidental cross-language contamination.
    return similarity >= 0.25 or bool(DIALECT_MARKER_RE.search(target))


def build_corpus_maps():
    spanish = fetch_json(f"{MC_LOCALES_BASE}/es_es.json")
    andalusian = fetch_json(f"{MC_LOCALES_BASE}/esan.json")
    shared = sorted(set(spanish) & set(andalusian))
    exact = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0

    for key in shared:
        source = str(spanish[key])
        target = str(andalusian[key])
        if not safe_corpus_pair(source, target):
            rejected += 1
            continue
        if source != target:
            exact[source] = target

        src_words = WORD_RE.findall(source)
        dst_words = WORD_RE.findall(target)
        if not src_words or len(src_words) != len(dst_words) or len(src_words) > 40:
            continue
        for src, dst in zip(src_words, dst_words):
            s = src.casefold()
            d = dst.casefold()
            if s != d:
                votes[s][d] += 1

    learned = {}
    for source, counter in votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        share = top / total
        similarity = SequenceMatcher(None, source, target).ratio()
        plausible = len(target) >= 2 and similarity >= 0.30
        # Never trust singleton alignments: repeated corpus evidence is required.
        if plausible and (
            (top >= 2 and share >= 0.60)
            or (top >= 5 and share >= 0.50)
        ):
            learned[source] = target

    destructive = {s: t for s, t in learned.items() if len(s) >= 5 and len(t) <= 1}
    if destructive:
        raise RuntimeError(f"Destructive learned Andalusian mappings detected: {destructive}")

    learned.update(MANUAL_WORDS)
    print(
        f"Minecraft Andalusian corpus: {len(shared)} aligned entries, "
        f"{rejected} rejected suspicious pairs, {len(exact)} exact dialect strings, "
        f"{len(learned)} learned word mappings"
    )
    return exact, learned


def andalusianize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
    if text in MANUAL_VALUES:
        return MANUAL_VALUES[text]
    if text in exact:
        result = exact[text]
        if sorted(PLACEHOLDER_RE.findall(text)) != sorted(PLACEHOLDER_RE.findall(result)):
            raise RuntimeError(f"Corpus exact-map placeholder mismatch: {text!r} -> {result!r}")
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
    print(f"Local Spanish fallback pool: {len(merged)} distinct keys")
    return merged


def neo_spanish(ref: str, english: dict[str, str], local_spanish: dict[str, str]) -> dict[str, str]:
    official = fetch_optional_json(NEO_BASE.format(ref=ref, locale="es_es"))
    merged = dict(official)
    for key, value in local_spanish.items():
        merged.setdefault(key, value)
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"Spanish NeoOrigins semantic source incomplete at {ref}: {len(missing)} missing, sample={missing[:20]}"
        )
    print(f"NeoOrigins {ref}: Spanish source official={len(official)}, merged={len(merged)}")
    return {key: merged[key] for key in english}


def addon_spanish(namespace: str, english: dict[str, str], local_spanish: dict[str, str]) -> dict[str, str]:
    direct = ASSETS / namespace / "lang/es_es.json"
    merged = dict(local_spanish)
    if direct.exists():
        merged.update(read_json(direct))
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"Spanish source incomplete for {namespace}: {len(missing)} missing, sample={missing[:20]}"
        )
    return {key: merged[key] for key in english}


def translated_payload(spanish: dict[str, str], exact, learned):
    return {key: andalusianize(value, exact, learned) for key, value in spanish.items()}


def main():
    neo_121_en = read_json(ROOT / "build/esan-discovery-mc-1.21.1/esan_missing_en.json")
    neo_261_en = read_json(ROOT / "build/esan-discovery-mc-26.1/esan_missing_en.json")
    neo_262_en = read_json(ROOT / "build/esan-discovery-mc-26.2/esan_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins Andalusian split: common={len(common_en)}, "
        f"1.21.1={len(delta_121_en)}, 26.1={len(delta_261_en)}, 26.2={len(delta_262_en)}"
    )

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
    addons_en = {namespace: read_json(path) for namespace, path in source_files.items()}
    shared_background_keys = set(addons_en["origins_backgrounds"])
    addons_en["origins_backgrounds_two"] = {
        key: value for key, value in addons_en["origins_backgrounds_two"].items()
        if key not in shared_background_keys
    }
    addons_en["origins_backgrounds_iss"] = {
        key: value for key, value in addons_en["origins_backgrounds_iss"].items()
        if key not in shared_background_keys
    }

    local_spanish = collect_local_spanish()
    exact, learned = build_corpus_maps()

    spanish_121 = neo_spanish(NEO_REFS["mc-1.21.1"], neo_121_en, local_spanish)
    spanish_261 = neo_spanish(NEO_REFS["mc-26.1"], neo_261_en, local_spanish)
    spanish_262 = neo_spanish(NEO_REFS["mc-26.2"], neo_262_en, local_spanish)

    disagreements = [
        key for key in common_en
        if spanish_121.get(key) != spanish_261.get(key) or spanish_121.get(key) != spanish_262.get(key)
    ]
    print(f"Common Spanish target disagreements: {len(disagreements)}")

    common_es = {key: spanish_121[key] for key in common_en}
    delta_121_es = {key: spanish_121[key] for key in delta_121_en}
    delta_261_es = {key: spanish_261[key] for key in delta_261_en}
    delta_262_es = {key: spanish_262[key] for key in delta_262_en}

    common_esan = translated_payload(common_es, exact, learned)
    delta_121_esan = translated_payload(delta_121_es, exact, learned)
    delta_261_esan = translated_payload(delta_261_es, exact, learned)
    delta_262_esan = translated_payload(delta_262_es, exact, learned)

    common_items = list(common_esan.items())
    chunk_size = 150
    common_chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(common_chunks):
        write_json(
            ASSETS / f"neoorigins_esan_common_{index + 1:02d}/lang/esan.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_esan_121/lang/esan.json", delta_121_esan)
    write_json(ASSETS / "neoorigins_26_1/lang/esan.json", delta_261_esan)
    write_json(ASSETS / "neoorigins_26_2/lang/esan.json", delta_262_esan)

    addon_total = 0
    for namespace, english in addons_en.items():
        spanish = addon_spanish(namespace, english, local_spanish)
        output = translated_payload(spanish, exact, learned)
        write_json(ASSETS / namespace / "lang/esan.json", output)
        addon_total += len(output)

    files = sorted(ASSETS.glob("**/lang/esan.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Andalusian files after bootstrap, found {len(files)}")

    values = [str(value) for path in files for value in read_json(path).values()]
    source_values = [*common_es.values(), *delta_121_es.values(), *delta_261_es.values(), *delta_262_es.values()]
    changed_neo = sum(andalusianize(value, exact, learned) != value for value in source_values)
    text = "\n".join(values)
    markers = len(DIALECT_MARKER_RE.findall(text))
    print(
        f"Generated Andalusian locale: {len(files)} files; NeoOrigins changed-vs-Spanish "
        f"{changed_neo}/{len(source_values)}; Andalusian markers={markers}; add-on strings={addon_total}"
    )
    if changed_neo < int(len(source_values) * 0.25):
        raise RuntimeError(
            f"Andalusian projection too weak: only {changed_neo}/{len(source_values)} NeoOrigins strings changed"
        )
    if markers < 250:
        raise RuntimeError(f"Andalusian marker sanity too low: {markers}")


if __name__ == "__main__":
    main()
