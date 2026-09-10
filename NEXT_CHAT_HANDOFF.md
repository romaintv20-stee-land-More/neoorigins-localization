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

The first **70 languages are complete and integrated through the Breton staging flow**.

Latest completed language:
- **#70 Breton — `br_fr / Brezhoneg`**

Breton is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 70 locales. Do not redo Breton.

## Breton final references

- staging branch: `release/0.9.0-breton`
- staging base: `6cd7efc642b22313f58d1024975ae7b5406d7f67`
- bootstrap run/job: `34499084751` / `102944976049` — successful
- translation commit: `551f79ef1c402dfa37140e6574590cdc42c2e436`
- bootstrap audit artifact: `10161171163`; SHA256 `7628f5374445b6058637b4b34c005d949cb42a6d8ec45ec246c8afbdee7b7f21`
- refinement run/job: `34499606349` / `102946756904` — successful
- refinement commit: `ae5dffcdcfbd1d5cf9d489912383f5a76a3f4a1f`
- refinement: 317 values across 21 files, including 244 spacing repairs; final sanity 108,480 Latin chars / 4,568 Breton orthographic signals / 4,323 lexical markers
- final build source: `6871dfe04d3c7742c500da45c2c4181472989f73`
- build run: `34499725033` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102947162125`; 26.1.x `102947161983`; 26.2 `102947162157`
- packaged Breton file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10161377271`; 26.1.x `10161372162`; 26.2 `10161365047`
- artifact SHA256: 1.21.1 `d8cedd93d490c09b103b4ea06f1eb0492190f04ed1056f0e2d8118f02e8b0875`; 26.1.x `de1b59c502979851568bcc825b3e04da1fbb386b4f7530a61af2a989a28d9970`; 26.2 `7e69754747c0f28771b70473e4ef1312dcb12c37439a6c9b261c44c3c588fa14`
- metadata run/job: `34499961101` / `102947953799` — successful
- metadata commit: `d620425512de44e031c51a6135433aca4848246c`

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

Start and finish **language #71**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #71 is only complete once the full integration cycle is finished.
