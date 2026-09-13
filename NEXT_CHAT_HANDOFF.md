# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-13
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything. For the current 1.0.0 language-expansion state, this file and the locale plan supersede older 0.9.0 status text still present in `PROJECT_HANDOFF.txt`.
- Use `release/1.0.0` as the source-of-truth integration branch.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Work one locale at a time and continue it through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, PR, and integration.
- Automated/generative translation assistance is used; never claim native-speaker review unless one actually occurred.
- Do not bump public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue and final global release gates are complete.
- Never use isolated-word projection to build mixed English/target-language sentences. Prefer safe manual full values, exact corpus full-string matches, then direct full automatic translation of remaining English.

## Completed integration baseline

The first **87 selected locales are complete and integrated** into `release/1.0.0`, through **#87 Ido — `io_en / Ido`**.

Recent integrated languages:
- #83 Friulian — `fur_it / Furlan`
- #84 Gallo — `go_fr / Galo`
- #85 Manx — `gv_im / Gaelg`
- #86 Hawaiian — `haw_us / ʻŌlelo Hawaiʻi`
- #87 Ido — `io_en / Ido`

The catalogue and README are at **87 locales**. There are **26 selected locales remaining** for 1.0.0. The authoritative queue is `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Ido #87 — final references

- staging branch: `release/1.0.0-ido`
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`, file `java/io_en.json`
- generated layout: 16 common chunks + `neoorigins_io_121` + shared 26.x deltas + 10 add-ons = **29 `io_en` source files**
- completion path: safe manual full values, exact Minecraft Ido whole-string matches, then direct English → Ido translation with `Helsinki-NLP/opus-mt-en-mul` (Apache-2.0), target prefix `>>ido<<`
- no isolated-word projection; placeholders and technical/project names protected; `Origin Architect` intentionally preserved
- bootstrap run: `34747547429` — successful
- final refinement run: `34771622691` — successful
- generated translation commit: `fc7da509b430c517fc5a5e4d05e8c7d0751162af`
- strict JSON, key, placeholder, upstream-overlap and protected-token gates passed across all 29 files
- build trigger commit: `e37817e620f047ee0cbc3c7b7445f2977f92c3ce`
- build run: `34772475271` — successful
- JAR inspection results:
  - 1.21.1: **27** `io_en` files, delta `neoorigins_io_121`, 10 add-ons present
  - 26.1.x: **17** `io_en` files, delta `neoorigins_26_1`, no 1.21.1 add-ons
  - 26.2: **17** `io_en` files, delta `neoorigins_26_2`, no 1.21.1 add-ons
- metadata run: `34777236473` — successful
- final metadata commit: `dddc9c896bc232044d50e5750d36d466c6e3bc96`
- metadata final state: 87 supported locales, `io_en` across all 11 projects, native/French name `Ido`
- fallback namespaces: `ido_common_glob = neoorigins_io_common_*`; `ido_mc_1_21_1 = neoorigins_io_121`
- build workflow restored to manual-only after validation
- integration PR: `#24`
- integration merge commit: `d97d72b298950982fd10f32fd2354dcb210ec4b0`
- locale-plan advancement commit: `500ad7a498c6328e22f0a32e8168165a3c6e2c0d`
- Ido remains machine-generated; no native-speaker review is claimed
- public build version remains `0.9.0-beta`

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

Pinned Minecraft locale corpus:
- repository: `teaSummer/minecraft-locales`
- ref: `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- Java locale files: `java/<locale>.json`

The 1.21.1 build supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #88 — Interslavic (`isv`)** from the current `release/1.0.0` integration branch. First inspect the pinned Minecraft `isv` corpus and verify a reliable full-string automatic-translation path before generating anything. Keep exact corpus matches ahead of direct full-string translation and preserve all technical tokens/placeholders.

Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that genuinely targets Low German is available.
