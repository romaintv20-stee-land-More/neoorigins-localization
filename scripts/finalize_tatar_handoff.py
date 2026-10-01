#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Update the long-lived project handoff conservatively: preserve all historical
# material and only advance the baseline + append the validated Tatar record.
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

old = '0.9.0 development currently has 75 locales:'
new = '0.9.0 development currently has 76 locales:'
if old not in text:
    raise SystemExit('PROJECT_HANDOFF 75-locale baseline header not found')
text = text.replace(old, new, 1)

old_tail = 'fy_nl, oc_fr, ig_ng, yo_ng.'
new_tail = 'fy_nl, oc_fr, ig_ng, yo_ng, tt_ru.'
if old_tail not in text:
    raise SystemExit('PROJECT_HANDOFF locale tail not found')
text = text.replace(old_tail, new_tail, 1)

if '- 76: Tatar / tt_ru' not in text:
    anchor = '- 75: Yoruba / yo_ng\n'
    if anchor not in text:
        raise SystemExit('PROJECT_HANDOFF expansion-order anchor not found')
    text = text.replace(anchor, anchor + '- 76: Tatar / tt_ru\n', 1)

text = text.replace('SEVENTY-FIVE IS NOT THE FINAL TARGET.', 'SEVENTY-SIX IS NOT THE FINAL TARGET.', 1)

section = '''

76. TATAR 0.9.0 STATUS
----------------------
Tatar locale: tt_ru / Татарча.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, JAR-INSPECTED, AND DOCUMENTED.

Selection / upstream:
- Tatar is a current Minecraft Java locale and is materially distinct under the regional-dedup rule.
- NeoOrigins official Tatar strings: 0 on all three pinned refs.
- All 10 supported 1.21.1 add-ons: 0 official Tatar strings.
- Translation was automated/generative with contextual QA; do NOT describe it as native-speaker-reviewed.

Architecture / coverage:
- 16 common namespaces: neoorigins_tt_common_01 through neoorigins_tt_common_16
- 1.21.1 delta: neoorigins_tt_121 (6 keys)
- 26.1.x delta: tt_ru in neoorigins_26_1 (17 keys)
- 26.2 delta: tt_ru in neoorigins_26_2 (17 keys)
- 10 add-on fallback files on 1.21.1
- NeoOrigins: 2296/2296 on 1.21.1; 2307/2307 on 26.1.x; 2307/2307 on 26.2
- strict missing=0 / overlap=0 / placeholder errors=0 across NeoOrigins and all 10 add-ons

Bootstrap:
- staging branch: release/0.9.0-tatar
- staging base: 26e7613f27f0c9bc79a3ff904ea76d8e0dc06dae
- successful bootstrap run/job: 34570202254 / 103170494373
- validated bootstrap commit: c8df93d654479a92265124ae627810a140ba3535
- audit artifact: 10187659782; size 291,548 bytes; SHA256 4df903723e34ffc74f1f5353d78f286eac345de5a8ef4a77981a420c409c1bf9
- bootstrap sanity: 93,556 Cyrillic chars / 8,966 Tatar-specific letters / 1,371 lexical markers across 29 files

Contextual refinement:
- run/job: 34571876349 / 103175545574
- refinement commit: d2ff4fe42c674479b0557c58d1e87a41f6c47c14
- 93 values changed across 20 files; 11 spacing repairs
- final sanity: 93,582 Cyrillic chars / 9,028 Tatar-specific letters / 1,385 lexical markers across 29 files

Build / JAR verification:
- build source: 7968312f286ad352591c360573cadf5399f1ba04
- build run: 34572020195 — all three jobs successful
- 1.21.1 job 103175976530 — exactly 27 tt_ru files: 16 common + neoorigins_tt_121 + 10 add-ons; no 26.x Tatar delta
- 26.1.x job 103175976288 — exactly 17 tt_ru files: 16 common + neoorigins_26_1; no add-ons / 1.21.1 delta / 26.2 delta
- 26.2 job 103175976591 — exactly 17 tt_ru files: 16 common + neoorigins_26_2; no add-ons / 1.21.1 delta / 26.1 delta
- 1.21.1 artifact 10188158311; size 6,130,932 bytes; SHA256 1396f5e22c8d99db8460672ccdb8359a3cd3bb147ebd3347886fda2f92993bf7
- 26.1.x artifact 10188143554; size 3,404,682 bytes; SHA256 e29d00f7c3ac525feb0b52a5609a8d1dfaf3572960fe4819b28bd82156b437b3
- 26.2 artifact 10188156712; size 3,404,760 bytes; SHA256 28bd14bfb9a91fc551478671c8d82ac18805151c7145b12659b8341241cdd361

Metadata:
- metadata run/job: 34572317420 / 103176902431
- metadata commit: 7dc9eb82481f4341788ef2a4c3209fdff831daa3
- catalog.json supported_locale_count: 76
- Tatar is listed for NeoOrigins + all 10 supported add-ons; README/CATALOG synchronized.

NEXT LANGUAGE:
- #77 is next after Tatar is fast-forwarded into release/0.9.0-beta.
- Re-evaluate the current Minecraft locale inventory before selecting it; do not guess or redo Tatar.
'''
if '76. TATAR 0.9.0 STATUS' not in text:
    text = text.rstrip() + section + '\n'
