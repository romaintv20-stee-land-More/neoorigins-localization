#!/usr/bin/env python3
"""Generate Gallo (`go_fr`) fallback localization.

The semantic source is the project's complete French coverage, with official NeoOrigins
French translations taking precedence. Gallo projection is learned from the pinned
Minecraft Java `fr_fr` <-> `go_fr` parallel corpus. Suspicious, untranslated,
placeholder-breaking and non-Latin corpus pairs are rejected. This is deterministic
bootstrap assistance, not native-speaker review.
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
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿẞ]+(?:[-'’`][A-Za-zÀ-ÖØ-öø-ÿẞ]+)*")
GALLO_MARKER_RE = re.compile(
    r"\b(?:servouer|pouint|eune|qheuqe|blloqe|blloqes|vilaije|vilaijouéz|deûz|asteure|"
    r"qhi|qe|ao|châqe|mettr|terouer|qeriature|qeriatures|alivë|alivës|dezalivë|"
    r"bouéte|comande|ghiments|valants|dizou|aperchantivitë|qheur|cië|haot|bâs|"
    r"bergolin|bergolins|flleche|cllë|uzinouer|uzinouers|miriaodéz|qemercer)\b",
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

# Do not invent dialect spellings here. Repeated corpus evidence is the only lexical
# projector; this table exists so future explicit high-confidence forms can be pinned.
MANUAL_WORDS: dict[str, str] = {}
MANUAL_VALUES = {"Origin Architect": "Origin Architect"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Gallo-Bootstrap"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def fetch_optional_json(url: str):
    try:
        return fetch_json(url)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {}
        raise


def placeholder_signature(text: str):
    return sorted(PLACEHOLDER_RE.findall(text))


def preserve_case(source: str, target: str) -> str:
    if source.isupper():
        return target.upper()
    if source[:1].isupper() and target:
        return target[:1].upper() + target[1:]
    return target


def protect(text: str):
    tokens: list[str] = []

    def repl(match):
        token = f"ZXQTK{len(tokens):04d}QXZ"
        tokens.append(match.group(0))
        return token

    return TOKEN_RE.sub(repl, text), tokens


def restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        text = text.replace(f"ZXQTK{index:04d}QXZ", token)
    return text


def unsupported_script(text: str) -> bool:
    for char in text:
        if not char.isalpha():
            continue
        if char.isascii() or "À" <= char <= "ÿ" or char == "ẞ":
            continue
        return True
    return False


def safe_pair(source: str, target: str, english: str | None) -> bool:
    if not source.strip() or not target.strip() or unsupported_script(target):
        return False
    if placeholder_signature(source) != placeholder_signature(target):
        return False
    if english is not None and target == english and source != target:
        return False
    if source == target:
        return True
    similarity = SequenceMatcher(None, source.casefold(), target.casefold()).ratio()
    return similarity >= 0.20 or bool(GALLO_MARKER_RE.search(target))


def isolated_word_replacements(source: str, target: str):
    src_words = WORD_RE.findall(source)
    dst_words = WORD_RE.findall(target)
    if not src_words or not dst_words or len(src_words) > 50 or len(dst_words) > 50:
        return []
    matcher = SequenceMatcher(None, [w.casefold() for w in src_words], [w.casefold() for w in dst_words])
    pairs = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "replace" or i2 - i1 != 1 or j2 - j1 != 1:
            continue
        src = src_words[i1].casefold()
        dst = dst_words[j1].casefold()
        if src != dst:
            pairs.append((src, dst))
    return pairs


def build_corpus_maps():
    french = fetch_json(f"{MC_LOCALES_BASE}/fr_fr.json")
    gallo = fetch_json(f"{MC_LOCALES_BASE}/go_fr.json")
    english = fetch_json(f"{MC_LOCALES_BASE}/en_us.json")
    shared = sorted(set(french) & set(gallo))
    exact: dict[str, str] = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    unchanged = 0

    for key in shared:
        source = str(french[key])
        target = str(gallo[key])
        en_value = str(english[key]) if key in english else None
        if not safe_pair(source, target, en_value):
            rejected += 1
            continue
        if source == target:
            unchanged += 1
            continue
        exact[source] = target
        for src, dst in isolated_word_replacements(source, target):
            votes[src][dst] += 1

    learned: dict[str, str] = {}
    for source, counter in votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        share = top / total
        similarity = SequenceMatcher(None, source, target).ratio()
        if len(target) >= 2 and similarity >= 0.22 and (
            (top >= 3 and share >= 0.82)
            or (top >= 7 and share >= 0.70)
        ):
            learned[source] = target

    destructive = {
        source: target
        for source, target in learned.items()
        if len(source) >= 5 and (len(target) <= 1 or SequenceMatcher(None, source, target).ratio() < 0.16)
    }
    if destructive:
        raise RuntimeError(f"Destructive Gallo mappings detected: {destructive}")

    learned.update(MANUAL_WORDS)
    print(
        f"Minecraft Gallo corpus: {len(shared)} aligned entries, "
        f"{rejected} rejected suspicious/untranslated pairs, {unchanged} unchanged pairs, "
        f"{len(exact)} exact Gallo strings, {len(learned)} learned word mappings"
    )
    return exact, learned


def galloize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
    if text in MANUAL_VALUES:
        return MANUAL_VALUES[text]
    if text in exact:
        result = exact[text]
        if placeholder_signature(text) != placeholder_signature(result):
            raise RuntimeError(f"Exact-map placeholder mismatch: {text!r} -> {result!r}")
        return result

    masked, tokens = protect(text)

    def replace_word(match):
        word = match.group(0)
        mapped = learned.get(word.casefold())
        return preserve_case(word, mapped) if mapped is not None else word

    result = WORD_RE.sub(replace_word, masked)
    result = restore(result, tokens)
    if placeholder_signature(text) != placeholder_signature(result):
        raise RuntimeError(f"Gallo placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_french() -> dict[str, str]:
    merged: dict[str, str] = {}
    files = sorted(ASSETS.glob("**/lang/fr_fr.json"))
    for path in files:
        for key, value in read_json(path).items():
            merged.setdefault(key, value)
    print(f"Local French fallback pool: {len(merged)} distinct keys from {len(files)} files")
    return merged


def neo_french(ref: str, english: dict[str, str], local_french: dict[str, str]) -> dict[str, str]:
    official = fetch_optional_json(NEO_BASE.format(ref=ref, locale="fr_fr"))
    merged = dict(official)
    for key, value in local_french.items():
        merged.setdefault(key, value)
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"French NeoOrigins semantic source incomplete at {ref}: {len(missing)} missing, sample={missing[:20]}"
        )
    print(f"French semantic source {ref}: official={len(official)}, merged={len(merged)}")
    return {key: str(merged[key]) for key in english}


def addon_french(namespace: str, english: dict[str, str], local_french: dict[str, str]) -> dict[str, str]:
    merged = dict(local_french)
    direct = ASSETS / namespace / "lang/fr_fr.json"
    if direct.exists():
        merged.update(read_json(direct))
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(f"French source incomplete for {namespace}: {len(missing)} missing, sample={missing[:20]}")
    return {key: str(merged[key]) for key in english}


def translated_payload(source: dict[str, str], exact, learned):
    return {key: galloize(value, exact, learned) for key, value in source.items()}


def main():
    neo_121_en = read_json(ROOT / "build/go-discovery-mc-1.21.1/go_fr_missing_en.json")
    neo_261_en = read_json(ROOT / "build/go-discovery-mc-26.1/go_fr_missing_en.json")
    neo_262_en = read_json(ROOT / "build/go-discovery-mc-26.2/go_fr_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins Gallo split: common={len(common_en)}, "
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

    local_french = collect_local_french()
    exact, learned = build_corpus_maps()
    fr_121 = neo_french(NEO_REFS["mc-1.21.1"], neo_121_en, local_french)
    fr_261 = neo_french(NEO_REFS["mc-26.1"], neo_261_en, local_french)
    fr_262 = neo_french(NEO_REFS["mc-26.2"], neo_262_en, local_french)

    disagreements = [
        key for key in common_en
        if fr_121.get(key) != fr_261.get(key) or fr_121.get(key) != fr_262.get(key)
    ]
    print(f"Common French target disagreements: {len(disagreements)}")

    common_go = translated_payload({k: fr_121[k] for k in common_en}, exact, learned)
    delta_121_go = translated_payload({k: fr_121[k] for k in delta_121_en}, exact, learned)
    delta_261_go = translated_payload({k: fr_261[k] for k in delta_261_en}, exact, learned)
    delta_262_go = translated_payload({k: fr_262[k] for k in delta_262_en}, exact, learned)

    for path in ASSETS.glob("neoorigins_go_common_*/lang/go_fr.json"):
        path.unlink()

    common_items = list(common_go.items())
    chunk_size = 150
    chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(chunks):
        write_json(
            ASSETS / f"neoorigins_go_common_{index + 1:02d}/lang/go_fr.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_go_121/lang/go_fr.json", delta_121_go)
    write_json(ASSETS / "neoorigins_26_1/lang/go_fr.json", delta_261_go)
    write_json(ASSETS / "neoorigins_26_2/lang/go_fr.json", delta_262_go)

    for namespace, english in addons_en.items():
        french = addon_french(namespace, english, local_french)
        write_json(ASSETS / namespace / "lang/go_fr.json", translated_payload(french, exact, learned))

    files = sorted(ASSETS.glob("**/lang/go_fr.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Gallo files after generation, found {len(files)}")

    all_values = [str(v) for path in files for v in read_json(path).values()]
    marker_count = sum(len(GALLO_MARKER_RE.findall(value)) for value in all_values)
    marked_values = sum(1 for value in all_values if GALLO_MARKER_RE.search(value))
    if marker_count < 150 or marked_values < 120:
        raise RuntimeError(f"Gallo differentiation too weak: markers={marker_count}, marked_values={marked_values}")
    if any(unsupported_script(value) for value in all_values):
        raise RuntimeError("Unexpected non-Latin script found in Gallo output")
    print(
        f"Gallo bootstrap generated {len(files)} files; "
        f"dialect markers={marker_count}, marked values={marked_values}"
    )


if __name__ == "__main__":
    main()
