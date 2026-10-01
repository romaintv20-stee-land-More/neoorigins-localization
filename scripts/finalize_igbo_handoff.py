#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
project_path = ROOT / 'PROJECT_HANDOFF.txt'
next_path = ROOT / 'NEXT_CHAT_HANDOFF.md'

project = project_path.read_text(encoding='utf-8')

# Update only the cumulative/current baseline at the top. Historical per-language
# NEXT LANGUAGE notes are intentionally left intact as provenance.
old = '0.9.0 development currently has 73 locales:'
new = '0.9.0 development currently has 74 locales:'
if old not in project and new not in project:
    raise SystemExit('Could not find cumulative 73-locale baseline')
project = project.replace(old, new, 1)

old_tail = 'fy_nl, oc_fr.'
new_tail = 'fy_nl, oc_fr, ig_ng.'
if old_tail not in project and new_tail not in project:
    raise SystemExit('Could not find cumulative locale-list tail')
project = project.replace(old_tail, new_tail, 1)

old_order = '- 73: Occitan / oc_fr\n\nSEVENTY-THREE IS NOT THE FINAL TARGET.'
new_order = '- 73: Occitan / oc_fr\n- 74: Igbo / ig_ng\n\nSEVENTY-FOUR IS NOT THE FINAL TARGET.'
if old_order not in project and new_order not in project:
    raise SystemExit('Could not find expansion-order anchor')
project = project.replace(old_order, new_order, 1)

project = project.replace('- catalog.json says 73 supported locales', '- catalog.json says 74 supported locales', 1)
project = project.replace('- README.md says 73 languages and includes Occitan / oc_fr.', '- README.md says 74 languages and includes Occitan / oc_fr plus Igbo / ig_ng.', 1)

igbo_block = '''

IGBO / LANGUAGE #74 FINAL STATUS
---------------------------------
Igbo locale: ig_ng / Igbo.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, CONTEXT-REFINED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Selection / staging:
- staging branch: release/0.9.0-igbo
- exact beta base used: a62e6fb15615f24d10467b04db47654e148d131a
- locale: ig_ng / Igbo
- selected from current Minecraft Java locale data; Igbo is a distinct language and has no regional-dedup conflict with the existing locale set.
- automated/generative translation assistance was used; this is not a claim of full native-speaker review.

Bootstrap / upstream audit:
- final successful workflow run 34513745788 / job 102993943356: SUCCESS
- validated translation commit: d95c009ade599f1ec93c3df2b03d571daf6e0f48
- upstream official Igbo strings found: 0 for all three NeoOrigins targets and 0 for all 10 supported add-ons at the pinned references
- 29 ig_ng.json source files generated
- bootstrap sanity: 95,348 Latin-script characters, 14,283 Igbo orthographic signals, 5,054 lexical markers
- bootstrap audit artifact: 10167049707; size 291,550 bytes; SHA256 9a10d81cadd3821830caf44ed4ebf99d8188e918c94320a2ba8d76e42e941797
- earlier attempts failed only while hardening public-translation batching/rate-limit/token transport; the final successful run is authoritative.

NeoOrigins coverage against the pinned 2.2.27 baselines:
- 1.21.1: 2,296 / 2,296
- 26.1.x: 2,307 / 2,307
- 26.2: 2,307 / 2,307
- missing keys: 0
- overlap errors: 0
- placeholder errors: 0

1.21.1 add-on coverage:
- Medieval Origins Revival: 401 / 401
- ibarn's quartet origins addon: 69 / 69
- Origins Fantasy: 240 / 240
- Origins: Backgrounds: 65 / 65
- Origins: More Backgrounds: 44 / 44 effective
- Origins: Backgrounds ISS: 79 / 79 effective
- Origins Furries: 117 / 117
- Origins: Classes Extended: 124 / 124
- Origins: Classes ISS: 99 / 99
- Origin Architect: 22 / 22
- all strict add-on audits passed with missing=0, overlap=0 and placeholder errors=0.

Localization architecture:
- 16 Igbo common namespaces: neoorigins_ig_common_01 through neoorigins_ig_common_16
- 1.21.1 delta: neoorigins_ig_121
- Igbo entries in neoorigins_26_1 and neoorigins_26_2
- 10 Igbo add-on fallback files on 1.21.1
- 29 ig_ng.json source files total
- Gradle switch: include_igbo_121_translations / includeIgbo121Translations

Contextual QA / refinement:
- workflow run 34515088488 / job 102998388143: SUCCESS
- refinement commit: 4ac1335f0b4c404ca4310a68229337de1d05e8d3
- 68 values refined across 19 files
- 0 sentence-spacing repairs were needed
- JSON validation and git diff --check passed
- final sanity: 95,363 Latin-script characters, 15,082 Igbo orthographic signals, 5,579 lexical markers
- high-visibility UI terminology was context-refined, while Origin and NeoOrigins branding remains canonical.

Final builds and JAR inspection:
- workflow: .github/workflows/build-0.9.0-igbo.yml
- final build source SHA: 08f7f3becc3c705f0bce3883fe00904a569fa262
- successful run: 34515317584
- 1.21.1 job 102999143169: SUCCESS; 27 Igbo files packaged
- 26.1.x job 102999143300: SUCCESS; 17 Igbo files packaged
- 26.2 job 102999142841: SUCCESS; 17 Igbo files packaged
- each build passed automated JAR-content inspection including all 16 common namespaces, required target delta, exact file count, and wrong-version/add-on exclusion checks.
- 1.21.1 artifact: 10167475323; size 5,958,393 bytes; SHA256 4845c5308aa45534351927e47da395d42b6613691a9a69a5dbb5d66909736791
- 26.1.x artifact: 10167467067; size 3,303,163 bytes; SHA256 6eeb4de265df30ec3e5fdc55eabfc79e77914d48b19b618a70c6ac26210ec3e7
- 26.2 artifact: 10167472739; size 3,303,253 bytes; SHA256 5fc31ce80069248a09f9ace1050c8da7ea22154665b0aaacbb7182b9850109df

Metadata:
- metadata workflow run 34515339345 / job 102999216329: SUCCESS
- metadata commit: 6f99eb011d4207a2cee7ef9af9396deb2f075ef9
- catalog.json now declares 74 supported locales and includes ig_ng / Igbo for NeoOrigins plus all 10 supported add-ons
- CATALOG.md and README.md document Igbo and the exact 2,296 / 2,307 / 2,307 core coverage.

Integration rule:
- release/0.9.0-beta must be fast-forwarded to the final release/0.9.0-igbo HEAD with force=false only after this handoff validation succeeds and compare shows behind_by=0 with the exact old beta merge base.
- main remains intentionally untouched.

NEXT LANGUAGE
-------------
Language #75 is the next expansion task. Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 74-locale set, apply the regional-variant deduplication rule, then repeat the complete upstream audit, translation, contextual QA, builds, JAR inspection, metadata, handoff, and non-forced fast-forward flow.
'''
if 'IGBO / LANGUAGE #74 FINAL STATUS' not in project:
    project = project.rstrip() + igbo_block
