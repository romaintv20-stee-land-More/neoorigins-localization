#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
project_path = ROOT / 'PROJECT_HANDOFF.txt'
next_path = ROOT / 'NEXT_CHAT_HANDOFF.md'

project = project_path.read_text(encoding='utf-8')
project = project.replace('Last updated: 2026-09-10', 'Last updated: 2026-09-11', 1)

old = '0.9.0 development currently has 74 locales:'
new = '0.9.0 development currently has 75 locales:'
if old not in project and new not in project:
    raise SystemExit('Could not find cumulative 74-locale baseline')
project = project.replace(old, new, 1)

old_tail = 'fy_nl, oc_fr, ig_ng.'
new_tail = 'fy_nl, oc_fr, ig_ng, yo_ng.'
if old_tail not in project and new_tail not in project:
    raise SystemExit('Could not find cumulative locale-list tail')
project = project.replace(old_tail, new_tail, 1)

old_order = '- 74: Igbo / ig_ng\n\nSEVENTY-FOUR IS NOT THE FINAL TARGET.'
new_order = '- 74: Igbo / ig_ng\n- 75: Yoruba / yo_ng\n\nSEVENTY-FIVE IS NOT THE FINAL TARGET.'
if old_order not in project and new_order not in project:
    raise SystemExit('Could not find expansion-order anchor')
project = project.replace(old_order, new_order, 1)

project = project.replace('- catalog.json says 74 supported locales', '- catalog.json says 75 supported locales', 1)
project = project.replace('- README.md says 74 languages and includes Occitan / oc_fr plus Igbo / ig_ng.', '- README.md says 75 languages and includes Occitan / oc_fr, Igbo / ig_ng, and Yoruba / yo_ng.', 1)

yoruba_block = '''

YORUBA / LANGUAGE #75 FINAL STATUS
-----------------------------------
Yoruba locale: yo_ng / Yorùbá.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, STRICTLY AUDITED, CONTEXT-REFINED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND COMMITTED.

Selection / staging:
- staging branch: release/0.9.0-yoruba
- exact beta base used: da37f6628fc54a9bd55909211e48b293a9a48fcd
- locale: yo_ng / Yorùbá
- selected from current Minecraft Java locale data; Yoruba is a distinct language and has no regional-dedup conflict with the existing locale set.
- automated/generative translation assistance was used; this is not a claim of full native-speaker review.

Bootstrap / upstream audit:
- final successful workflow run 34567349486 / job 103162079968: SUCCESS
- validated translation commit: 0ce252fc3102d02db94925c85c789636ae83f7fc
- upstream official Yoruba strings found: 0 for all three NeoOrigins targets and 0 for all 10 supported add-ons at the pinned references
- 29 yo_ng.json source files generated
- bootstrap sanity: 91,064 Latin-script characters, 9,288 Yoruba orthographic signals, 5,586 lexical markers
- bootstrap audit artifact: 10186637364; size 291,553 bytes; SHA256 9dbbbc6c9161d278ff7cede7cd1dc2d00f3cf5ede82ef4f752451d612b064f42
- one internal bootstrap token transport case fell back safely during generation; final strict placeholder audits passed with zero errors.

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
- 16 Yoruba common namespaces: neoorigins_yo_common_01 through neoorigins_yo_common_16
- 1.21.1 delta: neoorigins_yo_121
- Yoruba entries in neoorigins_26_1 and neoorigins_26_2
- 10 Yoruba add-on fallback files on 1.21.1
- 29 yo_ng.json source files total
- Gradle switch: include_yoruba_121_translations / includeYoruba121Translations

Contextual QA / refinement:
- workflow run 34568292817 / job 103164814413: SUCCESS
- refinement trigger/source commit: 214170886e4c9a0229b3fe784fe3300a6bd6b6ae
- refinement commit: 734f13fe855a87c191ef56a3bc980a006e64f977
- 80 values refined across 18 files
- 2 sentence-spacing repairs
- JSON validation and git diff --check passed
- final sanity: 91,057 Latin-script characters, 9,374 Yoruba orthographic signals, 5,751 lexical markers
- high-visibility UI terminology was context-refined, while Origin and NeoOrigins branding remains canonical.

Final builds and JAR inspection:
- workflow: .github/workflows/build-0.9.0-yoruba-push.yml
- final build source SHA: b9d899e821c60551cbc1155c8f372f6721be9a92
- successful run: 34568924469
- 1.21.1 job 103166661972: SUCCESS; 27 Yoruba files packaged
- 26.1.x job 103166662064: SUCCESS; 17 Yoruba files packaged
- 26.2 job 103166662118: SUCCESS; 17 Yoruba files packaged
- each build passed automated JAR-content inspection including all 16 common namespaces, required target delta, exact file count, and wrong-version/add-on exclusion checks.
- 1.21.1 artifact: 10187053675; size 6,037,615 bytes; SHA256 c438c21a1e60e3e46861bbf2cb8e07dffef3f3d331789a78fae687c410263476
- 26.1.x artifact: 10187049368; size 3,350,206 bytes; SHA256 a3082238049d9b9e28b898e82231b691a08af7a369a50d01069bac524b952bd8
- 26.2 artifact: 10187050767; size 3,350,300 bytes; SHA256 87b91374434de54a3a96088a6b603d49e118313c67232f9666c4d4b5a97a2c96

Metadata:
- metadata workflow run 34568960023 / job 103166767297: SUCCESS
- metadata trigger/source commit: 18403650d97461dce4161001423f281b0b01986b
- metadata commit: 2fd590a29d9fb3ca84de6c221d3b7454c2a70a97
- catalog.json now declares 75 supported locales and includes yo_ng / Yoruba for NeoOrigins plus all 10 supported add-ons
- CATALOG.md and README.md document Yoruba and the exact 2,296 / 2,307 / 2,307 core coverage.

Integration rule:
- release/0.9.0-beta must be fast-forwarded to the final release/0.9.0-yoruba HEAD with force=false only after this handoff validation succeeds and compare shows behind_by=0 with the exact old beta merge base.
- main remains intentionally untouched.

NEXT LANGUAGE
-------------
Language #76 is the next expansion task. Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 75-locale set, apply the regional-variant deduplication rule, then repeat the complete upstream audit, translation, contextual QA, builds, JAR inspection, metadata, handoff, and non-forced fast-forward flow.
'''
if 'YORUBA / LANGUAGE #75 FINAL STATUS' not in project:
    project = project.rstrip() + yoruba_block
