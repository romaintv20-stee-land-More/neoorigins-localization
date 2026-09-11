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

The first **82 selected locales are complete and integrated**.

Latest completed languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**
- **#79 Bavarian — `bar / Boarisch`**
- **#80 Brabantian — `brb / Braobans`**
- **#81 Andalusian — `esan / Andalûh`**
- **#82 East Franconian — `fra_de / Fränggisch`**

The catalogue and README are at **82 locales**. There are **31 selected locales remaining** for 1.0.0; the authoritative queue and exclusion policy are in `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## East Franconian final references

- staging branch: `release/1.0.0-east-franconian`
- bootstrap run: `34637339952`
- bootstrap commit: `dccecd0` — 29 `fra_de` source locale files generated
- source strategy: complete German semantic coverage plus pinned Minecraft `de_de` ↔ `fra_de` corpus; suspicious/untranslated corpus pairs are rejected
- bootstrap corpus metrics: 8,557 aligned entries, 3,252 suspicious/untranslated pairs rejected, 4,804 exact dialect strings, 205 initial learned mappings
- contextual QA detected over-aggressive projections such as `teleboadiead`, `Phandom`, `Schdandard`, and `Schlieaßa`
- safe refinement run: `34638832312` — successful
- safe refinement commit: `6342645`
- refinement regenerated all 3,583 values, changed 526 bootstrap outputs, retained 415 dialect markers, and left zero known unsafe projection patterns
- strict NeoOrigins audits passed at 2,296/2,296 keys on 1.21.1 and 2,307/2,307 on both 26.x targets; all 10 compatible 1.21.1 add-on audits passed; overlaps and placeholder errors are zero
- build run: `34638996305` — successful on all three targets
- packaged East Franconian file counts:
  - 1.21.1: 27
  - 26.1.x: 17
  - 26.2: 17
- JAR isolation checks passed for 1.21.1 add-ons and all version-specific deltas
- metadata run: `34639226494` — successful
- final branch metadata commit: `43dfc1edda0ffca03b15cdb79b1688a676f79220`
- native metadata/catalog name: `Fränggisch`
- integration PR: `#19`
- integration commit on `release/1.0.0`: `bbf3d9144b45436300dcd3cd8fe5b43514296f12`

Do not redo East Franconian, Andalusian, Brabantian, Bavarian, Northern Sami, or Traditional Chinese metadata.

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #83 — Friulian (`fur_it`)** from the current `release/1.0.0` branch.

Follow the full established flow and integrate only after all audits/build/JAR gates pass. Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
