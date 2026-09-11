# NeoOrigins Localization — Next Chat Handoff

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
