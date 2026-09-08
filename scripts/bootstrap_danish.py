#!/usr/bin/env python3
"""Generate Danish fallback localization from pinned English audit payloads.

The translation cache is kept under build/ so interrupted CI runs can resume within
one job. Official upstream Danish strings are pruned by the audit pass after this
bootstrap; NeoOrigins itself is generated directly from the upstream-missing set.
"""

from pathlib import Path
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
CACHE_PATH = ROOT / "build/danish_translation_cache.json"
TOKEN_RE = re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\{[^{}]+\}|<[^<>]+>")
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
SEPARATOR_RE = re.compile(r"\n?ZXQSEP\d{4}ZXQ\n?")

# Canonical/product names and short UI wording that should not be mangled by a
# generic machine pass. These overrides can be extended after in-game review.
MANUAL_OVERRIDES = {
    "Open Origin Creator": "Åbn Origin-skaberen",
    "Mob Origin Creator": "Mob-Origin-skaber",
    "Split": "Opdel",
    "Elytra Boost": "Elytra-boost",
    "Sonic Boom": "Sonisk brag",
    "Pack Bond": "Flokbånd",
    "Speed Mining": "Hurtig minedrift",
    "Camoflauge": "Camouflage",
    "Pack Boost": "Flok-boost",
    "Max Mana Boost": "Boost til maksimal mana",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Tildel loot-pulje",
    "Rage Counter.": "Raserimåler.",
    "Rage Counter": "Raserimåler",
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def protect(text: str):
    tokens = []

    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"ZXQPH{index:04d}ZXQ"

    return TOKEN_RE.sub(replace, text), tokens


def restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        text = text.replace(f"ZXQPH{index:04d}ZXQ", token)
    return text


def translate_rpc(text: str, attempts: int = 5):
    inner = json.dumps([[text, "en", "da", True], [None]])
    payload = json.dumps([[["MkEWBc", inner, None, "generic"]]])
    data = urllib.parse.urlencode({"f.req": payload}).encode()
    request = urllib.request.Request(
        "https://translate.google.com/_/TranslateWebserverUi/data/batchexecute",
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
    )
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            raw = urllib.request.urlopen(request, timeout=60).read().decode("utf-8")
            outer = json.loads(raw.split("\n", 2)[2])
            parsed = json.loads(outer[0][2])
            segments = parsed[1][0][0][5]
            return "".join(segment[0] for segment in segments)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, TypeError, IndexError) as exc:
            last_error = exc
            if attempt != attempts:
                time.sleep(2 ** (attempt - 1))
    raise RuntimeError(f"Translation failed after {attempts} attempts: {last_error}")


def make_batches(values: list[str], max_chars: int = 3500, max_items: int = 35):
    batches = []
    current = []
    current_size = 0
    for value in values:
        estimated = len(value) + 24
        if current and (current_size + estimated > max_chars or len(current) >= max_items):
            batches.append(current)
            current = []
            current_size = 0
        current.append(value)
        current_size += estimated
    if current:
        batches.append(current)
    return batches


def translate_values(values: list[str]):
    cache = read_json(CACHE_PATH) if CACHE_PATH.exists() else {}
    pending = list(dict.fromkeys(value for value in values if value not in cache))
    batches = make_batches(pending)
    print(f"Danish cache: {len(cache)} entries; {len(pending)} new strings in {len(batches)} batches")

    for batch_number, batch in enumerate(batches, 1):
        protected = []
        token_sets = []
        for value in batch:
            masked, tokens = protect(value)
            protected.append(masked)
            token_sets.append(tokens)
        joined = "".join(
            value if index == 0 else f"\nZXQSEP{index:04d}ZXQ\n{value}"
            for index, value in enumerate(protected)
        )
        translated_joined = translate_rpc(joined)
        translated = SEPARATOR_RE.split(translated_joined)
        if len(translated) != len(batch):
            raise RuntimeError(
                f"Batch {batch_number}: expected {len(batch)} translated strings, received {len(translated)}"
            )
        for source, result, tokens in zip(batch, translated, token_sets):
            result = restore(result, tokens).strip()
            if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):
                raise RuntimeError(f"Placeholder mismatch after translation: {source!r} -> {result!r}")
            cache[source] = result
        write_json(CACHE_PATH, cache)
        print(f"Translated batch {batch_number}/{len(batches)} ({len(cache)} cached strings)")
        time.sleep(0.15)
    return cache


