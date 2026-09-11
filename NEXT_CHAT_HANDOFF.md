# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-11
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything. For the current 1.0.0 language-expansion state, this file and the locale plan supersede older 0.9.0 status text still present in `PROJECT_HANDOFF.txt`.
- Use `release/1.0.0` as the source-of-truth integration branch for the ongoing 1.0.0 cycle.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Continue each locale through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, and integration.
- Automated/generative translation assistance is used; do not describe generated locales as fully native-speaker-reviewed unless a real native review occurred.
- Do not bump the public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue is finished and the final global release gates pass.

## Completed language baseline

The first **84 selected locales are complete and integrated**.

Latest completed languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**
- **#79 Bavarian — `bar / Boarisch`**
- **#80 Brabantian — `brb / Braobans`**
- **#81 Andalusian — `esan / Andalûh`**
- **#82 East Franconian — `fra_de / Fränggisch`**
- **#83 Friulian — `fur_it / Furlan`**
- **#84 Gallo — `go_fr / Galo`**

The catalogue and README are at **84 locales**. There are **29 selected locales remaining** for 1.0.0; the authoritative queue and exclusion policy are in `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Gallo final references

- staging branch: `release/1.0.0-gallo`
- successful bootstrap run: `34642158821`
- bootstrap output commit: `3ef631a8c90842e177b595433405d9dc1cac6099`
- generated source layout: 16 common NeoOrigins chunks + 1.21.1 delta + shared 26.x deltas + 10 add-ons = 29 `go_fr` source files
- source strategy: complete French semantic coverage plus pinned Minecraft `fr_fr` ↔ `go_fr` corpus; projection is conservative and official upstream strings retain priority
- contextual QA found the unsafe high-visibility projection `Phantom` → `Sebllan`; all 3 affected Phantom values were restored/protected
- safe refinement run: `34642867766`
- safe refinement commit: `5565fbf7f50670cf28ca0b092c97b2e647b617d1`
- refinement result: all 3,583 generated values checked; 3 unsafe Phantom projections corrected; 459 Gallo lexical markers retained
- strict NeoOrigins audits passed at 2,296/2,296 keys on 1.21.1 and 2,307/2,307 on both 26.x targets; all 10 compatible 1.21.1 add-on audits passed; overlaps and placeholder errors are zero
- build workflow commit: `34ed82f78e024f1c7901f695f5e2a6612d40bbe9`
- build run: `34643042947` — successful on all three targets
- packaged Gallo file counts enforced by JAR inspection gates:
  - 1.21.1: 27 (16 common + `neoorigins_go_121` + 10 add-ons)
  - 26.1.x: 17 (16 common + `neoorigins_26_1`)
  - 26.2: 17 (16 common + `neoorigins_26_2`)
- JAR isolation gates passed: 26.x contain no 1.21.1 add-ons or `neoorigins_go_121`; each build contains only its proper version delta
- metadata workflow run: `34643884667`
- metadata job/check: `103409897617`
- final branch metadata commit: `593402eb323d5b33b14c0b2f5dd1bab846840467`
- metadata final state: 84 supported locales, `go_fr` present across all 11 projects, 29 source files, fallback namespaces `gallo_common_glob = neoorigins_go_common_*` and `gallo_mc_1_21_1 = neoorigins_go_121`
- native metadata/catalog name: `Galo`; README French label: `Gallo`
- integration PR: `#21`
- integration commit on `release/1.0.0`: `83a697348e1b8d15741cbe6bb7fe53bd8dc0445c`

Do not redo Gallo, Friulian, East Franconian, Andalusian, Brabantian, Bavarian, Northern Sami, or Traditional Chinese metadata.

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

Pinned Minecraft locale corpus:
- repository: `teaSummer/minecraft-locales`
- ref: `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- Java locale files: `java/<locale>.json`

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #85 — Manx (`gv_im`)** from the current `release/1.0.0` branch.

Inspect the pinned `gv_im` Minecraft corpus first and choose a defensible semantic/projection strategy before generating anything. Do not assume that another Celtic language can safely stand in for Manx. Then use the full established flow: bootstrap conservatively, run strict audits, perform contextual QA/refinement, build all three targets with JAR isolation checks, finalize metadata to 85, merge, and update this handoff plus the locale plan.

Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
