#!/usr/bin/env python3
"""Generate Norwegian Nynorsk fallback localization from validated Bokmål fallbacks.

The project already has a fully audited Norwegian Bokmål locale (no_no). For Nynorsk,
we preserve that Minecraft/domain terminology and convert the prose with Apertium's
purpose-built nob-nno language pair. Any source key unexpectedly missing from the
Bokmål fallback is first translated from English to Bokmål using the existing
bootstrap helper, then converted to Nynorsk.
"""

from pathlib import Path
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
CACHE_PATH = ROOT / "build/nynorsk_translation_cache.json"
TOKEN_RE = re.compile(r"%(?:\d+\$)?[sdif]|§.|\n|\{[^{}]+\}|<[^<>]+>|\\n")
PLACEHOLDER_RE = re.compile(r"%(?:\d+\$)?[sdif]")

# Keep product names / technical tokens untouched while Apertium handles Norwegian prose.
PROTECTED_LITERALS = (
    "Origin Architect", "NeoOrigins", "Minecraft", "Origins", "Origin", "HUD", "JSON",
    "Elytra", "Ultimine", "NeoForge", "Fabric", "Java", "GitHub", "XP",
)

# Canonical short UI/domain wording where a direct, stable Nynorsk form is preferable.
MANUAL_OVERRIDES = {
    "Open Origin Creator": "Opna Origin-opprettaren",
    "Mob Origin Creator": "Mob Origin-opprettar",
    "Split": "Del",
    "Elytra Boost": "Elytra-forsterking",
    "Sonic Boom": "Sonisk drønn",
    "Pack Bond": "Flokkband",
    "Speed Mining": "Rask gruvedrift",
    "Camoflauge": "Kamuflasje",
    "Pack Boost": "Flokkforsterking",
    "Max Mana Boost": "Maks mana-forsterking",
    "NeoOrigins: Grant Loot Pool": "NeoOrigins: Tildel loot-pool",
    "Rage Counter.": "Raserimålar.",
    "Rage Counter": "Raserimålar",
    "Origin Architect": "Origin Architect",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_locale_map(locale: str, namespace_glob: str, extra_namespace: str | None = None):
    result = {}
    for path in sorted(ASSETS.glob(f"{namespace_glob}/lang/{locale}.json")):
        result.update(read_json(path))
    if extra_namespace:
        path = ASSETS / extra_namespace / "lang" / f"{locale}.json"
        if path.exists():
            result.update(read_json(path))
    return result


def protect(text: str):
    tokens = []

    def stash(value: str):
        index = len(tokens)
        tokens.append(value)
        return f"ZXQPH{index:04d}ZXQ"

    for literal in PROTECTED_LITERALS:
        text = text.replace(literal, stash(literal))

    def replace(match):
        return stash(match.group(0))

    return TOKEN_RE.sub(replace, text), tokens


def restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        text = text.replace(f"ZXQPH{index:04d}ZXQ", token)
    return text


def convert_batch(values: list[str]):
    """Convert a batch with one protected value per physical line."""
    if not values:
        return []
    masked_values = []
    token_sets = []
    for value in values:
        masked, tokens = protect(value)
        if "\n" in masked:
            raise RuntimeError(f"Unprotected newline in Apertium input: {value!r}")
        masked_values.append(masked)
        token_sets.append(tokens)

    env = os.environ.copy()
    # Prefer the common "vi" pronoun choice while keeping otherwise standard Nynorsk.
    env.setdefault("AP_SETVAR", "me_vi")
    proc = subprocess.run(
        ["apertium", "-u", "nob-nno"],
        input="\n".join(masked_values) + "\n",
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Apertium failed with {proc.returncode}: {proc.stderr}")
    lines = proc.stdout.splitlines()
    if len(lines) != len(values):
        raise RuntimeError(
            f"Apertium batch line mismatch: expected {len(values)}, got {len(lines)}"
        )

    results = []
    for source, result, tokens in zip(values, lines, token_sets):
        result = restore(result, tokens).strip()
        if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):
            raise RuntimeError(f"Placeholder mismatch after Nynorsk conversion: {source!r} -> {result!r}")
        results.append(result)
    return results


def english_to_bokmal(values: list[str]):
    if not values:
        return {}
    import bootstrap_norwegian
    cache = bootstrap_norwegian.translate_values(values)
    return {value: cache[value] for value in values}


def choose_bokmal(payload_no: dict, key: str, english: str, fallback_bokmal: dict):
    if key in payload_no:
        return payload_no[key]
    return fallback_bokmal[english]


def main():
    neo_121_en = read_json(ROOT / "build/nn-discovery-mc-1.21.1/nn_no_missing_en.json")
    neo_261_en = read_json(ROOT / "build/nn-discovery-mc-26.1/nn_no_missing_en.json")
    neo_262_en = read_json(ROOT / "build/nn-discovery-mc-26.2/nn_no_missing_en.json")

    common_en = {
        key: value
        for key, value in neo_121_en.items()
        if neo_261_en.get(key) == value and neo_262_en.get(key) == value
    }
    delta_121_en = {key: value for key, value in neo_121_en.items() if key not in common_en}
    delta_261_en = {key: value for key, value in neo_261_en.items() if key not in common_en}
    delta_262_en = {key: value for key, value in neo_262_en.items() if key not in common_en}

    print(
        "NeoOrigins Nynorsk split: "
        f"common={len(common_en)}, 1.21.1={len(delta_121_en)}, "
        f"26.1={len(delta_261_en)}, 26.2={len(delta_262_en)}"
    )

    no_common = load_locale_map("no_no", "neoorigins_no_common_*")
    no_121 = dict(no_common)
    no_121.update(load_locale_map("no_no", "__never__", "neoorigins_no_121"))
    no_261 = dict(no_common)
    no_261.update(load_locale_map("no_no", "__never__", "neoorigins_26_1"))
    no_262 = dict(no_common)
    no_262.update(load_locale_map("no_no", "__never__", "neoorigins_26_2"))

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
    addons_no = {
        namespace: read_json(ASSETS / namespace / "lang/no_no.json")
        if (ASSETS / namespace / "lang/no_no.json").exists() else {}
        for namespace in addons_en
    }

    payload_specs = [
        ("common", common_en, no_common),
        ("121", delta_121_en, no_121),
        ("261", delta_261_en, no_261),
        ("262", delta_262_en, no_262),
        *[(namespace, payload, addons_no[namespace]) for namespace, payload in addons_en.items()],
    ]

    missing_bokmal_english = []
    for _name, payload_en, payload_no in payload_specs:
        for key, english in payload_en.items():
            if key not in payload_no:
                missing_bokmal_english.append(english)
    missing_bokmal_english = list(dict.fromkeys(missing_bokmal_english))
    print(f"Bokmål source fallback needed for {len(missing_bokmal_english)} unique strings")
    fallback_bokmal = english_to_bokmal(missing_bokmal_english)

    source_to_nynorsk = read_json(CACHE_PATH) if CACHE_PATH.exists() else {}
    all_bokmal = []
    for _name, payload_en, payload_no in payload_specs:
        for key, english in payload_en.items():
            all_bokmal.append(choose_bokmal(payload_no, key, english, fallback_bokmal))
    unique_bokmal = list(dict.fromkeys(all_bokmal))
    pending = [value for value in unique_bokmal if value not in source_to_nynorsk]
    print(f"Nynorsk cache: {len(source_to_nynorsk)} entries; converting {len(pending)} Bokmål strings")

    batch_size = 400
    for start in range(0, len(pending), batch_size):
        batch = pending[start:start + batch_size]
        results = convert_batch(batch)
        source_to_nynorsk.update(zip(batch, results))
        write_json(CACHE_PATH, source_to_nynorsk)
        print(f"Converted {min(start + len(batch), len(pending))}/{len(pending)} Bokmål strings")

    for english, nynorsk in MANUAL_OVERRIDES.items():
        candidates = []
        for _name, payload_en, payload_no in payload_specs:
            for key, source_en in payload_en.items():
                if source_en == english:
                    if key in payload_no:
                        candidates.append(payload_no[key])
                    elif english in fallback_bokmal:
                        candidates.append(fallback_bokmal[english])
        for bokmal in candidates:
            source_to_nynorsk[bokmal] = nynorsk
    write_json(CACHE_PATH, source_to_nynorsk)

    def translated(payload_en: dict, payload_no: dict):
        out = {}
        for key, english in payload_en.items():
            bokmal = choose_bokmal(payload_no, key, english, fallback_bokmal)
            out[key] = source_to_nynorsk[bokmal]
        return out

    common_items = list(common_en.items())
    chunk_size = 150
    common_chunks = (len(common_items) + chunk_size - 1) // chunk_size
    for index in range(common_chunks):
        chunk_en = dict(common_items[index * chunk_size : (index + 1) * chunk_size])
        write_json(
            ASSETS / f"neoorigins_nn_common_{index + 1:02d}/lang/nn_no.json",
            translated(chunk_en, no_common),
        )

    write_json(ASSETS / "neoorigins_nn_121/lang/nn_no.json", translated(delta_121_en, no_121))
    write_json(ASSETS / "neoorigins_26_1/lang/nn_no.json", translated(delta_261_en, no_261))
    write_json(ASSETS / "neoorigins_26_2/lang/nn_no.json", translated(delta_262_en, no_262))
    for namespace, payload_en in addons_en.items():
        write_json(
            ASSETS / namespace / "lang/nn_no.json",
            translated(payload_en, addons_no[namespace]),
        )

    print(
        "Generated Nynorsk locale: "
        f"NeoOrigins {len(common_en)} common + {len(delta_121_en)}/{len(delta_261_en)}/{len(delta_262_en)} deltas; "
        f"add-ons {sum(len(payload) for payload in addons_en.values())} physical strings"
    )


if __name__ == "__main__":
    main()
