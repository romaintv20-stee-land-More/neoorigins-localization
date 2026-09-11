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

The first **80 selected locales are complete and integrated**.

Latest completed languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**
- **#79 Bavarian — `bar / Boarisch`**
- **#80 Brabantian — `brb / Braobans`**

The catalogue and README are at **80 locales**. There are **33 selected locales remaining** for 1.0.0; the authoritative queue and exclusion policy are in `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Brabantian final references

- staging branch: `release/1.0.0-brabantian`
- validated build source: `7bd19fa2bebbffd8638333e1845fb57cef653c88`
- build run: `34634057893` — successful on all three targets
- packaged Brabantian file counts:
  - 1.21.1: 27
  - 26.1.x: 17
  - 26.2: 17
- bootstrap source strategy: complete local Dutch semantic coverage + pinned Minecraft `nl_nl` ↔ `brb` corpus, with contaminated/suspicious pairs filtered and singleton learned transformations rejected
- contextual refinements: `Human` → `Mens`; edit UI label → `Beweireke`
- metadata run: `34634337318` — successful
- final metadata commit: `2dc089e9c9330cb923a0128e1fdc38da53858e71`
- integration PR: `#17`
- integration commit on `release/1.0.0`: `7c358f40c6b55af42d9ac1d17c1f8a774e4ce05a`

Do not redo Brabantian, Bavarian, Northern Sami, or Traditional Chinese metadata.

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #81 — Andalusian (`esan`)** from the current `release/1.0.0` branch.

Follow the full established flow and integrate only after all audits/build/JAR gates pass. Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
