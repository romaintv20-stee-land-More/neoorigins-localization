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

The first **67 languages are complete and integrated through the Lao staging flow**.

Latest completed language:
- **#67 Lao — `lo_la / ລາວ`**

Lao is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 67 locales. Do not redo Lao.

## Lao final references

- staging branch: `release/0.9.0-lao`
- staging base: `7843a7511e5c618733e3d485a74d42c302535cfd`
- bootstrap run/job: `34465982708` / `102834552752` — successful
- translation commit: `1ee66f61eca3c33e7ceabc0889d71bb736f7c5bd`
- refinement run/job: `34466422963` / `102835964108` — successful
- refinement commit: `1d6ab15ead3597a0415151f897b6c39af403573a`
- final build source: `f15d657b56227083df4e7fb844e483851a9e7dda`
- build run: `34466597033` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102836514572`; 26.1.x `102836514235`; 26.2 `102836514614`
- packaged Lao file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10147827354`; 26.1.x `10147821367`; 26.2 `10147795437`
- artifact SHA256: 1.21.1 `4e8b664f4f7f379ba4398f6d6f3742eda440c0d4c2b6530d0f39a774b148d671`; 26.1.x `1de8476269fbbcaf6f872ef78866274057e207bdebd687b2d7e531902b47e427`; 26.2 `66e46b893c5ab67c7550200a6298c177ec93d8e5df08d0606c3e85da62613b4a`
- metadata run/job: `34466658695` / `102836711475` — successful
- metadata commit: `b6ceffa4b3428dc95ac4d64e08ce5c766c729120`

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

Start and finish **language #68**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #68 is only complete once the full integration cycle is finished.
