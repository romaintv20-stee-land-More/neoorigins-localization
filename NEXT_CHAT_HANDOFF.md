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

The first **68 languages are complete and integrated through the Bosnian staging flow**.

Latest completed language:
- **#68 Bosnian — `bs_ba / Bosanski`**

Bosnian is complete: NeoOrigins and all 10 supported 1.21.1 add-ons are fully covered; strict missing/overlap/placeholder checks and JSON validation passed; contextual refinement passed; all three pinned builds and automated JAR inspections passed; catalog/README metadata is at 68 locales. Do not redo Bosnian.

## Bosnian final references

- staging branch: `release/0.9.0-bosnian`
- staging base: `94ff74b7a4e7ed3571d94bff1a41ff171158426f`
- bootstrap run/job: `34469365449` / `102845395440` — successful
- translation commit: `ad27a83ada1156b5ba7ffea155faa3f59c49f258`
- bootstrap audit artifact: `10148972792`; SHA256 `a4f5468f996484cd0dc19428fb8546f0350e58b7b77044a4d7a3929f3cbb6517`
- refinement run/job: `34469833240` / `102846888580` — successful
- refinement commit: `c4874f19d108ce23118920a0c78d0fdd6d2aad69`
- final build source: `1167b4f0d7d6b350f98b75d1fcd6744742709b92`
- build run: `34469928487` — all three targets successful and JAR-inspected
- build jobs: 1.21.1 `102847193069`; 26.1.x `102847192735`; 26.2 `102847192853`
- packaged Bosnian file counts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- build artifacts: 1.21.1 `10149121049`; 26.1.x `10149112587`; 26.2 `10149131718`
- artifact SHA256: 1.21.1 `131df8a0fad135ee302da35f94ef5c7991aea576f522b69bc9a2e2188a115075`; 26.1.x `f02bfd71854421d36d31dc5e48a39d0f1d6539cc9c0f7ad428ac923f45ac8e5f`; 26.2 `bd471371808c0b31ca24edc3a5d1e92b3403f9925c03e969ec409b76d0142dd5`
- metadata run/job: `34469948759` / `102847260469` — successful
- metadata commit: `caf356913e18a20068fca1519c04e0e58d0641d8`

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

Start and finish **language #69**. Identify the next useful Minecraft locale from current locale data, applying the existing regional-variant deduplication rule. Then complete the full established flow: NeoOrigins + 10 add-on upstream audits, translation, contextual QA, placeholders/JSON checks, pinned 1.21.1 / 26.1.x / 26.2 builds, JAR-content inspection, metadata, both handoffs, and finally fast-forward the validated staging HEAD to `release/0.9.0-beta` with `force=false`.

Do not stop after generation or QA: language #69 is only complete once the full integration cycle is finished.
