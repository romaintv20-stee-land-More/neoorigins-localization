# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-11
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything.
- Use `release/1.0.0` as the source-of-truth integration branch for the ongoing 1.0.0 cycle.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Continue each locale through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, and integration.
- Automated/generative translation assistance is used; do not describe generated locales as fully native-speaker-reviewed unless a real native review occurred.
- Do not bump the public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue is finished and the final global release gates pass.

## Completed language baseline

The first **78 selected locales are complete and integrated**.

Latest completed languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**

The catalogue and README are at **78 locales**. There are **35 selected locales remaining** for 1.0.0; the authoritative queue and exclusion policy are in `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Northern Sami final references

- staging branch: `release/1.0.0-northern-sami`
- refined source commit: `5b2190d7fc0d259ed8cd80f3ab06dc8575dd89f1`
- build workflow source commit: `c2a009303ee0eba843f7a21a4269a0ac098e4cc9`
- build run: `34590740817` — successful on all three targets
- build jobs:
  - 1.21.1: `103235214321`
  - 26.1.x: `103235214660`
  - 26.2: `103235214603`
- packaged Northern Sami file counts:
  - 1.21.1: 27
  - 26.1.x: 17
  - 26.2: 17
- build artifacts:
  - 1.21.1: `10195568704`
  - 26.1.x: `10195550884`
  - 26.2: `10195550128`
- metadata run/job: `34591141087` / `103236468908` — successful
- metadata integration also finalized pending Traditional Chinese (`zh_tw`) metadata and moved the project count 76 → 78
- integration PR: `#15`
- integration commit on `release/1.0.0`: `af8250dd2a3e122eacdae1812f3089db83637dda`

Do not redo Northern Sami or Traditional Chinese metadata.

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #79** from `release/1.0.0`. The first locale in the current queue is **Bavarian (`bar`)**.

Follow the full established flow and integrate only after all audits/build/JAR gates pass. Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
