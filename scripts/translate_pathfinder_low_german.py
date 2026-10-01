#!/usr/bin/env python3
from pathlib import Path
import json
import bootstrap_low_german as base
from refine_low_german import (
    MT, PRIMARY_MODEL_ID, FALLBACK_MODEL_ID, TARGET_TOKEN,
    safe_pair, sanitize, sentence_count,
)

ROOT = Path(__file__).resolve().parents[1]
LANG = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets/pathfinder_origins/lang"
SOURCE = LANG / "fr_fr.json"
OUTPUT = LANG / "nds_de.json"

source_map = json.loads(SOURCE.read_text(encoding="utf-8"))
sources = list(source_map.keys())
exact = base.build_corpus_map()
translated = {}
direct = []
for source in sources:
    if source in base.MANUAL_VALUES:
        translated[source] = base.MANUAL_VALUES[source]
    elif source in exact:
        translated[source] = exact[source]
    else:
        direct.append(source)

primary = MT(PRIMARY_MODEL_ID)
fallback = None
fallback_count = 0
for start in range(0, len(direct), 24):
    batch = direct[start:start + 24]
    singles = [s for s in batch if sentence_count(s) < 2]
    values = dict(zip(singles, primary.batch(singles)))
    for source in batch:
        value = primary.sentence_complete(source) if source not in values else values[source]
        value = sanitize(source, value)
        if not safe_pair(source, value):
            value = sanitize(source, primary.structural(source))
        if not safe_pair(source, value):
            if fallback is None:
                fallback = MT(FALLBACK_MODEL_ID)
            value = sanitize(source, fallback.sentence_complete(source))
            fallback_count += 1
        if not safe_pair(source, value):
            raise SystemExit(f"Unsafe Pathfinder Low German translation: {source!r} -> {value!r}")
        translated[source] = value
    print(f"Pathfinder Low German: {min(start + len(batch), len(direct))}/{len(direct)}", flush=True)

result = {source: translated[source] for source in sources}
if len(result) != 406:
    raise SystemExit(f"Expected 406 Pathfinder strings, got {len(result)}")
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT} with {len(result)} strings; fallback={fallback_count}")
