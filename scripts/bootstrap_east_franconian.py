#!/usr/bin/env python3
"""Generate East Franconian (`fra_de`) fallback localization.

The semantic source is the project's complete German coverage, with official NeoOrigins
German translations taking precedence when they exist. Dialect projection is learned
from the pinned Minecraft Java `de_de` <-> `fra_de` parallel corpus. Only safe exact
pairs and isolated one-word replacements are learned. This is a deterministic bootstrap,
not a native-speaker review.
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
DIALECT_MARKER_RE = re.compile(
    r"\b(?:ned|san|nua|vo|Seava|Bfehl|Monsda|Ealech|Enddeck|gsetzd|gmeißeldn|Doaf|Weld|Greadua)\b",
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

# High-confidence forms visible repeatedly in Minecraft's East Franconian locale.
# Statistical mappings remain the primary source; these only provide conservative
# coverage for very common grammar words when isolated-diff evidence is sparse.
MANUAL_WORDS = {
    "nicht": "ned",
    "sind": "san",
    "nur": "nua",
    "von": "vo",
    "server": "seava",
    "befehl": "bfehl",
    "monster": "monsda",
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
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-East-Franconian-Bootstrap"})
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
    # The community fra_de file contains some newer entries still in English.
    # Never use an untranslated English target to teach the dialect projector.
    if english is not None and target == english and source != target:
        return False
    if source == target:
        return True
    similarity = SequenceMatcher(None, source.casefold(), target.casefold()).ratio()
    return similarity >= 0.24 or bool(DIALECT_MARKER_RE.search(target))


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
    de = fetch_json(f"{MC_LOCALES_BASE}/de_de.json")
    fra = fetch_json(f"{MC_LOCALES_BASE}/fra_de.json")
    en = fetch_json(f"{MC_LOCALES_BASE}/en_us.json")
    shared = sorted(set(de) & set(fra))
    exact: dict[str, str] = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    unchanged = 0

    for key in shared:
        source = str(de[key])
        target = str(fra[key])
        english = str(en[key]) if key in en else None
        if not safe_pair(source, target, english):
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
        # East Franconian remains closely related to German. Repeated, dominant,
        # reasonably similar replacements are safe enough for a bootstrap.
        if len(target) >= 2 and similarity >= 0.30 and (
            (top >= 2 and share >= 0.72)
            or (top >= 5 and share >= 0.60)
        ):
            learned[source] = target

    destructive = {s: t for s, t in learned.items() if len(s) >= 5 and len(t) <= 1}
    if destructive:
        raise RuntimeError(f"Destructive East Franconian mappings detected: {destructive}")

    learned.update(MANUAL_WORDS)
    print(
        f"Minecraft East Franconian corpus: {len(shared)} aligned entries, "
        f"{rejected} rejected suspicious/untranslated pairs, {unchanged} unchanged pairs, "
        f"{len(exact)} exact dialect strings, {len(learned)} learned word mappings"
    )
    return exact, learned


def dialectize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
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
        raise RuntimeError(f"East Franconian placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_german() -> dict[str, str]:
    merged: dict[str, str] = {}
    files = sorted(ASSETS.glob("**/lang/de_de.json"))
    for path in files:
        for key, value in read_json(path).items():
            merged.setdefault(key, value)
    print(f"Local German fallback pool: {len(merged)} distinct keys from {len(files)} files")
    return merged


def neo_german(ref: str, english: dict[str, str], local_german: dict[str, str]) -> dict[str, str]:
    official = fetch_optional_json(NEO_BASE.format(ref=ref, locale="de_de"))
    merged = dict(official)
    for key, value in local_german.items():
        merged.setdefault(key, value)
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(
            f"German NeoOrigins semantic source incomplete at {ref}: {len(missing)} missing, sample={missing[:20]}"
        )
    print(f"German semantic source {ref}: official={len(official)}, merged={len(merged)}")
    return {key: str(merged[key]) for key in english}


def addon_german(namespace: str, english: dict[str, str], local_german: dict[str, str]) -> dict[str, str]:
    merged = dict(local_german)
    direct = ASSETS / namespace / "lang/de_de.json"
    if direct.exists():
        merged.update(read_json(direct))
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(f"German source incomplete for {namespace}: {len(missing)} missing, sample={missing[:20]}")
    return {key: str(merged[key]) for key in english}


def translated_payload(source: dict[str, str], exact, learned):
    return {key: dialectize(value, exact, learned) for key, value in source.items()}


def main():
    neo_121_en = read_json(ROOT / "build/fra-discovery-mc-1.21.1/fra_de_missing_en.json")
    neo_261_en = read_json(ROOT / "build/fra-discovery-mc-26.1/fra_de_missing_en.json")
    neo_262_en = read_json(ROOT / "build/fra-discovery-mc-26.2/fra_de_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins East Franconian split: common={len(common_en)}, "
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

    local_german = collect_local_german()
    exact, learned = build_corpus_maps()
    de_121 = neo_german(NEO_REFS["mc-1.21.1"], neo_121_en, local_german)
    de_261 = neo_german(NEO_REFS["mc-26.1"], neo_261_en, local_german)
    de_262 = neo_german(NEO_REFS["mc-26.2"], neo_262_en, local_german)

    disagreements = [
        key for key in common_en
        if de_121.get(key) != de_261.get(key) or de_121.get(key) != de_262.get(key)
    ]
    print(f"Common German target disagreements: {len(disagreements)}")

    common_fra = translated_payload({k: de_121[k] for k in common_en}, exact, learned)
    delta_121_fra = translated_payload({k: de_121[k] for k in delta_121_en}, exact, learned)
    delta_261_fra = translated_payload({k: de_261[k] for k in delta_261_en}, exact, learned)
    delta_262_fra = translated_payload({k: de_262[k] for k in delta_262_en}, exact, learned)

    # Clean only this locale's generated NeoOrigins namespaces before rewriting.
    for path in ASSETS.glob("neoorigins_fra_common_*/lang/fra_de.json"):
        path.unlink()

    common_items = list(common_fra.items())
    chunk_size = 150
    chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(chunks):
        write_json(
            ASSETS / f"neoorigins_fra_common_{index + 1:02d}/lang/fra_de.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_fra_121/lang/fra_de.json", delta_121_fra)
    write_json(ASSETS / "neoorigins_26_1/lang/fra_de.json", delta_261_fra)
    write_json(ASSETS / "neoorigins_26_2/lang/fra_de.json", delta_262_fra)

    for namespace, english in addons_en.items():
        german = addon_german(namespace, english, local_german)
        write_json(ASSETS / namespace / "lang/fra_de.json", translated_payload(german, exact, learned))

    files = sorted(ASSETS.glob("**/lang/fra_de.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 East Franconian files after generation, found {len(files)}")

    all_values = [str(v) for path in files for v in read_json(path).values()]
    marker_count = sum(len(DIALECT_MARKER_RE.findall(value)) for value in all_values)
    dialect_values = 0
    german_values = []
    for value in de_121.values():
        german_values.append(value)
    # Exact corpus and learned replacements should create substantial differentiation.
    for value in all_values:
        if DIALECT_MARKER_RE.search(value):
            dialect_values += 1
    if marker_count < 100 or dialect_values < 80:
        raise RuntimeError(
            f"East Franconian differentiation too weak: markers={marker_count}, dialect_values={dialect_values}"
        )
    print(
        f"East Franconian bootstrap generated {len(files)} files; "
        f"dialect markers={marker_count}, marked values={dialect_values}"
    )


if __name__ == "__main__":
    main()