project_path.write_text(project.rstrip() + '\n', encoding='utf-8')

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

The first **75 languages are complete and integrated through the Yoruba staging flow**.

Latest completed language:
- **#75 Yoruba — `yo_ng / Yorùbá`**

Yoruba is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 75 locales. Do not redo Yoruba.

## Yoruba final references

- staging branch: `release/0.9.0-yoruba`
- staging base: `da37f6628fc54a9bd55909211e48b293a9a48fcd`
- bootstrap run/job: `34567349486` / `103162079968` — successful
- translation commit: `0ce252fc3102d02db94925c85c789636ae83f7fc`
- bootstrap audit artifact: `10186637364`; size `291,553 bytes`; SHA256 `9dbbbc6c9161d278ff7cede7cd1dc2d00f3cf5ede82ef4f752451d612b064f42`
- bootstrap sanity: 91,064 Latin chars / 9,288 Yoruba orthographic signals / 5,586 lexical markers
- refinement run/job: `34568292817` / `103164814413` — successful
- refinement commit: `734f13fe855a87c191ef56a3bc980a006e64f977`
- refinement: 80 values across 18 files; 2 spacing repairs; final sanity 91,057 Latin chars / 9,374 orthographic signals / 5,751 lexical markers
- final build source: `b9d899e821c60551cbc1155c8f372f6721be9a92`
- build run: `34568924469` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `103166661972`; 26.1.x `103166662064`; 26.2 `103166662118`
- packaged Yoruba file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10187053675`; 26.1.x `10187049368`; 26.2 `10187050767`
- artifact SHA256: 1.21.1 `c438c21a1e60e3e46861bbf2cb8e07dffef3f3d331789a78fae687c410263476`; 26.1.x `a3082238049d9b9e28b898e82231b691a08af7a369a50d01069bac524b952bd8`; 26.2 `87b91374434de54a3a96088a6b603d49e118313c67232f9666c4d4b5a97a2c96`
- metadata run/job: `34568960023` / `103166767297` — successful
- metadata commit: `2fd590a29d9fb3ca84de6c221d3b7454c2a70a97`

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #76**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #76 is only complete once the full integration cycle is finished.
'''
next_path.write_text(next_text, encoding='utf-8')
print('Yoruba handoffs prepared for 75 completed locales; language #76 next.')
