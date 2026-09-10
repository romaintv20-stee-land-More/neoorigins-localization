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

The first **71 languages are complete and integrated through the Asturian staging flow**.

Latest completed language:
- **#71 Asturian — `ast_es / Asturianu`**

Asturian is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 71 locales. Do not redo Asturian.

## Asturian final references

- staging branch: `release/0.9.0-asturian`
- staging base: `4d19e06eb0adba2476330a2d6cb8541a13c191c6`
- bootstrap run/job: `34503615246` / `102960216880` — successful
- translation commit: `c27a6fd526df7c45b658d4f1cfb752eb58ac8c2b`
- bootstrap audit artifact: `10162968911`; SHA256 `fbad94ef90654da2896963564d36294a4afb6a2cfeed0eca468d5b7a9677b169`
- refinement run/job: `34504053058` / `102961692864` — successful
- refinement commit: `246f4ad1cd19bc4a0bce33d8651614e4fa2d7579`
- refinement: 117 values across 20 files; final sanity 97,090 Latin chars / 1,032 Asturian orthographic signals / 40 lexical markers
- final build source: `ca9af33d43fe52d1980de1d64ba31a69e9dabf62`
- build run: `34504996882` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102964864622`; 26.1.x `102964864208`; 26.2 `102964864491`
- packaged Asturian file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10163475348`; 26.1.x `10163472700`; 26.2 `10163490791`
- artifact SHA256: 1.21.1 `664fa5414476193f6ca1fff459e9e700fa2462f55cdfa1cdde312311274c2fc0`; 26.1.x `46a191016eb1d8a3b94175af2546fe4690ce0757b878c0f564d2cff081e70433`; 26.2 `fb82ce40b0e97799a8b4a4c385b5597acd002ee4ec87469009d1fb79afde9224`
- metadata run/job: `34505083168` / `102965157510` — successful
- metadata commit: `10dcd15ccc5048587770d5c2624a2ab66e0b7d98`

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

Start and finish **language #72**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #72 is only complete once the full integration cycle is finished.