p.write_text(text, encoding='utf-8')

# Keep the short next-chat handoff deliberately compact and authoritative.
next_text = '''# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-11
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/0.9.0-beta`

## Mandatory starting rules

- Read this file and `PROJECT_HANDOFF.txt` before changing anything.
- Use `release/0.9.0-beta` as the source-of-truth branch.
- **Do not use `main`**; it is intentionally behind the cumulative 0.9.0 beta development state.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Continue automatically through audit, translation, contextual QA, builds, JAR inspection, metadata, handoffs and a non-forced fast-forward back to `release/0.9.0-beta`.
- Automated/generative translation assistance is used; do not describe generated locales as fully native-speaker-reviewed unless a real native review occurred.

## Completed language baseline

The first **76 languages are complete through the Tatar staging flow**.

Latest completed language:
- **#76 Tatar — `tt_ru / Татарча`**

Tatar is complete on staging: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 76 locales. Do not redo Tatar.

## Tatar final references

- staging branch: `release/0.9.0-tatar`
- staging base: `26e7613f27f0c9bc79a3ff904ea76d8e0dc06dae`
- bootstrap run/job: `34570202254` / `103170494373` — successful
- bootstrap commit: `c8df93d654479a92265124ae627810a140ba3535`
- bootstrap audit artifact: `10187659782`; size `291,548 bytes`; SHA256 `4df903723e34ffc74f1f5353d78f286eac345de5a8ef4a77981a420c409c1bf9`
- bootstrap sanity: 93,556 Cyrillic chars / 8,966 Tatar-specific letters / 1,371 lexical markers
- refinement run/job: `34571876349` / `103175545574` — successful
- refinement commit: `d2ff4fe42c674479b0557c58d1e87a41f6c47c14`
- refinement: 93 values across 20 files; 11 spacing repairs; final sanity 93,582 Cyrillic chars / 9,028 Tatar-specific letters / 1,385 lexical markers
- build source: `7968312f286ad352591c360573cadf5399f1ba04`
- build run: `34572020195` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `103175976530`; 26.1.x `103175976288`; 26.2 `103175976591`
- packaged Tatar file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10188158311`; 26.1.x `10188143554`; 26.2 `10188156712`
- artifact SHA256: 1.21.1 `1396f5e22c8d99db8460672ccdb8359a3cd3bb147ebd3347886fda2f92993bf7`; 26.1.x `e29d00f7c3ac525feb0b52a5609a8d1dfaf3572960fe4819b28bd82156b437b3`; 26.2 `28bd14bfb9a91fc551478671c8d82ac18805151c7145b12659b8341241cdd361`
- metadata run/job: `34572317420` / `103176902431` — successful
- metadata commit: `7dc9eb82481f4341788ef2a4c3209fdff831daa3`

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

After confirming Tatar is integrated into `release/0.9.0-beta`, start and finish **language #77**. Re-evaluate the current Minecraft Java locale inventory and choose the next useful distinct locale under the regional-variant deduplication rule. Then complete the full established flow through non-forced beta integration.

Do not stop after generation or QA: language #77 is only complete once the full integration cycle is finished.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_text, encoding='utf-8')

print('Tatar handoffs prepared: baseline advanced to 76 and next language set to #77.')
