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

The first **69 languages are complete and integrated through the Bashkir staging flow**.

Latest completed language:
- **#69 Bashkir — `ba_ru / Башҡортса`**

Bashkir is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 69 locales. Do not redo Bashkir.

## Bashkir final references

- staging branch: `release/0.9.0-bashkir`
- staging base: `a52ed0fa7f70c61f93e70520cb7f1f536b44b6be`
- final successful bootstrap run/job: `34471747172` / `102853001005` — successful
- translation commit: `cec9ab0a71957b24962080248f1df0cdb6222515`
- bootstrap audit artifact: `10149880478`; SHA256 `daa959a3fbf638371afc3f275cb5453696ef9c0072a22f1d755c99ab99792316`
- refinement run/job: `34472164124` / `102854348131` — successful
- refinement commit: `debf0015dbc1b8e656bc2f122c95cfd7351aaad0`
- final build source: `69f334d70c5aa86eeda69dc25a96daa1380aec63`
- build run: `34472412396` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102855147842`; 26.1.x `102855147718`; 26.2 `102855147907`
- packaged Bashkir file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10150102626`; 26.1.x `10150108739`; 26.2 `10150094595`
- artifact SHA256: 1.21.1 `d4acbd23c9ada2e87b0212d3642b68689402601cfc1a63a1f4e2f5003449fd15`; 26.1.x `9f087da8bbdda18ecb40b17a9d9877c3c768a91099a48d030e6449e21081465e`; 26.2 `8a49f9ef080d42f8228ee1f8415b1c615d64eccdb5afae3da57de52ccf2ea926`
- metadata run/job: `34472476635` / `102855353494` — successful
- metadata commit: `cf3cb363f19c89f9f121407c3a5ca01ed9787c58`

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

Start and finish **language #70**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #70 is only complete once the full integration cycle is finished.
