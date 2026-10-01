#!/usr/bin/env python3
"""Generate Manx (`gv_im`) fallback localization.

English remains the semantic source. Manx replacements come only from the pinned
Minecraft Java `en_us` <-> `gv_im` parallel corpus, plus explicitly protected values.
Whole-string corpus translations are preferred; reusable single-word mappings require
repeated, dominant corpus evidence. This is deterministic bootstrap assistance, not
native-speaker review.
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
TOKEN_RE = re.compile(r"%(?:\d+\$)?[sdif]|§.|\\n|\{[^{}]+\}|<[^<>]+>")
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")
WORD_RE = re.compile(r"[^\W\d_]+(?:[-'’`][^\W\d_]+)*", re.UNICODE)
MANX_MARKER_RE = re.compile(
    r"\b(?:yn|ny|ta|cha|nel|jeant|erash|scryssey|seose|sheese|dagh|ennym|"
    r"tendeilagh|sarey|cloieder|slaynt|bieauid|keyll|faarkey|dorrys|cleigh|"
    r"fuygh|seihll|ushtey|aile|reaghey|sauail|croo|reih|crootagh|mayrnaght|"
    r"cadjin|follit|aachroo|kiangil|cretooryn|cooid|bundeilyn|kishtey|lioar|"
    r"ollan|baatey|side|mod|gyn|lesh|da|dy|jeh|ass)\b",
    re.IGNORECASE,
)

MC_LOCALES_REF = "83af272f5a618b287781ee9ce2a48cfc8f47dd61"
MC_LOCALES_BASE = f"https://raw.githubusercontent.com/teaSummer/minecraft-locales/{MC_LOCALES_REF}/java"

# These are exact, high-visibility values observed directly in the pinned Manx corpus.
# Keep technical/proper project names unchanged rather than inventing a Manx form.
MANUAL_VALUES = {
    "Origin Architect": "Origin Architect",
    "Back": "Erash",
    "Cancel": "Scryssey",
    "Done": "Jeant",
    "Edit": "Reaghey",
    "Save": "Sauail",
    "Yes": "Ta",
    "No": "Cha Nel",
    "Up": "Seose",
    "Down": "Sheese",
    "All": "Dagh",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "NeoOrigins-Manx-Bootstrap"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


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
    # Unchanged English strings are useful neither as a translation nor as a lexical vote.
    if source.casefold() == target.casefold():
        return False
    return True


def build_corpus_maps():
    english = fetch_json(f"{MC_LOCALES_BASE}/en_us.json")
    manx = fetch_json(f"{MC_LOCALES_BASE}/gv_im.json")
    shared = sorted(set(english) & set(manx))

    exact_votes: dict[str, Counter[str]] = defaultdict(Counter)
    word_votes: dict[str, Counter[str]] = defaultdict(Counter)
    rejected = 0
    unchanged = 0

    for key in shared:
        source = str(english[key])
        target = str(manx[key])
        if source.casefold() == target.casefold():
            unchanged += 1
            continue
        if not safe_pair(source, target):
            rejected += 1
            continue

        exact_votes[source][target] += 1

        src_words = WORD_RE.findall(source)
        dst_words = WORD_RE.findall(target)
        if len(src_words) == 1 and len(dst_words) == 1:
            src = src_words[0].casefold()
            dst = dst_words[0].casefold()
            if len(src) >= 2 and len(dst) >= 2 and src != dst:
                word_votes[src][dst] += 1

    exact: dict[str, str] = {}
    ambiguous_exact = 0
    for source, counter in exact_votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        if top / total >= 0.80:
            exact[source] = target
        else:
            ambiguous_exact += 1

    learned: dict[str, str] = {}
    for source, counter in word_votes.items():
        target, top = counter.most_common(1)[0]
        total = sum(counter.values())
        # Reusing an isolated word inside a larger sentence is riskier than an exact
        # full-string match, so require repeated and nearly unanimous evidence.
        if top >= 2 and top / total >= 0.90:
            learned[source] = target

    print(
        f"Minecraft Manx corpus: {len(shared)} aligned entries, "
        f"{rejected} rejected pairs, {unchanged} unchanged English pairs, "
        f"{len(exact)} exact Manx strings, {ambiguous_exact} ambiguous exact sources, "
        f"{len(learned)} reusable word mappings"
    )
    return exact, learned


def manxize(text: str, exact: dict[str, str], learned: dict[str, str]) -> str:
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
        raise RuntimeError(f"Manx placeholder mismatch: {text!r} -> {result!r}")
    return result


def translated_payload(source: dict[str, str], exact, learned):
    return {key: manxize(str(value), exact, learned) for key, value in source.items()}


def main():
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
    print(
        f"NeoOrigins Manx split: common={len(common_en)}, "
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

    exact, learned = build_corpus_maps()

    common_gv = translated_payload(common_en, exact, learned)
    delta_121_gv = translated_payload(delta_121_en, exact, learned)
    delta_261_gv = translated_payload(delta_261_en, exact, learned)
    delta_262_gv = translated_payload(delta_262_en, exact, learned)

    for path in ASSETS.glob("neoorigins_gv_common_*/lang/gv_im.json"):
        path.unlink()

    common_items = list(common_gv.items())
    chunk_size = 150
    chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(chunks):
        write_json(
            ASSETS / f"neoorigins_gv_common_{index + 1:02d}/lang/gv_im.json",
            dict(common_items[index * chunk_size:(index + 1) * chunk_size]),
        )
    write_json(ASSETS / "neoorigins_gv_121/lang/gv_im.json", delta_121_gv)
    write_json(ASSETS / "neoorigins_26_1/lang/gv_im.json", delta_261_gv)
    write_json(ASSETS / "neoorigins_26_2/lang/gv_im.json", delta_262_gv)

    for namespace, english in addons_en.items():
        write_json(ASSETS / namespace / "lang/gv_im.json", translated_payload(english, exact, learned))

    files = sorted(ASSETS.glob("**/lang/gv_im.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 Manx files after generation, found {len(files)}")

    all_values = [str(v) for path in files for v in read_json(path).values()]
    marker_count = sum(len(MANX_MARKER_RE.findall(value)) for value in all_values)
    marked_values = sum(1 for value in all_values if MANX_MARKER_RE.search(value))
    if marker_count < 25 or marked_values < 20:
        raise RuntimeError(
            f"Manx differentiation unexpectedly weak: markers={marker_count}, marked_values={marked_values}"
        )
    if any(unsupported_script(value) for value in all_values):
        raise RuntimeError("Unexpected non-Latin script found in Manx output")

    print(
        f"Manx bootstrap generated {len(files)} files; "
        f"Manx markers={marker_count}, marked values={marked_values}"
    )


if __name__ == "__main__":
    main()
