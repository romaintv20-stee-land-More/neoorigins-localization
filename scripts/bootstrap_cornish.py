#!/usr/bin/env python3
"""Generate Cornish (`kw_gb`) fallback bootstrap files.

English is the semantic source. Exact whole-string Minecraft `kw_gb` corpus matches
are reused first; remaining English strings are left for a direct full-sentence
English -> Cornish (`cor`) MT refinement. No word projection or language pivot.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
MC_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_REF}/java"
MANUAL_VALUES = {"Origin Architect": "Origin Architect"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Cornish-Bootstrap"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def placeholder_signature(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def build_corpus_map() -> dict[str, str]:
    english = fetch_json(f"{MC_BASE}/en_us.json")
    cornish = fetch_json(f"{MC_BASE}/kw_gb.json")
    shared = sorted(set(english) & set(cornish))
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = unchanged = 0
    for key in shared:
        source, target = str(english[key]), str(cornish[key])
        if source.casefold() == target.casefold():
            unchanged += 1
            continue
        if not source.strip() or not target.strip() or placeholder_signature(source) != placeholder_signature(target):
            rejected += 1
            continue
        votes[source][target] += 1
    exact: dict[str, str] = {}
    ambiguous = 0
    for source, counter in votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        if top / total >= 0.80:
            exact[source] = target
        else:
            ambiguous += 1
    print(
        f"Minecraft Cornish corpus: {len(shared)} aligned entries, {rejected} rejected, "
        f"{unchanged} unchanged, {len(exact)} exact strings, {ambiguous} ambiguous sources"
    )
    return exact


def translate_payload(source: dict[str, str], exact: dict[str, str]):
    result = {}
    for key, raw in source.items():
        value = str(raw)
        translated = MANUAL_VALUES.get(value, exact.get(value, value))
        if placeholder_signature(value) != placeholder_signature(translated):
            raise RuntimeError(f"Cornish placeholder mismatch: {value!r} -> {translated!r}")
        result[key] = translated
    return result


def main():
    neo121 = read_json(ROOT / "build/kw-discovery-mc-1.21.1/kw_gb_missing_en.json")
    neo261 = read_json(ROOT / "build/kw-discovery-mc-26.1/kw_gb_missing_en.json")
    neo262 = read_json(ROOT / "build/kw-discovery-mc-26.2/kw_gb_missing_en.json")
    common = {k: v for k, v in neo121.items() if neo261.get(k) == v and neo262.get(k) == v}
    delta121 = {k: v for k, v in neo121.items() if k not in common}
    delta261 = {k: v for k, v in neo261.items() if k not in common}
    delta262 = {k: v for k, v in neo262.items() if k not in common}
    print(f"NeoOrigins Cornish split: common={len(common)}, 1.21.1={len(delta121)}, 26.1={len(delta261)}, 26.2={len(delta262)}")

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
    shared_bg = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {k: v for k, v in addons["origins_backgrounds_two"].items() if k not in shared_bg}
    addons["origins_backgrounds_iss"] = {k: v for k, v in addons["origins_backgrounds_iss"].items() if k not in shared_bg}

    exact = build_corpus_map()
    common_kw = translate_payload(common, exact)
    for path in ASSETS.glob("neoorigins_kw_common_*/lang/kw_gb.json"):
        path.unlink()
    items = list(common_kw.items())
    for index in range((len(items) + 149) // 150):
        write_json(ASSETS / f"neoorigins_kw_common_{index + 1:02d}/lang/kw_gb.json", dict(items[index * 150:(index + 1) * 150]))
    write_json(ASSETS / "neoorigins_kw_121/lang/kw_gb.json", translate_payload(delta121, exact))
    write_json(ASSETS / "neoorigins_26_1/lang/kw_gb.json", translate_payload(delta261, exact))
    write_json(ASSETS / "neoorigins_26_2/lang/kw_gb.json", translate_payload(delta262, exact))
    for ns, english in addons.items():
        write_json(ASSETS / ns / "lang/kw_gb.json", translate_payload(english, exact))

    files = sorted(ASSETS.glob("**/lang/kw_gb.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Cornish files, found {len(files)}")
    payloads = [common, delta121, delta261, delta262, *addons.values()]
    total = sum(len(p) for p in payloads)
    hits = sum(1 for p in payloads for value in p.values() if str(value) in exact or str(value) in MANUAL_VALUES)
    print(f"Cornish bootstrap generated 29 files; exact/manual replacements {hits}/{total}; {total-hits} remain for direct MT")


if __name__ == "__main__":
    main()
