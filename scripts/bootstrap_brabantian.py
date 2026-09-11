#!/usr/bin/env python3
"""Generate Brabantian fallback localization from the project's Dutch coverage.

Minecraft ships Brabantian as the independent `brb` locale (Braobans). This bootstrap
uses the project's complete Dutch localization as the semantic source and projects it
into Minecraft-style Brabantian with a pinned nl_nl/brb parallel corpus. The result is
a deterministic bootstrap and must not be described as a native-speaker review.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
TOKEN_RE = re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\{[^{}]+\}|<[^<>]+>")
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'’][A-Za-zÀ-ÖØ-öø-ÿ]+)*")

MC_LOCALES_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_LOCALES_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_LOCALES_REF}/java"
NEO_BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/{locale}.json"
NEO_REFS = {
    "mc-1.21.1": "af467a3bc118f6bbc0970d68f7e03fa631d7e6f2",
    "mc-26.1": "aa207ef14cf3b938e28b4081162701953957c1d5",
    "mc-26.2": "511cadcafe3027d2a56b4448652ec9b74e2f3b07",
}

# Conservative high-confidence Brabantian forms. Statistical mappings learned from
# Minecraft's own nl_nl/brb corpus remain the primary dialect source.
MANUAL_WORDS = {
    "niet": "nie",
    "jij": "gij",
    "jou": "oe",
    "jouw": "oew",
    "jullie": "gullie",
    "dat": "da",
    "wat": "wa",
    "maar": "mar",
    "voor": "veur",
    "geen": "gin",
    "kunnen": "kunne",
    "doen": "doen",
}

# Product names and technical labels are intentionally conservative until contextual
# refinement has inspected the generated locale.
MANUAL_VALUES = {
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Brabantian-Bootstrap"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


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


def build_corpus_maps():
    nl = fetch_json(f"{MC_LOCALES_BASE}/nl_nl.json")
    brb = fetch_json(f"{MC_LOCALES_BASE}/brb.json")
    shared = sorted(set(nl) & set(brb))
    exact = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)

    for key in shared:
        source = str(nl[key])
        target = str(brb[key])
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
        plausible = len(target) >= 2 and similarity >= 0.35
        if plausible and (
            (top >= 2 and share >= 0.60)
            or (top >= 5 and share >= 0.50)
            or (top == 1 and total == 1 and len(source) >= 4 and similarity >= 0.52)
        ):
            learned[source] = target

    destructive = {s: t for s, t in learned.items() if len(s) >= 5 and len(t) <= 1}
    if destructive:
        raise RuntimeError(f"Destructive learned Brabantian mappings detected: {destructive}")

    learned.update(MANUAL_WORDS)
    print(
        f"Minecraft Brabantian corpus: {len(shared)} aligned entries, "
        f"{len(exact)} exact dialect strings, {len(learned)} learned word mappings"
    )
    return exact, learned


def brabantianize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
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
        if mapped is None:
            return word
        return preserve_case(word, mapped)

    result = WORD_RE.sub(replace_word, masked)
    result = restore(result, tokens)
    if sorted(PLACEHOLDER_RE.findall(text)) != sorted(PLACEHOLDER_RE.findall(result)):
        raise RuntimeError(f"Brabantian placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_dutch() -> dict[str, str]:
    merged = {}
    for path in sorted(ASSETS.glob("**/lang/nl_nl.json")):
        for key, value in read_json(path).items():
            merged.setdefault(key, value)
    print(f"Local Dutch fallback pool: {len(merged)} distinct keys")
    return merged


def neo_dutch(ref: str, english: dict[str, str], local_dutch: dict[str, str]) -> dict[str, str]:
    official = fetch_json(NEO_BASE.format(ref=ref, locale="nl_nl"))
    merged = dict(official)
    for key, value in local_dutch.items():
        merged.setdefault(key, value)
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"Dutch NeoOrigins semantic source incomplete at {ref}: {len(missing)} missing, sample={missing[:20]}"
        )
    return {key: merged[key] for key in english}


def addon_dutch(namespace: str, english: dict[str, str], local_dutch: dict[str, str]) -> dict[str, str]:
    direct = ASSETS / namespace / "lang/nl_nl.json"
    merged = dict(local_dutch)
    if direct.exists():
        merged.update(read_json(direct))
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"Dutch source incomplete for {namespace}: {len(missing)} missing, sample={missing[:20]}"
        )
    return {key: merged[key] for key in english}


def translated_payload(dutch: dict[str, str], exact, learned):
    return {key: brabantianize(value, exact, learned) for key, value in dutch.items()}


def main():
    neo_121_en = read_json(ROOT / "build/brb-discovery-mc-1.21.1/brb_missing_en.json")
    neo_261_en = read_json(ROOT / "build/brb-discovery-mc-26.1/brb_missing_en.json")
    neo_262_en = read_json(ROOT / "build/brb-discovery-mc-26.2/brb_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins Brabantian split: common={len(common_en)}, "
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
        key: value
        for key, value in addons_en["origins_backgrounds_two"].items()
        if key not in shared_background_keys
    }
    addons_en["origins_backgrounds_iss"] = {
        key: value
        for key, value in addons_en["origins_backgrounds_iss"].items()
        if key not in shared_background_keys
    }

    local_dutch = collect_local_dutch()
    exact, learned = build_corpus_maps()

    dutch_121 = neo_dutch(NEO_REFS["mc-1.21.1"], neo_121_en, local_dutch)
    dutch_261 = neo_dutch(NEO_REFS["mc-26.1"], neo_261_en, local_dutch)
    dutch_262 = neo_dutch(NEO_REFS["mc-26.2"], neo_262_en, local_dutch)

    disagreements = [
        key
        for key in common_en
        if dutch_121.get(key) != dutch_261.get(key) or dutch_121.get(key) != dutch_262.get(key)
    ]
    print(f"Common Dutch target disagreements: {len(disagreements)}")

    common_nl = {key: dutch_121[key] for key in common_en}
    delta_121_nl = {key: dutch_121[key] for key in delta_121_en}
    delta_261_nl = {key: dutch_261[key] for key in delta_261_en}
    delta_262_nl = {key: dutch_262[key] for key in delta_262_en}

    common_brb = translated_payload(common_nl, exact, learned)
    delta_121_brb = translated_payload(delta_121_nl, exact, learned)
    delta_261_brb = translated_payload(delta_261_nl, exact, learned)
    delta_262_brb = translated_payload(delta_262_nl, exact, learned)

    common_items = list(common_brb.items())
    chunk_size = 150
    common_chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(common_chunks):
        write_json(
            ASSETS / f"neoorigins_brb_common_{index + 1:02d}/lang/brb.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_brb_121/lang/brb.json", delta_121_brb)
    write_json(ASSETS / "neoorigins_26_1/lang/brb.json", delta_261_brb)
    write_json(ASSETS / "neoorigins_26_2/lang/brb.json", delta_262_brb)

    addon_total = 0
    for namespace, english in addons_en.items():
        dutch = addon_dutch(namespace, english, local_dutch)
        output = translated_payload(dutch, exact, learned)
        write_json(ASSETS / namespace / "lang/brb.json", output)
        addon_total += len(output)

    files = sorted(ASSETS.glob("**/lang/brb.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Brabantian files after bootstrap, found {len(files)}")

    values = [str(value) for path in files for value in read_json(path).values()]
    nl_values = [*common_nl.values(), *delta_121_nl.values(), *delta_261_nl.values(), *delta_262_nl.values()]
    changed_neo = sum(brabantianize(value, exact, learned) != value for value in nl_values)
    text = "\n".join(values).casefold()
    markers = len(
        re.findall(
            r"\b(?:nie|gij|oe|oew|gullie|da|wa|mar|veur|gin|hedde|bende|kunde|unne|ge)\b",
            text,
        )
    )
    print(
        f"Generated Brabantian locale: {len(files)} files; NeoOrigins changed-vs-Dutch "
        f"{changed_neo}/{len(nl_values)}; Brabantian lexical markers={markers}; add-on strings={addon_total}"
    )
    if changed_neo < int(len(nl_values) * 0.20):
        raise RuntimeError(
            f"Brabantian projection too weak: only {changed_neo}/{len(nl_values)} NeoOrigins strings changed"
        )
    if markers < 150:
        raise RuntimeError(f"Brabantian lexical marker sanity too low: {markers}")


if __name__ == "__main__":
    main()
