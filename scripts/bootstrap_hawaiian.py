#!/usr/bin/env python3
"""Generate Hawaiian (`haw_us`) fallback localization bootstrap files.

English remains the semantic source. Exact whole-string replacements are reused from
the pinned Minecraft Java `en_us` <-> `haw_us` corpus. Remaining English strings are
left intact for the dedicated full-translation refinement pass. No isolated-word
projection is performed, because projecting words into English sentences can create
unsafe mixed-language output. This is automated assistance, not native-speaker review.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import unicodedata
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")

MC_LOCALES_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_LOCALES_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_LOCALES_REF}/java"

# Proper project/technical name: deliberately preserved rather than invented.
MANUAL_VALUES = {
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Hawaiian-Bootstrap"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def placeholder_signature(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def unsupported_script(text: str) -> bool:
    for char in text:
        if not char.isalpha() or char.isascii():
            continue
        if "LATIN" in unicodedata.name(char, ""):
            continue
        return True
    return False


def safe_pair(source: str, target: str) -> bool:
    if not source.strip() or not target.strip():
        return False
    if unsupported_script(target):
        return False
    if placeholder_signature(source) != placeholder_signature(target):
        return False
    if source.casefold() == target.casefold():
        return False
    return True


def build_corpus_map() -> dict[str, str]:
    english = fetch_json(f"{MC_LOCALES_BASE}/en_us.json")
    hawaiian = fetch_json(f"{MC_LOCALES_BASE}/haw_us.json")
    shared = sorted(set(english) & set(hawaiian))

    exact_votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    unchanged = 0
    for key in shared:
        source = str(english[key])
        target = str(hawaiian[key])
        if source.casefold() == target.casefold():
            unchanged += 1
            continue
        if not safe_pair(source, target):
            rejected += 1
            continue
        exact_votes[source][target] += 1

    exact: dict[str, str] = {}
    ambiguous = 0
    for source, counter in exact_votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        if top / total >= 0.80:
            exact[source] = target
        else:
            ambiguous += 1

    print(
        f"Minecraft Hawaiian corpus: {len(shared)} aligned entries, "
        f"{rejected} rejected pairs, {unchanged} unchanged English pairs, "
        f"{len(exact)} exact Hawaiian strings, {ambiguous} ambiguous exact sources"
    )
    return exact


def hawaiianize(text: str, exact: dict[str, str]) -> str:
    if text in MANUAL_VALUES:
        return MANUAL_VALUES[text]
    result = exact.get(text, text)
    if placeholder_signature(text) != placeholder_signature(result):
        raise RuntimeError(f"Hawaiian placeholder mismatch: {text!r} -> {result!r}")
    return result


def translated_payload(source: dict[str, str], exact: dict[str, str]):
    return {key: hawaiianize(str(value), exact) for key, value in source.items()}


def main():
    neo_121_en = read_json(ROOT / "build/haw-discovery-mc-1.21.1/haw_us_missing_en.json")
    neo_261_en = read_json(ROOT / "build/haw-discovery-mc-26.1/haw_us_missing_en.json")
    neo_262_en = read_json(ROOT / "build/haw-discovery-mc-26.2/haw_us_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins Hawaiian split: common={len(common_en)}, "
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
        k: v for k, v in addons_en["origins_backgrounds_two"].items() if k not in shared_background_keys
    }
    addons_en["origins_backgrounds_iss"] = {
        k: v for k, v in addons_en["origins_backgrounds_iss"].items() if k not in shared_background_keys
    }

    exact = build_corpus_map()

    common_haw = translated_payload(common_en, exact)
    delta_121_haw = translated_payload(delta_121_en, exact)
    delta_261_haw = translated_payload(delta_261_en, exact)
    delta_262_haw = translated_payload(delta_262_en, exact)

    for path in ASSETS.glob("neoorigins_haw_common_*/lang/haw_us.json"):
        path.unlink()

    common_items = list(common_haw.items())
    chunk_size = 150
    chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(chunks):
        write_json(
            ASSETS / f"neoorigins_haw_common_{index + 1:02d}/lang/haw_us.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_haw_121/lang/haw_us.json", delta_121_haw)
    write_json(ASSETS / "neoorigins_26_1/lang/haw_us.json", delta_261_haw)
    write_json(ASSETS / "neoorigins_26_2/lang/haw_us.json", delta_262_haw)

    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/haw_us.json", translated_payload(english, exact))

    files = sorted(ASSETS.glob("**/lang/haw_us.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Hawaiian files after generation, found {len(files)}")

    source_payloads = [common_en, delta_121_en, delta_261_en, delta_262_en, *addons_en.values()]
    exact_hits = sum(
        1 for payload in source_payloads for value in payload.values()
        if str(value) in exact or str(value) in MANUAL_VALUES
    )
    values = [str(v) for path in files for v in read_json(path).values()]
    if any(unsupported_script(value) for value in values):
        raise RuntimeError("Unexpected non-Latin script found in Hawaiian bootstrap output")

    print(
        f"Hawaiian bootstrap generated {len(files)} files; "
        f"exact/manual corpus replacements applied to {exact_hits} source values. "
        "Remaining English strings are intentionally deferred to full refinement."
    )


if __name__ == "__main__":
    main()
