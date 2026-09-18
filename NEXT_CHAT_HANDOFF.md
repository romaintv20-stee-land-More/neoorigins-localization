# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-14
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything.
- Use `release/1.0.0` as the source-of-truth integration branch.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Work one locale at a time through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, PR, and integration.
- Automated/generative translation assistance is used; never claim native-speaker review unless one actually occurred.
- Do not bump public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue and final global release gates are complete.
- Never use isolated-word projection to build mixed English/target-language sentences. Prefer safe manual full values, exact corpus full-string matches, then direct full automatic translation of remaining English.

## Completed integration baseline

The first **88 selected locales are complete and integrated** into `release/1.0.0`, through **#88 Interslavic — `isv / Medžuslovjansky`**.

Recent integrated languages:
- #84 Gallo — `go_fr / Galo`
- #85 Manx — `gv_im / Gaelg`
- #86 Hawaiian — `haw_us / ʻŌlelo Hawaiʻi`
- #87 Ido — `io_en / Ido`
- #88 Interslavic — `isv / Medžuslovjansky`

The catalogue and README are at **88 locales**. There are **25 selected locales remaining** for 1.0.0. The authoritative queue is `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Interslavic #88 — final references

- staging branch: `release/1.0.0-interslavic`
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`, file `java/isv.json`
- bootstrap run: `34777502902` — successful
- bootstrap structure: **29 `isv` source files** = 16 common chunks + `neoorigins_isv_121` + two 26.x deltas + 10 add-ons
- refinement model: `salavat/nllb-200-distilled-600M-finetuned-isv_v2`, direct `eng_Latn` → `isv_Latn`
- final refinement run: `34777854565` — successful
- generated translation commit: `f7a79133060eaf4058d4f29ea2aa669839e3ec6f`
- strict JSON, source-key, placeholder, upstream-overlap and protected-token gates passed; no isolated-word projection
- build run: `34893764953` — successful, packaged **27 / 17 / 17** `isv` files with correct add-on/version-delta isolation
- final staging metadata commit: `cd7805cec57dee509680e055980cfeb72418a586`
- metadata: 88 supported locales, `isv` across all 11 projects, `interslavic_common_glob = neoorigins_isv_common_*`, `interslavic_mc_1_21_1 = neoorigins_isv_121`
- integration PR: `#25`
- integration merge commit: `b4efe78fe46513a582ce36403cf746625b6dcecb`
- locale-plan advancement commit: `a78979ae8814f87118822ec1bac49a594d2ab31c`
- Interslavic remains machine-generated; no native-speaker review is claimed

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

Start and finish **#89 Kabyle (`kab_kab`)** from the current `release/1.0.0` branch. Inspect the pinned `java/kab_kab.json` corpus first. English remains the semantic source. Prefer safe manual full values and exact whole-string Minecraft corpus matches, then direct full-string English → Kabyle translation for the remaining strings with a model that genuinely targets Kabyle. Preserve placeholders and technical/project tokens, run strict audits, then validate **27 / 17 / 17** packaging, metadata, PR, and integration.

Low German (`nds_de`) remains selected but explicitly deferred until a translation path that genuinely targets Low German is available.
