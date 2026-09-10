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
