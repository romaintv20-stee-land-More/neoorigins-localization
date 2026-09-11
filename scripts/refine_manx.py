#!/usr/bin/env python3
"""Refine generated Manx (`gv_im`) fallback output with full Manx translation.

Contextual QA showed that projecting isolated corpus words into otherwise-English
sentences creates unsafe hybrids. Google Translate has direct Manx support, so this
pass translates the complete English semantic source to Manx while keeping the pinned
Minecraft en_us -> gv_im corpus as the preferred source for exact whole-string matches.
Technical tokens and placeholders are protected and validated. This is automated
translation assistance, not native-speaker review.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlencode
import json
import random
import re
import time
import urllib.error
import urllib.request

import bootstrap_manx as base

ROOT = base.ROOT
ASSETS = base.ASSETS
GOOGLE_ENDPOINT = "https://translate.googleapis.com/translate_a/single"

GOOGLE_PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)

FORBIDDEN_MIXED_PATTERNS = (
    re.compile(r"\bAquatic Bieauid\b", re.I),
    re.compile(r"\bSky Bieauid\b", re.I),
    re.compile(r"\bflight bieauid\b", re.I),
    re.compile(r"\bthe seihll\b", re.I),
    re.compile(r"\benergy tappee\b", re.I),
    re.compile(r"\bwater coirrey\b", re.I),
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protect_for_google(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(match: re.Match[str]) -> str:
        marker = f"ZXQTK{len(tokens):04d}QXZ"
        tokens.append(match.group(0))
        return marker

    return GOOGLE_PROTECT_RE.sub(repl, text), tokens


def restore_google_tokens(text: str, tokens: list[str]) -> str:
    for index, token in enumerate(tokens):
        marker = f"ZXQTK{index:04d}QXZ"
        if marker not in text:
            raise RuntimeError(f"Google translation lost protected token {marker}: {text!r}")
        text = text.replace(marker, token)
    if re.search(r"ZXQTK\d{4}QXZ", text):
        raise RuntimeError(f"Unexpected protected token survived restoration: {text!r}")
    return text


def google_translate_one(source: str) -> str:
    masked, tokens = protect_for_google(source)
    params = urlencode(
        {
            "client": "gtx",
            "sl": "en",
            "tl": "gv",
            "dt": "t",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "q": masked,
        }
    )
    url = f"{GOOGLE_ENDPOINT}?{params}"
    last_error: Exception | None = None
    for attempt in range(6):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 NeoOrigins-Manx-Localization/1.0",
                    "Accept": "application/json,text/plain,*/*",
                },
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            segments = payload[0]
            translated = "".join(segment[0] for segment in segments if segment and segment[0])
            translated = restore_google_tokens(translated, tokens)
            if base.placeholder_signature(source) != base.placeholder_signature(translated):
                raise RuntimeError(
                    f"Placeholder mismatch after Google translation: {source!r} -> {translated!r}"
                )
            if not translated.strip():
                raise RuntimeError(f"Empty Google translation for {source!r}")
            return translated
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError, ValueError) as exc:
            last_error = exc
            if attempt == 5:
                break
            time.sleep((1.4 ** attempt) + random.random() * 0.35)
    raise RuntimeError(f"Google Manx translation failed for {source!r}: {last_error}")


def build_sources() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, dict[str, str]]]:
    neo_121_en = read_json(ROOT / "build/gv-discovery-mc-1.21.1/gv_im_missing_en.json")
    neo_261_en = read_json(ROOT / "build/gv-discovery-mc-26.1/gv_im_missing_en.json")
    neo_262_en = read_json(ROOT / "build/gv-discovery-mc-26.2/gv_im_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}

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
    return common_en, delta_121_en, delta_261_en, delta_262_en, addons_en


def translate_value(source: str, exact: dict[str, str]) -> str:
    if source in base.MANUAL_VALUES:
        return base.MANUAL_VALUES[source]
    if source in exact:
        return exact[source]
    return google_translate_one(source)


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Manx files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    common_en, delta_121_en, delta_261_en, delta_262_en, addons_en = build_sources()
    print(
        f"NeoOrigins Manx source split: common={len(common_en)}, "
        f"1.21.1={len(delta_121_en)}, 26.1={len(delta_261_en)}, 26.2={len(delta_262_en)}"
    )

    exact, learned = base.build_corpus_maps()
    print(
        f"Manx refinement policy: {len(exact)} exact Minecraft corpus strings take priority; "
        f"{len(learned)} isolated word mappings are disabled; remaining strings use direct en->gv translation."
    )

    source_payloads: list[dict[str, str]] = [common_en, delta_121_en, delta_261_en, delta_262_en]
    source_payloads.extend(addons_en.values())
    unique_sources = sorted({str(value) for payload in source_payloads for value in payload.values()})

    translated_by_source: dict[str, str] = {}
    network_sources = []
    for source in unique_sources:
        if source in base.MANUAL_VALUES:
            translated_by_source[source] = base.MANUAL_VALUES[source]
        elif source in exact:
            translated_by_source[source] = exact[source]
        else:
            network_sources.append(source)

    print(
        f"Manx translation pool: {len(unique_sources)} unique strings; "
        f"{len(translated_by_source)} corpus/manual hits; {len(network_sources)} direct Google translations."
    )

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(google_translate_one, source): source for source in network_sources}
        completed = 0
        for future in as_completed(futures):
            source = futures[future]
            translated_by_source[source] = future.result()
            completed += 1
            if completed % 250 == 0 or completed == len(network_sources):
                print(f"Direct Manx translations completed: {completed}/{len(network_sources)}")

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result = {}
        for key, raw_value in source.items():
            value = str(raw_value)
            translated = translated_by_source[value]
            if base.placeholder_signature(value) != base.placeholder_signature(translated):
                raise SystemExit(f"Placeholder mismatch for {key}: {value!r} -> {translated!r}")
            result[key] = translated
        return result

    common_gv = translated_payload(common_en)
    delta_121_gv = translated_payload(delta_121_en)
    delta_261_gv = translated_payload(delta_261_en)
    delta_262_gv = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_gv_common_*/lang/gv_im.json"):
        path.unlink()
    common_items = list(common_gv.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_gv_common_{index + 1:02d}/lang/gv_im.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_gv_121/lang/gv_im.json", delta_121_gv)
    write_json(ASSETS / "neoorigins_26_1/lang/gv_im.json", delta_261_gv)
    write_json(ASSETS / "neoorigins_26_2/lang/gv_im.json", delta_262_gv)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/gv_im.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Manx files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    total_values = 0
    source_changed = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Manx refinement: {path}")
        for key, value in new_data.items():
            total_values += 1
            seen[key] = str(value)
            if old_data[key] != value:
                changed_values += 1

    for payload in source_payloads:
        for value in payload.values():
            source = str(value)
            if translated_by_source[source] != source:
                source_changed += 1

    text = "\n".join(str(value) for data in after.values() for value in data.values())
    for pattern in FORBIDDEN_MIXED_PATTERNS:
        match = pattern.search(text)
        if match:
            raise SystemExit(f"Known mixed-language Manx projection survived: {match.group(0)!r}")

    marker_count = len(base.MANX_MARKER_RE.findall(text))
    marked_values = sum(
        1
        for data in after.values()
        for value in data.values()
        if base.MANX_MARKER_RE.search(str(value))
    )
    if marker_count < 250 or marked_values < 200:
        raise SystemExit(
            f"Manx differentiation unexpectedly weak after full translation: "
            f"markers={marker_count}, marked_values={marked_values}"
        )
    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived full Manx translation: only {source_changed} values changed"
        )

    expected_values = {
        "gui.neoorigins.info.edit": "Reaghey",
        "gui.neoorigins.creator.save": "Sauail",
        "screen.originsmodernui.search": "Ronsee",
        "key.categories.originsmodernui": "Origin Architect",
    }
    for key, expected in expected_values.items():
        actual = seen.get(key)
        if actual != expected:
            raise SystemExit(
                f"High-visibility Manx QA failed for {key}: {actual!r}, expected {expected!r}"
            )

    print(
        f"Manx full refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        f"{marker_count} Manx lexical markers across {marked_values} values; "
        "0 known mixed-language projection patterns."
    )


if __name__ == "__main__":
    main()
