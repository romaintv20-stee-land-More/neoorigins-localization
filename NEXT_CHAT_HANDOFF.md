# NeoOrigins Localization — Next Chat Handoff

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

The first **72 languages are complete and integrated through the West Frisian staging flow**.

Latest completed language:
- **#72 West Frisian — `fy_nl / Frysk`**

West Frisian is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 72 locales. Do not redo West Frisian.

## West Frisian final references

- staging branch: `release/0.9.0-frisian`
- staging base: `c288b5c65f8a3526057cb59c8f1c95c85b511e58`
- bootstrap run/job: `34505725859` / `102967316056` — successful
- translation commit: `1b0e26fdcd19be85c0cabbf54e432e708c42ee9f`
- bootstrap audit artifact: `10163849684`; SHA256 `db62cbcc1d81c15efe1c7d9b81f25bf4621c0a0144e9b062894bdefd1604d791`
- bootstrap sanity: 102,704 Latin chars / 2,648 Frisian orthographic signals / 3,301 lexical markers
- refinement run/job: `34506347347` / `102969373852` — successful
- refinement commit: `dee444f7140f2ce6383dc103921dee7371800394`
- refinement: 110 values across 22 files; 0 spacing repairs; final sanity 102,739 Latin chars / 2,675 orthographic signals / 3,314 lexical markers
- final build source: `1be8937ef448d914b60323ebb403cad2ba827578`
- build run: `34506531174` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102969980296`; 26.1.x `102969980489`; 26.2 `102969979932`
- packaged Frisian file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10164115614`; 26.1.x `10164097519`; 26.2 `10164081973`
- artifact SHA256: 1.21.1 `989dbe3da2ad5328eed75b94a3cfb4f541169437170b06b7f1a34e15d07b43f2`; 26.1.x `34f234fea2db05a98ecfcfa14a4e3609d851393eac8faea5fef876b3f2285056`; 26.2 `2ed3c81f535a3994faa4698dc8d67714baff99bc8dc0ccf78bf09b8621e0cdc2`
- metadata run/job: `34506557210` / `102970064631` — successful
- metadata commit: `515038c299a2946d6405d20b5d55d21bb8251048`

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

Start and finish **language #73**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #73 is only complete once the full integration cycle is finished.
