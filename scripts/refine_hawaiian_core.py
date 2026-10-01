#!/usr/bin/env python3
"""Refine generated Hawaiian (`haw_us`) fallback output with full Hawaiian translation.

English remains the semantic source. Exact whole-string replacements from the pinned
Minecraft en_us -> haw_us corpus take priority; all remaining strings are translated
as complete strings with Google Translate's Hawaiian target (`haw`). No isolated-word
projection is used, avoiding artificial mixed-language output. Technical tokens and
placeholders are protected and validated. Network requests are serialized, cached,
and grouped into validated batches. This is automated translation assistance, not
native-speaker review.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode
import html as html_module
import json
import random
import re
import time
import urllib.error
import urllib.request

import bootstrap_hawaiian as base

ROOT = base.ROOT
ASSETS = base.ASSETS
GOOGLE_RPC_ENDPOINT = "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute"
GOOGLE_MOBILE_ENDPOINT = "https://translate.google.com/m"
CACHE_PATH = ROOT / "build/hawaiian-google-cache.json"

GOOGLE_PROTECT_RE = re.compile(
    r"%(?:\d+\$)?[sdif]|§.|\\n|\n|\{[^{}]+\}|<[^<>]+>|"
    r"\b(?:NeoOrigins|Origin Architect|HUD|JSON|XP|HP|NeoForge|Minecraft|CurseForge)\b"
)
BATCH_SEPARATOR_RE = re.compile(r"\s*ZXQSEP(\d{4})QXZ\s*")


class BatchValidationError(RuntimeError):
    """Raised when Google returns a batch that cannot be split safely."""


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        raw = read_json(CACHE_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Ignoring unreadable Hawaiian translation checkpoint: {exc}", flush=True)
        return {}
    if not isinstance(raw, dict):
        return {}
    valid: dict[str, str] = {}
    for source, translated in raw.items():
        if not isinstance(source, str) or not isinstance(translated, str) or not translated.strip():
            continue
        if base.placeholder_signature(source) != base.placeholder_signature(translated):
            continue
        if "ZXQTK" in translated or "ZXQSEP" in translated:
            continue
        if any(0xE000 <= ord(char) <= 0xF8FF for char in translated):
            continue
        valid[source] = translated
    return valid


def save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp = CACHE_PATH.with_suffix(".tmp")
    temp.write_text(json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(CACHE_PATH)


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
            raise BatchValidationError(f"Google translation lost protected token {marker}: {text!r}")
        text = text.replace(marker, token)
    if re.search(r"ZXQTK\d{4}QXZ", text):
        raise BatchValidationError(f"Unexpected protected token survived restoration: {text!r}")
    return text


def retry_delay(exc: Exception, attempt: int) -> float:
    if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
        retry_after = exc.headers.get("Retry-After") if exc.headers else None
        try:
            server_delay = float(retry_after) if retry_after else 0.0
        except ValueError:
            server_delay = 0.0
        return max(server_delay, min(90.0, 8.0 * (2 ** attempt))) + random.uniform(0.5, 1.5)
    return min(30.0, 2.0 * (2 ** attempt)) + random.uniform(0.25, 1.0)


def parse_rpc_response(raw: str) -> str:
    token_found = False
    response_json = ""
    opening_brackets = 0
    closing_brackets = 0
    for line in raw.splitlines():
        if not token_found:
            token_found = '"MkEWBc"' in line[:120]
            if not token_found:
                continue
        in_string = False
        escaped = False
        for char in line:
            if escaped:
                escaped = False
                continue
            if char == "\\" and in_string:
                escaped = True
                continue
            if char == '"':
                in_string = not in_string
                continue
            if not in_string:
                if char == "[":
                    opening_brackets += 1
                elif char == "]":
                    closing_brackets += 1
        response_json += line
        if opening_brackets and opening_brackets == closing_brackets:
            break

    if not response_json:
        raise RuntimeError("Google web RPC response did not contain MkEWBc payload")
    envelope = json.loads(response_json)
    payload = json.loads(envelope[0][2])
    try:
        translation_group = payload[1][0][0]
        segments = translation_group[5]
        joiner = " " if translation_group[3] else ""
        translated = joiner.join(part[0] for part in segments if part and part[0])
    except (IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected Google web RPC payload shape: {payload!r}") from exc
    if not translated.strip():
        raise RuntimeError("Google web RPC returned an empty translation")
    return translated


def google_rpc_request(masked: str) -> str:
    inner = json.dumps([[masked, "en", "haw", True], [None]], ensure_ascii=False, separators=(",", ":"))
    rpc_request = json.dumps(
        [[["MkEWBc", inner, None, "generic"]]], ensure_ascii=False, separators=(",", ":")
    )
    query = urlencode(
        {
            "rpcids": "MkEWBc",
            "source-path": "/",
            "soc-app": "1",
            "soc-platform": "1",
            "soc-device": "1",
            "rt": "c",
        }
    )
    request = urllib.request.Request(
        f"{GOOGLE_RPC_ENDPOINT}?{query}",
        data=urlencode({"f.req": rpc_request}).encode("utf-8"),
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://translate.google.com",
            "Referer": "https://translate.google.com/",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        raw = response.read().decode("utf-8")
    return parse_rpc_response(raw)


def google_mobile_request(masked: str) -> str:
    query = urlencode({"sl": "en", "tl": "haw", "q": masked})
    request = urllib.request.Request(
        f"{GOOGLE_MOBILE_ENDPOINT}?{query}",
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/152.0.0.0 Mobile Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        page = response.read().decode("utf-8", errors="replace")
    match = re.search(r'<div[^>]+class="result-container"[^>]*>(.*?)</div>', page, re.S | re.I)
    if not match:
        raise RuntimeError("Google mobile page did not contain result-container")
    translated = re.sub(r"<[^>]+>", "", match.group(1))
    translated = html_module.unescape(translated).strip()
    if not translated:
        raise RuntimeError("Google mobile page returned an empty translation")
    return translated


def google_request(masked: str) -> str:
    last_error: Exception | None = None
    for attempt in range(6):
        try:
            translated = google_rpc_request(masked)
            time.sleep(random.uniform(1.1, 1.5))
            return translated
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            try:
                translated = google_mobile_request(masked)
                print(
                    f"Google web RPC unavailable ({type(exc).__name__}: {exc}); mobile web fallback succeeded.",
                    flush=True,
                )
                time.sleep(random.uniform(1.25, 1.7))
                return translated
            except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as mobile_exc:
                last_error = mobile_exc
            if attempt == 5:
                break
            delay = retry_delay(last_error, attempt)
            if isinstance(last_error, urllib.error.HTTPError) and last_error.code == 429:
                print(
                    f"Google web routes returned HTTP 429; backing off for {delay:.1f}s "
                    f"(attempt {attempt + 1}/6).",
                    flush=True,
                )
            else:
                print(
                    f"Google web request retry in {delay:.1f}s after "
                    f"{type(last_error).__name__}: {last_error}",
                    flush=True,
                )
            time.sleep(delay)
    raise RuntimeError(f"Google Hawaiian web translation failed after retries: {last_error}")


def google_translate_one(source: str) -> str:
    masked, tokens = protect_for_google(source)
    translated = restore_google_tokens(google_request(masked), tokens)
    if base.placeholder_signature(source) != base.placeholder_signature(translated):
        raise RuntimeError(f"Placeholder mismatch after Google translation: {source!r} -> {translated!r}")
    return translated


def google_translate_batch(sources: list[str]) -> dict[str, str]:
    if not sources:
        return {}
    if len(sources) == 1:
        return {sources[0]: google_translate_one(sources[0])}

    protected = [protect_for_google(source) for source in sources]
    pieces: list[str] = []
    for index, (masked, _) in enumerate(protected):
        pieces.append(masked)
        if index + 1 < len(protected):
            pieces.append(f"\nZXQSEP{index:04d}QXZ\n")
    joined = "".join(pieces)

    try:
        translated_joined = google_request(joined)
        matches = list(BATCH_SEPARATOR_RE.finditer(translated_joined))
        if len(matches) != len(sources) - 1:
            raise BatchValidationError(
                f"separator count mismatch: expected {len(sources) - 1}, found {len(matches)}"
            )
        translated_parts: list[str] = []
        start = 0
        for expected_index, match in enumerate(matches):
            if int(match.group(1)) != expected_index:
                raise BatchValidationError(
                    f"separator order mismatch: expected {expected_index}, got {match.group(1)}"
                )
            translated_parts.append(translated_joined[start:match.start()].strip())
            start = match.end()
        translated_parts.append(translated_joined[start:].strip())
        if len(translated_parts) != len(sources):
            raise BatchValidationError("batch split produced the wrong number of translations")

        result: dict[str, str] = {}
        for source, translated, (_, tokens) in zip(sources, translated_parts, protected):
            translated = restore_google_tokens(translated, tokens)
            if base.placeholder_signature(source) != base.placeholder_signature(translated):
                raise BatchValidationError(f"placeholder mismatch: {source!r} -> {translated!r}")
            if not translated.strip():
                raise BatchValidationError(f"empty batch translation for {source!r}")
            result[source] = translated
        return result
    except BatchValidationError as exc:
        midpoint = len(sources) // 2
        print(f"Batch validation split ({len(sources)} strings): {exc}", flush=True)
        result = google_translate_batch(sources[:midpoint])
        result.update(google_translate_batch(sources[midpoint:]))
        return result


def make_batches(sources: list[str], max_items: int = 20, max_chars: int = 2500) -> list[list[str]]:
    batches: list[list[str]] = []
    current: list[str] = []
    current_chars = 0
    for source in sources:
        source_chars = len(source)
        separator_cost = 20 if current else 0
        if current and (len(current) >= max_items or current_chars + separator_cost + source_chars > max_chars):
            batches.append(current)
            current = []
            current_chars = 0
        current.append(source)
        current_chars += separator_cost + source_chars
    if current:
        batches.append(current)
    return batches


def build_sources() -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, dict[str, str]]]:
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
    return common_en, delta_121_en, delta_261_en, delta_262_en, addons_en


def main() -> None:
    before_files = sorted(ASSETS.glob("**/lang/haw_us.json"))
    if len(before_files) != 29:
        raise SystemExit(f"Expected 29 Hawaiian files before refinement, found {len(before_files)}")
    before = {path: read_json(path) for path in before_files}

    common_en, delta_121_en, delta_261_en, delta_262_en, addons_en = build_sources()
    print(
        f"NeoOrigins Hawaiian source split: common={len(common_en)}, "
        f"1.21.1={len(delta_121_en)}, 26.1={len(delta_261_en)}, 26.2={len(delta_262_en)}",
        flush=True,
    )

    exact = base.build_corpus_map()
    print(
        f"Hawaiian refinement policy: {len(exact)} exact Minecraft corpus strings take priority; "
        "isolated-word projection is disabled; remaining strings use direct en->haw translation.",
        flush=True,
    )

    source_payloads: list[dict[str, str]] = [common_en, delta_121_en, delta_261_en, delta_262_en]
    source_payloads.extend(addons_en.values())
    unique_sources = sorted({str(value) for payload in source_payloads for value in payload.values()})

    translated_by_source: dict[str, str] = {}
    network_sources: list[str] = []
    for source in unique_sources:
        if source in base.MANUAL_VALUES:
            translated_by_source[source] = base.MANUAL_VALUES[source]
        elif source in exact:
            translated_by_source[source] = exact[source]
        else:
            network_sources.append(source)

    cache = load_cache()
    cache_hits = 0
    for source in network_sources:
        cached = cache.get(source)
        if cached is not None:
            translated_by_source[source] = cached
            cache_hits += 1

    missing_network_sources = [source for source in network_sources if source not in translated_by_source]
    batches = make_batches(missing_network_sources)
    print(
        f"Hawaiian translation pool: {len(unique_sources)} unique strings; "
        f"{len(unique_sources) - len(network_sources)} corpus/manual hits; "
        f"{cache_hits} checkpoint hits; {len(missing_network_sources)} direct translations "
        f"in {len(batches)} serialized validated web batches.",
        flush=True,
    )

    completed_strings = cache_hits
    for batch_index, batch in enumerate(batches, start=1):
        translated_batch = google_translate_batch(batch)
        translated_by_source.update(translated_batch)
        cache.update(translated_batch)
        save_cache(cache)
        completed_strings += len(batch)
        if batch_index % 10 == 0 or batch_index == len(batches):
            print(
                f"Direct Hawaiian translation progress: {completed_strings}/{len(network_sources)} strings "
                f"({batch_index}/{len(batches)} new batches)",
                flush=True,
            )

    def translated_payload(source: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, raw_value in source.items():
            value = str(raw_value)
            translated = translated_by_source[value]
            if base.placeholder_signature(value) != base.placeholder_signature(translated):
                raise SystemExit(f"Placeholder mismatch for {key}: {value!r} -> {translated!r}")
            result[key] = translated
        return result

    common_haw = translated_payload(common_en)
    delta_121_haw = translated_payload(delta_121_en)
    delta_261_haw = translated_payload(delta_261_en)
    delta_262_haw = translated_payload(delta_262_en)

    for path in ASSETS.glob("neoorigins_haw_common_*/lang/haw_us.json"):
        path.unlink()
    common_items = list(common_haw.items())
    for index in range((len(common_items) + 149) // 150):
        write_json(
            ASSETS / f"neoorigins_haw_common_{index + 1:02d}/lang/haw_us.json",
            dict(common_items[index * 150:(index + 1) * 150]),
        )
    write_json(ASSETS / "neoorigins_haw_121/lang/haw_us.json", delta_121_haw)
    write_json(ASSETS / "neoorigins_26_1/lang/haw_us.json", delta_261_haw)
    write_json(ASSETS / "neoorigins_26_2/lang/haw_us.json", delta_262_haw)
    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/haw_us.json", translated_payload(english))

    after_files = sorted(ASSETS.glob("**/lang/haw_us.json"))
    if len(after_files) != 29:
        raise SystemExit(f"Expected 29 Hawaiian files after refinement, found {len(after_files)}")
    after = {path: read_json(path) for path in after_files}

    changed_values = 0
    total_values = 0
    source_changed = 0
    seen: dict[str, str] = {}
    for path, new_data in after.items():
        old_data = before[path]
        if set(old_data) != set(new_data):
            raise SystemExit(f"Key set changed unexpectedly during Hawaiian refinement: {path}")
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
    if "__HAWAIIAN_BATCH_LOCK__" in text or "ZXQSEP" in text or "ZXQTK" in text:
        raise SystemExit("Temporary Hawaiian translation marker survived generated output")
    if any(0xE000 <= ord(char) <= 0xF8FF for char in text):
        raise SystemExit("Private-use placeholder marker survived Hawaiian generated output")
    if source_changed < 2500:
        raise SystemExit(
            f"Too many English source values survived full Hawaiian translation: only {source_changed} values changed"
        )
    if seen.get("key.categories.originsmodernui") != "Origin Architect":
        raise SystemExit("Technical project name Origin Architect was not preserved")

    print(
        f"Hawaiian full refinement passed: checked {total_values} values across 29 files; "
        f"changed {changed_values} bootstrap values; source translations changed {source_changed} values; "
        "0 temporary markers and no isolated-word projection pipeline.",
        flush=True,
    )


if __name__ == "__main__":
    main()
