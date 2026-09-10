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

The first **73 languages are complete and integrated through the Occitan staging flow**.

Latest completed language:
- **#73 Occitan — `oc_fr / Occitan`**

Occitan is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 73 locales. Do not redo Occitan.

## Occitan final references

- staging branch: `release/0.9.0-occitan`
- staging base: `5102ca8bebfd1d0934ca580dfa94ca442f665097`
- bootstrap run/job: `34508278437` / `102975735103` — successful
- translation commit: `b17e68f045068492f0b1d3c862cf557e8bb0407a`
- bootstrap audit artifact: `10164816852`; SHA256 `a7d1c3cdc8148c3893facaa2debb46e554af5ba0208bdfb08602bead4460cb77`
- bootstrap sanity: 114,301 Latin chars / 4,578 Occitan orthographic signals / 6,297 lexical markers
- refinement run/job: `34508845577` / `102977624166` — successful
- refinement commit: `4f5c1e4832a83f3baee7caa18271ffef21bcf2a4`
- refinement: 77 values across 20 files; 0 spacing repairs; final sanity 114,347 Latin chars / 4,567 orthographic signals / 6,403 lexical markers
- final build source: `12b0907cb0b64ba16d3b580f8d624956c9ce0507`
- build run: `34509055896` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102978341229`; 26.1.x `102978340959`; 26.2 `102978341174`
- packaged Occitan file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10165061817`; 26.1.x `10165053701`; 26.2 `10165062695`
- artifact SHA256: 1.21.1 `985829a6d7af4aaa416fab26ecfd147feb500905691ed887bc299845da29ffef`; 26.1.x `81dd4f7c4e0178202561804b502b01f9acd76b41634f707a263d22145785a421`; 26.2 `01369a0df00858961f8c297ebabdfd1d759f8ab414cfb9ecf6ec7296f1c7e850`
- metadata run/job: `34509107556` / `102978517417` — successful
- metadata commit: `667164192da1c464e282d6f89428abf4598ae94c`

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

Start and finish **language #74**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #74 is only complete once the full integration cycle is finished.
