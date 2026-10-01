#!/usr/bin/env python3
"""Generate Bavarian fallback localization from the project's German coverage.

Bavarian is not treated as a generic German regional duplicate here: Minecraft ships
an independent `bar` locale with substantial dialect wording.  This bootstrap uses
our already-complete German localization as the semantic source, then projects it
into Minecraft-style Bavarian with a pinned 8k+ sentence de_de/bar parallel corpus.
The result is a deterministic bootstrap, not a native-speaker review.
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
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿẞ]+(?:[-'’][A-Za-zÀ-ÖØ-öø-ÿẞ]+)*")

MC_LOCALES_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_LOCALES_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_LOCALES_REF}/java"
NEO_BASE = "https://raw.githubusercontent.com/CyberDay1/NeoOrigins/{ref}/src/main/resources/assets/neoorigins/lang/{locale}.json"
NEO_REFS = {
    "mc-1.21.1": "af467a3bc118f6bbc0970d68f7e03fa631d7e6f2",
    "mc-26.1": "aa207ef14cf3b938e28b4081162701953957c1d5",
    "mc-26.2": "511cadcafe3027d2a56b4448652ec9b74e2f3b07",
}

# High-confidence dialect forms visible throughout Minecraft's own Bavarian locale.
# The learned corpus dictionary handles most vocabulary; these guarantee common
# function words and UI wording do not stay mechanically Standard German.
MANUAL_WORDS = {
    "nicht": "ned",
    "ist": "is",
    "sind": "san",
    "kann": "ko",
    "kannst": "kost",
    "können": "kenna",
    "ein": "a",
    "eine": "a",
    "einen": "an",
    "einem": "am",
    "einer": "ana",
    "oder": "oda",
    "mit": "mid",
    "von": "vo",
    "auf": "af",
    "für": "fia",
    "über": "üba",
    "unter": "unta",
    "dich": "di",
    "dir": "da",
    "dein": "dei",
    "deiner": "deina",
    "deinem": "deim",
    "deinen": "dein",
    "diesem": "diesm",
    "dieser": "dera",
    "dieses": "des",
    "immer": "imma",
    "auch": "a",
    "schon": "scho",
    "noch": "no",
    "zurück": "zruck",
    "ausgabe": "Asgobe",
    "eingeben": "oangebn",
    "auslösen": "Aslösn",
    "wiederholen": "Wiederholn",
    "der": "da",
    "die": "de",
    "das": "as",
    "aus": "as",
    "durch": "duach",
    "wird": "wiad",
    "werden": "wern",
    "alle": "olle",
    "mehr": "meah",
    "weniger": "weniga",
    "klein": "kloan",
}

# Context-sensitive project vocabulary.  Keep canonical product/technical names
# where translating them would reduce recognisability.
MANUAL_VALUES = {
    "Ursprung": "Uasprung",
    "Wähle deinen Ursprung": "Wähl dein Uasprung",
    "Wähle deine Klasse": "Wähl dei Klass",
    "Ursprünge durchsuchen": "Uasprüng durchsua",
    "Kräfte": "Kräfd",
    "Fähigkeit": "Fähigkeit",
    "Klasse": "Klass",
    "Zufällig": "Zufällig",
    "Bestätigen >": "Bestätign >",
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Bavarian-Bootstrap"})
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
    de = fetch_json(f"{MC_LOCALES_BASE}/de_de.json")
    bar = fetch_json(f"{MC_LOCALES_BASE}/bar.json")
    shared = sorted(set(de) & set(bar))
    exact = {}
    votes: dict[str, Counter[str]] = defaultdict(Counter)

    for key in shared:
        source = str(de[key])
        target = str(bar[key])
        if source != target:
            exact[source] = target
        src_words = WORD_RE.findall(source)
        dst_words = WORD_RE.findall(target)
        # Conservative positional alignment: Bavarian and German are close enough
        # that equal-length token sequences yield useful, high-precision mappings.
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
        # Prefer repeated evidence, but also admit one-off morphological spellings
        # when the aligned German/Bavarian tokens are strongly orthographically
        # related.  These pairs still come exclusively from Minecraft's official
        # de_de/bar parallel corpus.
        similarity = SequenceMatcher(None, source, target).ratio()
        plausible = len(target) >= 3 and similarity >= 0.45
        if plausible and (
            (top >= 2 and share >= 0.60)
            or (top >= 5 and share >= 0.50)
            or (top == 1 and total == 1 and len(source) >= 4 and similarity >= 0.55)
        ):
            learned[source] = target

    destructive = {s: t for s, t in learned.items() if len(s) >= 5 and len(t) <= 2}
    if destructive:
        raise RuntimeError(f"Destructive learned Bavarian mappings detected: {destructive}")

    # Explicit Minecraft-observed/manual forms win over the statistical dictionary.
    learned.update(MANUAL_WORDS)
    print(
        f"Minecraft Bavarian corpus: {len(shared)} aligned entries, "
        f"{len(exact)} exact dialect strings, {len(learned)} learned word mappings"
    )
    return exact, learned


def bavarianize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
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
        raise RuntimeError(f"Bavarian placeholder mismatch: {text!r} -> {result!r}")
    return result


def collect_local_german() -> dict[str, str]:
    merged = {}
    for path in sorted(ASSETS.glob("**/lang/de_de.json")):
        for key, value in read_json(path).items():
            merged.setdefault(key, value)
    print(f"Local German fallback pool: {len(merged)} distinct keys")
    return merged


def neo_german(ref: str, english: dict[str, str], local_german: dict[str, str]) -> dict[str, str]:
    official = fetch_json(NEO_BASE.format(ref=ref, locale="de_de"))
    merged = dict(official)
    for key, value in local_german.items():
        merged.setdefault(key, value)
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(f"German NeoOrigins semantic source incomplete at {ref}: {len(missing)} missing, sample={missing[:20]}")
    return {key: merged[key] for key in english}


def addon_german(namespace: str, english: dict[str, str], local_german: dict[str, str]) -> dict[str, str]:
    direct = ASSETS / namespace / "lang/de_de.json"
    merged = dict(local_german)
    if direct.exists():
        merged.update(read_json(direct))
    missing = sorted(set(english) - set(merged))
    if missing:
        raise RuntimeError(f"German source incomplete for {namespace}: {len(missing)} missing, sample={missing[:20]}")
    return {key: merged[key] for key in english}


def translated_payload(german: dict[str, str], exact, learned):
    return {key: bavarianize(value, exact, learned) for key, value in german.items()}


def main():
    neo_121_en = read_json(ROOT / "build/bar-discovery-mc-1.21.1/bar_missing_en.json")
    neo_261_en = read_json(ROOT / "build/bar-discovery-mc-26.1/bar_missing_en.json")
    neo_262_en = read_json(ROOT / "build/bar-discovery-mc-26.2/bar_missing_en.json")

    common_en = {
        key: value for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}
    print(
        f"NeoOrigins Bavarian split: common={len(common_en)}, "
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
        key: value for key, value in addons_en["origins_backgrounds_two"].items() if key not in shared_background_keys
    }
    addons_en["origins_backgrounds_iss"] = {
        key: value for key, value in addons_en["origins_backgrounds_iss"].items() if key not in shared_background_keys
    }

    local_german = collect_local_german()
    exact, learned = build_corpus_maps()

    german_121 = neo_german(NEO_REFS["mc-1.21.1"], neo_121_en, local_german)
    german_261 = neo_german(NEO_REFS["mc-26.1"], neo_261_en, local_german)
    german_262 = neo_german(NEO_REFS["mc-26.2"], neo_262_en, local_german)

    # German semantics are target-specific; common values should nevertheless
    # agree for all common English keys. Prefer 1.21.1 and report disagreements.
    disagreements = [
        key for key in common_en
        if german_121.get(key) != german_261.get(key) or german_121.get(key) != german_262.get(key)
    ]
    print(f"Common German target disagreements: {len(disagreements)}")
    common_de = {key: german_121[key] for key in common_en}
    delta_121_de = {key: german_121[key] for key in delta_121_en}
    delta_261_de = {key: german_261[key] for key in delta_261_en}
    delta_262_de = {key: german_262[key] for key in delta_262_en}

    common_bar = translated_payload(common_de, exact, learned)
    delta_121_bar = translated_payload(delta_121_de, exact, learned)
    delta_261_bar = translated_payload(delta_261_de, exact, learned)
    delta_262_bar = translated_payload(delta_262_de, exact, learned)

    common_items = list(common_bar.items())
    chunk_size = 150
    common_chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(common_chunks):
        write_json(
            ASSETS / f"neoorigins_bar_common_{index + 1:02d}/lang/bar.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_bar_121/lang/bar.json", delta_121_bar)
    write_json(ASSETS / "neoorigins_26_1/lang/bar.json", delta_261_bar)
    write_json(ASSETS / "neoorigins_26_2/lang/bar.json", delta_262_bar)

    addon_total = 0
    for namespace, english in addons_en.items():
        german = addon_german(namespace, english, local_german)
        output = translated_payload(german, exact, learned)
        write_json(ASSETS / namespace / "lang/bar.json", output)
        addon_total += len(output)

    files = sorted(ASSETS.glob("**/lang/bar.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Bavarian files after bootstrap, found {len(files)}")

    values = [str(value) for path in files for value in read_json(path).values()]
    de_values = [*common_de.values(), *delta_121_de.values(), *delta_261_de.values(), *delta_262_de.values()]
    changed_neo = sum(
        bavarianize(value, exact, learned) != value
        for value in de_values
    )
    text = "\n".join(values).casefold()
    markers = len(re.findall(r"\b(?:ned|san|ko|kenna|oda|mid|vo|af|fia|üba|unta|imma|scho|no|zruck|oangebn|ois|doaf|viech|schiaß)\b", text))
    print(
        f"Generated Bavarian locale: {len(files)} files; NeoOrigins changed-vs-German "
        f"{changed_neo}/{len(de_values)}; Bavarian lexical markers={markers}; add-on strings={addon_total}"
    )
    if changed_neo < int(len(de_values) * 0.35):
        raise RuntimeError(f"Bavarianization too weak: only {changed_neo}/{len(de_values)} NeoOrigins strings changed")
    if markers < 300:
        raise RuntimeError(f"Bavarian lexical marker sanity too low: {markers}")


if __name__ == "__main__":
    main()