def refine_identical_titles(cache: dict):
    candidates = [
        source
        for source, result in cache.items()
        if source.strip().casefold() == result.strip().casefold()
        and re.search(r"[A-Za-z]", source)
        and not source.isupper()
    ]
    lowered = list(dict.fromkeys(source.lower() for source in candidates))
    if not lowered:
        return cache
    lower_cache = translate_values(lowered)
    cache.update(lower_cache)
    changed = 0
    for source in candidates:
        result = lower_cache[source.lower()]
        if result.casefold() == source.casefold():
            continue
        if source[:1].isupper() and result:
            result = result[:1].upper() + result[1:]
        cache[source] = result
        changed += 1
    write_json(CACHE_PATH, cache)
    print(f"Refined {changed}/{len(candidates)} title-like strings left in English")
    return cache


def main():
    neo_121 = read_json(ROOT / "build/da-discovery-mc-1.21.1/da_dk_missing_en.json")
    neo_261 = read_json(ROOT / "build/da-discovery-mc-26.1/da_dk_missing_en.json")
    neo_262 = read_json(ROOT / "build/da-discovery-mc-26.2/da_dk_missing_en.json")

    common = {
        key: value
        for key, value in neo_121.items()
        if neo_261.get(key) == value and neo_262.get(key) == value
    }
    delta_121 = {key: value for key, value in neo_121.items() if key not in common}
    delta_261 = {key: value for key, value in neo_261.items() if key not in common}
    delta_262 = {key: value for key, value in neo_262.items() if key not in common}

    print(
        "NeoOrigins Danish split: "
        f"common={len(common)}, 1.21.1={len(delta_121)}, 26.1={len(delta_261)}, 26.2={len(delta_262)}"
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
    addons = {namespace: read_json(path) for namespace, path in source_files.items()}
    shared_background_keys = set(addons["origins_backgrounds"])
    addons["origins_backgrounds_two"] = {
        key: value for key, value in addons["origins_backgrounds_two"].items() if key not in shared_background_keys
    }
    addons["origins_backgrounds_iss"] = {
        key: value for key, value in addons["origins_backgrounds_iss"].items() if key not in shared_background_keys
    }

    payloads = [common, delta_121, delta_261, delta_262, *addons.values()]
    cache = translate_values([value for payload in payloads for value in payload.values()])
    cache = refine_identical_titles(cache)
    cache.update(MANUAL_OVERRIDES)
    write_json(CACHE_PATH, cache)

    def translated(payload):
        return {key: cache[value] for key, value in payload.items()}

    common_items = list(common.items())
    chunk_size = 150
    common_chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(common_chunks):
        chunk = dict(common_items[index * chunk_size : (index + 1) * chunk_size])
        write_json(ASSETS / f"neoorigins_da_common_{index + 1:02d}/lang/da_dk.json", translated(chunk))

    write_json(ASSETS / "neoorigins_da_121/lang/da_dk.json", translated(delta_121))
    write_json(ASSETS / "neoorigins_26_1/lang/da_dk.json", translated(delta_261))
    write_json(ASSETS / "neoorigins_26_2/lang/da_dk.json", translated(delta_262))
    for namespace, payload in addons.items():
        write_json(ASSETS / namespace / "lang/da_dk.json", translated(payload))

    print(
        "Generated Danish locale: "
        f"NeoOrigins {len(common)} common + {len(delta_121)}/{len(delta_261)}/{len(delta_262)} deltas; "
        f"add-ons {sum(len(payload) for payload in addons.values())} physical strings"
    )


if __name__ == "__main__":
    main()
