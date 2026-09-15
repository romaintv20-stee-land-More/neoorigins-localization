#!/usr/bin/env python3
"""Pre-fill stubborn unchanged English Limburgish labels from Dutch references.

The Dutch locale is only a close-language reference. Every produced value is still
validated semantically against the original English source before it is written.
"""
from __future__ import annotations

import repair_limburgish_semantics as repair

ASSETS = repair.ASSETS


def main() -> None:
    common, d121, d261, d262, addons = repair.build_sources()
    locations = repair.current_targets(common, d121, d261, d262, addons)

    suspects = []
    for label, source_payload, target_payload, _paths in locations:
        for key, source in source_payload.items():
            target = str(target_payload[key])
            reasons = repair.semantic_reasons(str(source), target)
            if reasons:
                suspects.append((label, key, str(source), target, reasons))

    refs = repair.dutch_references(suspects)
    unique = []
    for _label, _key, source, _target, reasons in suspects:
        if reasons == ["unchanged-english"] and source in refs and source not in unique:
            unique.append(source)

    chosen = {}
    if unique:
        mt = repair.Translator()
        ref_texts = [refs[source] for source in unique]
        outputs = mt.batch(ref_texts, repair.DUTCH_LANG)
        for source, ref, raw in zip(unique, ref_texts, outputs):
            value = repair.sanitize(source, raw)
            reasons = repair.semantic_reasons(source, value)
            if not reasons:
                chosen[source] = value
            else:
                print(f"REFERENCE REJECTED {source!r}: nl={ref!r} -> {value!r} => {reasons}")

    for source, value in repair.MANUAL_REPAIRS.items():
        if not repair.semantic_reasons(source, value):
            chosen[source] = value

    if not chosen:
        print("Limburgish Dutch-reference prefill: no safe changes")
        return

    repairs = {}
    for label, key, source, old_target, _reasons in suspects:
        value = chosen.get(source)
        if value is not None and value != old_target:
            repairs[(label, key)] = value

    common_target = {}
    common_paths = sorted(ASSETS.glob("neoorigins_li_common_*/lang/li_li.json"))
    for path in common_paths:
        common_target.update(repair.read_json(path))

    for (label, key), value in repairs.items():
        if label == "common":
            common_target[key] = value
        elif label == "1.21.1":
            path = ASSETS / "neoorigins_li_121/lang/li_li.json"
            data = repair.read_json(path); data[key] = value; repair.write_json(path, data)
        elif label == "26.1":
            path = ASSETS / "neoorigins_26_1/lang/li_li.json"
            data = repair.read_json(path); data[key] = value; repair.write_json(path, data)
        elif label == "26.2":
            path = ASSETS / "neoorigins_26_2/lang/li_li.json"
            data = repair.read_json(path); data[key] = value; repair.write_json(path, data)
        else:
            path = ASSETS / label / "lang/li_li.json"
            data = repair.read_json(path); data[key] = value; repair.write_json(path, data)

    if any(label == "common" for label, _key in repairs):
        items = list(common_target.items())
        for i, path in enumerate(common_paths):
            repair.write_json(path, dict(items[i * 150:(i + 1) * 150]))

    print(f"Limburgish Dutch-reference prefill: {len(chosen)} source strings accepted; {len(repairs)} values changed")


if __name__ == "__main__":
    main()