project_path.write_text(project.rstrip() + '\n', encoding='utf-8')

next_text = '''# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-10
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

The first **74 languages are complete and integrated through the Igbo staging flow**.

Latest completed language:
- **#74 Igbo — `ig_ng / Igbo`**

Igbo is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 74 locales. Do not redo Igbo.

## Igbo final references

- staging branch: `release/0.9.0-igbo`
- staging base: `a62e6fb15615f24d10467b04db47654e148d131a`
- bootstrap run/job: `34513745788` / `102993943356` — successful
- translation commit: `d95c009ade599f1ec93c3df2b03d571daf6e0f48`
- bootstrap audit artifact: `10167049707`; size `291,550 bytes`; SHA256 `9a10d81cadd3821830caf44ed4ebf99d8188e918c94320a2ba8d76e42e941797`
- bootstrap sanity: 95,348 Latin chars / 14,283 Igbo orthographic signals / 5,054 lexical markers
- refinement run/job: `34515088488` / `102998388143` — successful
- refinement commit: `4ac1335f0b4c404ca4310a68229337de1d05e8d3`
- refinement: 68 values across 19 files; 0 spacing repairs; final sanity 95,363 Latin chars / 15,082 orthographic signals / 5,579 lexical markers
- final build source: `08f7f3becc3c705f0bce3883fe00904a569fa262`
- build run: `34515317584` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102999143169`; 26.1.x `102999143300`; 26.2 `102999142841`
- packaged Igbo file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10167475323`; 26.1.x `10167467067`; 26.2 `10167472739`
- artifact SHA256: 1.21.1 `4845c5308aa45534351927e47da395d42b6613691a9a69a5dbb5d66909736791`; 26.1.x `6eeb4de265df30ec3e5fdc55eabfc79e77914d48b19b618a70c6ac26210ec3e7`; 26.2 `5fc31ce80069248a09f9ace1050c8da7ea22154665b0aaacbb7182b9850109df`
- metadata run/job: `34515339345` / `102999216329` — successful
- metadata commit: `6f99eb011d4207a2cee7ef9af9396deb2f075ef9`

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports these 10 projects:
1. Medieval Origins Revival
2. ibarn's quartet origins addon
3. Origins Fantasy for NeoOrigins
4. Origins: Backgrounds for NeoOrigins
5. Origins: More Backgrounds for NeoOrigins
6. Origins: Backgrounds ISS for NeoOrigins
7. Origins Furries for NeoOrigins
8. Origins: Classes Extended for NeoOrigins
9. Origins: Classes ISS for NeoOrigins
10. Origin Architect

26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #75**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #75 is only complete once the full integration cycle is finished.
'''
next_path.write_text(next_text, encoding='utf-8')
print('Igbo handoffs prepared for 74 completed locales; language #75 next.')
